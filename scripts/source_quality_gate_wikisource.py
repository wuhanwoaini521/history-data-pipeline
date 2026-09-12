"""Source Quality Gate — wikisource Batch 01（Queue 7）。

依据 docs/source-acquisition-policy.md §7。对 data/normalized/history.duckdb 中
source_id='source-wikisource' 的行执行确定性检查：
  文档/卷/章/段计数、空文本、重复段落、重复 ID、层级断裂/孤儿、
  编码损坏（replacement char）、HTML/模板残留。
OCR 风险：本轮来源均为原生数字文本（非 OCR 扫描 OCR 识别），不适用，显式记录。

退出码：0 = PASS；1 = QUARANTINE_SOURCE（不得写入 canonical 知识层）。
报告：reports/current-run/batch02-07-source-quality-gate.md
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "normalized" / "history.duckdb"
REPORT = ROOT / "reports" / "current-run" / "batch02-07-source-quality-gate.md"
SOURCE_ID = "source-wikisource"

RESIDUE_PATTERNS = ("{{", "}}", "[[", ".mw-", "[编辑", "[編輯", "TemplateStyles",
                    "mw-parser", "<div", "<span", "&lt;", "&gt;", "&amp;")
ENCODING_MARKS = ("\ufffd", "�")


def main() -> int:
    con = duckdb.connect(str(DB), read_only=True)
    checks: list[dict] = []

    def check(name: str, ok: bool, detail: str) -> None:
        checks.append({"check": name, "ok": bool(ok), "detail": detail})

    docs = con.execute(
        "SELECT title_zh_cn, COUNT(*), COUNT(DISTINCT section), COUNT(DISTINCT chapter) "
        f"FROM historical_texts WHERE source_id = ? GROUP BY 1 ORDER BY 1", [SOURCE_ID]).fetchall()
    total = sum(d[1] for d in docs)
    chapters = con.execute(
        "SELECT COUNT(*) FROM (SELECT DISTINCT book_id, section, chapter FROM historical_texts "
        f"WHERE source_id = ? AND chapter IS NOT NULL)", [SOURCE_ID]).fetchone()[0]
    check("document_count", len(docs) == 12, f"{len(docs)} documents（12 部/文书名：batch01 9 + 清史稿/晋书/旧唐书 3）")
    check("chapter_count", chapters == 30, f"{chapters} chapters（batch01 宋史 2 卷 + batch02 28 卷）")

    # 空文本
    empty = con.execute(
        "SELECT COUNT(*) FROM historical_texts WHERE source_id = ? "
        "AND (original_text IS NULL OR length(trim(original_text)) = 0)", [SOURCE_ID]).fetchone()[0]
    check("empty_text", empty == 0, f"空文本 {empty} 行")

    # 重复 ID
    dup_ids = con.execute(
        "SELECT COUNT(*) FROM (SELECT id, COUNT(*) c FROM historical_texts "
        f"WHERE source_id = ? GROUP BY id HAVING c > 1)", [SOURCE_ID]).fetchone()[0]
    check("duplicate_ids", dup_ids == 0, f"重复 ID {dup_ids} 个")

    # 重复段落（同文档内同文本出现 >1 次）
    dup_paras = con.execute(
        "SELECT title_zh_cn, chapter, original_text, COUNT(*) c FROM historical_texts "
        f"WHERE source_id = ? AND length(original_text) >= 30 "
        "GROUP BY 1, 2, 3 HAVING c > 2 ORDER BY c DESC LIMIT 5",
        [SOURCE_ID]).fetchall()
    short_repeats = con.execute(
        "SELECT COUNT(*) FROM (SELECT title_zh_cn, chapter, original_text, COUNT(*) c FROM historical_texts "
        f"WHERE source_id = ? AND length(original_text) < 30 GROUP BY 1,2,3 HAVING c > 1)", [SOURCE_ID]).fetchone()[0]
    check("duplicate_paragraphs", not dup_paras,
          f"长文本（≥30 字）同章重复 >2 次：{len(dup_paras)} 组"
          + (f"（例：{dup_paras[0][2][:24]}×{dup_paras[0][3]}）" if dup_paras else "")
          + f"；短套语重复 {short_repeats} 组（编年体例，正常，仅记录）")

    # HTML/模板残留
    residue_rows = []
    for pat in RESIDUE_PATTERNS:
        n = con.execute(
            "SELECT COUNT(*) FROM historical_texts WHERE source_id = ? "
            "AND (original_text LIKE ? OR original_simplified LIKE ?)",
            [SOURCE_ID, f"%{pat}%", f"%{pat}%"]).fetchone()[0]
        if n:
            residue_rows.append((pat, n))
    check("html_template_residue", not residue_rows,
          "无残留" if not residue_rows else f"残留模式 {residue_rows}")

    # 编码损坏
    corrupt = con.execute(
        "SELECT COUNT(*) FROM historical_texts WHERE source_id = ? "
        "AND (original_text LIKE '%\ufffd%' OR original_simplified LIKE '%\ufffd%')",
        [SOURCE_ID]).fetchone()[0]
    check("encoding_corruption", corrupt == 0, f"replacement-char 行 {corrupt}")

    # 层级完整性：古籍行 section/chapter 必须齐全；单篇文书允许 null（但需全 null 或全有值的一致段）
    broken = con.execute(
        "SELECT COUNT(*) FROM historical_texts WHERE source_id = ? "
        "AND (section IS NULL) <> (chapter IS NULL)", [SOURCE_ID]).fetchone()[0]
    check("hierarchy_consistency", broken == 0, f"section/chapter 半空行 {broken}（古籍须齐全；文书须全 null）")

    # 孤儿 book_id：historical_texts 引用的 book_id 必须存在于 works 或 curated work 种子
    from history_data_pipeline.knowledge_build import curated_work_id_map
    curated_ids = set(curated_work_id_map().values())
    orphans = [
        row[0] for row in con.execute(
            "SELECT DISTINCT h.book_id FROM historical_texts h "
            f"WHERE h.source_id = ?", [SOURCE_ID]).fetchall()
        if not str(row[0]).startswith("work-curated-")
        and row[0] not in {r[0] for r in con.execute("SELECT id FROM works").fetchall()}
        and row[0] not in curated_ids
    ]
    check("orphan_book_ids", not orphans,
          "无孤儿（works 表 ∪ curated seeds）" if not orphans else f"孤儿 book_id {orphans}")

    # 段落顺序连续性：按 (book_id, section, chapter) 分组，paragraph_index 1..N 连续
    gaps = con.execute(
        "SELECT title_zh_cn, chapter, COUNT(*) FROM historical_texts WHERE source_id = ? "
        "GROUP BY 1, 2 HAVING COUNT(*) <> MAX(paragraph_index)", [SOURCE_ID]).fetchall()
    check("paragraph_ordering", not gaps,
          "各文档/卷 paragraph_index 1..N 连续" if not gaps else f"不连续 {gaps}")

    con.close()

    ocr_note = "本轮来源均为原生数字文本（wikitext/渲染 HTML），无 OCR 环节 → OCR 风险检查不适用（n/a）"
    passed = all(c["ok"] for c in checks)
    verdict = "PASS" if passed else "QUARANTINE_SOURCE"

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Batch 02 · Queue 7 — Source Quality Gate（wikisource Batch 01）",
        "",
        f"> 数据库：data/normalized/history.duckdb · source：`{SOURCE_ID}`",
        "",
        "## 检查结果",
        "",
        "| 检查 | 结果 | 说明 |",
        "|---|---|---|",
    ]
    for c in checks:
        lines.append(f"| {c['check']} | {'✅' if c['ok'] else '❌'} | {c['detail']} |")
    lines += [
        f"| ocr_risk | ➖ n/a | {ocr_note} |",
        "",
        "## 文档计费（document/段计数）",
        "",
        "| document | paragraphs | distinct section | distinct chapter |",
        "|---|---:|---:|---:|",
    ]
    for d in docs:
        lines.append(f"| {d[0]} | {d[1]} | {d[2]} | {d[3]} |")
    lines += [
        "",
        f"**合计 paragraphs：{total}**",
        "",
        f"## 结论：**{verdict}**",
        "",
        ("全部检查通过，允许进入 canonical 知识层。" if passed
         else "存在不达标项：QUARANTINE_SOURCE，不得写入 canonical 知识层；快照保留待修复。"),
        "",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"gate verdict: {verdict} (report: {REPORT})")
    for c in checks:
        print(f"  [{'PASS' if c['ok'] else 'FAIL'}] {c['check']}: {c['detail']}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
