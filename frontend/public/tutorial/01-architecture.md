# Chapter 1: Architecture Overview

## System Design

The Teaching Agent is a full-stack AI application that combines several AWS services into a cohesive learning platform. This chapter introduces the overall design before we deep-dive into each component.

Everything is defined as infrastructure-as-code with **AWS CDK v2 (Python)** across **six stacks**, and the app you're reading this in is served publicly from **CloudFront**.

---

## High-Level Architecture

```
                          Browser (student / instructor)
                                     │  HTTPS
                                     ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                        CloudFront distribution                             │
│                     (<id>.cloudfront.net — public URL)                     │
│                                                                            │
│   default behavior  /*        ──►  private S3 bucket (OAC)  → React SPA    │
│   cache behavior    /api/*    ──►  API Gateway origin  (same-origin proxy) │
└───────────────┬───────────────────────────────────┬───────────────────────┘
                │ SPA assets (cached)                │ /api/* (not cached,
                │                                    │  cookies + headers forwarded)
        ┌───────▼────────┐            ┌──────────────▼───────────────┐
        │  S3 (private)  │            │   API Gateway (REST, proxy)   │
        │  SPA: index +  │            │   stage: prod  — no authorizer │
        │  hashed assets │            └──────────────┬────────────────┘
        └────────────────┘                           │
                                     ┌────────────────▼────────────────────┐
                                     │        Lambda (FastAPI via Mangum)   │
                                     │  JWTAuthMiddleware verifies the JWT  │
                                     │  (Cognito JWKS) on every request     │
                                     │                                      │
                                     │  Auth · RAG · Guardrails · Tracking  │
                                     │  · Admin · Tutorial routers          │
                                     └───┬─────┬─────────┬────────┬─────────┘
                                         │     │         │        │
                                    ┌────▼─┐ ┌─▼──────┐ ┌▼───────┐ ┌▼────────┐
                                    │Cognito││Bedrock │ │Bedrock │ │DynamoDB │
                                    │ User  ││  KB    │ │Guardrl │ │ table   │
                                    │ Pool  ││+Claude │ └────────┘ └─────────┘
                                    └───────┘└────────┘
```

**Key point:** the SPA and the API share the **same origin** (`https://<id>.cloudfront.net`). CloudFront serves the static React app for `/*` and transparently proxies `/api/*` to API Gateway. Because it's same-origin, browser requests carry the auth cookies with no CORS complications.

---

## The Six CDK Stacks

| Stack | Purpose |
|-------|---------|
| `TeachingAgentAuth` | Cognito user pool, app client (PKCE), hosted UI domain, `instructors`/`students` groups |
| `TeachingAgentRAG` | S3 bucket for course materials (the Knowledge Base itself is created out-of-band) |
| `TeachingAgentGuardrails` | Bedrock Guardrail (published version) |
| `TeachingAgentTracking` | DynamoDB single-table for interaction logging |
| `TeachingAgentAPI` | Lambda (FastAPI) + API Gateway REST API |
| `TeachingAgentFrontend` | Private S3 bucket (OAC) + CloudFront distribution serving the SPA and proxying `/api/*` |

---

## Component Breakdown

### 1. Frontend Delivery (CloudFront + S3)
- **What**: A private S3 bucket holding the built React/Vite SPA, fronted by CloudFront with Origin Access Control (OAC).
- **Why**: Cheap, fast, globally cached static hosting on a free `*.cloudfront.net` URL — no servers to run for the UI.
- **How**: `/*` is served from S3; unknown paths fall back to `/index.html` (so client-side routes like `/admin` and `/auth/callback` work). A separate `/api/*` behavior proxies to API Gateway so the whole app is one origin.

### 2. Authentication Layer
- **What**: Amazon Cognito User Pool with hosted UI and an authorization-code + PKCE app client.
- **Why**: Managed auth — no password storage, MFA-ready, group-based access control.
- **How**: Students sign in on the hosted UI → the backend exchanges the code for tokens → JWTs are stored in httpOnly cookies → verified **inside the Lambda** on every API call (see below).

### 3. RAG (Retrieval-Augmented Generation)
- **What**: Amazon Bedrock Knowledge Base backed by course-material files in S3.
- **Why**: Grounding — the agent answers from verified course content, not hallucinations.
- **How**: Student question → retrieve relevant chunks → synthesize an answer with citations. The KB is created out-of-band and its ID is handed to the Lambda via SSM (Chapter 3). An optional **web-search mode** can supplement the course materials with live results ([Chapter 7](./07-extending.md)).

### 4. Guardrails
- **What**: Amazon Bedrock Guardrails (topic denial + content filters + PII + word policy + contextual grounding), published as a **version** (not DRAFT).
- **Why**: Safety — prevents off-topic answers, harmful content, prompt injection, and data leaks.
- **How**: Applied to Bedrock calls on both input and output.

