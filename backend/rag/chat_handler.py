"""Chat handler — orchestrates retrieval → guardrails → generation.

This module sits between the API routes and the Bedrock services.
It owns conversation history management and decides which retrieval
path to use:

- For standard (non-streaming) requests: ``retrieve`` + Converse API
  so guardrails can be applied with full trace visibility.

- For streaming requests: ``retrieve`` + ``converse_stream`` API,
  yielding SSE-compatible chunks.

Conversation history is stored in-process in a session map. For
multi-instance/Lambda deployments this should be replaced with a
DynamoDB or ElastiCache session store — that is a Phase 2 item.
"""

import asyncio
import json
import os
import time
import uuid
from collections import OrderedDict
from typing import AsyncIterator, Optional

import boto3
import structlog
from botocore.exceptions import BotoCoreError, ClientError

from backend.guardrails.config import GUARDRAIL_ID, GUARDRAIL_VERSION, POLICY
from backend.rag.knowledge_base import (
    BEDROCK_REGION,
    MODEL_ARN,
    build_converse_messages,
    retrieve,
    retrieve_and_generate,
)
from backend.rag.prompt_templates import (
    CONVERSE_SYSTEM_PROMPT,
    FALLBACK_RESPONSE,
    OUT_OF_SCOPE_RESPONSE,
    SERVICE_ERROR_RESPONSE,
)

# Bedrock runtime client — owned by chat_handler, separate from knowledge_base client
_bedrock_runtime: Optional[boto3.client] = None


def _get_bedrock_runtime() -> boto3.client:
    """Return a cached bedrock-runtime client for Converse API calls."""
    global _bedrock_runtime
    if _bedrock_runtime is None:
        _bedrock_runtime = boto3.client("bedrock-runtime", region_name=BEDROCK_REGION)
    return _bedrock_runtime

logger = structlog.get_logger()

# ── Session store ─────────────────────────────────────────────────────────────
# Simple LRU-bounded dict: session_id → list of Converse-format messages.
# Max 500 sessions × ~5KB each ≈ 2.5 MB RAM.
_MAX_SESSIONS = 500
_SESSION_TTL_SECONDS = 3600  # 1 hour idle expiry

# OrderedDict used as a simple LRU cache
_sessions: OrderedDict[str, dict] = OrderedDict()


def _get_session(session_id: str) -> dict:
    """Return the session dict, creating it if absent.

    Each session dict holds:
      - ``history``: Converse-format message list
      - ``last_active``: Unix timestamp
      - ``turn_count``: Number of completed turns
    """
    _evict_expired_sessions()

    if session_id not in _sessions:
        _sessions[session_id] = {
            "history": [],
            "last_active": time.time(),
            "turn_count": 0,
        }
    else:
        # Move to end (most recently used)
        _sessions.move_to_end(session_id)
        _sessions[session_id]["last_active"] = time.time()

    return _sessions[session_id]


def _evict_expired_sessions() -> None:
    """Remove sessions that have been idle for more than _SESSION_TTL_SECONDS
    and enforce the maximum session count.
    """
    cutoff = time.time() - _SESSION_TTL_SECONDS
    expired = [sid for sid, s in _sessions.items() if s["last_active"] < cutoff]
    for sid in expired:
        del _sessions[sid]

    # Enforce max by evicting oldest
    while len(_sessions) >= _MAX_SESSIONS:
        _sessions.popitem(last=False)


def _append_turn(session: dict, user_text: str, assistant_text: str) -> None:
    """Add a completed turn to the session history."""
    session["history"].extend(
        [
            {"role": "user", "content": [{"text": user_text}]},
            {"role": "assistant", "content": [{"text": assistant_text}]},
        ]
    )
    session["turn_count"] += 1


# ── Main handler ──────────────────────────────────────────────────────────────


