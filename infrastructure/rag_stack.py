"""CDK Stack: S3 bucket for course materials.

The Bedrock Knowledge Base + OpenSearch Serverless collection should be
created via the Bedrock Console (it handles AOSS permissions automatically).
This stack just creates the S3 bucket for course material storage.
"""

from aws_cdk import (
    Stack,
    RemovalPolicy,
    CfnOutput,
    aws_s3 as s3,
)
from constructs import Construct


class TeachingAgentRAGStack(Stack):
    """S3 bucket for course materials ingestion."""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # S3 bucket for course materials (PDFs, markdown, docs)
        self.materials_bucket = s3.Bucket(
            self,
            "CourseMaterials",
            bucket_name=f"teaching-agent-materials-062788795053",
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            enforce_ssl=True,
            removal_policy=RemovalPolicy.RETAIN,
            auto_delete_objects=False,
        )

        # Placeholder — set after creating KB via console
        self.knowledge_base_id = ""

        # Outputs
        CfnOutput(self, "MaterialsBucketName", value=self.materials_bucket.bucket_name)
        CfnOutput(self, "MaterialsBucketArn", value=self.materials_bucket.bucket_arn)
        CfnOutput(
            self,
            "NextStep",
            value="Create Bedrock KB via console pointing to this S3 bucket, then set BEDROCK_KB_ID env var on Lambda",
        )
