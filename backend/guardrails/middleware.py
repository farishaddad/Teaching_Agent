"""Guardrails middleware — wraps all LLM calls with Bedrock Guardrails.

This module ensures every student interaction passes through guardrails
BEFORE reaching the LLM (input filtering) and AFTER the LLM responds
(output filtering).
"""

import structlog
import boto3
from typing import Optional

from backend.guardrails.config import GUARDRAIL_ID, GUARDRAIL_VERSION, POLICY

logger = structlog.get_logger()

bedrock_runtime = boto3.client("bedrock-runtime", region_name="eu-west-2")


class GuardrailResult:
    """Result of a guardrail check."""

    def __init__(self, allowed: bool, message: str, violation_type: Optional[str] = None):
        self.allowed = allowed
        self.message = message
        self.violation_type = violation_type


def apply_guardrails_to_converse(
    messages: list[dict],
    system_prompt: str,
    model_id: str = "anthropic.claude-3-5-sonnet-20241022-v2:0",
    student_id: str = "",
) -> dict:
    """Call Bedrock Converse API with guardrails applied.

    The guardrails are applied automatically by including guardrailConfig
    in the Converse API call. Bedrock handles both input and output filtering.

    Args:
        messages: Conversation messages in Converse format.
        system_prompt: System prompt for the agent.
        model_id: Bedrock model identifier.
        student_id: For logging purposes.

    Returns:
        Converse API response dict, or a guardrail denial response.
    """
    try:
        response = bedrock_runtime.converse(
            modelId=model_id,
            messages=messages,
            system=[{"text": system_prompt}],
            guardrailConfig={
                "guardrailIdentifier": GUARDRAIL_ID,
                "guardrailVersion": GUARDRAIL_VERSION,
                "trace": "enabled",  # For debugging/tutorial — disable in prod
            },
        )

        # Check if guardrails intervened
        if response.get("stopReason") == "guardrail_intervened":
            guardrail_trace = response.get("trace", {}).get("guardrail", {})
            violation_type = _extract_violation_type(guardrail_trace)

            logger.warning(
                "guardrail_triggered",
                student_id=student_id,
                violation_type=violation_type,
                action="blocked",
            )

            return {
                "blocked": True,
                "message": POLICY.denial_message,
                "violation_type": violation_type,
            }

        return {
            "blocked": False,
            "response": response,
        }

    except Exception as e:
        logger.error("converse_api_error", error=str(e), student_id=student_id)
        raise


def _extract_violation_type(trace: dict) -> str:
    """Extract the type of guardrail violation from the trace."""
    # Bedrock guardrail trace structure varies — extract what we can
    assessments = trace.get("inputAssessment", {}).get("topicPolicy", {})
    if assessments:
        return "topic_denial"

    content_policy = trace.get("inputAssessment", {}).get("contentPolicy", {})
    if content_policy:
        return "content_filter"

    return "unknown"
