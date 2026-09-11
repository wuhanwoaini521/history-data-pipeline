"""阶段三 · QUARANTINE 事件知识层重打分（knowledge → evidence → event 链路验证）。

对 10 个 QUARANTINE_MEDIUM 候选：
1. 用恢复后的知识层锚定候选 evidence（alias/content 等，语料无覆盖则保持原状）；
2. score_event 前后对照（evidence_precision 因 historical_text_id 实锚 +1.0/条）；
3. 输出 reports/current-run/quarantine-after-knowledge-rebuild.md。

原则：不虚构章节/出处；语料未覆盖的著作保持 needs_linking/QUARANTINE；
若分数仍 <90（AUTO_ACCEPT 阈值），如实保留 QUARANTINE 状态。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from history_data_pipeline.backbone.evidence_link import (  # noqa: E402
    KnowledgeIndex,
    alias_map,
    link_event_evidence,
)
from history_data_pipeline.backbone.loader import load_backbone  # noqa: E402
from history_data_pipeline.backbone.quality import score_event  # noqa: E402
from history_data_pipeline.config import PipelinePaths  # noqa: E402

QUARANTINE_EVENT_IDS = [
    "event-mongol-jianguo",
    "event-western-xia-jianguo",
    "event-yuan-jianguo",
    "event-jiuyiba-shibian",
    "event-nanjing-datusha",
    "event-qiqishi-bian",
    "event-wusi-yundong",
    "event-xian-shibian",
    "event-riben-touxiang",
    "event-xinzhongguo-chengli",
]

DIMENSION_LABELS = {
    "place": "地点", "evidence": "证据", "background": "背景", "process": "过程",
    "result": "结果", "impact": "影响", "people": "人物", "related_event": "关联事件",
    "source": "来源",
}


def find_candidate(root: Path, event_id: str) -> Path | None:
    for batch in sorted((root / "data" / "candidates").glob("batch*")):
        path = batch / f"{event_id}.yml"
        if path.exists():
            return path
    return None


def anchor_candidate(path: Path, index: KnowledgeIndex, aliases: dict, knowledge_db: Path,
                     *, apply: bool) -> tuple[dict, list]:
    import yaml

    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    results = list(link_event_evidence([doc], index, aliases, knowledge_db=knowledge_db))
    if apply:
        for evidence, result in zip(doc.get("evidence", []), results):
            if result.status != "linked":
                continue
            evidence["historical_text_id"] = result.historical_text_id
            evidence["chapter_anchor"] = result.chapter_anchor
            evidence["link_method"] = result.match_method
            evidence["link_status"] = "linked"
            evidence["link_confidence"] = result.confidence
            note = "知识层章节锚定（source_reference normalizer；anchor=章首段）"
            if note not in (evidence.get("review_note") or ""):
                evidence["review_note"] = ((evidence.get("review_note") or "") + "；" + note).strip("；")
        path.write_text(yaml.safe_dump(doc, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return doc, results


def missing_dimensions(event: dict) -> list[str]:
    missing = []
    for key, label in DIMENSION_LABELS.items():
        if key == "place":
            if not event.get("places"):
                missing.append(label)
        elif key == "people":
            if not (event.get("people") or event.get("event_person")):
                missing.append(label)
        elif key == "related_event":
            if not event.get("relations"):
                missing.append(label)
        elif key == "evidence":
            if not event.get("evidence"):
                missing.append(label)
        elif key == "source":
            if not (event.get("source_ids") or event.get("source_reference")):
                missing.append(label)
        else:
            if not event.get(f"{key}_zh_cn"):
                missing.append(label)
    return missing


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    paths = PipelinePaths(root)
    knowledge_db = paths.database
    index = KnowledgeIndex.load(knowledge_db)
    aliases = alias_map(root)

    rows = []
    for event_id in QUARANTINE_EVENT_IDS:
        candidate_path = find_candidate(root, event_id)
        if candidate_path is None:
            rows.append({"event_id": event_id, "error": "候选文件缺失"})
            continue
        original = yaml_load(candidate_path)
        before = score_event(original)
        doc, results = anchor_candidate(candidate_path, index, aliases, knowledge_db, apply=True)
        after = score_event(doc)
        links = [
            {
                "work": r.work, "term": r.term, "status": r.status,
                "method": r.match_method, "anchor": r.chapter_anchor,
                "text_id": r.historical_text_id,
            }
            for r in results
        ]
        rows.append({
            "event_id": event_id,
            "batch": candidate_path.parent.name,
            "before": {"score": before["score"], "verdict": before["verdict"]},
            "after": {"score": after["score"], "verdict": after["verdict"]},
            "evidence_links": links,
            "missing_after": missing_dimensions(doc),
            "gaps": after.get("reasons") or [],
        })

    report_path = root / "reports" / "current-run" / "quarantine-after-knowledge-rebuild.json"
    report_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"written: {report_path}")
    for row in rows:
        if "error" in row:
            print(f"  {row['event_id']}: {row['error']}")
            continue
        print(f"  {row['event_id']} [{row['batch']}]: {row['before']['score']} ({row['before']['verdict']})"
              f" -> {row['after']['score']} ({row['after']['verdict']})")
    return 0


def yaml_load(path: Path) -> dict:
    import yaml
    return yaml.safe_load(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    raise SystemExit(main())
