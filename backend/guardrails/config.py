"""Amazon Bedrock Guardrails configuration and policy definitions.

This module defines the guardrail policies applied to all LLM interactions.
The actual guardrail is created via CDK (see infrastructure/guardrails_stack.py)
and referenced here by ID and version.
"""

import os
from dataclasses import dataclass, field

# Guardrail identifiers (set via environment, deployed by CDK)
GUARDRAIL_ID = os.environ.get("BEDROCK_GUARDRAIL_ID", "")
GUARDRAIL_VERSION = os.environ.get("BEDROCK_GUARDRAIL_VERSION", "DRAFT")


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
        "NAME": "ANONYMIZE",  # In logs only — not in live responses
        "AWS_ACCESS_KEY": "BLOCK",
        "AWS_SECRET_KEY": "BLOCK",
    })

    # Contextual grounding
    grounding_threshold: float = 0.7  # Block if <70% grounded in retrieved context

    # Denial response shown to students
    denial_message: str = (
        "I'm your Agentic AI course guide — I can help with topics from the course "
        "like AI agents, RAG, prompt engineering, and multi-agent systems. "
        "Could you rephrase your question to relate to these areas?"
    )


# Singleton policy instance
POLICY = GuardrailPolicy()
