"""Admin API routes — student management, analytics, and dashboard.

All admin routes require the requesting user to be in the 'instructors' Cognito group.
"""

from typing import Optional

import structlog
from fastapi import APIRouter, Depends, HTTPException, Request, Query

from backend.admin.analytics import get_cost_breakdown, get_overall_dashboard, get_student_progress
from backend.admin.models import (
    CostBreakdown,
    OverallDashboard,
    StudentBulkCreate,
    StudentCreate,
    StudentInteractionHistory,
    StudentProfile,
    StudentProgressReport,
    StudentUpdate,
)
from backend.admin.student_manager import (
    bulk_create_students,
    create_student,
    disable_student,
    get_student,
    list_students,
    reset_student_password,
    update_student,
)

logger = structlog.get_logger()
router = APIRouter()


# ─── Authorization Dependency ─────────────────────────────────────────

async def require_instructor(request: Request):
    """Verify the requesting user is in the 'instructors' Cognito group.

    The JWT includes `cognito:groups` claim when the user belongs to groups.
    Only users in 'instructors' group can access admin endpoints.
    """
    user = request.state.current_user
    # In production, check cognito:groups from the decoded JWT
    # For now, check if the user's email matches admin list or group membership
    # This would be implemented via a custom JWT claim or group check
    groups = getattr(user, "groups", []) or []
    if "instructors" not in groups:
        # Fallback: check against admin email list (env var)
        import os
        admin_emails = os.environ.get("ADMIN_EMAILS", "").split(",")
        if user.email not in admin_emails:
            raise HTTPException(
                status_code=403,
                detail="Access denied. Instructor privileges required.",
            )


# ─── Dashboard ────────────────────────────────────────────────────────

@router.get("/dashboard", response_model=OverallDashboard)
async def dashboard(
    request: Request,
    days: int = Query(30, ge=1, le=90, description="Number of days to include"),
    _: None = Depends(require_instructor),
):
    """Get the overall admin dashboard metrics.

    Returns: total students, active students, interactions, token usage,
    estimated costs, guardrail trigger rate, daily metrics, top topics,
    and common student weaknesses.
    """
    return await get_overall_dashboard(days=days)


# ─── Student Management ───────────────────────────────────────────────

@router.get("/students", response_model=list[StudentProfile])
async def list_all_students(
    request: Request,
    cohort: Optional[str] = Query(None, description="Filter by cohort"),
    limit: int = Query(50, ge=1, le=200),
    _: None = Depends(require_instructor),
):
    """List all students, optionally filtered by cohort."""
    return await list_students(cohort=cohort, limit=limit)


@router.post("/students", response_model=StudentProfile, status_code=201)
async def create_new_student(
    request: Request,
    student: StudentCreate,
    _: None = Depends(require_instructor),
):
    """Create a single student account.

    If temporary_password is provided, the student must change it on first login.
    If omitted, Cognito sends an invitation email with a generated password.
    """
    return await create_student(student)


@router.post("/students/bulk", status_code=201)
async def bulk_create(
    request: Request,
    body: StudentBulkCreate,
    _: None = Depends(require_instructor),
):
    """Bulk-create student accounts from a list.

    Returns per-student results: created, already_exists, or failed.
    """
    results = await bulk_create_students(body.students)
    return {"created": sum(1 for r in results if r["status"] == "created"), "results": results}


@router.get("/students/{student_id}", response_model=StudentProfile)
async def get_student_detail(
    request: Request,
    student_id: str,
    _: None = Depends(require_instructor),
):
    """Get full profile for a specific student."""
    return await get_student(student_id)


@router.patch("/students/{student_id}", response_model=StudentProfile)
async def update_student_detail(
    request: Request,
    student_id: str,
    update: StudentUpdate,
    _: None = Depends(require_instructor),
):
    """Update a student's profile (name, cohort, enabled status)."""
    return await update_student(student_id, update)


@router.post("/students/{student_id}/disable")
async def disable_student_account(
    request: Request,
    student_id: str,
    _: None = Depends(require_instructor),
):
    """Disable a student account (revoke access without deleting data)."""
    return await disable_student(student_id)


@router.post("/students/{student_id}/reset-password")
async def reset_password(
    request: Request,
    student_id: str,
    _: None = Depends(require_instructor),
):
    """Trigger a password reset email for a student."""
    return await reset_student_password(student_id)


