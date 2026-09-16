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
- **Your AWS CLI/profile region must be `eu-west-2`** (all resources live there, and
  CDK's synth-time SSM lookup resolves in your CLI region). Set it with
  `export AWS_REGION=eu-west-2` or in your profile, or pass `-c region=eu-west-2`.
  The account is taken from your credentials (`CDK_DEFAULT_ACCOUNT`) or `-c account=<id>`.

### Deploy
```bash
cd infrastructure
pip install -r requirements.txt
cdk bootstrap
# Pass your public frontend host once the CloudFront distribution exists.
cdk deploy --all -c frontend_domain=<distribution-id>.cloudfront.net
```

> **`frontend_domain` matters.** It has no default — several resources are
> configured from it, and they come out blank/broken if it's omitted:
> - the **materials S3 bucket CORS** rule (browser presigned uploads in the
>   admin Course Materials panel fail without it),
> - the **Cognito** hosted-UI callback/logout URLs, and
> - the API **CORS** allowed origin.
>
> On the very first deploy the distribution doesn't exist yet, so deploy once
> without it, then redeploy the `TeachingAgentRAG`, `TeachingAgentAuth`, and
> `TeachingAgentAPI` stacks with `-c frontend_domain=<host>` once you know the
> CloudFront domain. Pass the same flag on every subsequent deploy.

### 🧠 Knowledge Base setup

The API Lambda needs a Bedrock Knowledge Base (KB) ID to answer questions with RAG. That ID is **not** hardcoded — it is sourced from an SSM Parameter Store parameter that CDK reads at synth time, so the deployed value always matches the template (no configuration drift, no manual Lambda edits).

**SSM parameter convention** — the KB ID lives at a per-environment path:

```
/teaching-agent/{env}/bedrock-kb-id
```

The `{env}` segment is selected via CDK context (`-c env=dev|prod`) and defaults to `dev`. So the dev parameter is `/teaching-agent/dev/bedrock-kb-id` and prod is `/teaching-agent/prod/bedrock-kb-id`.

**Seed the parameter** once the KB exists:

```bash
aws ssm put-parameter \
  --name "/teaching-agent/dev/bedrock-kb-id" \
  --type String \
  --value "<KB_ID>" \
  --overwrite \
  --region eu-west-2
```

`scripts/create_kb.sh` runs this command for you automatically after it creates the Knowledge Base, so you only need to run it by hand if you created the KB some other way (e.g. the console).

**Deploy ordering** — because the API stack reads the KB ID at synth time, follow this order:

1. Deploy the RAG/S3 and other stacks first (`cdk deploy --all`, or at least `TeachingAgentRAG`). This creates the `teaching-agent-materials-*` bucket that the KB ingests from.
2. Create the Knowledge Base pointing at the materials bucket — via the Bedrock console or `scripts/create_kb.sh`.
3. Seed the SSM parameter with the new KB ID (the script does this; otherwise run the `put-parameter` command above).
4. Deploy the API stack so the Lambda picks up the real KB ID:
   ```bash
   cdk deploy TeachingAgentAPI
   ```

**First-deploy bootstrap** — on the very first deploy, before the KB exists and before the SSM parameter is set, the app resolves `BEDROCK_KB_ID` to an empty string. Synth and deploy still succeed, and RAG degrades gracefully: the runtime logs `knowledge_base_id_not_configured` and returns a safe "knowledge base not configured" response instead of erroring. Once you seed the parameter and redeploy `TeachingAgentAPI`, RAG comes online — no manual Lambda patching needed.

**Drift guarantee** — the KB ID is resolved from SSM at synth time (`value_from_lookup`) and stamped as a plain literal into the CloudFormation template, not a `{{resolve:ssm:...}}` dynamic reference. Because the deployed value equals the template value, `aws cloudformation detect-stack-drift --stack-name TeachingAgentAPI` reports the stack `IN_SYNC`, and redeploys no longer revert the KB ID to a placeholder.

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

Released under the [MIT License](./LICENSE).

Note that **course materials are not included** in this repository — the code
and infrastructure are open source, but the course content itself is private.
See `course_materials/README.md`.
