# -*- coding: utf-8 -*-
"""Post-fix QA: recount backward relations + rerun Phase-1 checks on rebuilt dist DB."""
import sys

import duckdb

sys.stdout.reconfigure(encoding="utf-8")
db = duckdb.connect("dist/history.duckdb", read_only=True)

q = lambda sql: db.execute(sql).fetchone()[0]

print("event_relations total =", q("SELECT count(*) FROM event_relations"))
print(
    "backward(leads_to/precedes) =",
    q(
        "SELECT count(*) FROM event_relations r JOIN events e1 ON e1.id=r.source_event_id "
        "JOIN events e2 ON e2.id=r.target_event_id "
        "WHERE e1.end_year IS NOT NULL AND e2.start_year < e1.end_year "
        "AND r.relation_type IN ('leads_to','precedes')"
    ),
)
print("dangling source =", q(
    "SELECT count(*) FROM event_relations r LEFT JOIN events e ON e.id=r.source_event_id WHERE e.id IS NULL"))
print("dangling target =", q(
    "SELECT count(*) FROM event_relations r LEFT JOIN events e ON e.id=r.target_event_id WHERE e.id IS NULL"))
print("self-loops =", q("SELECT count(*) FROM event_relations WHERE source_event_id=target_event_id"))
print("duplicates(s,t,type) =", q(
    "SELECT count(*) FROM (SELECT source_event_id,target_event_id,relation_type,count(*) c "
    "FROM event_relations GROUP BY 1,2,3 HAVING c>1)"))
# the 7 fixed pairs: verify old wrong edges gone
fixed = [
    ("event-ran-wei", "event-qian-yan-qiang"),
    ("event-fu-jian-wangmeng", "event-qian-yan-qiang"),
    ("event-yanya-haizhan", "event-song-meng-zhanzheng"),
    ("event-sui-mie-chen", "event-chenbaxian-jianzhen"),
    ("event-tang-mie-gaogouli", "event-baijiangkou-zhizhan"),
    ("event-tubo-ru-changan", "event-dafeichuan-zhizhan"),
    ("event-wu-zhao-linchao", "event-dafeichuan-zhizhan"),
]
for s, t in fixed:
    n = q(f"SELECT count(*) FROM event_relations WHERE source_event_id='{s}' AND target_event_id='{t}' AND relation_type IN ('leads_to','precedes')")
    print(f"removed? {s} -> {t}: {'OK(0)' if n == 0 else f'STILL PRESENT x{n}'}")
added = [
    ("event-qian-yan-qiang", "event-fu-jian-wangmeng"),
    ("event-dafeichuan-zhizhan", "event-tubo-ru-changan"),
]
for s, t in added:
    n = q(f"SELECT count(*) FROM event_relations WHERE source_event_id='{s}' AND target_event_id='{t}'")
    print(f"added? {s} -> {t}: {'OK(>=1)' if n >= 1 else 'MISSING'}")
