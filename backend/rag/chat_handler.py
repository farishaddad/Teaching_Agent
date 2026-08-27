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
)
from backend.rag.prompt_templates import (
    CONVERSE_SYSTEM_PROMPT,
    FALLBACK_RESPONSE,
    OUT_OF_SCOPE_RESPONSE,
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
    """Handle a single chat turn synchronously.

    Flow:
    1. Resolve or create session.
    2. Retrieve relevant chunks from Bedrock KB.
    3. Build Converse API messages with history + context.
    4. Call Converse API with guardrails.
    5. Detect guardrail interventions and empty answers.
    6. Update session history.
    7. Return response dict.

    Args:
        query: Student's question.
        student_id: Cognito sub for logging.
        session_id: Existing session ID, or None to create a new one.

    Returns:
        Dict with:
          - ``answer``: Response text
          - ``sources``: List of citation dicts
          - ``session_id``: Session ID (new or existing)
          - ``tokens_used``: Dict with input/output/total counts
          - ``guardrail_triggered``: bool
          - ``violation_type``: str or None
    """
    log = logger.bind(student_id=student_id, query_preview=query[:80])

    # Resolve session
    if not session_id:
        session_id = str(uuid.uuid4())
        log.info("chat_new_session", session_id=session_id)
    session = _get_session(session_id)
    is_first_turn = session["turn_count"] == 0

    # Step 1: Retrieve relevant chunks (run in thread pool — sync boto3 call)
    chunks = await asyncio.get_event_loop().run_in_executor(
        None, retrieve, query, student_id
    )

    # Step 2: Build messages list
    messages = build_converse_messages(
        query=query,
        retrieved_chunks=chunks,
        conversation_history=session["history"],
        include_few_shots=is_first_turn,
    )

    # Step 3: Call Converse API with guardrails (in thread pool)
    try:
        raw_response = await asyncio.get_event_loop().run_in_executor(
            None,
            _call_converse,
            messages,
            student_id,
        )
    except (ClientError, BotoCoreError) as exc:
        log.error("converse_api_error", error=str(exc))
        return _build_result(
            answer="I'm having trouble connecting to the AI service. Please try again in a moment.",
            sources=[],
            session_id=session_id,
            tokens_used=_zero_tokens(),
            guardrail_triggered=False,
        )

    # Step 4: Handle guardrail intervention
    if raw_response.get("stopReason") == "guardrail_intervened":
        trace = raw_response.get("trace", {}).get("guardrail", {})
        violation_type = _extract_violation_type(trace)
        log.warning(
            "guardrail_triggered",
            violation_type=violation_type,
            session_id=session_id,
        )
        return _build_result(
            answer=POLICY.denial_message,
            sources=[],
            session_id=session_id,
            tokens_used=_zero_tokens(),
            guardrail_triggered=True,
            violation_type=violation_type,
        )

    # Step 5: Extract answer text
    answer = _extract_answer(raw_response)
    if not answer:
        answer = FALLBACK_RESPONSE

    # Step 6: Extract token usage
    tokens = _extract_token_usage(raw_response)

    # Step 7: Derive citations from the chunks used
    sources = [
        {"source": c["source"], "excerpt": c["text"][:200]}
        for c in chunks
        if c.get("score", 0) > 0.4  # Only cite reasonably relevant chunks
    ]

    # Step 8: Persist turn in session history
    _append_turn(session, query, answer)

    log.info(
        "chat_turn_complete",
        session_id=session_id,
        turn=session["turn_count"],
        sources_count=len(sources),
        tokens_total=tokens["total"],
    )

    return _build_result(
        answer=answer,
        sources=sources,
        session_id=session_id,
        tokens_used=tokens,
        guardrail_triggered=False,
    )


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
        "modelId": MODEL_ARN.split("/")[-1]
        if MODEL_ARN.startswith("arn:")
        else MODEL_ARN,
        "messages": messages,
        "system": [{"text": CONVERSE_SYSTEM_PROMPT}],
        "inferenceConfig": {
            "maxTokens": 1024,
            "temperature": 0.2,
            "topP": 0.9,
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
        "modelId": MODEL_ARN.split("/")[-1]
        if MODEL_ARN.startswith("arn:")
        else MODEL_ARN,
        "messages": messages,
        "system": [{"text": CONVERSE_SYSTEM_PROMPT}],
        "inferenceConfig": {
            "maxTokens": 1024,
            "temperature": 0.2,
            "topP": 0.9,
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
