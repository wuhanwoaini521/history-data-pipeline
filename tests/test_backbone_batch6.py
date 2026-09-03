"""China History Backbone V1 · Batch 6（元→元末→明）测试。

覆盖：baseline / 元建立复用 / 南宋亡复用 / 行省为具体制度节点 / 元末群雄并列 /
明建立 / 靖难 / 永乐迁都 / 郑和 / 土木堡 / 张居正 / 后金与萨尔浒 / 1644 边界 / source / timeline。
"""

from __future__ import annotations

from pathlib import Path

import pytest

from history_data_pipeline.backbone.loader import load_backbone

ROOT = Path(__file__).parents[1]


@pytest.fixture(scope="module")
def backbone():
    return load_backbone(ROOT)


def _batch6(event):
    f = event.get("_file", "").replace("\\", "/").replace("//", "/")
    return "/yuan/" in f or "/ming/" in f


def test_batch6_backbone_baseline(backbone):
    by_period = {pid: [e for e in backbone.events if e["period_id"] == pid] for pid in
                 {"period-yuan", "period-ming"}}
    assert len(by_period["period-yuan"]) >= 25
    assert len(by_period["period-ming"]) >= 45
    names = {e["name_zh_cn"] for e in backbone.events}
    for key in ("朱元璋称帝、明朝建立", "迁都北京", "土木堡之变",
                "李自成攻入北京、明朝灭亡"):
        assert key in names, f"缺少 Batch6 关键节点: {key}"
    batch6_new = [e for e in backbone.events if _batch6(e)]
    assert len(batch6_new) >= 82
    assert all(e["importance"] in {"critical", "major"} for e in batch6_new)


def test_yuan_boundary_reused(backbone):
    """1271 元建立（Batch5）与南宋灭亡段被复用，不重复建档。"""
    by_id = {e["id"]: e for e in backbone.events}
    assert by_id["event-yuan-jianguo"]["start_year"] == 1271
    assert len([e for e in backbone.events if "元建立" in e["name_zh_cn"] or "元朝建立" in e["name_zh_cn"]]) == 1
    assert "event-yanya-haizhan" in by_id and by_id["event-yanya-haizhan"]["start_year"] == 1279


def test_xingsheng_concrete_node(backbone):
    """行省制度必须是具体制度节点，不是 Concept Event。"""
    by_id = {e["id"]: e for e in backbone.events}
    ev = by_id["event-yuan-xingsheng-zhidu"]
    assert ev["event_type"] == "reform"
    assert ev["start_year"] >= 1270 and ev["start_year"] <= 1300
    assert "行省" in ev["summary_zh_cn"]


def test_yuan_late_powers_parallel(backbone):
    """元末群雄并列：朱元璋势力/大汉（陈友谅）/大周（张士诚）/大宋（韩林儿）Regime 并存。"""
    regimes = {r["id"]: r for r in backbone.regimes}
    for rid in ("regime-zhuzhang", "regime-dahan", "regime-dazhou", "regime-dasong"):
        assert rid in regimes, rid
    by_id = {e["id"]: e for e in backbone.events}
    assert set(by_id["event-poyanghu-zhizhan"]["regime_ids"]) == {"regime-zhuzhang", "regime-dahan"}
    assert "event-zhangshichen-ju-gaoyou" in by_id and "event-fangguozhen-jiang" in by_id


def test_ming_foundation_and_beida(backbone):
    by_id = {e["id"]: e for e in backbone.events}
    assert by_id["event-zhuyuanzhang-chendi"]["start_year"] == 1368
    assert by_id["event-zhuyuanzhang-chendi"]["importance"] == "critical"
    assert "regime-ming" in by_id["event-zhuyuanzhang-chendi"]["regime_ids"]
    xd = by_id["event-xuda-beifa"]
    assert xd["start_year"] == 1368
    assert set(xd["regime_ids"]) == {"regime-ming", "regime-yuan"}


def test_jingnan_and_yongle(backbone):
    by_id = {e["id"]: e for e in backbone.events}
    assert by_id["event-jingnan-zhizhan"]["start_year"] == 1399 and by_id["event-jingnan-zhizhan"]["end_year"] == 1402
    assert by_id["event-jingnan-zhizhan"]["importance"] == "critical"
    children = {e["id"] for e in backbone.events
                if any(r.get("relation_type") == "part_of" and r.get("target_event_id") == "event-jingnan-zhizhan"
                       for r in e.get("relations", []))}
    assert children == {"event-jingnan-qibing", "event-yanjun-ru-jing"}
    assert by_id["event-qian-du-beijing"]["start_year"] == 1421 and by_id["event-qian-du-beijing"]["importance"] == "critical"


