# Chapter 8: Managing Course Materials

## Keeping the Knowledge Base Fresh — Without Touching AWS

Chapter 3 showed how the RAG pipeline turns your course documents into grounded
answers. But those documents change: you add a new module deck, fix a typo in a
handout, retire an old reading. This chapter covers the **admin Course Materials
panel** — an instructor-only UI to upload, list, and delete the files behind the
Knowledge Base, plus a one-click **Sync** that re-indexes them.

The whole point: an instructor manages course content from the browser, and
never has to open the S3 console or run a CLI command.

```
Instructor → Course Materials panel → S3 (materials bucket) → "Sync" → Bedrock re-ingests → students get updated answers
```

---

## Why Not Just Upload Through the API?

The obvious design is: browser sends the file to the API, the API writes it to
S3. That breaks on real course materials. API Gateway caps a request body at
**10 MB**, and lecture decks and PDFs routinely exceed that.

The fix is **presigned uploads**. The browser asks the backend for a short-lived,
pre-signed S3 URL, then uploads the file **directly to S3** — bypassing API
Gateway entirely.

```
1. Browser → API:  "I want to upload lecture12.pdf (application/pdf)"
2. API → Browser:  a presigned PUT URL (valid ~15 min) + the object key
3. Browser → S3:   PUT the file bytes straight to that URL (no API Gateway)
4. Browser → API:  refresh the list
```

The API never touches the file bytes, so there's no size ceiling beyond S3's own
(and a friendly 500 MB cap we enforce for sanity).

---

## The Backend: `backend/admin/materials.py`

Four instructor-only operations, all reading config from environment variables
(`MATERIALS_BUCKET_NAME`, `BEDROCK_KB_ID`):

```python
def list_materials(prefix: str = "") -> list[dict]:
    """List objects in the materials bucket (key, size, last_modified)."""

def presign_upload(key: str, content_type: str) -> dict:
    """Return a presigned PUT URL so the browser uploads directly to S3."""

def delete_material(key: str) -> dict:
    """Delete an object. The bucket is versioned, so this is recoverable."""

def sync_knowledge_base() -> dict:
    """Start a Bedrock ingestion job for every data source on the KB."""
```

### Presigning an upload

```python
url = s3.generate_presigned_url(
    ClientMethod="put_object",
    Params={"Bucket": bucket, "Key": key, "ContentType": content_type},
    ExpiresIn=900,  # 15 minutes
)
return {"url": url, "key": key, "method": "PUT",
        "headers": {"Content-Type": content_type}, "max_bytes": 500 * 1024 * 1024}
```

The client **must** send the same `Content-Type` header it was signed for, or S3
rejects the PUT with a signature mismatch.

### Sync: re-index without hardcoding a data-source ID

Adding or deleting an S3 object does **nothing** to the Knowledge Base until it
re-ingests. Rather than store a specific data-source ID, we ask the KB what data
sources it has and start an ingestion job for each — so it keeps working even if
the KB is later reconfigured with multiple sources:

```python
def sync_knowledge_base() -> dict:
    agent = boto3.client("bedrock-agent")
    data_sources = agent.list_data_sources(knowledgeBaseId=KB_ID)["dataSourceSummaries"]
    jobs = []
    for ds in data_sources:
        try:
            job = agent.start_ingestion_job(
                knowledgeBaseId=KB_ID, dataSourceId=ds["dataSourceId"]
            )
            jobs.append({"data_source_id": ds["dataSourceId"],
                         "status": job["ingestionJob"]["status"]})
        except ClientError as exc:
            # A sync already running for this source isn't a hard failure.
            if exc.response["Error"]["Code"] == "ConflictException":
                jobs.append({"data_source_id": ds["dataSourceId"],
                             "status": "ALREADY_IN_PROGRESS"})
                continue
            raise
    return {"knowledge_base_id": KB_ID, "jobs": jobs}
```

