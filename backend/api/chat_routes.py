"""Chat API routes — student Q&A endpoints.

Endpoints:
  POST /api/chat         — Standard (non-streaming) Q&A
  POST /api/chat/stream  — Streaming Q&A via Server-Sent Events (SSE)
"""

import asyncio
from typing import AsyncIterator

import structlog
from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse

from backend.api.models import (
    ChatRequest,
    ChatResponse,
    SourceCitation,
    TokenUsage,
)
from backend.auth.cognito import get_current_user
from backend.auth.models import StudentUser
from backend.rag.chat_handler import handle_chat, handle_chat_stream
from backend.tracking.repository import log_interaction

logger = structlog.get_logger()
router = APIRouter()


@router.post("/", response_model=ChatResponse)
async def chat(
    body: ChatRequest,
    current_user: StudentUser = Depends(get_current_user),
) -> ChatResponse:
    """Handle a student question — retrieve, guard, generate, track.

    Flow:
    1. Authenticate via JWT dependency.
    2. Delegate to ``chat_handler.handle_chat`` (retrieval + guardrails + Converse).
    3. Log interaction asynchronously (fire-and-forget).
    4. Return grounded answer with citations.

    Args:
        body: ``ChatRequest`` containing the student's message and optional session_id.
        current_user: Injected by the ``get_current_user`` dependency.

    Returns:
        ``ChatResponse`` with answer, sources, session_id, and token usage.
    """
    logger.info(
        "chat_request",
        student_id=current_user.id,
        session_id=body.session_id,
        query_length=len(body.message),
    )

    result = await handle_chat(
        query=body.message,
        student_id=current_user.id,
        session_id=body.session_id,
    )

    sources = [
        SourceCitation(
            source=s.get("source", ""),
            excerpt=s.get("excerpt", ""),
        )
        for s in result.get("sources", [])
    ]

    tokens = TokenUsage(
        input=result["tokens_used"]["input"],
        output=result["tokens_used"]["output"],
        total=result["tokens_used"]["total"],
    )

    # Fire-and-forget: log to DynamoDB without blocking the response
    asyncio.create_task(
        log_interaction(
            student_id=current_user.id,
            query=body.message,
            response=result["answer"],
            sources=[s.source for s in sources],
            tokens_input=tokens.input,
            tokens_output=tokens.output,
            guardrail_triggered=result.get("guardrail_triggered", False),
            violation_type=result.get("violation_type"),
        )
    )

    return ChatResponse(
        answer=result["answer"],
        sources=sources,
        session_id=result["session_id"],
        tokens_used=tokens,
        guardrail_triggered=result.get("guardrail_triggered", False),
    )


@router.post("/stream")
async def chat_stream(
    body: ChatRequest,
    current_user: StudentUser = Depends(get_current_user),
) -> StreamingResponse:
    """Streaming Q&A via Server-Sent Events.

    Emits a series of SSE events:
      ``data: {"type": "chunk",   "text": "..."}``
      ``data: {"type": "sources", "sources": [...]}``
      ``data: {"type": "done",    "session_id": "...", "tokens_used": {...}}``

    On guardrail intervention or error:
      ``data: {"type": "chunk",   "text": "<guardrail message>"}``
      ``data: {"type": "error",   "message": "..."}``

    The client must include the session_id from the ``done`` event in
    subsequent requests to maintain conversation continuity.

    Args:
        body: ``ChatRequest`` with message and optional session_id.
        current_user: Injected by ``get_current_user``.

    Returns:
        ``StreamingResponse`` with ``text/event-stream`` content type.
    """
    logger.info(
        "chat_stream_request",
        student_id=current_user.id,
        session_id=body.session_id,
        query_length=len(body.message),
    )

    async def event_generator() -> AsyncIterator[str]:
        full_answer_parts: list[str] = []
        sources_sent: list[dict] = []
        session_id_out: str = body.session_id or ""
        tokens_total: int = 0
        guardrail_hit: bool = False

        async for sse_line in handle_chat_stream(
            query=body.message,
            student_id=current_user.id,
            session_id=body.session_id,
        ):
            yield sse_line

            # Parse for logging / fire-and-forget tracking
            if sse_line.startswith("data: "):
                try:
                    import json
                    event = json.loads(sse_line[6:])
                    event_type = event.get("type")
                    if event_type == "chunk":
                        full_answer_parts.append(event.get("text", ""))
                    elif event_type == "sources":
                        sources_sent = event.get("sources", [])
                    elif event_type == "done":
                        session_id_out = event.get("session_id", "")
                        tokens_total = event.get("tokens_used", {}).get("total", 0)
                    elif event_type == "error":
                        guardrail_hit = True
                except (ValueError, KeyError):
                    pass

        # Log after stream completes
        if full_answer_parts or guardrail_hit:
            full_answer = "".join(full_answer_parts)
            await log_interaction(
                student_id=current_user.id,
                query=body.message,
                response=full_answer,
                sources=[s.get("source", "") for s in sources_sent],
                tokens_input=tokens_total // 2,
                tokens_output=tokens_total // 2,
                guardrail_triggered=guardrail_hit,
            )

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            # Prevent proxy/CDN buffering
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )
