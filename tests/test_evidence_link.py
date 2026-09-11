"""Evidence Linking 测试：exact 写回 / fuzzy 只报告 / unmatched 保留。"""

from __future__ import annotations

from pathlib import Path

from history_data_pipeline.backbone.evidence_link import (
    KnowledgeIndex,
    apply_links,
    link_event_evidence,
    match_chapter_by_content,
)


def _index() -> KnowledgeIndex:
    works = {"元史": {"id": "work-niutrans-yuanshi", "title": "元史", "title_zh_cn": "元史"}}
    chapter_index = {
        ("work-niutrans-yuanshi", "卷一"): ("本纪", "卷一"),
        ("work-niutrans-yuanshi", "本纪"): ("本纪", None),
    }
    chapter_anchor = {("work-niutrans-yuanshi", "本纪", "卷一"): "text-niutrans-anchor001"}
    part_first_chapter = {("work-niutrans-yuanshi", "本纪"): "卷一"}
    chapter_heads = {"work-niutrans-yuanshi": [("本纪", "卷一", "◎太祖太祖法天启运圣武皇帝，讳铁木真")]}
    return KnowledgeIndex(works=works, chapter_index=chapter_index,
                          chapter_anchor=chapter_anchor, part_first_chapter=part_first_chapter,
                          chapter_heads=chapter_heads)


ALIASES = {"元史·太祖纪": {"part": "本纪", "chapter": "卷一", "note": "《元史》卷一〈太祖本纪〉（中华书局点校本目录）"}}


def _event(work: str, term: str, event_id: str = "event-test") -> dict:
    return {"id": event_id, "evidence": [{"work": work, "term": term, "evidence_role": "primary",
                                          "historical_text_id": None, "link_status": "needs_linking"}]}


def test_alias_link_result():
    results = list(link_event_evidence([_event("元史", "太祖纪")], _index(), ALIASES))
    assert len(results) == 1
    result = results[0]
    assert result.status == "linked"
    assert result.historical_text_id == "text-niutrans-anchor001"
    assert result.chapter_anchor == "本纪/卷一"
    assert result.match_method == "alias"


def test_exact_part_level_link():
    results = list(link_event_evidence([_event("元史", "本纪")], _index(), {}))
    result = results[0]
    assert result.status == "linked"
    # 卷类级命中 → 锚到该卷类下第一篇卷的首段
    assert result.historical_text_id == "text-niutrans-anchor001"
    assert result.chapter_anchor == "本纪/卷一"


def test_fuzzy_never_links(tmp_path: Path):
    # 与"卷一"相近但非精确的 term → fuzzy，不写回
    events_dir = tmp_path / "events"
    (events_dir / "sub").mkdir(parents=True)
    results = list(link_event_evidence([_event("元史", "卷壹")], _index(), ALIASES))
    assert results[0].status in ("fuzzy_candidate", "unmatched", "needs_manual_review")
    stats = apply_links(events_dir, results, apply=True)
    assert stats["written"] == 0


def test_content_match_ji_zhuan():
    """语料章首行核实：帝纪跨卷（太祖一/二/三）锚定首章；传/志主名前缀核实。"""
    index = _index()
    index.chapter_heads["work-tang"] = [
        ("本纪", "卷六", "则天皇后则天皇后武氏，讳曌，并州文水人也。"),
        ("本纪", "卷一", "高祖高祖神尧大圣大光孝皇帝姓李氏，讳渊。"),
        ("本纪", "卷二", "太宗太宗文武大圣大广孝皇帝，讳世民。"),
    ]
    result = match_chapter_by_content(index, "work-tang", "高祖纪")
    assert result == ("本纪", "卷一")
    result = match_chapter_by_content(index, "work-tang", "则天皇后纪")
    assert result == ("本纪", "卷六")
    # 无命中
    assert match_chapter_by_content(index, "work-tang", "玄宗纪") is None


def test_content_match_spanning_juan():
    """太祖纪 跨 卷一/卷二/卷三（◎太祖一/◎太祖二）→ 锚定首章。"""
    index = _index()
    index.chapter_heads["work-ming"] = [
        ("本纪", "卷三", "◎成祖三十二年春正月"),
        ("本纪", "卷一", "◎太祖一太祖开天行道肇纪立极大圣至神仁文义武俊德成功高皇帝，讳元璋"),
        ("本纪", "卷二", "◎太祖二洪武元年春正月乙亥，祀天地于南郊，即皇帝位。"),
    ]
    result = match_chapter_by_content(index, "work-ming", "太祖纪")
    assert result == ("本纪", "卷一")


def test_fuzzy_with_coordinates_never_links(tmp_path: Path):
    """fuzzy 命中带篇章坐标也绝不写回（AGENTS.md §7 硬规则回归）。"""
    index = _index()
    index.chapter_index[("work-niutrans-yuanshi", "僖宗本纪")] = ("本纪", "卷九")
    events_dir = tmp_path / "events"
    events_dir.mkdir(parents=True)
    event_file = events_dir / "event-fuzzy.yml"
    event_file.write_text(
        "id: event-fuzzy\n"
        "name_zh_cn: 模糊事件\n"
        "evidence:\n"
        "- work: 元史\n"
        "  term: 僖宗纪\n"
        "  historical_text_id: null\n"
        "  link_status: needs_linking\n",
        encoding="utf-8",
    )
    results = list(link_event_evidence(
        [{"id": "event-fuzzy", "evidence": [{"work": "元史", "term": "僖宗纪", "evidence_role": "primary",
                                             "historical_text_id": None, "link_status": "needs_linking"}]}],
        index, {}, knowledge_db=None))
    assert results[0].status == "fuzzy_candidate"
    stats = apply_links(events_dir, results, apply=True)
    assert stats["written"] == 0
    assert "text-niutrans-" not in event_file.read_text(encoding="utf-8")


def test_unmatched_result():
    results = list(link_event_evidence([_event("不存在的书", "某传")], _index(), ALIASES))
    assert results[0].status == "unmatched"
    assert results[0].historical_text_id is None


def test_apply_writes_yaml(tmp_path: Path):
    events_dir = tmp_path / "events" / "song"
    events_dir.mkdir(parents=True)
    event_file = events_dir / "event-test.yml"
    event_file.write_text(
        "id: event-test\n"
        "name_zh_cn: 测试事件\n"
        "evidence:\n"
        "- work: 元史\n"
        "  term: 太祖纪\n"
        "  historical_text_id: null\n"
        "  link_status: needs_linking\n"
        "# event-test — trailing comment\n",
        encoding="utf-8",
    )
    results = list(link_event_evidence(
        [{"id": "event-test", "evidence": [{"work": "元史", "term": "太祖纪", "evidence_role": "primary",
                                            "historical_text_id": None, "link_status": "needs_linking"}]}],
        _index(), ALIASES))
    stats = apply_links(events_dir, results, apply=True)
    assert stats["written"] == 1
    text = event_file.read_text(encoding="utf-8")
    assert "text-niutrans-anchor001" in text
    assert "link_status: linked" in text
    assert "chapter_anchor: 本纪/卷一" in text
    assert "trailing comment" in text  # 尾部注释保留
    assert "link_method: alias" in text
