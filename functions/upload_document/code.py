#input_type_name: UploadDocumentInput
#output_type_name: UploadDocumentResult
#function_name: upload_document
from pydantic import BaseModel, Field
from lemma_sdk import FunctionContext, Pod
from datetime import datetime, timezone
DOC_STATUS_OPTS = ["pdf","docx","pptx","txt","image","github_link","portfolio_link","other_url","manual"]

class UploadDocumentInput(BaseModel):
    title: str = Field(min_length=1, max_length=240)
    source_type: str = Field(pattern=r"^(pdf|docx|pptx|txt|image|github_link|portfolio_link|other_url|manual)$")
    file_path: str | None = Field(default=None, max_length=700)
    source_url: str | None = None
    mime_type: str | None = Field(default=None, max_length=120)
    size_bytes: int | None = None

class UploadDocumentResult(BaseModel):
    document_id: str

async def upload_document(ctx: FunctionContext, data: UploadDocumentInput) -> UploadDocumentResult:
    pod = Pod.from_env()
    if not data.file_path and not data.source_url:
        raise ValueError("either file_path or source_url must be provided")
    now = datetime.now(timezone.utc).isoformat()
    row = pod.table("documents").create({
        "title": data.title, "source_type": data.source_type,
        "file_path": data.file_path, "source_url": data.source_url,
        "mime_type": data.mime_type, "size_bytes": data.size_bytes,
        "status": "upload_pending", "uploaded_at": now,
    })
    pod.table("audit_logs").create({
        "action":"document_uploaded","subject_type":"document","subject_id": row["id"],
        "metadata":{"title": data.title, "source_type": data.source_type, "file_path": data.file_path},
    })
    return UploadDocumentResult(document_id=str(row["id"]))
