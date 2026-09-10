# Calibration Batch 02–07 — Final Review (AUTO_PROMOTE + Rescue)

Status generated: 2026-09-10 — batches **COMPLETE** (rescue pass applied):
52 critical events produced, deterministic verification passed, strict gate
PASS, **42 AUTO_ACCEPT** promoted to canonical, 10 QUARANTINE_MEDIUM (honest
residual quarantine), dist rebuilt, test suite green.

## 1. Mandate

- Continue Batch 01's calibration workflow for the remaining 52 Critical Events
  (Batch 01 covered 10 events; batches 02–07 below).
- Producer: `scripts/calibration_produce_candidates.py` (Batch 01 pattern,
  data-driven), source of scoring: `src/history_data_pipeline/backbone/quality.py`
  (thresholds NOT weakened).
- No guessing policy (AGENTS.md §7): evidence rows only transcribe terms named
  in the canonical `source_reference`; chapter-level rows only when the source
  reference names a concrete 篇/章 term; whole-book-only citations stay in
  `source_reference` + `source_ids` and are never converted into fabricated rows.
- **Rescue pass (2026-09-10)**: the 16 QUARANTINE events whose `source_reference`
  clearly documents a second chapter term received a second real evidence row,
  dual-written into `data/candidates/…` and the canonical event YAML. Every new
  row = a registered work (id resolved from `reference.py` at runtime) + a term
  already present in the extended `source_reference`; no invented chapters,
  locators, text ids, or `source_ids`.

## 2. Scope

| batch | span | events |
| --- | --- | --- |
| batch02 | 秦汉–魏晋南北朝（新莽末 ~ 北魏统一北方） | 10 |
| batch03 | 南北朝–隋唐（北魏分裂 → 玄武门之变 → 武周） | 10 |
| batch04 | 唐末–宋元（黄巢 → 陈桥兵变 → 靖康 → 元建） | 10 |
| batch05 | 明（鄱阳湖之战 → 土木之变 → 清入关） | 10 |
| batch06 | 明清–近现代（三藩 → 甲午 → 辛亥革命 → 七七事变） | 10 |
| batch07 | 近现代（日本投降 → 中华人民共和国成立） | 2 |

## 3. Final verdict — 42 AUTO_ACCEPT + 10 QUARANTINE_MEDIUM

Score distribution over 52:

- 90–100: **42** (AUTO_ACCEPT), 75–89: **10** (QUARANTINE_MEDIUM), 0–74: 0
- all: min 81.0 / max 96.0 / mean 91.8
- AUTO set: min 90.9 / max 96.0 / mean 93.9
- quarantine set: min 81.0 / max 87.7 / mean 83.0

No hard failures (no fabricated dates/persons/places/locators; no broken refs).

### Promoted (AUTO_ACCEPT → canonical)

| batch | promoted | scores |
| --- | --- | --- |
| batch02 | 10 | 96.0×2, 93.9×7, 90.9×1 |
| batch03 | 10 | 93.9×10 |
| batch04 | 7 | 93.9×7 |
| batch05 | 10 | 93.9×10 |
| batch06 | 5 | 93.9×5 |
| batch07 | 0 | — |

Full list (42): `reports/_promotion_set.json` (`auto_ids`) and
`reports/calibration_batches_02_07_metrics.json`
(`scope.per_batch.*.auto_ids`).

### Rescue rows added (second supporting row, real registered works)

| event | batch | new row |
| --- | --- | --- |
| event-guangwu-chengdi | 02 | 资治通鉴·汉纪 |
| event-dongjin-jianguo | 02 | 资治通鉴·晋纪 |
| event-tang-jianguo | 03 | 资治通鉴·唐纪·武德元年 |
| event-wu-zhou-jianguo | 03 | 资治通鉴·唐纪·天授元年 |
| event-shenlong-zhengbian | 03 | 资治通鉴·唐纪·神龙元年 |
| event-houliang-dai-tang | 04 | 资治通鉴·后梁纪 |
| event-guo-wei-dai-han | 04 | 资治通鉴·后周纪 |
| event-chenqiao-bingbian | 04 | 续资治通鉴长编·建隆元年 |
| event-jin-jianguo | 04 | 辽史·天祚帝纪 |
| event-zhuyuanzhang-chendi | 05 | 明实录·太祖实录 |
| event-tumu-bao-zhibian | 05 | 明实录·英宗实录 |
| event-lizicheng-gong-beijing | 05 | 明史·李自成传 |
| event-diyici-yapian-zhanzheng | 06 | 筹办夷务始末·道光朝 |
| event-jiawu-zhanzheng | 06 | 清史稿·德宗本纪 |
| event-wuchang-qiyi | 06 | 辛亥革命回忆录·武昌起义 |
| event-qingdi-tuiwei | 06 | 清史稿·宣统本纪 |

