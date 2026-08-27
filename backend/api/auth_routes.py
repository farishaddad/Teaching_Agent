"""FastAPI routes for authentication lifecycle.

Endpoints:
  POST /api/auth/callback  — Exchange Cognito auth code for tokens (sets cookies)
  GET  /api/auth/me        — Return current user profile (requires valid cookie)
  POST /api/auth/logout    — Revoke refresh token and clear cookies
  POST /api/auth/refresh   — Explicitly refresh access token
"""

import os
from typing import Optional

import httpx
import structlog
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from pydantic import BaseModel

from backend.auth.cognito import (
    get_current_user,
    refresh_access_token,
    verify_token,
)
from backend.auth.models import StudentUser

logger = structlog.get_logger()

router = APIRouter()

# ── Configuration ─────────────────────────────────────────────────────────────
COGNITO_REGION: str = os.environ.get("COGNITO_REGION", "eu-west-2")
COGNITO_USER_POOL_ID: str = os.environ.get("COGNITO_USER_POOL_ID", "")
COGNITO_APP_CLIENT_ID: str = os.environ.get("COGNITO_APP_CLIENT_ID", "")
COGNITO_DOMAIN: str = os.environ.get("COGNITO_DOMAIN", "")  # e.g. https://teaching-agent-auth.auth.eu-west-2.amazoncognito.com

_TOKEN_ENDPOINT = f"{COGNITO_DOMAIN}/oauth2/token"

# Cookie settings — must stay in sync with middleware.py
_COOKIE_SECURE = os.environ.get("COOKIE_SECURE", "true").lower() != "false"
_COOKIE_SAMESITE = "lax"
_COOKIE_MAX_AGE_ACCESS = 3600       # 1 hour
_COOKIE_MAX_AGE_REFRESH = 2592000   # 30 days


# ── Pydantic models ────────────────────────────────────────────────────────────

class CallbackRequest(BaseModel):
    """Body for the /callback endpoint."""
    code: str
    code_verifier: str
    redirect_uri: str


class UserProfile(BaseModel):
    """Public user profile returned by /me."""
    id: str
    email: str
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    cohort: Optional[str] = None
    enrollment_date: Optional[str] = None
    groups: list[str]
    display_name: str


# ── Helpers ───────────────────────────────────────────────────────────────────

def _set_auth_cookies(response: Response, tokens: dict) -> None:
    """Write JWTs as httpOnly secure cookies on the response."""
    response.set_cookie(
        key="access_token",
        value=tokens["access_token"],
        httponly=True,
        secure=_COOKIE_SECURE,
        samesite=_COOKIE_SAMESITE,
        max_age=_COOKIE_MAX_AGE_ACCESS,
        path="/",
    )
    if "id_token" in tokens:
        response.set_cookie(
            key="id_token",
            value=tokens["id_token"],
            httponly=True,
            secure=_COOKIE_SECURE,
            samesite=_COOKIE_SAMESITE,
            max_age=_COOKIE_MAX_AGE_ACCESS,
            path="/",
        )
    if "refresh_token" in tokens:
        response.set_cookie(
            key="refresh_token",
            value=tokens["refresh_token"],
            httponly=True,
            secure=_COOKIE_SECURE,
            samesite=_COOKIE_SAMESITE,
            max_age=_COOKIE_MAX_AGE_REFRESH,
            path="/api/auth",  # Restrict refresh token to auth paths only
        )


def _clear_auth_cookies(response: Response) -> None:
    """Delete all auth cookies."""
    for cookie in ("access_token", "id_token", "refresh_token"):
        response.delete_cookie(cookie, path="/")
    response.delete_cookie("refresh_token", path="/api/auth")


# ── Routes ────────────────────────────────────────────────────────────────────

