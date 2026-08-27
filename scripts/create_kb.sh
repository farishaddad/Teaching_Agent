#!/bin/bash
# Create Bedrock Knowledge Base via CLI
# Alternative to console-based setup
# Run after S3 upload: bash scripts/create_kb.sh

set -e

REGION="eu-west-2"
BUCKET="teaching-agent-course-materials"
KB_NAME="teaching-agent-kb"
KB_DESCRIPTION="Agentic AI course materials — 16 modules + references + guides"
EMBEDDING_MODEL="amazon.titan-embed-text-v2:0"

echo "🧠 Creating Bedrock Knowledge Base..."
echo "  Name: $KB_NAME"
echo "  Region: $REGION"
echo "  Data source: s3://$BUCKET"
echo ""

# Step 1: Create the Knowledge Base
# Note: This requires an existing IAM role with Bedrock + S3 + OpenSearch permissions
# The CDK stack (TeachingAgentRAG) creates this role automatically

KB_ROLE_ARN=$(aws iam list-roles --query "Roles[?contains(RoleName, 'TeachingAgentRAG')].Arn | [0]" --output text)

if [ "$KB_ROLE_ARN" == "None" ] || [ -z "$KB_ROLE_ARN" ]; then
    echo "⚠️  KB execution role not found."
    echo "  Deploy CDK first: cd infrastructure && cdk deploy TeachingAgentRAG"
    echo "  Or create via console: Bedrock → Knowledge Bases → Create"
    exit 1
fi

echo "  Role: $KB_ROLE_ARN"
echo ""

# Create KB
KB_RESPONSE=$(aws bedrock-agent create-knowledge-base \
    --name "$KB_NAME" \
    --description "$KB_DESCRIPTION" \
    --role-arn "$KB_ROLE_ARN" \
    --knowledge-base-configuration '{
        "type": "VECTOR",
        "vectorKnowledgeBaseConfiguration": {
            "embeddingModelArn": "arn:aws:bedrock:'$REGION'::foundation-model/'$EMBEDDING_MODEL'"
        }
    }' \
    --storage-configuration '{
        "type": "OPENSEARCH_SERVERLESS",
        "opensearchServerlessConfiguration": {
            "collectionArn": "AUTO_CREATE",
            "vectorIndexName": "teaching-agent-index",
            "fieldMapping": {
                "vectorField": "embedding",
                "textField": "text",
                "metadataField": "metadata"
            }
        }
    }' \
    --region "$REGION" \
    --output json 2>/dev/null)

KB_ID=$(echo "$KB_RESPONSE" | python3 -c "import json,sys; print(json.load(sys.stdin)['knowledgeBase']['knowledgeBaseId'])")

echo "✅ Knowledge Base created: $KB_ID"
echo ""

# Step 2: Add S3 data source
echo "📂 Adding S3 data source..."

DS_RESPONSE=$(aws bedrock-agent create-data-source \
    --knowledge-base-id "$KB_ID" \
    --name "course-materials-s3" \
    --description "Course materials from S3 bucket" \
    --data-source-configuration '{
        "type": "S3",
        "s3Configuration": {
            "bucketArn": "arn:aws:s3:::'$BUCKET'"
        }
    }' \
    --vector-ingestion-configuration '{
        "chunkingConfiguration": {
            "chunkingStrategy": "FIXED_SIZE",
            "fixedSizeChunkingConfiguration": {
                "maxTokens": 500,
                "overlapPercentage": 20
            }
        }
    }' \
    --region "$REGION" \
    --output json 2>/dev/null)

DS_ID=$(echo "$DS_RESPONSE" | python3 -c "import json,sys; print(json.load(sys.stdin)['dataSource']['dataSourceId'])")

echo "✅ Data source added: $DS_ID"
echo ""

# Step 3: Start ingestion sync
echo "🔄 Starting ingestion job..."
aws bedrock-agent start-ingestion-job \
    --knowledge-base-id "$KB_ID" \
    --data-source-id "$DS_ID" \
    --region "$REGION" \
    --output json > /dev/null

echo "✅ Ingestion started!"
echo ""
echo "============================================"
echo "Knowledge Base ID: $KB_ID"
echo "Data Source ID:    $DS_ID"
echo ""
echo "Set this in your environment:"
echo "  export BEDROCK_KB_ID=$KB_ID"
echo ""
echo "Monitor progress:"
echo "  aws bedrock-agent list-ingestion-jobs --knowledge-base-id $KB_ID --data-source-id $DS_ID --region $REGION"
echo ""
echo "Or check the Bedrock Console → Knowledge Bases → $KB_NAME → Data source → Sync history"
