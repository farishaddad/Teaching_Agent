"""Guardrails middleware — wraps all LLM calls with Bedrock Guardrails.

Provides:
- apply_guardrails_to_converse(): Full round-trip guardrail check via Converse API
- check_input(): Standalone input pre-screening before KB retrieval
- parse_guardrail_trace(): Detailed trace parsing for violation classification
"""

import boto3
import structlog
from typing import Optional

from backend.guardrails.config import get_guardrail_config
from backend.guardrails.violation_handler import (
    classify_violation,
    get_friendly_message,
    is_rate_limited,
    log_violation,
    record_violation_for_rate_limit,
)

logger = structlog.get_logger()

_bedrock_runtime = None


def _get_runtime():
    """Lazy-init Bedrock runtime client."""
    global _bedrock_runtime
    if _bedrock_runtime is None:
        _bedrock_runtime = boto3.client("bedrock-runtime", region_name="eu-west-2")
    return _bedrock_runtime


class GuardrailResult:
    """Result of a guardrail check."""

    def __init__(
        self,
        allowed: bool,
        message: str,
        violation_type: Optional[str] = None,
        details: Optional[str] = None,
        trace: Optional[dict] = None,
    ):
        self.allowed = allowed
        self.message = message
        self.violation_type = violation_type
        self.details = details
        self.trace = trace


async def check_input(text: str, student_id: str = "") -> GuardrailResult:
    """Pre-screen a student's input BEFORE sending to the LLM/KB.

    Uses the ApplyGuardrail API for input-only checking.
    This is a lightweight pre-flight check — the full guardrail
    is also applied in the Converse call for output filtering.
    """
    guardrail_config = get_guardrail_config()
    if not guardrail_config:
        return GuardrailResult(allowed=True, message="")

    # Check rate limiting first
    if is_rate_limited(student_id):
        return GuardrailResult(
            allowed=False,
            message=get_friendly_message("rate_limited"),
            violation_type="rate_limited",
        )

    try:
        client = _get_runtime()
        response = client.apply_guardrail(
            guardrailIdentifier=guardrail_config["guardrailIdentifier"],
            guardrailVersion=guardrail_config["guardrailVersion"],
            source="INPUT",
            content=[{"text": {"text": text}}],
        )

        action = response.get("action", "NONE")

        if action == "GUARDRAIL_INTERVENED":
            # Parse the trace to classify the violation
            assessments = response.get("assessments", [{}])
            trace = assessments[0] if assessments else {}
            violation = classify_violation({"inputAssessment": trace})

            # Record for rate limiting
            record_violation_for_rate_limit(student_id)

            # Log asynchronously
            import asyncio
            asyncio.create_task(log_violation(
                student_id=student_id,
                violation_type=violation["violation_type"],
                query_summary=text[:200],
                details=violation["details"],
            ))

            logger.warning(
                "guardrail_input_blocked",
                student_id=student_id,
                violation_type=violation["violation_type"],
            )

            return GuardrailResult(
                allowed=False,
                message=get_friendly_message(violation["violation_type"]),
                violation_type=violation["violation_type"],
                details=violation["details"],
                trace=trace,
            )

        return GuardrailResult(allowed=True, message="")

    except Exception as e:
        # If guardrail check fails, allow through (fail-open for availability)
        # but log the error for monitoring
        logger.error("guardrail_input_check_failed", error=str(e), student_id=student_id)
        return GuardrailResult(allowed=True, message="")


def apply_guardrails_to_converse(
    messages: list[dict],
    system_prompt: str,
    model_id: str = "anthropic.claude-3-5-sonnet-20241022-v2:0",
    student_id: str = "",
) -> dict:
    """Call Bedrock Converse API with guardrails applied (input + output filtering).

    The guardrails are applied automatically by including guardrailConfig
    in the Converse API call. Bedrock handles both input and output filtering.

    Args:
        messages: Conversation messages in Converse format.
        system_prompt: System prompt for the agent.
        model_id: Bedrock model identifier.
        student_id: For logging purposes.

    Returns:
        Dict with 'blocked' (bool), 'response' or 'message', 'violation_type'.
    """
    guardrail_config = get_guardrail_config()
    client = _get_runtime()

    try:
        converse_params = {
            "modelId": model_id,
            "messages": messages,
            "system": [{"text": system_prompt}],
        }

        if guardrail_config:
            converse_params["guardrailConfig"] = guardrail_config

        response = client.converse(**converse_params)

        # Check if guardrails intervened
        if response.get("stopReason") == "guardrail_intervened":
            trace = response.get("trace", {}).get("guardrail", {})
            violation = classify_violation(trace)

            # Record for rate limiting
            record_violation_for_rate_limit(student_id)

            # Log violation asynchronously
            import asyncio
            asyncio.create_task(log_violation(
                student_id=student_id,
                violation_type=violation["violation_type"],
                query_summary="[from converse output]",
                details=violation["details"],
            ))

            logger.warning(
                "guardrail_converse_blocked",
                student_id=student_id,
                violation_type=violation["violation_type"],
                stop_reason="guardrail_intervened",
            )

            return {
                "blocked": True,
                "message": get_friendly_message(violation["violation_type"]),
                "violation_type": violation["violation_type"],
            }

        return {
            "blocked": False,
            "response": response,
        }

    except Exception as e:
        logger.error("converse_api_error", error=str(e), student_id=student_id)
        raise


def parse_guardrail_trace(response: dict) -> Optional[dict]:
    """Extract and parse the guardrail trace from a Converse API response.

    Returns None if no guardrail trace present.
    Returns classified violation dict if guardrails were involved.
    """
    trace = response.get("trace", {}).get("guardrail", {})
    if not trace:
        return None
    return classify_violation(trace)