Ingestion runs in the background and takes a few minutes, so the endpoint returns
as soon as the jobs are *started* — it doesn't block until indexing finishes.

---

## The Routes: `backend/admin/routes.py`

All four are gated by the `require_instructor` dependency (Chapter 2's group
check), so students can't reach them:

```python
@router.get("/materials",          ...)  # list
@router.post("/materials/presign", ...)  # get an upload URL
@router.delete("/materials/{key:path}")  # delete (key may contain slashes)
@router.post("/materials/sync")           # re-index the KB
```

Uploaded filenames are sanitised into safe S3 keys (stripping unsafe characters
and prefixing a short unique id) so a student-supplied name can't traverse paths
or collide.

---

## The Infrastructure: permissions

The API Lambda needs S3 access on the materials bucket and permission to trigger
ingestion. In `infrastructure/api_stack.py`:

```python
# S3: list / get / put / delete on the materials bucket + its objects
materials_bucket.grant_read_write(self.api_lambda)

# Bedrock: ingestion control for the Sync button
self.api_lambda.add_to_role_policy(iam.PolicyStatement(
    actions=[
        "bedrock:ListDataSources",
        "bedrock:StartIngestionJob",
        "bedrock:GetIngestionJob",
        "bedrock:ListIngestionJobs",
        # ...plus the existing InvokeModel/Retrieve/Converse/ApplyGuardrail
    ],
    resources=["*"],
))
```

The bucket name is passed to the Lambda as `MATERIALS_BUCKET_NAME`. Because the
bucket lives in the RAG stack, wiring it into the API stack creates a cross-stack
dependency — deploy the RAG stack (which exports the bucket) before the API stack.

---

## The Frontend: `MaterialsList.tsx`

A new **Course Materials** tab in the admin panel. It uses React Query to load the
list, and three actions:

```typescript
// Upload: presign, then PUT the file straight to S3 (no credentials on the PUT)
export async function uploadMaterial(file: File): Promise<{ key: string }> {
  const presign = await adminFetch('/materials/presign', {
    method: 'POST',
    body: JSON.stringify({ filename: file.name, content_type: file.type }),
  });
  await fetch(presign.url, {              // direct to S3
    method: 'PUT',
    headers: presign.headers,             // must include the signed Content-Type
    body: file,
  });
  return { key: presign.key };
}
```

The table shows each file's key, size, and last-modified date, with a
confirm-guarded **Delete**, an **Upload File** button, and a **Sync Knowledge
Base** button. Because the bucket is versioned, a deleted file is recoverable —
delete creates a delete-marker rather than erasing history.

---

## The Instructor Workflow

Putting it together, updating course content is three clicks:

1. **Upload** the new or revised file (goes straight to S3 via the presigned URL).
2. **Delete** anything that's been retired.
3. **Sync Knowledge Base** — starts ingestion so the new content is embedded and
   searchable.

Wait a couple of minutes for ingestion to finish, then ask the agent a question
about the new material. Because retrieval is grounded (Chapter 3), the answer now
reflects the updated content — and cites it.

> ⚠️ **The #1 pitfall**: uploading a file and forgetting to Sync. The file is in
> S3, but the Knowledge Base won't return it until ingestion runs. If a student
> says "the agent doesn't know about the new module," check that Sync was run and
> that the ingestion job completed.

---

## What You Learned

- Why large uploads use **presigned PUT** (browser → S3 directly) instead of
  routing bytes through API Gateway's 10 MB limit.
- How the **Sync** button triggers Bedrock ingestion across all KB data sources
  without hardcoding an ID.
- The IAM the API Lambda needs (`grant_read_write` on the bucket + Bedrock
  ingestion actions) and the RAG→API cross-stack dependency.
- That the bucket is **versioned**, so deletes are recoverable.

Next: [Extending the Agent](./07-extending.md) — tool use, multi-agent patterns,
and pulling in **live web results** to complement the course materials.
