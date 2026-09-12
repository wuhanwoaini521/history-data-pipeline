"""Evidence Linking：event evidence (work, term) → knowledge historical_texts 章级锚定。

链路（Knowledge Layer V2）：
    source → historical_texts(document/section/chapter/paragraph) → evidence → event

策略（确定性 + 可解释）：
- 匹配分级：exact > normalized_exact > alias（curated 卷号映射表）> fuzzy（只报告）；
- 仅 match_method ∈ {exact, normalized_exact, alias} 且 confidence ≥ 0.85 允许自动写回；
- 锚定行为「章级锚」：historical_text_id 指向该章首段行（真实存在的行，非虚构），
  chapter_anchor 记录 '卷类/篇卷' 全路径；段级 excerpt 需人工或后续按 quote 核对后升级；
- fuzzy 结果只进 candidates + 报告，绝不写 YAML。

写回 YAML 用 PyYAML round-trip（sort_keys=False 保序），并保留文件尾部注释块
（与 calibration_produce_candidates.py 的既有写回约定一致）。
"""

from __future__ import annotations

import json
import re
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

import yaml

from .source_reference import (
    _METHOD_CONFIDENCE,
    CitationResolver,
    MATCH_ALIAS,
    MATCH_CONTENT,
    MATCH_EXACT,
    MATCH_FUZZY,
    MATCH_MANUAL,
    MATCH_NORMALIZED,
    normalize_term,
    normalize_work_title,
)


@dataclass
class KnowledgeIndex:
    """knowledge store 的匹配索引（works + chapter 双键 + 章首段锚点 + 章首行）。"""

    works: dict[str, dict]                  # normalized_title -> work row
    chapter_index: dict[tuple, tuple]       # (work_id, normalized_text) -> (section, chapter)
    chapter_anchor: dict[tuple, str]        # (work_id, section, chapter) -> 首段 text id
    part_first_chapter: dict[tuple, str]    # (work_id, section) -> 该卷类下第一篇卷名
    chapter_heads: dict[str, list[tuple]]   # work_id -> [(section, chapter, head_text)]

    @classmethod
    def load(cls, knowledge_db: Path) -> "KnowledgeIndex":
        import duckdb

        works: dict[str, dict] = {}
        chapter_index: dict[tuple, tuple] = {}
        chapter_anchor: dict[tuple, str] = {}
        part_first_chapter: dict[tuple, str] = {}
        heads: dict[str, list[tuple]] = {}
        with duckdb.connect(str(knowledge_db), read_only=True) as connection:
            for row in connection.execute(
                "SELECT id, title, title_zh_cn, title_raw FROM works"
            ).fetchall():
                row = {"id": row[0], "title": row[1], "title_zh_cn": row[2], "title_raw": row[3]}
                for key in (row["title"], row["title_zh_cn"], row["title_raw"]):
                    if key:
                        works.setdefault(normalize_work_title(key), row)
            # 语料自身也可作为 work 索引来源（curated work id 复用时 knowledge 库 works 表可为空）
            for row in connection.execute(
                "SELECT DISTINCT book_id, title_zh_cn FROM historical_texts WHERE title_zh_cn IS NOT NULL"
            ).fetchall():
                row = {"id": row[0], "title": row[1], "title_zh_cn": row[1], "title_raw": row[1]}
                works.setdefault(normalize_work_title(row["title"]), row)
            # 章/卷类 双键索引（DISTINCT，~2k 行）
            for book_id, chapter, section in connection.execute(
                "SELECT DISTINCT book_id, chapter, section FROM historical_texts "
                "WHERE chapter IS NOT NULL OR section IS NOT NULL"
            ).fetchall():
                if chapter:
                    chapter_index.setdefault((book_id, normalize_term(chapter)), (section, chapter))
                if section:
                    chapter_index.setdefault((book_id, normalize_term(section)), (section, None))
            # 章首段锚点：每章取 min(paragraph_index) 的行 id
            for book_id, section, chapter, text_id in connection.execute(
                """
                SELECT t.book_id, t.section, t.chapter, t.id
                FROM historical_texts t
                JOIN (
                    SELECT book_id, section, chapter, MIN(paragraph_index) AS min_para
                    FROM historical_texts GROUP BY book_id, section, chapter
                ) g ON t.book_id = g.book_id
                   AND t.section IS NOT DISTINCT FROM g.section
                   AND t.chapter IS NOT DISTINCT FROM g.chapter
                   AND t.paragraph_index = g.min_para
                """
            ).fetchall():
                chapter_anchor[(book_id, section, chapter)] = text_id
            # 卷类 → 第一篇卷（用于卷类级锚点的 anchor 全路径）
            for book_id, section, first in connection.execute(
                "SELECT book_id, section, MIN(chapter) FROM historical_texts "
                "WHERE chapter IS NOT NULL AND section IS NOT NULL GROUP BY book_id, section"
            ).fetchall():
                part_first_chapter[(book_id, normalize_term(section))] = first
            # 章首行（evidence 内容核实依据）
            try:
                for book_id, work_title, section, chapter, head_text in connection.execute(
                    "SELECT book_id, work_title, section, chapter, head_text FROM chapter_heads"
                ).fetchall():
                    heads.setdefault(book_id, []).append((section, chapter, head_text))
            except duckdb.CatalogException:
                heads = {}
        return cls(works=works, chapter_index=chapter_index,
                   chapter_anchor=chapter_anchor, part_first_chapter=part_first_chapter,
                   chapter_heads=heads)


