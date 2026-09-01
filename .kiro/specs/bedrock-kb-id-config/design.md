# BEDROCK_KB_ID Configuration Drift Bugfix Design

## Overview

The `teaching-agent-api` Lambda in the `TeachingAgentAPI` stack receives its Bedrock Knowledge Base ID through the `BEDROCK_KB_ID` environment variable. The CDK source hardwires this value to the literal `PLACEHOLDER_SET_AFTER_KB_CREATION` (in `infrastructure/app.py`), while the live Lambda was manually patched out-of-band to the real, ACTIVE KB ID `JUZEF2UAU0`. The deployed value and the CDK template therefore disagree — this is CloudFormation configuration drift. Any `cdk deploy TeachingAgentAPI` reverts the Lambda back to the placeholder, silently breaking RAG retrieval until an operator re-patches the variable by hand.

The fix replaces the hardcoded placeholder with a durable, version-controlled, per-environment source of truth for the KB ID, so that the value CDK delivers always equals the active KB ID and the template matches the deployed resource (drift eliminated). The bug is fixed for the placeholder/mismatch condition while all other stack behavior — every other env var, IAM policy, the S3 bucket, and the four sibling stacks — is preserved unchanged.

After evaluating the three candidate mechanisms from the requirements (SSM Parameter Store, CDK context/`cdk.json`, and defining the KB in CDK), this design **recommends SSM Parameter Store read at deploy time via `StringParameter.value_from_lookup`**, with graceful bootstrap handling. The rationale and rejected-alternative tradeoffs are documented below.

## Glossary

- **Bug_Condition (C)**: The condition that triggers the bug — the `BEDROCK_KB_ID` value CDK delivers to the API Lambda is the placeholder (`PLACEHOLDER_SET_AFTER_KB_CREATION`) or otherwise not equal to the active KB ID.
- **Property (P)**: The desired behavior — CDK delivers the real, active KB ID from a durable version-controlled/configured source, producing no drift and no hardcoded secret, configurable per environment.
- **Preservation**: All stack behavior other than KB ID delivery must remain unchanged — other Lambda env vars, IAM policies, the S3 materials bucket, and the `TeachingAgentAuth`, `TeachingAgentGuardrails`, `TeachingAgentTracking` stacks.
- **`app.py` wiring**: `infrastructure/app.py` instantiates `TeachingAgentAPIStack(..., knowledge_base_id="PLACEHOLDER_SET_AFTER_KB_CREATION", ...)`. This is where the placeholder originates.
- **`api_stack.py` mapping**: `TeachingAgentAPIStack.__init__` maps the `knowledge_base_id` constructor argument directly into the Lambda `environment` dict as `"BEDROCK_KB_ID": knowledge_base_id`.
- **`rag_stack.py`**: `TeachingAgentRAGStack` creates only the S3 materials bucket, sets `self.knowledge_base_id = ""`, and emits a `NextStep` CfnOutput telling operators to create the KB in the console and set `BEDROCK_KB_ID` manually.
- **Runtime resolver**: `backend/rag/knowledge_base.py` resolves `KNOWLEDGE_BASE_ID` from `os.environ["BEDROCK_KB_ID"]` with fallback to `BEDROCK_KNOWLEDGE_BASE_ID`, and logs `knowledge_base_id_not_configured` + returns a safe empty/error result when unset.
- **activeKbId**: The ID of the live, ACTIVE Bedrock Knowledge Base (currently `JUZEF2UAU0`). `NONE` denotes the bootstrap case where no KB exists yet.
- **F / F'**: The original (unfixed) CDK source / the fixed CDK source.
- **SSM parameter**: An AWS Systems Manager Parameter Store `String` parameter holding the KB ID, keyed per environment.
- **`value_from_lookup`**: `ssm.StringParameter.value_from_lookup(scope, name)` — resolves the parameter value at **synth time** via a context lookup (cached in `cdk.context.json`), embedding the resolved literal into the synthesized template.
- **`from_string_parameter_attributes(...).string_value`**: resolves to a **CloudFormation dynamic-reference token** (`{{resolve:ssm:...}}`) at **deploy time**; the resolved value is not visible in `cdk diff` and, for Lambda env vars, does not stamp a literal into the template.

