"""Knowledge Layer（Layer 2）构建：NiuTrans Classical-Modern → historical_texts。

目标（docs/HISTORY_BACKBONE.md · Knowledge Store 重建）：
- 从 raw 快照（data/raw/classical-modern/<version>/repository/）确定性解析
  document（书）→ part（卷类）→ chapter（篇卷）→ paragraph（行）四级结构；
- 产出 data/normalized/history.duckdb（sources / works / historical_texts），
  供 `backbone build --knowledge` 并入 dist（build.py:187-198 现成路径）。

确定性（Gate D）：
- text_id = "text-niutrans-" + sha1(f"{source_path}:{line_number}")[:20]
- work_id = "work-niutrans-" + sha1(title)[:16]（与 legacy real_build.py 同构）
- 相同输入 → 相同 ID；build 可重复执行；INSERT OR REPLACE 防重复行。

本模块只读 raw；不访问互联网；不写 curated 数据。
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterator
from pathlib import Path

from .database import SCHEMA_SQL
from .normalization import simplify_text

# NiuTrans 双语数据的顶层目录（有 source/target 句对）；古文原文仅导入显式列出的书
_BILINGUAL_TOP = "双语数据"
_CLASSICAL_TOP = "古文原文"
_DEFAULT_CLASSICAL_BOOKS = ("三朝北盟会编",)

DEFAULT_SOURCE_ID = "source-classical-modern"

TEXT_COLUMNS = ("id", "title_zh_cn", "book_id", "chapter", "section", "paragraph_index",
                "source_path", "original_text", "original_simplified", "translation_zh_cn",
                "translation_type", "translation_source", "notes_zh_cn", "quality_status",
                "source_id", "alignment_quality")

WORK_COLUMNS = ("id", "title", "title_raw", "title_zh_cn", "book_type", "source_ids",
                "source_id", "quality_status")

# 章首行索引（仅 knowledge 库；供 evidence 内容核实，不入 dist schema）
CHAPTER_HEADS_SQL = """
CREATE TABLE IF NOT EXISTS chapter_heads (
  book_id VARCHAR, work_title VARCHAR, section VARCHAR, chapter VARCHAR,
  head_text VARCHAR, PRIMARY KEY(book_id, section, chapter)
);
"""


def _sql_path(path: Path) -> str:
    return str(path.resolve()).replace("'", "''")


def curated_work_id_map() -> dict[str, str]:
    """title → work-curated-* id（来自 reference.CURATED_WORK_SEEDS）。

    historical_texts.book_id 优先指向 curated work id，避免 dist 里出现
    同书双行（work-curated-* 与 work-niutrans-* 并存）。
    """
    from .backbone.reference import CURATED_WORK_SEEDS
    mapping: dict[str, str] = {}
    for row in CURATED_WORK_SEEDS:
        for key in (row.get("title"), row.get("title_zh_cn"), row.get("title_raw")):
            if key and key not in mapping:
                mapping[key] = row["id"]
    return mapping


def _work_id_for(title: str, curated: dict[str, str] | None = None) -> str:
    if curated and title in curated:
        return curated[title]
    return "work-niutrans-" + hashlib.sha1(title.encode("utf-8")).hexdigest()[:16]


def _text_id_for(source_path: str, line_number: int) -> str:
    return "text-niutrans-" + hashlib.sha1(f"{source_path}:{line_number}".encode("utf-8")).hexdigest()[:20]


def _read_lines(path: Path) -> list[str]:
    return [line.rstrip("\n\r") for line in path.read_text(encoding="utf-8-sig", errors="replace").splitlines()]


def _read_data_source_note(directory: Path) -> str | None:
    """读取该目录下的 数据来源.txt（NiuTrans 自带的来源/许可说明）。"""
    note = directory / "数据来源.txt"
    if note.exists():
        text = note.read_text(encoding="utf-8-sig", errors="replace").strip()
        return text or None
    return None


def _base_row(rel_path: str, line_number: int, title: str, book_id: str, part: str | None,
              chapter: str | None, note: str | None) -> dict:
    return {
        "id": _text_id_for(rel_path, line_number),
        "title_zh_cn": title,
        "book_id": book_id,
        "chapter": chapter,
        "section": part,
        "paragraph_index": line_number,
        "source_path": rel_path,
        "notes_zh_cn": note,
        "quality_status": "unverified",
        "source_id": DEFAULT_SOURCE_ID,
    }


def iter_bilingual_texts(snapshot_dir: Path, curated: dict[str, str] | None = None) -> Iterator[dict]:
    """解析 双语数据/<书>/<卷类>/<篇卷>/source.txt+target.txt → 行级句对。

    层级映射：
      document = 书名（works.title）
      part     = 卷类目录名（本纪/列传/十二本纪/秦纪…） → historical_texts.section
      chapter  = 篇卷目录名（卷一/秦始皇本纪/秦纪一…）  → historical_texts.chapter
      paragraph_index = source.txt 行号（1 起，与 text_id 生成一致）
    """
    repository = snapshot_dir / "repository"
    top = repository / _BILINGUAL_TOP
    if not top.is_dir():
        return
    for source in sorted(top.rglob("source.txt")):
        target = source.with_name("target.txt")
        if not target.exists():
            continue
        rel_path = str(source.relative_to(snapshot_dir))
        depth = source.parent.relative_to(top).parts
        title = depth[0] if depth else None
        part = depth[1] if len(depth) > 1 else None
        chapter = depth[2] if len(depth) > 2 else None
        if not title:
            continue
        note = _read_data_source_note(source.parent)
        source_lines, target_lines = _read_lines(source), _read_lines(target)
        for index, (original, translation) in enumerate(zip(source_lines, target_lines), 1):
            if not original.strip() or not translation.strip():
                continue
            row = _base_row(str(rel_path), index, title, _work_id_for(title, curated), part, chapter, note)
            row.update({
                "original_text": original,
                "original_simplified": simplify_text(original),
                "translation_zh_cn": translation,
                "translation_type": "dataset",
                "translation_source": "NiuTrans Classical-Modern",
                "quality_status": "unverified",
                "source_id": DEFAULT_SOURCE_ID,
                "alignment_quality": "heuristic_unverified",
            })
            yield row


def iter_classical_texts(snapshot_dir: Path,
                         books: tuple[str, ...] = _DEFAULT_CLASSICAL_BOOKS,
                         curated: dict[str, str] | None = None) -> Iterator[dict]:
    """解析 古文原文/<书>/<卷>/text.txt（无对照译文）；仅导入显式列出的书。"""
    repository = snapshot_dir / "repository"
    top = repository / _CLASSICAL_TOP
    if not top.is_dir():
        return
    for book in books:
        book_dir = top / book
        if not book_dir.is_dir():
            continue
        note = _read_data_source_note(book_dir)
        for text_file in sorted(book_dir.rglob("text.txt")):
            rel_path = str(text_file.relative_to(snapshot_dir))
            chapter = text_file.parent.name
            for index, original in enumerate(_read_lines(text_file), 1):
                if not original.strip():
                    continue
                row = _base_row(str(rel_path), index, book, _work_id_for(book, curated), _CLASSICAL_TOP, chapter, note)
                row.update({
                    "original_text": original,
                    "original_simplified": simplify_text(original),
                    "translation_zh_cn": None,
                    "translation_type": None,
                    "translation_source": None,
                    "quality_status": "unverified",
                    "source_id": DEFAULT_SOURCE_ID,
                    "alignment_quality": None,
                })
                yield row


def iter_chapter_heads(snapshot_dir: Path, curated: dict[str, str] | None = None) -> Iterator[dict]:
    """每个篇章取首行非空原文 → chapter_heads（evidence 章级内容核实的依据）。

    覆盖 双语数据（书/卷类/篇卷 三级）与显式列出的 古文原文 书。
    """
    repository = snapshot_dir / "repository"
    top = repository / _BILINGUAL_TOP
    if top.is_dir():
        seen_chapters = set()
        for source in sorted(top.rglob("source.txt")):
            depth = source.parent.relative_to(top).parts
            title = depth[0] if depth else None
            if not title:
                continue
            part = depth[1] if len(depth) > 1 else None
            chapter = depth[2] if len(depth) > 2 else None
            key = (title, part, chapter)
            if key in seen_chapters:
                continue
            seen_chapters.add(key)
            head = next((line.strip() for line in _read_lines(source) if line.strip()), None)
            if not head:
                continue
            yield {
                "book_id": _work_id_for(title, curated),
                "work_title": title,
                "section": part,
                "chapter": chapter,
                "head_text": head,
            }
    classical_top = repository / _CLASSICAL_TOP
    if classical_top.is_dir():
        for book in _DEFAULT_CLASSICAL_BOOKS:
            book_dir = classical_top / book
            if not book_dir.is_dir():
                continue
            for text_file in sorted(book_dir.rglob("text.txt")):
                head = next((line.strip() for line in _read_lines(text_file) if line.strip()), None)
                if not head:
                    continue
                yield {
                    "book_id": _work_id_for(book, curated),
                    "work_title": book,
                    "section": _CLASSICAL_TOP,
                    "chapter": text_file.parent.name,
                    "head_text": head,
                }


def resolve_snapshot(paths, snapshot_version: str | None = None) -> Path:
    """定位 raw 快照（data/raw/classical-modern/<version>）；默认取最新版本号。"""
    base = paths.raw / "classical-modern"
    if not base.is_dir():
        raise FileNotFoundError(f"未找到 NiuTrans raw 快照目录: {base}")
    if snapshot_version:
        target = base / snapshot_version
        if not target.is_dir():
            raise FileNotFoundError(f"未找到 NiuTrans 快照版本: {target}")
        return target
    versions = sorted((p for p in base.iterdir() if p.is_dir()), key=lambda p: p.name)
    if not versions:
        raise FileNotFoundError(f"NiuTrans raw 快照目录为空: {base}")
    return versions[-1]


def write_jsonl_rows(rows: Iterator[dict], target: Path) -> int:
    target.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with target.open("w", encoding="utf-8") as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False) + "\n")
            count += 1
    return count


def _insert_json(connection, table: str, path: Path, columns: tuple[str, ...] = TEXT_COLUMNS) -> None:
    if not path.exists() or path.stat().st_size == 0:
        return
    names = ", ".join(columns)
    connection.execute(
        f"INSERT OR REPLACE INTO {table} ({names}) "
        f"SELECT {names} FROM read_json_auto('{_sql_path(path)}', records=true)"
    )


def build_knowledge_store(paths, snapshot_version: str | None = None,
                          output: Path | None = None) -> dict:
    """构建 Layer 2 知识库（仅 NiuTrans 文本层；CBDB/CText 不在本轮范围）。

    返回 manifest dict；数据库写到 paths.database（data/normalized/history.duckdb）。
    """
    import duckdb

    snapshot = resolve_snapshot(paths, snapshot_version)
    curated = curated_work_id_map()
    target = output or paths.database
    target.parent.mkdir(parents=True, exist_ok=True)
    building = target.with_name("history.building.duckdb")
    if building.exists():
        building.unlink()
    bilingual_path = paths.staging / "knowledge" / "historical_texts.jsonl"
    bilingual_count = write_jsonl_rows(iter_bilingual_texts(snapshot, curated), bilingual_path)
    classical_path = paths.staging / "knowledge" / "classical_texts.jsonl"
    classical_count = write_jsonl_rows(iter_classical_texts(snapshot, curated=curated), classical_path)
    heads_path = paths.staging / "knowledge" / "chapter_heads.jsonl"
    heads_count = write_jsonl_rows(iter_chapter_heads(snapshot, curated), heads_path)
    books = _collect_book_titles(bilingual_path, classical_path, curated)
    works_path = paths.staging / "knowledge" / "works.jsonl"
    works_count = write_jsonl_rows((row for row in _works_rows(books)), works_path)
    connection = duckdb.connect(str(building))
    try:
        connection.execute(SCHEMA_SQL)
        connection.execute(CHAPTER_HEADS_SQL)
        connection.execute(
            "INSERT OR REPLACE INTO sources (id, dataset, source_type, license, quality, quality_status) "
            "VALUES (?, 'niutrans', 'official_snapshot', "
            "'MIT（仓库 LICENSE；数据文件另须保留各目录 数据来源.txt）', 'source_backed', 'source_backed')",
            [DEFAULT_SOURCE_ID],
        )
        for path in (bilingual_path, classical_path):
            _insert_json(connection, "historical_texts", path)
        _insert_json(connection, "works", works_path, WORK_COLUMNS)
        _insert_json(connection, "chapter_heads", heads_path,
                     ("book_id", "work_title", "section", "chapter", "head_text"))
        connection.execute("CHECKPOINT")
    finally:
        connection.close()
    if target.exists():
        target.unlink()
    building.replace(target)
    return {
        "snapshot": str(snapshot),
        "snapshot_version": snapshot.name,
        "texts_bilingual": bilingual_count,
        "texts_classical": classical_count,
        "chapter_heads": heads_count,
        "works": works_count,
        "database": str(target),
    }


def _iter_jsonl(path: Path) -> Iterator[dict]:
    if not path.exists():
        return
    with path.open(encoding="utf-8") as stream:
        for line in stream:
            if line.strip():
                yield json.loads(line)


def _collect_book_titles(bilingual_path: Path, classical_path: Path,
                         curated: dict[str, str]) -> list[tuple[str, str]]:
    """(title, work_id) 去重列表；curated 命中的书不产 work 行（dist 由种子提供）。"""
    seen: dict[str, str] = {}
    for path in (bilingual_path, classical_path):
        for row in _iter_jsonl(path):
            title = row["title_zh_cn"]
            if title not in seen:
                seen[title] = row["book_id"]
    return [(title, work_id) for title, work_id in sorted(seen.items()) if not work_id.startswith("work-curated-")]


def _works_rows(books: list[tuple[str, str]]) -> list[dict]:
    rows = []
    for title, work_id in books:
        rows.append({
            "id": work_id, "title": title, "title_raw": title, "title_zh_cn": title,
            "source_ids": f'["{DEFAULT_SOURCE_ID}"]', "source_id": DEFAULT_SOURCE_ID,
            "quality_status": "source_backed", "book_type": "bilingual_corpus",
        })
    return rows
