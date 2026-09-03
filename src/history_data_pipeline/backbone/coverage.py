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


def _event_in_batch(root: Path, event_id: str, batch: str) -> bool:
    """provenance：本批（batch4…）新增事件由 review 文件 reviewed_by 标识。"""
    review_file = root / "data" / "reviews" / "accepted" / f"{event_id}.review.json"
    if not review_file.exists():
        return False
    try:
        import json
        doc = json.loads(review_file.read_text(encoding="utf-8"))
        return batch in (doc.get("reviewed_by") or "")
    except Exception:
        return False


def compute_importance_by_period(backbone: Backbone, root: Path | None = None,
                                  current_batch: str = "batch5") -> list[dict[str, Any]]:
    """按 Period（taxonomy 顺序）统计 Event 数：critical/major/normal/minor + New/Reused。

    New = 本批（Batch3）新增（review provenance）；Reused = 该 Period 内既有 Event。
    （§53：固定区分 New / Reused / Total，不再把新增数量与当前总量混写。）
    """
    rows: list[dict[str, Any]] = []
    order = [p["id"] for p in backbone.periods]
    by_period: dict[str, dict[str, int]] = {}
    for event in backbone.events:
        period_id = event.get("period_id") or "?"
        bucket = by_period.setdefault(period_id, {"critical": 0, "major": 0, "normal": 0, "minor": 0, "new": 0})
        bucket[event.get("importance", "normal")] = bucket.get(event.get("importance", "normal"), 0) + 1
        if root is not None and _event_in_batch(root, event["id"], current_batch):
            bucket["new"] += 1
    for period_id in order:
        bucket = by_period.get(period_id, {"critical": 0, "major": 0, "normal": 0, "minor": 0, "new": 0})
        total = bucket["critical"] + bucket["major"] + bucket["normal"] + bucket["minor"]
        rows.append({
            "period_id": period_id,
            "name_zh_cn": next((p["name_zh_cn"] for p in backbone.periods if p["id"] == period_id), period_id),
            **bucket,
            "reused": total - bucket["new"],
            "total": total,
        })
    return rows


def write_backbone_coverage(root: Path, backbone: Backbone | None = None,
                            manifest: dict[str, Any] | None = None) -> Path:
    if backbone is None:
        from .loader import load_backbone
        backbone = load_backbone(root)
    coverage = compute_coverage(backbone)
    importance_rows = compute_importance_by_period(backbone, root=root)
    reports_dir = root / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    json_payload = {
        **coverage,
        "by_period": importance_rows,
    }
    (reports_dir / "backbone_coverage.json").write_text(
        json.dumps(json_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

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
        "## 按 Period 的重要性分布",
        "",
        "| Period | New | Reused | Total | Critical | Major |",
        "| ------ | --: | -----: | ----: | -------: | ----: |",
    ]
    for row in importance_rows:
        if row["total"] == 0:
            continue
        lines.append(
            f"| {row['name_zh_cn']} | {row['new']} | {row['reused']} | {row['total']} | {row['critical']} | {row['major']} |"
        )
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