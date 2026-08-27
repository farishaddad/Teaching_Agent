"""Amazon Bedrock Knowledge Base integration for RAG-based Q&A.

Retrieves relevant course material chunks and generates grounded answers
using the RetrieveAndGenerate API.
"""

import os
from typing import Optional

import boto3
import structlog

logger = structlog.get_logger()

# Configuration
KNOWLEDGE_BASE_ID = os.environ.get("BEDROCK_KB_ID", "")
MODEL_ARN = os.environ.get(
    "BEDROCK_MODEL_ARN",
    "arn:aws:bedrock:eu-west-2::foundation-model/anthropic.claude-3-5-sonnet-20241022-v2:0",
)

bedrock_agent_runtime = boto3.client("bedrock-agent-runtime", region_name="eu-west-2")

SYSTEM_PROMPT = """You are an expert teaching assistant for an Agentic AI course. Your role is to:

1. Answer student questions about Agentic AI, grounded in the course materials provided.
2. Explain concepts clearly with examples relevant to the course.
3. Reference specific sections/modules from the course when applicable.
4. If the question is outside the course scope, politely redirect to course topics.
5. Encourage deeper exploration and suggest related course modules.

IMPORTANT:
- Only provide information that is supported by the retrieved course materials.
- If you cannot find relevant information in the materials, say so honestly.
- Never make up information or hallucinate facts.
- Be encouraging and supportive — students are learning.
- Keep answers focused and concise unless asked for detail.

Course: Introduction to Agentic AI
Topics covered: AI agents, LLMs, prompt engineering, RAG, tool use, multi-agent systems,
AI safety, guardrails, evaluation, and building AI applications on AWS.
"""


def retrieve_and_generate(
    query: str,
    conversation_history: Optional[list[dict]] = None,
    student_id: str = "",
) -> dict:
    """Retrieve relevant course materials and generate a grounded answer.

    Args:
        query: The student's question.
        conversation_history: Previous turns for context continuity.
        student_id: For logging.

    Returns:
        Dict with 'answer', 'sources' (citations), and 'retrieved_chunks'.
    """
    logger.info("rag_query", student_id=student_id, query=query[:100])

    try:
        response = bedrock_agent_runtime.retrieve_and_generate(
            input={"text": query},
            retrieveAndGenerateConfiguration={
                "type": "KNOWLEDGE_BASE",
                "knowledgeBaseConfiguration": {
                    "knowledgeBaseId": KNOWLEDGE_BASE_ID,
                    "modelArn": MODEL_ARN,
                    "generationConfiguration": {
                        "promptTemplate": {
                            "textPromptTemplate": SYSTEM_PROMPT + "\n\nContext:\n$search_results$\n\nStudent question: $query$"
                        }
                    },
                    "retrievalConfiguration": {
                        "vectorSearchConfiguration": {
                            "numberOfResults": 5,  # Top 5 most relevant chunks
                        }
                    },
                },
            },
        )

        # Extract answer and citations
        answer = response.get("output", {}).get("text", "")
        citations = _extract_citations(response.get("citations", []))

        return {
            "answer": answer,
            "sources": citations,
            "session_id": response.get("sessionId"),
        }

    except Exception as e:
        logger.error("rag_error", error=str(e), student_id=student_id)
        return {
            "answer": "I'm having trouble accessing the course materials right now. Please try again in a moment.",
            "sources": [],
            "error": str(e),
        }


def _extract_citations(citations: list) -> list[dict]:
    """Extract readable citation references from the RAG response."""
    sources = []
    for citation in citations:
        for reference in citation.get("retrievedReferences", []):
            location = reference.get("location", {})
            s3_uri = location.get("s3Location", {}).get("uri", "")
            # Extract filename from S3 URI for display
            filename = s3_uri.split("/")[-1] if s3_uri else "Unknown source"
            sources.append({
                "source": filename,
                "excerpt": reference.get("content", {}).get("text", "")[:200],
            })
    return sources
