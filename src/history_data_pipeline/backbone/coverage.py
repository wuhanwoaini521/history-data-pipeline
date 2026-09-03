"""Backbone Coverage 报告：reports/BACKBONE_COVERAGE.md。

按时期组统计 Event/Story 数量，一眼看出哪段历史尚未建设。
同时写出 reports/backbone_coverage.json 供机器读取。
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .build import _coverage_by_group
from .loader import Backbone, PERIOD_DIR_HINTS

GROUP_LABELS: dict[str, str] = {
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


def compute_coverage(backbone: Backbone) -> dict[str, dict[str, int]]:
    coverage: dict[str, dict[str, int]] = {}
    for group, count in _coverage_by_group(backbone).items():
        coverage[group] = {"label": GROUP_LABELS.get(group, group), **count}
    return coverage


def write_backbone_coverage(root: Path, backbone: Backbone | None = None,
                            manifest: dict[str, Any] | None = None) -> Path:
    if backbone is None:
        from .loader import load_backbone
        backbone = load_backbone(root)
    coverage = compute_coverage(backbone)
    reports_dir = root / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    (reports_dir / "backbone_coverage.json").write_text(
        json.dumps(coverage, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    order = ("pre_qin", "chunqiu_zhanguo", "qin_han", "three_kingdoms", "jin_southern_northern",
             "sui_tang", "five_dynasties", "song_liao_xia_jin", "yuan", "ming", "qing", "modern")
    total_events = sum(coverage[group]["events"] for group in order)
    total_stories = sum(coverage[group]["stories"] for group in order)
    lines = [
        "# BACKBONE_COVERAGE",
        "",
        "> History Backbone 覆盖报告：按时期组统计 Event / Story 数量。",
        "> 目标：一眼看出哪段历史尚未建设；后续 China History Backbone V1 阶段按缺口补齐 Major Event 主干。",
        "",
        "## 总览",
        "",
        f"- Period：{len(backbone.periods)}",
        f"- Regime：{len(backbone.regimes)}",
        f"- Event：{total_events}",
        f"- Story：{total_stories}",
        "",
        "## 按时期组",
        "",
        "| 时期组 | Events | Stories |",
        "|---|---:|---:|",
    ]
    for group in order:
        label = GROUP_LABELS.get(group, group)
        lines.append(f"| {label} | {coverage[group]['events']} | {coverage[group]['stories']} |")
    lines += [
        "",
        "## 缺口提示",
        "",
    ]
    empty = [GROUP_LABELS.get(group, group) for group in order if coverage[group]["events"] == 0]
    if empty:
        lines.append(f"- 尚无 Event 的时期组：{', '.join(empty)}。")
        lines.append("- 下一阶段（China History Backbone V1）应优先为这些时期组补齐 critical/major Event。")
    else:
        lines.append("- 所有时期组已有至少 1 个 Event（部分为迁移样例）。")
    lines += [
        "",
        "## 说明",
        "",
        "- 本报告由 `history-data backbone coverage` 或 `history-data backbone build` 生成。",
        "- Event 归属按 events/ 目录约定（PERIOD_DIR_HINTS），可在 taxonomy 调整。",
        "",
    ]
    if manifest:
        lines += ["## 最新 Manifest", "", "```json", json.dumps(manifest.get("counts", {}), ensure_ascii=False, indent=2), "```", ""]
    report = reports_dir / "BACKBONE_COVERAGE.md"
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report