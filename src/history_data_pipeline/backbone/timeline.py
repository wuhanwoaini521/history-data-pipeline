"""Backbone Timeline：Critical/Major 主时间线查询与导出。

- CLI：history-data backbone timeline [--importance x] [--period <period_id/名称>]
- Build：dist/json/china_history_major_timeline.json（供 History UI 首页消费，
  只含 critical + major，按 start_year 升序，不添加 Display-only 字段）
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .loader import Backbone

TIMELINE_FIELDS = (
    "id", "name_zh_cn", "start_year", "end_year", "date_precision",
    "period_id", "regime_ids", "event_type", "importance",
    "summary_zh_cn", "quality_status",
)


def _sort_key(event: dict[str, Any]) -> tuple:
    start = event.get("start_year")
    return (start is None, start if start is not None else 0)


def filter_timeline(backbone: Backbone, importance: set[str] | None = None,
                    period_filter: str | None = None) -> list[dict[str, Any]]:
    """按 importance 集合与 period（id 或名称，宽松匹配）过滤事件，按 start_year 升序。"""
    importance = importance or {"critical", "major"}
    periods = backbone.periods
    matched_period_ids: set[str] | None = None
    if period_filter:
        needle = period_filter
        matched_period_ids = {
            p["id"] for p in periods
            if p["id"] == needle
            or p["id"].startswith("period-" + needle)
            or needle in p["id"]
            or p.get("name_zh_cn") == needle
            or p.get("name_zh_cn", "").startswith(needle)
        }
    events = []
    for event in backbone.events:
        if event.get("importance") not in importance:
            continue
        if matched_period_ids is not None and event.get("period_id") not in matched_period_ids:
            continue
        events.append(event)
    events.sort(key=_sort_key)
    return events


def timeline_record(event: dict[str, Any]) -> dict[str, Any]:
    """导出结构：去掉 loader 内部字段，保持 schema 字段顺序。"""
    return {key: event.get(key) for key in TIMELINE_FIELDS}


def write_major_timeline_json(dist_json: Path, backbone: Backbone, version: str) -> Path:
    """dist/json/china_history_major_timeline.json：critical + major，按 start_year 排序。"""
    dist_json.mkdir(parents=True, exist_ok=True)
    events = filter_timeline(backbone, importance={"critical", "major"})
    document = {
        "version": version,
        "generated_by": "history-data backbone build",
        "source_layer": "layer3_history_backbone",
        "includes": ["critical", "major"],
        "events": [timeline_record(event) for event in events],
    }
    target = dist_json / "china_history_major_timeline.json"
    target.write_text(json.dumps(document, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
    return target