def test_zhenghe_aggregate(backbone):
    by_id = {e["id"]: e for e in backbone.events}
    assert by_id["event-zhenghe-xiaxiyang"]["start_year"] == 1405 and by_id["event-zhenghe-xiaxiyang"]["end_year"] == 1433
    children = {e["id"] for e in backbone.events
                if any(r.get("relation_type") == "part_of" and r.get("target_event_id") == "event-zhenghe-xiaxiyang"
                       for r in e.get("relations", []))}
    assert children == {"event-zhenghe-di-yici", "event-zhenghe-zui-hou"}


def test_tumu_and_duomen(backbone):
    by_id = {e["id"]: e for e in backbone.events}
    assert by_id["event-tumu-bao-zhibian"]["start_year"] == 1449
    assert by_id["event-tumu-bao-zhibian"]["importance"] == "critical"
    for key in ("event-jingtai-jiwei", "event-beijing-baoweizhan", "event-duomen-zhibian"):
        assert key in by_id, key


def test_zhangjuzheng_aggregate(backbone):
    by_id = {e["id"]: e for e in backbone.events}
    assert by_id["event-zhangjuzheng-gaige"]["start_year"] == 1572 and by_id["event-zhangjuzheng-gaige"]["end_year"] == 1582
    children = {e["id"] for e in backbone.events
                if any(r.get("relation_type") == "part_of" and r.get("target_event_id") == "event-zhangjuzheng-gaige"
                       for r in e.get("relations", []))}
    assert children == {"event-kaocheng-fa", "event-yitiao-bianfa", "event-zhangjuzheng-shoucuo"}


def test_houjin_and_saerhu(backbone):
    """后金建立（1616）+ 七大恨 + 萨尔浒（1619）+ 辽沈（1621）链。"""
    regimes = {r["id"]: r for r in backbone.regimes}
    assert "regime-houjin" in regimes and regimes["regime-houjin"]["start_year"] == 1616
    assert regimes["regime-qing"].get("parent_regime_id") == "regime-houjin"
    by_id = {e["id"]: e for e in backbone.events}
    assert by_id["event-houjin-jianguo"]["start_year"] == 1616
    assert by_id["event-saerhu-zhizhan"]["start_year"] == 1619 and by_id["event-saerhu-zhizhan"]["importance"] == "critical"
    assert set(by_id["event-saerhu-zhizhan"]["regime_ids"]) == {"regime-ming", "regime-houjin"}
    assert by_id["event-qidahen"]["start_year"] == 1618
    assert by_id["event-liaoshen-shixian"]["start_year"] == 1621


def test_1644_boundary(backbone):
    """本批终点：1644 北京陷落崇祯自缢；南明/清入关为 Batch7。"""
    by_id = {e["id"]: e for e in backbone.events}
    ev = by_id["event-lizicheng-gong-beijing"]
    assert ev["start_year"] == 1644 and ev["importance"] == "critical"
    for banned in ("清军入关", "三藩之乱", "武昌起义"):
        assert not any(banned in e["name_zh_cn"] for e in backbone.events), f"Batch7 内容不应出现: {banned}"


def test_batch6_source_coverage(backbone):
    batch6_new = [e for e in backbone.events if _batch6(e)]
    assert len(batch6_new) >= 82
    for event in batch6_new:
        assert event.get("source_type") == "curated_reference", event["id"]
        assert event.get("source_reference"), event["id"]
        assert event.get("source_ids"), event["id"]
        assert "AI" not in event["source_reference"], event["id"]
        assert any(wid in event["source_ids"] for wid in
                   ("work-curated-yuanshi", "work-curated-mingshi", "work-curated-mingshilu")), event["id"]


def test_batch6_timeline_order(backbone):
    from history_data_pipeline.backbone.timeline import filter_timeline, timeline_record
    rows = [timeline_record(e) for e in filter_timeline(backbone)]
    years = [r["start_year"] for r in rows if r["start_year"] is not None]
    assert years == sorted(years)
    seq = {r["id"]: r["start_year"] for r in rows}
    chain = [("event-yuan-jianguo", 1271), ("event-yuan-zheng-ri-yi", 1274),
             ("event-hongjin-jun-qiyi", 1351), ("event-poyanghu-zhizhan", 1363),
             ("event-zhuyuanzhang-chendi", 1368), ("event-jingnan-zhizhan", 1399),
             ("event-qian-du-beijing", 1421), ("event-tumu-bao-zhibian", 1449),
             ("event-houjin-jianguo", 1616), ("event-saerhu-zhizhan", 1619),
             ("event-lizicheng-gong-beijing", 1644)]
    for eid, year in chain:
        assert eid in seq, f"timeline 缺少 {eid}"
        assert seq[eid] == year, f"{eid} 应为 {year} 实为 {seq[eid]}"