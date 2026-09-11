"""Source Reference 解析与章节归一化（Knowledge Layer V2 重建）。

职责：把事件 `source_reference` / evidence `work + term + chapter_hint` 中的
引用文本解析成可校验的结构化引文（work / part / chapter / locator），并给出
match_method + confidence 分级。

原则（AGENTS.md §7 / §17）：
- 匹配结果必须携带 match_method（exact / normalized_exact / alias / fuzzy / manual）
  与 confidence；
- exact / normalized_exact / alias 才允许自动写回正式 evidence；fuzzy 只产出
  candidates 与报告，绝不自动写回；manual 由人工映射表驱动，属于可解释映射；
- 卷号归一只做形式归一（第十二章 ↔ 第12章 ↔ 十二章；卷十二 ↔ 卷12 ↔ Chapter 12），
  不做语义级模糊。
"""

from __future__ import annotations

import difflib
import re
from dataclasses import dataclass, field
from functools import lru_cache

# ---------------------------------------------------------------- 数字归一化

_CN_DIGITS = {"零": 0, "一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5,
              "六": 6, "七": 7, "八": 8, "九": 9}
_CN_UNITS = {"十": 10, "百": 100, "千": 1000, "万": 10000}
_INT_TO_CN_SIMPLE = {1: "一", 2: "二", 3: "三", 4: "四", 5: "五", 6: "六", 7: "七",
                     8: "八", 9: "九", 10: "十"}
_INT_TO_CN_TEENS = {11: "十一", 12: "十二", 13: "十三", 14: "十四", 15: "十五",
                    16: "十六", 17: "十七", 18: "十八", 19: "十九"}


def cjk_numeral_to_int(value: str) -> int | None:
    """把 '十二' / '一百零三' 等简式中文数字转为 int；失败返回 None。"""
    text = value.strip()
    if not text or not re.fullmatch(r"[零一二两三四五六七八九十百千万]+", text):
        return None
    if text in _CN_DIGITS:
        return _CN_DIGITS[text]
    total, current = 0, 0
    for char in text:
        if char in _CN_DIGITS:
            current = _CN_DIGITS[char]
        elif char in _CN_UNITS:
            unit = _CN_UNITS[char]
            if char == "十":
                current = (current or 1) * 10
                total += current
                current = 0
            else:
                total = (total + current) * unit
                current = 0
        else:
            return None
    return total + current


def int_to_cjk_numeral(value: int) -> str | None:
    """把 int 转回简式中文数字（'12' → '十二'）；超出常规范围返回 None。"""
    if value <= 0:
        return None
    if value in _INT_TO_CN_SIMPLE:
        return _INT_TO_CN_SIMPLE[value]
    if value in _INT_TO_CN_TEENS:
        return _INT_TO_CN_TEENS[value]
    if 20 < value < 100 and value % 10 in _INT_TO_CN_SIMPLE:
        return f"{_INT_TO_CN_SIMPLE[value // 10]}十{_INT_TO_CN_SIMPLE[value % 10]}"
    if value in (20, 30, 40, 50, 60, 70, 80, 90):
        return f"{_INT_TO_CN_SIMPLE[value // 10]}十"
    if 100 <= value <= 999:
        hundreds = value // 100
        rest = value % 100
        head = _INT_TO_CN_SIMPLE.get(hundreds)
        if head is None:
            return None
        if rest == 0:
            return f"{head}百"
        tail = int_to_cjk_numeral(rest)
        if tail:
            return f"{head}百{tail}"
    return None


_FULLWIDTH_TRANS = str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)})


def normalize_work_title(title: str) -> str:
    """work 名归一：去书名号/空白/括注（点校本、主编等），统一全角→半角。"""
    text = title.strip()
    text = text.replace("《", "").replace("》", "").replace("〈", "").replace("〉", "")
    text = re.sub(r"[（(][^（）()]*[)）]", "", text)      # （韩儒林主编）/（点校本）
    text = re.sub(r"[\s\u3000]+", "", text)
    return text.translate(_FULLWIDTH_TRANS)


def normalize_term(term: str) -> str:
    """term 归一：去书名号/空白，统一全角→半角。"""
    text = term.strip()
    text = text.replace("《", "").replace("》", "")
    text = re.sub(r"[\s\u3000]+", "", text)
    return text.translate(_FULLWIDTH_TRANS)


