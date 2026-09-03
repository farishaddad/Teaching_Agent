# Chapter 3: Building the RAG Pipeline

## What is RAG?

**Retrieval-Augmented Generation (RAG)** is the technique of retrieving relevant information from a knowledge base and providing it as context to an LLM — so the model answers from your data, not from its general training.

```
Without RAG:  Student asks → LLM answers from general knowledge (may hallucinate)
With RAG:     Student asks → Retrieve relevant course docs → LLM answers from THOSE docs
```

**Why it matters for a teaching agent:**
- Answers are grounded in YOUR course content (not internet noise)
- You can cite specific slides, pages, and modules
- When course content updates, the agent's knowledge updates too (re-ingest)
- Hallucination is dramatically reduced

---

## How Amazon Bedrock Knowledge Bases Work

```
┌────────────────────────────────────────────────────────────┐
│                    INGESTION (One-time setup)               │
│                                                            │
│  Course PDFs/Slides → S3 Bucket → Bedrock KB ingests:      │
│    1. Chunk documents into passages                        │
│    2. Generate embeddings (Titan Embeddings v2)            │
│    3. Store in OpenSearch Serverless vector index          │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│                 QUERY TIME (Every student question)         │
│                                                            │
│  Student: "What is tool use in AI agents?"                 │
│    1. Embed the question                                   │
│    2. Vector search: find the most similar chunks          │
│    3. Pass chunks + question to Claude                     │
│    4. Claude synthesizes an answer FROM those chunks       │
│    5. Return answer + source citations                     │
└────────────────────────────────────────────────────────────┘
```

---

## How the KB fits our stack (important)

The `TeachingAgentRAG` CDK stack creates **only the S3 materials bucket**. The Knowledge Base + OpenSearch Serverless collection are created **out-of-band** (Bedrock console or `scripts/create_kb.sh`), because Bedrock's console flow handles the fiddly AOSS index/permission setup for you.

So how does the Lambda learn the KB's ID? Through **SSM Parameter Store**:

```
create KB (console or scripts/create_kb.sh)
        │  the script writes the KB ID to SSM:
        │  /teaching-agent/{env}/bedrock-kb-id
        ▼
CDK synth reads it: ssm.StringParameter.value_from_lookup(...)   (in app.py)
        │  stamps the literal ID into the API stack template
        ▼
Lambda env var  BEDROCK_KB_ID = <real KB id>
        │
        ▼
backend/rag/knowledge_base.py reads BEDROCK_KB_ID at runtime
```

`value_from_lookup` embeds the resolved ID as a literal into the synthesized template (so there's no CloudFormation drift), and it's bootstrap-safe: before the parameter exists, it resolves to an empty string and RAG degrades gracefully instead of blocking the deploy. See [Chapter 6](./06-deployment.md) for the full flow.

---

## Step 1: Prepare Course Materials

Upload your materials to the S3 bucket the RAG stack creates. Supported formats: PDF, TXT, MD, DOCX, HTML.

```
course_materials/
├── module_01_...md / .pdf
├── module_02_...md / .pdf
├── ...
└── references/ , guides/ , ...
```

`scripts/upload_to_s3.sh` handles uploading the course tree (and can convert slide decks to PDF for better chunking).

**Chunking tips:** fixed-size chunks around 500 tokens with ~20% overlap work well for slide decks. Overlap matters — without it, a concept split across two chunks leaves neither chunk with the full explanation.

---

## Step 2: CDK — The Materials Bucket (KB created out-of-band)

```python
# infrastructure/rag_stack.py (the whole stack, essentially)

class TeachingAgentRAGStack(Stack):
    def __init__(self, scope, construct_id, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # S3 bucket for course materials (account-suffixed for global uniqueness)
        self.materials_bucket = s3.Bucket(
            self, "CourseMaterials",
            bucket_name="teaching-agent-materials-062788795053",
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            enforce_ssl=True,
            removal_policy=RemovalPolicy.RETAIN,
            auto_delete_objects=False,
        )

        # The Bedrock KB itself is NOT created here — see the NextStep output.
        self.knowledge_base_id = ""   # populated at runtime via SSM, not CDK

        CfnOutput(self, "NextStep", value=(
            "Create the Bedrock KB (console or scripts/create_kb.sh) pointing "
            "to this S3 bucket, store the KB ID in SSM at "
            "/teaching-agent/{env}/bedrock-kb-id, then run: cdk deploy TeachingAgentAPI"
        ))
```

**Console/script setup:**
1. Bedrock Console → Knowledge Bases → Create (or run `scripts/create_kb.sh`)
2. Data source: the `teaching-agent-materials-<account>` S3 bucket
3. Embeddings: Amazon Titan Embeddings V2
4. Vector store: OpenSearch Serverless (auto-created)
5. Chunking: Fixed size, ~500 tokens, 20% overlap
6. Sync the data source → ingestion starts
7. **Store the KB ID in SSM** (`create_kb.sh` does this automatically) and redeploy `TeachingAgentAPI`

---

## Step 3: System Prompt Design

The system prompt (in `backend/rag/prompt_templates.py`) constrains the agent's behavior — establishing its identity and grounding rules before Bedrock Guardrails add enforcement. It instructs the model to answer only from retrieved course materials, decline when nothing relevant is found, and cite sources inline as `[Source: filename]`.

---

## Step 4: Two Retrieval Modes

`backend/rag/knowledge_base.py` supports **two** paths:

**A) `retrieve_and_generate`** — one Bedrock call that retrieves and generates together. Simple; used for straightforward Q&A.

