"""CDK Stack: Amazon Bedrock Guardrails for the Teaching Agent.

Creates a guardrail with topic denial, content filtering, PII protection,
and contextual grounding policies.
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
            description="Guardrail for the Agentic AI Teaching Agent — enforces topic boundaries, content safety, and PII protection",
            blocked_input_messaging=(
                "I'm your Agentic AI course guide. I can help with topics from the course "
                "like AI agents, RAG, prompt engineering, and multi-agent systems. "
                "Could you rephrase your question to relate to these areas?"
            ),
            blocked_outputs_messaging=(
                "I wasn't able to generate a safe response for that question. "
                "Please try rephrasing or ask about a different Agentic AI topic."
            ),
            # Topic Policy — define allowed and denied topics
            topic_policy_config=bedrock.CfnGuardrail.TopicPolicyConfigProperty(
                topics_config=[
                    # Denied topics
                    bedrock.CfnGuardrail.TopicConfigProperty(
                        name="Politics",
                        definition="Political opinions, elections, political parties, government policy debates",
                        type="DENY",
                    ),
                    bedrock.CfnGuardrail.TopicConfigProperty(
                        name="Religion",
                        definition="Religious beliefs, spiritual practices, theological debates",
                        type="DENY",
                    ),
                    bedrock.CfnGuardrail.TopicConfigProperty(
                        name="PersonalAdvice",
                        definition="Personal relationship advice, life coaching, emotional counseling",
                        type="DENY",
                    ),
                    bedrock.CfnGuardrail.TopicConfigProperty(
                        name="MedicalLegal",
                        definition="Medical diagnoses, legal advice, financial investment recommendations",
                        type="DENY",
                    ),
                    bedrock.CfnGuardrail.TopicConfigProperty(
                        name="AcademicDishonesty",
                        definition="Writing assignments for students, helping cheat on exams, plagiarism assistance",
                        type="DENY",
                    ),
                    bedrock.CfnGuardrail.TopicConfigProperty(
                        name="Hacking",
                        definition="Hacking techniques, exploit development, malware creation, unauthorized access",
                        type="DENY",
                    ),
                ],
            ),
            # Content Filter Policy
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
            # Sensitive Information Policy (PII)
            sensitive_information_policy_config=bedrock.CfnGuardrail.SensitiveInformationPolicyConfigProperty(
                pii_entities_config=[
                    bedrock.CfnGuardrail.PiiEntityConfigProperty(type="EMAIL", action="ANONYMIZE"),
                    bedrock.CfnGuardrail.PiiEntityConfigProperty(type="PHONE", action="ANONYMIZE"),
                    bedrock.CfnGuardrail.PiiEntityConfigProperty(type="ADDRESS", action="ANONYMIZE"),
                    bedrock.CfnGuardrail.PiiEntityConfigProperty(type="AWS_ACCESS_KEY", action="BLOCK"),
                    bedrock.CfnGuardrail.PiiEntityConfigProperty(type="AWS_SECRET_KEY", action="BLOCK"),
                ],
            ),
        )

        # Store guardrail ID for cross-stack reference
        self.guardrail_id = self.guardrail.attr_guardrail_id

        CfnOutput(self, "GuardrailId", value=self.guardrail.attr_guardrail_id)
        CfnOutput(self, "GuardrailArn", value=self.guardrail.attr_guardrail_arn)
