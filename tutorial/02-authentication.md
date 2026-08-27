# Chapter 2: Setting Up Authentication

## What You'll Build

A secure student login system using Amazon Cognito that:
- Lets students sign up/in with email + password
- Issues JWTs stored in httpOnly cookies (not localStorage)
- Protects all API endpoints — no valid token = no access
- Separates students from instructors via Cognito groups

---

## Amazon Cognito Concepts

| Concept | What It Is |
|---------|-----------|
| **User Pool** | A user directory — stores usernames, passwords, attributes |
| **App Client** | Your application's credentials to interact with the User Pool |
| **Hosted UI** | Pre-built login/signup page from Cognito (no custom form needed) |
| **JWT** | JSON Web Token — signed proof of identity, verified without calling Cognito |
| **PKCE** | Proof Key for Code Exchange — prevents authorization code interception |
| **Groups** | Role-based access control — `students`, `instructors` |

---

## Step 1: CDK — Create the Cognito User Pool

```python
# infrastructure/auth_stack.py

from aws_cdk import (
    Stack,
    Duration,
    RemovalPolicy,
    aws_cognito as cognito,
)
from constructs import Construct


class TeachingAgentAuthStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # User Pool — the identity store
        self.user_pool = cognito.UserPool(
            self, "StudentPool",
            user_pool_name="teaching-agent-students",
            
            # Sign-in with email
            sign_in_aliases=cognito.SignInAliases(email=True),
            
            # Self sign-up disabled — instructor creates accounts
            self_sign_up_enabled=False,
            
            # Password policy
            password_policy=cognito.PasswordPolicy(
                min_length=8,
                require_lowercase=True,
                require_uppercase=True,
                require_digits=True,
                require_symbols=False,
            ),
            
            # Custom attributes for course tracking
            custom_attributes={
                "cohort": cognito.StringAttribute(mutable=True),
                "enrollment_date": cognito.StringAttribute(mutable=False),
            },
            
            # Account recovery via email
            account_recovery=cognito.AccountRecovery.EMAIL_ONLY,
            
            removal_policy=RemovalPolicy.RETAIN,  # Don't delete users on stack removal
        )

        # App Client — how the frontend authenticates
        self.app_client = self.user_pool.add_client(
            "FrontendClient",
            user_pool_client_name="teaching-agent-frontend",
            
            # Authorization Code flow with PKCE (most secure for SPAs)
            auth_flows=cognito.AuthFlow(
                user_password=False,  # Don't allow direct password auth
                user_srp=True,
            ),
            
            # OAuth settings
            o_auth=cognito.OAuthSettings(
                flows=cognito.OAuthFlows(authorization_code_grant=True),
                scopes=[cognito.OAuthScope.OPENID, cognito.OAuthScope.EMAIL, cognito.OAuthScope.PROFILE],
                callback_urls=["http://localhost:5173/callback", "https://yourdomain.com/callback"],
                logout_urls=["http://localhost:5173/", "https://yourdomain.com/"],
            ),
            
            # Token validity
            access_token_validity=Duration.hours(1),
            refresh_token_validity=Duration.days(30),
            id_token_validity=Duration.hours(1),
        )

        # Groups for RBAC
        cognito.CfnUserPoolGroup(
            self, "InstructorsGroup",
            group_name="instructors",
            user_pool_id=self.user_pool.user_pool_id,
            description="Course instructors with admin access",
        )

        cognito.CfnUserPoolGroup(
            self, "StudentsGroup",
            group_name="students",
            user_pool_id=self.user_pool.user_pool_id,
            description="Enrolled students",
        )
```

---

## Step 2: JWT Verification in FastAPI

When a student makes an API call, we need to verify their JWT is:
1. Signed by our Cognito User Pool (not forged)
2. Not expired
3. Issued for our App Client

