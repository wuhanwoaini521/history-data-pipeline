"""China History Backbone V1 · Batch 8（中华民国→近现代 1912—1949）测试。

覆盖：baseline / 南京临时政府复用 / 民国初期 / 五四 / 军阀 / 国民革命 / 中共早期 /
九一八 / 全面抗战 / 南京大屠杀中性书写 / 1949 边界 / source 双层链 / timeline。
"""

from __future__ import annotations

from pathlib import Path

import pytest

from history_data_pipeline.backbone.loader import load_backbone

ROOT = Path(__file__).parents[1]


@pytest.fixture(scope="module")
def backbone():
    return load_backbone(ROOT)


def _batch8(event):
    return "/events/modern/" in event.get("_file", "").replace("\\", "/")


def test_batch8_backbone_baseline(backbone):
    by_period = {pid: [e for e in backbone.events if e["period_id"] == pid] for pid in
                 {"period-republic", "period-modern"}}
    assert len(by_period["period-republic"]) >= 40
    assert len(by_period["period-modern"]) >= 1
    names = {e["name_zh_cn"] for e in backbone.events}
    for key in ("五四运动", "九一八事变（沈阳）", "七七事变（卢沟桥事变）",
                "日本宣布投降（抗日战争胜利）", "中华人民共和国成立"):
        assert key in names, f"缺少 Batch8 关键节点: {key}"
    batch8_new = [e for e in backbone.events if _batch8(e)]
    assert len(batch8_new) >= 52
    assert all(e["importance"] in {"critical", "major"} for e in batch8_new)


def test_nanjing_linshi_reused(backbone):
    """1912-01-01 南京临时政府（Batch7）复用为民国起点前节点。"""
    by_id = {e["id"]: e for e in backbone.events}
    assert by_id["event-nanjing-linshi-zhengfu"]["start_year"] == 1912
    assert len([e for e in backbone.events if e["id"] == "event-nanjing-linshi-zhengfu"]) == 1
    # 袁世凯就任衔接
    assert any(r["target_event_id"] == "event-nanjing-linshi-zhengfu"
               for r in by_id["event-yuanshikai-jiuwei"]["relations"])


def test_early_republic_chain(backbone):
    by_id = {e["id"]: e for e in backbone.events}
    chain = [("event-yuanshikai-jiuwei", 1912), ("event-songjiaoren-yuci", 1913),
             ("event-erci-geming", 1913), ("event-yuanshikai-chendi", 1915),
             ("event-huguo-zhanzheng", 1915), ("event-yuanshikai-qushi", 1916)]
    for eid, year in chain:
        assert by_id[eid]["start_year"] == year, eid


def test_warlord_and_may4th(backbone):
    by_id = {e["id"]: e for e in backbone.events}
    for key in ("event-fuyuan-zhi-zheng", "event-zhangxun-fubi", "event-hufa-yundong",
                "event-zhiwan-zhanzheng", "event-diyici-zhifeng-zhanzheng",
                "event-dierci-zhifeng-zhanzheng", "event-bali-hehui"):
        assert key in by_id, key
    wusi = by_id["event-wusi-yundong"]
    assert wusi["start_year"] == 1919 and wusi["importance"] == "critical"
    # 五四 summary 不写"开启新民主主义革命"等特定理论框架
    assert "新民主主义" not in wusi["summary_zh_cn"]


def test_national_rev(backbone):
    by_id = {e["id"]: e for e in backbone.events}
    assert by_id["event-guomindang-gaizu"]["start_year"] == 1924
    assert by_id["event-huangpu-junxiao"]["start_year"] == 1924
    assert by_id["event-guomin-gemingjun-beifa"]["start_year"] == 1926
    assert by_id["event-nanjing-guominzhengfu"]["start_year"] == 1927
    assert by_id["event-dongbei-yizhi"]["start_year"] == 1928
    fl = by_id["event-guogong-fenlie-1927"]
    assert fl["start_year"] == 1927 and "清党" in fl["summary_zh_cn"]


def test_cpc_early_nodes(backbone):
    by_id = {e["id"]: e for e in backbone.events}
    assert by_id["event-zggcd-chengli"]["start_year"] == 1921
    assert by_id["event-nanchang-qiyi"]["start_year"] == 1927
    assert by_id["event-qiushou-qiyi"]["start_year"] == 1927
    assert by_id["event-zhonghua-suweiai"]["start_year"] == 1931
    cz = by_id["event-changzheng"]
    assert cz["start_year"] == 1934 and cz["end_year"] == 1936
    assert by_id["event-zunyi-huiyi"]["start_year"] == 1935
    assert any(r.get("relation_type") == "part_of" and r.get("target_event_id") == "event-changzheng"
               for r in by_id["event-zunyi-huiyi"]["relations"])