### 5. Student Tracking
- **What**: DynamoDB single-table design logging every interaction.
- **Why**: Traceability — per-student progress, weakness analysis, usage metrics.
- **How**: Fire-and-forget async writes after every response (don't block the chat).

### 6. Admin Dashboard
- **What**: Instructor-only routes for student management, analytics, and **course-materials management** (upload/list/delete the KB's source files + a one-click Knowledge Base **Sync**).
- **Why**: Course management — create logins, monitor engagement, spot struggling students, and keep the Knowledge Base content current without touching AWS.
- **How**: Gated by the `instructors` Cognito group (checked in the Lambda, and by a `RequireInstructor` guard in the SPA). Large uploads go **directly to S3 via presigned URLs**. Details in [Chapter 8](./08-course-materials.md).

---

## How Auth Is Actually Enforced (important)

There is **no API Gateway Cognito Authorizer**. The REST API is a plain Lambda proxy integration. Instead, a FastAPI middleware (`JWTAuthMiddleware`) runs inside the Lambda and:

1. Extracts the JWT from the `access_token` httpOnly cookie (or an `Authorization: Bearer` header).
2. Verifies the signature against the Cognito JWKS, plus issuer/expiry/client_id.
3. Attaches the authenticated user to the request, or returns `401`.
4. If the access token is expired but a `refresh_token` cookie is present, it silently refreshes.

This keeps verification logic in one place (versioned with the app) and lets the same code run locally under `uvicorn`. Details in [Chapter 2](./02-authentication.md).

---

## Why These AWS Services?

| Service | Alternative Considered | Why We Chose This |
|---------|----------------------|-------------------|
| **CloudFront + S3** | Amplify Hosting, EC2/nginx | Free `*.cloudfront.net` URL, global CDN, same-origin `/api` proxy, all in CDK |
| **Cognito** | Auth0, Firebase Auth | Native AWS integration, Cognito groups for RBAC, no extra vendor |
| **Bedrock KB** | Custom RAG (Pinecone + LangChain) | Fully managed — no vector DB ops, automatic chunking/embedding |
| **Bedrock Guardrails** | Custom content filters | Managed, versioned, no ML training needed, integrates natively |
| **DynamoDB** | PostgreSQL (RDS) | Serverless, pay-per-request, single-table design fits our access patterns |
| **Lambda + API Gateway** | ECS Fargate, EC2 | Zero idle cost, auto-scale, perfect for bursty student traffic |
| **CDK** | Terraform, CloudFormation YAML | Type-safe (Python), reusable constructs, better DX |

---

## Data Flow: Student Asks a Question

```
1. Student types: "What is RAG?"
2. SPA (served by CloudFront) sends POST /api/chat with the JWT cookie.
3. CloudFront routes /api/* to the API Gateway origin (same-origin, no CORS).
4. API Gateway (proxy) invokes the Lambda — there is NO Cognito authorizer.
5. Inside the Lambda, JWTAuthMiddleware verifies the JWT (Cognito JWKS) and
   extracts student_id; unauthenticated requests get 401 here.
6. RAG handler calls the Bedrock Knowledge Base:
   a. Retrieve: find relevant course-material chunks.
   b. Generate: Claude synthesizes an answer from those chunks.
7. Guardrails (attached to the Bedrock call):
   a. Input check: on-topic? no PII? no prompt injection?
   b. Output check: grounded in retrieved context? no harmful content?
8. If guardrails pass → return answer + citations.
   If guardrails block → return a friendly denial message.
9. Tracking: async write to DynamoDB (student_id, query, summary, timestamp).
10. SPA displays the grounded answer with source references.
```

---

## Security Architecture

```
┌─────────────────────────────────────────────────────────┐
│  DEFENSE IN DEPTH                                        │
│                                                          │
│  Layer 1: Edge / TLS      — CloudFront (HTTPS, private   │
│                              S3 via OAC — bucket not      │
│                              publicly reachable)          │
│  Layer 2: Authentication  — Cognito JWT (httpOnly cookie) │
│                              verified in-Lambda (JWKS)     │
│  Layer 3: Authorization   — Cognito groups (student/admin)│
│  Layer 4: Input Guard     — Bedrock Guardrails (input)    │
│  Layer 5: System Prompt   — Domain-locked instructions    │
│  Layer 6: Output Guard    — Bedrock Guardrails (output)   │
│  Layer 7: Data Isolation  — Per-student DynamoDB partition│
│                                                          │
│  No secrets in code (env vars / SSM)                     │
│  No localStorage tokens (httpOnly cookies only)          │
│  No cross-student data access                            │
└─────────────────────────────────────────────────────────┘
```

> Note: there is no AWS WAF in the current stack. TLS termination and the private-origin (OAC) model are provided by CloudFront; WAF would be a straightforward future addition on the distribution.

---

## Cost Model (Estimate for 50 Students)

| Component | Monthly Estimate | Notes |
|-----------|-----------------|-------|
| Bedrock (Claude) | ~$15–40 | Depends on usage volume and model (set via `BEDROCK_MODEL_ARN` — currently Claude Sonnet 4.5 via the EU cross-region inference profile; see Chapter 3) |
| Bedrock Knowledge Base | ~$5–10 | OpenSearch Serverless + retrieval |
| Bedrock Guardrails | ~$2–5 | Per-assessment pricing |
| DynamoDB | ~$1–3 | On-demand, low volume |
| Lambda | <$1 | 1024MB, short duration |
| S3 + CloudFront | <$1 | Small SPA + PDFs, cached at the edge |
| Cognito | ~$0.28 | 50 MAUs × $0.0055 |
| **Total** | **~$25–60/month** | For 50 active students |

---

## Next Chapter

In [Chapter 2: Authentication](./02-authentication.md), we'll set up Amazon Cognito and implement secure JWT-based login — including the PKCE hosted-UI flow, httpOnly cookies, and the in-Lambda middleware that enforces it.
