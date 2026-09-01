"""Topic detection and progress scoring for student tracking.

Classifies student questions by topic and maintains per-topic confidence scores.
"""

import os
from datetime import datetime, timezone
from typing import Optional

import boto3
import structlog

logger = structlog.get_logger()

TABLE_NAME = os.environ.get("TRACKING_TABLE_NAME", "teaching-agent-tracking-dev")
dynamodb = boto3.resource("dynamodb", region_name="eu-west-2")
table = dynamodb.Table(TABLE_NAME)

# ─── Course Topic Taxonomy (16 topics) ────────────────────────────────

COURSE_TOPICS = {
    "agent-fundamentals": "Agent Fundamentals & Architecture",
    "llm-foundations": "LLM Foundations",
    "prompt-engineering": "Prompt Engineering",
    "rag": "Retrieval-Augmented Generation (RAG)",
    "tool-use": "Tool Use & Function Calling",
    "multi-agent": "Multi-Agent Systems",
    "planning-reasoning": "Planning & Reasoning",
    "memory-state": "Memory & State Management",
    "guardrails-safety": "Guardrails & AI Safety",
    "evaluation": "Agent Evaluation & Testing",
    "deployment": "Deployment & Operations",
    "ethics-governance": "Ethics & Governance",
    "bedrock-services": "Amazon Bedrock Services",
    "use-cases": "Real-World Use Cases",
    "agent-frameworks": "Agent Frameworks (LangGraph, CrewAI, etc.)",
    "human-in-loop": "Human-in-the-Loop Patterns",
}

TOPIC_KEYWORDS = {
    "agent-fundamentals": ["agent", "autonomous", "architecture", "components", "agent loop", "perceive", "act", "observe"],
    "llm-foundations": ["llm", "language model", "transformer", "tokens", "context window", "foundation model", "inference", "fine-tun"],
    "prompt-engineering": ["prompt", "system prompt", "few-shot", "chain of thought", "cot", "instruction", "zero-shot", "prompt template"],
    "rag": ["rag", "retrieval", "knowledge base", "embeddings", "vector", "chunks", "grounding", "semantic search", "ingestion"],
    "tool-use": ["tool", "function calling", "api", "action", "tool use", "function call", "external tool"],
    "multi-agent": ["multi-agent", "orchestration", "crew", "swarm", "collaboration", "delegation", "supervisor"],
    "planning-reasoning": ["planning", "reasoning", "step by step", "decomposition", "react", "reflection", "self-critique"],
    "memory-state": ["memory", "state", "context", "conversation history", "persistence", "short-term", "long-term memory"],
    "guardrails-safety": ["guardrail", "safety", "filter", "content policy", "pii", "hallucination", "content filter", "topic denial"],
    "evaluation": ["evaluation", "testing", "benchmark", "metrics", "accuracy", "eval", "test suite", "red team"],
    "deployment": ["deploy", "production", "scaling", "lambda", "infrastructure", "cdk", "ci/cd", "monitoring"],
    "ethics-governance": ["ethics", "bias", "responsible", "governance", "fairness", "transparency", "accountability"],
    "bedrock-services": ["bedrock", "converse api", "knowledge base", "aws", "claude", "titan", "anthropic"],
    "use-cases": ["use case", "example", "application", "industry", "real world", "customer", "implementation"],
    "agent-frameworks": ["langgraph", "crewai", "autogen", "framework", "langchain", "llamaindex", "semantic kernel"],
    "human-in-loop": ["human", "approval", "review", "oversight", "escalation", "human-in-the-loop", "hitl"],
}


def detect_topic(query: str) -> Optional[str]:
    """Classify a student query into a course topic using keyword matching.

    Returns the topic_slug or None if no topic matches.
    """
    query_lower = query.lower()
    best_match = None
    best_score = 0

    for topic_slug, keywords in TOPIC_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in query_lower)
        if score > best_score:
            best_score = score
            best_match = topic_slug

    return best_match if best_score > 0 else None


async def update_topic_progress(
    student_id: str,
    topic_slug: str,
    session_id: Optional[str] = None,
) -> None:
    """Update a student's progress record for a specific topic.

    Increments question count, updates sessions, recalculates confidence.
    Fire-and-forget — errors are logged but not raised.
    """
    now = datetime.now(timezone.utc).isoformat()
    topic_name = COURSE_TOPICS.get(topic_slug, topic_slug)

    try:
        # Upsert: increment questions_asked, update last_accessed
        response = table.update_item(
            Key={
                "PK": f"STU#{student_id}",
                "SK": f"PRG#{topic_slug}",
            },
            UpdateExpression=(
                "SET topic_name = :name, last_accessed = :now "
                "ADD questions_asked :one"
            ),
            ExpressionAttributeValues={
                ":name": topic_name,
                ":now": now,
                ":one": 1,
            },
            ReturnValues="ALL_NEW",
        )

        item = response.get("Attributes", {})
        questions_asked = float(item.get("questions_asked", 1))

        # Recalculate confidence (simplified — full version uses session tracking)
        unique_sessions = float(item.get("unique_sessions", 1))
        avg_depth = questions_asked / max(unique_sessions, 1)
        confidence = min(1.0, (avg_depth * 0.3) + (unique_sessions * 0.1))
        weakness = questions_asked > 5 and confidence < 0.4

        # Update derived fields
        table.update_item(
            Key={
                "PK": f"STU#{student_id}",
                "SK": f"PRG#{topic_slug}",
            },
            UpdateExpression=(
                "SET confidence_score = :conf, weakness_flag = :weak, "
                "avg_follow_up_depth = :depth"
            ),
            ExpressionAttributeValues={
                ":conf": str(round(confidence, 3)),
                ":weak": weakness,
                ":depth": str(round(avg_depth, 2)),
            },
        )

    except Exception as e:
        logger.error(
            "progress_update_failed",
            error=str(e),
            student_id=student_id,
            topic=topic_slug,
        )


async def get_student_topics(student_id: str) -> list[dict]:
    """Get all topic progress records for a student."""
    try:
        response = table.query(
            KeyConditionExpression="PK = :pk AND begins_with(SK, :prefix)",
            ExpressionAttributeValues={
                ":pk": f"STU#{student_id}",
                ":prefix": "PRG#",
            },
        )
        return response.get("Items", [])
    except Exception as e:
        logger.error("get_topics_failed", error=str(e), student_id=student_id)
        return []
