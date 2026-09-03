# 🎓 Tutorial: Build Your Own AI Teaching Agent

## How This Agent Was Built — And How You Can Build One Too

Welcome! This tutorial walks you through every component of the Teaching Agent you're using right now — including the CloudFront-hosted frontend that served you this page. By the end, you'll understand how to build a production-ready AI agent with authentication, grounded Q&A, safety guardrails, student tracking, and public hosting.

---

## Tutorial Chapters

| # | Chapter | What You'll Learn |
| --- | --- | --- |
| 1 | [Architecture Overview](./01-architecture.md) | The six CDK stacks, the CloudFront front door, in-Lambda JWT auth, how components connect |
| 2 | [Authentication](./02-authentication.md) | Cognito hosted UI + PKCE, httpOnly-cookie JWTs, the in-Lambda middleware, silent refresh |
| 3 | [RAG Pipeline](./03-rag-pipeline.md) | Bedrock Knowledge Bases, the out-of-band KB + SSM handoff, grounded answers |
| 4 | **[Guardrails](./04-guardrails.md)** | Topic denial, content filtering, PII protection, word policy, contextual grounding |
| 5 | [Tracking & Analytics](./05-tracking.md) | DynamoDB single-table logging, progress tracking, usage analytics |
| 6 | [Deployment](./06-deployment.md) | The 6-stack CDK deploy, KB-in-SSM, Lambda bundling, **CloudFront + S3 frontend hosting** |
| 7 | [Extending the Agent](./07-extending.md) | Tool use, multi-agent patterns, evaluation, **web search augmentation** |
| 8 | [Managing Course Materials](./08-course-materials.md) | Admin panel: presigned S3 upload, list/delete, one-click Knowledge Base **Sync** |

> Frontend hosting (CloudFront + private S3 + the same-origin `/api` proxy) is introduced in Chapter 1 and deployed in Chapter 6.

---

## Prerequisites

- AWS account with Bedrock access (eu-west-2)
- Python 3.12+
- Node.js 18+
- AWS CDK CLI (`npm install -g aws-cdk`)
- Basic understanding of AI/ML concepts (covered in the main course)

---

## Quick Start

```bash
# Clone the repo
git clone <repo-url>
cd Teaching_Agent

# Install Python deps (requirements.txt is at the PROJECT ROOT)
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Install frontend deps
cd frontend && npm install && cd ..

# 1) Bootstrap + deploy the non-frontend stacks
cd infrastructure
cdk bootstrap aws://YOUR_ACCOUNT_ID/eu-west-2
cdk deploy TeachingAgentAuth TeachingAgentRAG TeachingAgentGuardrails TeachingAgentTracking

# 2) Create the Bedrock Knowledge Base and store its ID in SSM
#    (create_kb.sh writes /teaching-agent/{env}/bedrock-kb-id)
bash ../scripts/upload_to_s3.sh
bash ../scripts/create_kb.sh

# 3) Deploy the API (now it resolves a real BEDROCK_KB_ID from SSM)
cdk deploy TeachingAgentAPI

# 4) Build + deploy the frontend to CloudFront
cd ../frontend && npm run build && cd ../infrastructure
cdk deploy TeachingAgentFrontend      # publishes frontend/dist + invalidates CloudFront
```

Local development (optional):

```bash
# Backend (uses the same root requirements.txt)
uvicorn backend.main:app --reload --port 8000

# Frontend dev server (proxies /api to the deployed API)
cd frontend && npm run dev
```

> The deployed app is served from the CloudFront distribution URL (e.g. `https://<id>.cloudfront.net`) — see Chapter 6.

---

## Key Learning Outcomes

After completing this tutorial, you will be able to:

1. **Design** a secure AI agent architecture with proper authentication
2. **Implement** RAG for grounding AI responses in your own knowledge base
3. **Configure** Amazon Bedrock Guardrails to keep an agent safe and on-topic
4. **Track** user interactions for analytics and progress monitoring
5. **Deploy** the complete system on AWS with CDK — including public CloudFront hosting

---

> 💡 **Meta-learning**: You're learning about AI agents by studying the AI agent that's teaching you — right down to the CloudFront distribution serving this page. This is Agentic AI in action!