def alias_map(root: Path) -> dict[str, dict]:
    """curated 卷号/纪名映射表（人工可解释；数据文件见 data/curated/knowledge/）。"""
    path = root / "data" / "curated" / "knowledge" / "chapter_aliases.json"
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as stream:
        raw = json.load(stream)
    aliases: dict[str, dict] = {}
    for entry in raw:
        key = normalize_work_title(f"{entry['work']}·{entry['term']}")
        aliases[key] = {"part": entry.get("part"), "chapter": entry.get("chapter"), "note": entry.get("note")}
    return aliases


@dataclass
class LinkResult:
    event_id: str
    work: str
    term: str
    status: str                      # linked / fuzzy_candidate / unmatched / needs_source
    match_method: str | None
    confidence: float | None
    historical_text_id: str | None
    chapter_anchor: str | None
    note: str | None = None


def _anchor_text_id(index: KnowledgeIndex, work_id: str, section: str | None,
                    chapter: str | None) -> str | None:
    if chapter:
        return index.chapter_anchor.get((work_id, section, chapter))
    if section:
        first = index.part_first_chapter.get((work_id, normalize_term(section)))
        if first:
            return index.chapter_anchor.get((work_id, section, first))
    return None


def _chapter_tokens(term: str) -> list[str]:
    """term → 主名 token 候选（按可信度排序，首个命中者生效）。

    '孝惠帝纪' = 孝惠+帝纪；'文帝纪' = 文帝+纪 —— 两种切法都保留：
    候选顺序 [剥'帝纪', 剥'纪']，'文帝' 案例因剥'帝纪'后不足 2 字自动跳过。
    """
    text = normalize_term(term)
    candidates: list[str] = []
    for suffix in ("本纪", "载记", "世家", "列传", "帝纪", "纪", "传", "志"):
        if text.endswith(suffix) and len(text) > len(suffix):
            stem = text[: -len(suffix)]
            if len(stem) >= 2 and stem not in candidates:
                candidates.append(stem)
    if len(text) >= 2 and text not in candidates:
        candidates.append(text)     # 汉书·高祖 这类无后缀 term 直接前缀核实
    return candidates


