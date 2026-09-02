"""JWT Authentication Middleware for FastAPI.

Intercepts every request (except public paths), extracts the JWT from
the ``access_token`` httpOnly cookie or ``Authorization: Bearer`` header,
verifies it via Cognito JWKS, and attaches the ``StudentUser`` to
``request.state.current_user``.

If the access token is expired but a valid ``refresh_token`` cookie is
present, the middleware transparently refreshes the token and sets updated
cookies on the response.
"""

import structlog
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import jwt as pyjwt

from backend.auth.cognito import refresh_access_token, verify_token
from backend.auth.models import StudentUser

logger = structlog.get_logger()

# Paths that bypass authentication entirely.
# NOTE: /api/auth/callback is public (no session exists yet — it CREATES one).
# But /api/auth/me, /api/auth/logout and /api/auth/refresh must NOT be public:
# they rely on the middleware verifying the token and setting
# request.state.current_user. (Previously the broad "/api/auth/" prefix made
# /api/auth/me bypass auth, so it never had a user and always returned 401 —
# which broke session rehydration and bounced logged-in users back to login.)
# /api/auth/refresh is exempt because it authenticates via the refresh_token
# cookie itself, not the access token.
PUBLIC_PATHS = frozenset(
    {
        "/health",
        "/docs",
        "/openapi.json",
        "/redoc",
        "/api/auth/callback",
        "/api/auth/refresh",
    }
)

# Path prefixes that bypass auth (tutorial content is public course material).
PUBLIC_PREFIXES = ("/api/tutorial",)

# Cookie settings — must match those set at login
_COOKIE_SECURE = True   # HTTPS only; set False for local dev via env if needed
_COOKIE_SAMESITE = "lax"
_COOKIE_MAX_AGE_ACCESS = 3600        # 1 hour (matches Cognito access token TTL)
_COOKIE_MAX_AGE_REFRESH = 2592000    # 30 days (matches Cognito refresh token TTL)


class JWTAuthMiddleware(BaseHTTPMiddleware):
    """Verify JWT on every non-public request and inject student context.

    Flow:
    1. Skip public paths.
    2. Extract access token from ``access_token`` cookie or ``Authorization`` header.
    3. Verify token via Cognito JWKS.
    4. If expired and a ``refresh_token`` cookie exists → refresh silently.
    5. Attach ``StudentUser`` to ``request.state.current_user``.
    6. Return 401 for missing/invalid tokens with no refresh fallback.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        # ── Public paths bypass ───────────────────────────────────────────────
        if request.url.path in PUBLIC_PATHS:
            return await call_next(request)
        if request.url.path.startswith(PUBLIC_PREFIXES):
            return await call_next(request)

        # ── Extract token ─────────────────────────────────────────────────────
        access_token = self._extract_token(request)

        if not access_token:
            return self._unauthorized("Authentication required. Please log in.")

        # ── Verify token ──────────────────────────────────────────────────────
        new_tokens: dict | None = None

        try:
            student = verify_token(access_token)
        except pyjwt.ExpiredSignatureError:
            # Access token expired — try silent refresh
            student, new_tokens = await self._try_refresh(request)
            if student is None:
                return self._unauthorized(
                    "Session expired. Please log in again.", clear_cookies=True
                )
        except pyjwt.InvalidTokenError as exc:
            logger.warning(
                "auth_token_invalid",
                error=str(exc),
                path=request.url.path,
            )
            return self._unauthorized("Invalid token. Please log in again.")

        # ── Attach user context ───────────────────────────────────────────────
        request.state.current_user = student
        logger.info(
            "authenticated_request",
            student_id=student.id,
            path=request.url.path,
            method=request.method,
        )

        response = await call_next(request)

        # ── Set refreshed cookies on response if tokens were renewed ──────────
        if new_tokens:
            self._set_auth_cookies(response, new_tokens)

        return response

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _extract_token(self, request: Request) -> str | None:
        """Extract JWT from httpOnly cookie (preferred) or Authorization header."""
        token = request.cookies.get("access_token")
        if token:
            return token

        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            return auth_header[7:]

        return None

    async def _try_refresh(
        self, request: Request
    ) -> tuple[StudentUser | None, dict | None]:
        """Attempt a silent token refresh using the refresh_token cookie.

        Returns:
            Tuple of (StudentUser, new_tokens_dict) on success, or (None, None).
        """
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            return None, None

        try:
            new_tokens = await refresh_access_token(refresh_token)
            student = verify_token(new_tokens["access_token"])
            logger.info("token_refreshed_silently", student_id=student.id)
            return student, new_tokens
        except Exception as exc:
            logger.warning("token_refresh_failed", error=str(exc))
            return None, None

    @staticmethod
    def _set_auth_cookies(response: Response, tokens: dict) -> None:
        """Write refreshed JWT cookies onto the response."""
        response.set_cookie(
            key="access_token",
            value=tokens["access_token"],
            httponly=True,
            secure=_COOKIE_SECURE,
            samesite=_COOKIE_SAMESITE,
            max_age=_COOKIE_MAX_AGE_ACCESS,
            path="/",
        )
        # id_token may also be present
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

    @staticmethod
    def _unauthorized(detail: str, clear_cookies: bool = False) -> JSONResponse:
        """Return a 401 JSON response, optionally clearing auth cookies."""
        response = JSONResponse(
            status_code=401,
            content={"detail": detail},
        )
        if clear_cookies:
            response.delete_cookie("access_token")
            response.delete_cookie("id_token")
            response.delete_cookie("refresh_token")
        return response
