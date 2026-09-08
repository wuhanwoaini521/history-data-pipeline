"""Enrichment orchestrator tests (bootstrap run: score + quarantine + audit).

Covers: parse_year coercion (never invents), temporal conflict rules,
candidate intake shapes, build_report artifact writing, determinism.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from history_data_pipeline.backbone.enrichment import (
    REPORT_FILES,
    TemporalInventory,
    build_report,
    check_curated_person_lifespans,
    check_event_person_temporal,
    check_event_place_temporal,
    iter_candidate_documents,
    parse_year,
)
from history_data_pipeline.backbone.quality import (
    VERDICT_QUARANTINE_LOW,
    VERDICT_QUARANTINE_MEDIUM,
)

ROOT = Path(__file__).parents[1]


# ---------------------------------------------------------------------------
# parse_year — never invents
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "raw,expected",
    [
        (None, None),
        ("", None),
        (0, 0),
        (200, 200),
        (-770, -770),
        ("-770", -770),
        ("256", 256),
        ("100s", 100),  # 's' 后缀（风俗纪年）剥除
        ("公元前722", None),  # 中文纪年不猜
        ("元前", None),
        (True, None),
        (3.9, 3),
    ],
)
def test_parse_year_coercion(raw, expected):
    assert parse_year(raw) == expected


# ---------------------------------------------------------------------------
# Temporal rules (G2) — only fire when window known
# ---------------------------------------------------------------------------


def _inv(person=None, place=None):
    return TemporalInventory(
        persons={"p1": person} if person is not None else {},
        places={"pl1": place} if place is not None else {},
    )


def test_person_born_after_event_end_conflict():
    inv = _inv(person=(200, 250))
    event = {
        "id": "e1",
        "start_year": 100,
        "end_year": 120,
        "people": [{"person_id": "p1", "person_name_raw": "甲"}],
    }
    errors = check_event_person_temporal(event, inv)
    assert errors and "p1" in errors[0]


def test_person_died_before_event_start_conflict():
    inv = _inv(person=(-300, -200))
    event = {
        "id": "e2",
        "start_year": -100,
        "people": [{"person_id": "p1", "person_name_raw": "甲"}],
    }
    assert check_event_person_temporal(event, inv)


def test_person_within_lifespan_ok():
    inv = _inv(person=(-100, 200))
    event = {
        "id": "e3",
        "start_year": 50,
        "end_year": 60,
        "people": [{"person_id": "p1"}],
    }
    assert check_event_person_temporal(event, inv) == []


def test_unknown_person_years_skipped():
    # 关键不变式：不知道就不猜，绝不产生冲突
    inv = _inv(person=(None, None))
    event = {"id": "e4", "start_year": 1911, "people": [{"person_id": "p1"}]}
    assert check_event_person_temporal(event, inv) == []


def test_place_window_conflict_and_ok():
    inv = _inv(place=(None, 50))
    event = {
        "id": "e5",
        "start_year": 100,
        "places": [{"place_id": "pl1", "place_name_raw": "某地"}],
    }
    assert check_event_place_temporal(event, inv)
    inv_ok = _inv(place=(None, 500))
    assert (
        check_event_place_temporal(
            {"id": "e6", "start_year": 100, "places": [{"place_id": "pl1"}]}, inv_ok
        )
        == []
    )


def test_lifespan_inversion_detected():
    inv = TemporalInventory(persons={"p1": (300, 200)})
    assert check_curated_person_lifespans(inv)  # birth > death


def test_event_without_date_never_flags():
    inv = _inv(person=(2000, None))
    event = {"id": "e7", "people": [{"person_id": "p1"}]}  # no start_year
    assert check_event_person_temporal(event, inv) == []


# ---------------------------------------------------------------------------
# Candidate intake
# ---------------------------------------------------------------------------


def test_candidate_intake_container_and_bare(tmp_path):
    (tmp_path / "a").mkdir()
    (tmp_path / "a" / "one.yml").write_text(
        "version: backbone-candidates-v1\ncandidates:\n"
        "  - id: cand-1\n    name_zh_cn: 甲\n    start_year: -770\n",
        encoding="utf-8",
    )
    (tmp_path / "events.yml").write_text(
        "events:\n" "  - id: cand-2\n    name_zh_cn: 乙\n    start_year: 0\n",
        encoding="utf-8",
    )
    (tmp_path / "bare.yml").write_text("id: cand-3\nname_zh_cn: 丙\n", encoding="utf-8")
    docs = [d for _, d in iter_candidate_documents(tmp_path)]
    ids = {d["id"] for d in docs}
    assert ids == {"cand-1", "cand-2", "cand-3"}
    assert all("_source" in d for d in docs)


def test_candidate_bad_yaml_flagged(tmp_path):
    (tmp_path / "broken.yml").write_text("id: [unclosed\n", encoding="utf-8")
    docs = [d for _, d in iter_candidate_documents(tmp_path)]
    assert "_error" in docs[0]


# ---------------------------------------------------------------------------
# build_report (integration over the real backbone, tmp report dir)
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def run_report(tmp_path_factory):
    report_dir = tmp_path_factory.mktemp("current-run") / "current-run"
    return build_report(ROOT, report_dir=report_dir, sample_size=3, seed=1)


def test_report_files_written(run_report):
    for name in REPORT_FILES:
        path = run_report.report_dir / name
        assert path.exists(), f"{name} missing"


def test_report_format(run_report):
    quarantine = (
        (run_report.report_dir / "quarantine.jsonl").read_text(encoding="utf-8").strip()
    )
    for line in quarantine.splitlines():
        json.loads(line)  # 每行 JSON


def test_metrics_keys(run_report):
    m = run_report.metrics
    assert m["counts"]["backbone_events"] > 0
    assert set(m["counts"]) >= {
        "backbone_events",
        "candidates",
        "accepted",
        "quarantined",
        "audited",
    }
    assert set(m["score"]) >= {"mean", "min", "max", "histogram"}
    hist = m["score"]["histogram"]
    assert sorted(hist) == ["0-74", "75-89", "90-100"]


def test_audit_sample_is_deterministic(tmp_path):
    a = build_report(ROOT, report_dir=str(tmp_path / "r1"), sample_size=3, seed=7)
    b = build_report(ROOT, report_dir=str(tmp_path / "r2"), sample_size=3, seed=7)
    assert a.metrics["audit"] == b.metrics["audit"]
    assert a.metrics["counts"]["audited"] == 3


def test_seed_changes_audit_sample(tmp_path):
    a = build_report(ROOT, report_dir=str(tmp_path / "r1"), sample_size=3, seed=1)
    b = build_report(ROOT, report_dir=str(tmp_path / "r2"), sample_size=3, seed=99)
    assert a.metrics["audit"] != b.metrics["audit"]


def test_no_curated_mutation(tmp_path):
    curated_before = sorted((ROOT / "data/curated/history_backbone").rglob("*"))
    build_report(ROOT, report_dir=str(tmp_path / "r"), sample_size=0)
    curated_after = sorted((ROOT / "data/curated/history_backbone").rglob("*"))
    assert curated_before == curated_after  # 只读；绝不写 canonical


# ---------------------------------------------------------------------------
# candidate quarantine integration
# ---------------------------------------------------------------------------


def test_candidate_quarantine_intake(tmp_path):
    (tmp_path / "candidates").mkdir()
    (tmp_path / "candidates" / "bad.yml").write_text(
        "candidates:\n"
        "  - id: cand-x\n"
        "    name_zh_cn: 无来源无证据\n"
        "    start_year: 300\n",
        encoding="utf-8",
    )
    report = build_report(
        ROOT,
        report_dir=str(tmp_path / "report"),
        candidate_dir=str(tmp_path / "candidates"),
        sample_size=1,
        seed=1,
    )
    quarantine = (
        (tmp_path / "report" / "quarantine.jsonl").read_text(encoding="utf-8").strip()
    )
    rows = [json.loads(line) for line in quarantine.splitlines()]
    assert rows, "candidate 应产生隔离行"
    assert any(r.get("id") == "cand-x" and r.get("source") == "candidate" for r in rows)
    assert any(
        r["verdict"] in (VERDICT_QUARANTINE_LOW, VERDICT_QUARANTINE_MEDIUM)
        for r in rows
    )
    assert report.metrics["counts"]["candidates"] == 1
    assert report.metrics["counts"]["quarantined"] >= 1
