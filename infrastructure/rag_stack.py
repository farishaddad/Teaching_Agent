"""CDK Stack: Bedrock Knowledge Base and supporting infrastructure.

Creates:
  - S3 bucket for course materials (source data for the KB)
  - Bedrock Knowledge Base backed by the S3 bucket
  - OpenSearch Serverless collection as the vector store
  - IAM roles for Bedrock to access S3 and OpenSearch Serverless
  - Lifecycle rules on S3 (Intelligent-Tiering for older objects)

Note on OpenSearch Serverless:
  AWS CDK v2 does not yet have L2 constructs for OpenSearch Serverless.
  We use L1 (CfnXxx) constructs. The collection must be created before
  the KB data source can be configured.
"""

import json

import aws_cdk as cdk
from aws_cdk import (
    CfnOutput,
    RemovalPolicy,
    Stack,
    aws_iam as iam,
    aws_s3 as s3,
    aws_opensearchserverless as aoss,
    aws_bedrock as bedrock,
)
from constructs import Construct

# Bedrock model ARN for generation inside the KB
_MODEL_ARN = (
    "arn:aws:bedrock:eu-west-2::foundation-model/"
    "anthropic.claude-3-5-sonnet-20241022-v2:0"
)
# Titan Embeddings V2 — available in eu-west-2
_EMBEDDING_MODEL_ARN = (
    "arn:aws:bedrock:eu-west-2::foundation-model/"
    "amazon.titan-embed-text-v2:0"
)


