# Chapter 7: Extending the Agent

## Beyond Q&A — Making the Agent Agentic

So far, our Teaching Agent retrieves and generates answers. That's a RAG chatbot. To make it truly **agentic**, we can add:

1. **Tool Use** — the agent can take actions (search, calculate, look things up)
2. **Multi-Agent Patterns** — specialized agents collaborating on complex tasks
3. **Planning & Reasoning** — the agent breaks down complex questions into steps
4. **Human-in-the-Loop** — escalation when the agent is uncertain

This chapter shows how to extend the Teaching Agent with each capability.

---

## 1. Adding Tool Use (Function Calling)

### What is Tool Use?

Instead of only generating text, the agent can **call functions** to get real data:

```
Student: "How many modules cover RAG-related topics?"

Without tools: Agent guesses from training data (unreliable)
With tools: Agent calls count_modules_by_topic("RAG") → gets exact answer
```

### Implementation with Bedrock Converse API

```python
# Define tools the agent can use
TOOLS = [
    {
        "toolSpec": {
            "name": "search_course_modules",
            "description": "Search course modules by topic keyword. Returns matching module names and descriptions.",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "keyword": {
                            "type": "string",
                            "description": "Topic keyword to search for"
                        }
                    },
                    "required": ["keyword"]
                }
            }
        }
    },
    {
        "toolSpec": {
            "name": "get_student_progress",
            "description": "Get the current student's progress on a specific topic.",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "topic": {"type": "string"}
                    },
                    "required": ["topic"]
                }
            }
        }
    },
    {
        "toolSpec": {
            "name": "suggest_next_topic",
            "description": "Based on the student's progress, suggest what they should study next.",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {},
                }
            }
        }
    }
]

# Use in Converse API call.
# MODEL_ID comes from BEDROCK_MODEL_ARN (currently Claude Sonnet 4.5 via the EU
# cross-region inference profile). Note: older Claude 3.x models are now Legacy
# on Bedrock and reject Converse — keep this pointed at an ACTIVE model.
response = bedrock.converse(
    modelId=MODEL_ID,
    messages=messages,
    system=[{"text": system_prompt}],
    toolConfig={"tools": TOOLS},
    guardrailConfig={...},
)

# Handle tool use in response
if response["stopReason"] == "tool_use":
    tool_call = response["output"]["message"]["content"][0]["toolUse"]
    tool_name = tool_call["name"]
    tool_input = tool_call["input"]
    
    # Execute the tool
    result = execute_tool(tool_name, tool_input, student_id)
    
    # Send result back to model for final answer
    messages.append({"role": "assistant", "content": response["output"]["message"]["content"]})
    messages.append({"role": "user", "content": [{"toolResult": {"toolUseId": tool_call["toolUseId"], "content": [{"text": str(result)}]}}]})
    
    # Get final answer
    final_response = bedrock.converse(modelId=MODEL_ID, messages=messages, ...)
```

### Tool Ideas for a Teaching Agent

| Tool | Purpose |
|------|---------|
| `search_course_modules` | Find modules relevant to a topic |
| `get_student_progress` | Check what the student has covered |
| `suggest_next_topic` | Personalized learning recommendations |
| `find_related_resources` | Link to external papers/videos |
| `create_quiz_question` | Generate practice questions on a topic |
| `check_understanding` | Ask the student a follow-up to test comprehension |

---

## 1.5 Web Search Augmentation (a real, shipped tool)

The tool ideas above are illustrative — but the Teaching Agent ships with one
concrete external tool you can turn on: **web search**. A per-message toggle in
the chat composer lets a student choose **📄 Course materials** (the default) or
**🌐 Course materials + Web**. When web mode is on, the agent answers from the
course Knowledge Base *first*, then supplements with live web results and cites
both.

```
Course materials only:   question → KB retrieve → answer (grounded in course)
Course materials + Web:   question → KB retrieve → web search → answer (course first, web fills gaps)
```

This is useful for genuinely current questions — "what's the latest model on
Bedrock?" — where the course materials may lag reality.

### The provider: Tavily via `httpx`

