"""China History Backbone V1 · Batch 7（清→晚清→辛亥革命）测试。

覆盖：baseline / 后金与李自成入京复用 / 三藩 / 台湾 / 清俄 / 西北 / 鸦片战争 /
太平天国 / 洋务 / 新疆 / 甲午 / 戊戌 / 义和团 / 新政 / 辛亥 / 清帝退位边界 / source / timeline。
"""

from __future__ import annotations

from pathlib import Path

import pytest

from history_data_pipeline.backbone.loader import load_backbone

ROOT = Path(__file__).parents[1]


@pytest.fixture(scope="module")
def backbone():
    return load_backbone(ROOT)


def _batch7(event):
    return "/events/qing/" in event.get("_file", "").replace("\\", "/") \
        or "\\events\\qing\\" in event.get("_file", "")


def test_batch7_backbone_baseline(backbone):
    by_period = {pid: [e for e in backbone.events if e["period_id"] == pid] for pid in
                 {"period-qing", "period-late-qing"}}
    assert len(by_period["period-qing"]) >= 20
    assert len(by_period["period-late-qing"]) >= 30
    names = {e["name_zh_cn"] for e in backbone.events}
    for key in ("清军入关、定鼎北京（山海关之战）", "三藩之乱与平定", "武昌起义"):
        assert key in names, f"缺少 Batch7 关键节点: {key}"
    batch7_new = [e for e in backbone.events if _batch7(e)]
    assert len(batch7_new) >= 66
    assert all(e["importance"] in {"critical", "major"} for e in batch7_new)


def test_qing_boundary_reused(backbone):
    """后金建立（1616）与李自成入京（1644）被复用，不重复建档。"""
    by_id = {e["id"]: e for e in backbone.events}
    assert by_id["event-houjin-jianguo"]["start_year"] == 1616
    assert len([e for e in backbone.events if e["id"] == "event-houjin-jianguo"]) == 1
    assert by_id["event-lizicheng-gong-beijing"]["start_year"] == 1644
    # 清入关以 follows 衔接
    ru = by_id["event-qingjun-ru-guan"]
    assert any(r["target_event_id"] == "event-lizicheng-gong-beijing" for r in ru["relations"])


def test_sanfan_and_taiwan(backbone):
    by_id = {e["id"]: e for e in backbone.events}
    assert by_id["event-sanfan-zhi-luan"]["start_year"] == 1673 and by_id["event-sanfan-zhi-luan"]["end_year"] == 1681
    assert by_id["event-sanfan-zhi-luan"]["importance"] == "critical"
    assert by_id["event-zhengchenggong-qu-taiwan"]["start_year"] == 1661
    assert by_id["event-qing-tongyi-taiwan"]["start_year"] == 1683
    # 台湾统一与清俄
    assert by_id["event-yaquesha-zhizhan"]["start_year"] == 1685
    assert by_id["event-nibuchu-tiaoyue"]["start_year"] == 1689


def test_northwest_and_central(backbone):
    """西北（准噶尔）+ 清代中央政治（军机处/摊丁入亩/改土归流）骨干。"""
    by_id = {e["id"]: e for e in backbone.events}
    for key in ("event-kangxi-zheng-galdan", "event-qianlong-ping-jun",
                "event-junjichu", "event-tanding-rumu", "event-gaituguiliu",
                "event-bailianjiao-qiyi"):
        assert key in by_id, key
    # 无"康乾盛世"式 placeholder 事件（historiographical 概括不可代替事件）
    assert not any("康乾盛世" in e["name_zh_cn"] for e in backbone.events)


def test_opium_and_taiping(backbone):
    by_id = {e["id"]: e for e in backbone.events}
    assert by_id["event-linzexu-jinyan"]["end_year"] == 1839
    assert by_id["event-diyici-yapian-zhanzheng"]["start_year"] == 1840 and by_id["event-diyici-yapian-zhanzheng"]["importance"] == "critical"
    assert by_id["event-nanjing-tiaoyue"]["start_year"] == 1842
    tp = by_id["event-taiping-tianguo"]
    assert tp["start_year"] == 1851 and tp["end_year"] == 1864
    children = {e["id"] for e in backbone.events
                if any(r.get("relation_type") == "part_of" and r.get("target_event_id") == "event-taiping-tianguo"
                       for r in e.get("relations", []))}
    assert children == {"event-jintian-qiyi", "event-dingdu-tianjing", "event-tianjing-shibian", "event-tianjing-xianluo"}
    assert by_id["event-dierci-yapian-zhanzheng"]["start_year"] == 1856 and by_id["event-dierci-yapian-zhanzheng"]["end_year"] == 1860
    assert by_id["event-beijing-tiaoyue"]["start_year"] == 1860


