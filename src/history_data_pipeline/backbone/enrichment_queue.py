"""Enrichment Queue：reports/ENRICHMENT_QUEUE.json。

面向产品优先级（可读性 > 事件完整度 > 实体关联度）的补全队列：

    priority_score =
        importance_weight          Critical 40 / Major 25 / Normal 15 / Minor 10
      + missing_count × 4         缺失 9 个维度最多 +36
      + period_weakness (0–10)    所在 Period 的完整率越低越高（Coverage 短板）
      + frontend_visibility(0–10) Critical 事件在首页/概览高亮；Period 主窗口期内的 Critical 再 +5

    priority = Critical(≥70) > Major(≥50) > Normal

只读 curated 数据；数字全部来自真实计算。Q = priority_score 越大越靠前。
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .loader import Backbone, load_backbone
from .product_completeness import DIMENSION_LABELS, event_completeness

IMPORTANCE_WEIGHT = {"critical": 40, "major": 25, "normal": 15, "minor": 10}
IMPORTANCE_RANK = {"critical": 0, "major": 1, "normal": 2, "minor": 3}
MISSING_STEP = 4
CRITICAL_BOUND = 70
MAJOR_BOUND = 50
# 前端默认展示的时期（首页时间线起点）——产品可见性加权。
PRIMARY_PERIOD_IDS = (
    "period-xia", "period-shang", "period-western-zhou",
    "period-spring-autumn", "period-warring-states", "period-qin",
    "period-western-han", "period-eastern-han", "period-three-kingdoms",
    "period-sui", "period-tang", "period-song-liao-jin", "period-yuan",
    "period-ming", "period-qing", "period-republic",
)


def _prioritize(score: float) -> str:
    if score >= CRITICAL_BOUND:
        return "Critical"
    if score >= MAJOR_BOUND:
        return "Major"
    return "Normal"


def build_queue(backbone: Backbone) -> dict[str, Any]:
    """返回 enrichment 队列（含统计与排序后的事件条目）。"""
    period_names = {period["id"]: period.get("name_zh_cn", period["id"]) for period in backbone.periods}

    # 每个 Period 的完整率（用于 period_weakness）
    period_scores: dict[str, list[float]] = {}
    for event in backbone.events:
        row = event_completeness(event)
        period_scores.setdefault(row["period_id"], []).append(row["product_completeness_score"])
    period_weakness = {
        period_id: round((1.0 - (sum(values) / len(values)) / 100.0) * 10, 1)
        for period_id, values in period_scores.items()
    }

    rows: list[dict[str, Any]] = []
    for event in backbone.events:
        row = event_completeness(event)
        period_id = row["period_id"] or "period-unknown"
        importance = row["importance"]
        missing = row["missing"]
        visible = 5 if importance == "critical" else (3 if importance == "major" else 1)
        if period_id in PRIMARY_PERIOD_IDS:
            visible += 5
        weakness = period_weakness.get(period_id, 0.0)
        score = (
            IMPORTANCE_WEIGHT.get(importance, 15)
            + len(missing) * MISSING_STEP
            + weakness
            + visible
        )
        rows.append({
            "event_id": row["event_id"],
            "name_zh_cn": row["name_zh_cn"],
            "importance": importance,
            "period_id": period_id,
            "period_name_zh_cn": period_names.get(period_id, period_id),
            "missing": missing,
            "missing_labels": [DIMENSION_LABELS[key] for key in missing],
            "missing_count": len(missing),
            "score": round(score, 1),
            "product_completeness_score": row["product_completeness_score"],
            "period_weakness": weakness,
            "frontend_visibility": visible,
            "priority": _prioritize(score),
        })

    order = sorted(
        rows,
        key=lambda r: (
            0 if r["priority"] == "Critical" else 1 if r["priority"] == "Major" else 2,
            -r["score"],
            IMPORTANCE_RANK.get(r["importance"], 9),
            r["period_id"],
            r["event_id"],
        ),
    )

    by_priority: dict[str, int] = {"Critical": 0, "Major": 0, "Normal": 0}
    for row in order:
        by_priority[row["priority"]] += 1
    by_importance: dict[str, int] = {}
    for row in order:
        by_importance[row["importance"]] = by_importance.get(row["importance"], 0) + 1

    return {
        "schema": "enrichment-queue-v1",
        "note": "priority = 产品优先级（Critical ≥ 70 > Major ≥ 50 > Normal）；score = importance_weight + 缺失×4 + 时期短板 + 前端可见度。",
        "totals": {
            "events": len(order),
            "by_priority": by_priority,
            "by_importance": by_importance,
        },
        "queue": order,
    }


def write_enrichment_queue(root: Path, backbone: Backbone | None = None) -> Path:
    if backbone is None:
        backbone = load_backbone(root)
    payload = build_queue(backbone)
    reports_dir = root / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    path = reports_dir / "ENRICHMENT_QUEUE.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path