# ─── Student Progress & Weakness Analysis ────────────────────────────

@router.get("/students/{student_id}/progress", response_model=StudentProgressReport)
async def student_progress(
    request: Request,
    student_id: str,
    _: None = Depends(require_instructor),
):
    """Get detailed progress report for a student.

    Includes:
    - Topics engaged with (and depth of engagement)
    - Identified weaknesses (repeated basic questions, low confidence)
    - Strengths (advanced questions, high engagement depth)
    - Engagement trend over time
    """
    report = await get_student_progress(student_id)

    # Enrich with Cognito data
    try:
        profile = await get_student(student_id)
        report.student_name = f"{profile.first_name} {profile.last_name}"
        report.cohort = profile.cohort
        report.enrollment_date = profile.enrollment_date
    except Exception:
        pass

    return report


@router.get("/students/{student_id}/interactions", response_model=StudentInteractionHistory)
async def student_interactions(
    request: Request,
    student_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=5, le=100),
    _: None = Depends(require_instructor),
):
    """Get paginated interaction history for a student.

    Shows every question asked, response summary, topic detected,
    and whether guardrails were triggered.
    """
    from backend.admin.analytics import table as tracking_table
    from backend.admin.models import InteractionSummary

    # Query interactions with pagination
    response = tracking_table.query(
        KeyConditionExpression="PK = :pk AND begins_with(SK, :prefix)",
        ExpressionAttributeValues={
            ":pk": f"STU#{student_id}",
            ":prefix": "INT#",
        },
        ScanIndexForward=False,  # Most recent first
        Limit=page_size,
    )

    items = response.get("Items", [])
    interactions = [
        InteractionSummary(
            interaction_id=item.get("SK", "").split("#")[-1],
            timestamp=item.get("SK", "").split("#")[1] if "#" in item.get("SK", "") else "",
            query=item.get("query", ""),
            response_summary=item.get("response_summary", ""),
            topic_detected=item.get("topic_detected"),
            guardrail_triggered=item.get("guardrail_triggered", False),
            violation_type=item.get("violation_type"),
            tokens_used=item.get("tokens_used", 0),
        )
        for item in items
    ]

    # Get student name
    try:
        profile = await get_student(student_id)
        student_name = f"{profile.first_name} {profile.last_name}"
    except Exception:
        student_name = student_id

    return StudentInteractionHistory(
        student_id=student_id,
        student_name=student_name,
        interactions=interactions,
        total_count=len(interactions),  # Would use Count from a separate query
        page=page,
        page_size=page_size,
    )


# ─── Cost & Usage Metrics ────────────────────────────────────────────

@router.get("/costs", response_model=CostBreakdown)
async def cost_breakdown(
    request: Request,
    days: int = Query(30, ge=1, le=90),
    _: None = Depends(require_instructor),
):
    """Get AWS cost breakdown for the Teaching Agent platform.

    Includes per-service costs: Bedrock (inference + KB + guardrails),
    DynamoDB, Lambda, API Gateway, S3, Cognito.
    Also shows cost-per-student and cost-per-interaction.
    """
    return await get_cost_breakdown(period_days=days)


@router.get("/metrics/tokens")
async def token_usage(
    request: Request,
    days: int = Query(30, ge=1, le=90),
    group_by: str = Query("day", regex="^(day|week|student)$"),
    _: None = Depends(require_instructor),
):
    """Get token usage metrics, grouped by day, week, or student.

    Useful for monitoring consumption and projecting costs.
    """
    dashboard_data = await get_overall_dashboard(days=days)

    if group_by == "day":
        return {
            "group_by": "day",
            "data": [
                {
                    "date": m.date,
                    "tokens_input": m.total_tokens_input,
                    "tokens_output": m.total_tokens_output,
                    "total_tokens": m.total_tokens,
                    "estimated_cost_usd": m.estimated_bedrock_cost_usd,
                }
                for m in dashboard_data.daily_metrics
            ],
        }
    elif group_by == "week":
        # Aggregate by week
        # Simplified — would group daily_metrics into weeks
        return {"group_by": "week", "data": []}
    else:  # student
        # Per-student breakdown — would require scanning all students
        return {"group_by": "student", "data": []}
