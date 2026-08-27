"""Amazon Bedrock Guardrails configuration and policy definitions.

This module defines the guardrail policies applied to all LLM interactions.
The actual guardrail is created via CDK (see infrastructure/guardrails_stack.py)
and referenced here by ID and version.
"""

import os
from dataclasses import dataclass, field

# Guardrail identifiers (set via environment, deployed by CDK)
GUARDRAIL_ID = os.environ.get("BEDROCK_GUARDRAIL_ID", "")
GUARDRAIL_VERSION = os.environ.get("BEDROCK_GUARDRAIL_VERSION", "1")  # Published version, not DRAFT


def get_guardrail_config() -> dict:
    """Get the guardrailConfig dict for Bedrock Converse API calls.

    Returns empty dict if guardrail ID is not configured (local dev).
    """
    if not GUARDRAIL_ID:
        return {}
    return {
        "guardrailIdentifier": GUARDRAIL_ID,
        "guardrailVersion": GUARDRAIL_VERSION,
        "trace": "enabled" if os.environ.get("GUARDRAIL_TRACE_ENABLED", "false") == "true" else "disabled",
    }


@dataclass
class GuardrailPolicy:
    """Documents the guardrail policies for reference and tutorial purposes.

    These map to the Bedrock Guardrail configuration deployed via CDK.
    Kept in code for transparency and tutorial documentation.
    """

    # Topics the agent IS allowed to discuss
    allowed_topics: list[str] = field(default_factory=lambda: [
        "Agentic AI concepts and architectures",
        "AI agents, autonomous agents, multi-agent systems",
        "Large Language Models (LLMs) and foundation models",
        "Prompt engineering and prompt design",
        "Retrieval-Augmented Generation (RAG)",
        "Tool use and function calling",
        "AI safety, alignment, and responsible AI",
        "AI ethics and governance",
        "Agent evaluation and testing",
        "Course logistics and materials",
        "Building AI applications on AWS",
        "Amazon Bedrock services and capabilities",
        "Planning, reasoning, and chain-of-thought",
        "Memory and state management in agents",
        "Human-in-the-loop patterns",
        "Agent frameworks (LangGraph, CrewAI, AutoGen)",
    ])

    # Topics that are explicitly DENIED
    denied_topics: list[str] = field(default_factory=lambda: [
        "Politics, elections, political opinions",
        "Religion and religious beliefs",
        "Personal relationship advice",
        "Medical or legal advice",
        "Financial investment advice",
        "Homework/assignments unrelated to AI agents",
        "Hacking, exploits, or malicious activities",
        "Content generation for academic dishonesty",
        "General chat unrelated to the course",
    ])

    # Content filter thresholds (HIGH = most strict)
    content_filters: dict[str, str] = field(default_factory=lambda: {
        "HATE": "HIGH",
        "INSULTS": "MEDIUM",
        "SEXUAL": "HIGH",
        "VIOLENCE": "HIGH",
        "MISCONDUCT": "HIGH",
    })

    # PII handling
    pii_actions: dict[str, str] = field(default_factory=lambda: {
        "EMAIL": "ANONYMIZE",
        "PHONE": "ANONYMIZE",
        "ADDRESS": "ANONYMIZE",
        "NAME": "ANONYMIZE",
        "AWS_ACCESS_KEY": "BLOCK",
        "AWS_SECRET_KEY": "BLOCK",
        "CREDIT_DEBIT_CARD_NUMBER": "BLOCK",
    })

    # Managed word list for prompt injection / jailbreak attempts
    blocked_phrases: list[str] = field(default_factory=lambda: [
        "ignore previous instructions",
        "ignore all instructions",
        "disregard your instructions",
        "pretend you are",
        "you are now",
        "act as if you have no restrictions",
        "override your safety",
        "bypass your filters",
        "DAN mode",
        "jailbreak",
        "system prompt",
        "what are your instructions",
        "reveal your prompt",
    ])

    # Contextual grounding
    grounding_threshold: float = 0.7  # Block if <70% grounded in retrieved context
    relevance_threshold: float = 0.5  # Block if <50% relevant to query

    # Denial response shown to students
    denial_message: str = (
        "I'm your Agentic AI course guide — I can help with topics from the course "
        "like AI agents, RAG, prompt engineering, and multi-agent systems. "
        "Could you rephrase your question to relate to these areas?"
    )


# Singleton policy instance
POLICY = GuardrailPolicy()
