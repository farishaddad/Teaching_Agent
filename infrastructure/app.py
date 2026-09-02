"""CDK App — Teaching Agent Infrastructure."""

import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import aws_cdk as cdk
from aws_cdk import aws_ssm as ssm

from infrastructure.auth_stack import TeachingAgentAuthStack
from infrastructure.rag_stack import TeachingAgentRAGStack
from infrastructure.guardrails_stack import TeachingAgentGuardrailsStack
from infrastructure.tracking_stack import TeachingAgentTrackingStack
from infrastructure.api_stack import TeachingAgentAPIStack

app = cdk.App()

# A concrete account/region is required so synth-time context providers (the
# SSM ``value_from_lookup`` below) can resolve. The CDK CLI populates
# ``CDK_DEFAULT_ACCOUNT`` from the active credentials during synth/deploy; fall
# back to the project account when running outside the CLI.
env = cdk.Environment(
    account=os.environ.get("CDK_DEFAULT_ACCOUNT") or "062788795053",
    region="eu-west-2",
)

# Per-environment SSM parameter name for the Bedrock Knowledge Base ID. The
# same app deploys to dev/prod by selecting the environment via CDK context
# (``-c env=prod``), reading a different parameter for each.
deploy_env = app.node.try_get_context("env") or "dev"
kb_id_param_name = f"/teaching-agent/{deploy_env}/bedrock-kb-id"

# Stack 1: Authentication (Cognito)
auth_stack = TeachingAgentAuthStack(app, "TeachingAgentAuth", env=env)

# Stack 2: RAG (S3 bucket for course materials — KB created via console)
rag_stack = TeachingAgentRAGStack(app, "TeachingAgentRAG", env=env)

# Stack 3: Guardrails (Bedrock Guardrail)
guardrails_stack = TeachingAgentGuardrailsStack(app, "TeachingAgentGuardrails", env=env)

# Stack 4: Tracking (DynamoDB)
tracking_stack = TeachingAgentTrackingStack(app, "TeachingAgentTracking", env=env)

# Resolve the Bedrock Knowledge Base ID from the per-environment SSM parameter
# at synth time. ``value_from_lookup`` embeds the resolved literal into the
# synthesized template (drift-free) and caches it in ``cdk.context.json``. The
# lookup must be scoped to a Stack (not the App), so we run it in the RAG stack
# scope — the stack semantically responsible for the Knowledge Base materials.
#
# Bootstrap: before the parameter exists, ``value_from_lookup`` returns a dummy
# sentinel (``dummy-value-for-...``) during the first synth. We substitute an
# empty string so synth/deploy still succeed and the runtime degrades gracefully
# (RAG unavailable) instead of blocking the deployment.
_resolved_kb_id = ssm.StringParameter.value_from_lookup(rag_stack, kb_id_param_name)
resolved_kb_id = (
    "" if _resolved_kb_id.startswith("dummy-value-for-") else _resolved_kb_id
)

# Stack 5: API (Lambda + API Gateway) — depends on all others
api_stack = TeachingAgentAPIStack(
    app,
    "TeachingAgentAPI",
    env=env,
    user_pool=auth_stack.user_pool,
    app_client=auth_stack.app_client,
    cognito_domain=auth_stack.domain.base_url(),
    knowledge_base_id=resolved_kb_id,
    guardrail_id=guardrails_stack.guardrail_id,
    tracking_table=tracking_stack.table,
)

app.synth()
