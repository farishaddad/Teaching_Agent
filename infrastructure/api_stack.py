"""CDK Stack: Lambda + API Gateway for the Teaching Agent API."""

from aws_cdk import (
    Stack,
    Duration,
    CfnOutput,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_cognito as cognito,
    aws_dynamodb as dynamodb,
    aws_iam as iam,
)
from constructs import Construct


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

        # Cognito admin permissions (for student management)
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
            proxy=True,  # Forward all requests to Lambda
            deploy_options=apigw.StageOptions(stage_name="prod"),
        )

        # Outputs
        CfnOutput(self, "ApiUrl", value=self.api.url)
        CfnOutput(self, "LambdaArn", value=self.api_lambda.function_arn)
