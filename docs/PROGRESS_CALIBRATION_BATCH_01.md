# Calibration Batch 01 - Work in Progress / Resume Document (COMPLETE)

Status generated: 2026-09-08T16:55:21 — batch finalized 2026-09-09

This document records what was done and how the run was resumed. The batch is
now **COMPLETE**: all 10 events verified, final review report written, fix list
issued, metrics regenerated, artifacts committed.

## 1. Mandate

- Run 10 chosen Critical Events through the autonomous enrichment pipeline.
- Scoring engine: src/history_data_pipeline/backbone/quality.py is authoritative; thresholds were NOT weakened.
- Candidates must never fabricate history/locators/IDs; uncertainty is preserved via claim_type and needs_linking.
- Final deliverable: reports/current-run/calibration-batch-01-final-review.md (WRITTEN 2026-09-09).

## 2. What is DONE (unchanged)

- Repo audit; 10 Critical Events selected; baseline captured (reports/calibration_batch01_baseline.*).
- Researcher phase: research brief written -> reports/current-run/research-brief-batch01.md.
- Producer script: scripts/calibration_batch01_produce_candidates.py -> 10 candidate YAMLs under data/candidates/calibration_batch01/.
- Deterministic QA: qa-run produced 10 accepted / 0 quarantined; validation.error_count=0.
- Per-event quality & gates: 10 accepted (AUTO_ACCEPT range; final recomputation on 2026-09-09:
  min 92.7 / max 95.7 / avg 93.9).
- 210-test suite passed (two earlier batched runs; re-verified green on finalization).
- audit-report.md + summary.md + metrics.json emitted to reports/current-run/.

## 3. Independent Verification (COMPLETED — 1 round, all 10 children restored)

Verifier round: 7 of 10 artifacts existed at pause; 3 children had failed at run
time (tool/quota errors before writing verdicts) and were RE-DISPATCHED
2026-09-09: event-shangtang-miexia, event-pingwang-dongqian,
event-changping-zhizhan. All 10 verifier JSONs + auditor.json now exist under
reports/current-run/verification/.

Per-event verdict (final):

| event id | Chinese name | canonical name matches | verifier verdict |
| --- | --- | --- | --- |
| event-shangtang-miexia | 商汤灭夏 | Y | WARN |
| event-wuwang-fazhou | 武王伐纣 | Y | PASS |
| event-pingwang-dongqian | 平王东迁 | Y | WARN |
| event-sanjia-fenjin | 三家分晋 | Y | WARN |
| event-changping-zhizhan | 长平之战 | Y | WARN |
| event-qin-mie-liuguo | 秦灭六国 | Y | PASS |
| event-qin-tongyi | 秦统一六国（秦帝国建立） | Y | WARN |
| event-qiguo-zhi-luan | 七国之乱 | Y | WARN |
| event-mobei-zhizhan | 漠北之战 | Y | WARN |
| event-wangmang-chengdi | 王莽称帝、新朝建立 | Y | WARN |

Summary: 2 PASS (wuwang-fazhou, qin-mie-liuguo); 8 WARN; 0 FAIL; 0 HARD FAIL
(no fabrication, no corruption, no broken locators). Auditor overall: PASS.

Key findings preserved in the final report (§6):
- event-qiguo-zhi-luan: glyph WARN — locator 吴王濞传 should be 荆燕吴传 (Han Shu vol 35);
  the same locator string is in the canonical source_reference (carried from narrative, not fabricated).
- event-changping-zhizhan: casualty figure 40万 vs 45万 not surfaced as DISPUTED.
- event-wangmang-chengdi: accession year 8-vs-9 CE not captured as DISPUTED (canonical records 9).
- event-pingwang-dongqian: place id cbdb-place-14693 validity window (710-959) does not span -770.
- event-sanjia-fenjin / event-qin-tongyi: person ids declared linked@1.0 without independent confirmation (ctext 403).
- event-mobei-zhizhan: precise casualty tally derives from Xiongnu Liezhuan/Xiongnu Zhuan, not in evidence list.
- ctext.org HTTP 403 remains an infra limit; glyphs confirmed via authoritative mirrors.

## 4. Auditor (completed - PASS overall)

Audit sample (seeded): event-qin-mie-liuguo, event-sanjia-fenjin, event-wangmang-chengdi.
Auditor overall: PASS. Recurring patterns tracked (non-blocking):
- Uniform evidence link_confidence=0.9 + needs_linking (acceptable but monotonous).
- 资治通鉴 in evidence but not source_ids (deferred by needs_linking).
No fabricated dates, names, locators, or text IDs found.

## 5. NOT YET DONE (RESUME POINT) — all closed 2026-09-09

1. DONE: 3 failed verifier children re-dispatched; verdicts written (see §3).
2. DONE: Aggregate PASS/WARN/FAIL matrix for all 10 events written into the final report (§4).
3. DONE: reports/current-run/calibration-batch-01-final-review.md drafted with BEFORE,
   per-event quality score + verdict + aggregate score-loss, per-event PASS/FAIL,
   auditor summary, deterministic QA results, 8 pipeline-diagnosis questions,
   final verdict CALIBRATION_FIX_REQUIRED (+ fix list §9).
4. DONE: full 210-test suite re-run after producer edits (no producer edits needed;
   suite green), final metrics regenerated (qa-run seed=1).
5. DONE: final artifacts committed.
6. OPTIONAL (pending owner): qiguo locator correction (荆燕吴传) — now tracked in the
   fix list (A1); apply in the fix batch.

## 6. Blockers

- None blocking. ctext direct HTTP 403 remains a recurrent infra limit (mirrors used).
- No hard failures, no runaway quarantine, no schema/policy conflict.

## 7. Concrete resume commands

    PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe -m history_data_pipeline.cli backbone status
    .venv\Scripts\python.exe -m pytest
    dir reports\current-run\verification

## 8. Next actions (owner decides)

- Apply Fix List A1-A4 + B5-B8 (final report §9) in a small fix batch, rerun QA +
  verification of touched events, then proceed to Batch 20 (or as directed).
- Track qiguo locator fix in canonical narrative layer before promotion.