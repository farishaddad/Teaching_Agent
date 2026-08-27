"""Pydantic models for authenticated user context."""

from typing import Optional

from pydantic import BaseModel, field_validator


class StudentUser(BaseModel):
    """Authenticated user context extracted from a verified Cognito JWT.

    This model is attached to ``request.state.current_user`` by the
    JWTAuthMiddleware and injected as a FastAPI dependency via
    ``get_current_user``.
    """

    id: str
    """Cognito ``sub`` claim — stable, unique identifier for the student."""

    email: str
    """User's email address from the ``email`` claim."""

    given_name: Optional[str] = None
    """First name from ``given_name`` claim."""

    family_name: Optional[str] = None
    """Last name from ``family_name`` claim."""

    cohort: Optional[str] = None
    """Course cohort from ``custom:cohort`` claim (e.g. "aug-2026")."""

    enrollment_date: Optional[str] = None
    """Enrollment date from ``custom:enrollment_date`` claim (ISO: YYYY-MM-DD)."""

    groups: list[str] = []
    """Cognito groups the user belongs to (e.g. ["students"] or ["instructors"])."""

    @field_validator("id")
    @classmethod
    def id_must_not_be_empty(cls, v: str) -> str:
        """Ensure the sub claim is never empty."""
        if not v.strip():
            raise ValueError("User ID (sub) must not be empty")
        return v

    @property
    def is_instructor(self) -> bool:
        """Return True if the user is in the instructors group."""
        return "instructors" in self.groups

    @property
    def display_name(self) -> str:
        """Return full name or fall back to email prefix."""
        if self.given_name and self.family_name:
            return f"{self.given_name} {self.family_name}"
        return self.email.split("@")[0]
