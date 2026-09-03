# Chapter 2: Setting Up Authentication

## What You'll Build

A secure student login system using Amazon Cognito that:
- Lets students sign in on the Cognito **hosted UI** (instructors create the accounts — no self-signup)
- Uses the **authorization-code + PKCE** flow; the backend performs the code exchange
- Issues JWTs stored in **httpOnly cookies** (not localStorage)
- Verifies the JWT **inside the Lambda** on every API call (there is no API Gateway authorizer)
- Separates students from instructors via Cognito **groups**

---

## Amazon Cognito Concepts

| Concept | What It Is |
|---------|-----------|
| **User Pool** | A user directory — stores usernames, passwords, attributes |
| **App Client** | Your application's identity to interact with the User Pool (public, no secret) |
| **Hosted UI** | Pre-built login page from Cognito (no custom form needed) |
| **JWT** | JSON Web Token — signed proof of identity, verified without calling Cognito |
| **PKCE** | Proof Key for Code Exchange — prevents authorization code interception |
| **Groups** | Role-based access control — `students`, `instructors` |

---

## Step 1: CDK — Create the Cognito User Pool

```python
# infrastructure/auth_stack.py (abridged — matches the deployed config)

self.user_pool = cognito.UserPool(
    self, "TeachingAgentUserPool",
    user_pool_name="teaching-agent-user-pool",
    self_sign_up_enabled=False,                 # instructors create accounts
    sign_in_aliases=cognito.SignInAliases(email=True, username=False),
    sign_in_case_sensitive=False,
    auto_verify=cognito.AutoVerifiedAttrs(email=True),
    standard_attributes=cognito.StandardAttributes(
        email=cognito.StandardAttribute(required=True, mutable=True),
        given_name=cognito.StandardAttribute(required=True, mutable=True),
        family_name=cognito.StandardAttribute(required=True, mutable=True),
    ),
    custom_attributes={
        "cohort": cognito.StringAttribute(min_len=1, max_len=50, mutable=True),
        "enrollment_date": cognito.StringAttribute(min_len=10, max_len=10, mutable=True),
    },
    password_policy=cognito.PasswordPolicy(
        min_length=10,
        require_lowercase=True,
        require_uppercase=True,
        require_digits=True,
        require_symbols=True,
        temp_password_validity=cdk.Duration.days(7),
    ),
    account_recovery=cognito.AccountRecovery.EMAIL_ONLY,
    mfa=cognito.Mfa.OPTIONAL,
    mfa_second_factor=cognito.MfaSecondFactor(sms=False, otp=True),
    email=cognito.UserPoolEmail.with_cognito(),
)
```

The app client is a **public PKCE client** (no secret) using the authorization-code flow only. Note that SRP and direct user-password auth are **disabled** — students always go through the hosted UI. `admin_user_password` is enabled only so accounts can be seeded/managed via the AWS SDK:

```python
self.app_client = self.user_pool.add_client(
    "TeachingAgentAppClient",
    user_pool_client_name="teaching-agent-web-client",
    generate_secret=False,                       # public PKCE client
    auth_flows=cognito.AuthFlow(
        user_password=False,
        user_srp=False,
        admin_user_password=True,                # for admin SDK seeding only
    ),
    o_auth=cognito.OAuthSettings(
        flows=cognito.OAuthFlows(
            authorization_code_grant=True,
            implicit_code_grant=False,
        ),
        scopes=[cognito.OAuthScope.OPENID, cognito.OAuthScope.EMAIL, cognito.OAuthScope.PROFILE],
        # Built from `frontend_origin` (passed in from app.py). The default
        # frontend origin is the CloudFront URL; localhost is for dev.
        callback_urls=[
            "http://localhost:5173/auth/callback",
            f"{frontend_origin}/auth/callback",
        ],
        logout_urls=[
            "http://localhost:5173/",
            f"{frontend_origin}/",
        ],
    ),
    access_token_validity=cdk.Duration.hours(1),
    id_token_validity=cdk.Duration.hours(1),
    refresh_token_validity=cdk.Duration.days(30),
    enable_token_revocation=True,                # logout revokes refresh tokens
    prevent_user_existence_errors=True,
)

# Hosted UI domain: https://teaching-agent-auth.auth.<region>.amazoncognito.com
self.domain = self.user_pool.add_domain(
    "TeachingAgentDomain",
    cognito_domain=cognito.CognitoDomainOptions(domain_prefix="teaching-agent-auth"),
)

# Groups for RBAC
cognito.CfnUserPoolGroup(self, "InstructorsGroup", group_name="instructors",
                         user_pool_id=self.user_pool.user_pool_id, precedence=1)
cognito.CfnUserPoolGroup(self, "StudentsGroup", group_name="students",
                         user_pool_id=self.user_pool.user_pool_id, precedence=10)
```

