"""Course materials management — S3 objects backing the Bedrock Knowledge Base.

Instructor-only operations for the admin "Course Materials" panel:
- list objects in the RAG materials bucket
- generate a presigned URL so the browser can upload large files directly to S3
  (bypassing the API Gateway 10 MB request cap)
- delete an object
- trigger a Knowledge Base ingestion sync so uploads/deletes reach the agent

Configuration comes from environment variables set by the API stack:
- MATERIALS_BUCKET_NAME  — the RAG S3 bucket
- BEDROCK_KB_ID          — the Knowledge Base to sync (with fallback)
"""

import os
from typing import Optional

import boto3
import structlog
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError

logger = structlog.get_logger()

MATERIALS_BUCKET: str = os.environ.get("MATERIALS_BUCKET_NAME", "")
KNOWLEDGE_BASE_ID: str = (
    os.environ.get("BEDROCK_KB_ID", "")
    or os.environ.get("BEDROCK_KNOWLEDGE_BASE_ID", "")
)
REGION: str = os.environ.get("BEDROCK_REGION", os.environ.get("COGNITO_REGION", "eu-west-2"))

# Presigned URLs are valid for this many seconds.
_PRESIGN_TTL = 900  # 15 minutes

# Cap uploads to a sane size for course materials (matches the KB connector's
# 10 GB file cap loosely; we enforce a friendlier 500 MB here).
_MAX_UPLOAD_BYTES = 500 * 1024 * 1024

# Allowed content types for course materials.
_ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "text/plain",
    "text/markdown",
    "text/html",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",  # .docx
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",  # .pptx
    "application/msword",
    "application/octet-stream",
}

# ── boto3 clients (module-level, reused across warm invocations) ──────────────
_s3: Optional[boto3.client] = None
_bedrock_agent: Optional[boto3.client] = None


def _s3_client() -> boto3.client:
    global _s3
    if _s3 is None:
        # SigV4 + regional endpoint so presigned URLs verify correctly.
        _s3 = boto3.client(
            "s3",
            region_name=REGION,
            config=Config(signature_version="s3v4"),
        )
    return _s3


def _bedrock_agent_client() -> boto3.client:
    global _bedrock_agent
    if _bedrock_agent is None:
        _bedrock_agent = boto3.client("bedrock-agent", region_name=REGION)
    return _bedrock_agent


class MaterialsError(Exception):
    """Raised for expected, user-facing materials failures."""

    def __init__(self, message: str, status_code: int = 400) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def _require_bucket() -> str:
    if not MATERIALS_BUCKET:
        raise MaterialsError(
            "Materials bucket is not configured (MATERIALS_BUCKET_NAME unset).",
            status_code=503,
        )
    return MATERIALS_BUCKET


# ── Operations ────────────────────────────────────────────────────────────────


def list_materials(prefix: str = "") -> list[dict]:
    """List objects in the materials bucket.

    Args:
        prefix: Optional key prefix filter (e.g. "modules/").

    Returns:
        List of dicts with ``key``, ``size``, ``last_modified`` (ISO string).
    """
    bucket = _require_bucket()
    s3 = _s3_client()
    items: list[dict] = []

    paginator = s3.get_paginator("list_objects_v2")
    try:
        for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
            for obj in page.get("Contents", []):
                # Skip "folder placeholder" keys.
                if obj["Key"].endswith("/"):
                    continue
                items.append(
                    {
                        "key": obj["Key"],
                        "size": obj["Size"],
                        "last_modified": obj["LastModified"].isoformat(),
                    }
                )
    except (ClientError, BotoCoreError) as exc:
        logger.error("materials_list_failed", error=str(exc))
        raise MaterialsError("Could not list course materials.", status_code=502) from exc

    items.sort(key=lambda i: i["last_modified"], reverse=True)
    logger.info("materials_listed", count=len(items), prefix=prefix)
    return items


