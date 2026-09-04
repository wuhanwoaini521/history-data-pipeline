# -*- coding: utf-8 -*-
"""Find the exact definition that yields 62 backward relations (Phase 1 marker)."""
import duckdb

db = duckdb.connect("dist/history.duckdb", read_only=True)

def n(cond):
    return db.execute(
        "SELECT count(*) FROM event_relations r "
        "JOIN events e1 ON e1.id=r.source_event_id "
        "JOIN events e2 ON e2.id=r.target_event_id WHERE " + cond
    ).fetchone()[0]

print("end-based backward, leads_to/precedes:", n('e1.end_year IS NOT NULL AND e2.start_year < e1.end_year AND r.relation_type IN (\'leads_to\',\'precedes\')'))
print("end-based, follows:", n('e1.end_year IS NOT NULL AND e2.start_year < e1.end_year AND r.relation_type = \'follows\''))
print("end-based, part_of:", n('e1.end_year IS NOT NULL AND e2.start_year < e1.end_year AND r.relation_type = \'part_of\''))
print("fully-before & leads_to:", n('r.relation_type = \'leads_to\' AND e2.end_year < e1.start_year'))
print("start-based backward, all:", n('e2.start_year < e1.start_year'))
print("Period-cross total:", n('e1.period_id <> e2.period_id'))
# Try: backward AND cross-period
print("backward(start) + cross-period:", n('e2.start_year < e1.start_year AND e1.period_id <> e2.period_id'))
# backward(end-based) exactly before start (target fully before source) + period cross
print("target.end<source.start + cross-period:", n('e2.end_year < e1.start_year AND e1.period_id <> e2.period_id'))

# 62??? try gap>=20 includes part_of/contributes? Already know 63 with leads/follows/precedes
# Try excluding 'precedes'?
print("end-based backward, leads_to/follows (no precedes):", n("e1.end_year IS NOT NULL AND e2.start_year < e1.end_year AND r.relation_type IN ('leads_to','follows')"))
print("gap>=19 ... all types:", n('e2.start_year < e1.start_year - 19'))