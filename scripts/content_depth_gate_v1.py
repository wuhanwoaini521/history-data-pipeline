"""Content Depth Gate V1（audit-only，Queue 4）——透明、可解释、可重复。

不修改 canonical schema；输出 audit-only 状态：STRONG / ADEQUATE / CONTENT_DEPTH_LOW。

评分（12 分制）：
- 每维（background/process/result/impact）：STRONG=2 / ADEQUATE=1 / WEAK=0
  分级规则（确定性）：
    stages = 阶段分隔符计数（。；;：:—），要求段长 >= 6
    STRONG   = len >= 90 且 stages >= 3
    ADEQUATE = len >= 40 且 stages >= 2
    WEAK     = 其余（含空）
- evidence 深度：claim_field 覆盖核心四维数（background/process/result/impact）
    STRONG=2 (>=4) / ADEQUATE=1 (>=3) / WEAK=0 (<=2)
- context：relations 数：STRONG=2 (>=2) / ADEQUATE=1 (1) / WEAK=0 (0)
- 总判：
    STRONG   = total >= 8 且 process >= 1 且 impact >= 1 且 evidence >= 1
    ADEQUATE = total >= 5
    CONTENT_DEPTH_LOW = 其余
仅对 coverage_score == 100 的事件给出上述状态；<100 记 INCOMPLETE。

输出：reports/current-run/content-depth-gate-v1.json + CONTENT_DEPTH_REPORT.md（可重复运行）
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from history_data_pipeline.backbone.product_completeness import event_completeness

SEP = re.compile(r"[。；;：:—]")


def _stages(text: str | None) -> tuple[int, int]:
    if not text or not str(text).strip():
        return 0, 0
    t = str(text).strip()
    return len(t), len([s for s in SEP.split(t) if len(s) >= 6])


def dim_rating(text: str | None) -> str:
    length, stages = _stages(text)
    if length >= 90 and stages >= 3:
        return "STRONG"
    if length >= 40 and stages >= 2:
        return "ADEQUATE"
    return "WEAK"


def score_event(d: dict) -> dict:
    fields = {e.get("claim_field") for e in (d.get("evidence") or []) if e.get("claim_field")}
    core = {"background", "process", "result", "impact"}
    core_hit = len(fields & core)
    ev_rating = "STRONG" if core_hit >= 4 else ("ADEQUATE" if core_hit >= 3 else "WEAK")
    rels = len(d.get("relations") or [])
    ctx_rating = "STRONG" if rels >= 2 else ("ADEQUATE" if rels == 1 else "WEAK")
    dims = {k: dim_rating(d.get(f"{k}_zh_cn")) for k in ("background", "process", "result", "impact")}
    pts = sum(2 if v == "STRONG" else (1 if v == "ADEQUATE" else 0) for v in dims.values())
    pts += 2 if ev_rating == "STRONG" else (1 if ev_rating == "ADEQUATE" else 0)
    pts += 2 if ctx_rating == "STRONG" else (1 if ctx_rating == "ADEQUATE" else 0)
    if pts >= 8 and dims["process"] != "WEAK" and dims["impact"] != "WEAK" and ev_rating != "WEAK":
        status = "STRONG"
    elif pts >= 5:
        status = "ADEQUATE"
    else:
        status = "CONTENT_DEPTH_LOW"
    return {
        "dims": dims, "evidence_rating": ev_rating, "context_rating": ctx_rating,
        "points": pts, "depth_status": status,
        "core_claim_fields": core_hit, "claim_field_count": len(fields),
        "relation_count": rels, "evidence_count": len(d.get("evidence") or []),
    }


def main() -> int:
    rows = []
    for f in (ROOT / "data" / "curated" / "history_backbone" / "events").rglob("event-*.yml"):
        d = yaml.safe_load(f.read_text())
        eid = d.get("id")
        if not eid:
            continue
        c = event_completeness(d)
        r = {"event_id": eid, "name": d.get("name_zh_cn"),
             "period": d.get("period_id"), "coverage_score": c["product_completeness_score"],
             "importance": d.get("importance", "normal")}
        if c["product_completeness_score"] == 100.0:
            r.update(score_event(d))
        else:
            r["depth_status"] = "INCOMPLETE"
        r["missing"] = c["missing"]
        rows.append(r)
    out = ROOT / "reports" / "current-run" / "content-depth-gate-v1.json"
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    from collections import Counter
    cnt = Counter(r["depth_status"] for r in rows)
    print("depth gate v1:", dict(cnt))
    if len(sys.argv) > 1 and sys.argv[1] == "--detail":
        for r in rows:
            if r["depth_status"] == "CONTENT_DEPTH_LOW" and r["coverage_score"] == 100.0:
                print(f"  LOW {r['event_id']} pts={r.get('points')} dims={r.get('dims')} ev={r.get('evidence_rating')} ctx={r.get('context_rating')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
