#input_type_name: ParseDocumentInput
#output_type_name: ParseDocumentResult
#function_name: parse_document
from pydantic import BaseModel, Field
from lemma_sdk import FunctionContext, Pod
from datetime import datetime, timezone

class ParseDocumentInput(BaseModel):
    document_id: str

class ParseDocumentResult(BaseModel):
    text_length: int
    page_count: int | None

async def parse_document(ctx: FunctionContext, data: ParseDocumentInput) -> ParseDocumentResult:
    pod = Pod.from_env()
    doc = pod.table("documents").get(data.document_id)
    fp = doc.get("file_path")
    if not fp:
        # Pure-URL source (GitHub etc.) - no local parsing path for MVP; just mark as reached this stage.
        pod.table("documents").update(doc["id"], {
            "status": "extracted", "text_length": 0,
            "processed_at": datetime.now(timezone.utc).isoformat(),
        })
        return ParseDocumentResult(text_length=0, page_count=0)
    # Read auto-converted markdown for the file.
    md_text = pod.files.download_markdown(fp).decode("utf-8", errors="replace")
    page_count = md_text.count("<!-- page ") if "<!-- page " in md_text else None
    pod.table("documents").update(doc["id"], {
        "raw_text": md_text, "cleaned_text": md_text,
        "text_length": len(md_text), "page_count": page_count,
        "status": "extracted",
        "processed_at": datetime.now(timezone.utc).isoformat(),
        "ocr_used": False,
    })
    pod.table("audit_logs").create({
        "action":"document_extracted","subject_type":"document","subject_id": doc["id"],
        "metadata":{"text_length": len(md_text), "page_count": page_count},
    })
    return ParseDocumentResult(text_length=len(md_text), page_count=page_count)
