"""Backbone Build / Manifest / Exports 测试。

直接在当前仓库执行 `backbone build`（数据量小，幂等），验证：
- Validation Gate 会拦截 broken reference；
- dist/history.duckdb 可重建；
- manifest.json 含真实统计；
- parquet / json 导出齐全。
"""

from __future__ import annotations

import json
from pathlib import Path

import duckdb
import pytest
import yaml

from history_data_pipeline.backbone.build import build_backbone
from history_data_pipeline.backbone.validate import check_strict_gate

ROOT = Path(__file__).parents[1]


def test_backbone_build():
    from history_data_pipeline.config import PipelinePaths

    paths = PipelinePaths(ROOT)
    manifest = build_backbone(paths)
    db = paths.dist_database
    assert db.exists()
    with duckdb.connect(str(db), read_only=True) as connection:
        counts = {
            table: int(connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0])
            for table in ("events", "stories", "story_events", "event_relations",
                          "event_person", "event_place", "event_evidence", "periods", "regimes")
        }
    assert counts["events"] == 535  # + Batch7 OPIUM_TAIPING(11)
    assert counts["stories"] == 3
    assert counts["story_events"] == 26
    assert counts["event_relations"] == 930
    assert counts["event_person"] == 58
    assert counts["event_place"] == 26
    assert counts["event_evidence"] == 26
    assert counts["periods"] == 31
    assert counts["regimes"] == 62  # +Batch7 南明/太平天国/阿古柏
    assert manifest["counts"]["events"] == counts["events"]
    # 三个 Story 全部可按序查询
    with duckdb.connect(str(db), read_only=True) as connection:
        ordered = connection.execute(
            "SELECT story_id, sequence FROM story_events ORDER BY story_id, sequence"
        ).fetchall()
        by_story: dict[str, list[int]] = {}
        for story_id, sequence in ordered:
            by_story.setdefault(story_id, []).append(sequence)
        assert all(values == sorted(values) and len(values) == len(set(values)) for values in by_story.values())


def test_validation_gate_blocks_broken(event_tmp_root):
    """broken event reference / duplicate id / invalid date 必须被 Gate 拦截。"""
    from history_data_pipeline.backbone.loader import load_backbone
    from history_data_pipeline.backbone.validate import validate_backbone

    root = event_tmp_root
    backbone = load_backbone(root)
    errors = validate_backbone(backbone, root)
    messages = "\n".join(errors)
    assert "引用不存在 event-ghost" in messages  # Story → Event broken
    assert "start_year=300 > end_year=200" in messages  # invalid date
    assert "ID 重复 event-good" in messages  # duplicate id
    with pytest.raises(RuntimeError):
        check_strict_gate(backbone, errors, root)


@pytest.fixture(scope="module")
def event_tmp_root(tmp_path_factory):
    """构造最小坏 Backbone：重复 ID + broken story ref + 非法日期。"""
    root = tmp_path_factory.mktemp("broken_backbone")
    taxonomy = root / "data" / "curated" / "history_backbone" / "taxonomy"
    events = root / "data" / "curated" / "history_backbone" / "events" / "pre_qin"
    stories = root / "data" / "curated" / "history_backbone" / "stories" / "qin_han"
    taxonomy.mkdir(parents=True)
    events.mkdir(parents=True)
    stories.mkdir(parents=True)
    (taxonomy / "periods.yml").write_text(yaml.safe_dump({
        "periods": [{"id": "period-test", "name_zh_cn": "测试期", "start_year": -100, "end_year": 100,
                     "date_precision": "range", "description_zh_cn": "测试"}],
    }, allow_unicode=True), encoding="utf-8")
    (taxonomy / "regimes.yml").write_text("regimes: []\n", encoding="utf-8")
    (taxonomy / "event_types.yml").write_text("event_types: []\n", encoding="utf-8")
    (taxonomy / "relation_types.yml").write_text(
        "relation_types:\n- {id: precedes, name_zh_cn: 先于}\n- {id: leads_to, name_zh_cn: 引向}\n", encoding="utf-8")
    (taxonomy / "quality_status.yml").write_text(
        "quality_status:\n- {id: reviewed, name_zh_cn: 已复核}\n", encoding="utf-8")
    good = {
        "id": "event-good", "name_zh_cn": "好事件", "event_type": "war",
        "start_year": 100, "end_year": 100, "date_precision": "year",
        "period_id": "period-test", "importance": "major", "quality_status": "reviewed",
        "summary_zh_cn": "好", "source_type": "curated_reference", "source_reference": "测试",
        "people": [], "places": [], "evidence": [], "relations": [],
    }
    bad = {
        "id": "event-good", "name_zh_cn": "重复ID", "event_type": "war",
        "start_year": 300, "end_year": 200, "date_precision": "year",
        "period_id": "period-missing", "importance": "major", "quality_status": "reviewed",
        "summary_zh_cn": "坏", "relations": [{"target_event_id": "event-ghost", "relation_type": "leads_to"}],
    }
    (events / "event-good.yml").write_text(yaml.safe_dump(good, allow_unicode=True), encoding="utf-8")
    (events / "event-bad.yml").write_text(yaml.safe_dump(bad, allow_unicode=True), encoding="utf-8")
    (stories / "story-bad.yml").write_text(yaml.safe_dump({
        "id": "story-bad", "title_zh_cn": "坏故事", "start_year": 100, "end_year": 200,
        "story_type": "war", "period_id": "period-test",
        "events": [{"event_id": "event-ghost", "sequence": 1}],
    }, allow_unicode=True), encoding="utf-8")
    return root


def test_manifest():
    manifest_path = ROOT / "dist" / "manifest.json"
    assert manifest_path.exists()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["version"] == (ROOT / "DATA_VERSION").read_text(encoding="utf-8").strip()
    assert manifest["built_at"]
    assert manifest["counts"]["events"] == 535
    assert manifest["counts"]["stories"] == 3
    assert manifest["counts"]["historical_texts"] == 0  # 文本语料待知识库重建
    assert "by_period_group" in manifest
    assert manifest["reference_resolution"]["broken"] == 0


def test_exports():
    json_dir = ROOT / "dist" / "json"
    groups = {"periods", "regimes", "events", "event_relations", "stories", "story_events",
              "event_people", "event_places", "event_evidence", "people", "places", "works"}
    for group in groups:
        path = json_dir / f"{group}.json"
        assert path.exists(), f"缺少导出 {group}.json"
        records = json.loads(path.read_text(encoding="utf-8"))
        assert isinstance(records, list)
        if group == "events":
            assert len(records) == 535
    parquet_dir = ROOT / "dist" / "parquet"
    for group in ("events", "event_evidence", "people", "periods"):
        assert (parquet_dir / f"{group}.parquet").exists()


def test_dist_evidence_rows_are_reviewed():
    db = ROOT / "dist" / "history.duckdb"
    if not db.exists():
        pytest.skip("dist/history.duckdb 未构建")
    with duckdb.connect(str(db), read_only=True) as connection:
        total = connection.execute("SELECT COUNT(*) FROM event_evidence").fetchone()[0]
        reviewed = connection.execute(
            "SELECT COUNT(*) FROM event_evidence WHERE quality_status IN ('reviewed','verified') OR link_status='pending_knowledge'"
        ).fetchone()[0]
        assert reviewed == total
        # legacy 兼容表 event_text 与 event_evidence 一致
        legacy = connection.execute("SELECT COUNT(*) FROM event_text").fetchone()[0]
        assert legacy == total