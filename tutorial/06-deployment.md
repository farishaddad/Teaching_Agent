# Chapter 6: Deployment

## What You'll Deploy

The full Teaching Agent system as serverless infrastructure on AWS:

```
CDK Stacks:
├── TeachingAgentAuth        → Cognito User Pool + App Client + Groups
├── TeachingAgentRAG         → S3 Bucket + Bedrock Knowledge Base config
├── TeachingAgentGuardrails  → Bedrock Guardrail resource
├── TeachingAgentTracking    → DynamoDB Table + GSI
└── TeachingAgentAPI         → Lambda + API Gateway + CloudFront (frontend)
```

---

## Prerequisites

```bash
# AWS CLI configured with appropriate permissions
aws sts get-caller-identity

# CDK CLI installed
npm install -g aws-cdk
cdk --version

# Python 3.12 + venv
python3 --version

# Node 18+ (for frontend build)
node --version
```

---

## Step 1: Bootstrap CDK

CDK needs a one-time bootstrap to create its deployment bucket:

```bash
cdk bootstrap aws://YOUR_ACCOUNT_ID/eu-west-2
```

---

## Step 2: Deploy All Stacks

```bash
cd infrastructure

# Create virtual environment for CDK
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Synthesize (validate templates)
cdk synth

# Deploy all stacks (in dependency order)
cdk deploy --all --require-approval broadening
```

**Deployment Order** (CDK handles this automatically):
1. Auth → no dependencies
2. RAG → no dependencies
3. Guardrails → no dependencies
4. Tracking → no dependencies
5. API → depends on Auth, RAG, Guardrails, Tracking

---

## Step 3: Post-Deploy Configuration

After CDK completes, you need to:

### 3a. Create the Bedrock Knowledge Base
```bash
# Upload course materials to S3
aws s3 sync ./course_materials/ s3://teaching-agent-course-materials/

# Create KB via console (or CLI):
# Bedrock → Knowledge Bases → Create → Point to S3 bucket
# → Choose Titan Embeddings V2 → OpenSearch Serverless → Sync
```

### 3b. Note the Output Values
CDK outputs the IDs you need:
```
TeachingAgentAuth.UserPoolId = eu-west-2_abc123
TeachingAgentAuth.AppClientId = 1234567890abcdef
TeachingAgentGuardrails.GuardrailId = xyz789
TeachingAgentTracking.TableName = teaching-agent-tracking
```

### 3c. Set Lambda Environment Variables
These are set automatically by CDK cross-stack references.

---

## Step 4: Deploy Frontend

```bash
cd frontend
npm install
npm run build  # Creates dist/

# Upload to S3 + invalidate CloudFront
aws s3 sync dist/ s3://teaching-agent-frontend/ --delete
aws cloudfront create-invalidation --distribution-id YOUR_DIST_ID --paths "/*"
```

---

## Step 5: Create Your Admin Account

```bash
# Create yourself as an instructor
aws cognito-idp admin-create-user \
  --user-pool-id eu-west-2_abc123 \
  --username your.email@example.com \
  --user-attributes Name=email,Value=your.email@example.com \
                    Name=email_verified,Value=true \
                    Name=given_name,Value=Faris \
                    Name=family_name,Value=Haddad \
  --temporary-password YourTempPass123!

# Add to instructors group
aws cognito-idp admin-add-user-to-group \
  --user-pool-id eu-west-2_abc123 \
  --username your.email@example.com \
  --group-name instructors
```

---

## CI/CD Pipeline (Optional)

For automated deployments on every push:

```yaml
# .github/workflows/deploy.yml

name: Deploy Teaching Agent
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      
      - uses: actions/setup-node@v4
        with:
          node-version: '18'
      
      # Configure AWS credentials (OIDC)
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::YOUR_ACCOUNT:role/GitHubActionsRole
          aws-region: eu-west-2
      
      # Backend tests
      - run: |
          cd backend
          pip install -r ../requirements.txt
          pytest
      
      # CDK deploy
      - run: |
          cd infrastructure
          pip install -r requirements.txt
          npx cdk deploy --all --require-approval never
      
      # Frontend build + deploy
      - run: |
          cd frontend
          npm ci
          npm run build
          aws s3 sync dist/ s3://teaching-agent-frontend/ --delete
```

---

## Monitoring & Observability

### CloudWatch Logs
Lambda logs are automatic. Structured logging (`structlog` with JSON) means you can query:
```
fields @timestamp, student_id, query, guardrail_triggered
| filter guardrail_triggered = true
| sort @timestamp desc
| limit 20
```

### CloudWatch Alarms (Recommended)
```python
# In CDK:
alarm = cloudwatch.Alarm(
    self, "HighGuardrailRate",
    metric=lambda_fn.metric("guardrail_triggers"),
    threshold=50,
    evaluation_periods=1,
    alarm_description="More than 50 guardrail blocks in 5 minutes — possible abuse",
)
```

### Key Metrics to Watch
| Metric | Where | Alert Threshold |
|--------|-------|-----------------|
| Lambda errors | CloudWatch | >5% error rate |
| Lambda duration | CloudWatch | P99 > 25s |
| Guardrail triggers | DynamoDB/CW | >20% of requests |
| DynamoDB throttles | CloudWatch | Any throttle |
| Cognito failed logins | CloudWatch | >10 per student/hour |

---

## Cost Optimization

1. **Lambda memory**: Start at 512MB, monitor with Lambda Power Tuning
2. **DynamoDB**: On-demand billing (no capacity planning needed for bursty student traffic)
3. **Knowledge Base**: OpenSearch Serverless scales to zero when idle
4. **CloudFront**: Cache static frontend aggressively (1 year for hashed assets)
5. **Bedrock**: Use `maxTokens` in Converse calls to cap output length

---

## Tear-Down (When Course Ends)

```bash
# Remove stacks (DynamoDB + Cognito retained by default)
cdk destroy --all

# If you want full cleanup:
aws dynamodb delete-table --table-name teaching-agent-tracking
aws cognito-idp delete-user-pool --user-pool-id eu-west-2_abc123
```

---

## Next Chapter

In [Chapter 7: Extending the Agent](./07-extending.md), you'll learn how to add tools, implement multi-agent patterns, and evaluate your agent's quality.
