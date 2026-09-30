"""CDK Stack: Amazon Bedrock Guardrails for the Teaching Agent.

Creates a guardrail with topic denial, content filtering, PII protection,
word policy (jailbreak phrases), and contextual grounding.
Publishes a versioned guardrail (not just DRAFT).
"""

from aws_cdk import (
    Stack,
    CfnOutput,
    aws_bedrock as bedrock,
)
from constructs import Construct


class TeachingAgentGuardrailsStack(Stack):
    """Bedrock Guardrail with comprehensive safety policies."""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create the guardrail
        self.guardrail = bedrock.CfnGuardrail(
            self,
            "TeachingAgentGuardrail",
            name="teaching-agent-guardrail",
            description="Guardrail for the Agentic AI Teaching Agent — enforces topic boundaries, content safety, PII protection, and contextual grounding",
            blocked_input_messaging=(
                "I'm your Agentic AI course guide. I can help with topics from the course "
                "like AI agents, RAG, prompt engineering, and multi-agent systems. "
                "Could you rephrase your question to relate to these areas?"
            ),
            blocked_outputs_messaging=(
                "I wasn't able to generate a safe response for that question. "
                "Please try rephrasing or ask about a different Agentic AI topic."
            ),
            # ─── Topic Policy ─────────────────────────────────────────
            topic_policy_config=bedrock.CfnGuardrail.TopicPolicyConfigProperty(
                topics_config=[
                    bedrock.CfnGuardrail.TopicConfigProperty(
                        name="Politics",
                        definition="Political opinions, elections, political parties, government policy debates, voting recommendations",
                        type="DENY",
                    ),
                    bedrock.CfnGuardrail.TopicConfigProperty(
                        name="Religion",
                        definition="Religious beliefs, spiritual practices, theological debates, faith-based advice",
                        type="DENY",
                    ),
                    bedrock.CfnGuardrail.TopicConfigProperty(
                        name="PersonalAdvice",
                        definition="Personal relationship advice, life coaching, emotional counseling, dating advice",
                        type="DENY",
                    ),
                    bedrock.CfnGuardrail.TopicConfigProperty(
                        name="MedicalLegalFinancial",
                        definition="Medical diagnoses, legal advice, financial investment recommendations, tax advice",
                        type="DENY",
                    ),
                    bedrock.CfnGuardrail.TopicConfigProperty(
                        name="AcademicDishonesty",
                        definition="Writing assignments or essays for students, helping cheat on exams, plagiarism assistance, doing homework",
                        type="DENY",
                    ),
                    bedrock.CfnGuardrail.TopicConfigProperty(
                        name="Hacking",
                        definition="Hacking techniques, exploit development, malware creation, unauthorized access to systems, password cracking",
                        type="DENY",
                    ),
                    bedrock.CfnGuardrail.TopicConfigProperty(
                        name="GeneralChat",
                        definition="Casual conversation unrelated to AI, requests for jokes, stories, creative writing, entertainment, sports, food recommendations",
                        type="DENY",
                    ),
                    bedrock.CfnGuardrail.TopicConfigProperty(
                        name="OffTopicGeneralKnowledge",
                        definition=(
                            "Real-world facts, news, weather, geography, cooking, travel, "
                            "sports results, or any subject outside the Agentic AI course "
                            "curriculum on AI agents, LLMs, RAG, and prompt engineering."
                        ),
                        examples=[
                            "What is the weather in London today?",
                            "Who won the football match last night?",
                            "What is the capital of France?",
                        ],
                        type="DENY",
                    ),
                ],
            ),
            # ─── Content Filter Policy ────────────────────────────────
            content_policy_config=bedrock.CfnGuardrail.ContentPolicyConfigProperty(
                filters_config=[
                    bedrock.CfnGuardrail.ContentFilterConfigProperty(
                        type="HATE",
                        input_strength="HIGH",
                        output_strength="HIGH",
                    ),
                    bedrock.CfnGuardrail.ContentFilterConfigProperty(
                        type="INSULTS",
                        input_strength="MEDIUM",
                        output_strength="MEDIUM",
                    ),
                    bedrock.CfnGuardrail.ContentFilterConfigProperty(
                        type="SEXUAL",
                        input_strength="HIGH",
                        output_strength="HIGH",
                    ),
                    bedrock.CfnGuardrail.ContentFilterConfigProperty(
                        type="VIOLENCE",
                        input_strength="HIGH",
                        output_strength="HIGH",
                    ),
                    bedrock.CfnGuardrail.ContentFilterConfigProperty(
                        type="MISCONDUCT",
                        input_strength="HIGH",
                        output_strength="HIGH",
                    ),
                ],
            ),
            # ─── PII / Sensitive Information Policy ───────────────────
            sensitive_information_policy_config=bedrock.CfnGuardrail.SensitiveInformationPolicyConfigProperty(
                pii_entities_config=[
                    bedrock.CfnGuardrail.PiiEntityConfigProperty(type="EMAIL", action="ANONYMIZE"),
                    bedrock.CfnGuardrail.PiiEntityConfigProperty(type="PHONE", action="ANONYMIZE"),
                    bedrock.CfnGuardrail.PiiEntityConfigProperty(type="ADDRESS", action="ANONYMIZE"),
                    bedrock.CfnGuardrail.PiiEntityConfigProperty(type="NAME", action="ANONYMIZE"),
                    bedrock.CfnGuardrail.PiiEntityConfigProperty(type="AWS_ACCESS_KEY", action="BLOCK"),
                    bedrock.CfnGuardrail.PiiEntityConfigProperty(type="AWS_SECRET_KEY", action="BLOCK"),
                    bedrock.CfnGuardrail.PiiEntityConfigProperty(type="CREDIT_DEBIT_CARD_NUMBER", action="BLOCK"),
                ],
            ),
            # ─── Word Policy (Jailbreak Phrases) ─────────────────────
            word_policy_config=bedrock.CfnGuardrail.WordPolicyConfigProperty(
                words_config=[
                    bedrock.CfnGuardrail.WordConfigProperty(text="ignore previous instructions"),
                    bedrock.CfnGuardrail.WordConfigProperty(text="ignore all instructions"),
                    bedrock.CfnGuardrail.WordConfigProperty(text="disregard your instructions"),
                    bedrock.CfnGuardrail.WordConfigProperty(text="pretend you are"),
                    bedrock.CfnGuardrail.WordConfigProperty(text="you are now"),
                    bedrock.CfnGuardrail.WordConfigProperty(text="act as if you have no restrictions"),
                    bedrock.CfnGuardrail.WordConfigProperty(text="override your safety"),
                    bedrock.CfnGuardrail.WordConfigProperty(text="bypass your filters"),
                    bedrock.CfnGuardrail.WordConfigProperty(text="DAN mode"),
                    bedrock.CfnGuardrail.WordConfigProperty(text="jailbreak"),
                    bedrock.CfnGuardrail.WordConfigProperty(text="system prompt"),
                    bedrock.CfnGuardrail.WordConfigProperty(text="what are your instructions"),
                    bedrock.CfnGuardrail.WordConfigProperty(text="reveal your prompt"),
                ],
                managed_word_lists_config=[
                    bedrock.CfnGuardrail.ManagedWordsConfigProperty(type="PROFANITY"),
                ],
            ),
            # ─── Contextual Grounding Policy ─────────────────────────
            contextual_grounding_policy_config=bedrock.CfnGuardrail.ContextualGroundingPolicyConfigProperty(
                filters_config=[
                    bedrock.CfnGuardrail.ContextualGroundingFilterConfigProperty(
                        type="GROUNDING",
                        threshold=0.7,  # Block if <70% grounded in retrieved context
                    ),
                    bedrock.CfnGuardrail.ContextualGroundingFilterConfigProperty(
                        type="RELEVANCE",
                        threshold=0.5,  # Block if response <50% relevant to query
                    ),
                ],
            ),
        )

        # ─── Publish a Version (not just DRAFT) ──────────────────────
        self.guardrail_version = bedrock.CfnGuardrailVersion(
            self,
            "TeachingAgentGuardrailVersion",
            guardrail_identifier=self.guardrail.attr_guardrail_id,
            description="Production v2 — added OffTopicGeneralKnowledge denied topic",
        )
        self.guardrail_version.add_dependency(self.guardrail)

        # ─── Exports ─────────────────────────────────────────────────
        self.guardrail_id = self.guardrail.attr_guardrail_id

        CfnOutput(self, "GuardrailId", value=self.guardrail.attr_guardrail_id)
        CfnOutput(self, "GuardrailArn", value=self.guardrail.attr_guardrail_arn)
        CfnOutput(
            self,
            "GuardrailVersion",
            value=self.guardrail_version.attr_version,
            description="Published guardrail version number (use this, not DRAFT)",
        )
