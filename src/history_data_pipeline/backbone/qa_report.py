"""Backbone QA 报告：Duplicate Check + Granularity QA + Timeline Gap Detection。

输出 reports/BACKBONE_REVIEW.md 与 reports/backbone_review.json。

规则：
- Duplicate Check（§21）：按 name/时间/period/event_type 比较，只输出候选对，
  不自动 Merge（不自动删除/合并任何 Event）。
- Granularity QA（§22）：检查长跨度过程事件、aggregate（part_of）结构。
- Timeline Gap Detection（§25）：Critical/Major 时间线明显空白 → coverage_gap，
  但不要为了消灭 Gap 自动制造 Event（此处仅报告）。
"""

from __future__ import annotations

import difflib
import json
import re
from pathlib import Path
from typing import Any

from .loader import Backbone

GROUP_LABELS = {
    "pre_qin": "夏商周",
    "chunqiu_zhanguo": "春秋战国",
    "qin_han": "秦汉",
    "three_kingdoms": "魏晋南北朝（三国）",
    "jin_southern_northern": "魏晋南北朝",
    "sui_tang": "隋唐",
    "five_dynasties": "五代十国",
    "song_liao_xia_jin": "宋辽金夏",
    "yuan": "元",
    "ming": "明",
    "qing": "清",
    "modern": "近现代",
}

GAP_THRESHOLD_YEARS = 150


def _name_ratio(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, a, b).ratio()


_ORDINAL_RE = re.compile(r"第[一二三四五六七八九十百]+[次回合]")


def _is_enumerated_series(a: str, b: str) -> bool:
    """第X次/第X回 枚举型系列（如 第一次党锢之祸/第二次党锢之祸）：
    属刻意分列的不同阶段（§26），不是重复。"""
    stripped_a = _ORDINAL_RE.sub("", a)
    stripped_b = _ORDINAL_RE.sub("", b)
    return stripped_a == stripped_b and stripped_a != "" and stripped_a != a


def duplicate_check(backbone: Backbone) -> list[dict[str, Any]]:
    """输出疑似重复/上下层事件候选对（不自动合并）。

    模型感知：若两事件存在 part_of 父子关系或同属一个 aggregate 的姊妹子事件，
    视为已结构化解释，不重复标记（如 秦灭韩/秦灭赵 均为 秦灭六国 的 part_of 子事件）。
    """
    # 建立 part_of: 子 -> 父 与 父 -> 子集合
    child_of: dict[str, str] = {}
    children_of: dict[str, set[str]] = {}
    for event in backbone.events:
        for relation in event.get("relations", []):
            if relation.get("relation_type") == "part_of":
                child_of[event["id"]] = relation["target_event_id"]
                children_of.setdefault(relation["target_event_id"], set()).add(event["id"])

    def resolved_as_structure(a_id: str, b_id: str) -> bool:
        if child_of.get(a_id) == b_id or child_of.get(b_id) == a_id:
            return True  # 父子关系
        parent_a = child_of.get(a_id)
        parent_b = child_of.get(b_id)
        if parent_a and parent_a == parent_b:
            return True  # 同 aggregate 的姊妹子事件
        return False

    candidates: list[dict[str, Any]] = []
    events = sorted(backbone.events, key=lambda ev: (ev.get("period_id", ""), ev.get("start_year") or 0))
    for i, a in enumerate(events):
        for b in events[i + 1:]:
            if a["id"] == b["id"] or resolved_as_structure(a["id"], b["id"]):
                continue
            same_period = a.get("period_id") == b.get("period_id")
            a_start, b_start = a.get("start_year"), b.get("start_year")
            try:
                nearby = a_start is not None and b_start is not None and abs(a_start - b_start) <= 5
            except TypeError:
                nearby = False
            name_a, name_b = a["name_zh_cn"], b["name_zh_cn"]
            if _is_enumerated_series(name_a, name_b):
                continue  # 第X次枚举系列（如 党锢一/党锢二），刻意分列不视为重复
            contained = (name_a in name_b or name_b in name_a) and name_a != name_b
            ratio = _name_ratio(name_a, name_b)
            if same_period and (contained or (nearby and ratio >= 0.65)):
                candidates.append({
                    "kind": "name_contain_or_similar",
                    "event_a": {"id": a["id"], "name_zh_cn": name_a, "start_year": a_start,
                                "event_type": a.get("event_type"), "importance": a.get("importance")},
                    "event_b": {"id": b["id"], "name_zh_cn": name_b, "start_year": b_start,
                                "event_type": b.get("event_type"), "importance": b.get("importance")},
                    "period_id": a.get("period_id"),
                    "similarity": round(ratio, 2),
                    "note": "可能为同一事件的不同表述或上下层事件（aggregate/子事件）；需人工 review，不自动合并。",
                })
    return candidates