@router.post("/callback", response_model=UserProfile)
async def auth_callback(body: CallbackRequest, response: Response) -> UserProfile:
    """Exchange a Cognito authorization code for JWT tokens.

    The backend performs the code exchange (keeping client credentials
    server-side) and sets httpOnly cookies.  Returns the user profile
    so the frontend can update its auth state immediately.

    Args:
        body: Contains the authorization code, PKCE verifier, and redirect URI.

    Returns:
        The authenticated user's profile.

    Raises:
        HTTPException(400): If Cognito rejects the code exchange.
    """
    if not COGNITO_DOMAIN:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Auth service not configured. Contact support.",
        )

    try:
        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                _TOKEN_ENDPOINT,
                data={
                    "grant_type": "authorization_code",
                    "client_id": COGNITO_APP_CLIENT_ID,
                    "code": body.code,
                    "redirect_uri": body.redirect_uri,
                    "code_verifier": body.code_verifier,
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=15.0,
            )
            token_response.raise_for_status()
            tokens = token_response.json()
    except httpx.HTTPStatusError as exc:
        logger.warning("auth_code_exchange_failed", status=exc.response.status_code)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired authorization code.",
        ) from exc
    except httpx.RequestError as exc:
        logger.error("cognito_unreachable", error=str(exc))
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication service unavailable.",
        ) from exc

    # Verify the returned access token
    try:
        student = verify_token(tokens["access_token"])
    except Exception as exc:
        logger.error("post_exchange_token_invalid", error=str(exc))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token verification failed after code exchange.",
        ) from exc

    # Set cookies
    _set_auth_cookies(response, tokens)

    logger.info("student_logged_in", student_id=student.id)

    return UserProfile(
        id=student.id,
        email=student.email,
        given_name=student.given_name,
        family_name=student.family_name,
        cohort=student.cohort,
        enrollment_date=student.enrollment_date,
        groups=student.groups,
        display_name=student.display_name,
    )


@router.get("/me", response_model=UserProfile)
async def get_me(current_user: StudentUser = Depends(get_current_user)) -> UserProfile:
    """Return the currently authenticated user's profile.

    Requires a valid ``access_token`` cookie set by /callback or /refresh.
    Used by the frontend to rehydrate auth state on page load.
    """
    return UserProfile(
        id=current_user.id,
        email=current_user.email,
        given_name=current_user.given_name,
        family_name=current_user.family_name,
        cohort=current_user.cohort,
        enrollment_date=current_user.enrollment_date,
        groups=current_user.groups,
        display_name=current_user.display_name,
    )


@router.post("/logout")
async def logout(
    request: Request,
    response: Response,
    current_user: StudentUser = Depends(get_current_user),
) -> dict:
    """Clear auth cookies and revoke the Cognito refresh token.

    The frontend should additionally redirect to the Cognito logout URL
    to clear the Hosted UI session (done in useAuth.logout).
    """
    refresh_token = request.cookies.get("refresh_token")

    # Revoke the refresh token at Cognito (best-effort)
    if refresh_token and COGNITO_DOMAIN:
        try:
            async with httpx.AsyncClient() as client:
                await client.post(
                    f"{COGNITO_DOMAIN}/oauth2/revoke",
                    data={
                        "token": refresh_token,
                        "client_id": COGNITO_APP_CLIENT_ID,
                    },
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                    timeout=10.0,
                )
        except Exception as exc:
            # Log but don't fail — cookies will still be cleared
            logger.warning("refresh_token_revoke_failed", error=str(exc))

    _clear_auth_cookies(response)
    logger.info("student_logged_out", student_id=current_user.id)

    return {"detail": "Logged out successfully."}


@router.post("/refresh", response_model=UserProfile)
async def refresh_tokens(request: Request, response: Response) -> UserProfile:
    """Explicitly refresh the access token using the refresh_token cookie.

    Called by the frontend if it detects a 401 response (as a fallback
    to the middleware's transparent refresh).

    Returns:
        Updated user profile with refreshed cookie set on the response.

    Raises:
        HTTPException(401): If the refresh token is missing or invalid.
    """
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No refresh token. Please log in again.",
        )

    try:
        tokens = await refresh_access_token(refresh_token)
        student = verify_token(tokens["access_token"])
    except Exception as exc:
        logger.warning("explicit_token_refresh_failed", error=str(exc))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired. Please log in again.",
        ) from exc

    _set_auth_cookies(response, tokens)

    return UserProfile(
        id=student.id,
        email=student.email,
        given_name=student.given_name,
        family_name=student.family_name,
        cohort=student.cohort,
        enrollment_date=student.enrollment_date,
        groups=student.groups,
        display_name=student.display_name,
    )
