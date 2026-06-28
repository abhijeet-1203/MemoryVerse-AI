#input_type_name: LoginInput
#output_type_name: LoginResult
#function_name: auth_login

from pydantic import BaseModel, Field
from lemma_sdk import FunctionContext, Pod
from datetime import datetime, timedelta, timezone
import hashlib, secrets

class LoginInput(BaseModel):
    handle: str = Field(min_length=3, max_length=60)
    password: str = Field(min_length=1, max_length=200)
    ip_address: str | None = None
    user_agent: str | None = None

class LoginResult(BaseModel):
    session_token: str
    profile_id: str
    handle: str
    expires_at: str

def _new_token() -> str:
    return secrets.token_urlsafe(48)

async def auth_login(ctx: FunctionContext, data: LoginInput) -> LoginResult:
    pod = Pod.from_env()
    rows = pod.records.list("profiles",
        filter=[{"field":"handle","op":"eq","value":data.handle}], limit=5).to_dict()["items"]
    if not rows:
        raise ValueError("invalid handle or password")
    profile = rows[0]
    stored_hash = profile.get("password_hash") or ""
    salt        = profile.get("password_salt") or ""
    if not stored_hash or not salt:
        raise ValueError("invalid handle or password")
    candidate = hashlib.pbkdf2_hmac("sha256", data.password.encode(), salt.encode(), 200_000).hex()
    if not secrets.compare_digest(candidate, stored_hash):
        raise ValueError("invalid handle or password")
    token = _new_token()
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    now = datetime.now(timezone.utc)
    pod.table("sessions").create({
        "token_hash": token_hash,
        "issued_at": now.isoformat(),
        "expires_at": (now + timedelta(days=30)).isoformat(),
        "last_used_at": now.isoformat(),
        "ip_address": data.ip_address, "user_agent": data.user_agent,
    })
    pod.table("audit_logs").create({
        "action":"login","subject_type":"profile","subject_id": profile["id"],
        "ip_address": data.ip_address, "user_agent": data.user_agent,
    })
    return LoginResult(
        session_token=token, profile_id=str(profile["id"]),
        handle=profile["handle"],
        expires_at=(now + timedelta(days=30)).isoformat(),
    )