## Bug Details

### Bug Condition

The bug manifests whenever the `BEDROCK_KB_ID` value that CDK stamps into the API Lambda's environment is the hardcoded placeholder rather than the real active KB ID. Because the value is a compile-time constant in `app.py`, every deploy re-delivers the placeholder, overwriting any manually-set correct value on the live Lambda. The root defect is that the source of truth for the KB ID lives only in the deployed stack (out-of-band), not in the CDK source.

**Formal Specification:**
```
FUNCTION isBugCondition(X)
  INPUT: X of type DeploymentConfig   // the BEDROCK_KB_ID value delivered to the API Lambda by CDK
  OUTPUT: boolean

  RETURN X.deliveredKbId = "PLACEHOLDER_SET_AFTER_KB_CREATION"
         OR X.deliveredKbId <> X.activeKbId
END FUNCTION
```

### Examples

- **Redeploy reverts working value**: KB `JUZEF2UAU0` is set manually on the Lambda; running `cdk deploy TeachingAgentAPI` (F) delivers `BEDROCK_KB_ID = "PLACEHOLDER_SET_AFTER_KB_CREATION"`. Expected: the active KB ID is preserved. Actual: reverted to placeholder → `isBugCondition` true → RAG breaks.
- **Runtime failure on placeholder**: with `BEDROCK_KB_ID = "PLACEHOLDER_SET_AFTER_KB_CREATION"`, `retrieve()` / `retrieve_and_generate()` call Bedrock against a non-existent KB. Expected: successful retrieval. Actual: `ResourceNotFoundException`/`ValidationException`, safe error response returned to student.
- **No version-controlled record**: an operator inspecting `app.py` to find the KB ID sees only the placeholder. Expected: the real ID (or its configured source) is discoverable in version control. Actual: only the placeholder is recorded.
- **Drift detection**: `aws cloudformation detect-stack-drift --stack-name TeachingAgentAPI` on the manually-patched stack reports `MODIFIED` / `DRIFTED` for the Lambda env var. Expected: `IN_SYNC`.
- **Bootstrap edge case (`activeKbId = NONE`)**: first deploy before any KB exists. Expected: synth and deploy succeed with RAG gracefully unavailable. This case must not fail — see Bootstrap handling.

## Expected Behavior

### Preservation Requirements

**Unchanged Behaviors:**
- RAG retrieval (`Retrieve` / `RetrieveAndGenerate`) must continue to work exactly as today when a valid KB ID is configured (Req 3.1).
- The runtime KB ID resolution precedence (`BEDROCK_KB_ID` then fallback to `BEDROCK_KNOWLEDGE_BASE_ID`) and its graceful fallback (log `knowledge_base_id_not_configured`, return safe/empty result) must remain unchanged (Req 3.2).
- All other API Lambda environment variables must be set unchanged: `COGNITO_USER_POOL_ID`, `COGNITO_REGION`, `BEDROCK_GUARDRAIL_ID`, `BEDROCK_GUARDRAIL_VERSION`, `TRACKING_TABLE_NAME`, `TUTORIAL_DIR` (Req 3.3).
- The `TeachingAgentRAG` stack must continue to create and retain the `teaching-agent-materials-062788795053` S3 bucket with existing versioning, S3-managed encryption, SSL enforcement, and RETAIN removal policy (Req 3.4).
- `TeachingAgentAuth`, `TeachingAgentGuardrails`, `TeachingAgentTracking` and their cross-stack references (user pool, guardrail ID, tracking table) must remain unchanged (Req 3.5).
- The API Lambda's IAM policies — Bedrock (`InvokeModel`, `Converse`, `Retrieve`, `RetrieveAndGenerate`, `ApplyGuardrail`), DynamoDB read/write, and Cognito admin — must remain unchanged (Req 3.6).

**Scope:**
All deployments where the delivered KB ID already equals the active KB ID (`NOT isBugCondition`) must behave identically before and after the fix. The change is confined to how a single value (`BEDROCK_KB_ID`) is sourced. This explicitly does NOT touch:
- Any other environment variable on the API Lambda.
- Any IAM policy statement, resource, or grant.
- The S3 materials bucket configuration.
- The runtime resolver logic in `backend/rag/knowledge_base.py` (it keeps reading `BEDROCK_KB_ID`).
- The four sibling stacks.

