"""Amazon Bedrock Knowledge Base integration for RAG-based Q&A.

Two retrieval modes are supported:

1. ``retrieve_and_generate`` — single-call API that retrieves and generates
   in one Bedrock call. Simple but does not support streaming or guardrail
   tracing in the same response.

2. ``retrieve`` — returns raw chunks only. The caller (chat_handler) then
   formats them into a Converse API call with guardrails applied explicitly.
   This is the preferred path for streaming + guardrail transparency.
"""

import os
from typing import Optional

import boto3
import structlog
from botocore.exceptions import BotoCoreError, ClientError

from backend.rag.prompt_templates import (
    FALLBACK_RESPONSE,
    SYSTEM_PROMPT,
    build_user_message_with_context,
)

logger = structlog.get_logger()

# ── Configuration ──────────────────────────────────────────────────────────────
KNOWLEDGE_BASE_ID: str = os.environ.get("BEDROCK_KB_ID", "") or os.environ.get("BEDROCK_KNOWLEDGE_BASE_ID", "")
MODEL_ARN: str = os.environ.get("BEDROCK_MODEL_ARN", "arn:aws:bedrock:eu-west-2::foundation-model/anthropic.claude-3-haiku-20240307-v1:0")
BEDROCK_REGION: str = os.environ.get("BEDROCK_REGION", "eu-west-2")
GUARDRAIL_ID: str = os.environ.get("BEDROCK_GUARDRAIL_ID", "")
GUARDRAIL_VERSION: str = os.environ.get("BEDROCK_GUARDRAIL_VERSION", "DRAFT")

# Number of retrieved chunks to request from the KB
_NUM_RESULTS: int = 5
# Maximum conversation turns to send for context continuity (last N turns = N*2 messages)
_MAX_HISTORY_TURNS: int = 5

# ── Bedrock clients (module-level; reused across Lambda invocations) ──────────
_bedrock_agent_runtime: Optional[boto3.client] = None
_bedrock_runtime: Optional[boto3.client] = None


def _get_agent_runtime() -> boto3.client:
    global _bedrock_agent_runtime
    if _bedrock_agent_runtime is None:
        _bedrock_agent_runtime = boto3.client(
            "bedrock-agent-runtime", region_name=BEDROCK_REGION
        )
    return _bedrock_agent_runtime


def _get_bedrock_runtime() -> boto3.client:
    global _bedrock_runtime
    if _bedrock_runtime is None:
        _bedrock_runtime = boto3.client("bedrock-runtime", region_name=BEDROCK_REGION)
    return _bedrock_runtime


# ── Public API ────────────────────────────────────────────────────────────────


def retrieve_and_generate(
    query: str,
    conversation_history: Optional[list[dict]] = None,
    student_id: str = "",
    system_prompt: str = SYSTEM_PROMPT,
    session_id: Optional[str] = None,
) -> dict:
    """Single-call RAG: retrieve relevant chunks + generate answer via Bedrock KB.

    Uses the ``RetrieveAndGenerate`` API which handles retrieval and generation
    in one call. Conversation history is passed via ``sessionId`` — Bedrock
    maintains session state server-side for this API.

    Args:
        query: The student's question.
        conversation_history: Ignored here (session managed by Bedrock).
            For explicit history control, use ``retrieve`` + Converse API.
        student_id: For structured logging only.
        system_prompt: Override the default system prompt if needed.
        session_id: Bedrock session ID for conversation continuity (from previous call).

    Returns:
        Dict with keys:
          - ``answer``: Generated text
          - ``sources``: List of ``{source, excerpt}`` dicts
          - ``session_id``: Bedrock session ID (pass back on next call)
          - ``tokens_used``: Token count if available, else 0
    """
    log = logger.bind(student_id=student_id, query_preview=query[:80])
    log.info("rag_retrieve_and_generate_start")

    if not KNOWLEDGE_BASE_ID:
        logger.error("knowledge_base_id_not_configured")
        return _error_response("Knowledge base is not configured. Contact support.")

    kb_config: dict = {
        "knowledgeBaseId": KNOWLEDGE_BASE_ID,
        "modelArn": MODEL_ARN,
        "generationConfiguration": {
            "promptTemplate": {
                "textPromptTemplate": (
                    f"{system_prompt}\n\n"
                    "## Retrieved course materials\n$search_results$\n\n"
                    "## Student question\n$query$\n\n"
                    "Answer using ONLY the retrieved materials above. "
                    "Cite sources inline with [Source: filename]."
                )
            },
            "inferenceConfig": {
                "textInferenceConfig": {
                    "maxTokens": 1024,
                    "temperature": 0.2,   # Low temp for factual grounding
                    "topP": 0.9,
                }
            },
        },
        "retrievalConfiguration": {
            "managedSearchConfiguration": {
                "numberOfResults": _NUM_RESULTS,
            }
        },
    }

    # Optionally attach guardrail config if configured
    if GUARDRAIL_ID:
        kb_config["generationConfiguration"]["guardrailConfiguration"] = {
            "guardrailId": GUARDRAIL_ID,
            "guardrailVersion": GUARDRAIL_VERSION,
        }

    request_body: dict = {
        "input": {"text": query},
        "retrieveAndGenerateConfiguration": {
            "type": "KNOWLEDGE_BASE",
            "knowledgeBaseConfiguration": kb_config,
        },
    }

    # Pass session ID for conversation continuity
    if session_id:
        request_body["sessionId"] = session_id

    try:
        response = _get_agent_runtime().retrieve_and_generate(**request_body)
    except ClientError as exc:
        error_code = exc.response["Error"]["Code"]
        log.error("bedrock_client_error", error_code=error_code, error=str(exc))
        if error_code in ("ValidationException", "ResourceNotFoundException"):
            return _error_response(
                "Course materials are temporarily unavailable. Please try again shortly."
            )
        raise
    except BotoCoreError as exc:
        log.error("bedrock_botocore_error", error=str(exc))
        return _error_response("Unable to reach the AI service. Please try again.")

    answer = response.get("output", {}).get("text", "").strip()
    citations = _extract_citations(response.get("citations", []))
    returned_session_id = response.get("sessionId", "")

    # Detect empty/fallback answer
    if not answer:
        answer = FALLBACK_RESPONSE

    log.info(
        "rag_retrieve_and_generate_complete",
        sources_count=len(citations),
        answer_length=len(answer),
        session_id=returned_session_id,
    )

    return {
        "answer": answer,
        "sources": citations,
        "session_id": returned_session_id,
        "tokens_used": 0,  # RetrieveAndGenerate doesn't expose token counts
    }


