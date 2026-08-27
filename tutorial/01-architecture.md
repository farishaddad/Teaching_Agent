# Chapter 1: Architecture Overview

## System Design

The Teaching Agent is a full-stack AI application that combines several AWS services into a cohesive learning platform. This chapter introduces the overall design before we deep-dive into each component.

---

## High-Level Architecture

```
┌────────────────────────────────────────────────────────────────────────────┐
│                          FRONTEND (React + Vite)                           │
│  ┌──────────┐  ┌──────────────┐  ┌─────────────┐  ┌───────────────────┐  │
│  │  Login   │  │  Chat View   │  │  Tutorial   │  │  Admin Dashboard  │  │
│  └──────────┘  └──────────────┘  └─────────────┘  └───────────────────┘  │
└────────────────────────────────────────┬───────────────────────────────────┘
                                         │ HTTPS (JWT in httpOnly cookie)
┌────────────────────────────────────────▼───────────────────────────────────┐
│                     API GATEWAY + COGNITO AUTHORIZER                       │
└────────────────────────────────────────┬───────────────────────────────────┘
                                         │
┌────────────────────────────────────────▼───────────────────────────────────┐
│                        LAMBDA (FastAPI via Mangum)                         │
│                                                                            │
│  ┌──────────┐  ┌──────────┐  ┌────────────┐  ┌──────────┐  ┌─────────┐  │
│  │   Auth   │  │   RAG    │  │ Guardrails │  │ Tracking │  │  Admin  │  │
│  │Middleware│  │ Handler  │  │ Middleware │  │  Logger  │  │  Routes │  │
│  └──────────┘  └──────────┘  └────────────┘  └──────────┘  └─────────┘  │
└────────┬──────────────┬──────────────┬──────────────┬──────────────┬──────┘
         │              │              │              │              │
    ┌────▼────┐   ┌─────▼─────┐  ┌────▼────┐  ┌─────▼─────┐  ┌────▼────┐
    │ Cognito │   │  Bedrock  │  │ Bedrock │  │ DynamoDB  │  │ Cognito │
    │User Pool│   │    KB     │  │Guardrail│  │  Table    │  │  Admin  │
    └─────────┘   │ + Claude  │  └─────────┘  └───────────┘  │  APIs   │
                  └───────────┘                               └─────────┘
```

---

## Component Breakdown

### 1. Authentication Layer
- **What**: Amazon Cognito User Pool with hosted UI
- **Why**: Managed auth — no password storage, MFA-ready, group-based access control
- **How**: Students sign in → get JWT → JWT verified on every API call

### 2. RAG (Retrieval-Augmented Generation)
- **What**: Amazon Bedrock Knowledge Bases backed by course material PDFs
- **Why**: Grounding — the agent only answers from verified course content, not hallucinations
- **How**: Student question → retrieve top-5 relevant chunks → synthesize answer with citations

### 3. Guardrails
- **What**: Amazon Bedrock Guardrails (topic denial + content filters + PII + grounding)
- **Why**: Safety — prevents off-topic answers, harmful content, data leaks
- **How**: Applied automatically to every Converse API call (input + output filtering)

### 4. Student Tracking
- **What**: DynamoDB single-table design logging every interaction
- **Why**: Traceability — per-student progress, weakness analysis, usage metrics
- **How**: Fire-and-forget async writes after every response (don't block the chat)

### 5. Admin Dashboard
- **What**: Instructor-only backend with student management and analytics
- **Why**: Course management — create logins, monitor engagement, spot struggling students
- **How**: Protected by Cognito group membership (`instructors` group)

---

## Why These AWS Services?

| Service | Alternative Considered | Why We Chose This |
|---------|----------------------|-------------------|
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
2. Frontend sends POST /api/chat with JWT cookie
3. API Gateway validates JWT via Cognito Authorizer
4. Lambda receives request → Auth middleware extracts student_id from JWT
5. RAG handler calls Bedrock Knowledge Base:
   a. Retrieve: Find top-5 relevant course material chunks
   b. Generate: Claude synthesizes an answer from those chunks
6. Guardrails (configured in the Converse call):
   a. Input check: Is the question on-topic? No PII? No toxicity?
   b. Output check: Is the response grounded? No harmful content?
7. If guardrails pass → return answer + citations
   If guardrails block → return friendly denial message
8. Tracking: Async write to DynamoDB (student_id, query, response_summary, timestamp)
9. Frontend displays the grounded answer with source references
```

---

## Security Architecture

```
┌─────────────────────────────────────────────────────────┐
│  DEFENSE IN DEPTH                                       │
│                                                         │
│  Layer 1: Network        — CloudFront + WAF             │
│  Layer 2: Authentication — Cognito JWT (httpOnly cookie) │
│  Layer 3: Authorization  — Cognito groups (student/admin)│
│  Layer 4: Input Guard    — Bedrock Guardrails (input)    │
│  Layer 5: System Prompt  — Domain-locked instructions    │
│  Layer 6: Output Guard   — Bedrock Guardrails (output)   │
│  Layer 7: Data Isolation — Per-student DynamoDB partition │
│                                                         │
│  No secrets in code (env vars / Secrets Manager)        │
│  No localStorage tokens (httpOnly cookies only)         │
│  No cross-student data access                           │
└─────────────────────────────────────────────────────────┘
```

---

## Cost Model (Estimate for 50 Students)

| Component | Monthly Estimate | Notes |
|-----------|-----------------|-------|
| Bedrock (Claude 3.5 Sonnet) | ~$15–40 | Depends on usage volume |
| Bedrock Knowledge Base | ~$5–10 | OpenSearch Serverless + retrieval |
| Bedrock Guardrails | ~$2–5 | Per-assessment pricing |
| DynamoDB | ~$1–3 | On-demand, low volume |
| Lambda | <$1 | 512MB, short duration |
| S3 + CloudFront | <$1 | Small static site + PDFs |
| Cognito | ~$0.28 | 50 MAUs × $0.0055 |
| **Total** | **~$25–60/month** | For 50 active students |

---

## Next Chapter

In [Chapter 2: Authentication](./02-authentication.md), we'll set up Amazon Cognito and implement secure JWT-based login for students.
