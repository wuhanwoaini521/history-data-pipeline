"""One-off audit: table inventory + referential connectivity in dist/history.duckdb."""
import json
import sys
import duckdb

DB = r"D:\code\self-github\self-tools\history-data-pipeline\dist\history.duckdb"
OUT = r"D:\code\self-github\self-tools\history-data-pipeline\tools\audit_connectivity_out.json"

con = duckdb.connect(DB, read_only=True)

report = {"tables": {}, "checks": []}


def add_check(name, ok, broken, total, detail=""):
    report["checks"].append(
        {"name": name, "ok": ok, "broken": broken, "total": total, "detail": detail}
    )


# ---- inventory ----
tables = con.execute(
    "SELECT table_name FROM information_schema.tables ORDER BY table_name"
).fetchall()
for (t,) in tables:
    n = con.execute(f'SELECT count(*) FROM "{t}"').fetchone()[0]
    report["tables"][t] = n

# ---- schema of key tables ----
def cols(t):
    return [r[0] for r in con.execute(f'DESCRIBE "{t}"').fetchall()]


report["columns"] = {t[0]: cols(t[0]) for t in tables}

# ---- connectivity checks ----
def broken_refs(table, fk, pk_table, pk):
    q = f"""
    SELECT count(*) FROM "{table}" t
    LEFT JOIN "{pk_table}" p ON t."{fk}" = p."{pk}"
    WHERE t."{fk}" IS NOT NULL AND p."{pk}" IS NULL
    """
    return con.execute(q).fetchone()[0]


def total_nonnull(table, fk):
    return con.execute(
        f'SELECT count(*) FROM "{table}" WHERE "{fk}" IS NOT NULL'
    ).fetchone()[0]


# events -> period / regime
for fk, ref in [("period_id", "periods"), ("regime_id", "regimes")]:
    if fk in cols("events") and ref in report["tables"]:
        broken = broken_refs("events", fk, ref, "id")
        add_check(f"events.{fk} -> {ref}", broken == 0, broken, total_nonnull("events", fk), "")

# events -> dynasty fallback field names
for fk in ("dynasty_id", "period_dynasty_id"):
    if fk in cols("events"):
        broken = broken_refs("events", fk, "periods", "id")
        add_check(f"events.{fk} -> periods", broken == 0, broken, total_nonnull("events", fk), "")

# event_person
for fk, ref in [("event_id", "events"), ("person_id", "people")]:
    if "event_person" in report["tables"] and fk in cols("event_person") and ref in report["tables"]:
        broken = broken_refs("event_person", fk, ref, "id")
        total = total_nonnull("event_person", fk)
        add_check(f"event_person.{fk} -> {ref}", broken == 0, broken, total, "")

# event_place
for fk, ref in [("event_id", "events"), ("place_id", "places")]:
    if "event_place" in report["tables"] and fk in cols("event_place") and ref in report["tables"]:
        broken = broken_refs("event_place", fk, ref, "id")
        add_check(f"event_place.{fk} -> {ref}", broken == 0, broken, total_nonnull("event_place", fk), "")

# event_relations
if "event_relations" in report["tables"]:
    for fk in ("source_event_id", "target_event_id", "event_id", "related_event_id", "from_event_id", "to_event_id"):
        if fk in cols("event_relations"):
            broken = broken_refs("event_relations", fk, "events", "id")
            add_check(f"event_relations.{fk} -> events", broken == 0, broken, total_nonnull("event_relations", fk), "")

# story_events
if "story_events" in report["tables"]:
    for fk, ref in [("story_id", "stories"), ("event_id", "events")]:
        if fk in cols("story_events") and ref in report["tables"]:
            broken = broken_refs("story_events", fk, ref, "id")
            add_check(f"story_events.{fk} -> {ref}", broken == 0, broken, total_nonnull("story_events", fk), "")

# people -> period / regime
if "people" in report["tables"]:
    for fk in ("dynasty_id", "period_id", "regime_id"):
        if fk in cols("people"):
            broken = broken_refs("people", fk, "periods", "id")
            add_check(f"people.{fk} -> periods", broken == 0, broken, total_nonnull("people", fk), "")

# person_aliases -> people
if "person_aliases" in report["tables"]:
    broken = broken_refs("person_aliases", "person_id", "people", "id")
    add_check("person_aliases.person_id -> people", broken == 0, broken, total_nonnull("person_aliases", "person_id"), "")

