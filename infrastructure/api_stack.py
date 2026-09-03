"""CDK Stack: Lambda + API Gateway for the Teaching Agent API.

Uses local bundling (no Docker) — pip installs deps into asset output.
"""

from aws_cdk import (
    Stack,
    Duration,
    CfnOutput,
    BundlingOptions,
    DockerImage,
    ILocalBundling,
    AssetHashType,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_iam as iam,
)
from constructs import Construct
import jsii


@jsii.implements(ILocalBundling)
class LocalPipBundling:
    """Bundle Lambda code locally by running pip install + copying source."""

    def try_bundle(self, output_dir: str, *, image=None, **kwargs) -> bool:
        import os
        import subprocess
        import shutil

        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Install pip dependencies targeting the Lambda runtime, NOT the local
        # machine. Packages with compiled extensions (e.g. pydantic-core, which
        # ships a Rust `_pydantic_core` .so) must be the manylinux/x86_64 +
        # cp312 wheels or the Lambda fails at import with
        # "No module named 'pydantic_core._pydantic_core'".
        #
        # --platform + --only-binary=:all: forces pip to fetch prebuilt wheels
        # for the target platform instead of building/downloading for the host.
        # This keeps the no-Docker local-bundling approach while producing a
        # Linux-compatible artifact.
        subprocess.check_call([
            "pip", "install", "-r",
            os.path.join(project_root, "requirements.txt"),
            "-t", output_dir,
            "--platform", "manylinux2014_x86_64",
            "--python-version", "3.12",
            "--implementation", "cp",
            "--only-binary=:all:",
            "--upgrade",
            "--quiet",
        ])

        # Copy backend source
        shutil.copytree(
            os.path.join(project_root, "backend"),
            os.path.join(output_dir, "backend"),
            dirs_exist_ok=True,
        )

        # Copy tutorial content
        shutil.copytree(
            os.path.join(project_root, "tutorial"),
            os.path.join(output_dir, "tutorial"),
            dirs_exist_ok=True,
        )

        return True


