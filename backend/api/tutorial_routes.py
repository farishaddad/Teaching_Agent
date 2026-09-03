"""Tutorial API routes — serves chapter content from the tutorial/ directory."""

import os
from pathlib import Path

import structlog
from fastapi import APIRouter, HTTPException

logger = structlog.get_logger()
router = APIRouter()

# Resolve tutorial directory relative to Lambda task root (/var/task/)
# or relative to the project root for local dev
_env_dir = os.environ.get("TUTORIAL_DIR", "tutorial")
_base = Path("/var/task") if Path("/var/task").exists() else Path(__file__).resolve().parent.parent.parent
TUTORIAL_DIR = _base / _env_dir

CHAPTERS = [
    {"slug": "01-architecture", "title": "Architecture Overview", "estimated_minutes": 15},
    {"slug": "02-authentication", "title": "Setting Up Authentication", "estimated_minutes": 20},
    {"slug": "03-rag-pipeline", "title": "Building the RAG Pipeline", "estimated_minutes": 25},
    {"slug": "04-guardrails", "title": "Implementing Guardrails", "estimated_minutes": 25},
    {"slug": "05-tracking", "title": "Tracking & Analytics", "estimated_minutes": 20},
    {"slug": "06-deployment", "title": "Deployment", "estimated_minutes": 20},
    {"slug": "07-extending", "title": "Extending the Agent", "estimated_minutes": 25},
    {"slug": "08-course-materials", "title": "Managing Course Materials", "estimated_minutes": 15},
]


@router.get("/")
async def list_chapters():
    """List all tutorial chapters with metadata."""
    return {
        "chapters": CHAPTERS,
        "total_chapters": len(CHAPTERS),
        "total_estimated_minutes": sum(c["estimated_minutes"] for c in CHAPTERS),
    }


@router.get("/{slug}")
async def get_chapter(slug: str):
    """Get the markdown content of a specific tutorial chapter."""
    # Validate slug (prevent path traversal)
    if not slug.replace("-", "").replace("_", "").isalnum():
        raise HTTPException(status_code=400, detail="Invalid chapter slug")

    file_path = TUTORIAL_DIR / f"{slug}.md"
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"Chapter '{slug}' not found")

    content = file_path.read_text(encoding="utf-8")

    # Find chapter metadata
    chapter_meta = next((c for c in CHAPTERS if c["slug"] == slug), None)
    chapter_index = next((i for i, c in enumerate(CHAPTERS) if c["slug"] == slug), -1)

    return {
        "slug": slug,
        "title": chapter_meta["title"] if chapter_meta else slug,
        "content": content,
        "estimated_minutes": chapter_meta["estimated_minutes"] if chapter_meta else 0,
        "prev_chapter": CHAPTERS[chapter_index - 1]["slug"] if chapter_index > 0 else None,
        "next_chapter": CHAPTERS[chapter_index + 1]["slug"] if chapter_index < len(CHAPTERS) - 1 else None,
    }
