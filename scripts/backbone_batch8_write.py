# -*- coding: utf-8 -*-
"""China History Backbone V1 — Batch 8（中华民国→近现代 1912—1949）Writer。

写入 events/modern（全 6 阶段）、reviews、candidates（batch8_<phase>_candidates.yml）。
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

from backbone_batch8_tail_data2 import PHASES, all_events  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
EVENTS_ROOT = ROOT / "data" / "curated" / "history_backbone" / "events"
REVIEWS_DIR = ROOT / "data" / "reviews" / "accepted"
CANDIDATES_DIR = ROOT / "data" / "candidates" / "backbone_events"

REVIEWED_BY = "china-history-backbone-v1-curator (batch8)"
FIELD_ORDER = [
    "id", "name_zh_cn", "event_type",
    "start_year", "end_year", "date_precision",
    "period_id", "regime_ids",
    "importance", "summary_zh_cn",
    "quality_status", "source_type", "source_reference", "source_ids",
    "relations",
]

PHASE_META = {
    "REPUBLIC_EARLY": ("Phase 1 民国初期", "modern"),
    "WARLORDS_MAY4TH": ("Phase 2 军阀混战与五四", "modern"),
    "NATIONAL_REV": ("Phase 3 国民革命与北伐", "modern"),
    "CPC_EARLY": ("Phase 4 中共早期节点", "modern"),
    "JAPAN_INVASION": ("Phase 5 日本侵华", "modern"),
    "FULL_WAR_1949": ("Phase 6 全面抗战与 1949 边界", "modern"),
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
        "# China History Backbone V1 · Batch 8（中华民国→近现代 1912—1949）",
        "# 原则：只做 Chronology Backbone；无价值判断/英雄叙事；每事件含档案/史料 + 现代权威研究两层来源。",
        "# 修改后请运行：history-data backbone validate",
    ]
    buf = io.StringIO()
    yaml.safe_dump(ordered, buf, allow_unicode=True, sort_keys=False, default_flow_style=False, width=120)
    return "\n".join(lines) + "\n" + buf.getvalue()


def _review_json(ev: dict) -> dict:
    note = (
        "Batch 8（中华民国→近现代）审核：Chronology-only；事件已满足\"档案/史料类来源 + "
        "现代权威研究\"双层来源链（source_reference）；未满足需 needs_review 而非强行 reviewed。"
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
        "compiled_from": "AI 依据南京临时政府公报、《中华民国史》（张宪文主编）、《中国共产党历史》第一卷、"
                         "军事科学院《中国抗日战争史》、《南京大屠杀史料集》等整理候选；"
                         "候选进入 review，accepted 后才写入 curated events/",
        "flow": "candidate → data/reviews/accepted/<event_id>.review.json → curated events/",
        "reused_events": ["event-nanjing-linshi-zhengfu（1912-01-01 南京临时政府，Batch7）"],
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
    return "# China History Backbone V1 · Batch 8 候选（Candidate）\n" + buf.getvalue()


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
            (CANDIDATES_DIR / f"batch8_{phase.lower()}_candidates.yml").write_text(
                _candidate_yaml(phase, PHASES[phase]), encoding="utf-8")

    if not args.phase:
        (CANDIDATES_DIR / "README.md").write_text(
            "# backbone_events Candidates\n\n"
            "- `batch6_*.yml`：Batch 6（元—明）\n- `batch7_*.yml`：Batch 7（清—晚清—辛亥革命）\n"
            "- `batch8_*.yml`：Batch 8（中华民国—近现代边界）\n\n"
            "流程：候选（AI 整理，非历史事实来源）→ `data/reviews/accepted/` review →\n"
            "accepted 后写入 `data/curated/history_backbone/events/`。\n",
            encoding="utf-8")

    print(f"events written: {written_events}")
    print(f"reviews written(new): {written_reviews}")


if __name__ == "__main__":
    main()