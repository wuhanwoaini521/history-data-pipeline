"""Product Coverage 报告：reports/PRODUCT_COVERAGE.md + reports/product_coverage.json。

衡量「把历史当作可读产品」的成熟度（不是数据总量）：
- 总览：完整条目数/比例 + 平均分；
- 按重要性（含 Critical 高亮行）；
- 按维度满足矩阵；
- 按 Period 聚合：事件数 / 人物% / 地点% / 证据% / 关系% / 完整%；
- Lowest Coverage Periods：完整度最低的时期（改进优先级）。

所有数字来自真实数据（load_backbone + product_completeness），不写死。
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .loader import Backbone, load_backbone
from .product_completeness import (
    DIMENSION_LABELS,
    PRODUCT_COMPLETENESS_DIMENSIONS,
    event_completeness,
)

COMPLETE_THRESHOLD = 90.0
"""product_completeness_score >= 90 才算「完整可读条目」。"""

LOWEST_TOP = 5


def _pct(part: int, whole: int) -> float:
    return round(100.0 * part / whole, 1) if whole else 0.0


def build_product_stats(backbone: Backbone) -> dict[str, Any]:
    """总览 + 按重要性 + 按维度 + 按 Period 聚合（periods 按 taxonomy 顺序）。"""
    scores = [event_completeness(event) for event in backbone.events]
    total = len(scores)
    complete = sum(1 for row in scores if row["product_completeness_score"] >= COMPLETE_THRESHOLD)
    mean = round(sum(row["product_completeness_score"] for row in scores) / total, 1) if total else 0.0

    def holders(dimension: str, rows: list[dict[str, Any]]) -> int:
        return sum(1 for row in rows if row["has"][dimension])

    periods: list[dict[str, Any]] = []
    for period in backbone.periods:
        period_rows = [row for row in scores if row["period_id"] == period["id"]]
        n = len(period_rows)
        periods.append({
            "period_id": period["id"],
            "name_zh_cn": period.get("name_zh_cn", period["id"]),
            "start_year": period.get("start_year"),
            "end_year": period.get("end_year"),
            "events": n,
            "people_pct": _pct(holders("people", period_rows), n),
            "place_pct": _pct(holders("place", period_rows), n),
            "evidence_pct": _pct(holders("evidence", period_rows), n),
            "relation_pct": _pct(holders("related_event", period_rows), n),
            "source_pct": _pct(holders("source", period_rows), n),
            "complete_pct": _pct(
                sum(1 for r in period_rows if r["product_completeness_score"] >= COMPLETE_THRESHOLD),
                n,
            ),
            "mean_score": round(
                sum(r["product_completeness_score"] for r in period_rows) / n, 1
            ) if n else 0.0,
        })

    by_importance: dict[str, dict[str, Any]] = {}
    for row in scores:
        bucket = by_importance.setdefault(
            row["importance"], {"count": 0, "complete": 0, "score_sum": 0.0}
        )
        bucket["count"] += 1
        bucket["score_sum"] += row["product_completeness_score"]
        if row["product_completeness_score"] >= COMPLETE_THRESHOLD:
            bucket["complete"] += 1
    for bucket in by_importance.values():
        bucket["mean"] = round(bucket.pop("score_sum") / bucket["count"], 1) if bucket["count"] else 0.0

    by_dimension = {
        dimension: {
            "label": DIMENSION_LABELS[dimension],
            "count": holders(dimension, scores),
            "pct": _pct(holders(dimension, scores), total),
        }
        for dimension in PRODUCT_COMPLETENESS_DIMENSIONS
    }

    populated = [row for row in periods if row["events"]]
    lowest = sorted(populated, key=lambda row: (row["complete_pct"], -row["events"]))[:LOWEST_TOP]

    return {
        "schema": "product-coverage-v1",
        "dimensions": PRODUCT_COMPLETENESS_DIMENSIONS,
        "threshold": {"complete": COMPLETE_THRESHOLD},
        "total_events": total,
        "complete_events": complete,
        "complete_pct": _pct(complete, total),
        "mean_score": mean,
        "by_importance": by_importance,
        "by_dimension": by_dimension,
        "by_period": periods,
        "lowest_coverage_periods": lowest,
    }


def write_product_coverage(root: Path, backbone: Backbone | None = None) -> tuple[Path, Path]:
    if backbone is None:
        backbone = load_backbone(root)
    stats = build_product_stats(backbone)
    reports_dir = root / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    json_path = reports_dir / "product_coverage.json"
    json_path.write_text(json.dumps(stats, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines: list[str] = [
        "# PRODUCT_COVERAGE",
        "",
        "> History V2 产品完整度报告（可读性优先，非数据总量）。",
        "> 由 `history-data backbone build` / `history-data backbone coverage` 自动生成，数字来自真实数据。",
        "",
        "## 总览",
        "",
        f"- Events：{stats['total_events']}",
        f"- 完整条目（score ≥ {COMPLETE_THRESHOLD:.0f}）：{stats['complete_events']}（{stats['complete_pct']}%）",
        f"- 平均 product_completeness_score：{stats['mean_score']}",
        "",
        "## 按重要性",
        "",
        "| 重要性 | Events | 完整(≥90) | 平均分 |",
        "|---|---:|---:|---:|",
    ]
    for key in ("critical", "major", "normal", "minor"):
        bucket = stats["by_importance"].get(key, {"count": 0, "complete": 0, "mean": 0.0})
        lines.append(f"| {key} | {bucket['count']} | {bucket['complete']} | {bucket['mean']} |")

    lines += [
        "",
        "## 按维度（全部 Events）",
        "",
        "| 维度 | 满足 | 缺失 | 满足率 |",
        "|---|---:|---:|---:|",
    ]
    for dimension in PRODUCT_COMPLETENESS_DIMENSIONS:
        info = stats["by_dimension"][dimension]
        missing = stats["total_events"] - info["count"]
        lines.append(f"| {DIMENSION_LABELS[dimension]} | {info['count']} | {missing} | {info['pct']}% |")

    lines += [
        "",
        "## 按 Period 聚合",
        "",
        "| Period | Events | 人物% | 地点% | 证据% | 关系% | 完整% |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in stats["by_period"]:
        if row["events"] == 0:
            continue
        lines.append(
            f"| {row['name_zh_cn']} | {row['events']} | {row['people_pct']} | {row['place_pct']} | "
            f"{row['evidence_pct']} | {row['relation_pct']} | {row['complete_pct']} |"
        )

    lines += ["", "## Lowest Coverage Periods", ""]
    if stats["lowest_coverage_periods"]:
        lines.append("| Period | Events | 完整% | 平均分 |")
        lines.append("|---|---:|---:|")
        for row in stats["lowest_coverage_periods"]:
            lines.append(f"| {row['name_zh_cn']} | {row['events']} | {row['complete_pct']} | {row['mean_score']} |")
    else:
        lines.append("- 所有时期均完整（理想状态）。")

    lines += [
        "",
        "## 说明",
        "",
        "- 完整条目 = product_completeness_score ≥ 90（9 个产品维度中至少 8.1 个满足）。",
        "- 维度定义（不变式）见 `backbone/product_completeness.py`。",
        "",
    ]
    md_path = reports_dir / "PRODUCT_COVERAGE.md"
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return md_path, json_path