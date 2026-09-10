"""Completeness profile of dist/history.duckdb + parquet exports."""
import duckdb

con = duckdb.connect(r"D:\code\self-github\self-tools\history-data-pipeline\dist\history.duckdb", read_only=True)


def q(sql):
    return con.execute(sql).fetchall()


print("== events by importance ==")
for r in q("SELECT importance, count(*) FROM events GROUP BY 1 ORDER BY 2 DESC"):
    print(r)

print("== events by quality_status ==")
for r in q("SELECT quality_status, count(*) FROM events GROUP BY 1 ORDER BY 2 DESC"):
    print(r)

print("== events per period ==")
for r in q(
    "SELECT p.name_zh_cn, count(*) FROM events e JOIN periods p ON e.period_id=p.id GROUP BY 1 ORDER BY 2 DESC"
):
    print(r)

print("== timestamps: period coverage of people directly ==")
print(q("SELECT count(*) FROM people WHERE period_ids IS NULL OR period_ids = ''"))
print(q("SELECT count(*) FROM people WHERE regime_ids IS NULL OR regime_ids = ''"))

print("== event_person/place coverage ==")
print(
    q(
        "SELECT (SELECT count(DISTINCT event_id) FROM event_person), "
        "(SELECT count(DISTINCT event_id) FROM event_place), "
        "(SELECT count(*) FROM events), "
        "(SELECT count(*) FROM event_person), "
        "(SELECT count(*) FROM event_place)"
    )
)

print("== people per period (via event path) ==")
for r in q(
    "SELECT p.name_zh_cn, count(DISTINCT ep.person_id) "
    "FROM event_person ep JOIN events e ON ep.event_id=e.id "
    "JOIN periods p ON e.period_id=p.id GROUP BY 1 ORDER BY 2 DESC"
):
    print(r)

print("== people with period_ids set (direct) ==")
for r in q(
    "SELECT canonical_name_zh_cn, period_ids FROM people WHERE period_ids IS NOT NULL AND period_ids != '' LIMIT 20"
):
    print(r)

print("== empty mirrors ==")
print(
    q(
        "SELECT (SELECT count(*) FROM person_relations), "
        "(SELECT count(*) FROM person_place), "
        "(SELECT count(*) FROM fact_assertions), "
        "(SELECT count(*) FROM historical_texts), "
        "(SELECT count(*) FROM dynasties), "
        "(SELECT count(*) FROM works)"
    )
)
con.close()

print("== parquet exports ==")
con2 = duckdb.connect()
for f in ("historical_texts", "people", "event_evidence", "events"):
    n = con2.execute(f"SELECT count(*) FROM read_parquet('dist/parquet/{f}.parquet')").fetchone()[0]
    print(f, n)