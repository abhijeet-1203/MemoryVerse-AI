#input_type_name: GetSessionInput
#output_type_name: GetSessionResult
#function_name: auth_get_session

from pydantic import BaseModel
from lemma_sdk import FunctionContext, Pod
from datetime import datetime, timezone
import hashlib

class GetSessionInput(BaseModel):
    session_token: str

class GetSessionResult(BaseModel):
    valid: bool
    profile_id: str | None = None
    handle: str | None = None
    display_name: str | None = None
    expires_at: str | None = None

async def auth_get_session(ctx: FunctionContext, data: GetSessionInput) -> GetSessionResult:
    pod = Pod.from_env()
    token_hash = hashlib.sha256(data.session_token.encode()).hexdigest()
    rows = pod.records.list("sessions",
        filter=[{"field":"token_hash","op":"eq","value":token_hash}], limit=1).to_dict()["items"]
    if not rows:
        return GetSessionResult(valid=False)
    sess = rows[0]
    if sess.get("is_revoked"):
        return GetSessionResult(valid=False)
    # expire check
    exp = datetime.fromisoformat(sess["expires_at"].replace("Z","+00:00"))
    if exp < datetime.now(timezone.utc):
        return GetSessionResult(valid=False)
    # find the user's profile
    uid = sess.get("user_id")
    if not uid:
        return GetSessionResult(valid=False)
    profiles = pod.records.list("profiles",
        filter=[{"field":"user_id","op":"eq","value":uid}], limit=1).to_dict()["items"]
    if not profiles:
        return GetSessionResult(valid=False)
    prof = profiles[0]
    # update last_used_at
    pod.table("sessions").update(sess["id"], {"last_used_at": datetime.now(timezone.utc).isoformat()})
    return GetSessionResult(
        valid=True, profile_id=str(prof["id"]), handle=prof.get("handle"),
        display_name=prof.get("display_name"), expires_at=sess["expires_at"],
    )
