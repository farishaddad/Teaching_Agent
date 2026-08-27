# Spec: Student Tracking Module

## Goal
Log all student interactions and derive progress metrics — enabling per-student traceability, usage analytics, and learning progress tracking.

## Inputs
- Every chat interaction (question + response + sources)
- Student identity (from JWT)
- Timestamp, session info

## Outputs
- DynamoDB records for every interaction
- Student progress dashboard data (topics covered, engagement metrics)
- Admin analytics (aggregate usage, popular topics, guardrail violations)

## DynamoDB Single-Table Design

| Entity | PK | SK | Attributes |
|--------|----|----|------------|
| Interaction | `STU#{student_id}` | `INT#{timestamp}#{ulid}` | query, response_summary, sources, guardrail_triggered, tokens_used |
| Session | `STU#{student_id}` | `SES#{session_id}` | start_time, end_time, interaction_count |
| Progress | `STU#{student_id}` | `PRG#{topic_slug}` | topic_name, questions_asked, confidence_score, last_accessed |
| Daily Summary | `STU#{student_id}` | `DAY#{date}` | total_questions, topics_explored, time_spent_seconds |

### GSI1 (Admin queries)
- GSI1PK: `DATE#{date}` — query all activity for a given day
- GSI1SK: `STU#{student_id}` — sort by student

## Files to Create
- `backend/tracking/__init__.py`
- `backend/tracking/models.py` — DynamoDB entity models
- `backend/tracking/repository.py` — CRUD operations (boto3 DynamoDB)
- `backend/tracking/progress.py` — Topic extraction + confidence scoring
- `backend/tracking/analytics.py` — Aggregate metrics for dashboard
- `backend/api/progress_routes.py` — GET /api/progress, GET /api/usage
- `infrastructure/tracking_stack.py` — CDK: DynamoDB table + GSIs
- `tests/test_tracking.py`

## Acceptance Criteria
- [ ] Every chat interaction creates a DynamoDB record within 200ms (async write)
- [ ] Students can view their own progress: topics explored, questions asked, time spent
- [ ] Topic extraction identifies which course modules the student is engaging with
- [ ] Usage metrics: total questions, sessions, active days, avg session length
- [ ] Admin can query aggregate stats (no access to individual conversations without authorization)
- [ ] Data retention: 12 months, then TTL-based expiry

## Do Not Do
- Do NOT store full LLM responses in DynamoDB (too large) — store summary + token count
- Do NOT expose other students' data via any API endpoint
- Do NOT block the chat response waiting for tracking writes (fire-and-forget async)