**Note:** The expected correct behavior is defined in the Correctness Properties section (Property 1). This section focuses on what must NOT change.

## Hypothesized Root Cause

Based on the bug description and verified source, the root cause is a single design decision with several manifestations:

1. **Hardcoded compile-time placeholder (primary)**: `infrastructure/app.py` passes `knowledge_base_id="PLACEHOLDER_SET_AFTER_KB_CREATION"` as a literal. There is no external source of truth, so CDK cannot know the real KB ID and stamps the placeholder into the template on every synth/deploy.

2. **Out-of-band source of truth**: The real KB ID lives only on the deployed Lambda (set manually). CloudFormation considers the template authoritative, so the manual value is drift and is overwritten on the next deploy.

3. **Intentional deferral in `rag_stack.py`**: `TeachingAgentRAGStack` deliberately does not create the KB and sets `self.knowledge_base_id = ""`. Its `NextStep` output instructs operators to create the KB in the console and set the env var manually — institutionalizing the out-of-band, drift-prone flow.

4. **Documentation reinforces the manual flow**: `scripts/create_kb.sh` and `scripts/upload_to_s3.sh` both `echo` instructions to "set `BEDROCK_KB_ID`" by hand, so the manual step is treated as expected rather than as a defect.

The runtime resolver in `backend/rag/knowledge_base.py` is **not** a root cause — it already behaves correctly (reads the env var, honors fallback precedence, degrades gracefully). The fix is entirely in how CDK sources and delivers the value.

## Mechanism Evaluation and Recommendation

The requirements deferred the mechanism choice (2.A / 2.B / 2.C) to design. Evaluation criteria drawn from project AWS/CDK conventions: CDK v2 Python, L2 constructs preferred, per-environment dev/prod, region eu-west-2, all resources deployed via CDK, no secrets in source, minimal blast radius, drift elimination, and safe bootstrap.

### Option 1 — SSM Parameter Store (RECOMMENDED)

The KB ID is stored once in an SSM `String` parameter (per environment, e.g. `/teaching-agent/dev/bedrock-kb-id`) — written out-of-band or by the `create_kb.sh` script after KB creation. CDK reads it at synth/deploy time and stamps it into the Lambda env var.

Two SSM read modes behave very differently for drift, and the choice matters:

- **`StringParameter.value_from_lookup(self, name)` (synth-time lookup) — chosen.** Resolves the parameter's current value during `cdk synth` via a context lookup, caches it in `cdk.context.json`, and embeds the **resolved literal** KB ID directly into the synthesized CloudFormation template. Consequences:
  - `cdk diff` shows the real KB ID (`JUZEF2UAU0`) as a concrete string — reviewable in version control via `cdk.context.json`.
  - The deployed Lambda env var value equals the template value → **`detect-stack-drift` reports `IN_SYNC`** (no dynamic-reference token that CloudFormation could consider divergent).
  - To pick up a rotated KB ID, run `cdk synth`/`deploy` after clearing the cached context (`cdk context --reset` or delete the key), which is an explicit, version-controllable action.

- **`from_string_parameter_attributes(...).string_value` (deploy-time token) — considered, not chosen for this env var.** Produces a CloudFormation dynamic reference (`{{resolve:ssm:/name}}`). The template stores the token, not the value; CloudFormation resolves it at deploy. Consequences:
  - `cdk diff` shows the token, not the real KB ID — the actual value is invisible in review.
  - The deployed literal (resolved value) differs from the token stored in the template, which can cause **drift detection to report the env var as modified** and makes the "template matches deployed value" guarantee weaker. This directly undercuts requirement 2.3 (no drift), so it is rejected in favor of `value_from_lookup`.

**Pros:** L2/first-class CDK support; per-environment via parameter naming; no secret in source (the ID lives in SSM + reviewable `cdk.context.json`); drift eliminated with `value_from_lookup`; tiny blast radius (one value changes); consistent with "all config via AWS"; graceful bootstrap achievable with a default when the parameter is absent.
**Cons:** requires the parameter to be seeded once (a documented, scriptable step); `value_from_lookup` caches in `cdk.context.json`, so rotating the KB ID requires a context refresh (acceptable and explicit).

