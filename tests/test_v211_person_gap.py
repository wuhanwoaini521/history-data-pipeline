"""China History Backbone V2.1.1 · Critical Person Knowledge Gap Recovery — 测试。

验证：34 条 frozen scope；4 resolved_existing / 2 ambiguous / 28 supplemental（24 unique Person）；
补充 Person 全部落在 data/curated/persons/；new 链接 append-only（store 总 142 persons）；
ambiguous（刘玄、朱德）不建 Person 且以 null ambiguous 记录在 accepted review。
"""

from __future__ import annotations

from pathlib import Path

import pytest

from history_data_pipeline.backbone.loader import load_backbone, _iter_yaml_files
from history_data_pipeline.backbone.reference import resolve_references

from history_data_pipeline.v211_gap import (
    FROZEN_SCOPE, RESOLVED_EXISTING, AMBIGUOUS_GAPS, SUPPLEMENT_IDS,
    PERSON_SPECS, resolve_verdict,
)

ROOT = Path(__file__).parents[1]
STORE_DIR = ROOT / "data" / "curated" / "history_backbone" / "event_person"
PERSONS_DIR = ROOT / "data" / "curated" / "persons"
ACC_DIR = ROOT / "data" / "reviews" / "accepted" / "event_person"


@pytest.fixture(scope="module")
def backbone():
    return load_backbone(ROOT)


def _store_people():
    people = []
    for path in _iter_yaml_files(STORE_DIR):
        import yaml
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        for person in doc.get("people", []):
            people.append({"event_id": doc["event_id"], **person})
    return people


def test_scope_parsed_exactly_34(backbone):
    ids = {e["id"] for e in backbone.events}
    assert len(FROZEN_SCOPE) == 34
    for eid, _ in FROZEN_SCOPE:
        assert eid in ids


def test_classification_counts():
    from collections import Counter
    verdicts = Counter(resolve_verdict(eid, name)["verdict"] for eid, name in FROZEN_SCOPE)
    assert verdicts == {"supplemental": 28, "resolved_existing": 4, "ambiguous": 2}
    assert len(PERSON_SPECS) == 24  # 28 条补充 -> 24 位唯一 Person


def test_resolved_existing_are_real_ids():
    for (eid, name), meta in RESOLVED_EXISTING.items():
        assert meta["person_id"] not in PERSON_SPECS
        assert resolve_verdict(eid, name)["verdict"] == "resolved_existing"


def test_ambiguous_not_supplemented():
    store = _store_people()
    assert len(AMBIGUOUS_GAPS) == 2
    for (eid, name) in AMBIGUOUS_GAPS:
        assert name in {"刘玄", "朱德"}
        assert resolve_verdict(eid, name)["verdict"] == "ambiguous"
        assert not any(l["person_name_raw"] == name and l.get("person_id")
                       for l in store)


def test_ambiguous_recorded_in_accepted_review():
    for (eid, name) in AMBIGUOUS_GAPS:
        fp = ACC_DIR / f"{eid}.review.json"
        import json
        acc = json.loads(fp.read_text(encoding="utf-8"))
        assert any(x.get("person_name_raw") == name and x.get("person_id") is None
                   and x.get("resolution") == "ambiguous" for x in acc["accepted_links"])


def test_store_totals_after_v211():
    links = _store_people()
    assert len(links) == 142  # 58 legacy + 110 V2.1 + 32 V2.1.1
    supp_ids = set(SUPPLEMENT_IDS.values())
    assert len(supp_ids) == 24
    in_store = {l["person_id"] for l in links if l["person_id"]}
    assert supp_ids <= in_store


def test_person_files_exist():
    files = {p.stem for p in PERSONS_DIR.glob("*.yml")}
    assert len(files) == 24
    for pid in PERSON_SPECS:
        assert pid in files


def test_build_resolution_linked_200(backbone):
    result = resolve_references(backbone)
    assert result.persons["linked"] == 200  # 58 + 110 + 32
    assert result.broken == []


def test_dist_event_person_rows():
    db = ROOT / "dist" / "history.duckdb"
    if not db.exists():
        pytest.skip("dist 未构建")
    import duckdb
    with duckdb.connect(str(db), read_only=True) as connection:
        n = connection.execute("SELECT COUNT(*) FROM event_person").fetchone()[0]
        assert n == 200