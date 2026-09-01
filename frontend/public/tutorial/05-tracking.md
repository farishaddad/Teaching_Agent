# Chapter 5: Tracking & Analytics

## Why Track Everything?

A teaching agent without tracking is flying blind. Tracking gives you:
1. **Per-student traceability** — who asked what, when, and what the agent responded
2. **Progress monitoring** — which topics has a student covered? Are they progressing?
3. **Weakness detection** — which students are stuck? Which topics are confusing everyone?
4. **Usage controls** — token consumption, cost monitoring, abuse detection
5. **Compliance** — audit trail required by many educational institutions

---

## DynamoDB Single-Table Design

We use a single DynamoDB table for all entities (interactions, sessions, progress). This is the recommended pattern for serverless apps — fewer tables = fewer connections = faster cold starts.

### Table Schema

| Entity | PK | SK | Purpose |
|--------|----|----|---------|
| Interaction | `STU#{student_id}` | `INT#{timestamp}#{ulid}` | Every Q&A logged |
| Session | `STU#{student_id}` | `SES#{session_id}` | Group interactions into sessions |
| Progress | `STU#{student_id}` | `PRG#{topic_slug}` | Per-topic engagement scores |
| Daily | `STU#{student_id}` | `DAY#{date}` | Daily summary per student |

### GSI1 (Admin Cross-Student Queries)

| GSI1PK | GSI1SK | Use Case |
|--------|--------|----------|
| `DATE#{yyyy-mm-dd}` | `STU#{student_id}` | "Show all activity on a given day" |

### Why This Pattern?

- **Student queries are fast**: Everything for one student shares the same PK → single partition
- **Admin queries use GSI**: Cross-student views query by date
- **Sort keys enable ranges**: `begins_with(SK, "INT#2026-08")` = all August interactions
- **TTL for retention**: Auto-delete records after 12 months

---

## Implementation: Async Logging

**Critical principle**: Tracking MUST NOT slow down the chat response. We use fire-and-forget async writes.

```python
# backend/tracking/repository.py

async def log_interaction(
    student_id: str,
    query: str,
    response: str,    # Truncated to 500 chars
    sources: list,
    tokens_used: int,
    guardrail_triggered: bool,
) -> None:
    """Log interaction — fire and forget."""
    
    now = datetime.now(timezone.utc)
    interaction_id = str(ULID())  # Sortable unique ID
    
    try:
        table.put_item(Item={
            "PK": f"STU#{student_id}",
            "SK": f"INT#{now.isoformat()}#{interaction_id}",
            "GSI1PK": f"DATE#{now.strftime('%Y-%m-%d')}",
            "GSI1SK": f"STU#{student_id}",
            "query": query[:500],
            "response_summary": response[:500],
            "sources_used": sources,
            "tokens_used": tokens_used,
            "guardrail_triggered": guardrail_triggered,
            "ttl": int(time.time()) + (365 * 24 * 3600),
        })
    except Exception as e:
        # Log but don't crash — tracking is non-critical
        logger.error("tracking_write_failed", error=str(e))
```

**In the chat handler:**
```python
# Non-blocking — response returns immediately while write happens in background
asyncio.create_task(log_interaction(
    student_id=student.id,
    query=body.message,
    response=answer,
    sources=[s["source"] for s in sources],
    tokens_used=token_count,
    guardrail_triggered=False,
))
```

---

## Progress Tracking Logic

### Topic Detection

Every question is classified by topic using keyword matching:

```python
TOPIC_KEYWORDS = {
    "rag": ["rag", "retrieval", "knowledge base", "embeddings", "vector", "grounding"],
    "prompt-engineering": ["prompt", "system prompt", "few-shot", "chain of thought"],
    "multi-agent": ["multi-agent", "orchestration", "crew", "swarm"],
    # ... 16 topics total
}

def detect_topic(query: str) -> str | None:
    """Match a student query to a course topic."""
    query_lower = query.lower()
    best_match, best_score = None, 0
    
    for topic, keywords in TOPIC_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in query_lower)
        if score > best_score:
            best_score = score
            best_match = topic
    
    return best_match if best_score > 0 else None
```

### Weakness Detection Algorithm

A student is flagged as "struggling" on a topic when:
- They've asked **>5 questions** on that topic
- But their **confidence score is <0.4**

Confidence is derived from:
- **Follow-up depth**: Are they asking progressively deeper questions? (good)
- **Session spread**: Are they coming back to the same basics repeatedly? (bad)

```python
confidence = min(1.0, (avg_follow_up_depth * 0.3) + (unique_sessions * 0.1))
weakness = question_count > 5 and confidence < 0.4
```

---

## Student Progress Dashboard Data

```python
# GET /api/admin/students/{id}/progress returns:

{
    "student_id": "abc-123",
    "student_name": "Alice Smith",
    "total_questions": 47,
    "total_sessions": 12,
    "active_days": 8,
    "topics": [
        {
            "topic_name": "RAG",
            "questions_asked": 15,
            "unique_sessions": 5,
            "confidence_score": 0.72,
            "weakness_flag": false   # Strong area
        },
        {
            "topic_name": "Multi-Agent Systems",
            "questions_asked": 8,
            "unique_sessions": 6,
            "confidence_score": 0.32,
            "weakness_flag": true    # Struggling!
        }
    ],
    "weaknesses": [...],   # Filtered topics with weakness_flag=true
    "strengths": [...]     # Topics with confidence >= 0.7
}
```

---

## CDK: DynamoDB Table

```python
# infrastructure/tracking_stack.py

self.table = dynamodb.Table(
    self, "TrackingTable",
    table_name="teaching-agent-tracking",
    partition_key=dynamodb.Attribute(name="PK", type=dynamodb.AttributeType.STRING),
    sort_key=dynamodb.Attribute(name="SK", type=dynamodb.AttributeType.STRING),
    billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
    time_to_live_attribute="ttl",
    removal_policy=RemovalPolicy.RETAIN,
)

# GSI for admin date-based queries
self.table.add_global_secondary_index(
    index_name="GSI1",
    partition_key=dynamodb.Attribute(name="GSI1PK", type=dynamodb.AttributeType.STRING),
    sort_key=dynamodb.Attribute(name="GSI1SK", type=dynamodb.AttributeType.STRING),
)
```

---

## Privacy Considerations

- **Truncate responses**: Store only first 500 chars — not full LLM output
- **PII redaction**: Guardrails anonymize PII before it reaches DynamoDB
- **Access control**: Students can only view their own data
- **TTL-based deletion**: Records auto-expire after 12 months
- **No unnecessary fields**: Don't log what you don't need

---

## Next Chapter

In [Chapter 6: Deployment](./06-deployment.md), we'll deploy the entire system to AWS using CDK and set up CI/CD.
