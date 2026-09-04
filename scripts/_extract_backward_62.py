# -*- coding: utf-8 -*-
"""Read-only extraction of the 62 backward EventRelations marked in Phase 1 QA.

Exact Phase-1 definition (which yields exactly 62):
    target.start_year < source.end_year
    AND relation_type IN ('leads_to', 'precedes')

i.e. a leads_to/precedes edge whose target begins inside (or before) the source's
lifespan — the "backward pointing" set. Sources/targets printed with full metadata
for the agent_assisted_semantic_review step.
"""
import duckdb
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

DB = "dist/history.duckdb"
db = duckdb.connect(DB, read_only=True)

backward = db.execute(
    """
    SELECT
      r.source_event_id AS src, e1.name_zh_cn AS src_name,
      r.relation_type AS rel, r.confidence AS conf,
      e1.start_year AS src_start, e1.end_year AS src_end,
      e1.period_id AS src_period, e1.regime_id AS src_regime,
      e1.summary_zh_cn AS src_summary,
      r.target_event_id AS tgt, e2.name_zh_cn AS tgt_name,
      e2.start_year AS tgt_start, e2.end_year AS tgt_end,
      e2.period_id AS tgt_period, e2.regime_id AS tgt_regime,
      e2.summary_zh_cn AS tgt_summary,
      r.description_zh_cn AS rel_description
    FROM event_relations r
    JOIN events e1 ON e1.id = r.source_event_id
    JOIN events e2 ON e2.id = r.target_event_id
    WHERE e1.end_year IS NOT NULL
      AND e2.start_year IS NOT NULL
      AND r.relation_type IN ('leads_to', 'precedes')
      AND e2.start_year < e1.end_year
    ORDER BY e1.period_id, e1.start_year, r.relation_type, e2.start_year
    """
).fetchall()

cols = [
    "src", "src_name", "rel", "confidence", "src_start", "src_end",
    "src_period", "src_regime", "src_summary",
    "tgt", "tgt_name", "tgt_start", "tgt_end",
    "tgt_period", "tgt_regime", "tgt_summary", "relation_desc",
]

print(f"BACKWARD_COUNT = {len(backward)}")
rows = [dict(zip(cols, r)) for r in backward]
for r in rows:
    print(json.dumps(r, ensure_ascii=False))

with open("scripts/_backward_62.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=1)
print("saved scripts/_backward_62.json")