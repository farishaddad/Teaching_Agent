# Implementation Plan

Bugfix: `BEDROCK_KB_ID` configuration drift. Source the API Lambda's Knowledge Base ID from an SSM parameter (`/teaching-agent/{env}/bedrock-kb-id`) resolved at synth time via `StringParameter.value_from_lookup`, with a graceful bootstrap default (`""`). No runtime code changes.

Tests are CDK synthesis assertions (`aws_cdk.assertions`) and template snapshots under `tests/`, using `pytest` (project convention). The bug lives in synthesized configuration, so validation is primarily template inspection plus a final manual deploy-and-detect-drift step against AWS.

- [x] 1. Write bug condition exploration test (BEFORE implementing fix)
  - **Property 1: Bug Condition** - Synth Delivers Placeholder KB ID
  - **CRITICAL**: This test MUST FAIL on the fixed code and PASS on the current unfixed source — running it now establishes the harness and reproduces the bug. Do NOT change code to make it pass yet.
  - **GOAL**: Surface the counterexample proving the drift bug exists in the synthesized template.
  - Create `tests/test_kb_id_config.py` as the test harness for this spec.
  - Synthesize the `TeachingAgentAPI` stack from current source (`app = App(); ... Template.from_stack(api_stack)`), locating the `AWS::Lambda::Function` for `teaching-agent-api`.
  - **Scoped PBT Approach**: The bug is deterministic; scope the property to the concrete failing case — assert `Environment.Variables.BEDROCK_KB_ID == "PLACEHOLDER_SET_AFTER_KB_CREATION"` (the `deliveredKbId` from `isBugCondition`, which `<>` the active KB ID `JUZEF2UAU0`).
  - Run on UNFIXED code.
  - **EXPECTED OUTCOME**: Test PASSES on unfixed source (confirms `isBugCondition` is true today). It will be inverted/superseded by the fix-checking test in task 3.2 once the fix stamps the real ID.
  - Document the counterexample found (synthesized `BEDROCK_KB_ID` is the placeholder, not `JUZEF2UAU0`; root cause = hardcoded literal in `infrastructure/app.py`).
  - _Requirements: 1.1, 1.2, 1.3, 1.4_

- [x] 2. Write preservation property tests (BEFORE implementing fix)
  - **Property 2: Preservation** - Non-KB-ID Stack Behavior Unchanged
  - **IMPORTANT**: Follow the observation-first methodology — record the synthesized templates of the UNFIXED source as the baseline before any change.
  - In `tests/test_kb_id_config.py`, synthesize `TeachingAgentAPI` and the sibling stacks (`TeachingAgentAuth`, `TeachingAgentGuardrails`, `TeachingAgentTracking`, `TeachingAgentRAG`) on unfixed source and capture their template JSON.
  - Observe and assert the six other API Lambda env vars are present with their current values: `COGNITO_USER_POOL_ID`, `COGNITO_REGION`, `BEDROCK_GUARDRAIL_ID`, `BEDROCK_GUARDRAIL_VERSION`, `TRACKING_TABLE_NAME`, `TUTORIAL_DIR` (Req 3.3).
  - Observe and assert the API Lambda IAM policy statements (Bedrock `InvokeModel`/`Converse`/`Retrieve`/`RetrieveAndGenerate`/`ApplyGuardrail`, DynamoDB read/write, Cognito admin) are present (Req 3.6).
  - Observe and assert the `TeachingAgentRAG` S3 materials bucket `teaching-agent-materials-062788795053` with versioning, S3-managed encryption, SSL enforcement, and RETAIN removal policy (Req 3.4).
  - Snapshot the `TeachingAgentAuth`, `TeachingAgentGuardrails`, `TeachingAgentTracking` templates for later equality comparison (Req 3.5).
  - Assert `backend/rag/knowledge_base.py` is unmodified — capture a content hash/baseline so a later diff can prove the runtime resolver precedence and graceful fallback are untouched (Req 3.1, 3.2).
  - Run on UNFIXED code.
  - **EXPECTED OUTCOME**: Tests PASS (this is the baseline behavior to preserve). They must still PASS after the fix.
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6_

