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

        # Install pip dependencies
        subprocess.check_call([
            "pip", "install", "-r",
            os.path.join(project_root, "requirements.txt"),
            "-t", output_dir,
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
        knowledge_base_id: str,
        guardrail_id: str,
        tracking_table,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

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
                "BEDROCK_KB_ID": knowledge_base_id,
                "BEDROCK_GUARDRAIL_ID": guardrail_id,
                "BEDROCK_GUARDRAIL_VERSION": "1",
                "TRACKING_TABLE_NAME": tracking_table.table_name,
                "TUTORIAL_DIR": "tutorial",
            },
        )

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
