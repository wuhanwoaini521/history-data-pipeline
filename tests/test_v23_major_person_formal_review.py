# -*- coding: utf-8 -*-
"""V2.3 · Major-Event EventPerson 正式审查（agent_assisted）与正式 Backbone 集成。

覆盖：
- 全部 V2.2 machine 候选链接均被 V2.3 裁决覆盖（accept/reject/insufficient 三态，无遗漏）；
- 仅 formal_accepted 进入正式 Backbone；reject/insufficient 仅存在于 reviews/formal 审计层；
- 正式加载层总数 = 200（既有）+ 198（V2.3 净新增）= 398；
- 术语纪律：review 层方法 = agent_assisted_source_review，绝不出现 human_reviewed；
- 关键决策点（event-doujiande-shili 王世充、event-dierci-zhifeng-zhanzheng 孙中山、
  event-guan-yu-bei-fa 孙权 等）拒绝记录存在。
"""
from __future__ import annotations

import importlib.util
import sys
from collections import Counter
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "src"))

MACHINE_DIR = ROOT / "data" / "machine_review" / "event_person_v2_2"
FORMAL_DIR = ROOT / "data" / "curated" / "history_backbone" / "event_person"
REVIEW_DIR = ROOT / "data" / "reviews" / "formal" / "event_person_v2_3"


def _load_engine():
    spec = importlib.util.spec_from_file_location(
        "v23_major_person_formal_review",
        ROOT / "scripts" / "v23_major_person_formal_review.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def engine():
    return _load_engine()


def _machine_people() -> dict[str, dict[str, dict]]:
    out = {}
    for f in sorted(MACHINE_DIR.glob("*.yml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        out[doc["event_id"]] = {p["person_id"]: p for p in doc.get("people", [])}
    return out


def test_every_machine_link_has_review_adjudication(engine):
    """全域裁决：machine 每条候选链接都有 A/R/I 决策（引擎入口还额外 assert 持平）。"""
    r = engine.REVIEW
    total, reviewed = 0, 0
    for eid, people in _machine_people().items():
        spec = r.get(eid, {})
        for pid in people:
            total += 1
            assert pid in spec, f"{eid}/{pid} 无裁决"
        extra = set(spec) - set(people)
        assert not extra, f"{eid} 裁决含 machine 未承载 {extra}"
        reviewed += len(people)
    assert total == 223, total
    assert reviewed == 223


def test_accept_reject_insufficient_tally(engine):
    r = engine.REVIEW
    ver = Counter(r[eid][pid][0] for eid, people in _machine_people().items() for pid in people)
    assert ver["A"] == 208, ver
    assert ver["R"] == 13, ver
    assert ver["I"] == 2, ver


@pytest.mark.parametrize("eid,pid,verdict", [
    ("event-doujiande-shili", "cbdb-person-134932", "R"),
    ("event-guan-yu-bei-fa", "cbdb-person-20609", "R"),
    ("event-dierci-zhifeng-zhanzheng", "curated-person-sun-yat-sen", "R"),
    ("event-agubo-geju", "cbdb-person-54964", "R"),
])
def test_decision_rows(engine, eid, pid, verdict):
    r = engine.REVIEW
    assert pid in _machine_people()[eid], f"{eid} 无 {pid}"
    assert r[eid][pid][0] == verdict, f"{eid}/{pid} 应裁决 {verdict}"


def test_formal_store_only_accept_and_terminology(engine):
    """与 v2_2 同名正式文件必须带 curated_class/agent 声明，且不出现 human_reviewed。"""
    v22_names = {p.stem for p in MACHINE_DIR.glob("*.yml")}
    linked_checked = 0
    for f in sorted(FORMAL_DIR.glob("*.yml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        if f.stem in v22_names:
            assert doc.get("curated_class") == "curated_accepted", f"{f.name} 缺代理接受标记"
            for p in doc.get("people", []):
                note = p.get("review_note") or ""
                assert "human_reviewed" not in note, f"{f.name}: 术语违规"
            linked_checked += 1
    assert linked_checked >= 180


def test_loader_total_398():
    from history_data_pipeline.backbone.loader import load_backbone
    bb = load_backbone(ROOT)
    rows = [p for e in bb.events for p in (e.get("people") or []) if p.get("link_status") == "linked"]
    assert len(rows) == 398


def test_review_records_match_machine_events():
    machine_names = {p.stem for p in MACHINE_DIR.glob("*.yml")}
    review_names = {p.stem for p in REVIEW_DIR.glob("*.yml")}
    assert machine_names == review_names, "review 记录与 machine 事件集不一致"
    assert len(review_names) == 194