"""迁移：旧 data/curated/stories.yml（legacy Semantic Layer V1）→ History Backbone。

只迁移已经 QA 确认的数据：
- 26 个 Event → events/<period_dir>/<event_id>.yml（含 EventPerson/EventPlace/
  EventEvidence/EventRelation 独立结构）
- 3 个 Story → stories/<period_dir>/<story_id>.yml（只存 StoryEvent 顺序）

同时保留 legacy 文件不动（标记 legacy），并写出 data/reviews/accepted/ 审核记录。

协议：
- importance 映射：high→major、medium→normal。
- Person：沿用 legacy QA 的 canonical ID（CURATED_PERSON_NAMES），link_status=linked。
- Place：仅 3 个 legacy QA 接受的地点保留 place_id（linked）；其余
  place_id=null + link_status=needs_linking。
- Evidence：保留 historical_text_id + work/term；真实文本语料不在本 checkout，
  link_status=pending_knowledge（legacy QA 已审核，等待知识库重建）。
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ..config import PipelinePaths
from ..backbone.loader import read_yaml, PERIOD_DIR_HINTS
from ..backbone.reference import CANONICAL_PERSON_NAMES

LEGACY_IMPORTANCE = {"high": "major", "medium": "normal"}
ACCEPTED_PLACE_IDS = {"ctext-place-489739", "cbdb-place-14693", "cbdb-place-406333"}
EVIDENCE_ROLE_MAP = {"主要史料": "primary", "相关史料": "supporting"}
LEGACY_SEMANTIC_SOURCE = "source-curated-semantic-v1"
CURATED_SOURCE = "source-curated-backbone-v1"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _importance(value: str | None, default: str = "major") -> str:
    return LEGACY_IMPORTANCE.get(value or "", default)


def _event_period(event: dict[str, Any], story_period_id: str) -> str:
    """为迁移事件选择 Period（legacy 未给事件单独 period_id，按年代推断）。"""
    start = event.get("start_year")
    if start is None:
        return story_period_id
    if start < -770:
        return "period-xia"
    if start < -475:
        return "period-spring-autumn"
    if start < -221:
        return "period-warring-states"
    if start < -206:
        return "period-qin"
    if start <= 8:
        return "period-western-han"
    if start <= 23:
        return "period-xin"
    if start < 220:
        return "period-late-eastern-han"
    if start < 265:
        return "period-three-kingdoms"
    if start < 317:
        return "period-western-jin"
    if start < 420:
        return "period-eastern-jin"
    if start < 581:
        return "period-northern-southern"
    if start < 618:
        return "period-sui"
    if start < 907:
        return "period-tang"
    if start < 960:
        return "period-five-dynasties-ten-kingdoms"
    if start < 1127:
        return "period-northern-song"
    if start < 1279:
        return "period-song-liao-jin"
    if start < 1368:
        return "period-yuan"
    if start < 1644:
        return "period-ming"
    if start < 1912:
        return "period-qing"
    return "period-modern"


def _person_entry(raw: dict[str, Any], event: dict[str, Any]) -> dict[str, Any]:
    person_id = raw.get("person_id")
    name = CANONICAL_PERSON_NAMES.get(person_id) if person_id else None
    entry: dict[str, Any] = {
        "person_id": person_id,
        "person_name_raw": name or raw.get("person_name_raw") or "未知人物",
        "role": raw.get("role", "participant"),
        "role_zh_cn": raw.get("role_zh_cn"),
        "side": raw.get("side"),
        "importance": _importance(raw.get("importance"), "major"),
        "link_status": "linked" if person_id else "needs_linking",
        "link_quality_status": "reviewed" if person_id else None,
        "link_confidence": 0.9 if person_id else None,
        "review_note": f"legacy QA {LEGACY_SEMANTIC_SOURCE} 已确认 canonical identity" if person_id
                       else "无法确认，保留 needs_linking",
    }
    return entry


def _place_entry(raw: dict[str, Any], event: dict[str, Any]) -> dict[str, Any]:
    place_id = raw.get("place_id")
    accepted = place_id in ACCEPTED_PLACE_IDS
    entry: dict[str, Any] = {
        "place_id": place_id if accepted else None,
        "place_name_raw": raw.get("place_name_raw") or "未知地点",
        "role": raw.get("role", "地点"),
        "sequence": raw.get("sequence", 1),
        "description_zh_cn": raw.get("description_zh_cn"),
        "link_status": "linked" if accepted else "needs_linking",
        "link_quality_status": "reviewed" if accepted else None,
        "link_confidence": 0.9 if accepted else None,
        "review_note": None if accepted else (raw.get("description_zh_cn") or "当前知识库无可安全复用地点，保留 needs_linking"),
    }
    return entry


def _evidence_entry(raw: dict[str, Any], event: dict[str, Any]) -> dict[str, Any]:
    role = raw.get("role", "相关史料")
    entry: dict[str, Any] = {
        "historical_text_id": raw.get("historical_text_id"),
        "work": raw.get("work"),
        "term": raw.get("term"),
        "chapter_hint": raw.get("chapter_hint"),
        "context_keywords": raw.get("context_keywords"),
        "evidence_role": EVIDENCE_ROLE_MAP.get(role, "supporting"),
        "link_status": "pending_knowledge",
        "link_quality_status": "reviewed",
        "link_confidence": raw.get("confidence"),
        "review_note": f"legacy QA {LEGACY_SEMANTIC_SOURCE} 已审核（legacy role={role}）；文本语料不在本 checkout，等待知识库重建",
        "rejected_text_ids": raw.get("rejected_text_ids") or [],
    }
    return entry


def _relation_entry(raw: dict[str, Any], source_event_id: str) -> dict[str, Any]:
    return {
        "target_event_id": raw["target_event_id"],
        "relation_type": raw["relation_type"],
        "confidence": raw.get("confidence"),
        "description_zh_cn": raw.get("description_zh_cn"),
    }


def _event_doc(event: dict[str, Any], story: dict[str, Any]) -> dict[str, Any]:
    period_id = _event_period(event, story["period_id"])
    doc: dict[str, Any] = {
        "id": event["id"],
        "name_zh_cn": event["name_zh_cn"],
        "event_type": event.get("event_type", "other"),
        "start_year": event.get("start_year"),
        "end_year": event.get("end_year", event.get("start_year")),
        "date_precision": event.get("date_precision", "year"),
        "period_id": period_id,
        "regime_ids": [],
        "importance": _importance(event.get("importance"), "major"),
        "summary_zh_cn": event.get("summary_zh_cn"),
        "result_zh_cn": event.get("result_zh_cn"),
        "quality_status": "reviewed",
        "source_type": "curated_reference",
        "source_reference": (
            f"迁移自 legacy data/curated/stories.yml（{LEGACY_SEMANTIC_SOURCE}，QA 已确认）；"
            f"原文证据回溯 HistoricalText/NiuTrans Classical-Modern"
        ),
        "people": [_person_entry(item, event) for item in event.get("people", [])],
        "places": [_place_entry(item, event) for item in event.get("places", [])],
        "evidence": [_evidence_entry(item, event) for item in event.get("texts", [])],
        "relations": [_relation_entry(item, event["id"]) for item in event.get("relations", [])],
    }
    return doc


def _story_doc(story: dict[str, Any]) -> dict[str, Any]:
    doc: dict[str, Any] = {
        "id": story["id"],
        "title_zh_cn": story["title_zh_cn"],
        "start_year": story.get("start_year"),
        "end_year": story.get("end_year"),
        "story_type": story.get("story_type", "political-military"),
        "importance": _importance(story.get("importance"), "major"),
        "period_id": story["period_id"],
        "summary_zh_cn": story.get("summary_zh_cn"),
        "background_zh_cn": story.get("background_zh_cn"),
        "result_zh_cn": story.get("result_zh_cn"),
        "quality_status": "reviewed",
        "source_type": "curated_reference",
        "source_reference": f"迁移自 legacy data/curated/stories.yml（{LEGACY_SEMANTIC_SOURCE}，QA 已确认）；顺序为 curated editorial layer",
        "events": [
            {"event_id": event["id"], "sequence": event.get("sequence"),
             "importance": _importance(event.get("importance"), "major"),
             "transition_text_zh_cn": None}
            for event in story.get("events", [])
        ],
    }
    return doc


def _story_period_dir(story: dict[str, Any]) -> str:
    period_id = story.get("period_id", "")
    return PERIOD_DIR_HINTS.get(period_id, "qin_han")


def _write_event_files(paths: PipelinePaths, events: list[dict[str, Any]]) -> list[Path]:
    import yaml

    written: list[Path] = []
    for event in events:
        period_id = event.get("period_id", "pre_qin")
        directory = PERIOD_DIR_HINTS.get(period_id, "pre_qin")
        target = paths.backbone_events / directory / f"{event['id']}.yml"
        target.parent.mkdir(parents=True, exist_ok=True)
        body = {key: value for key, value in event.items() if not key.startswith("_")}
        target.write_text(
            "# 迁移自 legacy data/curated/stories.yml（QA 已确认）。\n"
            "# 修改 Event 请运行：history-data backbone validate\n"
            + yaml.safe_dump(body, allow_unicode=True, sort_keys=False, width=100),
            encoding="utf-8",
        )
        written.append(target)
    return written


def _write_story_files(paths: PipelinePaths, stories: list[dict[str, Any]]) -> list[Path]:
    import yaml

    written: list[Path] = []
    for story in stories:
        directory = _story_period_dir(story)
        target = paths.backbone_stories / directory / f"{story['id']}.yml"
        target.parent.mkdir(parents=True, exist_ok=True)
        body = {key: value for key, value in story.items() if not key.startswith("_")}
        target.write_text(
            "# 迁移自 legacy data/curated/stories.yml（QA 已确认）。\n"
            "# Story 顺序属于 curated editorial layer，允许人工整理。\n"
            + yaml.safe_dump(body, allow_unicode=True, sort_keys=False, width=100),
            encoding="utf-8",
        )
        written.append(target)
    return written


def _write_review_records(paths: PipelinePaths, events: list[dict[str, Any]]) -> list[Path]:
    now = _now()
    written: list[Path] = []
    for event in events:
        record = {
            "schema_version": 1,
            "event_id": event["id"],
            "review_status": "accepted",
            "reviewed_at": now,
            "reviewed_by": "history-data backbone migrate (legacy semantic v1 QA)",
            "decision": "accepted_from_legacy_qa",
            "source": LEGACY_SEMANTIC_SOURCE,
            "people": [
                {"person_id": item.get("person_id"), "person_name_raw": item.get("person_name_raw"),
                 "link_status": item.get("link_status")}
                for item in event.get("people", [])
            ],
            "places": [
                {"place_id": item.get("place_id"), "place_name_raw": item.get("place_name_raw"),
                 "link_status": item.get("link_status")}
                for item in event.get("places", [])
            ],
            "evidence": [
                {"historical_text_id": item.get("historical_text_id"), "work": item.get("work"),
                 "term": item.get("term"), "link_status": item.get("link_status")}
                for item in event.get("evidence", [])
            ],
            "note": "迁移自 legacy Semantic Layer V1 的 QA 结论；不建议直接删除原始 stories.yml。",
        }
        target = paths.data_reviews / "accepted" / f"{event['id']}.review.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        written.append(target)
    return written


def legacy_stories_doc(paths: PipelinePaths) -> dict[str, Any]:
    legacy = paths.root / "data" / "curated" / "stories.yml"
    if not legacy.exists():
        return {}
    return read_yaml(legacy)


def migrate_legacy_curated(paths: PipelinePaths, dry_run: bool = False) -> dict[str, Any]:
    """执行迁移，返回统计。dry_run 只报告不写文件。"""
    legacy = legacy_stories_doc(paths)
    stories_raw = legacy.get("stories", [])
    if not stories_raw:
        raise RuntimeError("data/curated/stories.yml 不存在或无 stories")

    events: list[dict[str, Any]] = []
    story_docs: list[dict[str, Any]] = []
    for story in stories_raw:
        story_docs.append(_story_doc(story))
        for event in story.get("events", []):
            events.append(_event_doc(event, story))
    # story 级 relations（legacy 存于 story.relations，生成目标=相邻 sequence 的上一个事件）
    for story in stories_raw:
        event_by_id = {event["id"]: event for event in story.get("events", [])}
        event_by_seq = {event.get("sequence"): event for event in story.get("events", [])}
        for relation in story.get("relations", []):
            target_event = event_by_id.get(relation["target_event_id"])
            if not target_event:
                continue
            source_event = event_by_seq.get((target_event.get("sequence") or 0) - 1)
            if not source_event:
                continue
            for doc in events:
                if doc["id"] == source_event["id"]:
                    doc["relations"].append(_relation_entry(relation, source_event["id"]))
                    break

    if dry_run:
        return {
            "events": len(events),
            "stories": len(story_docs),
            "written_event_files": 0,
            "written_story_files": 0,
            "written_reviews": 0,
            "dry_run": True,
        }

    event_files = _write_event_files(paths, events)
    story_files = _write_story_files(paths, story_docs)
    review_files = _write_review_records(paths, events)
    return {
        "events": len(events),
        "stories": len(story_docs),
        "written_event_files": len(event_files),
        "written_story_files": len(story_files),
        "written_reviews": len(review_files),
        "dry_run": False,
        "legacy_preserved": True,
        "legacy_note": "data/curated/stories.yml 保留为 legacy/deprecated 审计源，未删除",
    }