def granularity_check(backbone: Backbone) -> dict[str, Any]:
    """检查事件粒度：长跨度过程事件、aggregate（part_of 结构）、事件类型分布。"""
    aggregates: dict[str, int] = {}
    for event in backbone.events:
        for relation in event.get("relations", []):
            if relation.get("relation_type") == "part_of":
                aggregates.setdefault(relation["target_event_id"], 0)
                aggregates[relation["target_event_id"]] += 1
    long_range: list[dict[str, Any]] = []
    for event in backbone.events:
        precision = event.get("date_precision")
        start, end = event.get("start_year"), event.get("end_year")
        if precision in {"range", "approximate"} and start is not None and end is not None and (end - start) >= 80:
            long_range.append({
                "id": event["id"], "name_zh_cn": event["name_zh_cn"],
                "start_year": start, "end_year": end, "date_precision": precision,
                "note": "长跨度事件（>80 年）：多为阶段性过程/治世节点或宏观格局事件，注意与单点事件粒度区分。",
            })
    type_counts: dict[str, int] = {}
    for event in backbone.events:
        type_counts[event.get("event_type", "?")] = type_counts.get(event.get("event_type", "?"), 0) + 1
    return {
        "aggregates": [
            {"event_id": eid, "part_of_children": count} for eid, count in sorted(aggregates.items(), key=lambda kv: -kv[1])
        ],
        "long_range_events": long_range,
        "event_type_distribution": dict(sorted(type_counts.items(), key=lambda kv: -kv[1])),
    }


def gap_detection(backbone: Backbone, threshold: int = GAP_THRESHOLD_YEARS) -> list[dict[str, Any]]:
    """Critical/Major 时间线空白检测（每 Period 内相邻事件 gap > threshold）。"""
    gaps: list[dict[str, Any]] = []
    for period in backbone.periods:
        period_id = period["id"]
        events = [
            ev for ev in backbone.events
            if ev.get("period_id") == period_id and ev.get("importance") in {"critical", "major"}
            and ev.get("start_year") is not None
        ]
        events.sort(key=lambda ev: ev["start_year"])
        if not events:
            gaps.append({
                "period_id": period_id, "period_name": period.get("name_zh_cn"),
                "kind": "coverage_gap", "severity": "empty",
                "detail": "该 Period 尚无 critical/major Event。",
                "events": 0,
            })
            continue
        p_start, p_end = period.get("start_year"), period.get("end_year")
        span = (p_end - p_start) if (p_start is not None and p_end is not None) else None
        prev = events[0]
        for current in events[1:]:
            gap = current["start_year"] - prev["start_year"]
            if span is not None and gap > threshold and gap > span * 0.25:
                gaps.append({
                    "period_id": period_id, "period_name": period.get("name_zh_cn"),
                    "kind": "coverage_gap", "severity": "gap",
                    "from_event": {"id": prev["id"], "name_zh_cn": prev["name_zh_cn"], "start_year": prev["start_year"]},
                    "to_event": {"id": current["id"], "name_zh_cn": current["name_zh_cn"], "start_year": current["start_year"]},
                    "gap_years": gap,
                    "detail": f"相邻 critical/major 事件间隔 {gap} 年（阈值 {threshold} 年），可能遗漏重要节点；是否补点需人工判断。",
                })
            prev = current
    return gaps


