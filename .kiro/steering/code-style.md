# Code Style & Conventions

## Python (Backend)
- Python 3.12, type hints on all function signatures
- FastAPI with Pydantic v2 models for request/response validation
- Async handlers where possible (`async def`)
- Naming: `snake_case` for functions/variables, `PascalCase` for classes
- Docstrings: Google style
- Logging: `structlog` with JSON output (structured logging for CloudWatch)
- Error handling: Custom exception classes → FastAPI exception handlers
- Tests: `pytest` + `pytest-asyncio`, test files mirror source structure

## TypeScript/React (Frontend)
- TypeScript strict mode
- Functional components with hooks
- TailwindCSS for styling (no CSS modules)
- State management: React Query (TanStack Query) for server state
- Naming: `camelCase` for variables/functions, `PascalCase` for components
- File naming: `ComponentName.tsx`, `useHookName.ts`

## Git
- Conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`
- Branch per feature: `feature/auth-flow`, `feature/guardrails`
- PR = spec completion (one spec → one PR)

## Security
- No secrets in code — env vars or Secrets Manager
- All API endpoints require valid JWT (except `/health`)
- Input sanitization via Pydantic validators
- CORS restricted to frontend domain only
