# Spec: Authentication Module

## Goal
Implement secure student authentication using Amazon Cognito with JWT-based session management.

## Inputs
- Student email + password (via Cognito Hosted UI)
- Cognito User Pool configuration (CDK)

## Outputs
- JWT access token + refresh token (httpOnly cookie)
- Authenticated user context available in all API routes
- Student profile (id, email, cohort, enrollment_date)

## Files to Create
- `backend/auth/__init__.py`
- `backend/auth/cognito.py` — JWT verification, token refresh logic
- `backend/auth/middleware.py` — FastAPI dependency for route protection
- `backend/auth/models.py` — Pydantic models for user context
- `infrastructure/auth_stack.py` — CDK: Cognito User Pool, App Client, Domain
- `frontend/src/components/Login.tsx` — Login page (redirects to Cognito)
- `frontend/src/hooks/useAuth.ts` — Auth state management hook
- `tests/test_auth.py` — Unit tests for JWT verification

## Acceptance Criteria
- [ ] Students can sign up with email + password via Cognito Hosted UI
- [ ] Login returns JWT stored in httpOnly secure cookie
- [ ] All `/api/*` routes return 401 without valid JWT
- [ ] Token refresh happens transparently before expiry
- [ ] Student `sub` (Cognito user ID) is extracted and available as `current_user.id`
- [ ] Custom attributes (cohort, enrollment_date) are readable from token
- [ ] Logout clears cookies and invalidates refresh token

## Do Not Do
- Do NOT implement custom password hashing — Cognito handles this
- Do NOT store JWTs in localStorage (XSS risk)
- Do NOT allow unauthenticated access to any chat or tracking endpoint
