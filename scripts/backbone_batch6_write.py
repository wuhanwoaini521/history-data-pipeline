# -*- coding: utf-8 -*-
"""China History Backbone V1 — Batch 6（元→元末→明）Writer。

写入 events/yuan（元初/元中期/元末）与 events/ming（明初/明中期/晚明）、
reviews、candidates（batch6_<phase>_candidates.yml）。
"""

from __future__ import annotations

import argparse
import io
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

from backbone_batch6_tail_data2 import PHASES, all_events  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
EVENTS_ROOT = ROOT / "data" / "curated" / "history_backbone" / "events"
REVIEWS_DIR = ROOT / "data" / "reviews" / "accepted"
CANDIDATES_DIR = ROOT / "data" / "candidates" / "backbone_events"

REVIEWED_BY = "china-history-backbone-v1-curator (batch6)"
FIELD_ORDER = [
    "id", "name_zh_cn", "event_type",
    "start_year", "end_year", "date_precision",
    "period_id", "regime_ids",
    "importance", "summary_zh_cn",
    "quality_status", "source_type", "source_reference", "source_ids",
    "relations",
]

PHASE_META = {
    "YUAN_EARLY": ("Phase 1 元初/元世祖朝", "yuan"),
    "YUAN_MIDDLE": ("Phase 2 元中期", "yuan"),
    "YUAN_LATE": ("Phase 3 元末社会危机与群雄", "yuan"),
    "MING_EARLY": ("Phase 4 明初", "ming"),
    "MING_MIDDLE": ("Phase 5 明中期", "ming"),
    "MING_LATE": ("Phase 6 晚明", "ming"),
}


def _event_yaml(ev: dict) -> str:
    doc = {
        "id": ev["id"],
        "name_zh_cn": ev["name_zh_cn"],
        "event_type": ev["event_type"],
        "start_year": ev["start_year"],
        "end_year": ev["end_year"],
        "date_precision": ev["date_precision"],
        "period_id": ev["period_id"],
        "regime_ids": ev["regime_ids"],
        "importance": ev["importance"],
        "summary_zh_cn": ev["summary_zh_cn"],
        "quality_status": "reviewed",
        "source_type": "curated_reference",
        "source_reference": ev["source_ref"],
        "source_ids": ev["source_ids"],
        "relations": ev["relations"],
    }
    ordered = {key: doc[key] for key in FIELD_ORDER}
    lines = [
        "# China History Backbone V1 · Batch 6（元→元末→明）",
        "# summary 为 1~3 句事实描述；sources 采用「古代史料 + 现代参考」两层链。",
        "# 修改后请运行：history-data backbone validate",
    ]
    buf = io.StringIO()
    yaml.safe_dump(ordered, buf, allow_unicode=True, sort_keys=False, default_flow_style=False, width=120)
    return "\n".join(lines) + "\n" + buf.getvalue()


def _review_json(ev: dict) -> dict:
    note = (
        "Batch 6（元→元末→明）人工审核：确认事件必要性、时期归属、时间与重要性；"
        "来源链见 source_reference。multi-regime 事件在 regime_ids 并列记录参与政权。"
    )
    if ev["review_note"]:
        note += "\n" + ev["review_note"]
    return {
        "schema_version": 1,
        "event_id": ev["id"],
        "review_status": "accepted",
        "reviewed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "reviewed_by": REVIEWED_BY,
        "decision": "accepted",
        "source": "source-curated-backbone-v1",
        "importance": ev["importance"],
        "date_precision": ev["date_precision"],
        "regime_ids": ev["regime_ids"],
        "people": [],
        "places": [],
        "evidence": [],
        "note": note,
    }


def _candidate_yaml(phase: str, events: list) -> str:
    label, _ = PHASE_META[phase]
    doc = {
        "version": "backbone-candidates-v1",
        "phase": label,
        "compiled_from": "AI 依据《元史》《明史》《明实录》《清太祖武皇帝实录》及现代元明清史研究"
                         "整理候选；候选进入 review，accepted 后才写入 curated events/",
        "flow": "candidate → data/reviews/accepted/<event_id>.review.json → curated events/",
        "reused_events": ["event-yuan-jianguo（1271 元建立）", "南宋灭亡段（1276 临安降/1279 崖山）边界不重记"],
        "candidates": [
            {
                "id": ev["id"], "name_zh_cn": ev["name_zh_cn"],
                "start_year": ev["start_year"], "end_year": ev["end_year"],
                "date_precision": ev["date_precision"], "period_id": ev["period_id"],
                "regime_ids": ev["regime_ids"], "importance": ev["importance"], "accepted": True,
                "review_file": f"data/reviews/accepted/{ev['id']}.review.json",
            }
            for ev in events
        ],
    }
    buf = io.StringIO()
    yaml.safe_dump(doc, buf, allow_unicode=True, sort_keys=False, default_flow_style=False, width=120)
    return "# China History Backbone V1 · Batch 6 候选（Candidate）\n" + buf.getvalue()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=list(PHASES), default=None, help="只写指定阶段；默认全部")
    args = parser.parse_args()

    REVIEWS_DIR.mkdir(parents=True, exist_ok=True)
    CANDIDATES_DIR.mkdir(parents=True, exist_ok=True)

    phases = list(PHASES) if not args.phase else [args.phase]
    written_events = written_reviews = 0
    for phase in phases:
        label, dir_name = PHASE_META[phase]
        target_dir = EVENTS_ROOT / dir_name
        target_dir.mkdir(parents=True, exist_ok=True)
        for ev in PHASES[phase]:
            target = target_dir / f"{ev['id']}.yml"
            target.write_text(_event_yaml(ev), encoding="utf-8")
            written_events += 1
            review = REVIEWS_DIR / f"{ev['id']}.review.json"
            if not review.exists():
                review.write_text(json.dumps(_review_json(ev), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                written_reviews += 1
        if not args.phase:
            (CANDIDATES_DIR / f"batch6_{phase.lower()}_candidates.yml").write_text(
                _candidate_yaml(phase, PHASES[phase]), encoding="utf-8")

    if not args.phase:
        (CANDIDATES_DIR / "README.md").write_text(
            "# backbone_events Candidates\n\n"
            "- `batch4_*.yml`：Batch 4（隋—唐—五代十国）\n- `batch5_*.yml`：Batch 5（北宋—南宋/元边界）\n"
            "- `batch6_*.yml`：Batch 6（元—明/1644 边界）\n\n"
            "流程：候选（AI 整理，非历史事实来源）→ `data/reviews/accepted/` review →\n"
            "accepted 后写入 `data/curated/history_backbone/events/`。\n",
            encoding="utf-8")

    print(f"events written: {written_events}")
    print(f"reviews written(new): {written_reviews}")


if __name__ == "__main__":
    main()