def write_backbone_review(root: Path, backbone: Backbone) -> Path:
    duplicates = duplicate_check(backbone)
    granularity = granularity_check(backbone)
    gaps = gap_detection(backbone)

    review_json = {
        "duplicate_candidates": duplicates,
        "granularity": granularity,
        "coverage_gaps": gaps,
    }
    (root / "reports" / "backbone_review.json").write_text(
        json.dumps(review_json, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# BACKBONE_REVIEW",
        "",
        "> Backbone QA 报告：Duplicate Check + Granularity QA + Timeline Gap Detection。",
        "> 由 `history-data backbone qa --report` 生成；Duplicate 候选不自动合并，Gap 不自动补点。",
        "",
        "## 1. Duplicate Check（候选，不自动 Merge）",
        "",
    ]
    if duplicates:
        lines.append(f"共 {len(duplicates)} 组候选：")
        lines.append("")
        lines.append("| A | B | 类型 | 时间相邻 | 相似度 |")
        lines.append("|---|---|---|---|---:|")
        for item in duplicates:
            a, b = item["event_a"], item["event_b"]
            a_name = f"`{a['name_zh_cn']}`{a['id']}"
            b_name = f"`{b['name_zh_cn']}`{b['id']}"
            lines.append(f"| {a_name} | {b_name} | {item['kind']} | {abs((a['start_year'] or 0) - (b['start_year'] or 0))} 年 | {item['similarity']:.2f} |")
        lines.append("")
        lines.append("> 说明：可能为同一事件的不同表述或上下层事件（aggregate/子事件）；需人工 review。")
    else:
        lines.append("未发现疑似重复/上下层事件候选。")
    lines += [
        "",
        "## 2. Granularity QA",
        "",
        f"- 事件类型分布：{json.dumps(granularity['event_type_distribution'], ensure_ascii=False)}",
        "",
        f"- Aggregate（有子事件 part_of）数量：{len(granularity['aggregates'])}",
    ]
    for item in granularity["aggregates"]:
        lines.append(f"  - {item['event_id']}：{item['part_of_children']} 个子事件")
    lines += ["", "- 长跨度事件（>80 年，需注意与单点事件粒度区分）："]
    if granularity["long_range_events"]:
        for item in granularity["long_range_events"]:
            lines.append(f"  - {item['name_zh_cn']}（{item['id']}）：{item['start_year']}~{item['end_year']} {item['date_precision']}")
    else:
        lines.append("  - 无")
    lines += [
        "",
        "## 3. Timeline Gap Detection",
        "",
        f"- 阈值：相邻 critical/major 事件间隔 > {GAP_THRESHOLD_YEARS} 年（且 > 该 Period 跨度的 25%）",
    ]
    if gaps:
        lines.append(f"- 共 {len(gaps)} 处：")
        lines.append("")
        lines.append("| Period | 类型 | 明细 |")
        lines.append("|---|---|---|")
        for gap in gaps:
            name = gap["period_name"]
            if gap["severity"] == "empty":
                lines.append(f"| {name} | 空白 | {gap['detail']} |")
            else:
                detail = f"{gap['from_event']['name_zh_cn']}（{gap['from_event']['start_year']}）→ {gap['to_event']['name_zh_cn']}（{gap['to_event']['start_year']}）：间隔 {gap['gap_years']} 年。{gap['detail']}"
                lines.append(f"| {name} | 间隔过大 | {detail} |")
        lines.append("")
        lines.append("> 注意：此处仅报告，不自动补造 Event；是否补点由人工依据真实历史粒度判断。")
    else:
        lines.append("- 未发现显著空白。")
    lines += ["", "---", ""]
    target = root / "reports" / "BACKBONE_REVIEW.md"
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return target