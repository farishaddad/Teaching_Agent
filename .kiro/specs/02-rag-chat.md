# Spec: RAG Chat Module

## Goal
Implement the core Q&A functionality — students ask questions about Agentic AI, answers are grounded in course materials via Bedrock Knowledge Bases.

## Inputs
- Student question (text)
- Course materials (PDFs, slides) ingested into Bedrock Knowledge Base
- Student context (who they are, what they've asked before)

## Outputs
- Grounded answer with source citations
- Retrieved passages for transparency
- Interaction logged to DynamoDB

## Files to Create
- `backend/rag/__init__.py`
- `backend/rag/knowledge_base.py` — Bedrock KB retrieve + generate logic
- `backend/rag/prompt_templates.py` — System prompts, few-shot examples
- `backend/rag/chat_handler.py` — Orchestrates retrieval → guardrails → response
- `backend/api/chat_routes.py` — POST /api/chat endpoint
- `backend/api/models.py` — Request/response Pydantic models
- `infrastructure/rag_stack.py` — CDK: S3 bucket, KB, OpenSearch Serverless
- `tests/test_rag.py` — Unit tests with mocked Bedrock calls

## Acceptance Criteria
- [ ] POST /api/chat accepts `{ "message": "..." }` and returns grounded answer
- [ ] Answers cite specific course material sources (page/section references)
- [ ] System prompt constrains agent to Agentic AI domain
- [ ] Conversation history (last 5 turns) included for context continuity
- [ ] Streaming response via Server-Sent Events (SSE)
- [ ] Graceful fallback when no relevant material found ("I don't have information on that in the course materials")
- [ ] Every interaction logged: student_id, timestamp, query, response, sources_used

## Do Not Do
- Do NOT answer questions outside course scope (guardrails handle this, but also system prompt)
- Do NOT return raw retrieved chunks without synthesis
- Do NOT allow prompt injection — sanitize user input
