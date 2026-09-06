# Bugfix Requirements Document

## Introduction

The `teaching-agent-api` Lambda function in the `TeachingAgentAPI` CloudFormation stack has drifted from its CDK-defined configuration. The Lambda environment variable `BEDROCK_KB_ID` was set out-of-band (manually, after a console-based Knowledge Base creation) to the real, ACTIVE Bedrock Knowledge Base ID `JUZEF2UAU0` (KB name `teaching-agent-kb`). The CDK source, however, still hardwires the value `PLACEHOLDER_SET_AFTER_KB_CREATION`.

Because the real KB ID lives only in the deployed stack (not in version-controlled CDK), the configuration is in a state of drift. The next `cdk deploy` of `TeachingAgentAPI` will overwrite `BEDROCK_KB_ID` back to the placeholder. At runtime, `backend/rag/knowledge_base.py` reads `BEDROCK_KB_ID` (falling back to `BEDROCK_KNOWLEDGE_BASE_ID`) to call Bedrock `Retrieve` / `RetrieveAndGenerate`; with the placeholder value, those calls fail against a non-existent KB and RAG retrieval silently breaks until an operator manually re-sets the variable. This is a latent, production-breaking configuration drift.

Root cause chain (verified against source):
- `infrastructure/app.py` hardwires `knowledge_base_id="PLACEHOLDER_SET_AFTER_KB_CREATION"` when instantiating `TeachingAgentAPIStack`.
- `infrastructure/api_stack.py` maps that argument straight into the Lambda env var `"BEDROCK_KB_ID": knowledge_base_id`.
- `infrastructure/rag_stack.py` deliberately does not create the KB (only the S3 materials bucket), sets `self.knowledge_base_id = ""`, and emits a `NextStep` CfnOutput telling operators to create the KB via console and set `BEDROCK_KB_ID` manually.
- `backend/rag/knowledge_base.py` resolves the KB ID from the environment at runtime.
- Helper scripts `scripts/create_kb.sh` and `scripts/upload_to_s3.sh` echo instructions to set `BEDROCK_KB_ID` manually.

The desired outcome is that the KB ID reaches the API Lambda through a durable, version-controlled, per-environment mechanism so that deploys no longer revert it, drift is eliminated, and the bootstrap case (first deploy before the KB exists) does not fail synth or deploy. Three candidate mechanisms are captured as alternatives below; the specific choice is deferred to the design phase.

## Bug Analysis

### Current Behavior (Defect)

The CDK source and the live deployment disagree on `BEDROCK_KB_ID`, and any redeploy silently reverts the working value.

1.1 WHEN `cdk deploy TeachingAgentAPI` is run against the live stack THEN the system overwrites the Lambda `BEDROCK_KB_ID` environment variable from the real KB ID (`JUZEF2UAU0`) back to the literal `PLACEHOLDER_SET_AFTER_KB_CREATION`.
1.2 WHEN the `teaching-agent-api` Lambda runs with `BEDROCK_KB_ID` set to `PLACEHOLDER_SET_AFTER_KB_CREATION` THEN the system issues Bedrock `Retrieve` / `RetrieveAndGenerate` calls against a non-existent Knowledge Base ID and RAG retrieval fails.
1.3 WHEN the KB ID is changed only in the deployed stack (out-of-band) and not in CDK THEN the system leaves the CDK template and the live resource in configuration drift, with the working value recorded nowhere in version control.
1.4 WHEN an operator inspects the CDK source to determine the KB ID THEN the system provides only the placeholder value, giving no version-controlled record of the real, active KB.
1.5 WHEN the RAG retrieval breaks after a redeploy THEN the system requires a manual, out-of-band re-set of `BEDROCK_KB_ID` on the Lambda to restore service.

### Expected Behavior (Correct)

The KB ID is supplied to the API Lambda through a durable, version-controlled, per-environment mechanism that survives redeploys.

2.1 WHEN `cdk deploy TeachingAgentAPI` is run THEN the system SHALL resolve `BEDROCK_KB_ID` from a durable, version-controlled source of truth rather than a hardcoded placeholder, so the real KB ID is preserved across deploys.
2.2 WHEN the `teaching-agent-api` Lambda runs after a deploy THEN the system SHALL have `BEDROCK_KB_ID` set to the correct active Knowledge Base ID so RAG retrieval succeeds without manual intervention.
2.3 WHEN a deploy completes THEN the system SHALL leave no drift between the CDK-defined `BEDROCK_KB_ID` and the value on the live Lambda.
2.4 WHEN the KB ID must be changed (e.g. new KB, new environment) THEN the system SHALL allow it to be updated through the version-controlled / configured mechanism without editing hardcoded source constants, and per environment (dev/prod).
2.5 WHEN the KB ID is delivered to the Lambda THEN the system SHALL NOT hardcode any secret in source and SHALL keep the value configurable per environment.
2.6 WHEN the fix is applied THEN the system SHALL update the operator documentation, the helper scripts (`scripts/create_kb.sh`, `scripts/upload_to_s3.sh`), and the `rag_stack.py` `NextStep` CfnOutput to describe the chosen mechanism instead of instructing a manual `BEDROCK_KB_ID` set.

