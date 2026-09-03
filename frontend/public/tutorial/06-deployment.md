# Chapter 6: Deployment

## What You'll Deploy

The full Teaching Agent system as serverless infrastructure on AWS, across **six** CDK stacks:

```
CDK Stacks:
├── TeachingAgentAuth        → Cognito User Pool + App Client (PKCE) + hosted UI + groups
├── TeachingAgentRAG         → S3 bucket for course materials (KB created out-of-band)
├── TeachingAgentGuardrails  → Bedrock Guardrail (published version)
├── TeachingAgentTracking    → DynamoDB table + GSI1
├── TeachingAgentAPI         → Lambda (FastAPI/Mangum) + API Gateway REST
└── TeachingAgentFrontend    → private S3 (OAC) + CloudFront (SPA + /api proxy)
```

> The frontend is its **own stack** (`TeachingAgentFrontend`), not part of the API stack. It serves the React SPA from a private S3 bucket via CloudFront and proxies `/api/*` to API Gateway.

---

## Prerequisites

```bash
aws sts get-caller-identity          # AWS creds configured
npm install -g aws-cdk && cdk --version
python3 --version                    # 3.12
node --version                       # 18+
```

> **`requirements.txt` lives at the project root**, not in `backend/`. The Lambda bundler and CI both install from the root file.

---

## Step 1: Bootstrap CDK

```bash
cdk bootstrap aws://YOUR_ACCOUNT_ID/eu-west-2
```

---

## Step 2: Understand the Dependency Order

CDK resolves order automatically, but there's a real chain plus a manual prerequisite:

```
Auth ─┐
RAG  ─┤
Guard┤─►  API  ─►  Frontend
Track┘
        ▲            ▲
        │            └ imports the API Gateway REST-API id (cross-stack)
        └ reads BEDROCK_KB_ID from SSM (see Step 3) + cross-stack refs
```

- **API** depends on Auth (user pool + app client + hosted-UI domain), Guardrails (guardrail id), Tracking (table), and the **SSM KB-ID parameter**.
- **Frontend** depends on the API (it imports the REST-API id to build the `/api/*` origin).

So the KB ID must be in SSM **before** the API stack synthesizes a real value (Step 3).

---

## Step 3: Create the Knowledge Base + Seed SSM (the manual prerequisite)

The `TeachingAgentRAG` stack only creates the S3 bucket. The Knowledge Base is created out-of-band, and its ID is handed to the Lambda via SSM:

```bash
# 1. Deploy the RAG stack first so the materials bucket exists
cd infrastructure && cdk deploy TeachingAgentRAG

# 2. Upload course materials
bash ../scripts/upload_to_s3.sh
#    (uploads ./course_materials to teaching-agent-materials-<account>)

# 3. Create the Bedrock KB pointing at that bucket, then store its ID in SSM.
#    scripts/create_kb.sh does BOTH — it creates the KB and runs:
#      aws ssm put-parameter \
#        --name "/teaching-agent/dev/bedrock-kb-id" \
#        --type String --value "<KB_ID>" --overwrite --region eu-west-2
bash ../scripts/create_kb.sh
```

At synth time, `app.py` resolves that parameter with `ssm.StringParameter.value_from_lookup(...)` and stamps the literal KB ID into the API stack. If the parameter is absent, it resolves to `""` and RAG degrades gracefully (the deploy still succeeds).

---

## Step 4: Deploy the Stacks

```bash
cd infrastructure
python -m venv .venv && source .venv/bin/activate
pip install -r ../requirements.txt      # root requirements
cdk synth

# Deploy everything (order resolved automatically)
cdk deploy --all --require-approval never
```

### How the Lambda gets its config

The API Lambda's environment variables come from **three** sources — it's not all "automatic cross-stack refs":

