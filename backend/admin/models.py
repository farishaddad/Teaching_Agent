"""Pydantic models for the Admin dashboard API."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, EmailStr


# ─── Student Management ───────────────────────────────────────────────

class StudentCreate(BaseModel):
    """Request to create a new student account."""

    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    cohort: str = Field(..., description="Cohort identifier e.g. 'cohort-2026-q3'")
    temporary_password: Optional[str] = Field(
        None,
        min_length=8,
        description="If omitted, Cognito generates one and emails the student",
    )


class StudentUpdate(BaseModel):
    """Request to update student details."""

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    cohort: Optional[str] = None
    enabled: Optional[bool] = None  # Disable/enable account


class StudentProfile(BaseModel):
    """Full student profile returned from admin queries."""

    student_id: str
    email: str
    first_name: str
    last_name: str
    cohort: str
    enrollment_date: str
    enabled: bool = True
    last_login: Optional[str] = None
    total_interactions: int = 0
    total_tokens_used: int = 0


class StudentBulkCreate(BaseModel):
    """Bulk-create students from a CSV upload."""

    students: list[StudentCreate]


# ─── Course Materials (RAG S3 bucket) ─────────────────────────────────

class MaterialItem(BaseModel):
    """A single object in the course-materials S3 bucket."""

    key: str
    size: int
    last_modified: str


class MaterialList(BaseModel):
    """Listing of course materials."""

    bucket: str
    items: list[MaterialItem]
    count: int


class PresignUploadRequest(BaseModel):
    """Request a presigned URL to upload a course-material file."""

    filename: str = Field(..., min_length=1, max_length=255)
    content_type: str = Field(..., min_length=1, max_length=128)
    prefix: str = Field("", max_length=128, description="Optional key prefix, e.g. 'modules/'")


class PresignUploadResponse(BaseModel):
    """Presigned upload details the browser uses to PUT the file to S3."""

    url: str
    key: str
    method: str
    headers: dict
    expires_in: int
    max_bytes: int


# ─── Interaction Analytics ────────────────────────────────────────────

class InteractionSummary(BaseModel):
    """Summary of a single student interaction for admin view."""

    interaction_id: str
    timestamp: str
    query: str
    response_summary: str
    topic_detected: Optional[str] = None
    guardrail_triggered: bool = False
    violation_type: Optional[str] = None
    tokens_used: int = 0


class StudentInteractionHistory(BaseModel):
    """Paginated interaction history for a student."""

    student_id: str
    student_name: str
    interactions: list[InteractionSummary]
    total_count: int
    page: int
    page_size: int


# ─── Progress & Weakness Analysis ────────────────────────────────────

class TopicProgress(BaseModel):
    """A student's engagement with a specific course topic."""

    topic_slug: str
    topic_name: str
    questions_asked: int
    unique_sessions: int
    avg_follow_up_depth: float  # How many follow-ups per initial question
    confidence_score: float  # 0.0 - 1.0 derived from engagement pattern
    last_accessed: Optional[str] = None
    weakness_flag: bool = False  # True if student struggles here


class StudentProgressReport(BaseModel):
    """Full progress report for a student."""

    student_id: str
    student_name: str
    cohort: str
    enrollment_date: str
    total_questions: int
    total_sessions: int
    active_days: int
    topics: list[TopicProgress]
    weaknesses: list[TopicProgress]  # Topics with low confidence / repeat basic questions
    strengths: list[TopicProgress]  # Topics with high confidence / advanced questions
    engagement_trend: list[dict]  # [{date, questions_asked, time_spent_mins}]


# ─── Overall Metrics / Cost Tracking ─────────────────────────────────

class DailyMetrics(BaseModel):
    """Aggregate metrics for a single day."""

    date: str
    total_questions: int
    unique_students: int
    total_tokens_input: int
    total_tokens_output: int
    total_tokens: int
    estimated_bedrock_cost_usd: float
    guardrail_triggers: int
    avg_response_time_ms: int


class CostBreakdown(BaseModel):
    """AWS cost breakdown for the Teaching Agent."""

    period_start: str
    period_end: str
    bedrock_converse_cost: float  # LLM inference
    bedrock_kb_cost: float  # Knowledge Base retrieval
    bedrock_guardrails_cost: float  # Guardrail evaluations
    dynamodb_cost: float  # Read/write units
    lambda_cost: float  # Compute
    api_gateway_cost: float  # Requests
    s3_cost: float  # Course material storage
    cognito_cost: float  # MAU pricing
    total_cost: float
    cost_per_student: float
    cost_per_interaction: float


class OverallDashboard(BaseModel):
    """Top-level dashboard data for the admin."""

    total_students: int
    active_students_7d: int
    total_interactions: int
    total_tokens_used: int
    estimated_monthly_cost_usd: float
    guardrail_trigger_rate: float  # Percentage of interactions that triggered guardrails
    avg_questions_per_student: float
    daily_metrics: list[DailyMetrics]  # Last 30 days
    top_topics: list[dict]  # [{topic, question_count}]
    common_weaknesses: list[dict]  # [{topic, student_count, avg_confidence}]
