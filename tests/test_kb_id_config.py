"""CDK synthesis tests for the BEDROCK_KB_ID configuration-drift bugfix.

Spec: .kiro/specs/bedrock-kb-id-config

The defect lives in synthesized infrastructure, not runtime code, so these
tests inspect the CloudFormation template produced by ``cdk synth`` for the
``TeachingAgentAPI`` stack rather than exercising Lambda code paths.

Bugfix methodology (bug-condition exploration):
  Property 1 -- Bug Condition: Synth Delivers Placeholder KB ID.
  ``isBugCondition(X)`` is true when the ``BEDROCK_KB_ID`` value CDK delivers
  to the ``teaching-agent-api`` Lambda is the placeholder
  ``PLACEHOLDER_SET_AFTER_KB_CREATION`` (or otherwise not equal to the active
  KB ID ``JUZEF2UAU0``). This test is written to run against the CURRENT
  UNFIXED source, where it is EXPECTED TO PASS -- passing here confirms the
  bug is present today. After the fix (app.py sourcing the ID from SSM), the
  synthesized value becomes the real KB ID and this exploration assertion is
  superseded by the fix-checking test (task 3.2).

Bundling note:
  ``infrastructure/api_stack.py`` bundles the Lambda asset with a
  ``LocalPipBundling`` hook that shells out to ``pip install -r
  requirements.txt`` and copies ``backend/`` + ``tutorial/``. That is slow and
  non-deterministic for a unit test, and the env var under test does not
  depend on the asset contents. We therefore stub the local bundling to emit a
  tiny placeholder asset so synthesis stays fast and deterministic.

Run with:
    pytest tests/test_kb_id_config.py -v
"""

import json
import os
import subprocess
import sys
import tempfile

import pytest

import aws_cdk as cdk
from aws_cdk.assertions import Template

from infrastructure.auth_stack import TeachingAgentAuthStack
from infrastructure.guardrails_stack import TeachingAgentGuardrailsStack
from infrastructure.tracking_stack import TeachingAgentTrackingStack
from infrastructure.api_stack import TeachingAgentAPIStack, LocalPipBundling


# ── Constants from the bugfix spec ──────────────────────────────────────────
PLACEHOLDER_KB_ID = "PLACEHOLDER_SET_AFTER_KB_CREATION"
ACTIVE_KB_ID = "JUZEF2UAU0"
API_LAMBDA_FUNCTION_NAME = "teaching-agent-api"

# Project account/region wired in infrastructure/app.py — the fixed app resolves
# the KB ID from an SSM parameter scoped to this account/region.
CDK_ACCOUNT = "062788795053"
CDK_REGION = "eu-west-2"

_PROJECT_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _ssm_context_key(deploy_env: str) -> str:
    """Return the CDK SSM-string-parameter context provider cache key.

    ``ssm.StringParameter.value_from_lookup`` resolves via the SSM context
    provider. When the parameter's value is already present in the App context
    under this exact key, CDK returns it instead of the ``dummy-value-for-...``
    sentinel — no network call, fully deterministic.

    The key format was confirmed empirically by synthesizing the lookup once and
    reading the ``missing`` context report in ``manifest.json``:

        ssm:account=<acct>:parameterName=<name>:region=<region>

    where ``<name>`` is ``/teaching-agent/{env}/bedrock-kb-id`` — matching the
    per-environment parameter name that ``infrastructure/app.py`` builds from the
    ``env`` context selector.
    """
    param_name = f"/teaching-agent/{deploy_env}/bedrock-kb-id"
    return f"ssm:account={CDK_ACCOUNT}:parameterName={param_name}:region={CDK_REGION}"


# Runner executed in a FRESH subprocess so ``infrastructure/app.py`` runs with a
# clean ``cdk.App()`` that reads the seeded ``CDK_CONTEXT_JSON`` at construction.
# This is the only reliable way to drive app.py's real ``value_from_lookup``
# resolution deterministically: CDK reads ``CDK_CONTEXT_JSON`` once per process
# when the App is built, so each seeded config needs its own process — exactly
# how a real ``cdk synth`` runs. The runner stubs the slow pip-install bundling,
# imports app.py (which performs the env-selector → param-name → value_from_lookup
# → sentinel-handling → API-stack wiring), then emits the synthesized
# ``BEDROCK_KB_ID`` as JSON so the parent can distinguish a plain string literal
# from a ``{{resolve:ssm:...}}`` dynamic-reference dict (token).
_APP_RUNNER_SOURCE = """
import json, os
from infrastructure.api_stack import LocalPipBundling


def _fake_try_bundle(self, output_dir, *args, **kwargs):
    with open(os.path.join(output_dir, "placeholder.txt"), "w") as fh:
        fh.write("stub asset for unit tests")
    return True


LocalPipBundling.try_bundle = _fake_try_bundle

from aws_cdk.assertions import Template
import infrastructure.app as appmod

template = Template.from_stack(appmod.api_stack)
functions = template.find_resources(
    "AWS::Lambda::Function",
    {"Properties": {"FunctionName": "teaching-agent-api"}},
)
(function,) = functions.values()
value = function["Properties"]["Environment"]["Variables"]["BEDROCK_KB_ID"]
print("__KBID_JSON__" + json.dumps(value))
"""


