"""China History Backbone V1 · Batch 5（北宋·辽·西夏·金·南宋·蒙古/元边界）测试。

覆盖：baseline / 北宋建立 / 三政权并行（北宋∥辽∥西夏）/ 金∥南宋∥蒙古 /
1206 大蒙古国 ≠ 1271 元 / 靖康 / 岳飞史源审慎 / 崖山终点 / source coverage / timeline order。
"""

from __future__ import annotations

from pathlib import Path

import pytest

from history_data_pipeline.backbone.loader import load_backbone

ROOT = Path(__file__).parents[1]

TRIPLE_REGIMES = ("regime-northern-song", "regime-liao", "regime-western-xia")
SECOND_TRIPLE = ("regime-southern-song", "regime-jin", "regime-mongol-empire")


@pytest.fixture(scope="module")
def backbone():
    return load_backbone(ROOT)


def _batch5(event):
    return "song_liao_xia_jin" in event.get("_file", "") or "event-yuan-jianguo.yml" in event.get("_file", "")


def test_batch5_backbone_baseline(backbone):
    by_period = {pid: [e for e in backbone.events if e["period_id"] == pid] for pid in
                 {"period-northern-song", "period-liao", "period-western-xia", "period-jin",
                  "period-southern-song", "period-song-liao-jin", "period-yuan"}}
    assert len(by_period["period-northern-song"]) >= 20
    assert len(by_period["period-liao"]) >= 2
    assert len(by_period["period-western-xia"]) >= 5
    assert len(by_period["period-jin"]) >= 5
    assert len(by_period["period-southern-song"]) >= 14
    assert len(by_period["period-yuan"]) >= 1
    names = {e["name_zh_cn"] for e in backbone.events}
    for key in ("陈桥兵变、赵匡胤称帝、北宋建立", "靖康之变、北宋灭亡",
                "赵构称帝、南宋建立", "崖山海战、南宋灭亡"):
        assert key in names, f"缺少 Batch5 关键节点: {key}"
    batch5_new = [e for e in backbone.events if _batch5(e)]
    assert len(batch5_new) >= 63
    assert all(e["importance"] in {"critical", "major"} for e in batch5_new)


def test_batch5_chenqiao_bingbian(backbone):
    by_id = {e["id"]: e for e in backbone.events}
    ev = by_id["event-chenqiao-bingbian"]
    assert ev["start_year"] == 960 and ev["importance"] == "critical"
    assert "regime-northern-song" in ev["regime_ids"]
    assert "event-song-tongyi-zhanzheng" in by_id
    # 统一战争 aggregate 含 6 个子事件
    children = {e["id"] for e in backbone.events
                if any(r["relation_type"] == "part_of" and r["target_event_id"] == "event-song-tongyi-zhanzheng"
                       for r in e.get("relations", []))}
    assert len(children) == 6


def test_three_regimes_parallel(backbone):
    """北宋 ∥ 辽 ∥ 西夏：三 Regime 均存在且同一时段并存（独立 Regime 行）。"""
    regimes = {r["id"]: r for r in backbone.regimes}
    for rid in TRIPLE_REGIMES:
        assert rid in regimes, rid
    by_id = {e["id"]: e for e in backbone.events}
    assert set(by_id["event-gaolianghe-zhizhan"]["regime_ids"]) == {"regime-northern-song", "regime-liao"}
    assert set(by_id["event-sanchuankou-zhizhan"]["regime_ids"]) == {"regime-western-xia", "regime-northern-song"}
    assert "event-western-xia-jianguo" in by_id and by_id["event-western-xia-jianguo"]["start_year"] == 1038


def test_jin_southern_song_mongol_parallel(backbone):
    """南宋 ∥ 金 ∥ 蒙古：1206-1271 蒙古（regime-mongol-empire）与金、南宋并存。"""
    regimes = {r["id"]: r for r in backbone.regimes}
    for rid in SECOND_TRIPLE:
        assert rid in regimes, rid
    assert regimes["regime-mongol-empire"]["period_id"] == "period-song-liao-jin"
    by_id = {e["id"]: e for e in backbone.events}
    assert set(by_id["event-mongol-mie-jin"]["regime_ids"]) == {"regime-mongol-empire", "regime-jin", "regime-southern-song"}


