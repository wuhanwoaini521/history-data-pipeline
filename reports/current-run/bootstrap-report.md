# Bootstrap Report — Autonomous Enrichment + QA Framework

> Report `bootstrap-v1` · generated after framework bootstrap · seed=1
> Owner: history-data-pipeline automation (AGENTS.md §20).

This report describes the **initial bootstrap** of the deterministic enrichment
and QA framework per `docs/QUALITY_GATES.md`, not a data-enrichment batch. The
canonical `data/curated` dataset was treated as **read-only input** (AGENTS.md
§19); no record in it was modified by the bootstrap (verified by the
`test_no_curated_mutation` gate in `tests/test_backbone_enrichment.py`).

## 1. What was built

| Artifact | Path | Role |
| --- | --- | --- |
| Quality score engine | `src/history_data_pipeline/backbone/quality.py` | 100-point G4 scoring (AGENTS.md §16), verdict classification, hard-failure override (§17) |
| Enrichment/QA orchestrator | `src/history_data_pipeline/backbone/enrichment.py` | Validate → Score → Accept/Quarantine → Sample Audit → Report (G0–G5) |
| CLI entry | `src/history_data_pipeline/cli.py` | `history-data backbone qa-run` |
| Policy docs | `docs/QUALITY_GATES.md`, `docs/DATA_ENRICHMENT_POLICY.md`, `docs/SOURCE_POLICY.md` | Governing operating policy for the pipeline |
| Schema mapping | `docs/DATA_MODEL.md` § "Schema 等价映射" | No parallel schema; reuses `schemas/event.schema.json` + `event_evidence.schema.json` |
| Tests | `tests/test_backbone_quality.py`, `tests/test_backbone_enrichment.py` | 40 new tests (below) |

## 2. Test results

Full deterministic suite (no network):

```text
210 passed in 395.45s
```

- Pre-existing baseline: **170 passed** (unchanged, all green).
- New: `tests/test_backbone_quality.py` — **12 passed** (weights sum = 100,
  threshold classification, hard-failure override, per-dimension isolation,
  determinism, [0,100] bounds).
- New: `tests/test_backbone_enrichment.py` — **28 passed** (parse_year
  never-invents, temporal conflict rules G2, candidate intake shapes, report
  artifacts, deterministic seeded audit, no curated mutation, candidate
  quarantine integration).

## 3. First reference `qa-run` over the canonical backbone

Run: `.venv/Scripts/python.exe -m src.history_data_pipeline backbone qa-run
--candidate-dir data/candidates/backbone_events --report-dir
reports/current-run-candidates --seed 1`

| Metric | Value |
| --- | --- |
| Backbone events scored | 618 |
| Candidate events scored | 592 |
| Validation errors (G1) | 0 |
| AUTO_ACCEPT | 0 |
| QUARANTINE_MEDIUM (75–89) | 434 |
| QUARANTINE_LOW (0–74) | 776 |
| QUARANTINE_HARD | 0 |
| Audited (seeded sample, G5) | 3 |
| Mean / min / max score | 55.7 / 37.0 / 79.7 |

### Observations

- **No record auto-accepted.** Every scored record lands in quarantine. This is
  correct behavior for bootstrap: `QUALITY_GATES.md` and `SOURCE_POLICY.md`
  require two independent sources, precise evidence locators (`work`+`term`)
  and resolution markers that the current candidate set and legacy curated
  records do not yet carry. Scores are honest about missing evidence — they do
  **not** guess (§ No-Guessing).
- **Zero hard failures** — the deterministic G1 gate (broken refs, impossible
  chronology, `linked` without canonical ID) reports clean (0 errors).
- **Audit pool** draws from all review-accepted events + accepted candidates
  (AGENTS.md §18), seeded for reproducibility: `event-zuti-beifa`,
  `event-zhuge-liang-beifa`, `event-gaoping-zhizhan`.

## 4. Bootstrap output files

`reports/current-run/` (canonical backbone only, 618 events):

- `summary.md` — verdict counts + score histogram.
- `quarantine.jsonl` — per-record verdicts + reasons (0 rows; no hard
  violations).
- `audit-report.md` — seeded G5 audit queue (3 events * 5 check axes).
- `metrics.json` — machine-readable counts, score stats, histogram, audit ids.

`reports/current-run-candidates/` (candidate run, 592 candidates):

- Same four files; `quarantine.jsonl` holds every candidate because a
  discovery-stage candidate without sources/evidence cannot be accepted.

## 5. Known gaps (explicit, not silently filled)

- Curated records lack the two-independent-source marker and precise evidence
  locators needed to reach 90+ → the enrichment backlog (future batches)
  should add them **before** acceptance promotion.
- `event_evidence` rows exist (26) but `historical_texts` is empty — evidence
  locators reference works, not yet linked text tables.
- Audit report fields are placeholders ("needs_independent_audit"); an
  independent Verifier/Auditor fills real findings (docs `QUALITY_GATES.md` G5).

## 6. Scope boundary

No `data/curated` directory was written. No schema migration ran. No source was
invented. `reports/*` are non-canonical build artifacts and are safe to delete
and regenerate with `history-data backbone qa-run`.
