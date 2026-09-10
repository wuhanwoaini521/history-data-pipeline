"""Event Product Completeness（产品完整性不变式）。

以「产品可阅读性」为第一优先级的 9 个维度，回答：这条事件读起来像不像
一个完整的历史知识条目（而不只是占位记录）：

    has_people        人物层：people 列表非空
    has_place         地点层：places 列表非空
    has_source        来源可追溯：source_reference/source_ids 非空
    has_evidence      证据层：evidence 列表非空
    has_related_event 事件关联：relations 列表非空（有前驱/后继/因果）
    has_background    背景叙述：background_zh_cn 非空
    has_process       过程叙述：process_zh_cn 非空（Schema 扩展后字段）
    has_result        结果叙述：result_zh_cn 非空
    has_impact        影响叙述：impact_zh_cn 非空（Schema 扩展后字段）

product_completeness_score = round(100 * fulfilled / 9)。

本模块只读 curated YAML（含 V2.1 并入的 event_person 层），绝不写数据；
确定性（同一条 event 永远得到同一分数），与 quality.py（质量门）职责分离：
quality 打分评估「可信度」，此处评估「产品完整度」。
"""

from __future__ import annotations

from typing import Any

# 维度顺序同时是报告中的展示顺序（不变式，勿改顺序）。
PRODUCT_COMPLETENESS_DIMENSIONS: tuple[str, ...] = (
    "people",
    "place",
    "source",
    "evidence",
    "related_event",
    "background",
    "process",
    "result",
    "impact",
)

DIMENSION_LABELS: dict[str, str] = {
    "people": "人物",
    "place": "地点",
    "source": "来源",
    "evidence": "证据",
    "related_event": "关联事件",
    "background": "背景",
    "process": "过程",
    "result": "结果",
    "impact": "影响",
}


def _filled(value: Any) -> bool:
    if value is None:
        return False
    return bool(str(value).strip())


def dimension_satisfied(event: dict[str, Any], dimension: str) -> bool:
    """单一维度是否满足（确定性、可测试）。"""
    if dimension == "people":
        return bool(event.get("people"))
    if dimension == "place":
        return bool(event.get("places"))
    if dimension == "source":
        reference = str(event.get("source_reference") or "").strip()
        return bool(reference or event.get("source_ids"))
    if dimension == "evidence":
        return bool(event.get("evidence"))
    if dimension == "related_event":
        return bool(event.get("relations"))
    if dimension == "background":
        return _filled(event.get("background_zh_cn"))
    if dimension == "process":
        return _filled(event.get("process_zh_cn"))
    if dimension == "result":
        return _filled(event.get("result_zh_cn"))
    if dimension == "impact":
        return _filled(event.get("impact_zh_cn"))
    raise KeyError(f"unknown completeness dimension: {dimension}")


def event_completeness(event: dict[str, Any]) -> dict[str, Any]:
    """单事件完整度：维度满足矩阵 + product_completeness_score。"""
    satisfied = {
        dimension: dimension_satisfied(event, dimension)
        for dimension in PRODUCT_COMPLETENESS_DIMENSIONS
    }
    fulfilled = sum(1 for value in satisfied.values() if value)
    total = len(PRODUCT_COMPLETENESS_DIMENSIONS)
    return {
        "event_id": event.get("id"),
        "name_zh_cn": event.get("name_zh_cn"),
        "importance": event.get("importance", "normal"),
        "period_id": event.get("period_id"),
        "has": satisfied,
        "missing": [
            dimension
            for dimension in PRODUCT_COMPLETENESS_DIMENSIONS
            if not satisfied[dimension]
        ],
        "fulfilled": fulfilled,
        "total": total,
        "product_completeness_score": round(100.0 * fulfilled / total, 1),
    }


def compute_event_scores(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """批量计算（保持 events 顺序）。"""
    return [event_completeness(event) for event in events]


# Alias exported for callers that prefer the explicit name.
compute_completeness = compute_event_scores