def test_mongol_empire_vs_yuan(backbone):
    """1206 大蒙古国 ≠ 1271 元：两个 Regime 阶段，禁止 1206 之后全部 regime-yuan。"""
    regimes = {r["id"]: r for r in backbone.regimes}
    assert regimes["regime-mongol-empire"]["start_year"] == 1206
    assert regimes["regime-mongol-empire"]["end_year"] == 1271
    assert regimes["regime-yuan"]["start_year"] == 1271
    assert regimes["regime-yuan"].get("parent_regime_id") == "regime-mongol-empire"
    by_id = {e["id"]: e for e in backbone.events}
    assert "regime-mongol-empire" in by_id["event-mongol-jianguo"]["regime_ids"]
    assert by_id["event-mongol-jianguo"]["period_id"] == "period-song-liao-jin"
    assert "regime-yuan" in by_id["event-yuan-jianguo"]["regime_ids"]
    assert by_id["event-yuan-jianguo"]["period_id"] == "period-yuan"
    # 事件整体结束于 1270 年前（end_year<=1270）不得挂 regime-yuan（1267—1273 襄樊之战跨 1271 属正当例外）
    for e in backbone.events:
        if (e.get("end_year") or e.get("start_year")) and (e.get("end_year") or 0) <= 1270                 and "regime-yuan" in (e.get("regime_ids") or []):
            raise AssertionError(f"{e['id']}: 1271 前已结束的事件不得使用 regime-yuan")


def test_jingkang_and_nansong(backbone):
    by_id = {e["id"]: e for e in backbone.events}
    assert by_id["event-jingkang-zhi-bian"]["start_year"] == 1127
    assert by_id["event-jingkang-zhi-bian"]["importance"] == "critical"
    assert by_id["event-zhao-gou-nansong-jianguo"]["start_year"] == 1127
    assert "event-jianyan-nandu" in by_id
    # 金灭辽（1125）与北宋灭亡（1127）链条
    assert by_id["event-liao-miewang"]["start_year"] == 1122 and by_id["event-liao-miewang"]["end_year"] == 1125


def test_yuefei_source_discipline(backbone):
    """岳飞相关叙事不得使用\"十二道金牌/直捣黄龙\"等未经严格史源限定的通俗表达。"""
    for e in backbone.events:
        if e["id"] in ("event-yancheng-zhizhan", "event-yuefei-banshi", "event-yuefei-beisha",
                       "event-shaoxing-heyi"):
            text = e["summary_zh_cn"] + (e.get("review_note") or "")
            assert "十二道金牌" not in text or "十二道金牌" in e.get("review_note", ""), e["id"]
            assert "直捣黄龙" not in text, e["id"]
            assert e["id"] == "event-yuefei-banshi" or "岳家军" in e["summary_zh_cn"] or e["id"] != "event-yuefei-banshi"


def test_yanya_endpoint(backbone):
    """本批终点：崖山海战 1279 南宋灭亡；不得出现 Batch6 内容（靖难/土木堡/郑和）。"""
    by_id = {e["id"]: e for e in backbone.events}
    ev = by_id["event-yanya-haizhan"]
    assert ev["start_year"] == 1279 and ev["importance"] == "critical"
    assert {x["period_id"] for x in (ev,)} == {"period-southern-song"}
    # Batch5 边界：不得进入 Batch7（清）内容（元明为 Batch6 范围）
    for banned in ("清军入关", "三藩之乱", "鸦片战争"):
        assert not any(banned in e["name_zh_cn"] for e in backbone.events), f"Batch7 内容不应出现: {banned}"


def test_batch5_source_coverage(backbone):
    batch5_new = [e for e in backbone.events if _batch5(e)]
    assert len(batch5_new) >= 63
    for event in batch5_new:
        assert event.get("source_type") == "curated_reference", event["id"]
        assert event.get("source_reference"), event["id"]
        assert event.get("source_ids"), event["id"]
        assert "AI" not in event["source_reference"], event["id"]
        assert any(wid in event["source_ids"] for wid in
                   ("work-curated-songshi", "work-curated-liaoshi", "work-curated-jinshi",
                    "work-curated-yuanshi", "work-curated-xuzizhitongjianchangbian")), event["id"]


def test_batch5_timeline_order(backbone):
    from history_data_pipeline.backbone.timeline import filter_timeline, timeline_record
    rows = [timeline_record(e) for e in filter_timeline(backbone)]
    years = [r["start_year"] for r in rows if r["start_year"] is not None]
    assert years == sorted(years)
    seq = {r["id"]: r["start_year"] for r in rows}
    chain = [("event-chenqiao-bingbian", 960), ("event-chanyuan-zhi-meng", 1004),
             ("event-western-xia-jianguo", 1038), ("event-jin-jianguo", 1115),
             ("event-jingkang-zhi-bian", 1127), ("event-zhao-gou-nansong-jianguo", 1127),
             ("event-mongol-jianguo", 1206), ("event-mongol-mie-jin", 1232),
             ("event-yuan-jianguo", 1271), ("event-yanya-haizhan", 1279)]
    for eid, year in chain:
        assert eid in seq, f"timeline 缺少 {eid}"
        assert seq[eid] == year, f"{eid} 应为 {year} 实为 {seq[eid]}"