```python
# backend/auth/cognito.py

import jwt
from jwt import PyJWKClient

# Cognito publishes its public keys at this URL
JWKS_URL = (
    f"https://cognito-idp.{REGION}.amazonaws.com/"
    f"{USER_POOL_ID}/.well-known/jwks.json"
)

def verify_token(token: str) -> StudentUser:
    """Verify JWT signature, expiry, and audience."""
    
    # 1. Fetch the public key that signed this token
    jwks_client = PyJWKClient(JWKS_URL)
    signing_key = jwks_client.get_signing_key_from_jwt(token)
    
    # 2. Decode and verify in one step
    payload = jwt.decode(
        token,
        signing_key.key,
        algorithms=["RS256"],
        audience=APP_CLIENT_ID,       # Must match our app client
        issuer=f"https://cognito-idp.{REGION}.amazonaws.com/{USER_POOL_ID}",
    )
    
    # 3. Extract student identity
    return StudentUser(
        id=payload["sub"],          # Unique, immutable student ID
        email=payload["email"],
        cohort=payload.get("custom:cohort"),
    )
```

**Why RS256?** Cognito signs tokens with RSA — we verify using the public key (from JWKS URL) without needing any secret. The key rotates automatically.

---

## Step 3: FastAPI Auth Middleware

```python
# backend/auth/middleware.py

class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Public paths skip auth
        if request.url.path in {"/health", "/docs"}:
            return await call_next(request)
        
        # Extract token from httpOnly cookie (preferred) or header
        token = request.cookies.get("access_token")
        if not token:
            auth_header = request.headers.get("Authorization", "")
            token = auth_header.removeprefix("Bearer ")
        
        if not token:
            return JSONResponse(status_code=401, content={"detail": "Auth required"})
        
        # Verify and attach user context
        try:
            student = verify_token(token)
            request.state.current_user = student
        except Exception:
            return JSONResponse(status_code=401, content={"detail": "Invalid token"})
        
        return await call_next(request)
```

Now every route handler can access `request.state.current_user` — guaranteed to be verified.

---

## Step 4: Frontend — Cognito Hosted UI Flow

```
Student clicks "Login"
        │
        ▼
Redirect to Cognito Hosted UI
(https://your-domain.auth.eu-west-2.amazoncognito.com/login)
        │
        ▼
Student enters email + password
        │
        ▼
Cognito redirects back with authorization code
(http://localhost:5173/callback?code=xyz)
        │
        ▼
Frontend exchanges code for tokens (PKCE)
        │
        ▼
Backend sets tokens in httpOnly cookies
        │
        ▼
Authenticated! All API calls include cookie automatically.
```

---

## Security Best Practices

### ✅ Do This
- Store tokens in **httpOnly** cookies (inaccessible to JavaScript = no XSS theft)
- Use **PKCE** flow (prevents authorization code interception)
- Set **short** access token lifetime (1 hour)
- Use **Secure** + **SameSite=Strict** cookie attributes
- Let Cognito handle password hashing and storage
- Disable self-sign-up (instructor creates accounts)

### ❌ Don't Do This
- Store tokens in localStorage (XSS = stolen tokens)
- Use implicit flow (tokens in URL = logged in browser history)
- Build custom password storage (you will get it wrong)
- Hard-code Cognito credentials in frontend code
- Skip token expiry verification

---

## Testing Authentication

```python
# tests/test_auth.py

def test_missing_token_returns_401(client):
    """Unauthenticated requests are rejected."""
    response = client.get("/api/chat")
    assert response.status_code == 401

def test_invalid_token_returns_401(client):
    """Malformed tokens are rejected."""
    response = client.get("/api/chat", cookies={"access_token": "not.a.real.jwt"})
    assert response.status_code == 401

def test_valid_token_passes(client, valid_jwt):
    """Valid JWT grants access and populates current_user."""
    response = client.post("/api/chat",
        json={"message": "What is RAG?"},
        cookies={"access_token": valid_jwt}
    )
    assert response.status_code == 200
```

---

## Next Chapter

In [Chapter 3: RAG Pipeline](./03-rag-pipeline.md), we'll build the knowledge retrieval system that grounds the agent's answers in your course materials.