### Option 2 — CDK context / `cdk.json` (not chosen)

Supply the KB ID via `--context kbId=...` or persist it in `cdk.json` context; read it during synth with `self.node.try_get_context("kbId")`.

**Pros:** simplest possible change; fully version-controlled if written into `cdk.json`; per-environment via distinct context keys; drift-free (value is a synth-time literal).
**Cons:** puts an environment-specific runtime identifier into repo config, which mixes deploy-time infra config with a resource ID that changes when the KB is recreated; less aligned with treating AWS as the source of truth; `--context` on the CLI is easy to forget and not durable unless persisted. It is a viable fallback but is less clean than SSM for a value that is fundamentally an AWS resource identifier that operators may rotate.

### Option 3 — Define the KB in CDK (not chosen)

Create the Bedrock Knowledge Base (`CfnKnowledgeBase`) + OpenSearch Serverless collection + data source in `TeachingAgentRAG`, then pass the generated `knowledge_base_id` to `TeachingAgentAPI` via a cross-stack reference — eliminating the manual console step entirely.

**Pros:** the "correct" long-term IaC posture; zero manual step; KB ID is a native cross-stack reference, inherently drift-free and always correct; fully per-environment.
**Cons:** **significant added complexity** disproportionate to a config-drift bugfix. It requires:
  - An AOSS (OpenSearch Serverless) collection plus **encryption, network, and data-access policies** (the data-access policy must grant both the KB service role and any admin principals).
  - **Vector index creation** in AOSS, which CDK cannot do natively — it needs a custom resource / Lambda (or the `bedrock` L2 alpha construct `@aws-cdk/aws-bedrock-alpha`, which is experimental) to create the index before the KB, introducing ordering and retry fragility.
  - An **embeddings model** choice wired in (`amazon.titan-embed-text-v2:0`) and a KB execution IAM role with S3 + AOSS + Bedrock permissions.
  - Data-source + ingestion wiring.
  This is a multi-week infra effort with real operational risk (AOSS index timing is a well-known source of deploy failures). For a course-companion project where the KB is created once and rarely changes, this complexity is **not warranted** for the current bug. It should be recorded as a future enhancement, not the fix.

### Decision

**Recommend Option 1 (SSM Parameter Store via `value_from_lookup`).** It satisfies every acceptance criterion (durable, version-controlled/reviewable via `cdk.context.json`, per-environment, no hardcoded secret, drift-free, safe bootstrap) with a minimal, low-risk change, and aligns with project conventions of managing configuration in AWS and deploying everything via CDK. Option 3 is deferred as a future enhancement; Option 2 is the fallback if SSM is undesirable.

## Correctness Properties

Property 1: Bug Condition - KB ID Is Durable and Correct After Deploy

_For any_ deployment config where the bug condition holds (`isBugCondition` returns true — the delivered KB ID is the placeholder or not equal to the active KB ID), the fixed CDK (`F'`) SHALL deliver `BEDROCK_KB_ID` equal to the active KB ID from the SSM parameter, SHALL leave no CloudFormation drift between template and live Lambda, SHALL NOT hardcode any secret in source, and SHALL keep the value configurable per environment (dev/prod). In the bootstrap sub-case where no KB exists yet (`activeKbId = NONE`), `F'` SHALL still synthesize and deploy successfully with RAG gracefully unavailable.

**Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.5, 2.7**

Property 2: Preservation - Non-Buggy Configs and All Other Stack Behavior Unchanged

_For any_ deployment config where the bug condition does NOT hold (`isBugCondition` returns false — the delivered KB ID already equals the active KB ID), the fixed CDK (`F'`) SHALL produce the same deployment result as the original CDK (`F`), preserving all other API Lambda environment variables, all IAM policies, the S3 materials bucket configuration, the runtime resolver precedence/fallback, and the four sibling stacks (`TeachingAgentAuth`, `TeachingAgentGuardrails`, `TeachingAgentTracking`, and the `TeachingAgentRAG` bucket).

**Validates: Requirements 3.1, 3.2, 3.3, 3.4, 3.5, 3.6**

