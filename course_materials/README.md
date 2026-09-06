# Course Materials

This directory holds the source documents that back the agent's Retrieval-Augmented
Generation (RAG) Knowledge Base — lecture decks, PDFs, notes, and reference guides.

**These files are intentionally NOT committed to the repository.** Course content is
private (it may include unpublished teaching material and third-party documents), so
everything in this folder except this README is git-ignored.

## What goes here

Drop your own course documents in this folder. Supported formats for Bedrock
Knowledge Base ingestion include:

- `.pdf` — slide decks exported as PDF, handouts
- `.md`, `.txt` — notes, guides
- `.docx` — Word documents
- `.html` — web-based materials
- `.pptx` — PowerPoint decks

## How they reach the agent

1. Place files here (locally).
2. Upload them to the RAG S3 bucket — either:
   - run `scripts/upload_to_s3.sh` (syncs this folder to the materials bucket), or
   - use the admin **Course Materials** panel in the running app (Chapter 8 of the
     tutorial), which uploads directly to S3 via presigned URLs.
3. Trigger a Knowledge Base **Sync** (admin panel button, or re-sync the data source
     in the Bedrock console) so the new content is ingested and searchable.

See the tutorial's [RAG Pipeline](../tutorial/03-rag-pipeline.md) and
[Managing Course Materials](../tutorial/08-course-materials.md) chapters for details.
