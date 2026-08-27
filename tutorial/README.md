# 🎓 Tutorial: Build Your Own AI Teaching Agent

## How This Agent Was Built — And How You Can Build One Too

Welcome! This tutorial walks you through every component of the Teaching Agent you're using right now. By the end, you'll understand how to build a production-ready AI agent with authentication, grounded Q&A, safety guardrails, and student tracking.

---

## Tutorial Chapters

| # | Chapter | What You'll Learn |
| --- | --- | --- |
| 1 | [Architecture Overview](./01-architecture.md) | System design, AWS services, how components connect |
| 2 | [Authentication](./02-authentication.md) | Secure login with Amazon Cognito, JWT tokens, session management |
| 3 | [RAG Pipeline](./03-rag-pipeline.md) | Retrieval-Augmented Generation, Knowledge Bases, grounded answers |
| 4 | **[Guardrails](./04-guardrails.md)** | Safety policies, topic control, content filtering, PII protection |
| 5 | [Tracking & Analytics](./05-tracking.md) | DynamoDB logging, progress tracking, usage analytics |
| 6 | [Deployment](./06-deployment.md) | CDK infrastructure, CI/CD, monitoring |
| 7 | [Extending the Agent](./07-extending.md) | Tool use, multi-agent patterns, evaluation |

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

# Install backend dependencies
cd backend && pip install -r requirements.txt

# Install frontend dependencies
cd ../frontend && npm install

# Deploy infrastructure (requires AWS credentials)
cd ../infrastructure && cdk deploy --all

# Run locally
cd ../backend && uvicorn main:app --reload
cd ../frontend && npm run dev

```

---

## Key Learning Outcomes

After completing this tutorial, you will be able to:

1. **Design** a secure AI agent architecture with proper authentication
2. **Implement** RAG for grounding AI responses in your own knowledge base
3. **Configure** Amazon Bedrock Guardrails to keep an agent safe and on-topic
4. **Track** user interactions for analytics and progress monitoring
5. **Deploy** the complete system on AWS using Infrastructure as Code

---

> 💡 **Meta-learning**: You're learning about AI agents by studying the AI agent that's teaching you. This is Agentic AI in action!