## Fix Implementation

### Changes Required

Assuming the root cause analysis is correct, the fix sources `BEDROCK_KB_ID` from an SSM parameter resolved at synth time and flows it to the Lambda env var, with a graceful bootstrap default. No runtime code changes.

**File**: `infrastructure/app.py`

**Change**: Stop passing the hardcoded placeholder. Resolve the KB ID from SSM at synth time and pass the resolved value (or a safe default) into `TeachingAgentAPIStack`.
1. Introduce a per-environment SSM parameter name, derived from a deploy-time environment selector (e.g. context key `env` defaulting to `dev`): `/teaching-agent/{env}/bedrock-kb-id`.
2. Resolve the value with `ssm.StringParameter.value_from_lookup(app, param_name)`.
3. Handle bootstrap: `value_from_lookup` returns a dummy sentinel (e.g. `dummy-value-for-...`) when the parameter does not yet exist during the first synth. Detect that sentinel (or wrap the lookup) and substitute a safe default (empty string `""`, which the runtime treats as "not configured") so synth/deploy still succeed. Pass the resolved KB ID into `TeachingAgentAPIStack(..., knowledge_base_id=resolved_kb_id, ...)`.
4. Keep the `env` selector so the same app deploys to dev/prod with different parameter values (Req 2.4).

**File**: `infrastructure/api_stack.py`

**Change**: **No behavioral change required.** The stack keeps mapping its `knowledge_base_id` constructor argument to `"BEDROCK_KB_ID": knowledge_base_id`. Because `app.py` now supplies a real resolved value instead of the placeholder, the correct KB ID flows through unchanged. All other env vars, IAM statements, bundling, and API Gateway config are untouched (satisfies Preservation Req 3.3, 3.6). Optionally, accept an empty string gracefully (already handled downstream by the runtime resolver).

**File**: `infrastructure/rag_stack.py`

**Change**: Update the operator-facing guidance to describe the SSM mechanism instead of the manual env-var set (Req 2.6). Specifically, change the `NextStep` CfnOutput text to instruct: create the KB (console or `create_kb.sh`), then store the ID in SSM at `/teaching-agent/{env}/bedrock-kb-id`, then `cdk deploy TeachingAgentAPI`. The S3 bucket definition and `self.knowledge_base_id = ""` line are left unchanged (bucket preservation Req 3.4). Optionally add a second `CfnOutput` naming the exact SSM parameter path for discoverability. No KB/AOSS resources are added (Option 3 is out of scope).

**File**: `scripts/create_kb.sh`

**Change**: Replace the final `export BEDROCK_KB_ID=$KB_ID` guidance with a command that writes the ID to SSM per environment, e.g. `aws ssm put-parameter --name "/teaching-agent/${ENV:-dev}/bedrock-kb-id" --type String --value "$KB_ID" --overwrite --region eu-west-2`, followed by "then run `cdk deploy TeachingAgentAPI`". This makes KB creation feed the durable source of truth automatically (Req 2.6).

**File**: `scripts/upload_to_s3.sh`

**Change**: Update the trailing "Next steps" echo so the final step points to storing the KB ID in the SSM parameter (not a manual env-var set) and redeploying via CDK (Req 2.6). No functional upload logic changes.

**File**: operator documentation (e.g. `README` / deployment docs)

**Change**: Document the SSM parameter convention, the per-environment naming, the seed command, the bootstrap-first-deploy flow, and the drift guarantee (Req 2.6).

### KB ID Flow (after fix)

```
SSM parameter /teaching-agent/{env}/bedrock-kb-id  (source of truth, seeded once)
        │  value_from_lookup at synth time (cached in cdk.context.json)
        ▼
app.py: resolved_kb_id  (real ID, or "" on bootstrap)
        │  constructor arg knowledge_base_id=resolved_kb_id
        ▼
api_stack.py: environment["BEDROCK_KB_ID"] = knowledge_base_id
        │  stamped as literal into TeachingAgentAPI template
        ▼
teaching-agent-api Lambda env var BEDROCK_KB_ID
        │  os.environ["BEDROCK_KB_ID"] (fallback BEDROCK_KNOWLEDGE_BASE_ID)
        ▼
backend/rag/knowledge_base.py: KNOWLEDGE_BASE_ID  → Retrieve / RetrieveAndGenerate
```

