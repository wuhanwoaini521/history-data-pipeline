"""Wikisource Batch 01 → historical_texts（Layer 2 追加源，Queue 6）。

政策依据：docs/source-acquisition-policy.md（§2 载体/底本、§6 parser 要求）。

输入：data/raw/wikisource/<version>/（metadata.json 镜像 manifest，pages/*.wikitext 或 *.html）
- 快照文件 immutable；本模块只读。

确定性（Gate D）：
- text_id = "text-wikisource-" + sha1(f"{page_file}#{paragraph_index}")[:20]
- work_id = manifest.work_id_mapping（如宋史 → work-curated-songshi，与 NiuTrans 行归一）
            或 "work-wikisource-" + sha1(页面标题)[:16]（独立文书）
- 相同快照 → 相同行与 id；不访问网络；无时间戳/随机数。

层级映射（保留底本真实层级，允许 section/chapter 为 null）：
- 古籍（宋史卷）: document=宋史, section=列传, chapter=卷四百八十五（汉字卷号）
- 单篇文书:       document=页面标题, section=None, chapter=None（段落顺序 = 底本顺序）

原文与规范化分离：original_text 保留底本原貌（繁体/异体不动），
original_simplified 由 OpenCC t2s 派生（与 NiuTrans 行同一 normalizer）。
"""

from __future__ import annotations

import hashlib
import html as html_module
import json
import re
from collections.abc import Iterator
from pathlib import Path

from .normalization import simplify_text

WIKISOURCE_SOURCE_ID = "source-wikisource"
TEXT_ID_PREFIX = "text-wikisource-"
WORK_ID_PREFIX = "work-wikisource-"

TEXT_COLUMNS = ("id", "title_zh_cn", "book_id", "chapter", "section", "paragraph_index",
                "source_path", "original_text", "original_simplified", "translation_zh_cn",
                "translation_type", "translation_source", "notes_zh_cn", "quality_status",
                "source_id", "alignment_quality")

WORK_COLUMNS = ("id", "title", "title_raw", "title_zh_cn", "book_type", "source_ids",
                "source_id", "quality_status")

# ---------------------------------------------------------------------------
# wikitext → 段落（确定性规则；不做语义改写）
# ---------------------------------------------------------------------------

_TEMPLATE_RE = re.compile(r"\{\{[^{}]*\}\}")
# 异文注记模板 {{另|正字|异字}} → 保留正字（内容保真：不能整段删除）
_VARIANT_TEMPLATE_RE = re.compile(r"\{\{另\|([^|}]+)\|[^|}]+\}\}")
_WIKILINK_RE = re.compile(r"\[\[(?:[^[\]|]*\|)?([^[\]|]*)\]\]")
_EXTERNAL_LINK_RE = re.compile(r"\[https?://\S+\s+([^\]]+)\]|\[https?://\S+\]")
_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
_TAG_RE = re.compile(r"<[^>]+>")
_BOLD_RE = re.compile(r"'{2,5}")


def _strip_wikitext_markup(line: str) -> str:
    """单行 wikitext → 纯文本（模板/链接/标记剥离；顺序固定）。"""
    line = _COMMENT_RE.sub("", line)
    line = _TEMPLATE_RE.sub("", line)          # 单层模板（快照页无嵌套三层以上模板正文）
    while _TEMPLATE_RE.search(line):           # 嵌套模板由内向外剥（确定性收敛）
        line = _TEMPLATE_RE.sub("", line)
    line = _WIKILINK_RE.sub(r"\1", line)       # [[链接|文字]] → 文字
    line = _EXTERNAL_LINK_RE.sub(r"\1", line)
    line = _TAG_RE.sub("", line)               # <br/> <ref> 等残留标签
    line = _BOLD_RE.sub("", line)              # '''bold''' 标记
    line = html_module.unescape(line)
    line = line.replace("\u3000", " ").strip()
    return line


_SKIP_LINE_PREFIXES = ("#REDIRECT", "#重定向", "Category:", "分類:", "__NOTOC__")

# 行级精确噪声（chrome/标记残片）
_JUNK_LINES = {"<!--", "-->", "{{", "}}", "编辑", "編輯", "←", "→", "<", ">"}

# wiki 标题行（=...= / ==...== / ===校勘記=== 等结构性标题，非正文）
_HEADING_RE = re.compile(r"^=+.*=+$")


def _strip_multiline_markup(content: str) -> str:
    """整文级剥离：注释与多行模板（自内向外，确定性收敛）。"""
    content = _COMMENT_RE.sub("", content)
    content = _VARIANT_TEMPLATE_RE.sub(r"\1", content)  # {{另|止|置}} → 止（保真正字）
    prev = None
    while prev != content:
        prev = content
        content = _TEMPLATE_RE.sub("", content)
    return content