- [x] 3. Fix for BEDROCK_KB_ID configuration drift (SSM value_from_lookup)

  - [x] 3.1 Resolve the KB ID from SSM in `infrastructure/app.py`
    - Read an environment selector from context: `env = app.node.try_get_context("env") or "dev"`.
    - Build the per-environment parameter name `param_name = f"/teaching-agent/{env}/bedrock-kb-id"` (Req 2.4, 2.5).
    - Resolve at synth time with `ssm.StringParameter.value_from_lookup(app, param_name)` (embeds a literal into the template → drift-free).
    - Detect the `value_from_lookup` dummy sentinel (value starting with `dummy-value-for-`) and substitute `""` so the bootstrap first-deploy synthesizes and deploys successfully (Req 2.7).
    - Pass the resolved value into `TeachingAgentAPIStack(..., knowledge_base_id=resolved_kb_id, ...)`, replacing the hardcoded `"PLACEHOLDER_SET_AFTER_KB_CREATION"`.
    - _Bug_Condition: isBugCondition(X) where X.deliveredKbId = "PLACEHOLDER_SET_AFTER_KB_CREATION" OR X.deliveredKbId <> X.activeKbId_
    - _Expected_Behavior: F' delivers BEDROCK_KB_ID = activeKbId from SSM; bootstrap (activeKbId = NONE) substitutes "" and still synthesizes/deploys_
    - _Preservation: only the source of the single BEDROCK_KB_ID value changes; all other app.py wiring untouched_
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.7_

  - [x] 3.2 Verify bug condition exploration test now reflects the fix (fix-checking)
    - **Property 1: Expected Behavior** - KB ID Is Durable and Correct After Synth
    - **IMPORTANT**: Update/extend the assertion from task 1 to encode the fixed expected behavior — do NOT invent unrelated tests.
    - With the SSM lookup seeded (mock/`cdk.context.json`) to `JUZEF2UAU0`, synth `TeachingAgentAPI` and assert `Environment.Variables.BEDROCK_KB_ID == "JUZEF2UAU0"` (real ID, not placeholder).
    - Add a per-environment test: synth with context `env=dev` vs `env=prod` reading different seeded values → assert each stamps its respective KB ID (Req 2.4).
    - Add a bootstrap-success test: with the lookup returning the dummy sentinel, assert synth succeeds and `BEDROCK_KB_ID == ""` (Req 2.7).
    - Add a literal-not-token assertion: `BEDROCK_KB_ID` is a plain string, NOT a `{{resolve:ssm:...}}` dynamic reference — guarantees drift-free behavior (Req 2.3). This confirms `api_stack.py` needs no behavioral change (task 3.3).
    - **EXPECTED OUTCOME**: Tests PASS (confirms bug is fixed and per-env/bootstrap satisfied).
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.7_

  - [x] 3.3 Confirm `infrastructure/api_stack.py` needs no behavioral change
    - Verify the stack keeps mapping its `knowledge_base_id` constructor argument to `"BEDROCK_KB_ID": knowledge_base_id` unchanged — the real value now flows through because `app.py` supplies it.
    - Confirm no edits to other env vars, IAM statements, bundling, or API Gateway config.
    - Rely on the literal-not-token assertion added in task 3.2 to prove the mapping carries a concrete value.
    - _Bug_Condition: isBugCondition(X) — driven by app.py, not api_stack.py_
    - _Expected_Behavior: BEDROCK_KB_ID = knowledge_base_id passes the resolved real value through unchanged_
    - _Preservation: api_stack.py behavior identical to F (Req 3.3, 3.6)_
    - _Requirements: 2.2, 3.3, 3.6_

  - [x] 3.4 Update `infrastructure/rag_stack.py` operator guidance
    - Change the `NextStep` CfnOutput text to describe the SSM mechanism: create the KB (console or `create_kb.sh`), store the ID in SSM at `/teaching-agent/{env}/bedrock-kb-id`, then `cdk deploy TeachingAgentAPI` — instead of instructing a manual `BEDROCK_KB_ID` set.
    - Optionally add a second `CfnOutput` naming the exact SSM parameter path for discoverability.
    - Leave the S3 bucket definition and `self.knowledge_base_id = ""` unchanged (bucket preservation, Req 3.4). Do NOT add any KB/AOSS resources.
    - _Bug_Condition: documentation reinforced the out-of-band manual flow_
    - _Expected_Behavior: operator guidance points at the durable SSM source of truth_
    - _Preservation: S3 bucket and knowledge_base_id="" line unchanged (Req 3.4)_
    - _Requirements: 2.6, 3.4_

  - [x] 3.5 Update helper scripts `scripts/create_kb.sh` and `scripts/upload_to_s3.sh`
    - In `create_kb.sh`, replace the final `export BEDROCK_KB_ID=$KB_ID` guidance with `aws ssm put-parameter --name "/teaching-agent/${ENV:-dev}/bedrock-kb-id" --type String --value "$KB_ID" --overwrite --region eu-west-2`, followed by "then run `cdk deploy TeachingAgentAPI`".
    - In `upload_to_s3.sh`, update the trailing "Next steps" echo so the final step points to storing the KB ID in the SSM parameter and redeploying via CDK (no functional upload logic change).
    - _Bug_Condition: scripts institutionalized the manual env-var set_
    - _Expected_Behavior: KB creation feeds the durable SSM source of truth automatically_
    - _Preservation: no functional upload/KB-creation logic changes_
    - _Requirements: 2.6_

  - [x] 3.6 Update operator documentation (README / deployment docs)
    - Document the SSM parameter convention and per-environment naming `/teaching-agent/{env}/bedrock-kb-id`.
    - Document the seed command (`aws ssm put-parameter ...`), the bootstrap first-deploy flow (absent param → `""` → RAG degrades gracefully), and the drift guarantee (`value_from_lookup` stamps a literal → `detect-stack-drift` reports `IN_SYNC`).
    - _Bug_Condition: docs described the manual, drift-prone flow_
    - _Expected_Behavior: docs describe the durable SSM mechanism, bootstrap, and drift guarantee_
    - _Requirements: 2.6_

  - [x] 3.7 Verify preservation tests still pass
    - **Property 2: Preservation** - Non-KB-ID Stack Behavior Unchanged
    - **IMPORTANT**: Re-run the SAME tests from task 2 — do NOT write new tests.
    - Confirm the six other API Lambda env vars, the API Lambda IAM policies, the `TeachingAgentRAG` S3 bucket, and the `TeachingAgentAuth`/`TeachingAgentGuardrails`/`TeachingAgentTracking` templates are byte-for-byte equal to the baseline, except the `BEDROCK_KB_ID` value and the `rag_stack.py` `NextStep` output text.
    - Confirm `backend/rag/knowledge_base.py` is still unmodified (hash/baseline matches).
    - **EXPECTED OUTCOME**: Tests PASS (confirms no regressions).
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6_