# 章首行形态（语料实测）：
#   ◎太祖一太祖法天启运… / ○太祖一太祖启运… / 太祖纪太祖道武皇帝…（魏书）
#   高祖上高祖文皇帝…（隋书）/ 则天皇后则天皇后武氏…（旧唐书）/ ◎庄烈帝二（明史）
#   文帝下（周书）/ 高祖，沛丰邑中阳里人也（汉书·高帝纪）/ ◎仪卫（明书 志）
_HEAD_PREFIX_STRIP = "◎○"

# token 后允许紧邻的字符（防止短 token 误配）：
#   「英宗前纪」「瀛国公名」「孝闵皇帝讳觉」「文帝上」「高祖，沛丰邑…」等实测形态
_HEAD_TOKEN_TAIL = set("，。；、一二三四五六七八九十百千万0-9上中下前后帝纪传志讳姓名字皇后公王附")


def _natural_chapter_sort_key(chapter: str) -> tuple:
    import re as _re
    m = _re.search(r"([0-9]+|[零一二两三四五六七八九十百千万]+)", chapter or "")
    if not m:
        return (1, 0, chapter or "")
    raw = m.group(1)
    value = int(raw) if raw.isdigit() else (cjk_to_int(raw) or 0)
    return (0, value, chapter or "")


def cjk_to_int(value: str) -> int | None:
    from .source_reference import cjk_numeral_to_int
    return cjk_numeral_to_int(value)


def match_chapter_by_content(index: KnowledgeIndex, work_id: str, term: str) -> tuple[str, str] | None:
    """语料章首行核实：确定性 head 前缀匹配，多章同名锚定首章（纪跨卷场景）。"""
    for token in _chapter_tokens(term):
        hits: list[tuple[str, str]] = []
        for section, chapter, head_text in index.chapter_heads.get(work_id, []):
            if not head_text:
                continue
            stripped = head_text.lstrip(_HEAD_PREFIX_STRIP)
            if not stripped.startswith(token):
                continue
            rest = stripped[len(token):]
            tail = rest[:1]
            if tail and tail not in _HEAD_TOKEN_TAIL and not rest.startswith(token) \
                    and head_text.count(token) < 2:
                # 放行三类实测形态：良性紧邻字符（文帝上/瀛国公名…）、token 重复（高祖高祖…）、
                # token 再现（后主幼主后主讳纬…）；其余（权德舆 一类）拒绝
                continue
            hits.append((section or "", chapter or ""))
        if hits:
            # 纪跨多卷（太祖一/二/三）：全部同 token 前缀 → 锚定首章（确定性）
            hits.sort(key=lambda h: (h[0], _natural_chapter_sort_key(h[1])))
            return hits[0]
    return None


def search_paragraphs(knowledge_db: Path, work_id: str, term: str, limit: int = 5) -> list[dict]:
    """段级内容检索（fuzzy）：topic 词（如 巨鹿/官渡）出现在原文行中。

    仅产出候选（报告用），绝不自动写回 —— 段级锚定需人工确认 quote。
    """
    import duckdb

    pattern = f"%{normalize_term(term)}%"
    # 语料 original_text 为繁体，检索与摘录用 original_simplified（简体，与 UI 一致）
    with duckdb.connect(str(knowledge_db), read_only=True) as connection:
        rows = connection.execute(
            "SELECT h.id, h.book_id, h.section, h.chapter, h.paragraph_index, h.original_simplified "
            "FROM historical_texts h WHERE h.book_id = ? AND h.original_simplified LIKE ? "
            "ORDER BY h.paragraph_index LIMIT ?",
            [work_id, pattern, limit],
        ).fetchall()
    return [
        {"historical_text_id": r[0], "section": r[1], "chapter": r[2],
         "paragraph_index": r[3], "excerpt": r[4]}
        for r in rows
    ]