```python
# Uses the ManagedSearchConfiguration shape for a managed KB.
kb_config = {
    "knowledgeBaseId": KNOWLEDGE_BASE_ID,
    "modelArn": MODEL_ARN,
    "generationConfiguration": {
        "promptTemplate": {"textPromptTemplate": "...$search_results$...$query$..."},
        "inferenceConfig": {"textInferenceConfig": {
            "maxTokens": 1024, "temperature": 0.2, "topP": 0.9,
        }},
    },
    "retrievalConfiguration": {
        "managedSearchConfiguration": {"numberOfResults": 5},
    },
}
# If a guardrail is configured, it's attached here:
if GUARDRAIL_ID:
    kb_config["generationConfiguration"]["guardrailConfiguration"] = {
        "guardrailId": GUARDRAIL_ID, "guardrailVersion": GUARDRAIL_VERSION,
    }

response = bedrock_agent_runtime.retrieve_and_generate(
    input={"text": query},
    retrieveAndGenerateConfiguration={
        "type": "KNOWLEDGE_BASE",
        "knowledgeBaseConfiguration": kb_config,
    },
    # sessionId carries conversation continuity across turns
)
```

**B) `retrieve` + Converse** — `retrieve()` returns raw chunks only (no `retrievalConfiguration` — the managed KB uses its own defaults), and `chat_handler` then formats them into a **Converse** API call with guardrails and conversation history applied explicitly. This is the preferred path for guardrail transparency and multi-turn control.

> **Configuration reality:**
> - The KB ID comes from `os.environ["BEDROCK_KB_ID"]`, with a fallback to `BEDROCK_KNOWLEDGE_BASE_ID`.
> - `MODEL_ARN` comes from the `BEDROCK_MODEL_ARN` env var, currently **Claude Sonnet 4.5** via the EU cross-region inference profile (`eu.anthropic.claude-sonnet-4-5-20250929-v1:0`). ⚠️ Older Claude 3.x models (including the original Haiku default) are now **Legacy** on Bedrock and reject Converse with `ResourceNotFoundException` — always point this at an ACTIVE model. Also note newer Claude models reject setting both `temperature` and `topP` in one call, so the code sets only `temperature`.
> - If `BEDROCK_KB_ID` is empty (KB not yet created / SSM param unset), retrieval logs `knowledge_base_id_not_configured` and returns a safe fallback instead of erroring.

---

## Step 5: Handling Citations

Students need to know WHERE the answer came from. The code turns Bedrock's citation format into readable source references (filename + excerpt) pulled from each retrieved reference's `s3Location`. The frontend then shows something like:

> "RAG stands for Retrieval-Augmented Generation..."
>
> 📚 *Sources: module_03_prompt_engineering.md, module_07_rag.md*

---

## Chunking Deep Dive

| Strategy | Chunk Size | Best For |
|----------|-----------|----------|
| Small (200 tokens) | Precise, focused | Q&A with specific answers |
| Medium (500 tokens) | Balanced | Most use cases ✓ |
| Large (1000 tokens) | More context | Complex explanations |
| Semantic | Variable | Documents with clear sections |

**Overlap matters**: 20% overlap means the end of chunk N appears at the start of chunk N+1, so concepts spanning a boundary aren't lost. Because the KB is created out-of-band, these settings are chosen at KB-creation time (console/script), not in CDK.

---

## Common Pitfalls

1. **KB ID not in SSM**: created the KB but forgot to store its ID at `/teaching-agent/{env}/bedrock-kb-id`, so `BEDROCK_KB_ID` is empty and RAG silently degrades.
2. **Stale index**: updated materials but forgot to re-sync the data source. The admin **Sync Knowledge Base** button ([Chapter 8](./08-course-materials.md)) triggers this from the UI.
3. **Poor chunking**: chunks that split concepts mid-sentence.
4. **No fallback**: agent tries to answer even when retrieval finds nothing relevant (handled here by `FALLBACK_RESPONSE`).
5. **Legacy model**: pointing `BEDROCK_MODEL_ARN` at a retired Claude 3.x model — Converse then fails and the chat returns a generic error.

---

## Next Chapter

In [Chapter 4: Implementing Guardrails](./04-guardrails.md), we'll add the safety layer that prevents off-topic answers, blocks harmful content, and catches hallucinations.
