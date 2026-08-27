"""DynamoDB repository for student interaction tracking.

Single-table design with per-student partitioning for efficient queries
and strong isolation between students.
"""

import os
import time
from datetime import datetime, timezone
from typing import Optional
from ulid import ULID

import boto3
import structlog
from pydantic import BaseModel

logger = structlog.get_logger()

TABLE_NAME = os.environ.get("TRACKING_TABLE_NAME", "teaching-agent-tracking-dev")
dynamodb = boto3.resource("dynamodb", region_name="eu-west-2")
table = dynamodb.Table(TABLE_NAME)


class InteractionRecord(BaseModel):
    """A single student-agent interaction."""

    student_id: str
    timestamp: str
    interaction_id: str
    query: str
    response_summary: str  # First 500 chars of response (not full text)
    sources_used: list[str]
    tokens_used: int
    guardrail_triggered: bool = False
    violation_type: Optional[str] = None
    topic_detected: Optional[str] = None


class ProgressRecord(BaseModel):
    """Student progress on a specific topic."""

    student_id: str
    topic_slug: str
    topic_name: str
    questions_asked: int = 0
    last_accessed: str = ""
    confidence_score: float = 0.0  # Derived from engagement depth


async def log_interaction(
    student_id: str,
    query: str,
    response: str,
    sources: list[str],
    tokens_used: int,
    guardrail_triggered: bool = False,
    violation_type: Optional[str] = None,
) -> None:
    """Log a student interaction to DynamoDB (fire-and-forget).

    Args:
        student_id: Cognito sub (unique student ID).
        query: The student's question.
        response: The agent's response (truncated to 500 chars for storage).
        sources: List of source document names used.
        tokens_used: Total tokens consumed.
        guardrail_triggered: Whether guardrails intervened.
        violation_type: Type of violation if guardrails triggered.
    """
    now = datetime.now(timezone.utc)
    interaction_id = str(ULID())

    try:
        table.put_item(
            Item={
                "PK": f"STU#{student_id}",
                "SK": f"INT#{now.isoformat()}#{interaction_id}",
                "GSI1PK": f"DATE#{now.strftime('%Y-%m-%d')}",
                "GSI1SK": f"STU#{student_id}",
                "query": query[:500],  # Truncate for storage
                "response_summary": response[:500],
                "sources_used": sources,
                "tokens_used": tokens_used,
                "guardrail_triggered": guardrail_triggered,
                "violation_type": violation_type or "",
                "ttl": int(time.time()) + (365 * 24 * 3600),  # 12-month retention
            }
        )
        logger.info("interaction_logged", student_id=student_id, interaction_id=interaction_id)
    except Exception as e:
        # Fire-and-forget — don't fail the request if logging fails
        logger.error("tracking_write_failed", error=str(e), student_id=student_id)


async def get_student_progress(student_id: str) -> dict:
    """Retrieve a student's progress summary.

    Returns:
        Dict with total_questions, topics_explored, active_days, recent_topics.
    """
    try:
        response = table.query(
            KeyConditionExpression="PK = :pk AND begins_with(SK, :sk_prefix)",
            ExpressionAttributeValues={
                ":pk": f"STU#{student_id}",
                ":sk_prefix": "INT#",
            },
            Select="COUNT",
        )

        # Get recent interactions for topic analysis
        recent = table.query(
            KeyConditionExpression="PK = :pk AND begins_with(SK, :sk_prefix)",
            ExpressionAttributeValues={
                ":pk": f"STU#{student_id}",
                ":sk_prefix": "INT#",
            },
            ScanIndexForward=False,  # Most recent first
            Limit=20,
        )

        return {
            "total_questions": response.get("Count", 0),
            "recent_interactions": recent.get("Items", []),
        }

    except Exception as e:
        logger.error("progress_query_failed", error=str(e), student_id=student_id)
        return {"total_questions": 0, "recent_interactions": []}
