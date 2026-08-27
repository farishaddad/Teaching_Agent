"""DynamoDB repository for student interaction tracking.

Single-table design with per-student partitioning for efficient queries
and strong isolation between students. All writes are fire-and-forget async.
"""

import asyncio
import os
import time
from datetime import datetime, timezone
from typing import Optional

import boto3
import structlog
from ulid import ULID

from backend.tracking.progress import detect_topic, update_topic_progress

logger = structlog.get_logger()

TABLE_NAME = os.environ.get("TRACKING_TABLE_NAME", "teaching-agent-tracking-dev")
dynamodb = boto3.resource("dynamodb", region_name="eu-west-2")
table = dynamodb.Table(TABLE_NAME)


async def log_interaction(
    student_id: str,
    query: str,
    response: str,
    sources: list[str],
    tokens_input: int = 0,
    tokens_output: int = 0,
    session_id: Optional[str] = None,
    guardrail_triggered: bool = False,
    violation_type: Optional[str] = None,
    response_time_ms: int = 0,
) -> None:
    """Log a student interaction to DynamoDB (fire-and-forget).

    MUST NOT block the chat response. Errors are logged but not raised.

    Args:
        student_id: Cognito sub (unique student ID).
        query: Student's question (truncated to 500 chars).
        response: Agent's response (truncated to 500 chars).
        sources: List of source document names cited.
        tokens_input: Input tokens consumed.
        tokens_output: Output tokens consumed.
        session_id: Chat session ID for grouping.
        guardrail_triggered: Whether guardrails blocked this interaction.
        violation_type: Type of violation if blocked.
        response_time_ms: End-to-end response time.
    """
    now = datetime.now(timezone.utc)
    interaction_id = str(ULID())

    # Detect topic from query
    topic = detect_topic(query)

    try:
        table.put_item(
            Item={
                "PK": f"STU#{student_id}",
                "SK": f"INT#{now.isoformat()}#{interaction_id}",
                "GSI1PK": f"DATE#{now.strftime('%Y-%m-%d')}",
                "GSI1SK": f"STU#{student_id}",
                "query": query[:500],
                "response_summary": response[:500],
                "sources_used": sources,
                "tokens_input": tokens_input,
                "tokens_output": tokens_output,
                "tokens_total": tokens_input + tokens_output,
                "topic_detected": topic or "",
                "session_id": session_id or "",
                "guardrail_triggered": guardrail_triggered,
                "violation_type": violation_type or "",
                "response_time_ms": response_time_ms,
                "ttl": int(time.time()) + (365 * 24 * 3600),  # 12-month retention
            }
        )
        logger.info(
            "interaction_logged",
            student_id=student_id,
            interaction_id=interaction_id,
            topic=topic,
        )

        # Update topic progress (also fire-and-forget)
        if topic:
            await update_topic_progress(student_id, topic, session_id)

    except Exception as e:
        logger.error("tracking_write_failed", error=str(e), student_id=student_id)


async def get_student_interactions(
    student_id: str,
    limit: int = 20,
    newest_first: bool = True,
) -> list[dict]:
    """Get a student's interaction history (their own data only).

    Args:
        student_id: The requesting student's ID.
        limit: Max items to return.
        newest_first: Sort order.

    Returns:
        List of interaction items from DynamoDB.
    """
    try:
        response = table.query(
            KeyConditionExpression="PK = :pk AND begins_with(SK, :prefix)",
            ExpressionAttributeValues={
                ":pk": f"STU#{student_id}",
                ":prefix": "INT#",
            },
            ScanIndexForward=not newest_first,
            Limit=limit,
        )
        return response.get("Items", [])
    except Exception as e:
        logger.error("interaction_query_failed", error=str(e), student_id=student_id)
        return []


async def get_student_progress(student_id: str) -> dict:
    """Get a student's overall progress summary.

    Returns total questions, active days, topic breakdown.
    Students can only access their own data.
    """
    try:
        # Count total interactions
        count_response = table.query(
            KeyConditionExpression="PK = :pk AND begins_with(SK, :prefix)",
            ExpressionAttributeValues={
                ":pk": f"STU#{student_id}",
                ":prefix": "INT#",
            },
            Select="COUNT",
        )
        total_questions = count_response.get("Count", 0)

        # Get topic progress records
        topics_response = table.query(
            KeyConditionExpression="PK = :pk AND begins_with(SK, :prefix)",
            ExpressionAttributeValues={
                ":pk": f"STU#{student_id}",
                ":prefix": "PRG#",
            },
        )
        topics = topics_response.get("Items", [])

        # Calculate active days from recent interactions
        recent = table.query(
            KeyConditionExpression="PK = :pk AND begins_with(SK, :prefix)",
            ExpressionAttributeValues={
                ":pk": f"STU#{student_id}",
                ":prefix": "INT#",
            },
            ScanIndexForward=False,
            Limit=100,
        )
        active_dates = set()
        for item in recent.get("Items", []):
            sk = item.get("SK", "")
            if "#" in sk:
                date_part = sk.split("#")[1][:10]
                active_dates.add(date_part)

        # Separate strengths and weaknesses
        weaknesses = [t for t in topics if t.get("weakness_flag", False)]
        strengths = [
            t for t in topics
            if float(t.get("confidence_score", 0)) >= 0.7 and not t.get("weakness_flag", False)
        ]

        return {
            "student_id": student_id,
            "total_questions": total_questions,
            "total_sessions": max(1, total_questions // 5),  # Estimate
            "active_days": len(active_dates),
            "topics": topics,
            "weaknesses": weaknesses,
            "strengths": strengths,
            "recent_topics": list(set(
                t.get("topic_name", "") for t in topics
                if t.get("last_accessed")
            ))[:5],
        }

    except Exception as e:
        logger.error("progress_query_failed", error=str(e), student_id=student_id)
        return {
            "student_id": student_id,
            "total_questions": 0,
            "total_sessions": 0,
            "active_days": 0,
            "topics": [],
            "weaknesses": [],
            "strengths": [],
            "recent_topics": [],
        }
