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

import boto3
import httpx
import structlog
from botocore.exceptions import BotoCoreError, ClientError

logger = structlog.get_logger()

# The API key is stored in Secrets Manager (referenced by ARN via the
# TAVILY_SECRET_ARN env var set by the API stack). For local development a
# plaintext TAVILY_API_KEY env var is also honoured. The resolved value is
# cached at module level so warm Lambda invocations don't re-fetch the secret.
_TAVILY_SECRET_ARN: str = os.environ.get("TAVILY_SECRET_ARN", "")
_TAVILY_ENV_KEY: str = os.environ.get("TAVILY_API_KEY", "")
_REGION: str = os.environ.get("BEDROCK_REGION", os.environ.get("COGNITO_REGION", "eu-west-2"))

_TAVILY_URL = "https://api.tavily.com/search"

# Cached resolved key. Sentinel ``None`` means "not resolved yet"; empty string
# means "resolved, but no key available".
_cached_key: Optional[str] = None
_secrets_client = None


def _get_secrets_client():
    global _secrets_client
    if _secrets_client is None:
        _secrets_client = boto3.client("secretsmanager", region_name=_REGION)
    return _secrets_client


def _resolve_api_key() -> str:
    """Resolve the Tavily API key (Secrets Manager first, then env), cached.

    Returns an empty string if no key is available, which makes ``search_web``
    degrade gracefully to course-materials-only.
    """
    global _cached_key
    if _cached_key is not None:
        return _cached_key

    # Local-dev / override: plaintext env var wins if set.
    if _TAVILY_ENV_KEY:
        _cached_key = _TAVILY_ENV_KEY
        return _cached_key

    if _TAVILY_SECRET_ARN:
        try:
            resp = _get_secrets_client().get_secret_value(SecretId=_TAVILY_SECRET_ARN)
            _cached_key = (resp.get("SecretString") or "").strip()
        except (ClientError, BotoCoreError) as exc:
            logger.error("tavily_secret_fetch_failed", error=str(exc))
            _cached_key = ""
    else:
        _cached_key = ""

    return _cached_key

# Keep web latency bounded — the Lambda has a 60s budget shared with KB
# retrieval and generation.
_HTTP_TIMEOUT_SECONDS = 8.0

# Cap how much of each result's content we forward into the prompt so a few
# web results don't blow up the token budget.
_MAX_CONTENT_CHARS = 1000


def is_configured() -> bool:
    """Return True if a Tavily API key is available."""
    return bool(_resolve_api_key())


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
    api_key = _resolve_api_key()
    if not api_key:
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
        "Authorization": f"Bearer {api_key}",
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
