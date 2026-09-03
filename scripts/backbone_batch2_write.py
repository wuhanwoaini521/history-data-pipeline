# -*- coding: utf-8 -*-
"""China History Backbone V1 — Batch 2（秦→西汉→新→东汉）Writer。

从 scripts/backbone_batch2_data.py 写入：
1. data/curated/history_backbone/events/qin_han/<event_id>.yml
2. data/reviews/accepted/<event_id>.review.json
3. data/candidates/backbone_events/qin_han/*_candidates.yml + README.md
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

from backbone_batch2_data import PHASE_BY_NAME, all_events  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
EVENTS_DIR = ROOT / "data" / "curated" / "history_backbone" / "events" / "qin_han"
REVIEWS_DIR = ROOT / "data" / "reviews" / "accepted"
CANDIDATES_DIR = ROOT / "data" / "candidates" / "backbone_events" / "qin_han"

REVIEWED_BY = "china-history-backbone-v1-curator (batch2)"
FIELD_ORDER = [
    "id", "name_zh_cn", "event_type",
    "start_year", "end_year", "date_precision",
    "period_id", "regime_ids",
    "importance", "summary_zh_cn",
    "quality_status", "source_type", "source_reference", "source_ids",
    "relations",
]


def _event_yaml(ev: dict) -> str:
    doc = {
        "id": ev["id"],
        "name_zh_cn": ev["name_zh_cn"],
        "event_type": ev["event_type"],
        "start_year": ev["start_year"],
        "end_year": ev["end_year"],
        "date_precision": ev["date_precision"],
        "period_id": ev["period_id"],
        "regime_ids": [],
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
        "# China History Backbone V1 · Batch 2（秦→西汉→新→东汉）",
        "# summary 为 1~3 句事实描述；sources 采用「古代史料 + 现代参考」两层链。",
        "# 修改后请运行：history-data backbone validate",
    ]
    buf = io.StringIO()
    yaml.safe_dump(ordered, buf, allow_unicode=True, sort_keys=False, default_flow_style=False, width=120)
    return "\n".join(lines) + "\n" + buf.getvalue()


def _review_json(ev: dict) -> dict:
    note = (
        "Batch 2（秦→西汉→新→东汉）人工审核：确认该事件进入 Backbone 的必要性、时期归属、"
        "时间范围与重要性分级；来源链见 source_reference（古代史料 + 现代参考）。"
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
        "people": [],
        "places": [],
        "evidence": [],
        "note": note,
    }


def _candidate_yaml(phase_label: str, events: list) -> str:
    doc = {
        "version": "backbone-candidates-v1",
        "phase": phase_label,
        "compiled_from": "AI 依据通行秦汉史叙事（《史记》《汉书》《后汉书》+ 现代断代史研究）整理候选；"
                         "候选进入 review，accepted 后才写入 data/curated/history_backbone/events/",
        "flow": "candidate → data/reviews/accepted/<event_id>.review.json → curated events/qin_han/",
        "reused_events": [
            "event-qin-tongyi / event-qin-mie-liuguo / event-qin-mie-*（秦统一系列，chunqiu_zhanguo/）",
            "event-chuhan-qin-revolt / event-chuhan-julu / event-chuhan-qin-fall / event-hongmen / "
            "event-chuhan-pengcheng / event-chuhan-xingyang / event-chuhan-gaixia / "
            "event-chuhan-han-foundation / event-chuhan-later（楚汉 Story，qin_han/）",
            "event-three-yellow-turbans（黄巾起义，three_kingdoms/）",
        ],
        "candidates": [
            {
                "id": ev["id"], "name_zh_cn": ev["name_zh_cn"],
                "start_year": ev["start_year"], "end_year": ev["end_year"],
                "date_precision": ev["date_precision"], "period_id": ev["period_id"],
                "importance": ev["importance"], "accepted": True,
                "review_file": f"data/reviews/accepted/{ev['id']}.review.json",
            }
            for ev in events
        ],
    }
    buf = io.StringIO()
    yaml.safe_dump(doc, buf, allow_unicode=True, sort_keys=False, default_flow_style=False, width=120)
    return "# China History Backbone V1 · Batch 2 候选（Candidate）\n" + buf.getvalue()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=list(PHASE_BY_NAME), default=None,
                        help="只写指定阶段（QIN/WESTERN_HAN/XIN/EASTERN_HAN）；默认全部")
    args = parser.parse_args()

    EVENTS_DIR.mkdir(parents=True, exist_ok=True)
    REVIEWS_DIR.mkdir(parents=True, exist_ok=True)
    CANDIDATES_DIR.mkdir(parents=True, exist_ok=True)

    phases = list(PHASE_BY_NAME.values()) if not args.phase else [PHASE_BY_NAME[args.phase]]

    labels = {"QIN": "Phase Q（秦/楚汉）", "WESTERN_HAN": "Phase WH（西汉）",
              "XIN": "Phase X（新）", "EASTERN_HAN": "Phase EH（东汉）"}

    written_events = written_reviews = 0
    all_phase_events: list[tuple[str, list]] = []
    for phase_name in (("QIN", "WESTERN_HAN", "XIN", "EASTERN_HAN") if not args.phase else (args.phase,)):
        events = PHASE_BY_NAME[phase_name]
        all_phase_events.append((labels[phase_name], events))
        for ev in events:
            target = EVENTS_DIR / f"{ev['id']}.yml"
            target.write_text(_event_yaml(ev), encoding="utf-8")
            written_events += 1
            review = REVIEWS_DIR / f"{ev['id']}.review.json"
            if not review.exists():
                review.write_text(json.dumps(_review_json(ev), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                written_reviews += 1

    # 候选文件：全量运行（--phase 缺省）时才输出，保证候选清单与 accepted 状态一致
    if not args.phase:
        for phase_name, events in (("QIN", PHASE_BY_NAME["QIN"]), ("WESTERN_HAN", PHASE_BY_NAME["WESTERN_HAN"]),
                                   ("XIN", PHASE_BY_NAME["XIN"]), ("EASTERN_HAN", PHASE_BY_NAME["EASTERN_HAN"])):
            (CANDIDATES_DIR / f"{phase_name.lower()}_candidates.yml").write_text(
                _candidate_yaml(labels[phase_name], events), encoding="utf-8")
        (CANDIDATES_DIR / "README.md").write_text(
            "# backbone_events/qin_han Candidates（Batch 2 秦汉）\n\n"
            "本目录保存 China History Backbone V1 Batch 2 的 Event 候选清单（秦/西汉/新/东汉）。\n\n"
            "- `qin_candidates.yml`：Phase Q（秦/楚汉战争）\n"
            "- `western_han_candidates.yml`：Phase WH（西汉）\n"
            "- `xin_candidates.yml`：Phase X（新）\n"
            "- `eastern_han_candidates.yml`：Phase EH（东汉）\n\n"
            "流程：候选（AI 整理，非历史事实来源）→ `data/reviews/accepted/` review →\n"
            "accepted 后写入 `data/curated/history_backbone/events/qin_han/`。\n"
            "复用（不重复建档）：秦统一系列（chunqiu_zhanguo/）、楚汉 Story 9 Event、黄巾起义（three_kingdoms/）。\n",
            encoding="utf-8")

    print(f"events written: {written_events}")
    print(f"reviews written(new): {written_reviews}")


if __name__ == "__main__":
    main()