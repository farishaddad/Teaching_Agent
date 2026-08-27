# AWS Conventions

## CDK v2
- All constructs in a single `infrastructure/` directory
- Stack naming: `TeachingAgent{Component}Stack` (e.g. `TeachingAgentAuthStack`)
- Use L2 constructs where available
- Tags on all resources: `project=teaching-agent`, `environment={dev|prod}`

## Lambda
- Runtime: Python 3.12
- Memory: 512MB (default), 1024MB for RAG-heavy handlers
- Timeout: 30s (API handlers), 120s (RAG retrieval)
- Bundling: Docker-based (for numpy/boto3 layers)
- Handler pattern: `handler.lambda_handler`

## DynamoDB
- Single-table design
- PK: `student_id` (Cognito `sub`)
- SK: `{entity_type}#{timestamp}#{ulid}`
- GSI1: For querying by date range across all students (admin)
- On-demand billing mode

## Bedrock
- Model: `anthropic.claude-3-5-sonnet-20241022-v2:0`
- Guardrail: Created via CDK, referenced by ID + version
- Knowledge Base: S3 data source → OpenSearch Serverless collection
- Region: eu-west-2

## Cognito
- User Pool with email-based sign-up
- App client: Authorization code flow (PKCE)
- Custom attributes: `custom:cohort`, `custom:enrollment_date`
- Hosted UI for login/signup (custom domain optional)

## Naming
- Resources: `teaching-agent-{component}-{env}` (e.g. `teaching-agent-api-dev`)
- Lambda functions: `teaching-agent-{purpose}` (e.g. `teaching-agent-chat-handler`)
