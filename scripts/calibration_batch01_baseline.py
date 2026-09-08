"""Calibration Batch 01 · Phase 1 — capture baseline metrics for 10 selected events.

For each event, outputs:
  * full 100-pt quality score + per-dimension breakdown (quality.py)
  * source counts (total distinct + independent)
  * evidence count / locator coverage
  * person links (linked vs needs)
  * place links
  * event_relations count
  * completeness fields (background/result/importance present?)
  * verifier state (quality_status)

Outputs:
  reports/calibration_batch01_baseline.json
  reports/calibration_batch01_baseline.md
"""

from __future__ import annotations

import json
from pathlib import Path

from history_data_pipeline.backbone.enrichment import (
    TemporalInventory,
    temporal_conflicts_for_event,
)
from history_data_pipeline.backbone.loader import load_backbone
from history_data_pipeline.backbone.quality import (
    WEIGHTS,
    score_event,
)

ROOT = Path(__file__).resolve().parent.parent
_SELECTION_FILE = ROOT / "reports" / "calibration_batch01_selection.json"
try:
    SELECTION = json.loads(_SELECTION_FILE.read_text(encoding="utf-8"))
except (OSError, json.JSONDecodeError) as exc:
    raise SystemExit(f"无法读取 selection 文件 {_SELECTION_FILE}: {exc}")
OUT_JSON = ROOT / "reports" / "calibration_batch01_baseline.json"
OUT_MD = ROOT / "reports" / "calibration_batch01_baseline.md"

# 学术作者/现代参考关键词 → independent secondary source 计数
INDEPENDENT_AUTHORS = (
    "夏商周断代工程",
    "许倬云",
    "张岂之",
    "童书业",
    "白寿彝",
    "杨宽",
    "翦伯赞",
    "吕思勉",
    "田余庆",
)

# work id → 是否为主干古典文献（source_ids 中的 work-curated-*）
WORK_IDS_PREFIX = "work-curated-"


def main() -> None:
    bb = load_backbone(ROOT)
    inventory = TemporalInventory.from_curated_and_db(ROOT)

    rows = []
    for sel in SELECTION:
        eid = sel["id"]
        ev = bb.event(eid)
        if ev is None:
            raise SystemExit(f"event not found: {eid}")
        per_dims = score_event(
            ev,
            person_years={
                pid: (b, d)
                for pid, (b, d) in inventory.persons.items()
                if b is not None or d is not None
            },
            place_windows=dict(inventory.places),
            temporal_conflicts=temporal_conflicts_for_event(ev, inventory),
        )
        row = {
            "event_id": eid,
            "name_zh_cn": ev.get("name_zh_cn"),
            "quality_score": per_dims["score"],
            "verdict": per_dims["verdict"],
            "dims": {
                name: {
                    "score": per_dims["dims"][name]["score"],
                    "weight": WEIGHTS[name],
                }
                for name in WEIGHTS
            },
            "hard_failures": per_dims["hard_failures"],
            "raw": {
                "quality_status": ev.get("quality_status"),
                "source_type": ev.get("source_type"),
                "source_reference": ev.get("source_reference"),
                "source_count": len(ev.get("source_ids") or []),
                "source_ids": ev.get("source_ids") or [],
                "evidence_count": len(ev.get("evidence") or []),
                "evidence_locator_coverage": sum(
                    1
                    for e in (ev.get("evidence") or [])
                    if e.get("work") and e.get("term")
                )
                / max(1, len(ev.get("evidence") or [])),
                "person_linked": sum(
                    1
                    for p in (ev.get("people") or [])
                    if p.get("link_status") == "linked" and p.get("person_id")
                ),
                "person_total": len(ev.get("people") or []),
                "place_linked": sum(
                    1
                    for p in (ev.get("places") or [])
                    if p.get("link_status") == "linked" and p.get("place_id")
                ),
                "place_total": len(ev.get("places") or []),
                "relation_count": len(ev.get("relations") or []),
                "has_background": bool(ev.get("background_zh_cn")),
                "has_result": bool(ev.get("result_zh_cn")),
                "summary_len": len(ev.get("summary_zh_cn") or ""),
                "importance": ev.get("importance"),
                "independent_secondary_count": sum(
                    1
                    for a in INDEPENDENT_AUTHORS
                    if a in (ev.get("source_reference") or "")
                ),
                "classical_refs": [
                    a
                    for a in ("史记", "汉书", "资治通鉴", "左传", "尚书", "战国策")
                    if a in (ev.get("source_reference") or "")
                ],
            },
        }
        rows.append(row)

    metrics = {
        "batch": "calibration_batch01",
        "baseline": True,
        "n": len(rows),
        "events": rows,
        "agg": {
            "mean_score": round(sum(r["quality_score"] for r in rows) / len(rows), 1),
            "min_score": min(r["quality_score"] for r in rows),
            "max_score": max(r["quality_score"] for r in rows),
            "any_auto_accept": any(r["verdict"] == "AUTO_ACCEPT" for r in rows),
            "evidence_count_total": sum(r["raw"]["evidence_count"] for r in rows),
            "place_total_events_with_places": sum(
                1 for r in rows if r["raw"]["place_total"] > 0
            ),
        },
    }

    OUT_JSON.write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    lines = [
        "# Calibration Batch 01 · Phase 1 — Baseline (BEFORE)",
        "",
        f"- date: {metrics['n']} events selected",
        f"- mean: {metrics['agg']['mean_score']}, min: {metrics['agg']['min_score']}, max: {metrics['agg']['max_score']}",
        f"- AUTO_ACCEPT at baseline: {metrics['agg']['any_auto_accept']}",
        "",
        "| event | score | verdict | source_cnt | evidence | person | place | relations | bg/rslt | complete |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for r in rows:
        re_ = r["raw"]
        bg_rslt = f"{1 if re_['has_background'] else 0}/{1 if re_['has_result'] else 0}"
        lines.append(
            f"| `{r['event_id']}` | {r['quality_score']} | {r['verdict']} "
            f"| {re_['source_count']} | {re_['evidence_count']} "
            f"| {re_['person_linked']}/{re_['person_total']} | {re_['place_linked']}/{re_['place_total']} "
            f"| {re_['relation_count']} | {bg_rslt} "
            f"| {r['dims']['content_completeness']['score']} |"
        )
    lines += ["", "## 每事件 quality_score 组成（dims）", ""]
    for r in rows:
        parts = " ".join(f"{k}={r['dims'][k]['score']}" for k in WEIGHTS)
        lines.append(
            f"- `{r['event_id']}` → **{r['quality_score']}** ({r['verdict']})  |  {parts}"
        )
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("baseline metrics ->", OUT_JSON)
    print("baseline md      ->", OUT_MD)
    for r in rows:
        print(f"{r['event_id']}: {r['quality_score']}  {r['verdict']}")


if __name__ == "__main__":
    main()
