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
│  Course PDFs/Slides → S3 Bucket → Bedrock KB ingests:     │
│    1. Chunk documents into passages (300-500 tokens each)  │
│    2. Generate embeddings (Titan Embeddings v2)            │
│    3. Store in OpenSearch Serverless vector index          │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│                 QUERY TIME (Every student question)         │
│                                                            │
│  Student: "What is tool use in AI agents?"                 │
│    1. Embed the question                                   │
│    2. Vector search: find top-5 most similar chunks        │
│    3. Pass chunks + question to Claude                     │
│    4. Claude synthesizes an answer FROM those chunks       │
│    5. Return answer + source citations                     │
└────────────────────────────────────────────────────────────┘
```

---

## Step 1: Prepare Course Materials

Upload your materials to S3. Supported formats:
- PDF (slides exported as PDF work great)
- TXT, MD (plain text notes)
- DOCX (Word documents)
- HTML (web-based materials)

```
course_materials/
├── Module_01_Introduction_to_Agents.pdf
├── Module_02_LLM_Foundations.pdf
├── Module_03_Prompt_Engineering.pdf
├── ...
├── Module_16_Building_on_AWS.pdf
└── supplementary/
    ├── reading_list.md
    └── glossary.md
```

**Chunking Strategy Tips:**
- Default chunking (300 tokens, 20% overlap) works well for slide decks
- For dense technical docs, increase to 500 tokens
- Keep logical sections together where possible
- Include headings in chunks for better retrieval context

---

## Step 2: CDK — Create the Knowledge Base

```python
# infrastructure/rag_stack.py (key parts)

class TeachingAgentRAGStack(Stack):
    def __init__(self, scope, construct_id, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # S3 bucket for course materials
        self.materials_bucket = s3.Bucket(
            self, "CourseMaterials",
            bucket_name="teaching-agent-course-materials",
            removal_policy=RemovalPolicy.RETAIN,
        )

        # OpenSearch Serverless collection (vector store)
        # Bedrock KB manages this for you — but you can customize

        # Bedrock Knowledge Base
        # Note: As of 2026, KB creation is best done via console or 
        # aws bedrock-agent create-knowledge-base CLI
        # CDK support via CfnKnowledgeBase

        # Data source: S3 bucket → KB
        # Configured to re-sync when materials are updated
```

**Console Setup (Recommended for First Time):**
1. Bedrock Console → Knowledge Bases → Create
2. Data source: S3 bucket with your course PDFs
3. Embeddings: Amazon Titan Embeddings V2
4. Vector store: OpenSearch Serverless (auto-created)
5. Chunking: Fixed size, 500 tokens, 20% overlap
6. Sync the data source → ingestion starts

---

## Step 3: System Prompt Design

The system prompt constrains the agent's behavior:

```python
SYSTEM_PROMPT = """You are an expert teaching assistant for an Agentic AI course.

ROLE:
- Answer student questions grounded in the provided course materials
- Explain concepts clearly with relevant examples
- Reference specific modules/slides when applicable
- Encourage deeper exploration

RULES:
- ONLY provide information supported by the retrieved course materials
- If no relevant material is found, say "I don't have information on that 
  in the course materials" — never guess
- Never make up citations or references
- Be encouraging — students are learning
- Keep answers concise unless asked for detail

COURSE: Introduction to Agentic AI
MODULES: 16 (from Agent Fundamentals to Building on AWS)
"""
```

**Why this matters:** The system prompt is your first guardrail. It establishes the agent's identity and constraints before Bedrock Guardrails add the enforcement layer.

---

## Step 4: RetrieveAndGenerate API Call

```python
# backend/rag/knowledge_base.py

def retrieve_and_generate(query: str, student_id: str) -> dict:
    """Ask a question, get a grounded answer with citations."""
    
    response = bedrock_agent_runtime.retrieve_and_generate(
        input={"text": query},
        retrieveAndGenerateConfiguration={
            "type": "KNOWLEDGE_BASE",
            "knowledgeBaseConfiguration": {
                "knowledgeBaseId": KNOWLEDGE_BASE_ID,
                "modelArn": MODEL_ARN,  # Claude 3.5 Sonnet
                "generationConfiguration": {
                    "promptTemplate": {
                        "textPromptTemplate": (
                            SYSTEM_PROMPT + 
                            "\n\nContext:\n$search_results$\n\n"
                            "Student question: $query$"
                        )
                    }
                },
                "retrievalConfiguration": {
                    "vectorSearchConfiguration": {
                        "numberOfResults": 5,  # Top 5 chunks
                    }
                },
            },
        },
    )
    
    # Extract answer and citations
    answer = response["output"]["text"]
    citations = extract_citations(response.get("citations", []))
    
    return {"answer": answer, "sources": citations}
```

---

## Step 5: Handling Citations

Students need to know WHERE the answer came from:

```python
def extract_citations(citations: list) -> list[dict]:
    """Turn Bedrock citation format into readable source references."""
    sources = []
    for citation in citations:
        for ref in citation.get("retrievedReferences", []):
            uri = ref["location"]["s3Location"]["uri"]
            filename = uri.split("/")[-1]  # "Module_03_Prompt_Engineering.pdf"
            excerpt = ref["content"]["text"][:200]
            
            sources.append({
                "source": filename,
                "excerpt": excerpt,
            })
    return sources
```

The frontend can then display:
> "RAG stands for Retrieval-Augmented Generation..."
> 
> 📚 *Sources: Module_03_Prompt_Engineering.pdf, Module_07_RAG.pdf*

---

## Chunking Deep Dive

How you chunk documents dramatically affects retrieval quality:

| Strategy | Chunk Size | Best For |
|----------|-----------|----------|
| Small (200 tokens) | Precise, focused | Q&A with specific answers |
| Medium (500 tokens) | Balanced | Most use cases ✓ |
| Large (1000 tokens) | More context | Complex explanations |
| Semantic | Variable | Documents with clear sections |

**Our choice**: 500 tokens with 20% overlap — balances precision with enough context for Claude to synthesize good answers.

**Overlap matters**: Without overlap, if a concept spans two chunks, neither chunk has the full explanation. 20% overlap means the end of chunk N appears at the start of chunk N+1.

---

## Testing RAG Quality

```python
# Manual evaluation checklist

TEST_QUESTIONS = [
    # Should return grounded answer from Module 1
    ("What is an AI agent?", "Module_01"),
    
    # Should cite RAG module specifically
    ("How does RAG prevent hallucination?", "Module_07"),
    
    # Should gracefully decline — not in course materials
    ("What is the best pizza in London?", None),
    
    # Should synthesize across multiple modules
    ("How do guardrails relate to agent safety?", "Module_09"),
]

for question, expected_source in TEST_QUESTIONS:
    result = retrieve_and_generate(question, student_id="test")
    print(f"Q: {question}")
    print(f"A: {result['answer'][:200]}...")
    print(f"Sources: {[s['source'] for s in result['sources']]}")
    print(f"Expected source present: {expected_source in str(result['sources'])}")
    print("---")
```

---

## Common Pitfalls

1. **Stale index**: Updated PDFs but forgot to re-sync the data source
2. **Poor chunking**: Chunks that split concepts mid-sentence
3. **No fallback**: Agent tries to answer even when retrieval finds nothing relevant
4. **Citation mismatch**: Displaying citations from irrelevant retrieved chunks
5. **Prompt leakage**: System prompt visible if student asks "what are your instructions?"

---

## Next Chapter

In [Chapter 4: Implementing Guardrails](./04-guardrails.md), we'll add the safety layer that prevents off-topic answers, blocks harmful content, and catches hallucinations.