### Quarantined (10 — QUARANTINE_MEDIUM, residual)

These 10 have no second chapter-level term in `source_reference` (single
whole-book or archival-collection citations only), so `evidence_precision`
stays at 6.7/15 (1 row) or 0/15 (0 rows):

- batch04: event-western-xia-jianguo, event-mongol-jianguo, event-yuan-jianguo — 87.7（1 证据行）
- batch06: event-wusi-yundong, event-jiuyiba-shibian, event-xian-shibian, event-nanjing-datusha, event-qiqishi-bian — 81.0（无行级）
- batch07: event-riben-touxiang, event-xinzhongguo-chengli — 81.0（无行级）

They are quarantined, not rejected (AGENTS.md §6/§9); candidates with sources
are preserved under `data/candidates/…`.

## 4. Evidence model decision

- Rows only when `source_reference` names a 篇/章 term; whole-book-only keeps
  `source_reference` + `source_ids` without an invented row.
- `link_status=needs_linking`, `historical_text_id=null` on all rows
  (B5-conformant); every work is registered in
  `reference.py::knowledge_seed_rows` — the rescue added **zero** new work ids,
  all cited 塔 are already-registered titles.
- Build-level `works` 48 → **49**: `event_evidence` rows now also anchor
  《筹办夷务始末》 (registered as `work-curated-chaoban-yiwu-shimo`), a
  previously-registered work that had no anchored row yet.

## 5. Deterministic validation

- `backbone validate`: **0 errors**; strict gate (`check_strict_gate`) PASS;
  broken / pending references = 0.
- `backbone build`: events 618 (62 critical / 555 major); `event_evidence`
  98 → **130** (16 rescued events × 2 rows = +32); `event_person` 398;
  `works` 49; manifest written (version 2026.09.0).
- Full pytest suite green (baseline updated to 130 in
  `tests/test_backbone_build.py`).
- Post-rescue re-scoring (deterministic `score_event` on all 52):
  42 AUTO_ACCEPT (all ≥ 90.9), 10 QUARANTINE_MEDIUM; every promoted event has
  ≥2 distinct `source_ids` or a Tier-A anchor in `source_reference`
  (`independent_source_verification` = 10/10).

## 6. Independent-verifier / audit

- Whole-batch review (deterministic gate + cross-check of every promoted
  record + line-by-line comparison of the 16 rescue rows): no fabricated
  dates / titles / places / evidence; both sides (candidate + canonical) of
  each rescued event re-parsed and verified to carry identical
  `source_reference` / `source_ids` / evidence rows; the write is
  fail-closed — nothing was partially written.
- Process honesty (kept from the previous run): the earlier optimistic pass
  (52 AUTO, mean ~96) is NOT an acceptance gate — evidence rows without a
  real term were dropped, candidates regenerated, and the numbers in §3 are
  the only authoritative ones.

## 7. Residual-quarantine follow-ups

Every residual event was re-audited line by line (deterministic, per-event
reasons, registered-cited-book list, and the exact blocking step) in
[`calibration-10-residual-quarantine-audit.md`](calibration-10-residual-quarantine-audit.md).

- 3 dynasty-founding events (batch04: 西夏/蒙古/元): add a real chapter term
  after a curated text check / knowledge-layer chapter-map (87.7 → 93.9).
- 7 × 20th-century archival-collection citations (五四 / 九一八 / 西安 /
  南京 / 七七 / 日本投降 / 中华人民共和国): converting to term-level rows
  awaits the knowledge-layer chapter mapping (no fabricated terms added).

## 8. Blockers

- None blocking. The ctext direct HTTP 403 remains an infra limit (mirror
  used for term cross-checking in this batch).

## 9. Artifacts

- candidates: `data/candidates/batch02..07/` (16 edited: 1 → 2 evidence rows)
- metrics: `reports/calibration_batches_02_07_metrics.json`,
  `reports/_promotion_set.json`, `reports/_calibration_batch_plan.json`
- residual quarantine audit (per-event, deterministic):
  `reports/current-run/calibration-10-residual-quarantine-audit.md`
- canonical diffs: 42 event YAMLs (evidence/background/result/source_ids;
  clean summary), incl. 16 rescue edits
- rescue/re-score tooling: `scripts/_tmp_rescue16.py` +
  `scripts/_tmp_rescore16.py` (temporary; removed from the final commit)
- build: `dist/history.duckdb` + `dist/manifest.json` (rebuilt, 2026.09.0)