def link_event_evidence(backbone_events: list[dict], index: KnowledgeIndex,
                        aliases: dict[str, dict],
                        knowledge_db: Path | None = None) -> Iterator[LinkResult]:
    """对每个 event evidence 求匹配结果（不写回）。

    匹配阶梯：alias（人工已核实）→ exact（篇卷/卷类名，含 多段 term）→
    normalized_exact（卷号形式归一）→ content（语料章首行核实）→
    fuzzy（段级检索，仅候选）。fuzzy 与未命中一律不写回。
    """
    resolver = CitationResolver(index.works, index.chapter_index, aliases)
    for event in backbone_events:
        for evidence in event.get("evidence", []):
            work_raw = evidence.get("work") or ""
            term_raw = evidence.get("term") or evidence.get("chapter_hint")
            match = resolver.resolve(work_raw, term_raw) if work_raw else None
            method, part, chapter = (match.match_method, match.part, match.chapter) if match else (None, None, None)
            # 多段 term（如 三国志·魏书·文帝纪）：末段作章名、前段作卷类再试
            if match is None and term_raw and "·" in term_raw:
                segments = [s for s in term_raw.split("·") if s.strip()]
                if len(segments) >= 2:
                    part_hint, chapter_hint = "·".join(segments[:-1]), segments[-1]
                    direct = index.chapter_index.get(
                        (_work_id_of(index, work_raw), normalize_term(chapter_hint)))
                    if direct and (direct[0] == part_hint or not part_hint):
                        method, part, chapter = MATCH_EXACT, direct[0], direct[1]
            # 语料章首内容核实（帝纪/列传 卷号化语料）
            if (match is None or match.match_method == MATCH_FUZZY) and term_raw and work_raw:
                work_id = _work_id_of(index, work_raw)
                if work_id:
                    content = match_chapter_by_content(index, work_id, term_raw)
                    if content:
                        method, part, chapter = MATCH_CONTENT, content[0] or None, content[1] or None
            if work_raw and part is None and chapter is None and method is None:
                # 走段级 fuzzy 检索（topic 词，如 史记·巨鹿 / 资治通鉴·官渡）；需真实 knowledge db
                work_id = _work_id_of(index, work_raw)
                candidates = (search_paragraphs(knowledge_db, work_id, term_raw, 5)
                              if (knowledge_db is not None and work_id and term_raw) else [])
                if candidates:
                    best = candidates[0]
                    yield LinkResult(event_id=event["id"], work=work_raw, term=term_raw,
                                     status="fuzzy_candidate", match_method=MATCH_FUZZY,
                                     confidence=0.6,
                                     historical_text_id=best["historical_text_id"],
                                     chapter_anchor=_anchor_label(best["section"], best["chapter"], best["paragraph_index"]),
                                     note=f"段级候选 {len(candidates)} 条；需人工确认 quote 后升级")
                    continue
                yield LinkResult(event_id=event["id"], work=work_raw, term=term_raw or "",
                                 status="unmatched", match_method=None, confidence=None,
                                 historical_text_id=None, chapter_anchor=None,
                                 note="work 或篇章未命中语料")
                continue
            if method == MATCH_FUZZY:
                # fuzzy 一律只入候选（无论是否带篇章坐标），绝不写回 —— AGENTS.md §7
                yield LinkResult(event_id=event["id"], work=work_raw, term=term_raw,
                                 status="fuzzy_candidate", match_method=method,
                                 confidence=0.6, historical_text_id=None,
                                 chapter_anchor=_anchor_label(part, chapter) if (part or chapter) else None,
                                 note="fuzzy 匹配仅入候选，不自动写回")
                continue
            work_id = _work_id_of(index, work_raw)
            text_id = _anchor_text_id(index, work_id, part, chapter)
            if text_id is None:
                yield LinkResult(event_id=event["id"], work=work_raw, term=term_raw,
                                 status="unmatched", match_method=method,
                                 confidence=0.9 if method == MATCH_CONTENT else 0.9,
                                 historical_text_id=None, chapter_anchor=None,
                                 note="命中但章内无段落行")
                continue
            if not chapter and part:
                # 卷类级命中 → 锚点行取该卷类下第一篇卷的首段，anchor 记全路径
                chapter = index.part_first_chapter.get((work_id, normalize_term(part)))
            confidence = 0.95 if method == MATCH_CONTENT else _METHOD_CONFIDENCE.get(method, 0.9)
            yield LinkResult(event_id=event["id"], work=work_raw, term=term_raw,
                             status="linked", match_method=method,
                             confidence=confidence, historical_text_id=text_id,
                             chapter_anchor=_anchor_label(part, chapter))


