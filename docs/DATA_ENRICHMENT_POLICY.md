# Data Enrichment Policy

> Status: **bootstrap v1** — operational policy for the autonomous enrichment
> framework introduced with `history-data backbone qa-run`.
> This policy **extends** the existing repository contract (AGENTS.md, `ARCHITECTURE.md`,
> `DATA_MODEL.md`, `CONTRIBUTING_DATA.md`) and the existing Backbone lifecycle.
> It does **not** create a parallel data architecture.

## 1. Purpose and scope

This document governs **how candidate historical records move toward the canonical
Backbone**. The canonical Backbone is `data/curated/history_backbone/` and remains
the **only Source of Truth** (`ARCHITECTURE.md`). Nothing in this policy changes
that layer-ownership rule:

```text
raw → staging → candidate → validate → score → quarantine|accept → review → curated(event/story)
```

Autonomous enrichment produces **candidates and quarantine artifacts only**. Writing
directly into `data/curated/history_backbone/events/` still requires an accepted
review record (`data/reviews/accepted/*.review.json`), exactly as
`CONTRIBUTING_DATA.md` requires today.

## 2. Event-driven, never global

Enrichment is **event-driven** (AGENTS.md §4). The framework never tries to enrich
the entire Knowledge Store. Work starts from a batch of event candidates and only
pulls in the people / places / evidence / historical texts that batch requires.

Priority order (unchanged):

1. Critical Events
2. Major Events
3. Important Persons linked to those events
4. Important Places linked to those events
5. Evidence and historical texts
6. Event relations
7. Stories

## 3. The autonomous lifecycle

Default workflow per batch / run (identical in spirit to AGENTS.md §1):

```text
load backbone + candidates
→ deterministic validation (schema / FK / temporal / provenance)
→ independent verifier signal (existing review artifacts, quality_status)
→ 100-point quality score  (backbone/quality.py)
→ quality gate thresholds   (docs/QUALITY_GATES.md)
→ accept / quarantine
→ sampled audit (audit-report.md)
→ batch metrics + summary (reports/current-run/*)
→ human review of the SYSTEM at the end of the batch
```

Human review is reserved for sources, evidence traceability, uncertainty marking,
quarantine policy and sampled-audit findings — never for every individual fact.

## 4. Roles (unchanged principle)

Producer and verifier must be different agents; the same agent never both produces a
record and self-approves it. The bootstrap persisted this in both `quality.py`
(`independent_verifier` dimension) and `enrichment.py` (audit sampling never reuses
the producer's own verdict as the acceptance evidence).

## 5. The candidate intake format

`BACKEND qa-run --candidate-dir <dir>` reads candidate YAML that **already follows the
existing event shape** (the documented Event YAML in `CONTRIBUTING_DATA.md` and the
`schemas/event.schema.json` layout). A file may be:

* a bare event document (`id: event-...` at top level), or
* a list container `candidates:` / `events:` holding event-shaped documents.

Candidate lifecycle is preserved:

```text
candidate → data/reviews/accepted/<event_id>.review.json → curated events/
```

The enrichment run never writes into `data/curated/history_backbone/events/`
directly.

## 6. Quarantine as a successful outcome

Quarantine reasons (subset that the machine can determine deterministically):

* `ambiguous`
* `conflicting_sources`
* `insufficient_evidence`
* `unresolved_person`
* `unresolved_place`
* `uncertain_date`
* `weak_source`
* `duplicate_candidate`
* `evidence_locator_missing`
* `schema_problem`
* `verifier_failure`
* `no_provenance` (accepted/verified record without source provenance)

Quarantined rows are written to `reports/current-run/quarantine.jsonl` and always
preserve: the candidate payload, source hints, evidence, reason, computed score,
attempted resolution and a recommended next action. Useful research is never
deleted.

## 7. Quality status mapping (existing taxonomy)

The framework only uses the existing `quality_status.yml` vocabulary:

* `verified` / `reviewed` / `accepted` — accepted channels
* `candidate` / `needs_review` — machine stage, never promoted directly
* `needs_linking` / `pending_knowledge` — link state (never blocks scoring)
* `rejected` / `pending` / `legacy` / `deprecated` — as documented

`link_status` values `linked` / `needs_linking` / `pending_knowledge` / `rejected`
are used exactly as the schema defines.

## 8. Schema mapping (no duplicate schemas)

The bootstrap question was: do we need new `event_content.schema.json` /
`claim.schema.json`? **No.**

| Requested name | Existing equivalent | Notes |
| --- | --- | --- |
| `event_content.schema.json` | `schemas/event.schema.json` | The full event property model (content, people, places, evidence, relations, dates). Extend in place. |
| `claim.schema.json` | `schemas/event_evidence.schema.json` + `taxonomy/quality_status.yml` | The evidence/claim bridge and the status vocabulary already model claims. Extend in place. |

Any future addition to event content or claims must land inside the existing
schemas, never as parallel files.

## 9. What the bootstrap adds and does not

Adds:

* `backbone/quality.py` — 100-point scoring + verdicts
* `backbone/enrichment.py` — autonomous run/QA/report orchestrator + `qa-run` CLI
* `docs/QUALITY_GATES.md` — gate thresholds and hard failures
* `reports/current-run/` — machine-readable run output structure

Does not:

* enrich hundreds of records
* overwrite canonical datasets
* perform destructive migrations
* invent historical facts
* create duplicate data architectures

The first real autonomous batch is defined in
`reports/current-run/bootstrap-report.md` (proposed first batch + exact next command).
