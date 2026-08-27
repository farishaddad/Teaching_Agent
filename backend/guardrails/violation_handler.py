"""Guardrail Violation Handler — user-friendly messages + logging + rate limiting.

Maps guardrail violations to student-safe messages (never expose internals),
logs violations separately for admin monitoring, and detects abuse patterns.
"""

import os
import time
from collections import defaultdict
from datetime import datetime, timezone
from typing import Optional

import boto3
import structlog
from ulid import ULID

logger = structlog.get_logger()

TABLE_NAME = os.environ.get("TRACKING_TABLE_NAME", "teaching-agent-tracking-dev")
dynamodb = boto3.resource("dynamodb", region_name="eu-west-2")
table = dynamodb.Table(TABLE_NAME)

# Rate limiting: track violations per student (in-memory for Lambda instance)
_violation_counts: dict[str, list[float]] = defaultdict(list)
RATE_LIMIT_WINDOW_SECONDS = 600  # 10 minutes
RATE_LIMIT_THRESHOLD = 5  # Max violations before flagging


# ─── User-Friendly Messages ──────────────────────────────────────────

FRIENDLY_MESSAGES = {
    "topic_denial": (
        "I'm your Agentic AI course guide — I can help with topics like AI agents, "
        "RAG, prompt engineering, tool use, and multi-agent systems. "
        "Could you rephrase your question to relate to the course material?"
    ),
    "content_filter": (
        "I wasn't able to process that message. Let's keep our conversation "
        "focused on learning about Agentic AI. What topic can I help you with?"
    ),
    "pii_blocked": (
        "For your privacy, I can't process messages containing sensitive personal "
        "information like credentials or access keys. Please remove any sensitive "
        "data and try again."
    ),
    "grounding_failed": (
        "I don't have enough information in the course materials to give you a "
        "reliable answer on that. Could you try rephrasing, or ask about a specific "
        "module topic?"
    ),
    "word_policy": (
        "I'm your Agentic AI course guide — I can help with topics from the course "
        "like AI agents, RAG, prompt engineering, and multi-agent systems. "
        "How can I help you learn today?"
    ),
    "rate_limited": (
        "I've noticed several of your messages have been outside the course scope. "
        "I'm here to help you learn about Agentic AI — would you like to explore "
        "a specific module or topic?"
    ),
    "unknown": (
        "I wasn't able to generate a response for that. Could you try rephrasing "
        "your question about Agentic AI?"
    ),
}


def get_friendly_message(violation_type: str) -> str:
    """Get a student-safe message for a guardrail violation.

    IMPORTANT: Never expose guardrail policy names, IDs, or technical details.
    """
    return FRIENDLY_MESSAGES.get(violation_type, FRIENDLY_MESSAGES["unknown"])


# ─── Violation Classification ─────────────────────────────────────────