def test_yangwu_and_border(backbone):
    by_id = {e["id"]: e for e in backbone.events}
    assert by_id["event-yangwu-yundong"]["start_year"] == 1861 and by_id["event-yangwu-yundong"]["end_year"] == 1894
    assert "event-beiyang-haijun" in by_id and by_id["event-beiyang-haijun"]["start_year"] == 1888
    assert by_id["event-zuozongtang-xizheng"]["start_year"] == 1876
    assert by_id["event-xinjiang-jiansheng"]["start_year"] == 1884
    assert by_id["event-zhongfa-zhanzheng"]["start_year"] == 1883


def test_jiawu_and_wuxu(backbone):
    by_id = {e["id"]: e for e in backbone.events}
    jw = by_id["event-jiawu-zhanzheng"]
    assert jw["start_year"] == 1894 and jw["importance"] == "critical"
    assert by_id["event-huanghai-haizhan"]["start_year"] == 1894
    assert by_id["event-maguan-tiaoyue"]["start_year"] == 1895
    assert by_id["event-gongche-shangshu"]["start_year"] == 1895
    assert by_id["event-wuxu-bianfa"]["start_year"] == 1898
    # 甲午 summary 不作单因"腐败必败"结论
    assert "腐败" not in jw["summary_zh_cn"]


def test_yihetuan_and_xinzheng(backbone):
    by_id = {e["id"]: e for e in backbone.events}
    assert by_id["event-yihetuan-yundong"]["start_year"] == 1899
    assert by_id["event-baguo-lianjun-ru-jing"]["start_year"] == 1900
    assert by_id["event-xinchou-tiaoyue"]["start_year"] == 1901
    assert by_id["event-qingmo-xinzheng"]["start_year"] == 1901
    assert by_id["event-feichu-keju"]["start_year"] == 1905
    assert by_id["event-yubei-lixian"]["start_year"] == 1906
    # 义和团不加价值标签
    text = by_id["event-yihetuan-yundong"]["summary_zh_cn"] + (by_id["event-yihetuan-yundong"].get("review_note") or "")
    assert "义和团" in text


def test_xinhai_boundary(backbone):
    """本批终点：1912 清帝退位；民国初期为 Batch8。"""
    by_id = {e["id"]: e for e in backbone.events}
    assert by_id["event-wuchang-qiyi"]["start_year"] == 1911 and by_id["event-wuchang-qiyi"]["importance"] == "critical"
    assert by_id["event-qingdi-tuiwei"]["start_year"] == 1912 and by_id["event-qingdi-tuiwei"]["importance"] == "critical"
    for banned in ("五四运动", "九一八事变", "遵义会议"):
        assert not any(banned in e["name_zh_cn"] for e in backbone.events), f"Batch8 内容不应出现: {banned}"


def test_batch7_source_coverage(backbone):
    batch7_new = [e for e in backbone.events if _batch7(e)]
    assert len(batch7_new) >= 66
    for event in batch7_new:
        assert event.get("source_type") == "curated_reference", event["id"]
        assert event.get("source_reference"), event["id"]
        assert event.get("source_ids"), event["id"]
        assert "AI" not in event["source_reference"], event["id"]
        assert any(wid in event["source_ids"] for wid in
                   ("work-curated-qingshigao", "work-curated-qingshilu")), event["id"]


def test_batch7_timeline_order(backbone):
    from history_data_pipeline.backbone.timeline import filter_timeline, timeline_record
    rows = [timeline_record(e) for e in filter_timeline(backbone)]
    years = [r["start_year"] for r in rows if r["start_year"] is not None]
    assert years == sorted(years)
    seq = {r["id"]: r["start_year"] for r in rows}
    chain = [("event-qingjun-ru-guan", 1644), ("event-sanfan-zhi-luan", 1673),
             ("event-nibuchu-tiaoyue", 1689), ("event-diyici-yapian-zhanzheng", 1840),
             ("event-nanjing-tiaoyue", 1842), ("event-jintian-qiyi", 1851),
             ("event-tianjing-xianluo", 1864), ("event-jiawu-zhanzheng", 1894),
             ("event-wuxu-bianfa", 1898), ("event-wuchang-qiyi", 1911),
             ("event-qingdi-tuiwei", 1912)]
    for eid, year in chain:
        assert eid in seq, f"timeline 缺少 {eid}"
        assert seq[eid] == year, f"{eid} 应为 {year} 实为 {seq[eid]}"