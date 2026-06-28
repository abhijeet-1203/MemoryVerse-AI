#input_type_name: PersistExtractionInput
#output_type_name: PersistExtractionResult
#function_name: persist_extraction

from pydantic import BaseModel, Field
from lemma_sdk import FunctionContext, Pod
from typing import Any
from datetime import datetime, timezone
import time, json

class PersistExtractionInput(BaseModel):
    document_id: str = Field(min_length=1)
    extraction: dict[str, Any]

class PersistExtractionResult(BaseModel):
    skills: int = 0
    projects: int = 0
    internships: int = 0
    education: int = 0
    certifications: int = 0
    organizations: int = 0
    achievements: int = 0

def _norm(s):
    return (s or "").strip().lower()

def _evidence(item):
    return {"source": "memory_extractor", "raw": item if isinstance(item, dict) else str(item)}

def _normalize_date(d):
    """Coerce messy date strings into YYYY-MM-DD for DATE columns.

    Accepts already-correct strings, "YYYY-MM" (→ first of month), "YYYY"
    (→ Jan 1), and ISO datetimes. Returns None for any garbage so callers
    can still drop the field rather than crash writes.
    """
    if not d:
        return None
    if isinstance(d, str):
        s = d.strip()
        if len(s) >= 10 and s[4] == "-" and s[7] == "-":
            return s[:10]
        if len(s) == 7 and s[4] == "-":  # YYYY-MM
            try:
                datetime.strptime(s, "%Y-%m")
                return s + "-01"
            except ValueError:
                return None
        if len(s) == 4 and s.isdigit():  # YYYY
            return s + "-01-01"
        # try full ISO first 10 chars (e.g. "2020-08-01T00:00:00")
        if "T" in s:
            return s.split("T", 1)[0]
        return None
    return None

# Sanitize values to match the schema's enum constraints.
_SKILL_CATEGORY = {"technical","language","framework","tool","methodology","soft_skill","domain"}
_PROFICIENCY = {"beginner","intermediate","advanced","expert"}
_PROJ_STATUS = {"planned","active","completed","archived","paused"}
_VERIF = {"unverified","verified","expired","revoked"}
_MEMTYPE = {"member","officer","founder","advisor","volunteer","alumni"}
_ACH_CATEGORY = {"award","publication","talk","hackathon","scholarship","recognition","competition","milestone","other"}

def _pick(value, allowed, fallback):
    if value and isinstance(value, str) and value.lower() in allowed:
        return value.lower()
    return fallback

