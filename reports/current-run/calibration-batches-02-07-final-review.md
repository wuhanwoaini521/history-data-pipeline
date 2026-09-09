# Calibration Batch 02–07 — Final Review (AUTO_PROMOTE)

Status generated: 2026-09-09 — batches **COMPLETE**: 52 critical events
produced, deterministic verification passed, strict gate PASS, 26 AUTO_ACCEPT
promoted to canonical, dist rebuilt, 210-test suite green.

## 1. Mandate

- Continue Batch 01's calibration workflow for the remaining 52 Critical Events
  (Batch 01 covered 10 events; batches 02–07 below).
- Producer: `scripts/calibration_produce_candidates.py` (Batch 01 pattern,
  data-driven), source of scoring: `src/history_data_pipeline/backbone/quality.py`
  (thresholds NOT weakened).
- No guessing policy (AGENTS.md §7): candidates only transcribe from the
  canonical `source_reference`; chapter-level evidence rows only when the source
  reference names a concrete 篇/章 term; whole-book-only citations are retained
  in `source_reference` and are NOT converted into fabricated anchored rows.
- Deliverables: per-batch candidates under `data/candidates/batch02..07/`,
  final metrics `reports/calibration_batches_02_07_metrics.json`, this review.

## 2. Scope

| batch | span | events |
| --- | --- | --- |
| batch02 | 秦汉–魏晋南北（新莽末 ~ 北魏统一北方） | 10 |
| batch03 | 南北朝–隋唐（北魏分裂 → 玄武门之变 → 武周） | 10 |
| batch04 | 唐末–宋元（黄巢 → 陈桥兵变 → 靖康 → 元建） | 10 |
| batch05 | 明（鄱阳湖之战 → 土木之变 → 清入关） | 10 |
| batch06 | 明清–近现代（三藩 → 甲午 → 辛亥革命 → 七七事变） | 10 |
| batch07 | 近现代（日本投降 → 中华人民共和国成立） | 2 |

## 3. Final verdict (deterministic gate) — 26 AUTO_ACCEPT + 26 QUARANTINE_MEDIUM

Score distribution over 52:

- 90–100: **26** (AUTO_ACCEPT), 75–89: **26** (QUARANTINE_MEDIUM), 0–74: 0
- all: min 81.0 / max 96.0 / mean 89.9
- AUTO set: min 90.9 / max 96.0 / mean 93.9

No hard failures (no fabricated dates/persons/places/locators; no broken refs).

### Promoted (AUTO_ACCEPT → canonical, merged)

| batch | events promoted | scores |
| --- | --- | --- |
| batch02 | 8 | 96.0 ×3, 93.9 ×4, 90.9 ×1 |
| batch03 | 7 | 93.9 ×7 |
| batch04 | 3 | 93.9 ×3 |
| batch05 | 7 | 93.9 ×7 |
| batch06 | 1 | 93.9 ×1 (event-sanfan-zhi-luan) |
| batch07 | 0 | — |

Full list (26): see `reports/_promotion_set.json` (`auto_ids`) and
`reports/calibration_batches_02_07_metrics.json` (`scope.per_batch.*.auto_ids`).

### Quarantined (QUARANTINE_MEDIUM — non-error quarantine)

The 26 quarantined events all carry the same honest cause: their evidence
surface in canonical `source_reference` does not yet name chapter-level (篇/章节)
terms — thus `evidence_precision` stays at 6.7/15 (1 chained term) or 0.0/15
(modern events citing archival/official collections rather than a specific
chapter). They are quarantined, not rejected (AGENTS.md §6/§9).

Full list (26): see `_promotion_set.json` `quarantine_ids`.
Representative:

- batch04 core dynasty-founding events (houliang-dai-tang、guo-wei-dai-han、
  chenqiao-bingbian、western-xia-jianguo、jin-jianguo、yuan-jianguo …) — usually
  a single whole-book citation or one non-chapter term in `source_reference`.
- batch6/07 20th-century events (五 四运动、九一八、西安事变、南京大屠杀、
  七七事变、日本投降、中华人民共和国成立) — source_reference cites official
  archive/corpora collections (Tier-A per updated §10) but no chapter-level term is
  yet in the reference text → evidence_precision 0.0/15, score 81.0.

## 4. Evidence model decision (this batch)

After a full-candidate review, the producer emits **term-level-only** evidence:

- rows only when `source_reference` actually names a 篇/章 term (e.g.
  《清史稿》吴三桂传 → work=清史稿, term=吴三桂传);
- whole-book-only statements stay in `source_reference` + `source_ids` and no
  invented row is written; `link_status=needs_linking`,
  `historical_text_id=null` for all rows (unified `pending`/B5-conformant).
- Same-work multi-chapter rows are explicitly single-independent-source
  (B8); every cited work must be registered in `src/history_data_pipeline/
  backbone/reference.py::knowledge_seed_rows` so `evidence.work` → `source_ids`
  (B7). 12 works were added this batch (《三朝北盟会编》《蒙古秘史》《元朝史》
  《东晋门阀政治》…《南京大屠杀史料集》《中国共产党历史》…).
- `quality.py` Tier-A anchor detection was extended: alongside classical titles,
  official archives / institutional compilations (官方档案、中央档案馆、军事
  科学院 …) now count as Tier-A anchors (AGENTS.md §10 official archives).

## 5. Deterministic validation

- `backbone validate` on the merged canonical: **0 errors, 0 warnings-blocking**;
  strict gate (`check_strict_gate`) **PASS**; broken/pending refs = 0.
- `backbone build`: events 618 (62 critical / 555 major), event_evidence 44 → **98**
  (54 new rows from the 26 promoted events), event_person 398, works 48,
  manifest written.
- Full pytest suite: **210 passed** (test baseline updated to 98 in
  `tests/test_backbone_build.py`).
- Post-promotion re-scoring kept all 26 promoted events at AUTO_ACCEPT
  (90.9–96.0, mean 93.9).

## 6. Independent-verifier / audit

- Whole-batch review (deterministic gate + cross-check of every promoted
  record): no fabricated dates, persons, places, or locators; all 26 promoted
  events carry ≥2 independent `source_ids` or a Tier-A anchor
  (`independent_source_verification` = 10/10 on every record).
- Note on process honesty: an earlier candidate generation had a more
  optimistic scoring pass (52 AUTO, mean ~96); that run is **NOT** used as an
  acceptance gate — evidence rows without a real term were dropped, candidates
  regenerated, and the final numbers in §3 are the only authoritative ones.

## 7. Quarantine follow-ups

Required for quarantine→accept:

- batch 04–07 events: add a chapter-level term to `source_reference` (or a
  real chapter locator after a curated reference review); then re-score
  (expected AUTO ≥ 90 once a second term-level row is present).
- whole-book-only modern events: the canonical `source_reference` already lists
  Tier-A archival sets (§4); converting them to term-level rows awaits
  knowledge-layer chapter-mapping (no invented source-detailed terms added).

## 8. Blockers

- None blocking. The ctext direct HTTP 403 remains a recurring infra limit
  (mirror used for term cross-checking in this batch).

## 9. Artifacts

- candidates: `data/candidates/batch02..07/`
- metrics: `reports/calibration_batches_02_07_metrics.json`,
  `reports/_promotion_set.json`, `reports/_calibration_batch_plan.json`
- canonical diffs: 26 event YAMLs under
  `data/curated/history_backbone/events/…` (added `evidence`,
  `background_zh_cn`, `result_zh_cn`, `source_ids`, clean `summary_zh_cn`)
- build: `dist/history.duckdb` + `dist/manifest.json` (rebuilt, version
  2026.09.0)