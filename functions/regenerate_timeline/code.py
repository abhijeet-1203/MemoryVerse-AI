#input_type_name: RegenerateTimelineInput
#output_type_name: RegenerateTimelineResult
#function_name: regenerate_timeline
from pydantic import BaseModel
from lemma_sdk import FunctionContext, Pod

class RegenerateTimelineInput(BaseModel):
    pass

class RegenerateTimelineResult(BaseModel):
    events_written: int
    events_skipped_no_date: int
    events_skipped_existing: int
    entity_sources: dict


ENTITY_TO_EVENT = {
    "education":      ("education",     "education"),
    "internships":    ("internship",    "internship"),
    "projects":       ("project",       "project"),
    "certifications": ("certification", "certification"),
    "achievements":   ("achievement",   "achievement"),
    "organizations":  ("organization",  "milestone"),
}

DATE_FIELDS = {
    "education":      ["start_date", "end_date"],
    "internships":    ["start_date", "end_date"],
    "projects":       ["start_date", "end_date"],
    "certifications": ["issue_date", "expiry_date"],
    "achievements":   ["date"],
    "organizations":  ["start_date", "end_date"],
}

TITLE_FIELD = {
    "education":      "institution",
    "internships":    "company",
    "projects":       "name",
    "certifications": "name",
    "achievements":   "title",
    "organizations":  "name",
}

SUB_FIELD = {
    "education":      "degree",
    "internships":    "role",
    "projects":       "role",
    "certifications": "issuer",
    "achievements":   "issuer",
    "organizations":  "role",
}


def clean_date(d):
    if not d:
        return None
    if isinstance(d, str) and len(d) >= 10 and d[4] == "-" and d[7] == "-":
        return d[:10]
    return None


async def regenerate_timeline(ctx: FunctionContext, data: RegenerateTimelineInput) -> RegenerateTimelineResult:
    pod = Pod.from_env()
    started = 0
    skipped_no_date = 0
    skipped_existing = 0
    sources = {}

    # Build a set of (table,row_id) we already have events for, so we don't duplicate.
    existing = set()
    try:
        rows = pod.records.list("timeline_events", limit=500).to_dict()["items"]
        for r in rows:
            ev = r.get("evidence") or {}
            if ev.get("table") and ev.get("row_id"):
                existing.add((ev["table"], ev["row_id"]))
        print(f"found {len(existing)} prior timeline events to dedup against")
    except Exception as e:
        print(f"prior list failed (non-fatal): {e}")

    events = []
    for table, (etype, evtype) in ENTITY_TO_EVENT.items():
        try:
            rows = pod.records.list(table, limit=300).to_dict()["items"]
        except Exception as e:
            print(f"list {table} failed: {e}")
            sources[table] = 0
            continue
        sources[table] = len(rows)
        for r in rows:
            if (table, r.get("id")) in existing:
                skipped_existing += 1
                continue
            start = None
            end = None
            for f in DATE_FIELDS.get(table, []):
                v = clean_date(r.get(f))
                if not v: continue
                if start is None: start = v
                elif end is None: end = v
            if start is None and end is None:
                skipped_no_date += 1
                continue
            title = r.get(TITLE_FIELD.get(table)) or "?"
            subtitle_field = SUB_FIELD.get(table)
            subtitle = r.get(subtitle_field) if subtitle_field else None
            title_full = (f"{title} ({subtitle})" if subtitle else title).strip()[:200]
            ev = {
                "title": title_full,
                "event_type": evtype,
                "event_date": start or end,
                "end_date": (end if end and end != start else None),
                "linked_entity_type": etype,
                "linked_entity_id": r.get("id"),
                "source_document_id": r.get("source_document_id"),
                "evidence": {"table": table, "row_id": r.get("id")},
                "is_milestone": bool(r.get("is_ongoing") and not end),
            }
            ev = {k: v for k, v in ev.items() if v is not None and v != ""}
            events.append(ev)

    events.sort(key=lambda e: (e.get("event_date") or "0000-00-00"), reverse=True)

    for i in range(0, len(events), 50):
        chunk = events[i:i + 50]
        try:
            res = pod.records.bulk_create("timeline_events", chunk)
            if isinstance(res, list): started += len(res)
            else: started += res or 0
        except Exception as e:
            print(f"bulk_create failed for {len(chunk)} rows; falling back to per-row: {e}")
            for ev in chunk:
                try:
                    pod.records.create("timeline_events", ev)
                    started += 1
                except Exception as ee:
                    skipped_no_date += 1
                    print(f"  skip {ev.get('title','?')}: {ee}")

    return RegenerateTimelineResult(
        events_written=started,
        events_skipped_no_date=skipped_no_date,
        events_skipped_existing=skipped_existing,
        entity_sources=sources,
    )