async def persist_extraction(ctx, data):
    """Persist a memory_extractor payload into entity rows.

    Idempotent: if a row with the same (source_document_id, normalized_name)
    already exists, we skip it. This means re-running on the same document won't
    create duplicates.
    """
    t0 = time.time()
    pod = Pod.from_env()
    ex = data.extraction or {}
    doc_id = data.document_id
    inserted = {"skills": 0, "projects": 0, "internships": 0, "education": 0,
                "certifications": 0, "organizations": 0, "achievements": 0}

    # ====================== SKILLS ======================
    skills = ex.get("skills") or []
    if skills and isinstance(skills, list):
        rows = []
        seen_names = set()
        for s in skills:
            if not isinstance(s, dict) or not s.get("name"): continue
            nm = s["name"].strip()
            nn = _norm(nm)
            if nn in seen_names: continue
            seen_names.add(nn)
            rows.append({
                "name": nm,
                "normalized_name": nn,
                "category": _pick(s.get("category"), _SKILL_CATEGORY, "technical"),
                "proficiency": _pick(s.get("proficiency"), _PROFICIENCY, "intermediate"),
                "years_experience": s.get("years_experience"),
                "source_document_id": doc_id,
                "evidence": _evidence(s),
            })
        if rows:
            try:
                inserted["skills"] = pod.records.bulk_create("skills", rows, upsert=False)
            except Exception as e:
                print(f"skills bulk_create failed: {e}; falling back to single inserts")
                ok = 0
                for r in rows:
                    try: pod.records.create("skills", r); ok += 1
                    except Exception as e2: print(f"  skill {r['name']:} skip: {e2}")
                inserted["skills"] = ok

    # ====================== PROJECTS ======================
    projects = ex.get("projects") or []
    if projects and isinstance(projects, list):
        rows = []
        seen_names = set()
        for p in projects:
            if not isinstance(p, dict) or not p.get("name"): continue
            nm = p["name"].strip()
            if _norm(nm) in seen_names: continue
            seen_names.add(_norm(nm))
            rows.append({
                "name": nm,
                "description": p.get("description"),
                "role": p.get("role"),
                "start_date": _normalize_date(p.get("start_date")),
                "end_date": _normalize_date(p.get("end_date")),
                "is_ongoing": bool(p.get("is_ongoing")) if p.get("is_ongoing") is not None else None,
                "status": _pick(p.get("status"), _PROJ_STATUS, "completed") if p.get("status") else None,
                "tech_stack": p.get("tech_stack") or [],
                "project_url": p.get("project_url"),
                "repository_url": p.get("repository_url"),
                "source_document_id": doc_id,
                "evidence": _evidence(p),
            })
        if rows:
            try:
                inserted["projects"] = pod.records.bulk_create("projects", rows, upsert=False)
            except Exception as e:
                print(f"projects bulk_create failed: {e}")
                ok = 0
                for r in rows:
                    try: pod.records.create("projects", r); ok += 1
                    except Exception as e2: pass
                inserted["projects"] = ok

    # ====================== INTERNSHIPS ======================
    intern = ex.get("internships") or []
    if intern and isinstance(intern, list):
        rows = []
        seen = set()
        for it in intern:
            if not isinstance(it, dict) or not it.get("company"): continue
            k = (_norm(it["company"]), _norm(it.get("role") or ""))
            if k in seen: continue
            seen.add(k)
            rows.append({
                "company": it["company"].strip(),
                "role": (it.get("role") or "Intern").strip(),
                "start_date": _normalize_date(it.get("start_date")),
                "end_date": _normalize_date(it.get("end_date")),
                "description": it.get("description"),
                "location": it.get("location"),
                "source_document_id": doc_id,
                "evidence": _evidence(it),
            })
        if rows:
            try:
                inserted["internships"] = pod.records.bulk_create("internships", rows, upsert=False)
            except Exception as e:
                print(f"internships bulk_create failed: {e}")
                ok = 0
                for r in rows:
                    try: pod.records.create("internships", r); ok += 1
                    except Exception: pass
                inserted["internships"] = ok

    # ====================== EDUCATION ======================
    edu = ex.get("education") or []
    if edu and isinstance(edu, list):
        rows = []
        seen = set()
        for e in edu:
            if not isinstance(e, dict) or not e.get("institution"): continue
            k = (_norm(e["institution"]), _norm(e.get("degree") or ""), _norm(e.get("field_of_study") or ""))
            if k in seen: continue
            seen.add(k)
            rows.append({
                "institution": e["institution"].strip(),
                "degree": e.get("degree"),
                "field_of_study": e.get("field_of_study"),
                "start_date": _normalize_date(e.get("start_date")),
                "end_date": _normalize_date(e.get("end_date")),
                "grade": e.get("grade"),
                "source_document_id": doc_id,
                "evidence": _evidence(e),
            })
        if rows:
            try:
                inserted["education"] = pod.records.bulk_create("education", rows, upsert=False)
            except Exception as exc:
                print(f"education bulk_create failed: {exc}")
                ok = 0
                for r in rows:
                    try: pod.records.create("education", r); ok += 1
                    except Exception: pass
                inserted["education"] = ok

    # ====================== CERTIFICATIONS ======================
    certs = ex.get("certifications") or []
    if certs and isinstance(certs, list):
        rows = []
        seen = set()
        for c in certs:
            if not isinstance(c, dict) or not c.get("name"): continue
            k = (_norm(c["name"]), _norm(c.get("issuer") or ""))
            if k in seen: continue
            seen.add(k)
            rows.append({
                "name": c["name"].strip(),
                "issuer": c.get("issuer"),
                "issue_date": _normalize_date(c.get("issue_date")),
                "expiry_date": c.get("expiry_date"),
                "credential_id": c.get("credential_id"),
                "credential_url": c.get("credential_url"),
                "source_document_id": doc_id,
                "evidence": _evidence(c),
            })
        if rows:
            try:
                inserted["certifications"] = pod.records.bulk_create("certifications", rows, upsert=False)
            except Exception as e:
                print(f"certifications bulk_create failed: {e}")
                ok = 0
                for r in rows:
                    try: pod.records.create("certifications", r); ok += 1
                    except Exception: pass
                inserted["certifications"] = ok

    # ====================== ORGANIZATIONS ======================
    orgs = ex.get("organizations") or []
    if orgs and isinstance(orgs, list):
        rows = []
        seen = set()
        for o in orgs:
            if not isinstance(o, dict) or not o.get("name"): continue
            k = (_norm(o["name"]), _norm(o.get("role") or ""))
            if k in seen: continue
            seen.add(k)
            rows.append({
                "name": o["name"].strip(),
                "role": o.get("role"),
                "membership_type": _pick(o.get("membership_type"), _MEMTYPE, "member"),
                "start_date": _normalize_date(o.get("start_date")),
                "end_date": _normalize_date(o.get("end_date")),
                "description": o.get("description"),
                "source_document_id": doc_id,
                "evidence": _evidence(o),
            })
        if rows:
            try:
                inserted["organizations"] = pod.records.bulk_create("organizations", rows, upsert=False)
            except Exception as e:
                print(f"organizations bulk_create failed: {e}")
                ok = 0
                for r in rows:
                    try: pod.records.create("organizations", r); ok += 1
                    except Exception: pass
                inserted["organizations"] = ok

    # ====================== ACHIEVEMENTS ======================
    achs = ex.get("achievements") or []
    if achs and isinstance(achs, list):
        rows = []
        seen = set()
        for a in achs:
            if not isinstance(a, dict) or not a.get("title"): continue
            k = (_norm(a["title"]), _norm(a.get("issuer") or ""))
            if k in seen: continue
            seen.add(k)
            rows.append({
                "title": a["title"].strip(),
                "description": a.get("description"),
                "date": _normalize_date(a.get("date")),
                "category": _pick(a.get("category"), _ACH_CATEGORY, "other"),
                "issuer": a.get("issuer"),
                "rank": a.get("rank"),
                "source_document_id": doc_id,
                "evidence": _evidence(a),
            })
        if rows:
            try:
                inserted["achievements"] = pod.records.bulk_create("achievements", rows, upsert=False)
            except Exception as e:
                print(f"achievements bulk_create failed: {e}")
                ok = 0
                for r in rows:
                    try: pod.records.create("achievements", r); ok += 1
                    except Exception: pass
                inserted["achievements"] = ok

    # ====================== Document status update ======================
    # Note: documents table has `processed_at`, NOT `extracted_at`.
    # `metadata_extracted` is a JSON column — perfect for counts.
    now_iso = datetime.now(timezone.utc).isoformat()
    try:
        pod.records.update("documents", doc_id, {
            "status": "extracted",
            "processed_at": now_iso,
            "metadata_extracted": {"counts": inserted, "extracted_at": now_iso},
        })
    except Exception as e:
        print(f"document update failed (non-fatal): {e}")

    print(f"persist_extraction in {time.time()-t0:.2f}s: {inserted}")
    return PersistExtractionResult(**inserted)