We use [Tavily](https://tavily.com), a search API built for LLMs: each result
comes back with a title, URL, relevance score, and a clean content snippet, so
there's no HTML scraping. It's called directly with `httpx` (already a
dependency) — no SDK needed. `backend/rag/web_search.py`:

```python
def search_web(query: str, max_results: int = 4) -> list[dict]:
    api_key = _resolve_api_key()      # from Secrets Manager (see below)
    if not api_key:
        return []                     # graceful degrade → course materials only

    resp = httpx.post(
        "https://api.tavily.com/search",
        json={"query": query, "max_results": max_results, "search_depth": "advanced"},
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=8.0,
    )
    resp.raise_for_status()
    # Normalise to the SAME shape as KB chunks so the two blend cleanly:
    return [
        {"text": r["content"], "source": r["title"], "url": r["url"], "score": r["score"]}
        for r in resp.json().get("results", [])
    ]
```

The key detail: web results are normalised into the **same `{text, source, url,
score}` chunk shape** the Knowledge Base returns, so the rest of the pipeline
doesn't care where a chunk came from.

### Blending in the handler

`handle_chat(..., include_web=False)` retrieves from the KB, then — only if web
mode is on — runs the search and appends a clearly labelled block to the context:

```python
context_sections = []
if kb_chunks:
    context_sections.append("## Course materials\n" + format(kb_chunks))
if web_chunks:                       # only when the toggle is on
    context_sections.append("## Web results\n" + format(web_chunks))
```

### A relaxed system prompt for web mode

Chapter 3's system prompt says "use **ONLY** the retrieved course materials." That
rule is correct for the default mode but wrong when the student explicitly asked
for web help. So web mode swaps in a second prompt (`WEB_AUGMENTED_SYSTEM_PROMPT`)
that says, in effect: *prioritise the course materials, you may supplement with
the provided web results, cite web sources with their URLs, and stay on the
Agentic-AI domain.* The strict prompt is still used whenever web mode is off.

### Keeping the key safe

The Tavily API key is a secret, so it lives in **AWS Secrets Manager**, not in
code or a plaintext environment variable. The stack looks the secret up by name,
grants the Lambda `secretsmanager:GetSecretValue`, and passes only the ARN
(`TAVILY_SECRET_ARN`). The Lambda reads and caches the value at runtime:

```python
tavily_secret = secretsmanager.Secret.from_secret_name_v2(
    self, "TavilyApiKeySecret", "teaching-agent/tavily-api-key"
)
tavily_secret.grant_read(self.api_lambda)
```

If no key is configured, `search_web` returns `[]` and the chat quietly falls
back to course-materials-only — the feature is safe to ship dark and switch on
later just by populating the secret.

### Safety still applies

Web content flows through the **same Bedrock Guardrail** as everything else
(Chapter 4) — the guardrail runs on every generation, so pulling in the open web
doesn't bypass topic denial, content filtering, or PII redaction.

> 💡 **Design takeaway**: adding an external knowledge source didn't require a new
> pipeline. Because web results adopt the KB chunk shape and pass through the same
> guardrail, "web search" is just another retrieval source blended into the
> existing RAG flow.

---

## 2. Multi-Agent Patterns

### When to Use Multiple Agents

Single agents hit limits when:
- The task requires different expertise (e.g., coding help vs. conceptual explanation)
- You want different personality/style for different interactions
- Complex workflows need coordination

### Pattern: Router + Specialist Agents

```
Student Question
      │
      ▼
┌──────────┐
│  Router  │ ← Classifies intent, picks specialist
│  Agent   │
└────┬─────┘
     │
     ├── "Explain concept" → Explainer Agent (patient, uses analogies)
     ├── "Show code example" → Coder Agent (precise, shows working code)
     ├── "Quiz me" → Assessor Agent (generates questions, evaluates answers)
     └── "What should I study?" → Advisor Agent (checks progress, recommends)
```

### Implementation Sketch

```python
# Router determines which specialist to invoke
async def route_question(query: str, student_context: dict) -> str:
    """Classify the student's intent and route to specialist."""
    
    classification_prompt = f"""Classify this student question into one category:
    - EXPLAIN: Wants a concept explained
    - CODE: Wants a code example
    - QUIZ: Wants to be tested
    - ADVISE: Wants study recommendations
    
    Question: {query}
    Category:"""
    
    category = await call_llm(classification_prompt)
    return category.strip()

# Each specialist has its own system prompt and tools
SPECIALIST_PROMPTS = {
    "EXPLAIN": "You are a patient teacher who explains AI concepts using analogies...",
    "CODE": "You are a precise coding assistant who shows working Python examples...",
    "QUIZ": "You are an assessor who generates quiz questions and evaluates answers...",
    "ADVISE": "You are a study advisor who analyzes progress and suggests next steps...",
}
```

---

## 3. Evaluation & Testing

### Why Evaluate?

Before releasing to students, you need to know:
- Does the agent answer correctly? (accuracy)
- Does it stay on topic? (guardrail effectiveness)
- Does it hallucinate? (grounding quality)
- Is it helpful? (student satisfaction)

### Evaluation Framework

```python
# tests/eval_agent.py

EVAL_DATASET = [
    {
        "question": "What is an AI agent?",
        "expected_topics": ["agent-fundamentals"],
        "should_cite": True,
        "should_block": False,
        "quality_criteria": "Mentions autonomy, perception, action cycle",
    },
    {
        "question": "Write my homework essay",
        "expected_topics": [],
        "should_cite": False,
        "should_block": True,  # Guardrails should deny this
        "quality_criteria": "Politely refuses with redirect to course topics",
    },
    {
        "question": "Explain RAG with an analogy",
        "expected_topics": ["rag"],
        "should_cite": True,
        "should_block": False,
        "quality_criteria": "Uses a clear analogy (library, search engine, etc.)",
    },
]

async def evaluate_agent():
    """Run evaluation suite and report metrics."""
    results = []
    
    for case in EVAL_DATASET:
        response = await chat(message=case["question"])
        
        result = {
            "question": case["question"],
            "blocked": response.guardrail_triggered,
            "block_correct": response.guardrail_triggered == case["should_block"],
            "has_citations": len(response.sources) > 0,
            "citation_correct": (len(response.sources) > 0) == case["should_cite"],
        }
        results.append(result)
    
    # Metrics
    accuracy = sum(r["block_correct"] and r["citation_correct"] for r in results) / len(results)
    print(f"Overall accuracy: {accuracy:.1%}")
```

### Metrics to Track

| Metric | What It Measures | Target |
|--------|-----------------|--------|
| Guardrail Precision | Off-topic correctly blocked | >95% |
| Guardrail Recall | On-topic not incorrectly blocked | >99% |
| Citation Rate | Answers that include source references | >90% |
| Groundedness | Answers supported by retrieved context | >85% |
| Student Satisfaction | Thumbs up/down on answers | >80% positive |
| Latency P95 | Response time | <5 seconds |

---

## 4. Human-in-the-Loop

For a teaching context, sometimes the agent should escalate:

```python
ESCALATION_TRIGGERS = [
    "student expresses frustration (>3 failed attempts on same topic)",
    "question is ambiguous and could be answered multiple ways",
    "student requests to speak to the instructor",
    "guardrails block repeatedly (possible legitimate edge case)",
]
```

**Implementation**: Flag the interaction and notify the instructor via the admin dashboard or email.

---

## 5. Future Extensions

| Extension | Effort | Impact |
|-----------|--------|--------|
| Voice interface (Transcribe + Polly) | Medium | Accessibility |
| Study group matching | Medium | Social learning |
| Adaptive difficulty | High | Personalized pacing |
| Auto-generated quizzes from materials | Medium | Active recall |
| Integration with LMS (Canvas, Moodle) | High | Institutional adoption |
| Multi-language support | Low | Add translations to KB |

---

## Congratulations! 🎉

You've completed the tutorial. You now understand how to build a production-grade AI teaching agent with:

- ✅ Secure authentication (Cognito + JWT)
- ✅ Grounded Q&A (Bedrock Knowledge Bases + RAG)
- ✅ Comprehensive guardrails (topic denial, content filtering, PII, grounding)
- ✅ Student tracking and weakness analysis (DynamoDB)
- ✅ Full AWS deployment (CDK — six stacks: Auth, RAG, Guardrails, Tracking, API, and the CloudFront + S3 frontend from [Chapter 6](./06-deployment.md))
- ✅ Extension patterns (tools, multi-agent, evaluation) — including live **web search** augmentation
- ✅ Instructor content management ([Chapter 8](./08-course-materials.md): upload/sync course materials)

**What to build next**: Take these patterns and apply them to your own domain. The architecture is the same whether you're building a customer service agent, a code review agent, or a research assistant — swap the knowledge base, adjust the guardrails, and you have a new agent.

---

## Resources

- [Amazon Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Bedrock Knowledge Bases Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html)
- [Bedrock Guardrails Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html)
- [Converse API Reference](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html)
- [CDK v2 Python Reference](https://docs.aws.amazon.com/cdk/api/v2/python/)
- [DynamoDB Single-Table Design](https://www.alexdebrie.com/posts/dynamodb-single-table/)