### Bootstrap Handling (first deploy before KB exists)

Requirement 2.7: the first deploy, before any KB exists, must not fail synth or deploy and must degrade gracefully.
- When the SSM parameter is absent, `value_from_lookup` yields a dummy sentinel during synth. `app.py` detects the sentinel and substitutes `""` for `knowledge_base_id`.
- `api_stack.py` then sets `BEDROCK_KB_ID = ""`, which is a valid template value — synth and deploy succeed.
- At runtime, `backend/rag/knowledge_base.py` sees an empty `KNOWLEDGE_BASE_ID`, logs `knowledge_base_id_not_configured`, and returns a safe error/empty result. RAG is unavailable but the API and infrastructure are fully deployed.
- After the KB is created and its ID seeded into SSM, a normal `cdk deploy` (with context refreshed) stamps the real ID and RAG comes online — no manual Lambda patching.

### Drift Elimination

- With `value_from_lookup`, the resolved KB ID is embedded as a **literal** in the `TeachingAgentAPI` template. The deployed Lambda env var equals that literal, so `aws cloudformation detect-stack-drift` reports the resource `IN_SYNC`.
- Because the source of truth is now SSM + the version-controlled `cdk.context.json`, there is no longer a working value that lives only on the deployed resource. The next `cdk deploy` re-delivers the same correct value instead of reverting to a placeholder, permanently closing the drift loop.

## Testing Strategy

### Validation Approach

Two-phase approach: first surface counterexamples that demonstrate the drift/placeholder bug on the unfixed CDK, then verify the fix delivers the real KB ID, eliminates drift, and preserves all other behavior. Testing here is primarily infrastructure synthesis assertions (CDK assertions / template snapshots) plus manual deploy-and-detect-drift verification, since the defect is in synthesized configuration rather than runtime logic.

### Exploratory Bug Condition Checking

**Goal**: Surface counterexamples that demonstrate the bug BEFORE implementing the fix, and confirm/refute the root-cause hypothesis (hardcoded placeholder in `app.py`). If refuted, re-hypothesize.

**Test Plan**: Synthesize `TeachingAgentAPI` from the current (unfixed) source and inspect the `AWS::Lambda::Function` `Environment.Variables.BEDROCK_KB_ID`. Also inspect the live stack for drift. Run against UNFIXED code to observe the placeholder and the drift.

**Test Cases**:
1. **Synth-shows-placeholder**: `cdk synth TeachingAgentAPI` → assert `BEDROCK_KB_ID == "PLACEHOLDER_SET_AFTER_KB_CREATION"` (confirms bug on unfixed code).
2. **Live-drift**: `aws cloudformation detect-stack-drift --stack-name TeachingAgentAPI` on the manually-patched stack → assert the env var is reported `MODIFIED`/stack `DRIFTED` (will show drift on unfixed code).
3. **Redeploy-reverts**: simulate/deploy and confirm the Lambda env var returns to the placeholder (demonstrates the revert).
4. **Bootstrap edge case**: with no SSM parameter present, confirm current source still synths (baseline for comparison after fix).

**Expected Counterexamples**:
- Synthesized `BEDROCK_KB_ID` is the placeholder, not `JUZEF2UAU0`.
- Drift detection flags the env var as modified.
- Root cause confirmed: hardcoded literal in `app.py`.

### Fix Checking

**Goal**: Verify that for all inputs where the bug condition holds, the fixed CDK delivers the active KB ID with no drift, no hardcoded secret, and per-environment configurability.

**Pseudocode:**
```
FOR ALL X WHERE isBugCondition(X) DO
  result := deployApiStack'(X)             // F' = fixed CDK
  ASSERT result.deliveredKbId = X.activeKbId
  ASSERT drift(result) = FALSE
  ASSERT NOT hardcodedSecret(result)
  ASSERT configurablePerEnvironment(result) = TRUE
END FOR

FOR ALL X WHERE isBugCondition(X) AND X.activeKbId = NONE DO
  ASSERT synthAndDeploy'(X) SUCCEEDS
END FOR
```

