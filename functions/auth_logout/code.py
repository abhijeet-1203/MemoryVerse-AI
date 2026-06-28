#input_type_name: LogoutInput
#output_type_name: LogoutResult
#function_name: auth_logout

from pydantic import BaseModel
from lemma_sdk import FunctionContext, Pod
from datetime import datetime, timezone
import hashlib

class LogoutInput(BaseModel):
    session_token: str

class LogoutResult(BaseModel):
    revoked: bool

async def auth_logout(ctx: FunctionContext, data: LogoutInput) -> LogoutResult:
    pod = Pod.from_env()
    token_hash = hashlib.sha256(data.session_token.encode()).hexdigest()
    rows = pod.records.list("sessions",
        filter=[{"field":"token_hash","op":"eq","value":token_hash}], limit=1).to_dict()["items"]
    if not rows:
        return LogoutResult(revoked=False)
    sess = rows[0]
    pod.table("sessions").update(sess["id"], {
        "is_revoked": True,
        "revoked_at": datetime.now(timezone.utc).isoformat(),
        "revoked_reason": "user_logout",
    })
    pod.table("audit_logs").create({
        "action":"logout","subject_type":"session","subject_id": sess["id"],
    })
    return LogoutResult(revoked=True)