| Env var | Source |
|---------|--------|
| `COGNITO_USER_POOL_ID`, `COGNITO_APP_CLIENT_ID` | cross-stack ref → Auth |
| `COGNITO_DOMAIN` | cross-stack ref → Auth (hosted UI base URL) |
| `BEDROCK_GUARDRAIL_ID` | cross-stack ref → Guardrails |
| `TRACKING_TABLE_NAME` | cross-stack ref → Tracking |
| `BEDROCK_KB_ID` | **SSM lookup** (`value_from_lookup`) — NOT a cross-stack ref |
| `COGNITO_REGION`, `BEDROCK_GUARDRAIL_VERSION` (`"1"`), `TUTORIAL_DIR` | set explicitly in `api_stack.py` |
| `ALLOWED_ORIGINS` | set from the `frontend_origin` (CloudFront) value |

### How the Lambda is bundled (no Docker)

`api_stack.py` uses a **local** bundler (`LocalPipBundling`) — the `DockerImage` argument is a dummy that's never used. Two things matter:

- **Cross-platform wheels.** It installs dependencies for the Lambda runtime, not your laptop:
  ```
  pip install -r requirements.txt -t <out> \
    --platform manylinux2014_x86_64 --python-version 3.12 \
    --implementation cp --only-binary=:all:
  ```
  This avoids the classic `No module named 'pydantic_core._pydantic_core'` crash you get from bundling macOS/arm64 wheels for a Linux runtime.
- **Content-derived asset hash.** The asset hash is computed by walking `requirements.txt` + `backend/` + `tutorial/`. So a change to *any* backend source or tutorial file triggers a rebuild + redeploy. (A plain source-dir hash missed pip-flag-only changes; a static hash silently skipped code changes.) **Editing this very tutorial changes the hash and will redeploy the API Lambda on the next `cdk deploy`.**

---

## Step 5: Deploy the Frontend

The `TeachingAgentFrontend` stack creates a **private** S3 bucket (`teaching-agent-frontend-<account>`, reachable only via CloudFront OAC) and a CloudFront distribution. Two ways to publish the built SPA:

**Option A — CDK does it (recommended):** if `frontend/dist` exists, the stack's `BucketDeployment` uploads it and invalidates CloudFront automatically.
```bash
cd frontend && npm install && npm run build   # -> frontend/dist
cd ../infrastructure && cdk deploy TeachingAgentFrontend
```

**Option B — manual sync:**
```bash
cd frontend && npm run build
aws s3 sync dist/ s3://teaching-agent-frontend-<account>/ --delete
aws cloudfront create-invalidation --distribution-id <DIST_ID> --paths "/*"
```

The distribution serves `/*` from S3 (SPA; unknown paths fall back to `/index.html`) and routes `/api/*` to the API Gateway origin at path `/prod` — same origin, so cookies work with no CORS. The public URL is the distribution domain, e.g. **https://d32yz1ssnunfr5.cloudfront.net**.

> **Build-time env:** `frontend/.env.production` sets `VITE_API_URL=` (empty → relative `/api` via the proxy) and `VITE_COGNITO_REDIRECT_URI=https://<cloudfront-domain>/auth/callback`.

---

## Step 6: Per-environment config with CDK context

Two context values let the same code target different environments/domains:

```bash
# Environment selector — picks the SSM KB param /teaching-agent/{env}/bedrock-kb-id
cdk deploy --all -c env=prod

# Frontend origin — regenerates Cognito callback/logout URLs + API CORS
cdk deploy TeachingAgentAuth TeachingAgentAPI -c frontend_domain=my.cloudfront.net
```

Defaults: `env=dev`, `frontend_domain=<current CloudFront domain>`.

---

## Step 7: Create Your Admin Account

