"""China History Backbone V1 · Batch 4（隋→唐→五代十国）测试。

覆盖 §53：baseline / 隋统一复用 / 安史复用 / 无安史重复 / 唐建 / 武周 Regime /
唐亡 / 五代序列 / 十国并行 / 辽并行 / source coverage / timeline order。
"""

from __future__ import annotations

from pathlib import Path

import pytest

from history_data_pipeline.backbone.loader import load_backbone

ROOT = Path(__file__).parents[1]

ANLU_EVENTS = {
    "event-anlu-three-frontiers", "event-anlu-uprising", "event-anlu-luoyang",
    "event-anlu-tongguan", "event-anlu-changan", "event-anlu-xuanzong-shu",
    "event-anlu-changan-recapture", "event-anlu-shi-siming", "event-anlu-pacification",
}

FIVE_DYNASTIES = ("regime-later-liang", "regime-later-tang", "regime-later-jin",
                  "regime-later-han", "regime-later-zhou")


@pytest.fixture(scope="module")
def backbone():
    return load_backbone(ROOT)


def _batch4(event):
    return "sui_tang" in event.get("_file", "") or "five_dynasties" in event.get("_file", "")


def test_batch4_backbone_baseline(backbone):
    """隋/唐/五代十国各时期组有 backbone（数量下限 + 关键节点在场）。"""
    by_period = {pid: [e for e in backbone.events if e["period_id"] == pid] for pid in
                 {"period-sui", "period-tang", "period-five-dynasties-ten-kingdoms", "period-liao"}}
    assert len(by_period["period-sui"]) >= 20
    assert len(by_period["period-tang"]) >= 20
    assert len(by_period["period-five-dynasties-ten-kingdoms"]) >= 15
    assert len(by_period["period-liao"]) >= 1
    names = {e["name_zh_cn"] for e in backbone.events}
    for key in ("李渊称帝、唐朝建立", "玄武门之变", "武则天称帝、武周建立",
                "黄巢起义", "朱温废哀帝、后梁建立、唐朝灭亡", "郭威代汉、后周建立"):
        assert key in names, f"缺少 Batch4 关键节点: {key}"
    batch4_new = [e for e in backbone.events if _batch4(e) and e["id"] not in ANLU_EVENTS]
    assert len(batch4_new) >= 88
    assert all(e["importance"] in {"critical", "major"} for e in batch4_new)


def test_sui_existing_unification_reused(backbone):
    """581 隋建立 / 589 隋灭陈统一 复用既有（不新建）。"""
    by_id = {e["id"]: e for e in backbone.events}
    assert "event-yangjian-dai-beizhou" in by_id and by_id["event-yangjian-dai-beizhou"]["start_year"] == 581
    assert "event-sui-mie-chen" in by_id and by_id["event-sui-mie-chen"]["start_year"] == 589
    assert len([e for e in backbone.events if "隋" in e["name_zh_cn"] and "统一" in e["name_zh_cn"]]) == 1


def test_an_lushan_story_events_reused(backbone):
    """安史之乱 Story 9 个既有 Event 原样复用。"""
    by_id = {e["id"]: e for e in backbone.events}
    for eid in ANLU_EVENTS:
        assert eid in by_id, f"缺失安史既有 Event: {eid}"
        assert by_id[eid]["quality_status"] == "reviewed"


def test_no_duplicate_an_lushan_events(backbone):
    """不得出现 event-anlu-*-v2/-new 式重复。"""
    ids = [e["id"] for e in backbone.events]
    assert all(not (eid.startswith("event-anlu") and eid not in ANLU_EVENTS) for eid in ids)
    assert ids.count("event-anlu-uprising") == 1


def test_tang_foundation(backbone):
    """唐朝建立 618 + 隋→唐 转换清楚（唐建连接 隋亡）。"""
    by_id = {e["id"]: e for e in backbone.events}
    tang = by_id["event-tang-jianguo"]
    assert tang["start_year"] == 618 and tang["importance"] == "critical"
    assert "regime-tang" in tang["regime_ids"]
    # 隋亡（江都兵变炀帝被杀）为前一节点
    assert "event-jiangdu-bingbian" in by_id and by_id["event-jiangdu-bingbian"]["start_year"] == 618


def test_wu_zhou_regime(backbone):
    """武周 Regime 独立表达：regime-wu-zhou 存在、Period 仍属唐。"""
    regimes = {r["id"]: r for r in backbone.regimes}
    assert "regime-wu-zhou" in regimes
    assert regimes["regime-wu-zhou"]["period_id"] == "period-tang"
    by_id = {e["id"]: e for e in backbone.events}
    assert "regime-wu-zhou" in by_id["event-wu-zhou-jianguo"]["regime_ids"]
    assert by_id["event-wu-zhou-jianguo"]["start_year"] == 690
    # 神龙政变恢复唐
    assert "regime-wu-zhou" in by_id["event-shenlong-zhengbian"]["regime_ids"]


