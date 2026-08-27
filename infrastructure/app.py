"""CDK App — Teaching Agent Infrastructure."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import aws_cdk as cdk

from infrastructure.auth_stack import TeachingAgentAuthStack
from infrastructure.rag_stack import TeachingAgentRAGStack
from infrastructure.guardrails_stack import TeachingAgentGuardrailsStack
from infrastructure.tracking_stack import TeachingAgentTrackingStack
from infrastructure.api_stack import TeachingAgentAPIStack

app = cdk.App()

env = cdk.Environment(
    account=cdk.Aws.ACCOUNT_ID,
    region="eu-west-2",
)

# Stack 1: Authentication (Cognito)
auth_stack = TeachingAgentAuthStack(app, "TeachingAgentAuth", env=env)

# Stack 2: RAG (S3 bucket for course materials — KB created via console)
rag_stack = TeachingAgentRAGStack(app, "TeachingAgentRAG", env=env)

# Stack 3: Guardrails (Bedrock Guardrail)
guardrails_stack = TeachingAgentGuardrailsStack(app, "TeachingAgentGuardrails", env=env)

# Stack 4: Tracking (DynamoDB)
tracking_stack = TeachingAgentTrackingStack(app, "TeachingAgentTracking", env=env)

# Stack 5: API (Lambda + API Gateway) — depends on all others
api_stack = TeachingAgentAPIStack(
    app,
    "TeachingAgentAPI",
    env=env,
    user_pool=auth_stack.user_pool,
    knowledge_base_id="PLACEHOLDER_SET_AFTER_KB_CREATION",
    guardrail_id=guardrails_stack.guardrail_id,
    tracking_table=tracking_stack.table,
)

app.synth()