def presign_upload(key: str, content_type: str) -> dict:
    """Create a presigned PUT URL for a direct-to-S3 browser upload.

    Args:
        key: Destination object key (validated/sanitized by the caller).
        content_type: MIME type; the client MUST send the same Content-Type.

    Returns:
        Dict with ``url``, ``key``, ``method`` ("PUT"), ``headers``, ``expires_in``.
    """
    bucket = _require_bucket()

    if content_type not in _ALLOWED_CONTENT_TYPES:
        raise MaterialsError(f"Unsupported content type: {content_type}")

    s3 = _s3_client()
    try:
        url = s3.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": bucket,
                "Key": key,
                "ContentType": content_type,
            },
            ExpiresIn=_PRESIGN_TTL,
        )
    except (ClientError, BotoCoreError) as exc:
        logger.error("materials_presign_failed", key=key, error=str(exc))
        raise MaterialsError("Could not create upload URL.", status_code=502) from exc

    logger.info("materials_presigned", key=key, content_type=content_type)
    return {
        "url": url,
        "key": key,
        "method": "PUT",
        "headers": {"Content-Type": content_type},
        "expires_in": _PRESIGN_TTL,
        "max_bytes": _MAX_UPLOAD_BYTES,
    }


def delete_material(key: str) -> dict:
    """Delete an object from the materials bucket.

    The bucket is versioned, so this creates a delete-marker (recoverable).
    """
    bucket = _require_bucket()
    s3 = _s3_client()
    try:
        s3.delete_object(Bucket=bucket, Key=key)
    except (ClientError, BotoCoreError) as exc:
        logger.error("materials_delete_failed", key=key, error=str(exc))
        raise MaterialsError("Could not delete the file.", status_code=502) from exc

    logger.info("material_deleted", key=key)
    return {"key": key, "status": "deleted"}


def sync_knowledge_base() -> dict:
    """Start an ingestion job for every data source on the Knowledge Base.

    Adding/removing S3 objects does not update the KB until it re-ingests.
    We start ingestion on all of the KB's data sources (the setup may have
    more than one) so the agent picks up the latest materials.

    Returns:
        Dict with ``knowledge_base_id`` and a list of started ``jobs``.
    """
    if not KNOWLEDGE_BASE_ID:
        raise MaterialsError(
            "Knowledge Base is not configured (BEDROCK_KB_ID unset).",
            status_code=503,
        )

    agent = _bedrock_agent_client()
    try:
        ds_resp = agent.list_data_sources(knowledgeBaseId=KNOWLEDGE_BASE_ID)
        data_sources = ds_resp.get("dataSourceSummaries", [])
    except (ClientError, BotoCoreError) as exc:
        logger.error("materials_list_ds_failed", error=str(exc))
        raise MaterialsError("Could not list Knowledge Base data sources.", status_code=502) from exc

    if not data_sources:
        raise MaterialsError("No data sources found on the Knowledge Base.", status_code=404)

    jobs: list[dict] = []
    for ds in data_sources:
        ds_id = ds["dataSourceId"]
        try:
            job = agent.start_ingestion_job(
                knowledgeBaseId=KNOWLEDGE_BASE_ID,
                dataSourceId=ds_id,
            )
            jobs.append(
                {
                    "data_source_id": ds_id,
                    "ingestion_job_id": job["ingestionJob"]["ingestionJobId"],
                    "status": job["ingestionJob"]["status"],
                }
            )
        except ClientError as exc:
            code = exc.response.get("Error", {}).get("Code", "")
            # A sync already running for this DS is not a hard failure.
            if code == "ConflictException":
                logger.info("materials_sync_already_running", data_source_id=ds_id)
                jobs.append({"data_source_id": ds_id, "status": "ALREADY_IN_PROGRESS"})
                continue
            logger.error("materials_sync_failed", data_source_id=ds_id, error=str(exc))
            raise MaterialsError("Could not start Knowledge Base sync.", status_code=502) from exc

    logger.info("materials_sync_started", knowledge_base_id=KNOWLEDGE_BASE_ID, jobs=len(jobs))
    return {"knowledge_base_id": KNOWLEDGE_BASE_ID, "jobs": jobs}
