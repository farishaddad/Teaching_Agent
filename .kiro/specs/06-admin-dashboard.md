# Spec: Admin Dashboard & Student Management

## Goal
Provide an instructor-facing admin backend with a dashboard showing student interactions, weakness analysis, progress tracking, overall metrics (token usage, AWS costs), and student account management (create logins, manage access).

## Inputs
- Instructor authentication (must be in 'instructors' Cognito group)
- Student interaction data from DynamoDB
- Cognito user pool for student management
- AWS cost data (estimated from usage metrics)

## Outputs
- Overall dashboard: total students, interactions, tokens, costs, guardrail rates
- Per-student progress reports with weakness/strength analysis
- Student interaction history (paginated, searchable)
- Token usage and AWS cost breakdowns
- Student CRUD operations (create, update, disable, bulk-create, password reset)

## API Endpoints

### Dashboard
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/admin/dashboard` | Overall platform metrics (30d default) |
| GET | `/api/admin/costs` | AWS cost breakdown per service |
| GET | `/api/admin/metrics/tokens` | Token usage (by day/week/student) |

### Student Management
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/admin/students` | List all students (filter by cohort) |
| POST | `/api/admin/students` | Create single student account |
| POST | `/api/admin/students/bulk` | Bulk-create from list |
| GET | `/api/admin/students/{id}` | Get student profile |
| PATCH | `/api/admin/students/{id}` | Update student details |
| POST | `/api/admin/students/{id}/disable` | Disable account |
| POST | `/api/admin/students/{id}/reset-password` | Trigger password reset |

### Student Analytics
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/admin/students/{id}/progress` | Full progress report + weaknesses |
| GET | `/api/admin/students/{id}/interactions` | Paginated interaction history |

## Weakness Analysis Logic
- **Detection**: Keyword-based topic classification of each student query
- **Weakness flags**: >5 questions on a topic with confidence score <0.4
- **Confidence scoring**: Based on follow-up depth × sessions (surface-level repeats = low confidence)
- **Course taxonomy**: 16 topics mapped to keywords for automatic classification

## Cost Tracking
- Token costs: Input ($3/MTok) + Output ($15/MTok) for Claude 3.5 Sonnet
- Per-service breakdown: Bedrock inference, KB retrieval, Guardrails, DynamoDB, Lambda, API GW, S3, Cognito
- Derived metrics: cost-per-student, cost-per-interaction

## Authorization
- All `/api/admin/*` endpoints require `instructors` Cognito group membership
- Fallback: `ADMIN_EMAILS` environment variable (comma-separated)
- Students cannot access admin endpoints (403 Forbidden)

## Files Created
- `backend/admin/__init__.py`
- `backend/admin/models.py` — Pydantic models for all admin data structures
- `backend/admin/routes.py` — FastAPI router with all admin endpoints
- `backend/admin/student_manager.py` — Cognito CRUD operations
- `backend/admin/analytics.py` — Aggregation, weakness analysis, cost calculation

## Acceptance Criteria
- [ ] Only instructors (Cognito group or admin email list) can access admin routes
- [ ] Dashboard returns accurate 30-day metrics within 3 seconds
- [ ] Student creation triggers Cognito invite email with temporary password
- [ ] Bulk-create handles partial failures gracefully (per-student status)
- [ ] Weakness analysis correctly identifies struggling students by topic
- [ ] Cost breakdown reflects actual AWS pricing for eu-west-2
- [ ] Token usage can be grouped by day, week, or student
- [ ] Student interactions are paginated (max 100 per page)
- [ ] Disabled students cannot access the chat API

## Do Not Do
- Do NOT expose raw DynamoDB items — always use typed Pydantic models
- Do NOT allow students to access any admin endpoint
- Do NOT store AWS billing credentials in the app — use estimated costs from usage data
- Do NOT make cost queries synchronous if they're slow — cache with 15-min TTL
