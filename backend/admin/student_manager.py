"""Student Management — Cognito operations for creating/managing student accounts."""

import os
from datetime import datetime, timezone
from typing import Optional

import boto3
import structlog

from backend.admin.models import StudentCreate, StudentProfile, StudentUpdate

logger = structlog.get_logger()

COGNITO_USER_POOL_ID = os.environ.get("COGNITO_USER_POOL_ID", "")
REGION = os.environ.get("COGNITO_REGION", "eu-west-2")

cognito_client = boto3.client("cognito-idp", region_name=REGION)


async def create_student(student: StudentCreate) -> StudentProfile:
    """Create a new student in Cognito and return their profile.

    Creates the user with a temporary password (forces change on first login)
    or lets Cognito send an invite email with a generated password.
    """
    logger.info("creating_student", email=student.email, cohort=student.cohort)

    user_attributes = [
        {"Name": "email", "Value": student.email},
        {"Name": "email_verified", "Value": "true"},
        {"Name": "given_name", "Value": student.first_name},
        {"Name": "family_name", "Value": student.last_name},
        {"Name": "custom:cohort", "Value": student.cohort},
        {"Name": "custom:enrollment_date", "Value": datetime.now(timezone.utc).strftime("%Y-%m-%d")},
    ]

    create_params = {
        "UserPoolId": COGNITO_USER_POOL_ID,
        "Username": student.email,
        "UserAttributes": user_attributes,
        "DesiredDeliveryMediums": ["EMAIL"],
    }

    if student.temporary_password:
        create_params["TemporaryPassword"] = student.temporary_password
        create_params["MessageAction"] = "SUPPRESS"  # Don't send invite if manual password
    else:
        # Cognito sends an invitation email with temp password
        pass

    response = cognito_client.admin_create_user(**create_params)
    user = response["User"]

    logger.info("student_created", username=user["Username"], sub=_get_attr(user, "sub"))

    return StudentProfile(
        student_id=_get_attr(user, "sub") or user["Username"],
        email=student.email,
        first_name=student.first_name,
        last_name=student.last_name,
        cohort=student.cohort,
        enrollment_date=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        enabled=user.get("Enabled", True),
    )


async def bulk_create_students(students: list[StudentCreate]) -> list[dict]:
    """Create multiple students and return results (success/failure per entry)."""
    results = []
    for student in students:
        try:
            profile = await create_student(student)
            results.append({"email": student.email, "status": "created", "student_id": profile.student_id})
        except cognito_client.exceptions.UsernameExistsException:
            results.append({"email": student.email, "status": "already_exists", "error": "Account already exists"})
        except Exception as e:
            logger.error("bulk_create_failed", email=student.email, error=str(e))
            results.append({"email": student.email, "status": "failed", "error": str(e)})
    return results


async def update_student(student_id: str, update: StudentUpdate) -> StudentProfile:
    """Update a student's attributes in Cognito."""
    attrs_to_update = []

    if update.first_name:
        attrs_to_update.append({"Name": "given_name", "Value": update.first_name})
    if update.last_name:
        attrs_to_update.append({"Name": "family_name", "Value": update.last_name})
    if update.cohort:
        attrs_to_update.append({"Name": "custom:cohort", "Value": update.cohort})

    if attrs_to_update:
        cognito_client.admin_update_user_attributes(
            UserPoolId=COGNITO_USER_POOL_ID,
            Username=student_id,
            UserAttributes=attrs_to_update,
        )

    if update.enabled is not None:
        if update.enabled:
            cognito_client.admin_enable_user(UserPoolId=COGNITO_USER_POOL_ID, Username=student_id)
        else:
            cognito_client.admin_disable_user(UserPoolId=COGNITO_USER_POOL_ID, Username=student_id)

    return await get_student(student_id)


async def get_student(student_id: str) -> StudentProfile:
    """Get a student's full profile from Cognito."""
    response = cognito_client.admin_get_user(
        UserPoolId=COGNITO_USER_POOL_ID,
        Username=student_id,
    )

    attrs = {a["Name"]: a["Value"] for a in response.get("UserAttributes", [])}

    return StudentProfile(
        student_id=attrs.get("sub", student_id),
        email=attrs.get("email", ""),
        first_name=attrs.get("given_name", ""),
        last_name=attrs.get("family_name", ""),
        cohort=attrs.get("custom:cohort", ""),
        enrollment_date=attrs.get("custom:enrollment_date", ""),
        enabled=response.get("Enabled", True),
        last_login=response.get("UserLastModifiedDate", ""),
    )


async def list_students(cohort: Optional[str] = None, limit: int = 50) -> list[StudentProfile]:
    """List all students, optionally filtered by cohort."""
    params = {
        "UserPoolId": COGNITO_USER_POOL_ID,
        "Limit": limit,
    }

    if cohort:
        params["Filter"] = f'custom:cohort = "{cohort}"'

    response = cognito_client.list_users(**params)
    students = []

    for user in response.get("Users", []):
        attrs = {a["Name"]: a["Value"] for a in user.get("Attributes", [])}
        students.append(StudentProfile(
            student_id=attrs.get("sub", user["Username"]),
            email=attrs.get("email", ""),
            first_name=attrs.get("given_name", ""),
            last_name=attrs.get("family_name", ""),
            cohort=attrs.get("custom:cohort", ""),
            enrollment_date=attrs.get("custom:enrollment_date", ""),
            enabled=user.get("Enabled", True),
        ))

    return students


async def disable_student(student_id: str) -> dict:
    """Disable a student account (revoke access without deleting)."""
    cognito_client.admin_disable_user(UserPoolId=COGNITO_USER_POOL_ID, Username=student_id)
    logger.info("student_disabled", student_id=student_id)
    return {"student_id": student_id, "status": "disabled"}


async def reset_student_password(student_id: str) -> dict:
    """Trigger a password reset email for a student."""
    cognito_client.admin_reset_user_password(
        UserPoolId=COGNITO_USER_POOL_ID,
        Username=student_id,
    )
    logger.info("password_reset_triggered", student_id=student_id)
    return {"student_id": student_id, "status": "password_reset_sent"}


def _get_attr(user: dict, attr_name: str) -> Optional[str]:
    """Extract an attribute value from a Cognito user response."""
    for attr in user.get("Attributes", []):
        if attr["Name"] == attr_name:
            return attr["Value"]
    return None