def retrieve(
    query: str,
    student_id: str = "",
) -> list[dict]:
    """Retrieve relevant course material chunks WITHOUT generating an answer.

    Used by ``chat_handler`` to get raw context, which is then passed to
    the Converse API call (with guardrails applied explicitly).

    Args:
        query: The student's question.
        student_id: For structured logging.

    Returns:
        List of chunk dicts, each with ``text``, ``source``, ``score`` keys.
        Returns empty list on retrieval failure (caller handles fallback).
    """
    log = logger.bind(student_id=student_id, query_preview=query[:80])
    log.info("rag_retrieve_start")

    if not KNOWLEDGE_BASE_ID:
        logger.error("knowledge_base_id_not_configured")
        return []

    try:
        response = _get_agent_runtime().retrieve(
            knowledgeBaseId=KNOWLEDGE_BASE_ID,
            retrievalQuery={"text": query},
            # No retrievalConfiguration — Managed KB uses its own defaults
        )
    except (ClientError, BotoCoreError) as exc:
        log.error("bedrock_retrieve_error", error=str(exc))
        return []

    chunks = _parse_retrieval_results(response.get("retrievalResults", []))

    log.info("rag_retrieve_complete", chunks_returned=len(chunks))
    return chunks


def build_converse_messages(
    query: str,
    retrieved_chunks: list[dict],
    conversation_history: Optional[list[dict]] = None,
    include_few_shots: bool = False,
) -> list[dict]:
    """Build the messages list for a Bedrock Converse API call.

    Combines (optionally) few-shot examples + truncated conversation history
    + the current query with injected context.

    Args:
        query: Current student question.
        retrieved_chunks: Chunks from ``retrieve()``.
        conversation_history: List of ``{role, content: [{text: ...}]}`` dicts,
            ordered oldest-first. Will be trimmed to the last ``_MAX_HISTORY_TURNS``.
        include_few_shots: Whether to prepend few-shot examples (first turn only).

    Returns:
        Messages list in Bedrock Converse format.
    """
    from backend.rag.prompt_templates import FEW_SHOT_EXAMPLES

    messages: list[dict] = []

    # Prepend few-shot examples on new sessions
    if include_few_shots:
        messages.extend(FEW_SHOT_EXAMPLES)

    # Trim history to last N turns (N*2 messages: user + assistant alternating)
    if conversation_history:
        max_messages = _MAX_HISTORY_TURNS * 2
        trimmed = conversation_history[-max_messages:]
        messages.extend(trimmed)

    # Current turn — inject retrieved context into user message
    user_content = build_user_message_with_context(query, retrieved_chunks)
    messages.append({"role": "user", "content": [{"text": user_content}]})

    return messages


# ── Citation helpers ──────────────────────────────────────────────────────────


def _extract_citations(citations: list[dict]) -> list[dict]:
    """Parse Bedrock citation objects into simple source dicts.

    Args:
        citations: Raw citation list from ``RetrieveAndGenerate`` response.

    Returns:
        Deduplicated list of ``{source, excerpt, score}`` dicts.
    """
    seen_sources: set[str] = set()
    sources: list[dict] = []

    for citation in citations:
        for ref in citation.get("retrievedReferences", []):
            location = ref.get("location", {})
            s3_uri = location.get("s3Location", {}).get("uri", "")
            filename = s3_uri.split("/")[-1] if s3_uri else "Course materials"

            # Deduplicate by source filename
            if filename in seen_sources:
                continue
            seen_sources.add(filename)

            excerpt = ref.get("content", {}).get("text", "")
            sources.append({
                "source": filename,
                "excerpt": excerpt[:300].strip(),
            })

    return sources


def _parse_retrieval_results(results: list[dict]) -> list[dict]:
    """Parse raw Retrieve API results into chunk dicts.

    Args:
        results: ``retrievalResults`` list from Bedrock Retrieve response.

    Returns:
        List of ``{text, source, score}`` dicts, sorted by score descending.
    """
    chunks: list[dict] = []
    for result in results:
        content = result.get("content", {}).get("text", "").strip()
        if not content:
            continue

        location = result.get("location", {})
        s3_uri = location.get("s3Location", {}).get("uri", "")
        source = s3_uri.split("/")[-1] if s3_uri else "Course materials"
        score = result.get("score", 0.0)

        chunks.append({"text": content, "source": source, "score": score})

    # Sort highest relevance first
    chunks.sort(key=lambda c: c["score"], reverse=True)
    return chunks


# ── Error helpers ─────────────────────────────────────────────────────────────


def _error_response(message: str) -> dict:
    """Return a safe error dict that callers can treat as a failed RAG result."""
    return {
        "answer": message,
        "sources": [],
        "session_id": "",
        "tokens_used": 0,
        "error": True,
    }
