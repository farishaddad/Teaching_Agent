"""Amazon Cognito JWT verification and token management.

Responsibilities:
- Fetch and cache the Cognito JWKS for signature verification.
- Verify JWTs (RS256, audience, issuer, expiry).
- Extract the StudentUser context from verified claims.
- Provide a FastAPI dependency ``get_current_user`` for route injection.
- Expose a ``refresh_access_token`` helper for silent token renewal.
"""

import os
from typing import Optional

import httpx
import structlog
from fastapi import Depends, HTTPException, Request, status
from jwt import PyJWKClient, PyJWKClientError
import jwt as pyjwt

from backend.auth.models import StudentUser

logger = structlog.get_logger()

# ── Configuration (injected via environment) ──────────────────────────────────
COGNITO_REGION: str = os.environ.get("COGNITO_REGION", "eu-west-2")
COGNITO_USER_POOL_ID: str = os.environ.get("COGNITO_USER_POOL_ID", "")
COGNITO_APP_CLIENT_ID: str = os.environ.get("COGNITO_APP_CLIENT_ID", "")

_ISSUER = (
    f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}"
)
_JWKS_URL = f"{_ISSUER}/.well-known/jwks.json"

# Cognito token endpoint for refresh calls
_TOKEN_ENDPOINT = (
    f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}"
    f"/oauth2/token"
)

# ── JWKS client (module-level singleton, caches signing keys) ─────────────────
_jwks_client: Optional[PyJWKClient] = None


def _get_jwks_client() -> PyJWKClient:
    """Return a cached PyJWKClient pointed at the Cognito JWKS endpoint.

    The client is created once per process and caches signing keys
    internally, avoiding redundant HTTP requests.
    """
    global _jwks_client
    if _jwks_client is None:
        _jwks_client = PyJWKClient(
            _JWKS_URL,
            cache_keys=True,
            cache_jwk_set=True,
            lifespan=300,  # Refresh JWKS every 5 minutes
        )
    return _jwks_client


# ── Core verification ─────────────────────────────────────────────────────────


def verify_token(token: str) -> StudentUser:
    """Verify a Cognito JWT and return the authenticated student context.

    Validates signature, algorithm, audience, issuer, and expiry.
    Extracts standard and custom Cognito claims into a ``StudentUser``.

    Args:
        token: A Cognito access token or ID token (RS256, JWT format).

    Returns:
        ``StudentUser`` populated from verified JWT claims.

    Raises:
        ``jwt.InvalidTokenError`` subclasses on any validation failure.
    """
    jwks_client = _get_jwks_client()

    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)
    except PyJWKClientError as exc:
        logger.warning("jwks_key_lookup_failed", error=str(exc))
        raise pyjwt.InvalidTokenError("Unable to locate signing key") from exc

    payload: dict = pyjwt.decode(
        token,
        signing_key.key,
        algorithms=["RS256"],
        audience=COGNITO_APP_CLIENT_ID,
        issuer=_ISSUER,
        options={
            "verify_exp": True,
            "verify_aud": True,
            "verify_iss": True,
        },
    )

    # Cognito groups are in the cognito:groups claim
    groups: list[str] = payload.get("cognito:groups", [])

    return StudentUser(
        id=payload["sub"],
        email=payload.get("email", ""),
        given_name=payload.get("given_name"),
        family_name=payload.get("family_name"),
        cohort=payload.get("custom:cohort"),
        enrollment_date=payload.get("custom:enrollment_date"),
        groups=groups,
    )


# ── Token refresh ─────────────────────────────────────────────────────────────


async def refresh_access_token(refresh_token: str) -> dict:
    """Exchange a Cognito refresh token for a new access + id token pair.

    Calls the Cognito token endpoint using the ``REFRESH_TOKEN`` grant type.
    The app client must be configured without a client secret (public PKCE client).

    Args:
        refresh_token: The Cognito refresh token from the ``refresh_token`` cookie.

    Returns:
        Dict with ``access_token``, ``id_token``, and ``expires_in`` keys.

    Raises:
        ``httpx.HTTPStatusError``: If Cognito rejects the refresh token.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            _TOKEN_ENDPOINT,
            data={
                "grant_type": "refresh_token",
                "client_id": COGNITO_APP_CLIENT_ID,
                "refresh_token": refresh_token,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=10.0,
        )
        response.raise_for_status()
        return response.json()


# ── FastAPI dependency ────────────────────────────────────────────────────────


def get_current_user(request: Request) -> StudentUser:
    """FastAPI dependency that returns the authenticated StudentUser.

    The JWTAuthMiddleware runs first and attaches the verified user to
    ``request.state.current_user``.  This dependency simply retrieves it
    so route handlers can declare it cleanly:

        async def my_route(current_user: StudentUser = Depends(get_current_user)):
            ...

    Raises:
        ``HTTPException(401)``: If no user context is attached (middleware bypassed).
    """
    user: Optional[StudentUser] = getattr(request.state, "current_user", None)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please log in.",
        )
    return user


def require_instructor(
    current_user: StudentUser = Depends(get_current_user),
) -> StudentUser:
    """FastAPI dependency that requires the user to be in the instructors group.

    Use this on admin-only routes:

        async def admin_route(user: StudentUser = Depends(require_instructor)):
            ...

    Raises:
        ``HTTPException(403)``: If the authenticated user is not an instructor.
    """
    if not current_user.is_instructor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Instructor access required.",
        )
    return current_user
