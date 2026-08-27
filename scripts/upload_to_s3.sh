#!/bin/bash
# Upload course materials to S3 for Bedrock Knowledge Base ingestion
# Run from the project root: bash scripts/upload_to_s3.sh

set -e

BUCKET="teaching-agent-course-materials"
MATERIALS_DIR="./course_materials"

echo "📚 Teaching Agent — Course Materials Upload"
echo "============================================"
echo "Bucket: s3://$BUCKET"
echo ""

# Check bucket exists
if ! aws s3 ls "s3://$BUCKET" 2>/dev/null; then
    echo "⚠️  Bucket doesn't exist yet. Deploy CDK first: cd infrastructure && cdk deploy TeachingAgentRAG"
    exit 1
fi

# --- Tier 1: Core module content (markdown refreshes) ---
echo "📖 Uploading Tier 1 — Core module content..."
for f in $MATERIALS_DIR/module_*_aug2026_refresh.md; do
    aws s3 cp "$f" "s3://$BUCKET/modules/" --quiet
done
aws s3 cp "$MATERIALS_DIR/course_aug2026_master_guide.md" "s3://$BUCKET/modules/" --quiet
aws s3 cp "$MATERIALS_DIR/course_tutor_kb.md" "s3://$BUCKET/modules/" --quiet
echo "  ✓ 18 core files uploaded"

# --- Tier 2: Reference materials ---
echo "📎 Uploading Tier 2 — Reference materials..."
aws s3 cp "$MATERIALS_DIR/agentic-ai-patterns.pdf" "s3://$BUCKET/references/" --quiet
aws s3 cp "$MATERIALS_DIR/AGENTIC AI USE CASE COMPLEXITY FRAMEWORK.pdf" "s3://$BUCKET/references/" --quiet
aws s3 cp "$MATERIALS_DIR/AI Fundamentals Cheat Sheet — Final.pdf" "s3://$BUCKET/references/" --quiet
aws s3 cp "$MATERIALS_DIR/supplementary_reading_agentic_track.md" "s3://$BUCKET/guides/" --quiet
aws s3 cp "$MATERIALS_DIR/course_positioning.md" "s3://$BUCKET/guides/" --quiet
aws s3 cp "$MATERIALS_DIR/course_update_master_2026.md" "s3://$BUCKET/guides/" --quiet
echo "  ✓ 6 reference files uploaded"

# --- Tier 3: Supplementary ---
echo "📝 Uploading Tier 3 — Supplementary materials..."
for f in $MATERIALS_DIR/module_*_update_2026.md; do
    aws s3 cp "$f" "s3://$BUCKET/guides/" --quiet
done
aws s3 cp "$MATERIALS_DIR/a-leaders-guide-to-maximizing-the-business-value-of-generative-ai.pdf" "s3://$BUCKET/references/" --quiet
aws s3 cp "$MATERIALS_DIR/The-future-of-enterprise-automation.pdf" "s3://$BUCKET/references/" --quiet
aws s3 cp "$MATERIALS_DIR/build_your_own_ai_tutor_guide.md" "s3://$BUCKET/meta/" --quiet
aws s3 cp "$MATERIALS_DIR/avatar_tutor_architecture_spec.md" "s3://$BUCKET/meta/" --quiet
echo "  ✓ 20 supplementary files uploaded"

# --- Convert PPTX to PDF and upload ---
echo ""
echo "🔄 Converting v3 PPTX decks to PDF..."
mkdir -p "$MATERIALS_DIR/pdf_exports"

if command -v libreoffice &> /dev/null; then
    for f in $MATERIALS_DIR/module_*_v3_deck.pptx; do
        libreoffice --headless --convert-to pdf "$f" --outdir "$MATERIALS_DIR/pdf_exports/" 2>/dev/null
    done
    echo "  ✓ 16 decks converted to PDF"
    
    echo "📊 Uploading converted deck PDFs..."
    aws s3 sync "$MATERIALS_DIR/pdf_exports/" "s3://$BUCKET/decks_pdf/" --quiet
    echo "  ✓ Deck PDFs uploaded"
else
    echo "  ⚠️  LibreOffice not found. Skipping PPTX→PDF conversion."
    echo "     Install: brew install --cask libreoffice"
    echo "     Or upload PPTX directly (less optimal chunking):"
    echo "     aws s3 sync $MATERIALS_DIR/ s3://$BUCKET/decks/ --exclude '*' --include '*_v3_deck.pptx'"
fi

echo ""
echo "============================================"
echo "✅ Upload complete! Total files in S3:"
aws s3 ls "s3://$BUCKET" --recursive --summarize | tail -2
echo ""
echo "Next steps:"
echo "  1. Go to Bedrock Console → Knowledge Bases"
echo "  2. Create a new KB pointing to s3://$BUCKET"
echo "  3. Set chunking: Fixed, 500 tokens, 20% overlap"
echo "  4. Embeddings: Amazon Titan Embeddings V2"
echo "  5. Vector store: OpenSearch Serverless (auto-create)"
echo "  6. Click 'Sync' to ingest all materials"
echo ""
echo "  After sync completes, note the Knowledge Base ID"
echo "  and set it as BEDROCK_KB_ID environment variable."