# events' people linked back: people count referenced by events
try:
    ref_people = con.execute(
        'SELECT count(DISTINCT person_id) FROM event_person'
    ).fetchone()[0]
    total_people = report["tables"].get("people", 0)
    add_check("people linked from events", True, -1, ref_people,
              f"people referenced by events = {ref_people} / {total_people}")
except Exception as e:  # noqa: BLE001
    add_check("people linked from events", False, -1, -1, str(e))

# events without any period/regime link
try:
    ev_total = report["tables"].get("events", 0)
    ev_no_link = con.execute("""
        SELECT count(*) FROM events
        WHERE (period_id IS NULL OR period_id = '')
          AND (regime_id IS NULL OR regime_id = '')
    """).fetchone()[0]
    add_check("events without period/regime", ev_no_link == 0, ev_no_link, ev_total, "")
except Exception as e:  # pragma: BLE001
    add_check("events without period/regime", False, -1, -1, str(e))

# people without any event link
try:
    pe_total = report["tables"].get("people", 0)
    pe_linked = con.execute('SELECT count(DISTINCT person_id) FROM event_person').fetchone()[0]
    add_check("people linked to >=1 event", pe_linked == pe_total, pe_total - pe_linked, pe_total, "")
except Exception as e:  # pragma: BLE001
    add_check("people linked to >=1 event", False, -1, -1, str(e))

# ---- multi-value reference fields (comma separated ids) ----
def split_refs(table, field):
    """Return set of ids referenced by a JSON-array column (fallback: comma split)."""
    import json as _json

    ids = set()
    rows = con.execute(
        f'SELECT "{field}" FROM "{table}" WHERE "{field}" IS NOT NULL AND "{field}" != \'\''
    ).fetchall()
    for (v,) in rows:
        raw = str(v).strip()
        try:
            lst = _json.loads(raw)
            if isinstance(lst, list):
                for item in lst:
                    if item:
                        ids.add(str(item).strip())
                continue
            ids.add(str(lst).strip())
        except Exception:  # not JSON: comma split
            for part in raw.split(","):
                p = part.strip().strip('"[]')
                if p:
                    ids.add(p)
    return ids


def ids_of(table, pk="id"):
    return set(
        r[0] for r in con.execute(f'SELECT DISTINCT "{pk}" FROM "{table}"').fetchall()
    )


period_ids_set = ids_of("periods")
regime_ids_set = ids_of("regimes")

for table, field, ref_set, label in [
    ("events", "period_ids", period_ids_set, "events.period_ids -> periods"),
    ("events", "regime_ids", regime_ids_set, "events.regime_ids -> regimes"),
    ("events", "dynasty_ids", None, "events.dynasty_ids (no dynasties table)"),
    ("people", "period_ids", period_ids_set, "people.period_ids -> periods"),
    ("people", "regime_ids", regime_ids_set, "people.regime_ids -> regimes"),
    ("people", "dynasty_ids", None, "people.dynasty_ids (no dynasties table)"),
]:
    if field in cols(table):
        refs = split_refs(table, field)
        if ref_set is None:
            add_check(label, len(refs) == 0, len(refs), len(refs),
                      f"referenced ids: {sorted(refs)[:10]}")
        else:
            dangling = refs - ref_set
            add_check(label, len(dangling) == 0, len(dangling), len(refs),
                      f"dangling: {sorted(dangling)[:10]}" if dangling else "")

# event_evidence -> events
if "event_evidence" in report["tables"]:
    broken = broken_refs("event_evidence", "event_id", "events", "id")
    add_check("event_evidence.event_id -> events", broken == 0, broken,
              total_nonnull("event_evidence", "event_id"), "")
    # historical_text_id: references empty table? treat as pending link
    ht_id_total = total_nonnull("event_evidence", "historical_text_id")
    add_check("event_evidence.historical_text_id used", ht_id_total == 0, -1, ht_id_total,
              "all links are pending_knowledge (README: awaiting knowledge-store rebuild)")

# regimes.parent_regime_id / parent_dynasty_id
for fk, pk_ref in [("parent_regime_id", "regimes"), ("period_id", "periods")]:
    if fk in cols("regimes") and pk_ref in report["tables"]:
        broken = broken_refs("regimes", fk, pk_ref, "id")
        add_check(f"regimes.{fk} -> {pk_ref}", broken == 0, broken, total_nonnull("regimes", fk), "")
if "parent_dynasty_id" in cols("regimes"):
    n = total_nonnull("regimes", "parent_dynasty_id")
    add_check("regimes.parent_dynasty_id set", n == 0, -1, n, "dynasties table is empty")

con.close()

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=1)
print("written:", OUT)