> **Callback URL gotcha:** the redirect URI is `/auth/callback` (not `/callback`), and it must **exactly** match the URI used both in the login redirect and in the token exchange. When you deploy the frontend to a new domain, pass it via `-c frontend_domain=<host>` so the callback/logout URLs are regenerated (see Chapter 6).

---

## Step 2: JWT Verification in the Lambda

When a request arrives, the backend verifies the JWT is:
1. Signed by our Cognito User Pool (not forged)
2. Not expired
3. Issued for our App Client

```python
# backend/auth/cognito.py (abridged)

payload = pyjwt.decode(
    token,
    signing_key.key,                 # from Cognito JWKS
    algorithms=["RS256"],
    issuer=_ISSUER,                  # https://cognito-idp.<region>.amazonaws.com/<pool>
    options={"verify_exp": True, "verify_aud": False, "verify_iss": True},
)
# Cognito ACCESS tokens don't carry `aud`; verify `client_id` instead.
token_client = payload.get("client_id") or payload.get("aud")
if COGNITO_APP_CLIENT_ID and token_client != COGNITO_APP_CLIENT_ID:
    raise pyjwt.InvalidTokenError("Token client_id does not match app client")

groups = payload.get("cognito:groups", [])   # ["students"] or ["instructors"]
```

**Why RS256 / JWKS?** Cognito signs tokens with RSA. We verify using the public key from the JWKS endpoint — no shared secret needed, and the key rotates automatically. The `PyJWKClient` caches keys in-process.

> **Access-token nuance:** Cognito access tokens set `client_id` (not `aud`), so we disable `verify_aud` and check `client_id` explicitly. ID tokens use `aud` — this app authenticates with the access token.

---

## Step 3: The In-Lambda Auth Middleware

There is **no API Gateway Cognito Authorizer**. A FastAPI middleware runs on every request instead. Two things make it correct:

1. **Public paths must be precise.** Only endpoints that genuinely have no session yet may bypass auth: `/api/auth/callback` (creates the session) and `/api/auth/refresh` (authenticates via the refresh-token cookie). Crucially, `/api/auth/me` and `/api/auth/logout` are **not** public — they need the verified user.
2. **Silent refresh.** If the access token is expired but a valid `refresh_token` cookie exists, the middleware refreshes transparently and re-sets the cookies.

```python
# backend/auth/middleware.py (abridged)

PUBLIC_PATHS = frozenset({
    "/health", "/docs", "/openapi.json", "/redoc",
    "/api/auth/callback",   # public: no session yet — it CREATES one
    "/api/auth/refresh",    # public: authenticates via the refresh_token cookie
})
PUBLIC_PREFIXES = ("/api/tutorial",)   # public course material

class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.url.path in PUBLIC_PATHS:
            return await call_next(request)
        if request.url.path.startswith(PUBLIC_PREFIXES):
            return await call_next(request)

        token = self._extract_token(request)          # cookie, then Bearer
        if not token:
            return self._unauthorized("Authentication required. Please log in.")

        try:
            student = verify_token(token)
        except pyjwt.ExpiredSignatureError:
            student, new_tokens = await self._try_refresh(request)   # refresh_token cookie
            if student is None:
                return self._unauthorized("Session expired.", clear_cookies=True)
        except pyjwt.InvalidTokenError:
            return self._unauthorized("Invalid token. Please log in again.")

        request.state.current_user = student
        response = await call_next(request)
        if new_tokens:
            self._set_auth_cookies(response, new_tokens)   # refreshed cookies
        return response
```

