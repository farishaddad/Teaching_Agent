"""Web search augmentation for chat answers.

When a student opts into "Course materials + Web", the chat handler calls
``search_web`` to fetch supplementary results from the open web. Results are
returned in the same chunk shape as Knowledge Base retrieval
(``{text, source, url, score}``) so they can be blended into the same prompt
context and citation list.

Provider: Tavily (https://tavily.com) — a search API optimized for LLM/RAG
use. Each result includes a title, URL, relevance score, and a clean content
snippet, so no HTML scraping is needed.

Configuration:
- ``TAVILY_API_KEY`` — the Tavily API key. If unset, ``search_web`` returns an
  empty list, so the feature degrades gracefully to course-materials-only
  (the chat still works; it simply doesn't add web results).
"""

import os
from typing import Optional

import httpx
import structlog

logger = structlog.get_logger()

TAVILY_API_KEY: str = os.environ.get("TAVILY_API_KEY", "")
_TAVILY_URL = "https://api.tavily.com/search"

# Keep web latency bounded — the Lambda has a 60s budget shared with KB
# retrieval and generation.
_HTTP_TIMEOUT_SECONDS = 8.0

# Cap how much of each result's content we forward into the prompt so a few
# web results don't blow up the token budget.
_MAX_CONTENT_CHARS = 1000


def is_configured() -> bool:
    """Return True if a Tavily API key is available."""
    return bool(TAVILY_API_KEY)


def search_web(query: str, max_results: int = 4) -> list[dict]:
    """Search the web and return chunks compatible with KB retrieval.

    Args:
        query: The student's question (Tavily recommends concise queries).
        max_results: Maximum number of web results to return.

    Returns:
        List of dicts with ``text``, ``source`` (page title), ``url``, and
        ``score`` keys, sorted by relevance (highest first). Returns an empty
        list if no API key is configured or on any error — callers treat an
        empty list as "no web results" and fall back to course materials only.
    """
    if not TAVILY_API_KEY:
        logger.info("web_search_skipped_no_key")
        return []

    log = logger.bind(query_preview=query[:80])

    payload = {
        "query": query[:1500],  # Tavily best practice: keep queries concise.
        "max_results": max_results,
        "search_depth": "advanced",  # Better extraction for factual answers.
        "include_answer": False,     # We generate the answer ourselves via Bedrock.
    }
    headers = {
        "Authorization": f"Bearer {TAVILY_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        response = httpx.post(
            _TAVILY_URL,
            json=payload,
            headers=headers,
            timeout=_HTTP_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        data = response.json()
    except httpx.HTTPError as exc:
        # Network error, timeout, or non-2xx — degrade to KB-only.
        logger.warning("web_search_failed", error=str(exc))
        return []
    except ValueError as exc:  # JSON decode error
        logger.warning("web_search_bad_response", error=str(exc))
        return []

    chunks = _parse_results(data.get("results", []))
    log.info("web_search_complete", results=len(chunks))
    return chunks


def _parse_results(results: list[dict]) -> list[dict]:
    """Normalize Tavily results into the KB chunk shape."""
    chunks: list[dict] = []
    for r in results:
        content = (r.get("content") or "").strip()
        if not content:
            continue
        url = r.get("url", "")
        title = (r.get("title") or url or "Web result").strip()
        chunks.append(
            {
                "text": content[:_MAX_CONTENT_CHARS],
                "source": title,
                "url": url,
                "score": float(r.get("score", 0.0)),
            }
        )

    chunks.sort(key=lambda c: c["score"], reverse=True)
    return chunks