**Test Cases**:
1. **Synth-uses-SSM-value**: seed SSM param to `JUZEF2UAU0`, `cdk synth TeachingAgentAPI` → assert `BEDROCK_KB_ID == "JUZEF2UAU0"` (no placeholder).
2. **Diff-shows-real-id**: `cdk diff TeachingAgentAPI` → assert the real KB ID appears (not a token, not the placeholder).
3. **No-drift-after-deploy**: deploy, then `detect-stack-drift` → assert `IN_SYNC` on the Lambda env var.
4. **Per-environment**: synth with `env=dev` vs `env=prod` reading different SSM params → assert each stamps its respective KB ID.
5. **Bootstrap-success**: with SSM param absent, `cdk synth`/`deploy` → assert success and `BEDROCK_KB_ID == ""`.

### Preservation Checking

**Goal**: Verify that for all inputs where the bug condition does NOT hold, the fixed CDK produces the same deployment result as the original.

**Pseudocode:**
```
FOR ALL X WHERE NOT isBugCondition(X) DO
  ASSERT deployApiStack(X) = deployApiStack'(X)       // F(X) = F'(X)
END FOR
```

**Testing Approach**: Property-based / snapshot testing over the synthesized templates is well suited here: generate/compare the full `TeachingAgentAPI` template (minus the single `BEDROCK_KB_ID` value) and the sibling stacks' templates before and after the fix, asserting byte-for-byte equality of everything except the KB ID. This catches any unintended change across the large template surface.

**Test Plan**: Synthesize F and F' with the SSM value already equal to the active KB ID (so `NOT isBugCondition`), then diff the templates.

**Test Cases**:
1. **Other-env-vars-unchanged**: assert `COGNITO_USER_POOL_ID`, `COGNITO_REGION`, `BEDROCK_GUARDRAIL_ID`, `BEDROCK_GUARDRAIL_VERSION`, `TRACKING_TABLE_NAME`, `TUTORIAL_DIR` are identical between F and F' (Req 3.3).
2. **IAM-policies-unchanged**: assert the Bedrock, DynamoDB, and Cognito policy statements are identical (Req 3.6).
3. **S3-bucket-unchanged**: assert the `TeachingAgentRAG` bucket (name, versioning, encryption, SSL, RETAIN) is identical apart from the `NextStep` output text (Req 3.4).
4. **Sibling-stacks-unchanged**: snapshot-compare `TeachingAgentAuth`, `TeachingAgentGuardrails`, `TeachingAgentTracking` templates → assert unchanged (Req 3.5).
5. **Runtime-resolver-unchanged**: assert `backend/rag/knowledge_base.py` is not modified (precedence + graceful fallback preserved, Req 3.1, 3.2).

### Unit Tests

- CDK assertion test: `app.py` passes the SSM-resolved value (mock/seed the context lookup) into `TeachingAgentAPIStack`; assert the Lambda env var equals the seeded ID.
- CDK assertion test: bootstrap path substitutes `""` when the SSM lookup returns the dummy sentinel.
- Template assertion: `BEDROCK_KB_ID` is a literal string in the synthesized template (not a `{{resolve:ssm:...}}` dynamic reference), guaranteeing drift-free behavior.

### Property-Based Tests

- Generate random KB IDs, seed them into the (mocked) SSM lookup, synth, and assert the Lambda env var always equals the generated ID (Property 1 — fix checking across the input domain).
- Generate synthesized-template pairs (F vs F') for `NOT isBugCondition` inputs and assert equality of all fields except `BEDROCK_KB_ID` (Property 2 — preservation across many configs).

### Integration Tests

- End-to-end: seed SSM → `cdk deploy TeachingAgentAPI` → invoke a RAG endpoint → assert successful retrieval against the real KB.
- Drift lifecycle: deploy → `detect-stack-drift` returns `IN_SYNC`; then redeploy and confirm the value is not reverted.
- Bootstrap lifecycle: with no SSM param, deploy the full app → assert all stacks deploy, RAG endpoint returns the graceful "knowledge base not configured" response and logs `knowledge_base_id_not_configured`; then seed SSM, redeploy, and confirm RAG comes online with no manual Lambda edit.