def wikitext_paragraphs(content: str) -> list[str]:
    """wikitext 全文 → 段落列表（保留原行顺序；空行分段，标记行剔除）。"""
    content = _strip_multiline_markup(content)
    paragraphs: list[str] = []
    for raw_line in content.splitlines():
        stripped = raw_line.strip()
        if not stripped:
            continue
        if stripped.startswith(_SKIP_LINE_PREFIXES):
            continue
        if stripped.startswith("<pages"):
            continue
        if _HEADING_RE.match(stripped):
            continue
        text = _strip_wikitext_markup(stripped)
        if not text or text in _JUNK_LINES:
            continue
        # 链接剥离后可能露出 Category:/分類: 等命名空间前缀（[[Category:…]] 场景）
        if text.startswith(("Category:", "分類:", "File:", "Image:", "Template:")):
            continue
        paragraphs.append(text)
    return paragraphs


# ---------------------------------------------------------------------------
# html_rendered → 段落（仅用于扫描件转写页；同确定性规则）
# ---------------------------------------------------------------------------

# 维基文库渲染页 chrome（导航/页脚/模板框）按 class/id 剔除；正文在 mw-parser-output 内
_CHROME_CLASS_TOKENS = (
    "navbox", "vertical-navbox", "navigation", "mw-jump-link", "printfooter",
    "catlinks", "mw-catlinks", "sidebar", "header", "plate", "licenseContainer",
    "noprint", "mw-editsection", "toc", "mbox", "sistersitebox", "page-header",
    "footer", "sideBox", "noprint", "plainlinks", "mw-references", "reflist",
)
_BLOCK_TAGS = ("p", "div", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6")


def _strip_html_to_lines(content: str) -> list[str]:
    """渲染 HTML → 候选文本行（块级标签作行界；无状态、单遍、确定性）。"""
    # 去 head/script/style（TemplateStyles CSS 内嵌于 <style>）
    for tag in ("head", "script", "style"):
        content = re.sub(rf"<{tag}\b.*?</{tag}>", "", content, flags=re.DOTALL | re.IGNORECASE)
    # 去 [编辑] 区块（mw-editsection 整段 span，含括号文字）
    content = re.sub(r"<span[^>]*mw-editsection[^>]*>.*?</span>", "", content,
                     flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r"<span[^>]*mw-headline[^>]*>", "\n", content, flags=re.IGNORECASE)
    content = _COMMENT_RE.sub("", content)
    # 块级标签 → 换行（行界），其余标签删除
    for tag in _BLOCK_TAGS:
        content = re.sub(rf"</?{tag}\b[^>]*>", "\n", content, flags=re.IGNORECASE)
    content = _TAG_RE.sub("", content)
    content = html_module.unescape(content)
    lines = []
    for line in content.splitlines():
        line = line.replace("\u3000", " ").strip()
        line = line.replace("[编辑]", "").replace("[編輯]", "").strip()
        if line:
            lines.append(line)
    return lines


_NOISE_LINE_PATTERNS = (
    "维基文库", "維基文庫", "导航菜单", "導覽選單", "页面分类", "頁面分類",
    "取自「", "取自“", "本作品收录于", "本作品收錄於", "姊妹计划", "姊妹計劃",
    "查 · 论 · 编", "查·论·编", "目录", "目錄", "阅读其他语言", "閱讀其他語言",
    "此页面最后编辑", "此頁面最後編輯", "隐私政策", "隱私政策", "使用条款", "使用條款",
    "← ", "→ ", "跳转到", "跳轉到", "检索自", "檢索自",
)


def html_paragraphs(content: str, body_start: str | None = None,
                    body_end: str | None = None) -> list[str]:
    """渲染 HTML 全文 → 段落列表（chrome 剔除；manifest 正文起止标记裁剪；Queue 7 校验残留）。"""
    lines = _strip_html_to_lines(content)
    # manifest 驱动的正文裁剪：body_start 首次出现（含）至 body_end 首次出现（不含）
    if body_start:
        for offset, line in enumerate(lines):
            if body_start in line:
                lines = lines[offset:]
                break
    if body_end:
        for offset, line in enumerate(lines):
            if body_end in line:
                lines = lines[:offset]
                break
    paragraphs: list[str] = []
    for line in lines:
        if any(token in line for token in _CHROME_CLASS_TOKENS):
            # class 属性已随标签删除，此处兜底防御性过滤（无操作场景）
            continue
        if any(pattern in line for pattern in _NOISE_LINE_PATTERNS):
            continue
        if re.fullmatch(r"[0-9\s.,;:（）()\[\]【】|·\-—×]+", line):
            continue  # 纯页码/标点行
        if len(line) < 2 or line in _JUNK_LINES:
            continue
        paragraphs.append(line)
    return paragraphs


# ---------------------------------------------------------------------------
# 快照 → historical_texts / works 行
# ---------------------------------------------------------------------------


def _work_id_for_page(page: dict) -> str:
    if page.get("work_id_mapping"):
        return page["work_id_mapping"]
    title = page.get("title") or page.get("underlying_work") or page["file"]
    return WORK_ID_PREFIX + hashlib.sha1(title.encode("utf-8")).hexdigest()[:16]


def _doc_title(page: dict) -> str:
    """document 名：古籍用底本主名（宋史），单篇文书用页面标题。"""
    underlying = page.get("underlying_work") or ""
    if page.get("doc_class") == "classical_history":
        return underlying.split("·")[0].strip() or page["title"]
    return page["title"]


def resolve_snapshot(paths, version: str | None = None) -> Path | None:
    """定位 wikisource 快照（data/raw/wikisource/<version>）；不存在时返回 None（可选源）。"""
    base = paths.raw / "wikisource"
    if not base.is_dir():
        return None
    if version:
        target = base / version
        return target if target.is_dir() else None
    versions = sorted((p for p in base.iterdir() if p.is_dir()), key=lambda p: p.name)
    return versions[-1] if versions else None


def resolve_snapshots(paths) -> list[Path]:
    """全部 wikisource 快照（多批次采集：每个版本目录独立 manifest，全部并摄入库）。"""
    base = paths.raw / "wikisource"
    if not base.is_dir():
        return []
    return sorted((p for p in base.iterdir() if p.is_dir() and (p / "metadata.json").exists()),
                  key=lambda p: p.name)


def iter_wikisource_texts(snapshot_dir: Path) -> Iterator[dict]:
    """wikisource 快照 → historical_texts 行（逐页 manifest 驱动）。"""
    metadata = json.loads((snapshot_dir / "metadata.json").read_text(encoding="utf-8"))
    for page in metadata["pages"]:
        if page.get("canonical_use") != "allowed":
            # manifest 声明 gated_pending_review 的页：仅留档，不入 canonical 知识层
            continue
        path = snapshot_dir / page["file"]
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")
        fmt = page.get("fetch_format", "wikitext")
        if fmt == "wikitext":
            paragraphs = wikitext_paragraphs(content)
        else:
            paragraphs = html_paragraphs(content, page.get("body_start_marker"),
                                         page.get("body_end_marker"))
        book_id = _work_id_for_page(page)
        title = _doc_title(page)
        section = page.get("section")
        chapter = page.get("chapter")
        for index, text in enumerate(paragraphs, 1):
            yield {
                "id": TEXT_ID_PREFIX + hashlib.sha1(f"{page['file']}#{index}".encode("utf-8")).hexdigest()[:20],
                "title_zh_cn": title,
                "book_id": book_id,
                "chapter": chapter,
                "section": section,
                "paragraph_index": index,
                "source_path": f"wikisource/{snapshot_dir.name}/{page['file']}#p{index}",
                "original_text": text,
                "original_simplified": simplify_text(text),
                "translation_zh_cn": None,
                "translation_type": None,
                "translation_source": None,
                "notes_zh_cn": page.get("pd_reason"),
                "quality_status": "unverified",
                "source_id": WIKISOURCE_SOURCE_ID,
                "alignment_quality": "deterministic_parse",
            }


def iter_wikisource_works(snapshot_dir: Path) -> Iterator[dict]:
    """新独立文书的 works 行（古籍复用 curated work id，不重复生成）。"""
    metadata = json.loads((snapshot_dir / "metadata.json").read_text(encoding="utf-8"))
    seen: set[str] = set()
    for page in metadata["pages"]:
        if page.get("canonical_use") != "allowed":
            continue
        if page.get("work_id_mapping"):
            continue
        book_id = _work_id_for_page(page)
        if book_id in seen:
            continue
        seen.add(book_id)
        title = _doc_title(page)
        yield {
            "id": book_id,
            "title": title,
            "title_raw": title,
            "title_zh_cn": title,
            "book_type": page.get("doc_class") or "document",
            "source_ids": json.dumps([WIKISOURCE_SOURCE_ID], ensure_ascii=False),
            "source_id": WIKISOURCE_SOURCE_ID,
            "quality_status": "reviewed",
        }


def iter_wikisource_chapter_heads(snapshot_dir: Path) -> Iterator[dict]:
    """古籍卷的章首行（供 evidence content 核实）；单篇文书无 chapter，跳过。"""
    metadata = json.loads((snapshot_dir / "metadata.json").read_text(encoding="utf-8"))
    for page in metadata["pages"]:
        if page.get("canonical_use") != "allowed" or not page.get("chapter"):
            continue
        path = snapshot_dir / page["file"]
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")
        fmt = page.get("fetch_format", "wikitext")
        if fmt == "wikitext":
            paragraphs = wikitext_paragraphs(content)
        else:
            paragraphs = html_paragraphs(content, page.get("body_start_marker"),
                                         page.get("body_end_marker"))
        if not paragraphs:
            continue
        yield {
            "book_id": _work_id_for_page(page),
            "work_title": _doc_title(page),
            "section": page.get("section"),
            "chapter": page.get("chapter"),
            "head_text": paragraphs[0],
        }