class TeachingAgentRAGStack(Stack):
    """S3 course materials bucket + Bedrock Knowledge Base + OpenSearch Serverless."""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # ── S3: Course materials bucket ───────────────────────────────────────
        self.materials_bucket = s3.Bucket(
            self,
            "CourseMaterialsBucket",
            bucket_name=f"teaching-agent-materials-{self.account}",
            # Block all public access — only Bedrock IAM role can read
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            versioned=True,
            enforce_ssl=True,
            # Lifecycle: move old versions to cheaper storage
            lifecycle_rules=[
                s3.LifecycleRule(
                    id="IntelligentTieringRule",
                    enabled=True,
                    transitions=[
                        s3.Transition(
                            storage_class=s3.StorageClass.INTELLIGENT_TIERING,
                            transition_after=cdk.Duration.days(30),
                        )
                    ],
                    noncurrent_version_expiration=cdk.Duration.days(90),
                )
            ],
            removal_policy=RemovalPolicy.RETAIN,  # Never delete course content
        )

        cdk.Tags.of(self.materials_bucket).add("project", "teaching-agent")
        cdk.Tags.of(self.materials_bucket).add("environment", "dev")

        # ── IAM: Bedrock KB service role ──────────────────────────────────────
        kb_role = iam.Role(
            self,
            "BedrockKBRole",
            role_name="teaching-agent-bedrock-kb-role",
            assumed_by=iam.ServicePrincipal(
                "bedrock.amazonaws.com",
                conditions={
                    "StringEquals": {"aws:SourceAccount": self.account},
                    "ArnLike": {
                        "aws:SourceArn": f"arn:aws:bedrock:{self.region}:{self.account}:knowledge-base/*"
                    },
                },
            ),
            description="Allows Bedrock Knowledge Base to read from S3 and invoke the embedding model",
        )

        # Allow KB to read course materials from S3
        self.materials_bucket.grant_read(kb_role)

        # Allow KB to invoke the embedding model
        kb_role.add_to_policy(
            iam.PolicyStatement(
                sid="BedrockInvokeEmbeddingModel",
                effect=iam.Effect.ALLOW,
                actions=["bedrock:InvokeModel"],
                resources=[_EMBEDDING_MODEL_ARN],
            )
        )

        # ── OpenSearch Serverless: Encryption policy ──────────────────────────
        encryption_policy = aoss.CfnSecurityPolicy(
            self,
            "AOSSEncryptionPolicy",
            name="teaching-agent-enc-policy",
            type="encryption",
            policy=json.dumps(
                {
                    "Rules": [
                        {
                            "Resource": ["collection/teaching-agent-kb"],
                            "ResourceType": "collection",
                        }
                    ],
                    "AWSOwnedKey": True,
                }
            ),
        )

        # ── OpenSearch Serverless: Network policy ─────────────────────────────
        network_policy = aoss.CfnSecurityPolicy(
            self,
            "AOSSNetworkPolicy",
            name="teaching-agent-net-policy",
            type="network",
            policy=json.dumps(
                [
                    {
                        "Rules": [
                            {
                                "Resource": ["collection/teaching-agent-kb"],
                                "ResourceType": "collection",
                            },
                            {
                                "Resource": ["collection/teaching-agent-kb"],
                                "ResourceType": "dashboard",
                            },
                        ],
                        "AllowFromPublic": False,
                    }
                ]
            ),
        )

        # ── OpenSearch Serverless: Data access policy (Bedrock KB role) ───────
        data_access_policy = aoss.CfnAccessPolicy(
            self,
            "AOSSDataAccessPolicy",
            name="teaching-agent-data-policy",
            type="data",
            policy=json.dumps(
                [
                    {
                        "Rules": [
                            {
                                "Resource": ["collection/teaching-agent-kb"],
                                "Permission": [
                                    "aoss:CreateCollectionItems",
                                    "aoss:DeleteCollectionItems",
                                    "aoss:UpdateCollectionItems",
                                    "aoss:DescribeCollectionItems",
                                ],
                                "ResourceType": "collection",
                            },
                            {
                                "Resource": ["index/teaching-agent-kb/*"],
                                "Permission": [
                                    "aoss:CreateIndex",
                                    "aoss:DeleteIndex",
                                    "aoss:UpdateIndex",
                                    "aoss:DescribeIndex",
                                    "aoss:ReadDocument",
                                    "aoss:WriteDocument",
                                ],
                                "ResourceType": "index",
                            },
                        ],
                        "Principal": [kb_role.role_arn],
                    }
                ]
            ),
        )

        # ── OpenSearch Serverless: Collection ─────────────────────────────────
        collection = aoss.CfnCollection(
            self,
            "AOSSCollection",
            name="teaching-agent-kb",
            type="VECTORSEARCH",
            description="Vector store for Teaching Agent course material embeddings",
        )

        # Policies must be created before the collection
        collection.add_dependency(encryption_policy)
        collection.add_dependency(network_policy)
        collection.add_dependency(data_access_policy)

        cdk.Tags.of(collection).add("project", "teaching-agent")

        # ── Bedrock Knowledge Base ────────────────────────────────────────────
        knowledge_base = bedrock.CfnKnowledgeBase(
            self,
            "TeachingAgentKB",
            name="teaching-agent-kb",
            description="Course material knowledge base for the Agentic AI Teaching Agent",
            role_arn=kb_role.role_arn,
            knowledge_base_configuration=bedrock.CfnKnowledgeBase.KnowledgeBaseConfigurationProperty(
                type="VECTOR",
                vector_knowledge_base_configuration=bedrock.CfnKnowledgeBase.VectorKnowledgeBaseConfigurationProperty(
                    embedding_model_arn=_EMBEDDING_MODEL_ARN,
                ),
            ),
            storage_configuration=bedrock.CfnKnowledgeBase.StorageConfigurationProperty(
                type="OPENSEARCH_SERVERLESS",
                opensearch_serverless_configuration=bedrock.CfnKnowledgeBase.OpenSearchServerlessConfigurationProperty(
                    collection_arn=collection.attr_arn,
                    vector_index_name="course-materials",
                    field_mapping=bedrock.CfnKnowledgeBase.OpenSearchServerlessFieldMappingProperty(
                        vector_field="embedding",
                        text_field="text",
                        metadata_field="metadata",
                    ),
                ),
            ),
        )

        knowledge_base.add_dependency(collection)

        # ── S3 Data Source ────────────────────────────────────────────────────
        data_source = bedrock.CfnDataSource(
            self,
            "CourseMaterialsDataSource",
            name="course-materials",
            knowledge_base_id=knowledge_base.attr_knowledge_base_id,
            description="Course PDFs, slides, and markdown notes",
            data_source_configuration=bedrock.CfnDataSource.DataSourceConfigurationProperty(
                type="S3",
                s3_configuration=bedrock.CfnDataSource.S3DataSourceConfigurationProperty(
                    bucket_arn=self.materials_bucket.bucket_arn,
                    inclusion_prefixes=["course_materials/"],
                ),
            ),
            # Chunking: fixed 512 tokens with 20% overlap
            vector_ingestion_configuration=bedrock.CfnDataSource.VectorIngestionConfigurationProperty(
                chunking_configuration=bedrock.CfnDataSource.ChunkingConfigurationProperty(
                    chunking_strategy="FIXED_SIZE",
                    fixed_size_chunking_configuration=bedrock.CfnDataSource.FixedSizeChunkingConfigurationProperty(
                        max_tokens=512,
                        overlap_percentage=20,
                    ),
                )
            ),
        )

        # ── Expose properties for cross-stack references ───────────────────────
        self.knowledge_base_id: str = knowledge_base.attr_knowledge_base_id
        self.knowledge_base_arn: str = knowledge_base.attr_knowledge_base_arn
        self.data_source_id: str = data_source.attr_data_source_id
        self.materials_bucket_name: str = self.materials_bucket.bucket_name

        # ── Outputs ───────────────────────────────────────────────────────────
        CfnOutput(
            self,
            "KnowledgeBaseId",
            value=self.knowledge_base_id,
            description="Bedrock Knowledge Base ID — set as BEDROCK_KNOWLEDGE_BASE_ID env var",
            export_name="TeachingAgentKBId",
        )

        CfnOutput(
            self,
            "DataSourceId",
            value=self.data_source_id,
            description="KB Data Source ID — needed to trigger ingestion jobs",
        )

        CfnOutput(
            self,
            "MaterialsBucketName",
            value=self.materials_bucket_name,
            description="S3 bucket for course material uploads",
            export_name="TeachingAgentMaterialsBucket",
        )

        CfnOutput(
            self,
            "OpenSearchCollectionArn",
            value=collection.attr_arn,
            description="OpenSearch Serverless collection ARN",
        )
