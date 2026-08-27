"""Chat API routes — the core student Q&A endpoint."""

import asyncio

import structlog
from fastapi import APIRouter, Request
from pydantic import BaseModel, Field

from backend.guardrails.middleware import apply_guardrails_to_converse
from backend.rag.knowledge_base import retrieve_and_generate
from backend.tracking.repository import log_interaction

logger = structlog.get_logger()
router = APIRouter()


class ChatRequest(BaseModel):
    """Student chat message."""

    message: str = Field(..., min_length=1, max_length=2000, description="Student's question")


class ChatResponse(BaseModel):
    """Agent response with citations."""

    answer: str
    sources: list[dict] = []
    guardrail_triggered: bool = False


@router.post("/", response_model=ChatResponse)
async def chat(request: Request, body: ChatRequest):
    """Handle a student question — retrieve, guard, generate, track.

    Flow:
    1. Extract student identity from JWT (via middleware)
    2. Retrieve relevant course materials (RAG)
    3. Generate answer with guardrails applied
    4. Log interaction asynchronously
    5. Return grounded answer with sources
    """
    student = request.state.current_user
    logger.info("chat_request", student_id=student.id, query_length=len(body.message))

    # Step 1: RAG — retrieve relevant course materials and generate answer
    rag_result = retrieve_and_generate(
        query=body.message,
        student_id=student.id,
    )

    # Check if RAG itself returned an error
    if "error" in rag_result:
        return ChatResponse(
            answer=rag_result["answer"],
            sources=[],
            guardrail_triggered=False,
        )

    # Note: When using RetrieveAndGenerate, guardrails are applied via the
    # guardrailConfig in the Converse API call within the KB configuration.
    # For the MVP, guardrails are configured at the KB level.
    # For more control, use Retrieve + separate Converse call with guardrails.

    answer = rag_result["answer"]
    sources = rag_result.get("sources", [])

    # Step 2: Log interaction (fire-and-forget — don't block response)
    asyncio.create_task(
        log_interaction(
            student_id=student.id,
            query=body.message,
            response=answer,
            sources=[s.get("source", "") for s in sources],
            tokens_used=0,  # TODO: Extract from response metadata
            guardrail_triggered=False,
        )
    )

    return ChatResponse(
        answer=answer,
        sources=sources,
        guardrail_triggered=False,
    )
