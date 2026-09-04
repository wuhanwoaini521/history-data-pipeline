# -*- coding: utf-8 -*-
"""Preview / EventRelation 正确性测试。

背景：event-three-chibi（赤壁之战, 208）曾因 Preview 导出把
「排序前的数组序号」当作实体引用，Viewer 落入 DATA.events[573/574]
后呈现为 护法运动→赤壁之战→府院之争（1917 年代串台）。

本套测试从三个事实源各查一遍，并锁定「导出必须使用 canonical event_id，
绝不允许 surrogate index / row number」这条规则：
  1. dist/history.duckdb —— Backbone 事实层
  2. tools/history-preview/data/events.json —— Preview 导出层
  3. tools/history-preview/data/relations.json —— Preview 关系表
"""

from __future__ import annotations

import json
from pathlib import Path

import duckdb
import pytest

ROOT = Path(__file__).parents[1]
DIST_DB = ROOT / "dist" / "history.duckdb"
PREVIEW_EVENTS = ROOT / "tools" / "history-preview" / "data" / "events.json"
PREVIEW_RELATIONS = ROOT / "tools" / "history-preview" / "data" / "relations.json"

CHIBI = "event-three-chibi"            # 赤壁之战 208
REPUBLIC_IDS = {
    "event-fuyuan-zhi-zheng",          # 府院之争 1917
    "event-hufa-yundong",               # 护法运动 1917
    "event-zhangxun-fubi",            # 张勋复辟 1917
}


@pytest.fixture(scope="module")
def dist_conn():
    if not DIST_DB.exists():
        pytest.skip("dist/history.duckdb 未构建")
    return duckdb.connect(str(DIST_DB), read_only=True)


@pytest.fixture(scope="module")
def preview_events():
    if not PREVIEW_EVENTS.exists():
        pytest.skip("preview data 未构建")
    return json.loads(PREVIEW_EVENTS.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def preview_relations():
    if not PREVIEW_RELATIONS.exists():
        pytest.skip("preview data 未构建")
    return json.loads(PREVIEW_RELATIONS.read_text(encoding="utf-8"))


def _event_by_id(events, eid):
    found = [e for e in events if e["id"] == eid]
    assert len(found) == 1, f"preview 中事件 {eid} 唯一性损坏"
    return found[0]


def test_backbone_chibi_relations_are_clean(dist_conn):
    """Backbone（dist DB）事实层：chibi 只应连接回 三国 年代事件，绝不连民国。"""
    rows = dist_conn.execute(
        "SELECT source_event_id, target_event_id, relation_type "
        "FROM event_relations WHERE source_event_id=? OR target_event_id=?",
        [CHIBI, CHIBI],
    ).fetchall()
    assert rows, "chibi 没有任何 relation"
    for s, t, rt in rows:
        assert rt in ("leads_to", "precedes", "follows", "part_of", "contributes_to")
        other = t if s == CHIBI else s
        # 208 年的事件不可能与民国时期形成 DIRECT 关系
        assert other not in REPUBLIC_IDS, f"chibi 连接到民国事件 {other}"


def test_preview_relation_uses_canonical_event_id(preview_events):
    """preview 导出的 relations_in/out 必须是 canonical event id，不能是序号。"""
    chibi = _event_by_id(preview_events, CHIBI)
    for r in chibi["relations_in"]:
        assert isinstance(r["source"], str), "relations_in.source 必须是字符串 canonical id"
        assert r["source"].startswith("event-"), f"relations_in.source 不是 event id: {r['source']}"
    for r in chibi["relations_out"]:
        assert isinstance(r["target"], str), "relations_out.target 必须是字符串 canonical id"
        assert r["target"].startswith("event-"), f"relations_out.target 不是 event id: {r['target']}"


def test_chibi_relation_not_republican(preview_events):
    """赤壁之战（208）的 in/out 绝不能落入民国事件（核心 bug）。"""
    chibi = _event_by_id(preview_events, CHIBI)
    names = {e["id"]: e["name"] for e in preview_events}
    for r in chibi["relations_in"]:
        assert r["source"] not in REPUBLIC_IDS, f"relations_in {r['source']} 是民国事件"
        assert r["source"].startswith("event-three-"), \
            f"chibi in {r['source']} ({names.get(r['source'])}) 不是三国时期事件"
    for r in chibi["relations_out"]:
        assert r["target"] not in REPUBLIC_IDS, f"chibi out {r['target']} 是民国时期"
        assert r["target"].startswith("event-three-"), \
            f"chibi out {r['target']} ({names.get(r['target'])}) 不是三国事件"


def test_relation_source_target_exist(preview_events):
    """preview 的每个 relation 引用必须能解析到已导出的 event。"""
    ids = {e["id"] for e in preview_events}
    for e in preview_events:
        for r in e.get("relations_in", []):
            assert r["source"] in ids, f"{e['id']} relations_in.source {r['source']} 悬空"
        for r in e.get("relations_out", []):
            assert r["target"] in ids, f"{e['id']} relations_out.target {r['target']} 悬空"


def test_relation_no_surrogate_id_export(preview_events):
    """全量导出中不允许出现 int 型 surrogate 引用（数组 index / DB row id）。"""
    for e in preview_events:
        for r in e.get("relations_in", []):
            assert not isinstance(r["source"], int), \
                f"{e['id']} relations_in 使用 surrogate {r['source']}"
        for r in e.get("relations_out", []):
            assert not isinstance(r["target"], int), \
                f"{e['id']} relations_out 使用 surrogate {r['target']}"


def test_relation_cross_era_audit(preview_relations, preview_events):
    """chibi 不能出现在任何跨 100+ 年的强语义关系里（核心 bug 的放大器）。"""
    by_id = {e["id"]: e for e in preview_events}
    risky = []
    for r in preview_relations:
        s, t, rel = r.get("src"), r.get("tgt"), r.get("rel")
        if s != CHIBI and t != CHIBI:
            continue
        if rel not in ("leads_to", "precedes", "followed_by"):
            continue
        se = by_id[s]["start"]
        te = by_id[t]["start"]
        if se is None or te is None:
            risky.append(r)
        elif abs(te - se) > 100:
            risky.append(r)
    # 专项断言：赤壁 不允许跨世纪强关系（回归 573/574 bug）
    assert not risky, f"chibi 出现跨时代强关系: {risky}"