# ---------------------------------------------------------------- 引文解析

_LOCATOR_PATTERN = re.compile(
    r"(?:第(?P<cn_a>[零一二两三四五六七八九十百千万]+|[0-9]+)(?P<kind_a>[章卷篇回节编册部])"
    r"|卷\s*(?P<cn_b>[零一二两三四五六七八九十百千万]+|[0-9]+)"
    r"|(?P<cn_c>[零一二两三四五六七八九十百千万]+|[0-9]+)(?P<kind_c>[章卷篇回节编册部])"
    r"|Chapter\s*(?P<latin>[0-9]+))",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Locator:
    kind: str          # 章 / 卷 / 篇 / 编 ...
    value: int
    raw: str


def parse_locator(text: str) -> Locator | None:
    """解析单个定位符（第十二章 / 卷12 / Chapter 12 / 十二章）→ Locator。"""
    match = _LOCATOR_PATTERN.search(text or "")
    if not match:
        return None
    kind = match.group("kind_a") or match.group("kind_c") or ("卷" if match.group("cn_b") else "章")
    raw_value = match.group("latin") or match.group("cn_a") or match.group("cn_b") or match.group("cn_c") or ""
    try:
        value = int(raw_value)
    except ValueError:
        value = cjk_numeral_to_int(raw_value)
    if value is None:
        return None
    return Locator(kind=kind, value=value, raw=match.group(0))


def normalize_locator(text: str) -> tuple[str, int] | None:
    locator = parse_locator(text)
    return (locator.kind, locator.value) if locator else None


@dataclass(frozen=True)
class Citation:
    """一条结构化引文：work 必有，term/locator 可缺。"""
    work_raw: str
    term_raw: str | None = None       # 《史记·秦始皇本纪》 → 秦始皇本纪
    locator_raw: str | None = None    # 第X卷/第X章（书名内第三段或定位符）
    raw: str = ""
    source_reference: str | None = field(default=None, repr=False)


_CITE_PATTERN = re.compile(r"[《【]([^《》〔〕【】]+)[》〕]")


def parse_citations(source_reference: str | None) -> list[Citation]:
    """从 source_reference 提取《书名·篇章》形引用；非书名号文本不强行解析。"""
    citations: list[Citation] = []
    for match in _CITE_PATTERN.finditer(source_reference or ""):
        raw = match.group(0)
        body = match.group(1).translate(_FULLWIDTH_TRANS)
        parts = [p.strip() for p in re.split(r"[·.．・—－]", body) if p.strip()]
        if not parts:
            continue
        work_raw = parts[0]
        term_raw = "·".join(parts[1:]) if len(parts) > 1 else None
        locator = parse_locator(term_raw) if term_raw else None
        if locator and term_raw:
            term_clean = term_raw.replace(locator.raw, "").replace("·", "").strip()
            citations.append(Citation(work_raw=work_raw, term_raw=term_clean or None,
                                      locator_raw=locator.raw, raw=raw,
                                      source_reference=source_reference))
        else:
            citations.append(Citation(work_raw=work_raw, term_raw=term_raw,
                                      raw=raw, source_reference=source_reference))
    return citations


# ---------------------------------------------------------------- 匹配分级

MATCH_EXACT = "exact"
MATCH_NORMALIZED = "normalized_exact"
MATCH_ALIAS = "alias"
MATCH_FUZZY = "fuzzy"
MATCH_MANUAL = "manual"
MATCH_CONTENT = "content"   # 语料章首行核实（确定性，head 明证）

# 允许自动写回 evidence 的 match_method 集合（manual 由人工映射表驱动，可解释）
AUTO_LINK_METHODS = frozenset({MATCH_EXACT, MATCH_NORMALIZED, MATCH_ALIAS, MATCH_MANUAL, MATCH_CONTENT})
REPORT_ONLY_METHODS = frozenset({MATCH_FUZZY})

_METHOD_CONFIDENCE = {MATCH_EXACT: 1.0, MATCH_NORMALIZED: 0.9, MATCH_ALIAS: 0.85,
                      MATCH_FUZZY: 0.6, MATCH_MANUAL: 1.0, MATCH_CONTENT: 0.95}


@dataclass
class ChapterMatch:
    work_raw: str
    work_id: str | None
    work_title: str | None
    part: str | None            # 卷类（本纪/列传/秦纪…）
    chapter: str | None         # 篇卷（卷一/秦始皇本纪/秦纪一…）
    match_method: str
    confidence: float
    note: str | None = None

    @property
    def auto_linkable(self) -> bool:
        return self.match_method in AUTO_LINK_METHODS and self.confidence >= 0.85


def _fuzzy_ratio(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, a, b).ratio()


class CitationResolver:
    """对 (work, term/locator) 在 knowledge 实体集合上做分级匹配。

    works：{normalized_title: work_row}（work_row 至少含 id/title/title_zh_cn）
    chapter_index：{(work_id, normalized_text): (part, chapter)} —— part 与 chapter 双键
    aliases：{normalized('work·term'): {'part':..., 'chapter':..., 'note':...}}
    """

    FUZZY_THRESHOLD = 0.75

    def __init__(self, works: dict[str, dict], chapter_index: dict, aliases: dict | None = None):
        self.works = works
        self.chapter_index = chapter_index
        self.aliases = aliases or {}

    # -- 分步 ------------------------------------------------------------

    def _match_work(self, work_raw: str) -> tuple[dict | None, str | None]:
        key = normalize_work_title(work_raw)
        if key in self.works:
            return self.works[key], MATCH_EXACT
        for title, row in self.works.items():
            if _fuzzy_ratio(key, title) >= self.FUZZY_THRESHOLD:
                return row, MATCH_FUZZY
        return None, None

    def _match_chapter(self, work_id: str, term_raw: str | None) -> tuple[tuple[str, str] | None, str]:
        """返回 ((part, chapter), method)；term 归一后先精确、后模糊。"""
        if not term_raw:
            return None, None
        term = normalize_term(term_raw)
        hit = self.chapter_index.get((work_id, term))
        if hit:
            return hit, MATCH_EXACT
        # 卷号形式归一：卷十二 ↔ 卷12
        locator = parse_locator(term_raw)
        if locator and locator.kind == "卷":
            for alt in (f"卷{locator.value}", f"卷{int_to_cjk_numeral(locator.value) or ''}",
                        f"第{locator.value}卷", f"第{int_to_cjk_numeral(locator.value) or '?'}卷"):
                hit = self.chapter_index.get((work_id, normalize_term(alt)))
                if hit:
                    return hit, MATCH_NORMALIZED
        for (wid, text), hit in self.chapter_index.items():
            if wid != work_id:
                continue
            if _fuzzy_ratio(term, text) >= self.FUZZY_THRESHOLD:
                return hit, MATCH_FUZZY
        return None, None

    def resolve(self, work_raw: str, term_raw: str | None = None,
                locator_raw: str | None = None) -> ChapterMatch | None:
        work_row, work_method = self._match_work(work_raw)
        if work_row is None:
            return None
        work_id = str(work_row.get("id"))
        work_title = work_row.get("title") or work_row.get("title_zh_cn")
        alias_key = normalize_work_title(f"{work_raw}·{term_raw or ''}")
        alias = self.aliases.get(alias_key)
        if alias:
            return ChapterMatch(work_raw=work_raw, work_id=work_id, work_title=work_title,
                                part=alias.get("part"), chapter=alias.get("chapter"),
                                match_method=MATCH_ALIAS, confidence=_METHOD_CONFIDENCE[MATCH_ALIAS],
                                note=alias.get("note"))
        chapter, method = self._match_chapter(work_id, term_raw)
        if chapter is None and method is None and work_row is not None and not term_raw:
            # 仅书名引用：work 级命中即可（无章级定位）
            return ChapterMatch(work_raw=work_raw, work_id=work_id, work_title=work_title,
                                part=None, chapter=None,
                                match_method=MATCH_EXACT if self.works.get(normalize_work_title(work_raw)) else MATCH_FUZZY,
                                confidence=_METHOD_CONFIDENCE[MATCH_EXACT if self.works.get(normalize_work_title(work_raw)) else MATCH_FUZZY],
                                note="work 级匹配（无篇章定位）")
        if chapter is None:
            return None
        return ChapterMatch(work_raw=work_raw, work_id=work_id, work_title=work_title,
                            part=chapter[0], chapter=chapter[1], match_method=method,
                            confidence=_METHOD_CONFIDENCE[method])