def classify_violation(trace: dict) -> dict:
    """Parse a Bedrock Guardrail trace and classify the violation.

    Args:
        trace: The guardrail trace from the Converse API response.

    Returns:
        Dict with: violation_type, policy_name, details (sanitized for logging).
    """
    result = {
        "violation_type": "unknown",
        "policy_name": "",
        "details": "",
        "pii_detected": False,
    }

    # Check input assessment
    input_assessment = trace.get("inputAssessment", {})
    output_assessment = trace.get("outputAssessment", {})

    # Priority order: PII > Content > Topic > Grounding > Word
    assessment = input_assessment or output_assessment

    # Topic policy
    topic_policy = assessment.get("topicPolicy", {})
    if topic_policy.get("topics"):
        topics = topic_policy["topics"]
        result["violation_type"] = "topic_denial"
        result["policy_name"] = topics[0].get("name", "") if topics else ""
        result["details"] = f"topic_count={len(topics)}"
        return result

    # Content filter
    content_policy = assessment.get("contentPolicy", {})
    if content_policy.get("filters"):
        filters = content_policy["filters"]
        triggered = [f for f in filters if f.get("action") == "BLOCKED"]
        if triggered:
            result["violation_type"] = "content_filter"
            result["policy_name"] = triggered[0].get("type", "")
            result["details"] = f"filter_type={triggered[0].get('type')},confidence={triggered[0].get('confidence', 'N/A')}"
            return result

    # Sensitive information (PII)
    sensitive_policy = assessment.get("sensitiveInformationPolicy", {})
    if sensitive_policy.get("piiEntities"):
        entities = sensitive_policy["piiEntities"]
        blocked = [e for e in entities if e.get("action") == "BLOCKED"]
        anonymized = [e for e in entities if e.get("action") == "ANONYMIZED"]

        if blocked:
            result["violation_type"] = "pii_blocked"
            result["pii_detected"] = True
            # DO NOT log what the PII was — only that it occurred
            result["details"] = f"pii_types_blocked={len(blocked)}"
        elif anonymized:
            # Anonymization is not a block — log that it occurred
            result["violation_type"] = "pii_anonymized"
            result["pii_detected"] = True
            result["details"] = f"pii_types_anonymized={len(anonymized)}"
        return result

    # Word policy
    word_policy = assessment.get("wordPolicy", {})
    if word_policy.get("customWords") or word_policy.get("managedWordLists"):
        result["violation_type"] = "word_policy"
        result["details"] = "managed_word_match"
        return result

    # Contextual grounding
    grounding = assessment.get("contextualGroundingPolicy", {})
    if grounding.get("filters"):
        grounding_filters = grounding["filters"]
        failed = [f for f in grounding_filters if f.get("action") == "BLOCKED"]
        if failed:
            result["violation_type"] = "grounding_failed"
            result["details"] = f"grounding_score={failed[0].get('score', 'N/A')}"
            return result

    return result


# ─── Violation Logging ────────────────────────────────────────────────

async def log_violation(
    student_id: str,
    violation_type: str,
    query_summary: str,
    details: str = "",
) -> None:
    """Log a guardrail violation to DynamoDB (separate from interaction logs).

    IMPORTANT: Never log the actual PII content — only that a violation occurred.
    Query is truncated and sanitized before logging.
    """
    now = datetime.now(timezone.utc)
    violation_id = str(ULID())

    # Sanitize query for logging (truncate, don't store if PII was involved)
    safe_query = query_summary[:200] if violation_type != "pii_blocked" else "[REDACTED — PII detected]"

    try:
        table.put_item(
            Item={
                "PK": f"STU#{student_id}",
                "SK": f"VIO#{now.isoformat()}#{violation_id}",
                "GSI1PK": f"VIO#{now.strftime('%Y-%m-%d')}",
                "GSI1SK": f"STU#{student_id}",
                "violation_type": violation_type,
                "query_summary": safe_query,
                "details": details,
                "timestamp": now.isoformat(),
                "ttl": int(time.time()) + (180 * 24 * 3600),  # 6-month retention
            }
        )
        logger.info(
            "violation_logged",
            student_id=student_id,
            violation_type=violation_type,
            violation_id=violation_id,
        )
    except Exception as e:
        # Fire-and-forget — don't fail the request
        logger.error("violation_log_failed", error=str(e), student_id=student_id)


# ─── Rate Limiting ────────────────────────────────────────────────────

def check_rate_limit(student_id: str) -> bool:
    """Check if a student has exceeded the violation rate limit.

    Returns True if the student is rate-limited (too many violations).
    """
    now = time.time()
    window_start = now - RATE_LIMIT_WINDOW_SECONDS

    # Clean old entries
    _violation_counts[student_id] = [
        t for t in _violation_counts[student_id] if t > window_start
    ]

    return len(_violation_counts[student_id]) >= RATE_LIMIT_THRESHOLD


def record_violation_for_rate_limit(student_id: str) -> None:
    """Record a violation timestamp for rate limiting."""
    _violation_counts[student_id].append(time.time())


def is_rate_limited(student_id: str) -> bool:
    """Check if student is currently rate-limited and should get the rate-limit message."""
    return check_rate_limit(student_id)
