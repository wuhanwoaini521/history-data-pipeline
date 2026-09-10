# Calibration Batch 02–07 — Progress / Resume Document (COMPLETE + Rescue)

Status: batches **COMPLETE** as of 2026-09-10 — 52 candidates produced → **42
AUTO_ACCEPT promoted** (incl. the 2026-09-10 rescue pass: 16 quarantine events
gained a second real evidence chapter) → 10 QUARANTINE_MEDIUM residual → dist
rebuilt → test suite green → committed and pushed.

- Final report: `reports/current-run/calibration-batches-02-07-final-review.md`
- Metrics: `reports/calibration_batches_02_07_metrics.json`
- Batch plan: `reports/_calibration_batch_plan.json`
- Promotion/verdict set: `reports/_promotion_set.json`

## 1. State

- Producer: `scripts/calibration_produce_candidates.py` — transcribed canonical
  `source_reference` → term-level evidence rows only.
- Deterministic gates: `backbone validate` 0 errors; strict gate PASS; build
  event_evidence 44 → 98 → **130** (2026-09-10 rescue +32 rows); pytest green.
- Rescue (2026-09-10): `scripts/_tmp_rescue16.py` dual-wrote a second
  supporting evidence row (registered work + term present in the extended
  `source_reference`, `source_ids` extended, `source_reference` punctuation
  normalized) into candidate + canonical for all 16 fixable quarantine events;
  post-rescore with `score_event`: **42 AUTO_ACCEPT** (90.9–96.0, mean 93.9),
  **10 QUARANTINE_MEDIUM** (81.0–87.7). No hard failures.

## 2. Current status

- **PROMOTED**: 42 AUTO candidates merged into canonical
  `data/curated/history_backbone/events/…` (`evidence`, `background_zh_cn`,
  `result_zh_cn`, `source_ids`; clean `summary_zh_cn`). No invented
  events/people/places; people stay in the `event_person` denormalized store.
- **QUARANTINED (10, QUARANTINE_MEDIUM)**: candidates preserved under
  `data/candidates/batch02..07/`; no second chapter-level term in
  `source_reference` yet (evidence_precision 6.7 or 0); follow-ups in final
  review §7.

## 3. Resume commands

    PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe -m history_data_pipeline.cli backbone status
    .venv\Scripts\python.exe -m pytest

## 4. Known queue — next logical batch

- Residual quarantine remediation (10): dynasty-founding events (batch04) need
  a real chapter term; the 20th-century archival-citation events (batch06/07)
  await knowledge-layer chapter mapping — no fabricated terms.

## 5. Owners / policy notes

- DATA_VERSION remains `2026.09.0` (data-shape unchanged; enrichment only).
- An earlier optimistic scoring pass (52 AUTO) is explicitly NOT authoritative;
  see final review §6.
- Rescue rows contain zero invented data: every added row's work id resolves
  from `reference.py` at runtime and its term appears in the extended
  `source_reference` text.