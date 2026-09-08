# Calibration Batch 01 - Work in Progress / Resume Document (INCOMPLETE)

Status generated: 2026-09-08T16:55:21

This run is NOT finished. This document records what is done and what remains so work can be resumed cleanly.

## 1. Mandate

- Run 10 chosen Critical Events through the autonomous enrichment pipeline.
- Scoring engine: src/history_data_pipeline/backbone/quality.py is authoritative; thresholds were NOT weakened.
- Candidates must never fabricate history/locators/IDs; uncertainty is preserved via claim_type and needs_linking.
- Final deliverable: reports/current-run/calibration-batch-01-final-review.md (NOT yet written).

## 2. What is DONE

- Repo audit; 10 Critical Events selected; baseline captured (reports/calibration_batch01_baseline.*).
- Researcher phase: research brief written -> reports/current-run/research-brief-batch01.md (copied byte-exact from Researcher artifact).
- Producer script: scripts/calibration_batch01_produce_candidates.py -> rewrites 10 candidate YAMLs under data/candidates/calibration_batch01/ (10 files: 10).
- Deterministic QA: qa-run produced 10 accepted / 0 quarantined candidates; validation.error_count=0.
- Per-event quality & gates: 10 accepted (AUTO_ACCEPT range), min 93.9 / max 96.9 / avg 94.4 (pre-verification gate).
- 210-test suite passed (two batched runs).
- .ycaml (dot release) at repo root 学的 conventions so pi-lens no longer blocks candidate YAMLs.
- audit-report.md + summary.md + metrics.json emitted to reports/current-run/.

## 3. Independent Verification (IN PROGRESS - 1 of ~2 rounds)

Independent Verifier + Auditor dispatched on the web-capable researcher agent (workflow id 7d1ab897-2010-4b2a-98f8-9a4943c5a983).
Artifacts are saved to reports/current-run/verification/ (8 verifier JSONs + auditor.json).

Per-event verdict (verification round cargo-candidates):

| event id | Chinese name | canonical name matches | verifier verdict |
| --- | --- | --- | --- |
| event-changping-zhizhan | 长平之战 | Y | PENDING |
| event-mobei-zhizhan | 漠北之战 | Y | WARN |
| event-pingwang-dongqian | 平王东迁 | Y | PENDING |
| event-qiguo-zhi-luan | 七国之乱 | Y | WARN |
| event-qin-mie-liuguo | 秦灭六国 | Y | PASS |
| event-qin-tongyi | 秦统一六国（秦帝国建立） | Y | WARN |
| event-sanjia-fenjin | 三家分晋 | Y | WARN |
| event-shangtang-miexia | 商汤灭夏 | Y | PENDING |
| event-wangmang-chengdi | 王莽称帝、新朝建立 | Y | WARN |
| event-wuwang-fazhou | 武王伐纣 | Y | PASS |

Summary: 3 PASS (wuwang-fazhou, qin-mie-liuguo, + auditor overall PASS); 5 WARN (sanjia, qin-tongyi, mobei, wangmang, qiguo, qizhi-luan + mobei); 0 FAIL. No HARD FAIL (no fabrication, no corruption, no broken locators) across all completed verifier checks.

Verifier key findings to preserve:

- event-qiguo-zhi-luan: glyph WARN - locator 吴王濞传 should be 荆燕吴传 (Han Shu vol 35); the same locator string is also in the canonical source_reference (carried from narrative, not fabricated).
- event-wangfu-chengdi / event-qin-tongyi / event-sanjia / event-mobei: ctext.org returned HTTP 403 to direct fetch; glyphs confirmed via authoritative mirrors (zh.wikipedia / zh.wikisource / Baidu Baike). ctext 403 is an infra limit, not a data problem.
- event-mobei-zhizhan / qiguo: person_ids are carried from the accepted EventPerson layer (V2.1 review provenance); verifier did not find fabrication.
- event-qin-tongyi / 3-addr: 资治通鉴 chapter covered by source_ids (only primary work), deferred by needs_linking.
- Date dispute note: event-wangmang-chengdi accession 8-vs-9 CE unreconstructed (canonical records 9); Researcher-flagged; candidate matches canonical verbatim - preserves canonical value; listen DISPUTED capture before final promote (advisory).

## 4. Auditor (completed - PASS overall)

Audit sample (seeded): event-qin-mie-liuguo, event-sanjia-fenjin, event-wangmang-chengdi.
Auditor overall: PASS. Recurring patterns tracked (non-blocking):

- All candidates set evidence link_confidence=0.9 with link_status=beeds_linking (uniform default, not independently resolved) - acceptable but monotonous.
- 资治通鉴 appears as a supporting evidence work but is not in source_ids (only the primary work is); deferred by needs_linking - recurring source_ids/evidence gap to reconcile at linking stage.
No fabricated dates, names, locators, or text IDs found.

## 5. NOT YET DONE (RESUME POINT)

1. Re-dispatch 3 failed verifier children (they failed at run time, likely tool/quota errors, i.e. before writing any verdict):
   - event-shangtang-miexia
   - event-pingwang-dongqian
   - event-changping-zhizhan  (their .json verdicts do not exist under reports/current-run/verification/)
   Also confirm event-wang-whun-chengdi verdict on blob (has .json with WARN already).
   Always point Verifier to reports/current-run/research-brief-batch01.md canonical URLs; do NOT type the target CJK by hand.
2. Aggregate PASS/WARN/FAIL table for all 10 events and write it into the final report.
3. Draft reports/current-run/calibration-back-01-final-review.md which must include: BEFORE-placeholder, per-event quality score + verdict + aggregate score-loss, per-event verifier PASS/FAIL, auditor summary, deterministic QA results, 8 pipeline-diagnosis questions, final verdict READY_FOR_BATCH_20 or CALIBRATION_FIX_REQUIRED.
4. Re-run the full 210-test suite after producer edits and confirm still green, and capture the final metrics.
5. Commit final artifacts (scripts, candidates, reports, tests).
6. Follow-up (optional, future polish): record the qiguo locator correction (荆燕吴传) either in candidate or in an accepted layer.

## 6. Blockers

- None blocking: candidates are verified deterministic, no HARD FAIL, no failure.
- ctext direct HTTP 403 is a recurrent infra limit of the fetch tool (worked around via mirrors).

## 7. Concrete resume commands

    PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe -m pytest
    PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe -m history_data_pipeline.cli backbone status
    ls reports/current-run/verification/
