#input_type_name: SetupProfileInput
#output_type_name: SetupProfileResult
#function_name: auth_setup_profile

from pydantic import BaseModel, Field
from lemma_sdk import FunctionContext, Pod
from datetime import datetime, timedelta, timezone
import hashlib, secrets

class SetupProfileInput(BaseModel):
    handle: str = Field(min_length=3, max_length=60, pattern=r"^[a-zA-Z0-9_-]+$")
    display_name: str = Field(min_length=1, max_length=120)
    password: str = Field(min_length=8, max_length=200)
    bio: str | None = None
    headline: str | None = Field(default=None, max_length=240)
    ip_address: str | None = None
    user_agent: str | None = None

class SetupProfileResult(BaseModel):
    session_token: str
    profile_id: str
    handle: str
    expires_at: str

def _hash_pw(password: str) -> tuple[str, str]:
    salt = secrets.token_bytes(16).hex()
    h = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 200_000).hex()
    return h, salt

def _new_token() -> str:
    return secrets.token_urlsafe(48)

async def auth_setup_profile(ctx: FunctionContext, data: SetupProfileInput) -> SetupProfileResult:
    pod = Pod.from_env()
    # Check handle uniqueness (RLS-scoped; this user owns nothing yet so empty list)
    existing = pod.records.list("profiles",
        filter=[{"field":"handle","op":"eq","value":data.handle}], limit=5).to_dict()["items"]
    if existing:
        raise ValueError(f"handle '{data.handle}' is already taken")
    pw_hash, salt = _hash_pw(data.password)
    profile = pod.table("profiles").create({
        "handle": data.handle, "display_name": data.display_name,
        "password_hash": pw_hash, "password_salt": salt,
        "password_set_at": datetime.now(timezone.utc).isoformat(),
        "bio": data.bio, "headline": data.headline,
        "onboarded_at": datetime.now(timezone.utc).isoformat(),
    })
    token = _new_token()
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    now = datetime.now(timezone.utc)
    pod.table("sessions").create({
        "token_hash": token_hash,
        "issued_at": now.isoformat(),
        "expires_at": (now + timedelta(days=30)).isoformat(),
        "last_used_at": now.isoformat(),
        "ip_address": data.ip_address,
        "user_agent": data.user_agent,
    })
    pod.table("audit_logs").create({
        "action": "signup", "subject_type":"profile", "subject_id": profile["id"],
        "ip_address": data.ip_address, "user_agent": data.user_agent,
    })
    return SetupProfileResult(
        session_token=token, profile_id=str(profile["id"]),
        handle=data.handle,
        expires_at=(now + timedelta(days=30)).isoformat(),
    )
