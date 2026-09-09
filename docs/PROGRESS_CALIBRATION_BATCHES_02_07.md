# Calibration Batch 02–07 — Progress / Resume Document (COMPLETE)

Status: batches **COMPLETE** on 2026-09-09 — 52 candidates produced → 26
AUTO_ACCEPT promoted → dist rebuilt → 210 tests green → committed and pushed.

- Final report: `reports/current-run/calibration-batches-02-07-final-review.md`
- Metrics: `reports/calibration_batches_02_07_metrics.json`
- Batch plan: `reports/_calibration_batch_plan.json`
- Promotion/verdict set: `reports/_promotion_set.json`

## 1. State

- Producer: `scripts/calibration_produce_candidates.py` — transcribed canonical
  `source_reference` → term-level evidence rows only.
- Deterministic gates: `backbone validate` 0 errors; strict gate PASS; build
  event_evidence 44 → 98; pytest 210 passed.
- Scores: 26 AUTO_ACCEPT (90.9–96.0, mean 93.9), 26 QUARANTINE_MEDIUM
  (81.0–87.7). No hard failures.

## 2. Current status (2026-09-09)

- **PROMOTED**: 26 AUTO candidates merged into canonical
  `data/curated/history_backbone/events/…` (adds `evidence`,
  `background_zh_cn`, `result_zh_cn`, `source_ids`; clean `summary_zh_cn`).
  No new events/people/places invented; people stay in the event_person
  denormalized store (not written into event YAML).
- **QUARANTINED** 26 (QUARANTINE_MEDIUM, non-error): candidates preserved under
  `data/candidates/batch02..07/` with sources; reason = no chapter-level term
  in `source_reference` (evidence_precision 6.7 or 0.0).
  Follow-up path in final review §7.

## 3. Resume commands

    PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe -m history_data_pipeline.cli backbone status
    .venv\Scripts\python.exe -m pytest

## 4. Known queue — next logical batch

- Calibration Batch 08 (quarantine remediation): add chapter terms for batch04/05
  events (候梁/郭威/陈桥…) and for 20th-century events wire archival shelf
  chapter-level refs where the primary accounting (first-hand reports/books with
  concrete chapter) is available.

## 5. Owners / policy notes

- DATA_VERSION remains `2026.09.0` (data-shape unchanged; enrichment only).
- An earlier optimistic scoring pass (52 AUTO) is explicitly NOT authoritative;
  see final review §6.