def test_japan_invasion(backbone):
    by_id = {e["id"]: e for e in backbone.events}
    assert by_id["event-jiuyiba-shibian"]["start_year"] == 1931 and by_id["event-jiuyiba-shibian"]["importance"] == "critical"
    assert by_id["event-manzhouguo-jianli"]["start_year"] == 1932
    assert by_id["event-yi-er-ba-shibian"]["start_year"] == 1932
    assert by_id["event-huabei-shibian"]["start_year"] == 1935
    assert by_id["event-xian-shibian"]["start_year"] == 1936 and by_id["event-xian-shibian"]["importance"] == "critical"
    # 满洲国 Regime 表达
    regimes = {r["id"]: r for r in backbone.regimes}
    assert "regime-manchukuo" in regimes


def test_full_war_and_nanjing(backbone):
    by_id = {e["id"]: e for e in backbone.events}
    assert by_id["event-qiqishi-bian"]["start_year"] == 1937 and by_id["event-qiqishi-bian"]["importance"] == "critical"
    assert by_id["event-songhu-huizhan"]["start_year"] == 1937
    assert by_id["event-nanjing-baoweizhan"]["start_year"] == 1937
    nd = by_id["event-nanjing-datusha"]
    assert nd["start_year"] == 1937 and nd["importance"] == "critical"
    import json as _json
    note = _json.loads((ROOT / "data" / "reviews" / "accepted" / "event-nanjing-datusha.review.json")
                       .read_text(encoding="utf-8")).get("note") or ""
    # 中性：直述事实，无煽动性修辞，记统计口径差异
    assert "统计口径" in note and "南京大屠杀" in nd["summary_zh_cn"]
    for key in ("event-wuhan-huizhan", "event-changsha-huizhan", "event-baidatuan",
                "event-yuanzhengjun", "event-yuxianggui"):
        assert key in by_id, key
    assert by_id["event-riben-touxiang"]["start_year"] == 1945 and by_id["event-riben-touxiang"]["importance"] == "critical"
    assert by_id["event-taiwan-guangfu"]["start_year"] == 1945


def test_1949_boundary(backbone):
    """本批终点：1949-10-01 中华人民共和国成立（modern boundary）；1950+ 不展开。"""
    by_id = {e["id"]: e for e in backbone.events}
    xzg = by_id["event-xinzhongguo-chengli"]
    assert xzg["start_year"] == 1949 and xzg["importance"] == "critical"
    assert xzg["period_id"] == "period-modern"
    for key in ("event-chongqing-tanpan", "event-zhengzhi-xieshang-huiyi",
                "event-quanmian-neizhan", "event-liaoshen-zhanyi", "event-huaihai-zhanyi",
                "event-pingjin-zhanyi", "event-dujiang-nanjing"):
        assert key in by_id, key
    for banned in ("抗美援朝", "改革开放", "文化大革命", "香港回归"):
        assert not any(banned in e["name_zh_cn"] for e in backbone.events), f"V2(1950+) 内容不应出现: {banned}"


def test_batch8_source_coverage(backbone):
    """§65：1912—1949 每条需档案/史料类 + 现代权威研究双层来源。"""
    batch8_new = [e for e in backbone.events if _batch8(e)]
    assert len(batch8_new) >= 52
    for event in batch8_new:
        assert event.get("source_type") == "curated_reference", event["id"]
        sr = event.get("source_reference") or ""
        assert sr, event["id"]
        assert "档案" in sr or "史料" in sr or "公报" in sr or "文本" in sr or "纪录" in sr, event["id"]
        assert "AI" not in sr, event["id"]
        assert event.get("source_ids"), event["id"]


def test_batch8_timeline_order(backbone):
    from history_data_pipeline.backbone.timeline import filter_timeline, timeline_record
    rows = [timeline_record(e) for e in filter_timeline(backbone)]
    years = [r["start_year"] for r in rows if r["start_year"] is not None]
    assert years == sorted(years)
    seq = {r["id"]: r["start_year"] for r in rows}
    chain = [("event-yuanshikai-jiuwei", 1912), ("event-wusi-yundong", 1919),
             ("event-zggcd-chengli", 1921), ("event-guomin-gemingjun-beifa", 1926),
             ("event-jiuyiba-shibian", 1931), ("event-xian-shibian", 1936),
             ("event-qiqishi-bian", 1937), ("event-nanjing-datusha", 1937),
             ("event-riben-touxiang", 1945), ("event-liaoshen-zhanyi", 1948),
             ("event-xinzhongguo-chengli", 1949)]
    for eid, year in chain:
        assert eid in seq, f"timeline 缺少 {eid}"
        assert seq[eid] == year, f"{eid} 应为 {year} 实为 {seq[eid]}"