async def handle_chat(
    query: str,
    student_id: str,
    session_id: Optional[str] = None,
) -> dict:
    """Handle a single chat turn: Retrieve from Managed KB + Converse for generation."""
    log = logger.bind(student_id=student_id, query_preview=query[:80])

    if not session_id:
        session_id = str(uuid.uuid4())
        log.info("chat_new_session", session_id=session_id)

    log.info("rag_retrieve_start")

    try:
        # Step 1: Retrieve from Managed KB (no retrievalConfiguration needed)
        chunks = await asyncio.get_event_loop().run_in_executor(
            None, retrieve, query, student_id
        )

        # Step 2: Build prompt with retrieved context
        if chunks:
            context = "\n\n".join([f"[Source: {c.get('source','unknown')}]\n{c.get('text','')}" for c in chunks[:5]])
            user_message = f"Using the following course materials:\n\n{context}\n\nStudent question: {query}"
        else:
            user_message = f"Student question: {query}\n\nNote: No specific course material was found for this question."

        messages = [{"role": "user", "content": [{"text": user_message}]}]
        system = [{"text": "You are an expert teaching assistant for an Agentic AI course. Answer questions grounded in the provided course materials. If materials are insufficient, say so honestly."}]

        # Step 3: Generate with Converse API (EU cross-region inference profile)
        raw = await asyncio.get_event_loop().run_in_executor(
            None, _call_converse, messages, student_id
        )

        stop_reason = raw.get("stopReason", "")
        if stop_reason == "guardrail_intervened":
            return {
                "answer": POLICY.denial_message,
                "sources": [c.get("source","") for c in chunks],
                "session_id": session_id,
                "tokens_used": {"input": 0, "output": 0, "total": 0},
                "guardrail_triggered": True,
                "violation_type": "guardrail_intervened",
            }

        content_blocks = raw.get("output", {}).get("message", {}).get("content", [])
        answer = next((b["text"] for b in content_blocks if "text" in b), "")
        usage = raw.get("usage", {})

        return {
            "answer": answer or FALLBACK_RESPONSE,
            "sources": [{"source": c.get("source",""), "excerpt": c.get("text","")[:200]} for c in chunks[:3]],
            "session_id": session_id,
            "tokens_used": {
                "input": usage.get("inputTokens", 0),
                "output": usage.get("outputTokens", 0),
                "total": usage.get("totalTokens", 0),
            },
            "guardrail_triggered": False,
            "violation_type": None,
        }

    except (ClientError, BotoCoreError) as e:
        # Bedrock/AWS service failure (throttling, model unavailable, invalid
        # request, transient network). This is NOT "the answer isn't in the
        # materials" — surface a distinct, honest error so the student knows to
        # retry and so ops can see a real failure in the logs.
        error_code = (
            e.response.get("Error", {}).get("Code")
            if isinstance(e, ClientError)
            else type(e).__name__
        )
        log.error("chat_service_error", error_code=error_code, error=str(e))
        return _service_error_result(session_id)

    except Exception as e:  # noqa: BLE001 — last-resort guard
        # Any other unexpected error is still a system problem, not a content
        # gap. Return the service-error message rather than the "not in the
        # materials" fallback so the two are never conflated.
        log.error("chat_unexpected_error", error_type=type(e).__name__, error=str(e))
        return _service_error_result(session_id)


async def handle_chat_stream(
    query: str,
    student_id: str,
    session_id: Optional[str] = None,
) -> AsyncIterator[str]:
    """Handle a chat turn with streaming via SSE.

    Yields SSE-formatted strings:
      - ``data: {"type": "chunk", "text": "..."}`` — incremental text
      - ``data: {"type": "sources", "sources": [...]}`` — final citations
      - ``data: {"type": "done", "session_id": "...", "tokens_used": {...}}``
      - ``data: {"type": "error", "message": "..."}`` — on failure

    Args:
        query: Student's question.
        student_id: Cognito sub for logging.
        session_id: Existing session ID, or None to start a new one.

    Yields:
        SSE data lines (including the ``data: `` prefix and double newline).
    """
    log = logger.bind(student_id=student_id, query_preview=query[:80])

    if not session_id:
        session_id = str(uuid.uuid4())
        log.info("stream_new_session", session_id=session_id)
    session = _get_session(session_id)
    is_first_turn = session["turn_count"] == 0

    # Retrieve chunks (sync call, run in executor)
    chunks = await asyncio.get_event_loop().run_in_executor(
        None, retrieve, query, student_id
    )

    messages = build_converse_messages(
        query=query,
        retrieved_chunks=chunks,
        conversation_history=session["history"],
        include_few_shots=is_first_turn,
    )

    # Call converse_stream in executor
    try:
        stream_response = await asyncio.get_event_loop().run_in_executor(
            None,
            _call_converse_stream,
            messages,
            student_id,
        )
    except (ClientError, BotoCoreError) as exc:
        log.error("converse_stream_api_error", error=str(exc))
        yield _sse({"type": "error", "message": "AI service unavailable. Please try again."})
        return

    full_answer_parts: list[str] = []
    tokens: dict = _zero_tokens()

    try:
        event_stream = stream_response.get("stream", [])
        for event in event_stream:
            # Incremental text delta
            if "contentBlockDelta" in event:
                delta = event["contentBlockDelta"].get("delta", {})
                text_chunk = delta.get("text", "")
                if text_chunk:
                    full_answer_parts.append(text_chunk)
                    yield _sse({"type": "chunk", "text": text_chunk})

            # Stream metadata (token usage, stop reason)
            elif "messageStop" in event:
                stop_reason = event["messageStop"].get("stopReason", "")
                if stop_reason == "guardrail_intervened":
                    # Discard accumulated chunks, send guardrail message
                    full_answer_parts.clear()
                    yield _sse({"type": "chunk", "text": POLICY.denial_message})
                    yield _sse({"type": "done", "session_id": session_id, "tokens_used": tokens})
                    return

            elif "metadata" in event:
                usage = event["metadata"].get("usage", {})
                tokens = {
                    "input": usage.get("inputTokens", 0),
                    "output": usage.get("outputTokens", 0),
                    "total": usage.get("inputTokens", 0) + usage.get("outputTokens", 0),
                }

    except Exception as exc:
        log.error("stream_processing_error", error=str(exc))
        yield _sse({"type": "error", "message": "Stream interrupted. Please retry."})
        return

    full_answer = "".join(full_answer_parts).strip() or FALLBACK_RESPONSE

    # Citations
    sources = [
        {"source": c["source"], "excerpt": c["text"][:200]}
        for c in chunks
        if c.get("score", 0) > 0.4
    ]

    # Persist to session history
    _append_turn(session, query, full_answer)

    log.info(
        "stream_turn_complete",
        session_id=session_id,
        turn=session["turn_count"],
        tokens_total=tokens["total"],
    )

    yield _sse({"type": "sources", "sources": sources})
    yield _sse({"type": "done", "session_id": session_id, "tokens_used": tokens})


