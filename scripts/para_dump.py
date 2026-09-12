#!/usr/bin/env python3
"""Dump knowledge-layer paragraphs of a chapter by paragraph-index range.

Usage:
  python scripts/para_dump.py <work-substr> <chapter> [--from N] [--to M]

Prints `#pN <text_id>` + simplified text for anchoring enrichment quotes.
Audit-only: reads data/normalized/history.duckdb.
"""

from __future__ import annotations

import argparse
import sys

import duckdb

TEXT_DB = "data/normalized/history.duckdb"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("work")
    ap.add_argument("chapter")
    ap.add_argument("--from", dest="lo", type=int, default=0)
    ap.add_argument("--to", dest="hi", type=int, default=10**9)
    args = ap.parse_args()

    con = duckdb.connect(TEXT_DB, read_only=True)
    rows = con.execute(
        """
        select id, paragraph_index, original_simplified
        from historical_texts
        where book_id like ? and chapter = ?
        order by paragraph_index
        """,
        [f"%{args.work}%", args.chapter],
    ).fetchall()
    if not rows:
        print("NO ROWS", file=sys.stderr)
        return 1
    for tid, pidx, text in rows:
        if pidx < args.lo or pidx > args.hi:
            continue
        print(f"#p{pidx} {tid}")
        print((text or "").strip())
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
