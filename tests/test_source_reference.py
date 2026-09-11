"""source_reference 归一化与分级匹配测试（Knowledge Layer V2）。"""

from __future__ import annotations

import pytest

from history_data_pipeline.backbone.source_reference import (
    CitationResolver,
    cjk_numeral_to_int,
    int_to_cjk_numeral,
    normalize_locator,
    normalize_term,
    normalize_work_title,
    parse_citations,
    parse_locator,
)


def test_cjk_numeral_roundtrip():
    assert cjk_numeral_to_int("十二") == 12
    assert cjk_numeral_to_int("一") == 1
    assert cjk_numeral_to_int("二十七") == 27
    assert cjk_numeral_to_int("一百零三") == 103
    assert int_to_cjk_numeral(12) == "十二"
    assert int_to_cjk_numeral(27) == "二十七"
    assert int_to_cjk_numeral(0) is None


@pytest.mark.parametrize(
    "text,expected",
    [
        ("第十二章", ("章", 12)),
        ("第12章", ("章", 12)),
        ("十二章", ("章", 12)),
        ("卷十二", ("卷", 12)),
        ("卷12", ("卷", 12)),
        ("Chapter 12", ("章", 12)),
        ("chapter 3", ("章", 3)),
        ("卷一百九十三", ("卷", 193)),
    ],
)
def test_parse_locator_forms(text, expected):
    locator = parse_locator(text)
    assert locator is not None
    assert (locator.kind, locator.value) == expected
    assert normalize_locator(text) == expected


def test_parse_locator_unknown():
    assert parse_locator("某传") is None
    assert parse_locator("") is None


def test_parse_citations_basic():
    refs = "古代史料：《元史·太祖纪》；《蒙古秘史》；现代参考：韩儒林主编《元朝史》（人民出版社）"
    citations = parse_citations(refs)
    assert [c.work_raw for c in citations] == ["元史", "蒙古秘史", "元朝史"]
    assert citations[0].term_raw == "太祖纪"
    assert citations[1].term_raw is None
    assert citations[2].term_raw is None


def test_parse_citations_fullwidth_and_locator():
    citations = parse_citations("《资治通鉴．卷第十二》")
    assert len(citations) == 1
    assert citations[0].work_raw == "资治通鉴"
    # 全角句点被归一成 · 后拆出 term
    assert citations[0].term_raw in ("卷第十二", "第十二")


def test_normalize_helpers():
    assert normalize_work_title("《元史》") == "元史"
    assert normalize_work_title("元朝史（韩儒林主编）") == "元朝史"
    assert normalize_term(" 秦始皇本纪 ") == "秦始皇本纪"


def _resolver() -> CitationResolver:
    works = {
        "元史": {"id": "work-niutrans-yuanshi", "title": "元史", "title_zh_cn": "元史"},
        "资治通鉴": {"id": "work-curated-zizhitongjian", "title": "资治通鉴", "title_zh_cn": "资治通鉴"},
    }
    chapter_index = {
        ("work-niutrans-yuanshi", "卷一"): ("本纪", "卷一"),
        ("work-niutrans-yuanshi", "卷十二"): ("本纪", "卷十二"),
        ("work-niutrans-yuanshi", "本纪"): ("本纪", None),
        ("work-curated-zizhitongjian", "秦纪"): ("秦纪", None),
    }
    aliases = {
        "元史·太祖纪": {"part": "本纪", "chapter": "卷一", "note": "《元史》卷一〈太祖本纪〉（中华书局点校本目录）"},
    }
    return CitationResolver(works, chapter_index, aliases)


def test_resolver_exact_chapter():
    match = _resolver().resolve("资治通鉴", "秦纪")
    assert match is not None
    assert match.match_method == "exact"
    assert match.auto_linkable
    assert match.confidence == 1.0


def test_resolver_alias():
    match = _resolver().resolve("元史", "太祖纪")
    assert match is not None
    assert match.match_method == "alias"
    assert match.auto_linkable
    assert (match.part, match.chapter) == ("本纪", "卷一")


def test_resolver_normalized_卷号():
    match = _resolver().resolve("元史", "卷12")
    assert match is not None
    assert match.match_method == "normalized_exact"
    assert (match.part, match.chapter) == ("本纪", "卷十二")


def test_resolver_unmatched_work():
    assert _resolver().resolve("不存在的书", "某章") is None
