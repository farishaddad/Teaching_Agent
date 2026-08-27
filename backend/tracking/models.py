"""DynamoDB entity models for the tracking module — single-table design."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class InteractionRecord(BaseModel):
    """A single student-agent interaction stored in DynamoDB."""

    student_id: str  # PK: STU#{student_id}
    # SK: INT#{iso_timestamp}#{ulid}
    timestamp: str
    interaction_id: str
    query: str  # Truncated to 500 chars
    response_summary: str  # First 500 chars
    sources_used: list[str] = []
    tokens_input: int = 0
    tokens_output: int = 0
    tokens_total: int = 0
    topic_detected: Optional[str] = None
    session_id: Optional[str] = None
    guardrail_triggered: bool = False
    violation_type: Optional[str] = None
    response_time_ms: int = 0


class ProgressRecord(BaseModel):
    """Per-topic engagement record for a student."""

    student_id: str  # PK: STU#{student_id}
    # SK: PRG#{topic_slug}
    topic_slug: str
    topic_name: str
    questions_asked: int = 0
    unique_sessions: int = 0
    avg_follow_up_depth: float = 0.0
    confidence_score: float = 0.0
    last_accessed: Optional[str] = None
    weakness_flag: bool = False


class DailySummary(BaseModel):
    """Daily aggregate for a student."""

    student_id: str  # PK: STU#{student_id}
    # SK: DAY#{yyyy-mm-dd}
    date: str
    total_questions: int = 0
    topics_explored: list[str] = []
    time_spent_seconds: int = 0
    tokens_used: int = 0


class StudentProgressResponse(BaseModel):
    """Response model for the student-facing progress endpoint."""

    student_id: str
    total_questions: int
    total_sessions: int
    active_days: int
    topics: list[ProgressRecord] = []
    weaknesses: list[ProgressRecord] = []
    strengths: list[ProgressRecord] = []
    recent_topics: list[str] = []
