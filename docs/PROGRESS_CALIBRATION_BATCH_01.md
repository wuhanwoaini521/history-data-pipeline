# Calibration Batch 01 - Work in Progress / Resume Document (COMPLETE + FIXED)

Status generated: 2026-09-08T16:55:21 — batch finalized 2026-09-09; fix batch
executed 2026-09-09 (CALIBRATION_PASS).

This document records what was done and how the run was resumed. The batch is
now **COMPLETE + FIXED**: all 10 events re-verified post-fix, fix list §9
(A1–A4, B5–B8) closed, final review report updated, 210-test suite green,
metrics regenerated, artifacts committed.

## 1. Mandate

- Run 10 chosen Critical Events through the autonomous enrichment pipeline.
- Scoring engine: src/history_data_pipeline/backbone/quality.py is authoritative; thresholds were NOT weakened.
- Candidates must never fabricate history/locators/IDs; uncertainty is preserved via claim_type and needs_linking.
- Final deliverable: reports/current-run/calibration-batch-01-final-review.md (WRITTEN 2026-09-09).

## 2. What is DONE (unchanged)

- Repo audit; 10 Critical Events selected; baseline captured (reports/calibration_batch01_baseline.*).
- Researcher phase: research brief written -> reports/current-run/research-brief-batch01.md.
- Producer script: scripts/calibration_batch01_produce_candidates.py (v4 post-fix) -> 10 candidate YAMLs under data/candidates/calibration_batch01/.
- Deterministic QA: qa-run produced 9 accepted / 1 quarantined (event-pingwang-dongqian, 85.7, expected from A4 place fix); validation.error_count=0.
- Per-event quality & gates (final recomputation on 2026-09-09 after fix batch):
  min 85.7 / max 94.4 / avg 92.9; 9x AUTO_ACCEPT + 1x QUARANTINE_MEDIUM (desired).
- 210-test suite passed (re-verified green on 2026-09-09 after fix batch).
- audit-report.md + summary.md + metrics.json emitted to reports/current-run/.

## 2b. Fix List (2026-09-09), see final report §9

- A1 七国之乱 吴王濞传->荆燕吴传 (Han Shu vol 35): canonical + candidate corrected, byte-scan 0 remnants.
- A2 Changping casualties 40万 vs 45万 recorded as DISPUTED (canonical + candidate).
- A3 Wang Mang accession year 8 vs 9 AD recorded as DISPUTED; canonical value 9 retained.
- A4 Ping Wang Dong Qian place: fabricated 710-959 window removed -> place_id=null + needs_linking (AGENTS.md §12); deterministic score honestly drops to 85.7 (QUARANTINE_MEDIUM, non-error quarantine).
- B5 evidence rows all carry explicit historical_text_id: null; empty regime_ids preserved (10/10).
- B6 person linked requires anchor-set membership, else downgraded to needs_linking (10/10 verified).
- B7 every evidence work (史记/汉书/资治通鉴/左传/战国策/尚书) has its registered work id in source_ids (10/10).
- B8 same-work multi-chapter evidence explicitly noted as a single independent source (长平, 七国之乱).

## 3. Independent Verification (COMPLETED — 2 rounds, all 10 refreshed post-fix)

Round 1 (pre-fix): 7 of 10 artifacts existed at pause; 3 had failed at run time
(tool/quota errors) and were re-dispatched 2026-09-09; first-round verdicts
were 2 PASS / 8 WARN.

Round 2 (post-fix, 2026-09-09): all 10 verifier JSONs refreshed against the
regenerated candidates — 5 affected events fully re-audited (qiguo, changping,
wangmang, pingwang, plus mobei as control) and 5 unaffected events
template-consistency re-checked (B5/B6/B7/B8). Every verdict file now reflects
the current candidate state.

Per-event verdict (final, round 2):

| event id | Chinese name | canonical name matches | verifier verdict |
| --- | --- | --- | --- |
| event-shangtang-miexia | 商汤灭夏 | Y | PASS |
| event-wuwang-fazhou | 武王伐纣 | Y | PASS |
| event-pingwang-dongqian | 平王东迁 | Y | PASS |
| event-sanjia-fenjin | 三家分晋 | Y | PASS |
| event-changping-zhizhan | 长平之战 | Y | PASS |
| event-qin-mie-liuguo | 秦灭六国 | Y | WARN |
| event-qin-tongyi | 秦统一六国（秦帝国建立） | Y | WARN |
| event-qiguo-zhi-luan | 七国之乱 | Y | PASS |
| event-mobei-zhizhan | 漠北之战 | Y | WARN |
| event-wangmang-chengdi | 王莽称帝、新朝建立 | Y | PASS |

