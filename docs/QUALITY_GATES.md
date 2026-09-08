# Quality Gates

> Status: **bootstrap v1**. This document defines the deterministic gates and the
> 100-point quality model used by the autonomous enrichment framework. It extends —
> and does not replace — the existing gates:
>
> * `history-data backbone validate` → `backbone/validate.py` (structural + FK +
>   schema gate, blocking for `build`).
> * `history-data backbone qa` → `backbone/qa_report.py` (duplicate / granularity /
>   timeline-gap reporting).
> * `history-data backbone build` + `dist/manifest.json` (Layer-4 build gate).

## 1. Gate hierarchy

| Gate | Command | Fails hard on | Scope |
| --- | --- | --- | --- |
| G0 Schema | `backbone validate` (embedded) | invalid schema documents | taxonomy + events + stories |
| G1 Integrity | `backbone validate` | duplicate IDs, orphan FKs, broken references, invalid date ranges, env-invalid enums | curated backbone |
| G2 Temporal | `qa-run` (extended) | event dates vs person lifespans / place windows when known | curated + candidates |
| G3 Provenance | `qa-run` | accepted/verified records without source provenance | curated + candidates |
| G4 Quality score | `qa-run` | 100-point score below thresholds (unless hard-failed first) | candidates |
| G5 Sampling audit | `qa-run --sample` | sampled material-failure rate > 5% → batch REOPEN | accepted |

G1 is executed first and is the same gate that blocks `build`. G2–G5 are added by
this framework and run inside `backbone/enrichment.py`.

## 2. Deterministic validation coverage (G1 + G2 + G3)

Provisions verified deterministically (all already released or added by the
bootstrap):

1. **Schema validity** — `schemas/*.schema.json` via `backbone/schema.py`.
2. **Duplicate IDs** — `_ids_unique` for periods / regimes / events / stories.
3. **Foreign keys** — period/regime/story references exist.
4. **Orphan relations** — relation targets exist, story-event refs exist, no self-ref.
5. **Duplicate relationships** — duplicate `(source, target, relation_type[, confidence])`
   edges flagged (added by bootstrap; canonical set currently has 0).
6. **Invalid event date ranges** — `start_year > end_year` rejected;
   precision-vs-missing-year rejected.
7. **Invalid person lifespans** — `birth_year > death_year` rejected
   (legacy `validation.py` + bootstrap extended rule for curated persons).
8. **event/person temporal consistency** — when a person lifespan is known,
   `birth > event_end+1` or `death < event_start-1` is a conflict (bootstrap-added;
   canonical set currently has 0).
9. **event/place temporal consistency, where possible** — only when a place carries
   `valid_from`/`valid_to` (bootstrap-added; skipped when unknown — never invented).
10. **Missing source references** — accepted/verified events without either
    `source_reference` or `source_ids`.
11. **Broken evidence links** — evidence `linked` without a `historical_text_id`;
    evidence missing `work`/`term`; accepted evidence without source basis.
12. **Accepted records without provenance** — `no_provenance` quarantine.

## 3. The 100-point quality score (G4)

Implemented in `backbone/quality.py`. Dimensions and weights follow AGENTS.md §16
(exactly 100 points):

| Dimension | Weight | What it measures |
| --- | --- | --- |
| Schema / FK / uniqueness | 10 | deterministic structural health |
| Temporal consistency | 10 | valid ranges + no person/place conflicts |
| Person resolution | 10 | share of event people resolved with `linked` + confidence |
| Place resolution | 10 | share of event places resolved |
| Source quality | 15 | tier A/B presence, `source_reference`, `source_ids` |
| Evidence precision | 15 | `work`+`term`+`chapter_hint`, role, reviewed status |
| Independent source verification | 10 | ≥2 distinct/independent reference anchors |
| Content completeness | 10 | summary / background / result / importance present |
| Independent verifier | 10 | separate reviewer signal (quality_status verified/reviewed, review artifact) |

The score is deterministic for a given input; every dimension records why a point was
(when the score is less than the max).

### Thresholds (AGENTS.md §16)

| Score | Verdict |
| --- | --- |
| 90–100 | AUTO_ACCEPT |
| 75–89 | QUARANTINE_MEDIUM |
| 0–74 | QUARANTINE_LOW |
| any score + hard failure | QUARANTINE_HARD (hard failure wins) |

## 4. Hard failures (G4 override, AGENTS.md §17)

A hard failure **cannot be compensated by the score**:

* fabricated source / quotation
* broken evidence pointer / `evidence_locator_missing`
* unresolved identity presented as certain
* impossible chronology (start > end, or person/place temporal conflict)
* unsupported precise location
* missing required provenance
* verifier contradiction
* deterministic integrity failure

Hard failures always produce `quarantine.jsonl` rows with `verdict=QUARANTINE_HARD`.

## 5. Sampling audit (G5)

* Sample size: 3 per 20 accepted, else approx 5–10%; `qa-run --sample N --seed S`
  sets exact size and seed (deterministic for reproducibility).
* Sample rows are written to `reports/current-run/audit-report.md` with
  `status=needs_independent_audit`.
* For each row an independent auditor re-checks: identity resolution, dates, places,
  source independence, evidence linkage, wording-vs-evidence.
* If the sampled **material failure rate > 5%**: mark the batch `REOPEN`, surface
  the recurring error pattern, and quarantine affected records.

## 6. Outputs of a qa-run

Each run (canonical QA or candidate batch) writes:

| File | Content |
| --- | --- |
| `reports/current-run/summary.md` | run overview, verdict counts, score distribution |
| `reports/current-run/quarantine.jsonl` | every non-accepted row with payload/reasons/next steps |
| `reports/current-run/audit-report.md` | sampled audit queue + patterns |
| `reports/current-run/metrics.json` | machine-readable aggregate metrics |

A human reviews the **system** (these reports and the policy), not every record.
