# Course Materials — Ingestion Configuration

## Inventory (81 files, 30.3 MB)

| Type | Count | Purpose |
|------|-------|---------|
| PPTX (v3 decks) | 16 | Latest module slide decks — **primary teaching content** |
| PPTX (v2 decks) | 16 | Previous versions — include for completeness |
| Markdown | 39 | Module refreshes, guides, specs, knowledge base content |
| PDF | 5 | Reference frameworks, cheat sheets, whitepapers |
| DOCX | 4 | Master guide, course positioning, supplementary readings |
| HTML | 1 | Course index page |

## Recommended Ingestion Strategy

### For Bedrock Knowledge Base

**Include ALL files** — Bedrock KB handles multi-format ingestion natively (PDF, DOCX, MD, TXT, HTML). PPTX files should be converted to PDF first for better chunking.

### Chunking Configuration
- **Strategy**: Fixed-size chunking
- **Chunk size**: 500 tokens
- **Overlap**: 20% (100 tokens)
- **Rationale**: Course modules have discrete concepts per slide — 500 tokens captures a full concept without being too broad

### Pre-Processing (PPTX → PDF)
Bedrock KB doesn't natively chunk PPTX well. Convert to PDF before upload:
```bash
# Using LibreOffice (headless conversion)
for f in course_materials/*.pptx; do
  libreoffice --headless --convert-to pdf "$f" --outdir course_materials/pdf_exports/
done
```

### S3 Structure
```
s3://teaching-agent-course-materials/
├── modules/            ← Module markdown refreshes (primary)
├── decks_pdf/          ← Converted PPTX → PDF
├── references/         ← PDFs (frameworks, cheat sheets)
├── guides/             ← Master guide, positioning, supplementary
└── meta/               ← Architecture spec, tutor KB, course index
```

## Files to Ingest (Priority Order)

### Tier 1 — Core Content (ingest first, highest retrieval priority)
- `module_*_aug2026_refresh.md` (×16) — Latest module content
- `course_aug2026_master_guide.md` — Full course overview
- `course_tutor_kb.md` — Pre-built knowledge base content

### Tier 2 — Reference Materials
- `agentic-ai-patterns.pdf`
- `AGENTIC AI USE CASE COMPLEXITY FRAMEWORK.pdf`
- `AI Fundamentals Cheat Sheet — Final.pdf`
- `supplementary_reading_agentic_track.md`
- `course_positioning.md`
- `course_update_master_2026.md`

### Tier 3 — Supplementary (include for depth)
- `module_*_update_2026.md` (×16) — Earlier update notes
- `module_*_v3_deck.pptx` → converted to PDF (×16)
- `a-leaders-guide-to-maximizing-the-business-value-of-generative-ai.pdf`
- `The-future-of-enterprise-automation.pdf`
- `build_your_own_ai_tutor_guide.md`
- `avatar_tutor_architecture_spec.md`

### Exclude from RAG (not student-facing)
- `module_*_v2_deck.pptx` — superseded by v3 (keep in repo, skip ingestion)
- `course_2026_index.html` — navigation only, no content value
