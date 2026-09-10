"""Check whether event_evidence.historical_text_id resolves inside the parquet corpus."""
import duckdb

con = duckdb.connect(r"D:\code\self-github\self-tools\history-data-pipeline\dist\history.duckdb", read_only=True)
rows = con.execute(
    "SELECT DISTINCT historical_text_id FROM event_evidence "
    "WHERE historical_text_id IS NOT NULL AND historical_text_id != ''"
).fetchall()
con.close()

ids = [r[0] for r in rows]
print("event_evidence distinct historical_text_id:", len(ids))
print("sample:", ids[:10])

con2 = duckdb.connect()
tbl = "dist/parquet/historical_texts.parquet"
q = (
    "SELECT count(*) FROM read_parquet(?) WHERE id IN (SELECT unnest(?))"
)
hit = con2.execute(q, [tbl, ids]).fetchone()[0]
print("resolved in parquet:", hit)
con2.close()