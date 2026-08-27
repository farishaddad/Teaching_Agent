"""Student-facing progress API routes.

Students can only view their OWN progress data.
Admin routes (Module 6) handle cross-student views.
"""

import structlog
from fastapi import APIRouter, Request, Query

from backend.tracking.repository import get_student_interactions, get_student_progress

logger = structlog.get_logger()
router = APIRouter()


@router.get("/")
async def my_progress(request: Request):
    """Get the current student's progress summary.

    Returns: topics covered, strengths, weaknesses, active days, total questions.
    Students can ONLY see their own data.
    """
    student = request.state.current_user
    progress = await get_student_progress(student.id)
    return progress


@router.get("/history")
async def my_history(
    request: Request,
    limit: int = Query(20, ge=1, le=50, description="Max items to return"),
):
    """Get the current student's interaction history (paginated).

    Returns recent questions and responses (most recent first).
    Students can ONLY see their own history.
    """
    student = request.state.current_user
    interactions = await get_student_interactions(
        student_id=student.id,
        limit=limit,
        newest_first=True,
    )

    # Sanitize for student view (remove internal fields)
    sanitized = [
        {
            "timestamp": item.get("SK", "").split("#")[1][:19] if "#" in item.get("SK", "") else "",
            "query": item.get("query", ""),
            "response_summary": item.get("response_summary", ""),
            "topic": item.get("topic_detected", ""),
            "sources": item.get("sources_used", []),
        }
        for item in interactions
    ]

    return {
        "student_id": student.id,
        "interactions": sanitized,
        "count": len(sanitized),
    }
