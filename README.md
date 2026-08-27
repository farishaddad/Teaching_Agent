# 🤖 Teaching Agent — Agentic AI Course Companion

An AI-powered student guide for the **Introduction to Agentic AI** course. Built with Amazon Bedrock, this agent answers student questions grounded in course materials, with comprehensive safety guardrails and per-student progress tracking.

## ✨ Features

- **🔐 Secure Authentication** — Amazon Cognito with JWT, per-student identity
- **💬 RAG-Powered Q&A** — Answers grounded in course materials via Bedrock Knowledge Bases
- **🛡️ Safety Guardrails** — Topic denial, content filtering, PII protection, anti-hallucination
- **📊 Progress Tracking** — Per-student usage analytics, topic engagement, learning progress
- **📚 Built-in Tutorial** — Meta-learning: students learn how this agent was built

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│   React UI  │────▶│  API Gateway │────▶│  Lambda (FastAPI)│
│  (CloudFront)│     │  + Cognito   │     │                 │
└─────────────┘     └──────────────┘     └────────┬────────┘
                                                   │
                    ┌──────────────────────────────┼──────────────────┐
                    │                              │                  │
              ┌─────▼─────┐    ┌──────────────────▼┐    ┌───────────▼──┐
              │  Bedrock   │    │  Bedrock Knowledge │    │   DynamoDB   │
              │ Guardrails │    │  Base (RAG + S3)   │    │  (Tracking)  │
              └────────────┘    └────────────────────┘    └──────────────┘
```

## 🚀 Getting Started

### Prerequisites
- AWS Account with Bedrock access (eu-west-2)
- Python 3.12+, Node.js 18+
- AWS CDK CLI

### Deploy
```bash
cd infrastructure
pip install -r requirements.txt
cdk bootstrap
cdk deploy --all
```

### Local Development
```bash
# Backend
cd backend
pip install -r ../requirements.txt
uvicorn main:app --reload --port 8000

# Frontend
cd frontend
npm install && npm run dev
```

## 📖 Tutorial

This project includes a comprehensive tutorial teaching students how it was built:
- [Tutorial Home](./tutorial/README.md)
- [Chapter 4: Guardrails](./tutorial/04-guardrails.md) — Key safety chapter

## 🛡️ Guardrails

The agent enforces:
- **Topic boundaries**: Only Agentic AI course topics allowed
- **Content safety**: Hate, violence, sexual content blocked
- **PII protection**: Emails, phones, addresses anonymized in logs
- **Grounding**: Responses must be supported by course materials
- **Credential blocking**: AWS keys are never passed through

## 📁 Project Structure

```
Teaching_Agent/
├── backend/          # FastAPI application
│   ├── api/          # Route handlers
│   ├── auth/         # Cognito JWT verification
│   ├── guardrails/   # Bedrock Guardrails integration
│   ├── rag/          # Knowledge Base retrieval
│   └── tracking/     # DynamoDB student logging
├── frontend/         # React + Vite + TailwindCSS
├── infrastructure/   # AWS CDK stacks
├── tutorial/         # Step-by-step build guide
├── course_materials/ # PDFs/slides for RAG ingestion
└── tests/            # Unit + integration tests
```

## 📄 License

Internal — for course participants only.
