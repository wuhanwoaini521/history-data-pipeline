# -*- coding: utf-8 -*-
"""V2.2 Major EventPerson linking — machine-layer gate tests.

覆盖：确定性自动链接规则（唯一时窗存活）、审阅排除项强制不链接、
以及 V2.2 专用层与正式 (V1/V2.1) event_person store 不产生文件冲突。
不依赖落盘产物（在内存中复算 classify），保持测试对数据变化稳定。
"""
import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

MOD = ROOT / "scripts" / "v22_major_person_links.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("v22_major_person_links", MOD)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def v22():
    m = _load_module()
    m.index = m.NameIndex()
    return m


def _ev(stub: dict) -> dict:
    base = {"name_zh_cn": "测试事件", "summary_zh_cn": "", "start_year": 600, "end_year": 600}
    base.update(stub)
    return base


def test_exact_unique_link_accepted(v22):
    e = _ev({"name_zh_cn": "柏举之战", "summary_zh_cn": "前506年吴国伍子胥辅助孙武伐楚，攻入郢都。",
             "start_year": -506, "end_year": -506})
    res = v22.classify(v22.index, e)
    info = res.get("伍子胥")
    assert info and info["enough"]
    blk = v22.make_block(e, "伍子胥", info)
    assert blk["person_id"] == "ctext-person-6646198"
    assert blk["resolution"] == "exact"
    assert blk["review_note"].endswith("china-history-backbone-v2.2-machine")


def test_review_excluded_never_accepted(v22):
    """审阅排除表（地方/年号/助词等）强制不产链接。"""
    assert v22.EXCLUDED_BY_REVIEW
    for eid, (name, reason) in v22.EXCLUDED_BY_REVIEW.items():
        # 排除表语义：即使名字在候选宇宙中真的命中，也必须记录为 excluded_by_review。
        # 注入 stub 人名（不依赖 legacy KB 是否存在同名噪声候选）。
        stub = {"id": f"stub-{name}", "canonical": name, "birth": None, "death": None, "has_years": False}
        v22.index.persons.setdefault(stub["id"], stub)
        v22.index._put(name, stub)
        e = _ev({"id": eid, "name_zh_cn": "事件",
                 "summary_zh_cn": f"……{name}……", "start_year": 1000, "end_year": 1100})
        res = v22.classify(v22.index, e)
        accept, unlinked = v22.decide(e, res)
        by = {u["person_name_raw"]: u for u in unlinked}
        assert name not in {b["person_name_raw"] for b in accept}, f"{eid}: {name} 不应被接受"
        assert name in by and by[name]["resolution"] == "excluded_by_review", f"{eid}: {name} 应记录为排除"


def test_place_noise_not_linked(v22):
    """「中都」为地名的三个事件不得生成中都链接。"""
    for eid in ("event-jin-qian-du-bian", "event-yefengling-zhizhan", "event-yuan-dingdu-dadu"):
        assert eid in v22.EXCLUDED_BY_REVIEW
    e = _ev({"id": "event-yefengling-zhizhan", "name_zh_cn": "野狐岭之战",
             "summary_zh_cn": "蒙古败金于野狐岭，中都震动。", "start_year": 1211, "end_year": 1211})
    res = v22.classify(v22.index, e)
    accept, _ = v22.decide(e, res)
    assert not {b["person_name_raw"] for b in accept} & {"中都"}


def test_v22_store_dir_never_collides_with_formal(v22):
    formal = ROOT / "data" / "curated" / "history_backbone" / "event_person"
    v22_store = ROOT / "data" / "machine_review" / "event_person_v2_2"
    # 机器层目录与正式目录命名空间隔离（loader 只扫正式目录）
    assert v22_store != formal
    # 机器层不直接写正式层：凡与 v2_2 候选同名正式文件，必须携带 V2.3 策展标记
    import yaml
    for f in sorted(formal.glob("*.yml")):
        if f.stem in {p.stem for p in v22_store.glob("*.yml")}:
            doc = yaml.safe_load(f.read_text(encoding="utf-8"))
            assert doc.get("curated_class") == "curated_accepted", f"{f.name} 缺 V2.3 策展标记"
            note = " ".join(p.get("review_note", "") for p in doc.get("people", []))
            assert "agent_assisted_source_review" in note or "agent_assisted" in note, f"{f.name} 缺少 agent_assisted 复核声明"
            assert "human_reviewed" not in note, f"{f.name} 不得声称 human_reviewed"


def test_curated_era_person_via_curated_id(v22):
    e = _ev({"name_zh_cn": "贾后干政", "summary_zh_cn": "贾南风专权。",
             "start_year": 291, "end_year": 300})
    res = v22.classify(v22.index, e)
    info = res.get("贾南风")
    assert info and info["enough"]
    assert info["canonical"] == "贾南风"