def _anchor_label(section: str | None, chapter: str | None, paragraph: int | None = None) -> str:
    base = f"{section}/{chapter}" if (section and chapter) else (section or chapter or "")
    return f"{base}#p{paragraph}" if paragraph else base


def _work_id_of(index: KnowledgeIndex, work_raw: str) -> str | None:
    row = index.works.get(normalize_work_title(work_raw))
    return str(row["id"]) if row else None


def apply_links(events_dir: Path, results: list[LinkResult], *, apply: bool) -> dict:
    """把 linked 结果写回事件 YAML（apply=False 只统计，不落盘）。"""
    linked_by_event: dict[str, list[LinkResult]] = {}
    for result in results:
        if result.status == "linked":
            linked_by_event.setdefault(result.event_id, []).append(result)
    stats = {"events": len(linked_by_event), "evidence_linked": sum(len(v) for v in linked_by_event.values()), "written": 0}
    if not apply:
        return stats
    for event_id, links in sorted(linked_by_event.items()):
        path = _find_event_file(events_dir, event_id)
        if path is None:
            continue
        doc, _tail = _load_event_yaml(path)  # (head_block, tail_block)
        if doc is None:
            continue
        for evidence in doc.get("evidence", []):
            if evidence.get("link_method") == "manual":
                # manual 为人工核定的段落级锚点（chapter_anchor#pN）；自动重算只能降级为
                # 章级锚点，必须跳过（Batch 02 Queue 9 事故：24 条 manual 锚被覆盖为章首段）。
                continue
            for link in links:
                evidence_term = evidence.get("term") or evidence.get("chapter_hint") or ""
                if evidence.get("work") == link.work and evidence_term == (link.term or ""):
                    evidence["historical_text_id"] = link.historical_text_id
                    evidence["chapter_anchor"] = link.chapter_anchor
                    evidence["link_method"] = link.match_method
                    evidence["link_status"] = "linked"
                    evidence["link_confidence"] = link.confidence
                    note = "知识层章节锚定（source_reference normalizer；anchor=章首段）"
                    if note not in (evidence.get("review_note") or ""):
                        evidence["review_note"] = ((evidence.get("review_note") or "") + "；" + note).strip("；")
                    break
        stats["written"] += 1
        head_block, tail_block = _tail
        yaml_text = head_block + yaml.safe_dump(doc, allow_unicode=True, sort_keys=False) + tail_block
        path.write_text(yaml_text, encoding="utf-8")
    return stats


def _find_event_file(events_dir: Path, event_id: str) -> Path | None:
    for path in events_dir.rglob(f"{event_id}.yml"):
        return path
    return None


def _load_event_yaml(path: Path) -> tuple[dict | None, tuple[str, str]]:
    """safe_load + 保留文件头/尾的注释块（curated YAML 的批次说明都在头部）。"""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    head_lines: list[str] = []
    while lines and (lines[0].lstrip().startswith("#") or not lines[0].strip()):
        head_lines.append(lines.pop(0))
    tail_lines: list[str] = []
    while lines and (lines[-1].lstrip().startswith("#") or not lines[-1].strip()):
        tail_lines.insert(0, lines.pop())
    body = "\n".join(lines) + "\n"
    try:
        doc = yaml.safe_load(body)
    except yaml.YAMLError:
        return None, ("", "")
    if not isinstance(doc, dict):
        return None, ("", "")
    head_block = ("\n".join(head_lines) + "\n") if any(l.strip() for l in head_lines) else ""
    tail_block = ("\n".join(tail_lines) + "\n") if any(l.strip() for l in tail_lines) else ""
    return doc, (head_block, tail_block)