```bash
# Create yourself as an instructor
aws cognito-idp admin-create-user \
  --user-pool-id <USER_POOL_ID> \
  --username your.email@example.com \
  --user-attributes Name=email,Value=your.email@example.com \
                    Name=email_verified,Value=true \
                    Name=given_name,Value=Faris \
                    Name=family_name,Value=Haddad

# Set a permanent password (policy: 10+ chars, upper/lower/digit/symbol)
aws cognito-idp admin-set-user-password \
  --user-pool-id <USER_POOL_ID> \
  --username your.email@example.com \
  --password 'YourStrongPass!23' --permanent

# Add to the instructors group (required for the admin dashboard)
aws cognito-idp admin-add-user-to-group \
  --user-pool-id <USER_POOL_ID> \
  --username your.email@example.com \
  --group-name instructors
```

> Group membership is stamped into the JWT at login, so you must **log in fresh** after being added to `instructors` for the admin dashboard to unlock.

---

## CI/CD Pipeline (Optional)

```yaml
# .github/workflows/deploy.yml
name: Deploy Teaching Agent
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions: { id-token: write, contents: read }
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12' }
      - uses: actions/setup-node@v4
        with: { node-version: '18' }
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::YOUR_ACCOUNT:role/GitHubActionsRole
          aws-region: eu-west-2
      # Tests (requirements.txt is at the repo root)
      - run: |
          pip install -r requirements.txt
          pytest
      # Infra
      - run: |
          cd infrastructure
          pip install -r ../requirements.txt
          npx cdk deploy --all --require-approval never
      # Frontend
      - run: |
          cd frontend && npm ci && npm run build
          aws s3 sync dist/ s3://teaching-agent-frontend-${{ secrets.ACCOUNT_ID }}/ --delete
          aws cloudfront create-invalidation --distribution-id ${{ secrets.DIST_ID }} --paths "/*"
```

---

## Monitoring & Observability

### CloudWatch Logs
Structured logging (`structlog`, JSON) means you can query Lambda logs directly:
```
fields @timestamp, student_id, path, guardrail_triggered
| filter guardrail_triggered = true
| sort @timestamp desc
| limit 20
```

### Key Metrics to Watch
| Metric | Where | Alert Threshold |
|--------|-------|-----------------|
| Lambda errors | CloudWatch | >5% error rate |
| Lambda duration | CloudWatch | P99 > 25s |
| Guardrail triggers | DynamoDB/CW | >20% of requests |
| DynamoDB throttles | CloudWatch | Any throttle |
| CloudFront 5xx | CloudWatch | Sustained >1% |

---

## Cost Optimization

1. **Lambda memory**: 1024MB today; tune with Lambda Power Tuning.
2. **DynamoDB**: on-demand billing — no capacity planning for bursty traffic.
3. **Knowledge Base**: OpenSearch Serverless scales down when idle.
4. **CloudFront**: cache the SPA aggressively (hashed asset filenames); `/api/*` is not cached.
5. **Bedrock**: the code defaults to Claude 3 Haiku for cost; cap output with `maxTokens`.

---

## Tear-Down (When Course Ends)

```bash
cdk destroy --all
```

What actually gets removed vs retained:
- **Removed on destroy:** the `TeachingAgentFrontend` bucket (it's `RemovalPolicy.DESTROY` with `auto_delete_objects=True`), CloudFront, Lambda, API Gateway, the guardrail.
- **Retained by design:** the DynamoDB tracking table, the Cognito user pool, and the RAG materials bucket are `RETAIN` — so student data and course materials survive. Delete them manually if you truly want a full cleanup:
```bash
aws dynamodb delete-table --table-name teaching-agent-tracking
aws cognito-idp delete-user-pool --user-pool-id <USER_POOL_ID>
aws s3 rb s3://teaching-agent-materials-<account> --force
# Also delete the out-of-band Bedrock KB + its SSM parameter:
aws ssm delete-parameter --name "/teaching-agent/dev/bedrock-kb-id"
```

---

## Next Chapter

In [Chapter 7: Extending the Agent](./07-extending.md), you'll learn how to add tools, implement multi-agent patterns, and evaluate your agent's quality.