- [x] 4. Checkpoint - Ensure all automated tests pass
  - Run the full suite (`pytest tests/test_kb_id_config.py -v` plus the existing suite) and confirm Property 1 fix-checking and Property 2 preservation tests all pass.
  - Ensure no regressions in existing tests. Ask the user if questions arise.
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.7, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6_

- [~] 5. Manual AWS verification (NOT auto-runnable — requires live AWS)
  - **MANUAL EXECUTION REQUIRED** against AWS: profile `kiro-demo`, account `062788795053`, region `eu-west-2`. This task cannot be run by the automated test suite.
  - Seed the parameter: `aws ssm put-parameter --name "/teaching-agent/dev/bedrock-kb-id" --type String --value "JUZEF2UAU0" --overwrite --region eu-west-2 --profile kiro-demo`.
  - Run `cdk diff TeachingAgentAPI` and confirm `BEDROCK_KB_ID` shows the real KB ID `JUZEF2UAU0` (a literal, not a `{{resolve:ssm:...}}` token).
  - Run `cdk deploy TeachingAgentAPI --profile kiro-demo`.
  - Run `aws cloudformation detect-stack-drift --stack-name TeachingAgentAPI --region eu-west-2 --profile kiro-demo` and confirm the resulting drift status is `IN_SYNC` (Property 1 drift elimination, Req 2.3).
  - Optionally confirm a RAG endpoint returns a successful retrieval against the real KB.
  - _Requirements: 2.1, 2.2, 2.3_