def test_tang_fall(backbone):
    """唐亡：907 后梁建立（含唐亡 outcome）。"""
    by_id = {e["id"]: e for e in backbone.events}
    assert "event-houliang-dai-tang" in by_id
    assert by_id["event-houliang-dai-tang"]["start_year"] == 907
    assert by_id["event-houliang-dai-tang"]["importance"] == "critical"
    assert "regime-later-liang" in by_id["event-houliang-dai-tang"]["regime_ids"]


def test_five_dynasties_regime_sequence(backbone):
    """五代 5 Regime 均存在且同属 period-five-dynasties-ten-kingdoms。"""
    regimes = {r["id"]: r for r in backbone.regimes}
    for rid in FIVE_DYNASTIES:
        assert rid in regimes, rid
        assert regimes[rid]["period_id"] == "period-five-dynasties-ten-kingdoms"
    # 五代关键更替事件链
    by_id = {e["id"]: e for e in backbone.events}
    for eid in ("event-houliang-dai-tang", "event-hou-tang-jianguo", "event-shi-jingtang-dai-tang",
                "event-liuzhiyuan-jianhan", "event-guo-wei-dai-han"):
        assert eid in by_id, eid


def test_five_dynasties_parallel_ten_kingdoms(backbone):
    """十国并行：南唐/吴越/前蜀/后蜀/北汉等 Regime 与五代同期并存（独立 Regime 行）。"""
    regimes = {r["id"]: r for r in backbone.regimes}
    for rid in ("regime-wu", "regime-southern-tang", "regime-wuyue", "regime-chu", "regime-min",
                "regime-former-shu", "regime-later-shu", "regime-southern-han", "regime-jingnan",
                "regime-northern-han"):
        assert rid in regimes, rid
        assert regimes[rid]["period_id"] == "period-five-dynasties-ten-kingdoms"
    # 南唐建立事件存在（十国并有事件节点）
    by_id = {e["id"]: e for e in backbone.events}
    assert "event-nan-tang-jianli" in by_id and by_id["event-nan-tang-jianli"]["start_year"] == 937
    # 后周征南唐双政权并列
    assert set(by_id["event-houzhou-nanzheng"]["regime_ids"]) == {"regime-later-zhou", "regime-southern-tang"}


def test_liao_parallel_five_dynasties(backbone):
    """契丹/辽 与五代并行：regime-liao 存在于 taxonomy，且有并行事件。"""
    regimes = {r["id"]: r for r in backbone.regimes}
    assert "regime-liao" in regimes
    by_id = {e["id"]: e for e in backbone.events}
    assert "event-qidan-jianguo" in by_id  # 阿保机建契丹
    assert "event-qidan-mie-houjin" in by_id  # 契丹灭后晋
    assert set(by_id["event-qidan-mie-houjin"]["regime_ids"]) == {"regime-liao", "regime-later-jin"}
    assert set(by_id["event-yan-yun-shiliuzhou"]["regime_ids"]) == {"regime-later-jin", "regime-liao"}


def test_batch4_source_coverage(backbone):
    """Batch4 新增 Event 100% 携带 source_reference + source_ids。"""
    batch4_new = [e for e in backbone.events if _batch4(e) and e["id"] not in ANLU_EVENTS]
    assert len(batch4_new) >= 88
    for event in batch4_new:
        assert event.get("source_type") == "curated_reference", event["id"]
        assert event.get("source_reference"), event["id"]
        assert event.get("source_ids"), event["id"]
        assert "AI" not in event["source_reference"], event["id"]


def test_batch4_timeline_order(backbone):
    """Batch4 timeline：按 start_year 升序；关键链 589→618→626→630→690→705→755→763→875→907→923→936→947→951→956 前。"""
    from history_data_pipeline.backbone.timeline import filter_timeline, timeline_record
    rows = [timeline_record(e) for e in filter_timeline(backbone)]
    years = [r["start_year"] for r in rows if r["start_year"] is not None]
    assert years == sorted(years)
    seq = {r["id"]: r["start_year"] for r in rows}
    chain = [("event-sui-mie-chen", 589), ("event-tang-jianguo", 618),
             ("event-xuanwumen-zhibian", 626), ("event-tang-mie-dong-tujue", 630),
             ("event-wu-zhou-jianguo", 690), ("event-shenlong-zhengbian", 705),
             ("event-anlu-uprising", 755), ("event-anlu-pacification", 763),
             ("event-huangchao-qiyi", 875), ("event-houliang-dai-tang", 907),
             ("event-hou-tang-jianguo", 923), ("event-shi-jingtang-dai-tang", 936),
             ("event-liuzhiyuan-jianhan", 947), ("event-guo-wei-dai-han", 951)]
    for eid, year in chain:
        assert eid in seq, f"timeline 缺少 {eid}"
        assert seq[eid] == year, f"{eid} 应为 {year} 实为 {seq[eid]}"