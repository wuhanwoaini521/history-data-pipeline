"""China History Backbone V1 · Batch 3（东汉末→三国→西晋→东晋/十六国→南北朝→隋统一）测试。

覆盖 §55 要求：baseline / 三国既有复用 / 黄巾复用 / 官渡、赤壁无重复 /
三国并行 Regime / 东晋十六国并行 / 南北朝并行 / 北魏分裂结构 / 隋统一边界 /
source coverage / timeline order。
"""

from __future__ import annotations

from pathlib import Path

import pytest

from history_data_pipeline.backbone.loader import load_backbone

ROOT = Path(__file__).parents[1]


@pytest.fixture(scope="module")
def backbone():
    return load_backbone(ROOT)


BATCH3_DIRS = ("three_kingdoms", "jin_southern_northern")
REUSED_THREE = {
    "event-three-yellow-turbans", "event-three-dong-zhuo", "event-three-guandu",
    "event-three-north-consolidation", "event-three-jingzhou-change",
    "event-three-sun-liu-alliance", "event-three-chibi", "event-three-regime-formation",
}


def _is_batch3(event):
    return any(d in event.get("_file", "") for d in BATCH3_DIRS)


def test_batch3_backbone_baseline(backbone):
    """各时期组均有 backbone（数量下限 + 关键节点在场）+ 新 Event 只维护 critical/major。"""
    by_period = {pid: [e for e in backbone.events if e["period_id"] == pid] for pid in
                 {"period-late-eastern-han", "period-three-kingdoms", "period-western-jin",
                  "period-eastern-jin", "period-sixteen-kingdoms", "period-northern-southern", "period-sui"}}
    assert len(by_period["period-late-eastern-han"]) >= 15
    assert len(by_period["period-three-kingdoms"]) >= 14
    assert len(by_period["period-western-jin"]) >= 12
    assert len(by_period["period-eastern-jin"]) >= 8
    assert len(by_period["period-sixteen-kingdoms"]) >= 13
    assert len(by_period["period-northern-southern"]) >= 25
    assert len(by_period["period-sui"]) >= 1
    names = {e["name_zh_cn"] for e in backbone.events}
    for key in ("曹丕代汉、曹魏建立", "八王之乱", "永嘉之乱", "东晋建立", "淝水之战",
                "北魏统一北方（灭北凉）", "北魏分裂为东魏西魏", "侯景之乱",
                "北周灭北齐", "杨坚代北周、隋朝建立", "隋灭陈、隋统一"):
        assert key in names, f"缺少 Batch3 关键节点: {key}"
    batch3_new = [e for e in backbone.events if _is_batch3(e) and e["id"] not in REUSED_THREE]
    assert all(e["importance"] in {"critical", "major"} for e in batch3_new)


def test_three_kingdoms_existing_events_reused(backbone):
    by_id = {e["id"]: e for e in backbone.events}
    for eid in REUSED_THREE:
        assert eid in by_id, f"缺失既有 Event: {eid}"
    for keyword in ("官渡", "赤壁"):
        matches = [e for e in backbone.events if keyword in e["name_zh_cn"]]
        assert len(matches) == 1, f"{keyword} 事件应唯一: {[e['id'] for e in matches]}"


def test_yellow_turban_reused(backbone):
    matches = [e for e in backbone.events if "黄巾" in e["name_zh_cn"]]
    assert len(matches) == 1 and matches[0]["id"] == "event-three-yellow-turbans"
    assert matches[0]["start_year"] == 184


def test_guandu_no_duplicate(backbone):
    names = [e["name_zh_cn"] for e in backbone.events]
    assert names.count("官渡之战") == 1
    assert not any("event-guandu" in e["id"] and e["id"] != "event-three-guandu" for e in backbone.events)


def test_chibi_no_duplicate(backbone):
    names = [e["name_zh_cn"] for e in backbone.events]
    assert names.count("赤壁之战") == 1
    assert not any("chibi" in e["id"] and e["id"] != "event-three-chibi" for e in backbone.events)


def test_regime_parallel_three_kingdoms(backbone):
    """三国 Regime 并行：曹魏/蜀汉/东吴 同属 period-three-kingdoms，非串行。"""
    regimes = {r["id"]: r for r in backbone.regimes}
    for rid in ("regime-cao-wei", "regime-shu-han", "regime-eastern-wu"):
        assert rid in regimes and regimes[rid]["period_id"] == "period-three-kingdoms"
    by_id = {e["id"]: e for e in backbone.events}
    assert "regime-cao-wei" in by_id["event-caopi-dai-han"]["regime_ids"]
    assert "regime-shu-han" in by_id["event-liubei-chengdi"]["regime_ids"]
    assert "regime-eastern-wu" in by_id["event-sunquan-chengdi"]["regime_ids"]
    assert set(by_id["event-yiling-zhizhan"]["regime_ids"]) == {"regime-shu-han", "regime-eastern-wu"}


