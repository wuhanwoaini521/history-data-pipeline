"""Depth-sprint 共用工具：按事件替换叙事四段、追加 evidence/relations（去重），保留头部注释。"""
from __future__ import annotations
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
EVENTS = ROOT / "data" / "curated" / "history_backbone" / "events"


def ev(work, term, anchor, tid, field, role, quote, tag, note=""):
    return {
        "work": work, "term": term, "historical_text_id": tid, "chapter_anchor": anchor,
        "claim_field": field, "evidence_role": role, "link_status": "linked",
        "link_method": "manual", "link_confidence": 1.0, "link_quality_status": "reviewed",
        "context_keywords": [],
        "review_note": f"{tag}：{work}源引文：「{quote}」；claim_field={field}；anchor=段落精确锚。{note}",
    }


def apply(event_rel_path: str, patch: dict) -> str:
    path = EVENTS / event_rel_path
    if not path.exists():
        return f"MISSING {event_rel_path}"
    text = path.read_text(encoding="utf-8")
    header = []
    for line in text.splitlines():
        if line.startswith("#") or line.strip() == "":
            header.append(line)
        else:
            break
    d = yaml.safe_load(text)

    for k in ("background_zh_cn", "process_zh_cn", "result_zh_cn", "impact_zh_cn"):
        if k in patch:
            d[k] = patch[k]

    for key in ("people", "places"):
        if key in patch:
            old = d.get(key) or []
            names = {x.get("person_name_raw") or x.get("place_name_raw") for x in old}
            for item in patch[key]:
                nm = item.get("person_name_raw") or item.get("place_name_raw")
                if nm not in names:
                    old.append(item)
                    names.add(nm)
            d[key] = old

    if "evidence" in patch:
        old = d.get("evidence") or []
        seen = {(x.get("historical_text_id"), x.get("claim_field")) for x in old}
        added = 0
        for item in patch["evidence"]:
            key = (item.get("historical_text_id"), item.get("claim_field"))
            if key not in seen:
                old.append(item)
                seen.add(key)
                added += 1
        d["evidence"] = old
    else:
        added = 0

    if "relations" in patch:
        old = d.get("relations") or []
        have = {(r.get("target_event_id"), r.get("relation_type")) for r in old}
        for r in patch["relations"]:
            if (r.get("target_event_id"), r.get("relation_type")) not in have:
                old.append(r)
                have.add((r.get("target_event_id"), r.get("relation_type")))
        d["relations"] = old

    body = yaml.safe_dump(d, allow_unicode=True, sort_keys=False,
                          default_flow_style=False, width=10**6)
    path.write_text("\n".join(header).rstrip("\n") + "\n" + body, encoding="utf-8")
    lens = {k: len(d.get(f"{k}_zh_cn") or "") for k in ("background", "process", "result", "impact")}
    return f"patched {event_rel_path} +{added}ev {lens}"
