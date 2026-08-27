# Spec: Tutorial Module

## Goal
Create an interactive, step-by-step tutorial that teaches students how this Teaching Agent was built — including authentication, RAG, guardrails, and deployment. This is the "meta" layer: learning about AI agents by studying the agent that teaches them.

## Tutorial Structure

### Chapter 1: Architecture Overview
- System design diagram
- Component breakdown (auth, RAG, guardrails, tracking)
- AWS services used and why

### Chapter 2: Setting Up Authentication
- Cognito concepts (User Pools, App Clients, JWT)
- CDK code walkthrough for auth infrastructure
- Implementing JWT verification in FastAPI
- Security best practices (httpOnly cookies, PKCE flow)

### Chapter 3: Building the RAG Pipeline
- What is RAG and why it matters for grounding
- Creating a Bedrock Knowledge Base
- Ingesting course materials (chunking strategies)
- Writing effective system prompts
- Implementing retrieve-and-generate

### Chapter 4: Implementing Guardrails
- Why guardrails are essential for production AI
- Amazon Bedrock Guardrails overview
- Configuring topic denial policies
- Content filtering (toxicity, PII)
- Contextual grounding checks
- Testing guardrails with adversarial inputs
- **Hands-on**: Students configure their own guardrail policy

### Chapter 5: Tracking & Analytics
- DynamoDB single-table design for AI interactions
- Async logging patterns
- Building a progress dashboard

### Chapter 6: Deployment
- CDK stack overview
- CI/CD pipeline
- Monitoring and observability

### Chapter 7: Extending the Agent
- Adding new tools (function calling)
- Multi-agent patterns
- Evaluation and testing agents

## Files to Create
- `tutorial/README.md` — Tutorial overview and navigation
- `tutorial/01-architecture.md`
- `tutorial/02-authentication.md`
- `tutorial/03-rag-pipeline.md`
- `tutorial/04-guardrails.md` — **Key chapter**: detailed guardrails guide
- `tutorial/05-tracking.md`
- `tutorial/06-deployment.md`
- `tutorial/07-extending.md`
- `tutorial/assets/` — Diagrams, screenshots
- `frontend/src/components/Tutorial.tsx` — In-app tutorial viewer

## Acceptance Criteria
- [ ] Tutorial is accessible within the app (dedicated /tutorial route)
- [ ] Each chapter has working code examples students can reference
- [ ] Guardrails chapter is comprehensive enough for students to set up their own
- [ ] Code snippets match the actual production code (not separate examples)
- [ ] Tutorial tracks student progress (which chapters completed)
- [ ] Interactive elements: code blocks with copy button, expandable explanations

## Do Not Do
- Do NOT make tutorial code different from production code — keep them in sync
- Do NOT require students to have AWS accounts to follow along (provide screenshots/recordings for AWS Console steps)
- Do NOT make the guardrails chapter superficial — this is a key learning outcome