def test_eastern_jin_sixteen_kingdoms_parallel(backbone):
    """东晋/十六国 并行：东晋与前秦等并存；淝水之战双政权并列；时间轴交错。"""
    regimes = {r["id"]: r for r in backbone.regimes}
    assert regimes["regime-eastern-jin"]["period_id"] == "period-eastern-jin"
    for rid in ("regime-han-zhao", "regime-later-zhao", "regime-former-qin"):
        assert regimes[rid]["period_id"] == "period-sixteen-kingdoms"
    by_id = {e["id"]: e for e in backbone.events}
    assert set(by_id["event-feishui-zhizhan"]["regime_ids"]) == {"regime-eastern-jin", "regime-former-qin"}
    from history_data_pipeline.backbone.timeline import filter_timeline
    rows = [e for e in filter_timeline(backbone) if e["start_year"] and 317 <= e["start_year"] <= 439]
    periods = {r["period_id"] for r in rows}
    assert {"period-eastern-jin", "period-sixteen-kingdoms"} <= periods


def test_northern_southern_regime_parallel(backbone):
    """南北朝 Regime 并行：南朝（宋/齐/梁/陈）∥ 北朝（北魏/东魏/西魏/北齐/北周）。"""
    regimes = {r["id"]: r for r in backbone.regimes}
    for rid in ("regime-liu-song", "regime-southern-qi", "regime-liang", "regime-chen",
                "regime-northern-wei", "regime-eastern-wei", "regime-western-wei",
                "regime-northern-qi", "regime-northern-zhou"):
        assert rid in regimes, rid
        assert regimes[rid]["period_id"] == "period-northern-southern"
    by_id = {e["id"]: e for e in backbone.events}
    assert set(by_id["event-beizhou-mie-beiqi"]["regime_ids"]) == {"regime-northern-zhou", "regime-northern-qi"}
    assert set(by_id["event-zhongli-zhizhan"]["regime_ids"]) == {"regime-liang", "regime-northern-wei"}


def test_northern_wei_split_structure(backbone):
    """北魏分裂结构：东魏/西魏 parent=北魏；北齐/北周 分别继承东魏/西魏（非串行）。"""
    regimes = {r["id"]: r for r in backbone.regimes}
    assert regimes["regime-eastern-wei"]["parent_regime_id"] == "regime-northern-wei"
    assert regimes["regime-western-wei"]["parent_regime_id"] == "regime-northern-wei"
    assert regimes["regime-northern-qi"]["parent_regime_id"] == "regime-eastern-wei"
    assert regimes["regime-northern-zhou"]["parent_regime_id"] == "regime-western-wei"
    by_id = {e["id"]: e for e in backbone.events}
    assert {"regime-eastern-wei", "regime-western-wei"} <= set(by_id["event-beiwei-fenlie"]["regime_ids"])
    assert by_id["event-beiwei-fenlie"]["importance"] == "critical"


def test_sui_unification_boundary(backbone):
    """隋统一边界：581 隋建立、589 隋灭陈统一；无 隋炀帝/唐朝 等 Batch4 内容。"""
    by_id = {e["id"]: e for e in backbone.events}
    assert "event-yangjian-dai-beizhou" in by_id and "event-sui-mie-chen" in by_id
    assert by_id["event-yangjian-dai-beizhou"]["start_year"] == 581
    assert by_id["event-sui-mie-chen"]["start_year"] == 589
    assert by_id["event-sui-mie-chen"]["importance"] == "critical"
    # Batch3 边界：不得进入 Batch8（民国）内容（清为 Batch7 范围）
    for banned in ("抗美援朝", "改革开放", "文化大革命"):
        assert not any(banned in e["name_zh_cn"] for e in backbone.events), f"V2(1950+) 内容不应出现: {banned}"


def test_batch3_source_coverage(backbone):
    """Batch3 新增 Event 100% 携带 source_reference + source_ids（两层来源链），无 AI Source。"""
    batch3_new = [e for e in backbone.events if _is_batch3(e) and e["id"] not in REUSED_THREE]
    assert len(batch3_new) >= 89
    for event in batch3_new:
        assert event.get("source_type") == "curated_reference", event["id"]
        assert event.get("source_reference"), event["id"]
        assert event.get("source_ids"), event["id"]
        assert "AI" not in event["source_reference"], event["id"]


def test_batch3_timeline_order(backbone):
    """Batch3 timeline：按 start_year 升序；关键节点链 184→189→…→280→311→383→439→534→577→581→589。"""
    from history_data_pipeline.backbone.timeline import filter_timeline, timeline_record
    rows = [timeline_record(e) for e in filter_timeline(backbone)]
    years = [r["start_year"] for r in rows if r["start_year"] is not None]
    assert years == sorted(years)
    seq = {r["id"]: r["start_year"] for r in rows}
    chain = [("event-three-yellow-turbans", 184), ("event-three-dong-zhuo", 189),
             ("event-jin-mie-wu", 280), ("event-yongjia-zhi-luan", 311),
             ("event-dongjin-jianguo", 317), ("event-feishui-zhizhan", 383),
             ("event-beiwei-tongyi-beifang", 439), ("event-beiwei-fenlie", 534),
             ("event-beizhou-mie-beiqi", 576),  # 攻邺灭齐（576—577）
             ("event-yangjian-dai-beizhou", 581),
             ("event-sui-mie-chen", 589)]
    for eid, year in chain:
        assert eid in seq, f"timeLine 缺少 {eid}"
        assert seq[eid] == year, f"{eid} 应为 {year} 实为 {seq[eid]}"