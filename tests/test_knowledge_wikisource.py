"""knowledge_wikisource parser 测试（Batch 02 Queue 6/15）。

覆盖：wikitext 模板/标记剥离（含多行模板、异文模板）、HTML chrome 剔除与正文裁剪、
manifest gating、稳定 id、快照解析。全部确定性断言，不依赖网络与真实快照。
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from history_data_pipeline.knowledge_wikisource import (
    WIKISOURCE_SOURCE_ID,
    TEXT_ID_PREFIX,
    _strip_multiline_markup,
    html_paragraphs,
    iter_wikisource_chapter_heads,
    iter_wikisource_texts,
    iter_wikisource_works,
    resolve_snapshot,
    wikitext_paragraphs,
)


# ---------------------------------------------------------------------------
# wikitext 解析
# ---------------------------------------------------------------------------

def test_wikitext_strips_single_line_template():
    text = "前文{{Gap}}后文"
    assert wikitext_paragraphs(text) == ["前文后文"]


def test_wikitext_strips_multiline_header_template():
    text = "{{Header\n|title = 某某\n|author = 某人\n}}\n正文第一段。\n\n正文第二段。"
    assert wikitext_paragraphs(text) == ["正文第一段。", "正文第二段。"]


def test_wikitext_variant_template_keeps_primary_char():
    # {{另|止|置}} → 保留正字「止」，不得整段删除
    assert wikitext_paragraphs("悲憤不{{另|止|置}}。") == ["悲憤不止。"]


def test_wikitext_strips_wikilinks_and_bold():
    text = "見[[史記|太史公]]書'''本紀'''。"
    assert wikitext_paragraphs(text) == ["見太史公書本紀。"]


def test_wikitext_skips_headings_and_category_after_link_strip():
    text = "==校勘記==\n正文。\n[[Category:日本政府文件]]"
    assert wikitext_paragraphs(text) == ["正文。"]


def test_wikitext_skips_pages_transclusion_and_comments():
    text = "<pages index=\"x.pdf\" from=1 to=2/>\n<!-- 注释 -->\n正文。"
    assert wikitext_paragraphs(text) == ["正文。"]


# ---------------------------------------------------------------------------
# HTML（扫描件转写页）解析
# ---------------------------------------------------------------------------

def test_html_strips_style_and_editsection():
    html = (
        "<div class=\"mw-parser-output\">"
        "<style>.mw-parser-output .kaiti{font-family:Kaiti}</style>"
        "<div>标题<span class=\"mw-editsection\">[编辑]</span></div>"
        "<p>正文第一段。</p><p>正文第二段。</p></div>"
    )
    paras = html_paragraphs(html)
    # 标题行属正文内容保留；CSS 与 [编辑] 标记必须剥离
    assert paras == ["标题", "正文第一段。", "正文第二段。"]


def test_html_body_markers_trim_chrome():
    html = "<div><p>页眉导航</p><p>正文开始</p><p>正文结束</p><p>版权页脚</p></div>"
    paras = html_paragraphs(html, body_start="正文开始", body_end="版权页脚")
    assert paras == ["正文开始", "正文结束"]


# ---------------------------------------------------------------------------
# manifest 驱动与稳定 id
# ---------------------------------------------------------------------------

def _write_snapshot(tmp_path: Path, pages: list[dict], bodies: dict[str, str]) -> Path:
    snap = tmp_path / "wikisource" / "20260101"
    (snap / "pages").mkdir(parents=True)
    for page in pages:
        (snap / page["file"]).write_text(bodies[page["file"]], encoding="utf-8")
    metadata = {"source_id": WIKISOURCE_SOURCE_ID, "version": "20260101", "pages": pages}
    (snap / "metadata.json").write_text(json.dumps(metadata, ensure_ascii=False), encoding="utf-8")
    return snap


PAGE_OK = {
    "title": "宋史/卷485", "file": "pages/01.wikitext", "underlying_work": "宋史·卷485·夏国传上",
    "work_id_mapping": "work-curated-songshi", "section": "列传", "chapter": "卷四百八十五",
    "doc_class": "classical_history", "license": "public_domain", "pd_reason": "元代官修",
    "canonical_use": "allowed",
}
PAGE_GATED = {
    "title": "待核页", "file": "pages/02.wikitext", "underlying_work": "待核页",
    "work_id_mapping": None, "section": None, "chapter": None, "doc_class": "document",
    "license": "pending", "pd_reason": "待核", "canonical_use": "gated_pending_review",
}


def test_iter_texts_stable_ids_and_gating(tmp_path):
    snap = _write_snapshot(tmp_path, [PAGE_OK, PAGE_GATED],
                           {"pages/01.wikitext": "第一段。\n第二段。", "pages/02.wikitext": "不应入库"})
    rows1 = list(iter_wikisource_texts(snap))
    rows2 = list(iter_wikisource_texts(snap))
    assert len(rows1) == 2  # gated 页不产行
    assert [r["id"] for r in rows1] == [r["id"] for r in rows2]  # 幂等稳定
    assert all(r["id"].startswith(TEXT_ID_PREFIX) for r in rows1)
    assert rows1[0]["book_id"] == "work-curated-songshi"
    assert rows1[0]["section"] == "列传" and rows1[0]["chapter"] == "卷四百八十五"
    assert rows1[0]["source_id"] == WIKISOURCE_SOURCE_ID
    assert [r["paragraph_index"] for r in rows1] == [1, 2]


def test_iter_works_skips_mapped_and_gated(tmp_path):
    snap = _write_snapshot(tmp_path, [PAGE_OK, PAGE_GATED],
                           {"pages/01.wikitext": "段。", "pages/02.wikitext": "x"})
    works = list(iter_wikisource_works(snap))
    assert works == []  # 古籍复用 curated work id；gated 页不产 work 行


def test_iter_chapter_heads_first_paragraph(tmp_path):
    snap = _write_snapshot(tmp_path, [PAGE_OK],
                           {"pages/01.wikitext": "夏國主元昊。\n後文。"})
    heads = list(iter_wikisource_chapter_heads(snap))
    assert len(heads) == 1
    assert heads[0]["chapter"] == "卷四百八十五"
    assert heads[0]["head_text"] == "夏國主元昊。"


def test_resolve_snapshot_latest(tmp_path):
    class Paths:
        def __init__(self, raw): self.raw = raw
    raw = tmp_path / "data" / "raw"
    base = raw / "wikisource"
    (base / "20250101").mkdir(parents=True)
    (base / "20260912").mkdir(parents=True)
    assert resolve_snapshot(Paths(raw)).name == "20260912"
    assert resolve_snapshot(Paths(raw), "20250101").name == "20250101"


def test_strip_multiline_markup_nested():
    assert _strip_multiline_markup("a{{b{{c}}d}}e") == "ae"
