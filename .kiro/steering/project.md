# Project: Teaching Agent (Agentic AI Course Companion)

## Purpose
AI-powered student guide for an Agentic AI course. Provides Q&A grounded in course materials, tracks student progress, and includes a self-referential tutorial showing how to build such an agent.

## Stack
- **Runtime**: Python 3.12
- **Framework**: FastAPI (async)
- **Frontend**: React 18 + Vite + TailwindCSS
- **Auth**: Amazon Cognito (hosted UI + JWT)
- **LLM**: Amazon Bedrock — Claude 3.5 Sonnet via `bedrock-runtime` Converse API
- **RAG**: Amazon Bedrock Knowledge Bases (OpenSearch Serverless vector store)
- **Guardrails**: Amazon Bedrock Guardrails (content filtering, topic denial, PII redaction)
- **Database**: Amazon DynamoDB (single-table design)
- **IaC**: AWS CDK v2 (Python)
- **Region**: eu-west-2 (London)

## Deployment
- Backend: Lambda + API Gateway (REST)
- Frontend: S3 + CloudFront
- All infrastructure defined in CDK

## Contract
- This is a standalone project — no external service dependencies beyond AWS
- Students authenticate via Cognito hosted UI → receive JWT → all API calls carry JWT
- Every LLM response passes through Bedrock Guardrails before reaching the student
- Every interaction is logged to DynamoDB for traceability
