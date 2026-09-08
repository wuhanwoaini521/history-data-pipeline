# Goal Reference — Backbone QA + Enrichment Framework Bootstrap

> Reference target for a short `/goal` objective. This file holds the full
> long-form objective that exceeded the `/goal` character budget (9.5k > 4k).
> A `/goal` set it as: *"Bootstrap the autonomous backbone QA + enrichment
> framework. See docs/GOAL_BACKBONE_BOOTSTRAP.md."*

## 1. Mission

Bootstrap the deterministic, autonomous **Quality-Assurance + Enrichment**
framework for the History module, per the governing pipeline policy in
`AGENTS.md` (read it first) and the existing-in-repo architecture.

The framework is **read-only for `data/curated`, score-with-candidates, and
report-with-proof**. It must not invent facts, not mutate canonical data, and
not ask a human to adjudicate ordinary enrichment batches.

## 2. Scope of work (completed items in this bootstrap)

| # | Deliverable | Location |
| --- | --- | --- |
| 1 | Governing-policy read + full repository audit | `AGENTS.md`, repo tree |
| 2 | Policy / schema docs | `docs/QUALITY_GATES.md`, `docs/DATA_ENRICHMENT_POLICY.md`, `docs/SOURCE_POLICY.md`, `docs/DATA_MODEL.md` (§ "Schema 等价映射") |
| 3 | Deterministic validation reuse + new G2 temporal rules | live in `backbone/validate.py` + `backbone/enrichment.py` |
| 4 | Automated 100-point scoring (AGENTS.md §16) | `backbone/quality.py` `score_event` |
| 5 | Report generator: `summary.md` / `quarantine.jsonl` / `audit-report.md` / `metrics.json` | CLI `history-data backbone qa-run` |
| 6 | Tests for validation + scoring + pipeline | `tests/test_backbone_quality.py`, `tests/test_backbone_enrichment.py` |
| 7 | Bootstrap run + report | `reports/current-run/bootstrap-report.md` |

## 3. Non-negotiable constraints

1. `AGENTS.md` is the governing policy (No Guessing, Quarantine-not-block,
   Autonomous execution, Batch rule, Event-driven).
2. Never write into `data/curated` from the QA run (read-only for scoring).
3. Quality scores live in reports; the schema does not persist the score.
4. No new parallel schemas/directories; reuse `schemas/*.json` + taxonomy.
5. No invented facts, dates, coordinates, sources, or quotations.
6. Human review happens at the end of a batch; nothing may force a stop for a
   single ambiguous record (quarantine and continue).
7. Never count copied Tier-C sources as independent verification.
8. Score model must implement the AGENTS.md §16 weights and hard-failure
   override; thresholds 90/75.

## 4. Definition of Done

A batch is done when all of: candidates generated where possible (`qa run`),
deterministic tests completed and green, verification completed, quality gates
applied, failed records quarantined (not deleted), sample audit generated,
metrics + report written, and `pytest` green.

## 5. Method

Autonomous execution; do not ask “should I continue”. 用 batches: 10–50 events
per batch. Generate reports to `reports/current-run/`. Provide the user a final
human-readable bootstrap report with metrics and known gaps. Do not claim
success based only on file generation.

## 6. Status (bootstrap done)

- `210 passed` (repo baseline 170 remained green; 40 new QA-enrichment tests).
- `reports/current-run/` and `reports/current-run-candidates/` generated,
  deterministic seed=1, audited=3, no hard failures, no curation mutation.
- Bootstrap report: `reports/current-run/bootstrap-report.md`.