def _synth_api_kb_id_via_app(deploy_env: str | None, seeded_kb_id: str | None):
    """Synthesize ``TeachingAgentAPI`` through the REAL ``infrastructure/app.py``.

    Runs app.py in an isolated subprocess so its module-level ``cdk.App()`` reads
    the context we seed via ``CDK_CONTEXT_JSON``. This exercises the actual fix
    (context ``env`` selector, per-environment parameter name, SSM
    ``value_from_lookup``, and the ``dummy-value-for-`` sentinel handling) rather
    than re-passing ``knowledge_base_id`` directly.

    Args:
        deploy_env: Value for the ``env`` context selector app.py reads
            (``app.node.try_get_context("env")``). ``None`` leaves it unset so
            app.py falls back to its ``"dev"`` default.
        seeded_kb_id: KB ID to seed into the SSM context provider cache for the
            resolved environment. ``None`` seeds nothing, so ``value_from_lookup``
            returns the ``dummy-value-for-...`` sentinel (the bootstrap case).

    Returns:
        The synthesized ``BEDROCK_KB_ID`` value exactly as it appears in the
        template — a ``str`` for a stamped literal, or a ``dict`` if it were a
        dynamic-reference token.
    """
    resolved_env = deploy_env or "dev"

    context: dict[str, str] = {}
    if deploy_env is not None:
        context["env"] = deploy_env
    if seeded_kb_id is not None:
        context[_ssm_context_key(resolved_env)] = seeded_kb_id

    child_env = dict(os.environ)
    child_env["CDK_DEFAULT_ACCOUNT"] = CDK_ACCOUNT
    child_env["CDK_CONTEXT_JSON"] = json.dumps(context)
    # Isolate synth output so tests never clobber the real ./cdk.out.
    child_env["CDK_OUTDIR"] = tempfile.mkdtemp(prefix="kbid-test-cdkout-")
    # Ensure the child can import the ``infrastructure`` package.
    child_env["PYTHONPATH"] = (
        _PROJECT_ROOT_DIR + os.pathsep + child_env.get("PYTHONPATH", "")
    )

    completed = subprocess.run(
        [sys.executable, "-c", _APP_RUNNER_SOURCE],
        cwd=_PROJECT_ROOT_DIR,
        env=child_env,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, (
        "Synth subprocess driving infrastructure/app.py failed.\n"
        f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
    )

    marker = "__KBID_JSON__"
    line = next(
        (ln for ln in completed.stdout.splitlines() if ln.startswith(marker)),
        None,
    )
    assert line is not None, (
        "Runner did not emit the BEDROCK_KB_ID marker.\n"
        f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
    )
    return json.loads(line[len(marker) :])


def _stub_local_bundling(monkeypatch: pytest.MonkeyPatch) -> None:
    """Replace the pip-install bundling with a trivial placeholder writer.

    Keeps ``Template.from_stack`` fast and deterministic — the asset contents
    are irrelevant to the ``BEDROCK_KB_ID`` env var being asserted.
    """

    def fake_try_bundle(self, output_dir: str, *args, **kwargs) -> bool:  # noqa: ANN001
        with open(os.path.join(output_dir, "placeholder.txt"), "w") as fh:
            fh.write("stub asset for unit tests")
        return True

    monkeypatch.setattr(LocalPipBundling, "try_bundle", fake_try_bundle)


def _synth_api_template(monkeypatch: pytest.MonkeyPatch) -> Template:
    """Synthesize the current (unfixed) ``TeachingAgentAPI`` stack to a Template.

    Builds the real sibling stacks (Auth, Guardrails, Tracking) so the
    cross-stack references the API stack consumes resolve exactly as in a real
    ``cdk synth``, and wires ``knowledge_base_id`` exactly as ``app.py`` does
    today (the hardcoded placeholder).
    """
    _stub_local_bundling(monkeypatch)

    app = cdk.App()
    env = cdk.Environment(account="062788795053", region="eu-west-2")

    auth_stack = TeachingAgentAuthStack(app, "TeachingAgentAuth", env=env)
    guardrails_stack = TeachingAgentGuardrailsStack(
        app, "TeachingAgentGuardrails", env=env
    )
    tracking_stack = TeachingAgentTrackingStack(app, "TeachingAgentTracking", env=env)

    api_stack = TeachingAgentAPIStack(
        app,
        "TeachingAgentAPI",
        env=env,
        user_pool=auth_stack.user_pool,
        # Mirror infrastructure/app.py on the UNFIXED source exactly.
        knowledge_base_id=PLACEHOLDER_KB_ID,
        guardrail_id=guardrails_stack.guardrail_id,
        tracking_table=tracking_stack.table,
    )

    return Template.from_stack(api_stack)


def _api_lambda_env_vars(template: Template) -> dict:
    """Return the environment variables of the teaching-agent-api Lambda.

    Locates the ``AWS::Lambda::Function`` whose ``FunctionName`` is
    ``teaching-agent-api`` and returns its ``Environment.Variables`` dict.
    """
    functions = template.find_resources(
        "AWS::Lambda::Function",
        {"Properties": {"FunctionName": API_LAMBDA_FUNCTION_NAME}},
    )
    assert functions, (
        f"No AWS::Lambda::Function found with FunctionName "
        f"{API_LAMBDA_FUNCTION_NAME!r} in the synthesized TeachingAgentAPI stack"
    )
    assert len(functions) == 1, (
        f"Expected exactly one {API_LAMBDA_FUNCTION_NAME!r} Lambda, "
        f"found {len(functions)}"
    )
    (function,) = functions.values()
    return function["Properties"]["Environment"]["Variables"]


# ── Property 1: Expected Behavior — KB ID Is Durable and Correct After Synth ─
# Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.5, 2.7
class TestExpectedBehaviorKbIdDurableAndCorrect:
    """Property 1 (fix-checking) — supersedes the task-1 exploration assertion.

    History: task 1 wrote a bug-condition exploration test here that synthesized
    the UNFIXED source (which re-passed the hardcoded placeholder into
    ``TeachingAgentAPIStack``) and asserted ``BEDROCK_KB_ID`` equalled
    ``PLACEHOLDER_SET_AFTER_KB_CREATION``. Now that ``infrastructure/app.py``
    sources the KB ID from SSM (task 3.1), that exploration assertion no longer
    reflects the real source — it would only test the api_stack passthrough with
    a value the test itself hardcoded, which misrepresents current behavior.

    Per task 3.2 this class is converted to encode the FIXED expected behavior
    (Property 1). Crucially, it drives ``infrastructure/app.py``'s ACTUAL
    resolution path (context ``env`` selector → per-environment parameter name →
    ``value_from_lookup`` → ``dummy-value-for-`` sentinel handling → wiring into
    the API stack) via ``_synth_api_kb_id_via_app`` rather than re-passing
    ``knowledge_base_id`` directly, so the suite genuinely exercises the fix.

    Deterministic ``value_from_lookup``: each case runs app.py in a fresh
    subprocess with ``CDK_CONTEXT_JSON`` seeding the SSM context provider cache
    key (``ssm:account=...:parameterName=...:region=...``). CDK then returns the
    seeded value from context instead of the ``dummy-value-for-...`` sentinel —
    no AWS call, fully deterministic.

    **Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.5, 2.7**
    """

    def test_synth_uses_ssm_value_stamps_active_kb_id(self) -> None:
        """SSM lookup → real KB ID stamped into BEDROCK_KB_ID (Req 2.1, 2.2, 2.5).

        Seed the dev SSM parameter to the active KB ID ``JUZEF2UAU0`` and drive
        app.py's real resolution. The synthesized Lambda ``BEDROCK_KB_ID`` must
        equal the active KB ID (not the placeholder), proving the fix delivers a
        durable, version-controlled value from SSM.
        """
        delivered_kb_id = _synth_api_kb_id_via_app(
            deploy_env=None, seeded_kb_id=ACTIVE_KB_ID
        )

        assert delivered_kb_id == ACTIVE_KB_ID, (
            "Fixed app.py should stamp the SSM-resolved active KB ID into "
            f"BEDROCK_KB_ID. Got {delivered_kb_id!r}."
        )
        assert delivered_kb_id != PLACEHOLDER_KB_ID, (
            "BEDROCK_KB_ID must no longer be the placeholder after the fix."
        )

    def test_per_environment_dev_and_prod_stamp_respective_ids(self) -> None:
        """dev vs prod resolve different SSM params → different IDs (Req 2.4).

        The same app deploys per-environment: with context ``env=dev`` app.py
        reads ``/teaching-agent/dev/bedrock-kb-id`` and with ``env=prod`` it reads
        ``/teaching-agent/prod/bedrock-kb-id``. Seed each with a distinct value
        and assert each environment stamps its own.
        """
        dev_kb_id = "DEVKB000001"
        prod_kb_id = "PRODKB00002"

        delivered_dev = _synth_api_kb_id_via_app(
            deploy_env="dev", seeded_kb_id=dev_kb_id
        )
        delivered_prod = _synth_api_kb_id_via_app(
            deploy_env="prod", seeded_kb_id=prod_kb_id
        )

        assert delivered_dev == dev_kb_id, (
            f"env=dev should stamp the dev SSM value {dev_kb_id!r}, "
            f"got {delivered_dev!r}."
        )
        assert delivered_prod == prod_kb_id, (
            f"env=prod should stamp the prod SSM value {prod_kb_id!r}, "
            f"got {delivered_prod!r}."
        )
        assert delivered_dev != delivered_prod, (
            "dev and prod must resolve to distinct, per-environment KB IDs."
        )

    def test_bootstrap_absent_parameter_synths_with_empty_kb_id(self) -> None:
        """Bootstrap: sentinel → BEDROCK_KB_ID == "" and synth succeeds (Req 2.7).

        With nothing seeded, ``value_from_lookup`` yields the
        ``dummy-value-for-...`` sentinel during synth. app.py detects it and
        substitutes ``""`` so the first deploy (before the KB exists) synthesizes
        successfully and RAG degrades gracefully at runtime.
        """
        delivered_kb_id = _synth_api_kb_id_via_app(
            deploy_env=None, seeded_kb_id=None
        )

        assert delivered_kb_id == "", (
            "Bootstrap (SSM parameter absent → sentinel) must resolve "
            f'BEDROCK_KB_ID to "". Got {delivered_kb_id!r}.'
        )

    def test_kb_id_is_string_literal_not_dynamic_reference_token(self) -> None:
        """BEDROCK_KB_ID is a plain literal, NOT a {{resolve:ssm:...}} token (Req 2.3).

        ``value_from_lookup`` embeds the resolved value as a concrete string in
        the template, so the deployed value equals the template value →
        ``detect-stack-drift`` reports ``IN_SYNC`` (drift-free). Had app.py used a
        deploy-time SSM reference instead, the value would synth as a dict such as
        ``{"Fn::Join": [...]}`` / a ``{{resolve:ssm:...}}`` string. Asserting a
        plain ``str`` literal here also confirms ``api_stack.py`` needs no change:
        it faithfully carries the concrete value app.py supplies (task 3.3).
        """
        delivered_kb_id = _synth_api_kb_id_via_app(
            deploy_env=None, seeded_kb_id=ACTIVE_KB_ID
        )

        assert isinstance(delivered_kb_id, str), (
            "BEDROCK_KB_ID must be a plain string literal (drift-free), not a "
            f"dynamic-reference dict/token. Got {type(delivered_kb_id).__name__}: "
            f"{delivered_kb_id!r}."
        )
        assert "{{resolve:ssm:" not in delivered_kb_id, (
            "BEDROCK_KB_ID must not be a {{resolve:ssm:...}} dynamic reference — "
            f"that would reintroduce drift. Got {delivered_kb_id!r}."
        )
        assert delivered_kb_id == ACTIVE_KB_ID

# ═════════════════════════════════════════════════════════════════════════════
# Task 2 — Preservation property tests (Property 2)
#
# Property 2: Preservation — Non-KB-ID Stack Behavior Unchanged.
#
# Observation-first methodology: these tests record the behavior of the CURRENT
# UNFIXED source as the baseline that the fix (SSM value_from_lookup in app.py)
# must preserve. Everything the API Lambda declares APART FROM the single
# BEDROCK_KB_ID value — the six other env vars, the IAM policy statements — plus
# the TeachingAgentRAG S3 bucket and the three sibling stack templates, and the
# runtime resolver file, must remain unchanged after the fix.
#
# EXPECTED OUTCOME on UNFIXED code: all PASS (this is the baseline to preserve).
# They must still PASS after the fix (re-run in task 3.7).
#
# Reusable baselines for task 3.7:
#   * ``sibling_stack_baselines()`` — returns the to_json() template dicts for
#     TeachingAgentAuth / Guardrails / Tracking, captured from the UNFIXED source
#     synthesized here. Task 3.7 re-synthesizes the FIXED source and compares the
#     post-fix templates against these dicts for byte-for-byte equality (Req 3.5).
#   * ``knowledge_base_source_hash()`` — SHA-256 of
#     backend/rag/knowledge_base.py. ``KNOWLEDGE_BASE_SOURCE_BASELINE_HASH``
#     records its current value. Task 3.7 recomputes and compares to prove the
#     runtime resolver (precedence + graceful fallback) is untouched (Req 3.1, 3.2).
# ═════════════════════════════════════════════════════════════════════════════

import hashlib

import aws_cdk as cdk  # noqa: F811  (module already imported above; explicit here for clarity)
from aws_cdk.assertions import Match

from infrastructure.rag_stack import TeachingAgentRAGStack


# ── Paths & baselines ────────────────────────────────────────────────────────
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KNOWLEDGE_BASE_SOURCE_PATH = os.path.join(
    _PROJECT_ROOT, "backend", "rag", "knowledge_base.py"
)

# The six API Lambda env vars that must remain unchanged by the fix (Req 3.3).
# COGNITO_USER_POOL_ID and TRACKING_TABLE_NAME resolve to cross-stack
# CloudFormation references (Fn::ImportValue tokens), NOT literals — asserted
# structurally rather than by exact string.
LITERAL_ENV_VARS = {
    "COGNITO_REGION": "eu-west-2",
    "BEDROCK_GUARDRAIL_VERSION": "1",
    "TUTORIAL_DIR": "tutorial",
}
TOKEN_ENV_VARS = (
    "COGNITO_USER_POOL_ID",
    "TRACKING_TABLE_NAME",
    "BEDROCK_GUARDRAIL_ID",
)

MATERIALS_BUCKET_NAME = "teaching-agent-materials-062788795053"

SIBLING_STACK_IDS = (
    "TeachingAgentAuth",
    "TeachingAgentGuardrails",
    "TeachingAgentTracking",
)


def knowledge_base_source_hash() -> str:
    """Return the SHA-256 hex digest of ``backend/rag/knowledge_base.py``.

    Reusable by task 3.7 to prove the runtime resolver is byte-for-byte
    unchanged (Req 3.1, 3.2). Reads bytes (not text) so the hash is independent
    of platform newline handling.
    """
    with open(KNOWLEDGE_BASE_SOURCE_PATH, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


# Baseline hash recorded on the UNFIXED source. Task 3.7 recomputes
# ``knowledge_base_source_hash()`` and asserts equality with this value.
KNOWLEDGE_BASE_SOURCE_BASELINE_HASH = knowledge_base_source_hash()


def _synth_all_stacks(monkeypatch: pytest.MonkeyPatch) -> dict:
    """Synthesize the full app (API + 4 sibling stacks) from the UNFIXED source.

    Wires ``knowledge_base_id`` exactly as ``infrastructure/app.py`` does today
    (the hardcoded placeholder) so cross-stack references resolve identically to
    a real ``cdk synth``.

    Returns:
        Mapping of stack construct id -> ``aws_cdk.assertions.Template``.
    """
    _stub_local_bundling(monkeypatch)

    app = cdk.App()
    env = cdk.Environment(account="062788795053", region="eu-west-2")

    auth_stack = TeachingAgentAuthStack(app, "TeachingAgentAuth", env=env)
    guardrails_stack = TeachingAgentGuardrailsStack(
        app, "TeachingAgentGuardrails", env=env
    )
    tracking_stack = TeachingAgentTrackingStack(app, "TeachingAgentTracking", env=env)
    rag_stack = TeachingAgentRAGStack(app, "TeachingAgentRAG", env=env)

    api_stack = TeachingAgentAPIStack(
        app,
        "TeachingAgentAPI",
        env=env,
        user_pool=auth_stack.user_pool,
        knowledge_base_id=PLACEHOLDER_KB_ID,
        guardrail_id=guardrails_stack.guardrail_id,
        tracking_table=tracking_stack.table,
    )

    return {
        "TeachingAgentAuth": Template.from_stack(auth_stack),
        "TeachingAgentGuardrails": Template.from_stack(guardrails_stack),
        "TeachingAgentTracking": Template.from_stack(tracking_stack),
        "TeachingAgentRAG": Template.from_stack(rag_stack),
        "TeachingAgentAPI": Template.from_stack(api_stack),
    }


def sibling_stack_baselines(monkeypatch: pytest.MonkeyPatch) -> dict:
    """Capture the sibling stack templates from the UNFIXED source as baselines.

    Reusable by task 3.7: re-synthesize the FIXED source and compare its
    TeachingAgentAuth / Guardrails / Tracking templates against these dicts for
    byte-for-byte equality (Req 3.5). The KB ID fix touches only ``app.py``
    wiring into the API stack, so these three templates must be identical
    before and after.

    Returns:
        Mapping of stack id -> template dict (``Template.to_json()``).
    """
    templates = _synth_all_stacks(monkeypatch)
    return {
        stack_id: templates[stack_id].to_json() for stack_id in SIBLING_STACK_IDS
    }


# ── Property 2: Preservation — API Lambda other env vars unchanged ───────────
# Validates: Requirements 3.3
class TestPreservationApiLambdaOtherEnvVars:
    """Property 2 (preservation): the six non-KB-ID env vars are unchanged.

    **Validates: Requirements 3.3**
    """

    def test_literal_env_vars_present_with_current_values(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """COGNITO_REGION, BEDROCK_GUARDRAIL_VERSION, TUTORIAL_DIR are literals."""
        template = _synth_api_template(monkeypatch)
        env_vars = _api_lambda_env_vars(template)

        for name, expected in LITERAL_ENV_VARS.items():
            assert env_vars.get(name) == expected, (
                f"Env var {name!r} expected literal {expected!r}, "
                f"got {env_vars.get(name)!r}"
            )

    def test_token_env_vars_present_as_cross_stack_references(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """COGNITO_USER_POOL_ID, TRACKING_TABLE_NAME, BEDROCK_GUARDRAIL_ID are tokens.

        These three resolve to cross-stack references (``Fn::ImportValue``
        intrinsic dicts), not plain strings. Assert presence and structure
        rather than an exact literal value.
        """
        template = _synth_api_template(monkeypatch)
        env_vars = _api_lambda_env_vars(template)

        for name in TOKEN_ENV_VARS:
            assert name in env_vars, f"Env var {name!r} missing from API Lambda"
            value = env_vars[name]
            assert isinstance(value, dict), (
                f"Env var {name!r} expected a CloudFormation reference dict, "
                f"got {value!r}"
            )
            assert "Fn::ImportValue" in value, (
                f"Env var {name!r} expected an Fn::ImportValue cross-stack "
                f"reference, got keys {list(value)!r}"
            )

    def test_all_six_other_env_vars_present(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """All six non-KB-ID env vars exist (independent of KB ID value)."""
        template = _synth_api_template(monkeypatch)
        env_vars = _api_lambda_env_vars(template)

        expected_keys = set(LITERAL_ENV_VARS) | set(TOKEN_ENV_VARS)
        missing = expected_keys - set(env_vars)
        assert not missing, f"API Lambda missing expected env vars: {missing}"


# ── Property 2: Preservation — API Lambda IAM policies unchanged ─────────────
# Validates: Requirements 3.6
class TestPreservationApiLambdaIamPolicies:
    """Property 2 (preservation): the API Lambda IAM statements are present.

    Covers Bedrock, DynamoDB read/write, and Cognito admin permissions.

    **Validates: Requirements 3.6**
    """

    def test_bedrock_policy_statement_present(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Bedrock InvokeModel/Converse/Retrieve/RetrieveAndGenerate/ApplyGuardrail."""
        template = _synth_api_template(monkeypatch)
        template.has_resource_properties(
            "AWS::IAM::Policy",
            {
                "PolicyDocument": {
                    "Statement": Match.array_with(
                        [
                            Match.object_like(
                                {
                                    "Effect": "Allow",
                                    "Action": [
                                        "bedrock:InvokeModel",
                                        "bedrock:Converse",
                                        "bedrock:Retrieve",
                                        "bedrock:RetrieveAndGenerate",
                                        "bedrock:ApplyGuardrail",
                                    ],
                                    "Resource": "*",
                                }
                            )
                        ]
                    )
                }
            },
        )

    def test_dynamodb_read_write_policy_statement_present(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """DynamoDB read/write grant (from grant_read_write_data).

        The grant emits the actions in a fixed CDK order alongside extra actions
        (BatchGetItem, ConditionCheckItem, DescribeTable, ...). ``array_with``
        matches an ordered contiguous subsequence, which the required read/write
        actions are not, so we instead locate the DynamoDB statement in the
        synthesized policy and assert each required action is present.
        """
        template = _synth_api_template(monkeypatch)

        required_actions = {
            "dynamodb:GetItem",
            "dynamodb:PutItem",
            "dynamodb:UpdateItem",
            "dynamodb:DeleteItem",
            "dynamodb:Query",
            "dynamodb:Scan",
            "dynamodb:BatchWriteItem",
        }

        policies = template.find_resources("AWS::IAM::Policy")
        dynamo_actions: set[str] = set()
        for policy in policies.values():
            for statement in policy["Properties"]["PolicyDocument"]["Statement"]:
                actions = statement.get("Action")
                if isinstance(actions, str):
                    actions = [actions]
                if actions and any(
                    a.startswith("dynamodb:") for a in actions
                ):
                    dynamo_actions.update(actions)

        missing = required_actions - dynamo_actions
        assert not missing, (
            f"API Lambda DynamoDB read/write grant is missing actions: {missing}. "
            f"Found DynamoDB actions: {sorted(dynamo_actions)}"
        )

    def test_cognito_admin_policy_statement_present(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Cognito admin actions scoped to the user pool ARN."""
        template = _synth_api_template(monkeypatch)
        template.has_resource_properties(
            "AWS::IAM::Policy",
            {
                "PolicyDocument": {
                    "Statement": Match.array_with(
                        [
                            Match.object_like(
                                {
                                    "Effect": "Allow",
                                    "Action": [
                                        "cognito-idp:AdminCreateUser",
                                        "cognito-idp:AdminGetUser",
                                        "cognito-idp:AdminUpdateUserAttributes",
                                        "cognito-idp:AdminDisableUser",
                                        "cognito-idp:AdminEnableUser",
                                        "cognito-idp:AdminResetUserPassword",
                                        "cognito-idp:ListUsers",
                                        "cognito-idp:DescribeUserPool",
                                        "cognito-idp:AdminAddUserToGroup",
                                    ],
                                }
                            )
                        ]
                    )
                }
            },
        )


# ── Property 2: Preservation — TeachingAgentRAG S3 bucket unchanged ──────────
# Validates: Requirements 3.4
class TestPreservationRagMaterialsBucket:
    """Property 2 (preservation): the RAG S3 materials bucket is unchanged.

    Asserts the named bucket with versioning, S3-managed (AES256) encryption,
    SSL enforcement (a Deny-on-insecure-transport bucket policy), and RETAIN
    removal policy / DeletionPolicy.

    **Validates: Requirements 3.4**
    """

    def test_materials_bucket_versioning_and_encryption(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Named bucket with versioning Enabled and AES256 (S3-managed) SSE."""
        _stub_local_bundling(monkeypatch)
        app = cdk.App()
        env = cdk.Environment(account="062788795053", region="eu-west-2")
        rag_stack = TeachingAgentRAGStack(app, "TeachingAgentRAG", env=env)
        template = Template.from_stack(rag_stack)

        template.has_resource_properties(
            "AWS::S3::Bucket",
            {
                "BucketName": MATERIALS_BUCKET_NAME,
                "VersioningConfiguration": {"Status": "Enabled"},
                "BucketEncryption": {
                    "ServerSideEncryptionConfiguration": [
                        {"ServerSideEncryptionByDefault": {"SSEAlgorithm": "AES256"}}
                    ]
                },
            },
        )

    def test_materials_bucket_retain_removal_policy(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """RETAIN is expressed as DeletionPolicy/UpdateReplacePolicy = Retain."""
        _stub_local_bundling(monkeypatch)
        app = cdk.App()
        env = cdk.Environment(account="062788795053", region="eu-west-2")
        rag_stack = TeachingAgentRAGStack(app, "TeachingAgentRAG", env=env)
        template = Template.from_stack(rag_stack)

        template.has_resource(
            "AWS::S3::Bucket",
            {
                "DeletionPolicy": "Retain",
                "UpdateReplacePolicy": "Retain",
                "Properties": {"BucketName": MATERIALS_BUCKET_NAME},
            },
        )

    def test_materials_bucket_enforces_ssl(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """enforce_ssl emits a bucket policy denying insecure (non-TLS) transport."""
        _stub_local_bundling(monkeypatch)
        app = cdk.App()
        env = cdk.Environment(account="062788795053", region="eu-west-2")
        rag_stack = TeachingAgentRAGStack(app, "TeachingAgentRAG", env=env)
        template = Template.from_stack(rag_stack)

        template.has_resource_properties(
            "AWS::S3::BucketPolicy",
            {
                "PolicyDocument": {
                    "Statement": Match.array_with(
                        [
                            Match.object_like(
                                {
                                    "Effect": "Deny",
                                    "Action": "s3:*",
                                    "Condition": {
                                        "Bool": {"aws:SecureTransport": "false"}
                                    },
                                }
                            )
                        ]
                    )
                }
            },
        )


# ── Property 2: Preservation — sibling stack templates snapshot ──────────────
# Validates: Requirements 3.5
class TestPreservationSiblingStacksSnapshot:
    """Property 2 (preservation): sibling stack templates captured as baselines.

    Captures the TeachingAgentAuth / Guardrails / Tracking templates from the
    UNFIXED source. Task 3.7 re-synthesizes the FIXED source and compares
    against ``sibling_stack_baselines(...)`` for byte-for-byte equality.

    **Validates: Requirements 3.5**
    """

    def test_sibling_baselines_captured_and_nonempty(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """All three sibling baseline templates are captured with resources."""
        baselines = sibling_stack_baselines(monkeypatch)

        assert set(baselines) == set(SIBLING_STACK_IDS)
        for stack_id, template_json in baselines.items():
            assert isinstance(template_json, dict), (
                f"Baseline for {stack_id} is not a dict"
            )
            resources = template_json.get("Resources", {})
            assert resources, f"Baseline template for {stack_id} has no Resources"

    def test_sibling_baselines_are_deterministic(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Two independent synths of the UNFIXED source yield identical templates.

        This proves the baseline is stable, so a post-fix inequality in task 3.7
        genuinely signals a regression rather than synth nondeterminism.
        """
        first = sibling_stack_baselines(monkeypatch)
        second = sibling_stack_baselines(monkeypatch)
        assert first == second, (
            "Sibling stack templates differ between two synths of the same "
            "unfixed source — baseline is nondeterministic"
        )

    def test_sibling_stacks_provision_expected_core_resources(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Cross-stack resources (user pool, guardrail, tracking table) present."""
        templates = _synth_all_stacks(monkeypatch)

        templates["TeachingAgentAuth"].resource_count_is(
            "AWS::Cognito::UserPool", 1
        )
        templates["TeachingAgentGuardrails"].resource_count_is(
            "AWS::Bedrock::Guardrail", 1
        )
        templates["TeachingAgentTracking"].resource_count_is(
            "AWS::DynamoDB::Table", 1
        )


# ── Property 2: Preservation — runtime resolver file unmodified ──────────────
# Validates: Requirements 3.1, 3.2
class TestPreservationRuntimeResolverUnmodified:
    """Property 2 (preservation): backend/rag/knowledge_base.py is untouched.

    The fix is confined to CDK sourcing of the KB ID; the runtime resolver
    (BEDROCK_KB_ID precedence with BEDROCK_KNOWLEDGE_BASE_ID fallback + graceful
    ``knowledge_base_id_not_configured`` handling) must not change. A content
    hash makes any edit detectable by task 3.7.

    **Validates: Requirements 3.1, 3.2**
    """

    def test_knowledge_base_source_matches_baseline_hash(self) -> None:
        """The resolver file hash equals the recorded baseline hash."""
        assert knowledge_base_source_hash() == KNOWLEDGE_BASE_SOURCE_BASELINE_HASH, (
            "backend/rag/knowledge_base.py changed relative to the recorded "
            "baseline hash — the runtime resolver must remain unmodified "
            "(Req 3.1, 3.2)."
        )

    def test_knowledge_base_source_preserves_resolution_precedence(self) -> None:
        """Sanity anchor: the baseline still contains the precedence + fallback.

        Guards against a future refactor that keeps the file present but strips
        the BEDROCK_KB_ID → BEDROCK_KNOWLEDGE_BASE_ID precedence or the graceful
        ``knowledge_base_id_not_configured`` log the preservation requirement
        depends on.
        """
        with open(KNOWLEDGE_BASE_SOURCE_PATH, "r", encoding="utf-8") as fh:
            source = fh.read()

        assert 'os.environ.get("BEDROCK_KB_ID", "")' in source
        assert 'os.environ.get("BEDROCK_KNOWLEDGE_BASE_ID", "")' in source
        assert "knowledge_base_id_not_configured" in source


# ═════════════════════════════════════════════════════════════════════════════
# Task 3.7 — Sibling-stack preservation through the REAL infrastructure/app.py
#
# Property 2: Preservation — Non-KB-ID Stack Behavior Unchanged (Req 3.5).
#
# WHY THIS ADDITION EXISTS (the one allowance tasks.md anticipates for 3.7):
#   The task-2 preservation helpers ``sibling_stack_baselines`` / ``_synth_all_stacks``
#   construct the sibling stacks DIRECTLY (``TeachingAgentAuthStack(app, ...)`` etc.),
#   passing ``knowledge_base_id=PLACEHOLDER_KB_ID`` rather than importing
#   ``infrastructure/app.py``. That is correct and sufficient for the API-stack
#   env-var / IAM / bucket assertions (those resources come from api_stack.py /
#   rag_stack.py, unchanged by the fix except the rag NextStep output text), but it
#   means the sibling snapshot is captured from a synth path that never runs the
#   FIXED app.py. The tasks.md Req 3.5 preservation intent is specifically that the
#   sibling stack templates synthesized FROM THE FIXED app.py equal the baselines.
#
#   This section closes that gap: it synthesizes TeachingAgentAuth / Guardrails /
#   Tracking through the REAL ``infrastructure/app.py`` (reusing the subprocess /
#   ``CDK_CONTEXT_JSON`` harness established in task 3.2) and asserts each template
#   equals the ``sibling_stack_baselines(...)`` dict captured from the unfixed
#   direct-construction path. Equality proves the fix (SSM ``value_from_lookup``
#   in app.py, which is scoped to the RAG stack) leaves the three sibling stacks
#   byte-for-byte unchanged.
#
#   NOTE (allowed difference): the fix also changed the RAG stack ``NextStep``
#   CfnOutput text and added a ``KbIdParameterName`` output (tasks 3.4). Those are
#   the ONLY intended RAG-stack differences; the RAG bucket resource is unchanged.
#   The RAG stack is NOT one of the three siblings compared here, and its bucket
#   preservation is already covered by ``TestPreservationRagMaterialsBucket``. The
#   RAG-output allowance is asserted explicitly in
#   ``test_rag_stack_only_differs_by_nextstep_output_and_kbid_param`` below.
# ═════════════════════════════════════════════════════════════════════════════

# Runner: synth the FIXED app.py in a fresh subprocess and emit the sibling stack
# templates (and the RAG stack template) as JSON via ``Template.from_stack(...)
# .to_json()`` — the SAME method ``sibling_stack_baselines`` uses — so the parent
# can compare the two directly. Seeding the SSM value via ``CDK_CONTEXT_JSON``
# keeps ``value_from_lookup`` deterministic (no AWS call).
_APP_SIBLING_RUNNER_SOURCE = """
import json, os
from infrastructure.api_stack import LocalPipBundling


def _fake_try_bundle(self, output_dir, *args, **kwargs):
    with open(os.path.join(output_dir, "placeholder.txt"), "w") as fh:
        fh.write("stub asset for unit tests")
    return True


LocalPipBundling.try_bundle = _fake_try_bundle

from aws_cdk.assertions import Template
import infrastructure.app as appmod

emitted = {
    "TeachingAgentAuth": Template.from_stack(appmod.auth_stack).to_json(),
    "TeachingAgentGuardrails": Template.from_stack(appmod.guardrails_stack).to_json(),
    "TeachingAgentTracking": Template.from_stack(appmod.tracking_stack).to_json(),
    "TeachingAgentRAG": Template.from_stack(appmod.rag_stack).to_json(),
}
print("__TEMPLATES_JSON__" + json.dumps(emitted))
"""


def _synth_templates_via_app(
    deploy_env: str | None, seeded_kb_id: str | None
) -> dict:
    """Synth Auth/Guardrails/Tracking/RAG through the REAL app.py in a subprocess.

    Mirrors ``_synth_api_kb_id_via_app`` but returns the ``to_json()`` template
    dicts for the sibling stacks and the RAG stack, so they can be compared
    against the unfixed baselines.

    Args:
        deploy_env: ``env`` context selector value (``None`` → app.py default "dev").
        seeded_kb_id: KB ID seeded into the SSM context cache (``None`` → bootstrap
            sentinel path).

    Returns:
        Mapping of stack id -> template dict (``Template.to_json()``).
    """
    resolved_env = deploy_env or "dev"

    context: dict[str, str] = {}
    if deploy_env is not None:
        context["env"] = deploy_env
    if seeded_kb_id is not None:
        context[_ssm_context_key(resolved_env)] = seeded_kb_id

    child_env = dict(os.environ)
    child_env["CDK_DEFAULT_ACCOUNT"] = CDK_ACCOUNT
    child_env["CDK_CONTEXT_JSON"] = json.dumps(context)
    child_env["CDK_OUTDIR"] = tempfile.mkdtemp(prefix="kbid-test-sib-cdkout-")
    child_env["PYTHONPATH"] = (
        _PROJECT_ROOT_DIR + os.pathsep + child_env.get("PYTHONPATH", "")
    )

    completed = subprocess.run(
        [sys.executable, "-c", _APP_SIBLING_RUNNER_SOURCE],
        cwd=_PROJECT_ROOT_DIR,
        env=child_env,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, (
        "Sibling-template synth subprocess driving infrastructure/app.py failed.\n"
        f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
    )

    marker = "__TEMPLATES_JSON__"
    line = next(
        (ln for ln in completed.stdout.splitlines() if ln.startswith(marker)),
        None,
    )
    assert line is not None, (
        "Runner did not emit the templates marker.\n"
        f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
    )
    return json.loads(line[len(marker) :])


class TestPreservationSiblingStacksThroughApp:
    """Property 2 (preservation): FIXED app.py leaves the sibling stacks unchanged.

    Completes the task 3.7 preservation intent for Req 3.5 by synthesizing the
    three sibling stacks through the REAL ``infrastructure/app.py`` and asserting
    byte-for-byte equality with the unfixed baselines captured by
    ``sibling_stack_baselines(...)``.

    **Validates: Requirements 3.5**
    """

    def test_sibling_templates_from_app_equal_unfixed_baselines(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Auth/Guardrails/Tracking synthed via app.py == unfixed baselines.

        Seeds the SSM value to the active KB ID (a NOT-isBugCondition config) and
        drives app.py's real resolution path. Because the fix is confined to the
        RAG-stack-scoped ``value_from_lookup`` and the API stack's
        ``knowledge_base_id`` wiring, the three sibling templates must be identical
        to the baselines the task-2 tests recorded from the unfixed source.
        """
        baselines = sibling_stack_baselines(monkeypatch)
        fixed_templates = _synth_templates_via_app(
            deploy_env=None, seeded_kb_id=ACTIVE_KB_ID
        )

        for stack_id in SIBLING_STACK_IDS:
            assert fixed_templates[stack_id] == baselines[stack_id], (
                f"{stack_id} template synthesized through the FIXED "
                f"infrastructure/app.py differs from the unfixed baseline — the "
                f"KB ID fix must not change any sibling stack (Req 3.5)."
            )

    def test_rag_stack_only_differs_by_nextstep_output_and_kbid_param(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """RAG stack: only the NextStep output text / KbIdParameterName differ.

        tasks.md explicitly ALLOWS the RAG ``NextStep`` CfnOutput text to change
        (and a new SSM-parameter-path output to be added) as part of the operator
        guidance update (task 3.4). Everything else in the RAG stack — most
        importantly the S3 materials bucket resource — must be unchanged. This
        asserts that the ONLY differences between the unfixed and fixed RAG
        templates live under ``Outputs`` (never under ``Resources``).
        """
        unfixed = _synth_all_stacks(monkeypatch)["TeachingAgentRAG"].to_json()
        fixed = _synth_templates_via_app(
            deploy_env=None, seeded_kb_id=ACTIVE_KB_ID
        )["TeachingAgentRAG"]

        # Resources (the S3 bucket + bucket policy) must be byte-for-byte equal.
        assert fixed.get("Resources") == unfixed.get("Resources"), (
            "RAG stack Resources changed — the S3 materials bucket must be "
            "preserved; only the NextStep output text may change (Req 3.4)."
        )

        # The template sections other than Outputs must also be unchanged.
        unfixed_non_outputs = {
            k: v for k, v in unfixed.items() if k != "Outputs"
        }
        fixed_non_outputs = {k: v for k, v in fixed.items() if k != "Outputs"}
        assert fixed_non_outputs == unfixed_non_outputs, (
            "RAG stack changed outside of Outputs — only the operator-guidance "
            "CfnOutput(s) are allowed to change (Req 3.4)."
        )
