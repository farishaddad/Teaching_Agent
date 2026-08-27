# Teaching Agent — Agentic AI Course Companion

## What This Is

A full-stack AI teaching assistant that serves students enrolled in the **Agentic AI** course. Students can:

1. Ask questions about Agentic AI concepts, grounded in course materials (RAG)
2. Track their learning progress
3. Follow a built-in tutorial that teaches them how this agent was built (meta-learning)

## Tech Stack

| Layer | Technology |
| --- | --- |
| Frontend | React 18 + Vite + TailwindCSS |
| Backend API | Python 3.12 + FastAPI |
| Auth | Amazon Cognito (JWT) |
| LLM | Amazon Bedrock (Claude 3.5 Sonnet via Converse API) |
| RAG | Amazon Bedrock Knowledge Bases (OpenSearch Serverless) |
| Guardrails | Amazon Bedrock Guardrails |
| Tracking DB | Amazon DynamoDB |
| Infrastructure | AWS CDK v2 (Python) |
| Hosting | AWS Lambda + API Gateway (backend), CloudFront + S3 (frontend) |

## Project Structure

```
Teaching_Agent/
├── KIRO.md                    ← you are here
├── .kiro/
│   ├── steering/              ← persistent context for every Kiro session
│   ├── specs/                 ← per-module build specs
│   └── hooks/                 ← auto-validation on save
├── backend/
│   ├── api/                   ← FastAPI routes
│   ├── auth/                  ← Cognito JWT verification
│   ├── guardrails/            ← Bedrock Guardrails config + middleware
│   ├── rag/                   ← Bedrock KB retrieval + prompt construction
│   └── tracking/              ← DynamoDB student activity logging
│   └── admin/                 ← Instructor admin backend
│       ├── routes.py          ← /api/admin/* endpoints (dashboard, student mgmt)
│       ├── models.py          ← Dashboard + analytics Pydantic models
│       ├── student_manager.py ← Cognito CRUD (create/update/disable students)
│       └── analytics.py       ← Weakness analysis, progress, cost tracking
├── frontend/
│   └── src/
│       └── components/        ← React chat UI, auth, progress dashboard
├── infrastructure/            ← CDK stacks
├── course_materials/          ← PDFs, slides, references for RAG ingestion
├── tutorial/                  ← Step-by-step build guide (the meta-tutorial)
└── tests/                     ← Unit + integration tests

```

## Hard Rules

- **DO NOT** hardcode any secrets — all credentials via environment variables or AWS Secrets Manager
- **DO NOT** allow the agent to answer questions outside the Agentic AI domain (guardrails enforce this)
- **DO NOT** store plaintext passwords — Cognito handles auth entirely
- **DO NOT** expose student data in API responses to other students
- **ALL** LLM calls must pass through the guardrails middleware before reaching the student
- **ALL** student interactions must be logged to DynamoDB with timestamp, user_id, query, response_summary

## Current Priority

**Phase 1**: Authentication + Core Chat + Guardrails (MVP)

1. Cognito user pool + hosted UI for student login
2. FastAPI backend with JWT verification middleware
3. Bedrock RAG integration with course materials
4. Bedrock Guardrails (topic denial, PII filtering, toxicity)
5. Basic React chat interface

**Phase 2**: Tracking + Progress 6. DynamoDB activity logging 7. Student progress dashboard 8. Usage analytics per student

**Phase 2b**: Admin Backend 9. Instructor dashboard (overall metrics, daily trends) 10. Student management (create logins, bulk-create, disable, reset passwords) 11. Weakness analysis (per-topic confidence scoring, struggling-student detection) 12. Cost tracking (token usage, per-service AWS cost breakdown)

**Phase 3**: Tutorial Module 13. Interactive tutorial teaching students how this agent was built 14. Guardrails tutorial section

## Key Technical Notes

- Bedrock Guardrails are configured via `guardrailId` and `guardrailVersion` — passed in every Converse API call
- Cognito tokens have `sub` claim = unique student ID for tracking
- RAG retrieval uses `RetrieveAndGenerate` API with a knowledge base backed by course PDFs
- DynamoDB table: PK = `student_id`, SK = `timestamp#interaction_id`
- Frontend stores JWT in httpOnly cookies (not localStorage) for security