Summary: 7 PASS (shangtang, wuwang, pingwang, sanjia, changping, qiguo,
wangmang); 3 WARN (qin-mie-liuguo & qin-tongyi chapter_hint: null on the 通鉴
row — schema-legal template consistency; mobei-zhizhan is the unchanged control
with a casualty-evidence-row note); 0 FAIL; 0 HARD FAIL (no fabrication, no
corruption, no broken locators). Auditor overall: PASS.

Key fix verifications (round 2):
- event-qiguo-zhi-luan: glyph fixed to 荆燕吴传 in candidate + canonical,
  byte-scan 0 remnants of 吴王濞传.
- event-changping-zhizhan: casualty 40万 vs 45万 DISPUTED statement verbatim.
- event-wangmang-chengdi: accession 8 vs 9 AD DISPUTED statement verbatim;
  start_year=9 retained.
- event-pingwang-dongqian: place window 710-959 removed; place_id=null +
  needs_linking; no coordinates / valid_from / valid_to keys.
- All evidence rows carry explicit historical_text_id: null; regime_ids
  preserved identical to canonical (B5).
- Every classical work cited in evidence has its registered work id in
  source_ids, incl. 资治通鉴 -> work-curated-zizhitongjian (B7).

## 4. Auditor (completed - PASS overall, refreshed post-fix)

Audit sample (seeded, post-fix 2026-09-09): event-yangjian-zhuanquan,
event-three-regime-formation, event-zhangyi-po-chu (the deterministic seed=1
queue shifted to canonical events once the candidate pool shrank 10→9; the
refreshed auditor.json matches the current audit-report.md).
Auditor overall: PASS. Per-record verdicts 3/3 PASS — no fabrication; two
recurring, non-blocking paths recorded (claim-level evidence blocks thin in 2/3
records; source_ids sometimes omit works named in source_reference).
No fabricated dates, names, locators, person ids, or coordinates found.

## 5. NOT YET DONE (RESUME POINT) — all closed 2026-09-09

1. DONE: verifier round 2 (all 10 refreshed, 7 PASS / 3 WARN) — see §3.
2. DONE: Aggregate PASS/WARN/FAIL matrix for all 10 events written into the final report (§4).
3. DONE: reports/current-run/calibration-batch-01-final-review.md updated with BEFORE,
   per-event quality score + verdict, auditor summary, deterministic QA results,
   8 pipeline-diagnosis questions, final verdict **CALIBRATION_PASS** (fix list §9 all ✔).
4. DONE: full 210-test suite re-run after producer edits (green on 2026-09-09),
   final metrics regenerated (qa-run seed=1, 1 quarantine = expected).
5. DONE: fix batch artifacts committed + pushed.
6. DONE: qiguo locator correction (荆燕吴传) applied in canonical + candidate (A1);
   changwang/wangmang (A2/A3) DISPUTED statements written into canonical + candidate;
   pingwang (A4) place window defabricated (place_id=null + needs_linking).

## 6. Blockers

- None blocking. ctext direct HTTP 403 remains a recurrent infra limit (mirrors used).
- No hard failures, no runaway quarantine, no schema/policy conflict.

## 7. Concrete resume commands

    PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe -m history_data_pipeline.cli backbone status
    .venv\Scripts\python.exe -m pytest
    dir reports\current-run\verification

## 8. Next actions (owner decides)

- Fix List A1-A4 + B5-B8 executed and verified (final report §9 all ✔); batch
  verdict now **CALIBRATION_PASS**.
- Before Batch 2: optionally add chapter_hint: 秦纪 to the 资治通鉴 rows of
  qin-mie-liuguo / qin-tongyi (template polish; schema-legal as-is) and add the
  匈奴列传/匈奴传 evidence row to event-mobei-zhizhan.
- Promotion decision (owner)：9 AUTO_ACCEPT candidates may be promoted to
  canonical; event-pingwang-dongqian awaits a properly-windowed Zhou-era place
  entity before re-scoring.