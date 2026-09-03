"""Pydantic request/response models for the Chat API.

These models define the public contract of /api/chat endpoints.
Kept separate from internal domain models (backend/rag/*) so the
API surface can evolve independently.
"""

from typing import Optional

from pydantic import BaseModel, Field, field_validator


# ── Request models ────────────────────────────────────────────────────────────


class ChatRequest(BaseModel):
    """Body for POST /api/chat and POST /api/chat/stream."""

    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="The student's question or message.",
        examples=["What is the difference between a ReAct agent and a plan-and-execute agent?"],
    )
    session_id: Optional[str] = Field(
        default=None,
        max_length=64,
        description=(
            "Optional session ID to continue an existing conversation. "
            "Omit on the first message; include the returned value on subsequent turns."
        ),
    )
    include_web: bool = Field(
        default=False,
        description=(
            "When true, supplement the course materials with web search results "
            "(course materials are still used first). Defaults to false — "
            "course materials only."
        ),
    )

    @field_validator("message")
    @classmethod
    def message_must_not_be_blank(cls, v: str) -> str:
        """Reject whitespace-only messages."""
        if not v.strip():
            raise ValueError("Message must not be blank.")
        return v.strip()

    @field_validator("session_id")
    @classmethod
    def sanitize_session_id(cls, v: Optional[str]) -> Optional[str]:
        """Strip any non-alphanumeric/dash characters from session ID."""
        if v is None:
            return None
        sanitized = "".join(c for c in v if c.isalnum() or c == "-")
        return sanitized or None


# ── Response models ───────────────────────────────────────────────────────────


class SourceCitation(BaseModel):
    """A single cited source — a course-materials file or a web page."""

    source: str = Field(..., description="Filename or title of the source document.")
    excerpt: str = Field(
        default="",
        max_length=300,
        description="Short excerpt from the retrieved passage.",
    )
    url: Optional[str] = Field(
        default=None,
        description="Link to the source when it is a web result. Null for course materials.",
    )


class TokenUsage(BaseModel):
    """Bedrock token consumption for a single turn."""

    input: int = Field(default=0, ge=0, description="Tokens in the input (prompt + context).")
    output: int = Field(default=0, ge=0, description="Tokens in the generated response.")
    total: int = Field(default=0, ge=0, description="Total tokens consumed.")


class ChatResponse(BaseModel):
    """Response for POST /api/chat (non-streaming)."""

    answer: str = Field(..., description="The agent's grounded answer.")
    sources: list[SourceCitation] = Field(
        default_factory=list,
        description="Course material sources cited in the answer.",
    )
    session_id: str = Field(
        ...,
        description=(
            "Session ID for conversation continuity. "
            "Pass this back in the next ChatRequest.session_id."
        ),
    )
    tokens_used: TokenUsage = Field(
        default_factory=TokenUsage,
        description="Token consumption for this turn.",
    )
    guardrail_triggered: bool = Field(
        default=False,
        description="True if Bedrock Guardrails intervened and modified/blocked the response.",
    )


# ── SSE streaming models ──────────────────────────────────────────────────────


class StreamChunkType(str):
    """Discriminator values for SSE stream events."""
    CHUNK = "chunk"
    SOURCES = "sources"
    DONE = "done"
    ERROR = "error"


class StreamChunk(BaseModel):
    """A single SSE event in the chat stream.

    Events are discriminated by ``type``:

    - ``chunk``:   Incremental answer text. ``text`` is populated.
    - ``sources``: Final citations (sent once, after all text chunks). ``sources`` populated.
    - ``done``:    Stream complete. ``session_id`` and ``tokens_used`` populated.
    - ``error``:   Stream failed. ``message`` populated.
    """

    type: str = Field(
        ...,
        description="Event type: chunk | sources | done | error",
    )
    text: Optional[str] = Field(
        default=None,
        description="Incremental answer text (type=chunk only).",
    )
    sources: Optional[list[SourceCitation]] = Field(
        default=None,
        description="Source citations (type=sources only).",
    )
    session_id: Optional[str] = Field(
        default=None,
        description="Session ID (type=done only).",
    )
    tokens_used: Optional[TokenUsage] = Field(
        default=None,
        description="Token usage summary (type=done only).",
    )
    message: Optional[str] = Field(
        default=None,
        description="Error message (type=error only).",
    )
