"""Product Coverage / Enrichment Queue / 数据完整性（Gate 3/4/7 不变式）测试。

覆盖：
- product_completeness 的 9 维不变式与打分公式（含 process/impact 上限 77.8）；
- product_coverage 聚合（按重要性 / 按 Period / Lowest Coverage，数字来自真实计算）；
- enrichment_queue 的三档优先级边界与排序不变式；
- 报告写入确定性（同数据两次生成字节一致）；
- 已提交报告与当前代码重新生成的报告一致（regenerable）；
- 真实 dist 的引用完整性：事件/人物/地点/时期无孤儿，来源 license 非空。
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import duckdb
import pytest

from history_data_pipeline.backbone.loader import Backbone, load_backbone
from history_data_pipeline.backbone.product_completeness import (
    PRODUCT_COMPLETENESS_DIMENSIONS,
    dimension_satisfied,
    event_completeness,
)
from history_data_pipeline.backbone.product_coverage import (
    COMPLETE_THRESHOLD,
    build_product_stats,
    write_product_coverage,
)
from history_data_pipeline.backbone.enrichment_queue import (
    build_queue,
    write_enrichment_queue,
)

ROOT = Path(__file__).parents[1]


def _event(event_id: str, **overrides: object) -> dict:
    base: dict[str, object] = {
        "id": event_id,
        "name_zh_cn": event_id,
        "importance": "major",
        "period_id": "period-tang",
    }
    base.update(overrides)
    return base


def _full_event(event_id: str, period_id: str = "period-tang") -> dict:
    return _event(
        event_id,
        period_id=period_id,
        people=[{"person_id": "person-a"}],
        places=[{"place_id": "place-a"}],
        evidence=[{"id": "ev-a"}],
        relations=[{"target_event_id": "e-other", "relation_type": "related_to"}],
        source_reference="资治通鉴·卷201",
        background_zh_cn="背景叙述",
        process_zh_cn="过程叙述",
        result_zh_cn="结果叙述",
        impact_zh_cn="影响叙述",
    )


def _backbone(events: list[dict], periods: list[dict] | None = None) -> Backbone:
    if periods is None:
        periods = [{"id": "period-tang", "name_zh_cn": "唐", "start_year": 618, "end_year": 907}]
    return Backbone(
        root=ROOT,
        taxonomy_dir=ROOT / "taxonomy",
        periods=periods,
        events=events,
    )


# ---------------------------------------------------------------------------
# product_completeness：9 维不变式 + 打分公式
# ---------------------------------------------------------------------------


def test_completeness_dimensions_are_a_stable_invariant():
    assert PRODUCT_COMPLETENESS_DIMENSIONS == (
        "people", "place", "source", "evidence",
        "related_event", "background", "process", "result", "impact",
    )


def test_event_completeness_scores_exact():
    row = event_completeness(_full_event("e-full"))
    assert row["fulfilled"] == 9
    assert row["total"] == 9
    assert row["product_completeness_score"] == 100.0
    assert row["missing"] == []

    incomplete = event_completeness(_event("e-bare"))
    assert incomplete["fulfilled"] == 0
    assert incomplete["product_completeness_score"] == 0.0
    assert incomplete["missing"] == list(PRODUCT_COMPLETENESS_DIMENSIONS)


def test_process_and_impact_missing_caps_score_at_7_of_9():
    """Gate 5 前置：缺失 process/impact 时最高得分 77.8（无法达到完整阈值）。"""
    capped = _event(
        "e-cap",
        people=[{"name": "p1"}],
        places=[{"place_id": "a"}],
        evidence=[{"id": "x"}],
        relations=[{"target_event_id": "y", "relation_type": "related_to"}],
        source_reference="贞观政要",
        background_zh_cn="背景",
        result_zh_cn="结果",
    )
    row = event_completeness(capped)
    assert row["missing"] == ["process", "impact"]
    assert row["product_completeness_score"] == round(100.0 * 7 / 9, 1)


def test_dimension_satisfied_ignores_whitespace_only_text():
    event = _event("e-ws", background_zh_cn="   ", process_zh_cn="", impact_zh_cn=None)
    assert not dimension_satisfied(event, "background")
    assert not dimension_satisfied(event, "process")
    assert not dimension_satisfied(event, "impact")
    assert dimension_satisfied(_event("e-ok", process_zh_cn="真实过程"), "process")
    with pytest.raises(KeyError):
        dimension_satisfied(_event("e-x"), "unknown_dimension")


# ---------------------------------------------------------------------------
# product_coverage：聚合与 Lowest Coverage Periods
# ---------------------------------------------------------------------------


def test_product_coverage_aggregates_by_period_and_importance():
    periods = [
        {"id": "period-tang", "name_zh_cn": "唐", "start_year": 618, "end_year": 907},
        {"id": "period-ming", "name_zh_cn": "明", "start_year": 1368, "end_year": 1644},
    ]
    events = [
        _full_event("e-tang-t", "period-tang"),                          # 9/9 = 100
        _event("e-tang-p", period_id="period-tang",                      # 6/9 = 66.7
               people=[{"name": "p"}], places=[{"place_id": "a"}],
               evidence=[{"id": "x"}],
               relations=[{"target_event_id": "y", "relation_type": "related_to"}],
               source_reference="旧唐书", background_zh_cn="背景"),
        _event("e-ming-t", period_id="period-ming", importance="critical",  # 8/9 = 88.9（缺 impact）
               people=[{"name": "p"}], places=[{"place_id": "a"}],
               evidence=[{"id": "x"}], relations=[{"target_event_id": "y", "relation_type": "related_to"}],
               source_reference="明史", background_zh_cn="背景",
               process_zh_cn="过程", result_zh_cn="结果"),
        _event("e-ming-x", period_id="period-ming", importance="normal"),  # 0 维
    ]
    stats = build_product_stats(_backbone(events, periods))

    assert stats["schema"] == "product-coverage-v1"
    assert stats["total_events"] == 4
    assert stats["complete_events"] == 1
    assert stats["complete_pct"] == 25.0
    assert stats["mean_score"] == round((100.0 + 66.7 + 88.9 + 0.0) / 4, 1)

    by_period = {row["period_id"]: row for row in stats["by_period"]}
    assert by_period["period-tang"]["events"] == 2
    assert by_period["period-tang"]["complete_pct"] == 50.0
    assert by_period["period-ming"]["events"] == 2
    # 明：两条都不完整（88.9 / 0）→ 完整率 0%，低于唐的 50%
    assert by_period["period-ming"]["complete_pct"] == 0.0

    assert stats["by_importance"]["critical"]["count"] == 1
    assert stats["by_importance"]["critical"]["complete"] == 0

    # Lowest Coverage Periods：只统计有事件的时期，完整率由低到高。
    lowest = stats["lowest_coverage_periods"]
    assert lowest and lowest[0]["period_id"] == "period-ming"


# ---------------------------------------------------------------------------
# enrichment_enrichment：阈值边界 + 公式偏序
# ---------------------------------------------------------------------------


def test_enrichment_queue_priority_bounds():
    cases = [(70.0, "Critical"), (69.9, "Major"), (50.0, "Major"), (49.9, "Normal"), (0.0, "Normal")]
    from history_data_pipeline.backbone.enrichment_queue import _prioritize

    for score, expected in cases:
        assert _prioritize(score) == expected, f"score={score}"


def test_enrichment_queue_orders_critical_first_and_is_deterministic():
    periods = [
        {"id": "period-tang", "name_zh_cn": "唐", "start_year": 618, "end_year": 907},
        {"id": "period-others", "name_zh_cn": "他", "start_year": 1000, "end_year": 1100},
    ]
    events = [
        _event("e-c1", importance="critical", period_id="period-tang",
               people=[{"name": "p"}]),                     # 缺失 8 维
        _event("e-c2", importance="critical", period_id="period-tang",
               people=[{"name": "p"}], places=[{"place_id": "a"}]),
        _event("e-m1", importance="major", period_id="period-tang",
               people=[{"name": "p"}]),
        _event("e-n1", importance="normal", period_id="period-others",
               people=[{"name": "p"}]),
    ]
    first = build_queue(_backbone(events, periods))
    second = build_queue(_backbone(events, periods))
    assert first["totals"]["events"] == 4
    assert [
        row["event_id"] for row in first["queue"]
    ] == [row["event_id"] for row in second["queue"]], "队列排序必须确定性"

    order = first["queue"]
    ranks = {"Critical": 0, "Major": 1, "Normal": 2}
    assert all(
        ranks[order[i]["priority"]] <= ranks[order[i + 1]["priority"]]
        for i in range(len(order) - 1)
    ), "优先级必须 Critical ≥ Major ≥ Normal 整体有序"
    assert order[0]["priority"] == "Critical"
    assert order[0]["event_id"] == "e-c1"
    # Critical 事件缺失维度更多 → 分数更高、排在同优先级之前
    critical_rows = [row for row in order if row["event_id"].startswith("e-c")]
    assert critical_rows[0]["score"] >= critical_rows[1]["score"]
    # 缺失数参与评分
    c1, c2 = {row["event_id"]: row for row in order}["e-c1"], {row["event_id"]: row for row in order}["e-c2"]
    assert c1["missing_count"] > c2["missing_count"]
    assert c1["score"] > c2["score"]


def test_enrichment_queue_importance_weight_drives_score():
    periods = [{"id": "period-x", "name_zh_cn": "测试期", "start_year": 1000, "end_year": 1100}]
    base = {
        "people": [{"name": "p"}],
        "places": [{"place_id": "a"}],
        "evidence": [{"id": "x"}],
        "relations": [{"target_event_id": "y", "relation_type": "related_to"}],
    }
    events = [
        _event("e-a", importance="critical", period_id="period-x", **base),
        _event("e-b", importance="major", period_id="period-x", **base),
    ]
    payload = build_queue(_backbone(events, periods))
    by_id = {row["event_id"]: row for row in payload["queue"]}
    # 缺失数 / 时期弱点 / 主窗口期加成完全相同：
    # score 差 = importance_weight(40-25) + frontend_visibility(5-3) = 17
    assert by_id["e-a"]["score"] - by_id["e-b"]["score"] == pytest.approx(17)
    assert by_id["e-a"]["score"] > by_id["e-b"]["score"]


# ---------------------------------------------------------------------------
# 报告写入与再生
# ---------------------------------------------------------------------------


def _identical_reports(loc_a: Path, loc_b: Path) -> None:
    write_product_coverage(loc_a)
    write_product_coverage(loc_b)
    assert (loc_a / "reports" / "PRODUCT_COVERAGE.md").read_bytes() == (
        loc_b / "reports" / "PRODUCT_COVERAGE.md"
    ).read_bytes()
    assert (loc_a / "reports" / "product_coverage.json").read_bytes() == (
        loc_b / "reports" / "product_coverage.json"
    ).read_bytes()
    write_enrichment_queue(loc_a)
    write_enrichment_queue(loc_b)
    assert (loc_a / "reports" / "ENRICHMENT_QUEUE.json").read_bytes() == (
        loc_b / "reports" / "ENRICHMENT_QUEUE.json"
    ).read_bytes()


def test_report_regeneration_is_deterministic(tmp_path: Path) -> None:
    """同一数据源两次生成报告，字节级一致（regenerable / deterministic）。"""
    _identical_reports(tmp_path / "a", tmp_path / "b")


def test_committed_reports_are_current(tmp_path: Path) -> None:
    """已提交的 reports 必须与当前代码对当前数据的生成结果一致（否则提示重新生成）。"""
    live = build_product_stats(load_backbone(ROOT))
    committed = json.loads((ROOT / "reports" / "product_coverage.json").read_text(encoding="utf-8"))
    assert live["schema"] == committed["schema"] == "product-coverage-v1"
    assert live["total_events"] == committed["total_events"]
    assert live["complete_events"] == committed["complete_events"]
    assert live["mean_score"] == committed["mean_score"]

    live_queue = build_queue(load_backbone(ROOT))
    committed_queue = json.loads((ROOT / "reports" / "ENRICHMENT_QUEUE.json").read_text(encoding="utf-8"))
    assert live_queue["totals"] == committed_queue["totals"]
    assert live_queue["queue"][0]["priority"] == "Critical"


# ---------------------------------------------------------------------------
# dist 产物完整性：无孤儿引用 / 来源可追溯 / License 非空
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def dist_db() -> duckdb.DuckDBPyConnection:
    db = ROOT / "dist" / "history.duckdb"
    if not db.exists():
        pytest.skip("dist/history.duckdb 未构建；请先执行 `backbone build`")
    return duckdb.connect(str(db), read_only=True)


def test_dist_has_no_orphan_references(dist_db) -> None:
    # Gate 7: no orphan 元数据。
    assert dist_db.execute(
        "SELECT COUNT(*) FROM event_person WHERE person_id IS NOT NULL"
        " AND person_id NOT IN (SELECT id FROM people)"
    ).fetchone()[0] == 0
    assert dist_db.execute(
        "SELECT COUNT(*) FROM event_place WHERE place_id IS NOT NULL"
        " AND place_id NOT IN (SELECT id FROM places)"
    ).fetchone()[0] == 0
    assert dist_db.execute(
        "SELECT COUNT(*) FROM events WHERE period_id IS NOT NULL"
        " AND period_id NOT IN (SELECT id FROM periods)"
    ).fetchone()[0] == 0
    assert dist_db.execute(
        "SELECT COUNT(*) FROM event_relations WHERE source_event_id NOT IN (SELECT id FROM events)"
    ).fetchone()[0] == 0
    assert dist_db.execute(
        "SELECT COUNT(*) FROM event_relations WHERE target_event_id NOT IN (SELECT id FROM events)"
    ).fetchone()[0] == 0


def test_dist_event_source_ids_resolve_and_licenses_non_empty(dist_db) -> None:
    # Gate 7：每条事件都带来源 id；来源表 license / source_type 非空（License 隔离可追溯）。
    assert dist_db.execute(
        "SELECT COUNT(*) FROM events WHERE source_ids IS NULL OR source_ids = ''"
    ).fetchone()[0] == 0
    n_sources = dist_db.execute("SELECT COUNT(*) FROM sources").fetchone()[0]
    assert n_sources > 0
    assert dist_db.execute(
        "SELECT COUNT(*) FROM sources WHERE license IS NULL OR TRIM(license) = ''"
    ).fetchone()[0] == 0
    assert dist_db.execute(
        "SELECT COUNT(*) FROM sources WHERE source_type IS NULL OR TRIM(source_type) = ''"
    ).fetchone()[0] == 0


def test_dist_count_floor_matches_reports(dist_db) -> None:
    events = dist_db.execute("SELECT COUNT(*) FROM events").fetchone()[0]
    committed = json.loads((ROOT / "reports" / "product_coverage.json").read_text(encoding="utf-8"))
    assert events >= committed["total_events"] >= 600