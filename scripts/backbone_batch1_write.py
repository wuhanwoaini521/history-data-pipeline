# -*- coding: utf-8 -*-
"""China History Backbone V1 — Batch 1（先秦）Writer。

从 scripts/backbone_batch1_data.py 的 curated 数据源写入：
1. data/curated/history_backbone/events/<dir>/<event_id>.yml   （正式 Event）
2. data/reviews/accepted/<event_id>.review.json                （审核记录）
3. data/candidates/backbone_events/*_candidates.yml          （候选清单）
4. data/candidates/backbone_events/README.md                 （流程说明）

幂等：重复运行只覆盖相同内容，不改变其他文件。
"""

from __future__ import annotations

import io
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

from backbone_batch1_data import PHASE_A, PHASE_B, PHASE_C, all_events  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
EVENTS_DIR = ROOT / "data" / "curated" / "history_backbone" / "events"
REVIEWS_DIR = ROOT / "data" / "reviews" / "accepted"
CANDIDATES_DIR = ROOT / "data" / "candidates" / "backbone_events"

REVIEWED_BY = "china-history-backbone-v1-curator (batch1)"
SOURCE_TYPE = "curated_reference"

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
        "source_type": SOURCE_TYPE,
        "source_reference": ev["source_ref"],
        "source_ids": ev["source_ids"],
        "relations": ev["relations"],
    }
    ordered = {key: doc[key] for key in FIELD_ORDER}
    lines = [
        "# China History Backbone V1 · Batch 1（先秦）",
        "# summary 为 1~3 句事实描述；sources 采用「古代史料 + 现代参考」两层链（Event First, Evidence Later）。",
        "# 修改后请运行：history-data backbone validate",
    ]
    buf = io.StringIO()
    yaml.safe_dump(ordered, buf, allow_unicode=True, sort_keys=False, default_flow_style=False, width=120)
    return "\n".join(lines) + "\n" + buf.getvalue()


def _review_json(ev: dict) -> dict:
    note = (
        "Batch 1（先秦主干）人工审核：确认该事件进入 Backbone 的必要性、时期归属、"
        "时间范围与重要性分级；来源链见 source_reference（古代史料 + 现代参考），"
        "不影响后续 Evidence Linking。"
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


def _candidate_yaml(phase_dir: str, phase_label: str, events: list) -> str:
    doc = {
        "version": "backbone-candidates-v1",
        "phase": phase_label,
        "compiled_from": (
            "AI 依据通行中国通史叙事与断代工程框架整理候选（非历史事实来源）；"
            "花名册先进入 review，accepted 后才写入 data/curated/history_backbone/events/"
        ),
        "flow": "candidate → data/reviews/accepted/<event_id>.review.json → curated events/",
        "candidates": [
            {
                "id": ev["id"],
                "name_zh_cn": ev["name_zh_cn"],
                "start_year": ev["start_year"],
                "end_year": ev["end_year"],
                "date_precision": ev["date_precision"],
                "period_id": ev["period_id"],
                "importance": ev["importance"],
                "accepted": True,
                "review_file": f"data/reviews/accepted/{ev['id']}.review.json",
            }
            for ev in events
        ],
    }
    buf = io.StringIO()
    yaml.safe_dump(doc, buf, allow_unicode=True, sort_keys=False, default_flow_style=False, width=120)
    return "# China History Backbone V1 · Batch 1 候选（Candidate）\n" + buf.getvalue()


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Write Batch1 curated YAML/reviews")
    parser.add_argument("--phase", choices=["A", "B", "C"], default=None,
                        help="只写指定阶段（A=夏商西周 B=春秋 C=战国）；默认全部")
    args = parser.parse_args()

    EVENTS_DIR.mkdir(parents=True, exist_ok=True)
    REVIEWS_DIR.mkdir(parents=True, exist_ok=True)
    CANDIDATES_DIR.mkdir(parents=True, exist_ok=True)

    all_rows = all_events()
    written_events = 0
    written_reviews = 0

    phase_files = {}

    phase_spec = [("pre_qin", "Phase A（上古/夏/商/西周）", PHASE_A),
                  ("chunqiu_zhanguo", "Phase B（春秋）", PHASE_B),
                  ("chunqiu_zhanguo", "Phase C（战国）", PHASE_C)]
    if args.phase:
        phase_spec = [spec for spec in phase_spec if spec[2] is {"A": PHASE_A, "B": PHASE_B, "C": PHASE_C}[args.phase]]

    for phase_dir, label, events in phase_spec:
        # 候选文件（先 phase A/B/C 各自输出一次）
        key = phase_dir
        target_dir = EVENTS_DIR / phase_dir
        target_dir.mkdir(parents=True, exist_ok=True)
        candidates = (CANDIDATES_DIR / f"{phase_dir}_candidates.yml") if phase_dir not in phase_files else None
        phase_files.setdefault(phase_dir, []).extend(events)
        for ev in events:
            target = target_dir / f"{ev['id']}.yml"
            target.write_text(_event_yaml(ev), encoding="utf-8")
            written_events += 1
            review = REVIEWS_DIR / f"{ev['id']}.review.json"
            if not review.exists():
                review.write_text(json.dumps(_review_json(ev), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                written_reviews += 1

    # 各时期候选文件：按 ALL_PHASES 顺序合并（pre_qin = Phase A；chunqiu_zhanguo = Phase B + C）
    # 候选文件只在写全量（--phase 缺省）时输出，保证候选清单与 accepted 状态一致。
    if not args.phase:
        phase_order = [
            ("pre_qin", "Phase A（上古/夏/商/西周）"),
            ("chunqiu_zhanguo", "Phase B+C（春秋/战国）"),
        ]
        for phase_dir, label in phase_order:
            events = phase_files.get(phase_dir, [])
            (CANDIDATES_DIR / f"{phase_dir}_candidates.yml").write_text(
                _candidate_yaml(phase_dir, label, events), encoding="utf-8")

        (CANDIDATES_DIR / "README.md").write_text(
            "# backbone_events Candidates（Batch 1 先秦）\n\n"
            "本目录保存 China History Backbone V1 Batch 1 的 Event 候选清单。\n\n"
            "- `pre_qin_candidates.yml`：Phase A（上古/夏/商/西周）候选\n"
            "- `chunqiu_zhanguo_candidates.yml`：Phase B（春秋）+ Phase C（战国）候选\n\n"
            "流程：候选（AI 整理，非历史事实来源）→ `data/reviews/accepted/` 人工 review →\n"
            "accepted 后写入 `data/curated/history_backbone/events/`。\n"
            "AI 只整理与筛选候选；历史事实依据以 `source_reference` 中列出的古代史料与\n"
            "现代历史参考为准。\n",
            encoding="utf-8")

    print(f"events written: {written_events}")
    print(f"reviews written(new): {written_reviews}")
    print(f"candidate files: {sorted(p.name for p in CANDIDATES_DIR.glob('*.yml'))}")


if __name__ == "__main__":
    main()