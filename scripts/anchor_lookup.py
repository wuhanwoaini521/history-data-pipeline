#!/usr/bin/env python3
"""Anchor lookup helper for enrichment sprints.

Search the knowledge layer (data/normalized/history.duckdb) for paragraphs
matching a regex, printing the exact anchor tuple needed for manual evidence
records: work / chapter / paragraph_index -> anchor `section/chapter#pN`,
plus the canonical historical_text_id.

Usage:
  python scripts/anchor_lookup.py <work> <regex> [--limit N] [--ctx N] [--all]
    <work>   substring of book_id, e.g. jiutangshu, zizhitongjian, mingshi
    <regex>  regular expression over the simplified text

Audit-only tool: reads the knowledge DB, writes nothing.
"""

from __future__ import annotations

import argparse
import re
import sys

import duckdb


TEXT_DB = "data/normalized/history.duckdb"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("work")
    ap.add_argument("pattern")
    ap.add_argument("--limit", type=int, default=25)
    ap.add_argument("--ctx", type=int, default=60)
    ap.add_argument("--all", action="store_true", help="print every match, not grouped")
    args = ap.parse_args()

    con = duckdb.connect(TEXT_DB, read_only=True)
    rows = con.execute(
        """
        select id, book_id, section, chapter, paragraph_index, original_simplified
        from historical_texts
        where book_id like ?
        order by chapter, paragraph_index
        """,
        [f"%{args.work}%"],
    ).fetchall()

    rx = re.compile(args.pattern)
    hits = 0
    seen_chapters: dict[str, int] = {}
    for tid, book, section, chapter, pidx, text in rows:
        if not text:
            continue
        m = rx.search(text)
        if not m:
            continue
        hits += 1
        snip = text[max(0, m.start() - args.ctx) : m.end() + args.ctx].replace("\n", " ")
        anchor = f"{section}/{chapter}#p{pidx}"
        print(f"[{hits:3d}] {book} | {anchor} | {tid}")
        print(f"      {snip}")
        seen_chapters[chapter] = seen_chapters.get(chapter, 0) + 1
        if hits >= args.limit and not args.all:
            break
    print(f"-- {hits} hits --")
    if seen_chapters:
        top = sorted(seen_chapters.items(), key=lambda kv: -kv[1])[:12]
        print("chapters:", ", ".join(f"{c}:{n}" for c, n in top))
    return 0


if __name__ == "__main__":
    sys.exit(main())