> ⚠️ **A real bug we hit:** the public list was once the broad prefix `"/api/auth/"`, which accidentally made `/api/auth/me` bypass the middleware. That route then never had `request.state.current_user`, so it always returned `401` — and since the SPA calls `/api/auth/me` to rehydrate the session, a *successfully logged-in* user got bounced straight back to the login page. The fix was to make only `/api/auth/callback` and `/api/auth/refresh` public. Precise public paths matter.

---

## Step 4: The Login Flow (PKCE, backend-mediated)

```
Student clicks "Login"
        │  SPA generates a PKCE verifier + challenge (crypto.subtle),
        │  stores the verifier in sessionStorage
        ▼
Redirect to Cognito Hosted UI
(https://teaching-agent-auth.auth.<region>.amazoncognito.com/oauth2/authorize?...)
        │
        ▼
Student signs in
        │
        ▼
Cognito redirects back with an authorization code
(https://<cloudfront>/auth/callback?code=xyz)
        │
        ▼
SPA POSTs {code, code_verifier, redirect_uri} to /api/auth/callback
        │
        ▼
Backend exchanges the code at Cognito's /oauth2/token endpoint,
verifies the returned access token, and sets httpOnly cookies:
  access_token (path /), id_token (path /), refresh_token (path /api/auth)
        │
        ▼
Authenticated! Every API call carries the cookies automatically (same origin).
```

The backend keeps the code-exchange server-side and the tokens in httpOnly cookies, so raw JWTs never touch JavaScript or the URL. The route also exposes `/api/auth/me` (rehydrate session), `/api/auth/logout` (clear cookies + revoke refresh token), and `/api/auth/refresh`.

---

## Security Best Practices

### ✅ Do This
- Store tokens in **httpOnly** cookies (inaccessible to JavaScript = no XSS theft)
- Use **PKCE** (prevents authorization-code interception) with a backend code exchange
- Keep access-token lifetime **short** (1 hour) and rely on silent refresh
- Use **Secure** + **SameSite=Lax** cookie attributes (the SPA and API are same-origin via CloudFront)
- Let Cognito handle password hashing and storage
- Disable self-signup (instructors create accounts)
- Keep public paths **precise** — never blanket-exempt a whole `/api/auth/` prefix

### ❌ Don't Do This
- Store tokens in localStorage (XSS = stolen tokens)
- Use implicit flow (tokens in URL = logged in browser history)
- Build custom password storage (you will get it wrong)
- Hard-code Cognito credentials in frontend code
- Skip token-expiry verification

---

## Testing Authentication

```python
# tests/test_auth.py

def test_missing_token_returns_401(client):
    response = client.get("/api/chat")
    assert response.status_code == 401

def test_invalid_token_returns_401(client):
    response = client.get("/api/chat", cookies={"access_token": "not.a.real.jwt"})
    assert response.status_code == 401

def test_me_requires_auth(client):
    # /api/auth/me is NOT public — it must reject unauthenticated callers.
    assert client.get("/api/auth/me").status_code == 401

def test_valid_token_passes(client, valid_jwt):
    response = client.post("/api/chat",
        json={"message": "What is RAG?"},
        cookies={"access_token": valid_jwt})
    assert response.status_code == 200
```

---

## Next Chapter

In [Chapter 3: RAG Pipeline](./03-rag-pipeline.md), we'll build the knowledge retrieval system that grounds the agent's answers in your course materials — and see how the Knowledge Base ID reaches the Lambda via SSM.