# ── Bedrock call helpers ──────────────────────────────────────────────────────


def _call_converse(messages: list[dict], student_id: str) -> dict:
    """Synchronous Converse API call with guardrails.

    Separated into its own function so it can be run in an executor.
    """
    request: dict = {
        "modelId": MODEL_ARN,
        "messages": messages,
        "system": [{"text": CONVERSE_SYSTEM_PROMPT}],
        # Only set temperature (low, for factual grounding). Newer Claude
        # models reject specifying both temperature and topP in Converse.
        "inferenceConfig": {
            "maxTokens": 1024,
            "temperature": 0.2,
        },
    }

    if GUARDRAIL_ID:
        request["guardrailConfig"] = {
            "guardrailIdentifier": GUARDRAIL_ID,
            "guardrailVersion": GUARDRAIL_VERSION,
            "trace": "enabled",
        }

    return _get_bedrock_runtime().converse(**request)


def _call_converse_stream(messages: list[dict], student_id: str) -> dict:
    """Synchronous converse_stream call — returns the streaming response object."""
    request: dict = {
        "modelId": MODEL_ARN,
        "messages": messages,
        "system": [{"text": CONVERSE_SYSTEM_PROMPT}],
        # Only set temperature — newer Claude models reject temperature+topP
        # together in Converse.
        "inferenceConfig": {
            "maxTokens": 1024,
            "temperature": 0.2,
        },
    }

    if GUARDRAIL_ID:
        request["guardrailConfig"] = {
            "guardrailIdentifier": GUARDRAIL_ID,
            "guardrailVersion": GUARDRAIL_VERSION,
            "trace": "enabled",
        }

    return _get_bedrock_runtime().converse_stream(**request)


# ── Response parsing helpers ──────────────────────────────────────────────────


def _extract_answer(response: dict) -> str:
    """Pull text from the first content block of a Converse response."""
    output = response.get("output", {})
    message = output.get("message", {})
    content = message.get("content", [])
    for block in content:
        if "text" in block:
            return block["text"].strip()
    return ""


def _extract_token_usage(response: dict) -> dict:
    """Extract token counts from a Converse API response."""
    usage = response.get("usage", {})
    input_tokens = usage.get("inputTokens", 0)
    output_tokens = usage.get("outputTokens", 0)
    return {
        "input": input_tokens,
        "output": output_tokens,
        "total": input_tokens + output_tokens,
    }


def _extract_violation_type(trace: dict) -> str:
    """Best-effort extraction of guardrail violation category from trace."""
    if trace.get("inputAssessment", {}).get("topicPolicy"):
        return "topic_denial"
    if trace.get("inputAssessment", {}).get("contentPolicy"):
        return "content_filter"
    if trace.get("inputAssessment", {}).get("sensitiveInformationPolicy"):
        return "pii_detected"
    return "unknown"


def _zero_tokens() -> dict:
    return {"input": 0, "output": 0, "total": 0}


def _service_error_result(session_id: str) -> dict:
    """Result for a system/service failure (distinct from a content gap).

    Carries ``error=True`` so callers/logs can tell this apart from a normal
    answer, while still returning a friendly, retry-oriented message.
    """
    return {
        "answer": SERVICE_ERROR_RESPONSE,
        "sources": [],
        "session_id": session_id,
        "tokens_used": {"input": 0, "output": 0, "total": 0},
        "guardrail_triggered": False,
        "violation_type": None,
        "error": True,
    }


def _build_result(
    *,
    answer: str,
    sources: list[dict],
    session_id: str,
    tokens_used: dict,
    guardrail_triggered: bool,
    violation_type: Optional[str] = None,
) -> dict:
    return {
        "answer": answer,
        "sources": sources,
        "session_id": session_id,
        "tokens_used": tokens_used,
        "guardrail_triggered": guardrail_triggered,
        "violation_type": violation_type,
    }


def _sse(payload: dict) -> str:
    """Format a dict as an SSE data line."""
    return f"data: {json.dumps(payload)}\n\n"
