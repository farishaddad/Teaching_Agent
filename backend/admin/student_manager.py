"""Student Management — Cognito operations for creating/managing student accounts."""

import os
import secrets
import string
from datetime import datetime, timezone
from typing import Optional

import boto3
import structlog

from backend.admin.models import StudentCreate, StudentProfile, StudentUpdate

logger = structlog.get_logger()

COGNITO_USER_POOL_ID = os.environ.get("COGNITO_USER_POOL_ID", "")
REGION = os.environ.get("COGNITO_REGION", "eu-west-2")

# Cognito group all students belong to (used for authorization in the app).
STUDENTS_GROUP = "students"

cognito_client = boto3.client("cognito-idp", region_name=REGION)


def _generate_temp_password() -> str:
    """Generate a temporary password that satisfies the Cognito pool policy.

    The pool requires >= 10 chars with upper, lower, number, and symbol. We
    build 12 random alphanumerics for entropy and append one guaranteed
    character from each required class.
    """
    alphabet = string.ascii_letters + string.digits
    base = "".join(secrets.choice(alphabet) for _ in range(12))
    # Guarantee one of each required character class.
    return base + "A" + "a" + "1" + "!"


async def create_student(student: StudentCreate) -> StudentProfile:
    """Create a new student in Cognito and return their profile.

    Two invitation modes:
    - ``send_email=True`` (default): Cognito emails the student an invitation
      with a temporary password. Requires SES to be able to reach the address.
    - ``send_email=False``: no email is sent (``MessageAction=SUPPRESS``); a
      temporary password is generated (or the provided one used) and returned
      in the profile so the instructor can share it out of band. Use this while
      SES is in sandbox mode.

    Either way the account is created with ``FORCE_CHANGE_PASSWORD`` status, so
    the student must set their own password on first login, and is added to the
    ``students`` group.
    """
    logger.info(
        "creating_student",
        email=student.email,
        cohort=student.cohort,
        send_email=student.send_email,
    )

    enrollment_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    user_attributes = [
        {"Name": "email", "Value": student.email},
        {"Name": "email_verified", "Value": "true"},
        {"Name": "given_name", "Value": student.first_name},
        {"Name": "family_name", "Value": student.last_name},
        {"Name": "custom:cohort", "Value": student.cohort},
        {"Name": "custom:enrollment_date", "Value": enrollment_date},
    ]

    create_params = {
        "UserPoolId": COGNITO_USER_POOL_ID,
        "Username": student.email,
        "UserAttributes": user_attributes,
    }

    # Track the temp password to return only when we're NOT emailing it.
    returned_temp_password: Optional[str] = None

    if student.send_email:
        # Cognito generates (or uses the given) password and emails the invite.
        create_params["DesiredDeliveryMediums"] = ["EMAIL"]
        if student.temporary_password:
            create_params["TemporaryPassword"] = student.temporary_password
    else:
        # No email: suppress the invite and hand the password back to the caller.
        temp_password = student.temporary_password or _generate_temp_password()
        create_params["TemporaryPassword"] = temp_password
        create_params["MessageAction"] = "SUPPRESS"
        returned_temp_password = temp_password

    response = cognito_client.admin_create_user(**create_params)
    user = response["User"]

    # Add the student to the 'students' group so app authorization treats them
    # correctly (previously omitted).
    try:
        cognito_client.admin_add_user_to_group(
            UserPoolId=COGNITO_USER_POOL_ID,
            Username=student.email,
            GroupName=STUDENTS_GROUP,
        )
    except Exception as exc:  # noqa: BLE001 — don't fail creation if group add fails
        logger.error("student_group_add_failed", email=student.email, error=str(exc))

    logger.info("student_created", username=user["Username"], sub=_get_attr(user, "sub"))

    return StudentProfile(
        student_id=_get_attr(user, "sub") or user["Username"],
        email=student.email,
        first_name=student.first_name,
        last_name=student.last_name,
        cohort=student.cohort,
        enrollment_date=enrollment_date,
        enabled=user.get("Enabled", True),
        temporary_password=returned_temp_password,
        email_sent=student.send_email,
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


async def enable_student(student_id: str) -> dict:
    """Re-enable a previously disabled student account."""
    cognito_client.admin_enable_user(UserPoolId=COGNITO_USER_POOL_ID, Username=student_id)
    logger.info("student_enabled", student_id=student_id)
    return {"student_id": student_id, "status": "enabled"}


async def delete_student(student_id: str) -> dict:
    """Permanently delete a student's Cognito account.

    This is irreversible — the account and its sign-in credentials are removed.
    Interaction/progress records already written to DynamoDB are left intact
    for historical reporting (they are keyed by the Cognito ``sub``).
    """
    cognito_client.admin_delete_user(UserPoolId=COGNITO_USER_POOL_ID, Username=student_id)
    logger.info("student_deleted", student_id=student_id)
    return {"student_id": student_id, "status": "deleted"}


async def reset_student_password(student_id: str) -> dict:
    """Trigger a password reset for a student.

    Behaviour depends on the account status:
    - CONFIRMED (has set a password): ``admin_reset_user_password`` sends a
      reset code so the student can choose a new password.
    - FORCE_CHANGE_PASSWORD (never logged in — still on the temp password):
      ``admin_reset_user_password`` is not valid, so we re-send the original
      invitation instead (a fresh temp password + invite email).
    """
    # Look up the current status so we pick the right operation.
    try:
        user = cognito_client.admin_get_user(
            UserPoolId=COGNITO_USER_POOL_ID, Username=student_id
        )
    except cognito_client.exceptions.UserNotFoundException:
        logger.warning("password_reset_user_not_found", student_id=student_id)
        raise

    status = user.get("UserStatus")
    email = next(
        (a["Value"] for a in user.get("UserAttributes", []) if a["Name"] == "email"),
        None,
    )

    if status == "FORCE_CHANGE_PASSWORD":
        # Student hasn't logged in yet — resend the invite rather than reset.
        # RESEND goes through admin_create_user, which requires the email
        # (the sign-in alias), NOT the Cognito sub.
        if not email:
            raise cognito_client.exceptions.UserNotFoundException(
                {"Error": {"Code": "UserNotFoundException",
                           "Message": "No email on file for this student."}},
                "AdminCreateUser",
            )
        cognito_client.admin_create_user(
            UserPoolId=COGNITO_USER_POOL_ID,
            Username=email,
            MessageAction="RESEND",
            DesiredDeliveryMediums=["EMAIL"],
        )
        logger.info("password_invite_resent", student_id=student_id, status=status)
        return {"student_id": student_id, "status": "invite_resent"}

    cognito_client.admin_reset_user_password(
        UserPoolId=COGNITO_USER_POOL_ID,
        Username=student_id,
    )
    logger.info("password_reset_triggered", student_id=student_id, status=status)
    return {"student_id": student_id, "status": "password_reset_sent", "email": email}


def _get_attr(user: dict, attr_name: str) -> Optional[str]:
    """Extract an attribute value from a Cognito user response."""
    for attr in user.get("Attributes", []):
        if attr["Name"] == attr_name:
            return attr["Value"]
    return None