Candidate mechanisms (alternatives — decision deferred to design phase):

2.A SSM Parameter Store — the KB ID is stored once in an SSM parameter (out-of-band or scripted) and CDK reads it at deploy time to populate the Lambda env var.
2.B CDK context / `cdk.json` — the KB ID is supplied via `--context kbId=...` or persisted in `cdk.json` context, and read during synth.
2.C Define the Knowledge Base in CDK — create the Bedrock Knowledge Base (`CfnKnowledgeBase`) and its OpenSearch Serverless collection in the `TeachingAgentRAG` stack, then pass the generated KB ID to `TeachingAgentAPI` via a cross-stack reference, eliminating the manual console step entirely.

### Bootstrap requirement (first deploy before KB exists)

2.7 WHEN the stack is deployed for the first time before any Knowledge Base exists (bootstrap case) THEN the system SHALL synthesize and deploy successfully without failing, degrading gracefully (RAG unavailable) rather than blocking infrastructure deployment.

### Unchanged Behavior (Regression Prevention)

The fix must be scoped to KB ID delivery only; all other stack behavior must be preserved.

3.1 WHEN a Knowledge Base ID is correctly configured through the chosen mechanism THEN the system SHALL CONTINUE TO perform RAG retrieval (`Retrieve` / `RetrieveAndGenerate`) exactly as it does today with a valid ID.
3.2 WHEN the runtime resolves the KB ID THEN the system SHALL CONTINUE TO honour the existing precedence of `BEDROCK_KB_ID` with fallback to `BEDROCK_KNOWLEDGE_BASE_ID`, and CONTINUE TO fall back gracefully (log `knowledge_base_id_not_configured` and return a safe response / empty results) when no ID is present.
3.3 WHEN `TeachingAgentAPI` is deployed THEN the system SHALL CONTINUE TO set all other Lambda environment variables (`COGNITO_USER_POOL_ID`, `COGNITO_REGION`, `BEDROCK_GUARDRAIL_ID`, `BEDROCK_GUARDRAIL_VERSION`, `TRACKING_TABLE_NAME`, `TUTORIAL_DIR`) unchanged.
3.4 WHEN `TeachingAgentRAG` is deployed THEN the system SHALL CONTINUE TO create and retain the `teaching-agent-materials-123456789012` S3 materials bucket with its existing versioning, encryption, SSL enforcement, and RETAIN removal policy.
3.5 WHEN the other stacks (`TeachingAgentAuth`, `TeachingAgentGuardrails`, `TeachingAgentTracking`) are deployed THEN the system SHALL CONTINUE TO provision their resources and cross-stack references (user pool, guardrail ID, tracking table) unchanged.
3.6 WHEN the API Lambda's IAM policies are evaluated THEN the system SHALL CONTINUE TO grant the existing Bedrock, DynamoDB, and Cognito admin permissions unchanged.

## Bug Condition and Property Specification

### Bug Condition

```pascal
FUNCTION isBugCondition(X)
  INPUT: X of type DeploymentConfig   // the BEDROCK_KB_ID value delivered to the API Lambda by CDK
  OUTPUT: boolean

  // The bug is present whenever the value CDK delivers is the placeholder
  // (or otherwise not the real, active KB ID) rather than a durable, correct value.
  RETURN X.deliveredKbId = "PLACEHOLDER_SET_AFTER_KB_CREATION"
         OR X.deliveredKbId <> X.activeKbId
END FUNCTION
```

Concrete counterexample: after the KB `JUZEF2UAU0` is set manually on the Lambda, running `cdk deploy TeachingAgentAPI` (F, the current source) delivers `BEDROCK_KB_ID = "PLACEHOLDER_SET_AFTER_KB_CREATION"`, so `isBugCondition` is true and RAG retrieval breaks.

### Property — Fix Checking

```pascal
// Property: Fix Checking — KB ID is durable and correct after deploy
FOR ALL X WHERE isBugCondition(X) DO
  result ← deployApiStack'(X)          // F' = fixed CDK
  ASSERT result.deliveredKbId = X.activeKbId          // real KB ID, not placeholder
  ASSERT drift(result) = FALSE                        // no CFN drift after deploy
  ASSERT NOT hardcodedSecret(result)                  // no secret hardcoded in source
  ASSERT configurablePerEnvironment(result) = TRUE    // dev/prod configurable
END FOR

// Bootstrap sub-case: KB does not yet exist
FOR ALL X WHERE isBugCondition(X) AND X.activeKbId = NONE DO
  ASSERT synthAndDeploy'(X) SUCCEEDS                  // deploy does not fail
END FOR
```

### Property — Preservation Checking

```pascal
// Property: Preservation Checking — non-buggy configs behave identically
FOR ALL X WHERE NOT isBugCondition(X) DO
  ASSERT deployApiStack(X) = deployApiStack'(X)       // F(X) = F'(X)
END FOR
```

Where **F** is the current (unfixed) CDK/app source and **F'** is the fixed source. `activeKbId` is the ID of the live, ACTIVE Bedrock Knowledge Base (currently `JUZEF2UAU0`), and `NONE` denotes the bootstrap case where no KB exists yet.