class TeachingAgentAPIStack(Stack):
    """Lambda function running FastAPI + API Gateway REST API."""

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        user_pool,
        app_client,
        cognito_domain,
        knowledge_base_id: str,
        guardrail_id: str,
        tracking_table,
        materials_bucket=None,
        frontend_origin: str = "",
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Derive a content-based asset hash from EVERYTHING that affects the
        # bundle: requirements.txt (deps), the backend/ and tutorial/ source
        # trees (copied into the bundle), plus a bundling-strategy version tag.
        # The default source-dir hash misses pip-flag-only changes, and a static
        # hash must be bumped by hand and silently skips backend code changes
        # (a real bug we hit: a main.py edit deployed as "no changes"). Hashing
        # the real inputs makes CDK re-bundle + publish whenever deps, backend
        # source, tutorial content, or the strategy change.
        import hashlib as _hashlib
        import os as _os

        _project_root = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))

        def _hash_path(hasher, path):
            """Fold a file or directory tree into the hasher (name + bytes)."""
            if _os.path.isfile(path):
                hasher.update(path.encode())
                with open(path, "rb") as fh:
                    hasher.update(fh.read())
            elif _os.path.isdir(path):
                for root, dirs, files in _os.walk(path):
                    # Skip caches for stable, meaningful hashes.
                    dirs[:] = sorted(d for d in dirs if d != "__pycache__")
                    for name in sorted(files):
                        if name.endswith(".pyc"):
                            continue
                        fp = _os.path.join(root, name)
                        rel = _os.path.relpath(fp, _project_root)
                        hasher.update(rel.encode())
                        with open(fp, "rb") as fh:
                            hasher.update(fh.read())

        _h = _hashlib.sha256()
        # Bump the strategy tag when LocalPipBundling logic itself changes.
        _h.update(b"linux-cp312-x86_64-v4")
        _hash_path(_h, _os.path.join(_project_root, "requirements.txt"))
        _hash_path(_h, _os.path.join(_project_root, "backend"))
        _hash_path(_h, _os.path.join(_project_root, "tutorial"))
        _asset_hash = f"teaching-agent-api-{_h.hexdigest()[:24]}"

        # Lambda function — FastAPI via Mangum
        self.api_lambda = _lambda.Function(
            self,
            "APIHandler",
            function_name="teaching-agent-api",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="backend.main.handler",
            code=_lambda.Code.from_asset(
                ".",
                bundling=BundlingOptions(
                    image=DockerImage.from_registry("dummy"),  # Won't be used
                    local=LocalPipBundling(),
                ),
                # Explicit CUSTOM asset hash. The default source-based hash does
                # not change when only the bundling strategy (pip flags in
                # LocalPipBundling) changes, so CDK would reuse a stale, broken
                # bundle. Bump BUNDLE_VERSION whenever the bundling logic changes
                # to force a re-bundle + re-publish.
                asset_hash_type=AssetHashType.CUSTOM,
                asset_hash=_asset_hash,
                exclude=[
                    "node_modules",
                    ".venv",
                    "venv",
                    "frontend",
                    "cdk.out",
                    ".git",
                    "tests",
                    "__pycache__",
                    "*.pyc",
                    "infrastructure",
                    ".kiro",
                    "course_materials",
                ],
            ),
            memory_size=1024,
            timeout=Duration.seconds(60),
            environment={
                "COGNITO_USER_POOL_ID": user_pool.user_pool_id,
                "COGNITO_REGION": "eu-west-2",
                # App client ID — required to verify the token client_id claim
                # and to perform the authorization-code exchange in
                # /api/auth/callback. Public PKCE client (no secret).
                "COGNITO_APP_CLIENT_ID": app_client.user_pool_client_id,
                # Hosted UI base URL (e.g. https://<prefix>.auth.<region>.amazoncognito.com)
                # — the /api/auth/callback route 500s without it.
                "COGNITO_DOMAIN": cognito_domain,
                "BEDROCK_KB_ID": knowledge_base_id,
                "BEDROCK_GUARDRAIL_ID": guardrail_id,
                "BEDROCK_GUARDRAIL_VERSION": "1",
                "TRACKING_TABLE_NAME": tracking_table.table_name,
                "TUTORIAL_DIR": "tutorial",
                # Public frontend origin allowed by CORS (read by main.py's
                # ALLOWED_ORIGINS). Same-origin CloudFront /api proxy means CORS
                # isn't normally exercised, but this keeps direct cross-origin
                # calls working and avoids hardcoding the domain in app code.
                "ALLOWED_ORIGINS": frontend_origin,
                # RAG course-materials bucket — the admin "Course Materials"
                # panel lists/uploads/deletes objects here.
                "MATERIALS_BUCKET_NAME": materials_bucket.bucket_name if materials_bucket else "",
            },
        )

        # Course-materials bucket permissions (admin materials panel).
        if materials_bucket is not None:
            materials_bucket.grant_read_write(self.api_lambda)

        # Grant Lambda permissions
        tracking_table.grant_read_write_data(self.api_lambda)

        # Bedrock permissions
        self.api_lambda.add_to_role_policy(
            iam.PolicyStatement(
                actions=[
                    "bedrock:InvokeModel",
                    "bedrock:Converse",
                    "bedrock:Retrieve",
                    "bedrock:RetrieveAndGenerate",
                    "bedrock:ApplyGuardrail",
                    # Knowledge Base ingestion (admin "Sync Knowledge Base").
                    "bedrock:ListDataSources",
                    "bedrock:StartIngestionJob",
                    "bedrock:GetIngestionJob",
                    "bedrock:ListIngestionJobs",
                ],
                resources=["*"],
            )
        )

        # Cognito admin permissions
        self.api_lambda.add_to_role_policy(
            iam.PolicyStatement(
                actions=[
                    "cognito-idp:AdminCreateUser",
                    "cognito-idp:AdminGetUser",
                    "cognito-idp:AdminUpdateUserAttributes",
                    "cognito-idp:AdminDisableUser",
                    "cognito-idp:AdminEnableUser",
                    "cognito-idp:AdminDeleteUser",
                    "cognito-idp:AdminResetUserPassword",
                    "cognito-idp:ListUsers",
                    "cognito-idp:DescribeUserPool",
                    "cognito-idp:AdminAddUserToGroup",
                ],
                resources=[user_pool.user_pool_arn],
            )
        )

        # API Gateway
        self.api = apigw.LambdaRestApi(
            self,
            "TeachingAgentAPI",
            rest_api_name="teaching-agent-api",
            handler=self.api_lambda,
            proxy=True,
            deploy_options=apigw.StageOptions(stage_name="prod"),
        )

        # Outputs
        CfnOutput(self, "ApiUrl", value=self.api.url)
        CfnOutput(self, "LambdaArn", value=self.api_lambda.function_arn)
