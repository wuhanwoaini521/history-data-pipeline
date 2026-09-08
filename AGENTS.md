# AGENTS.md

## Project Mission

This repository builds a trustworthy, structured, evidence-backed historical knowledge dataset for the History module.

The primary goal is NOT to maximize record count.

The primary goals are:

1. historical entity completeness
2. evidence traceability
3. source quality
4. cross-source consistency
5. uncertainty preservation
6. product usefulness
7. deterministic validation
8. reproducibility

Never optimize for dataset size at the expense of trustworthiness.

---

# 1. Core Operating Principle

The pipeline must operate autonomously.

The default workflow is:

Research
→ Resolve
→ Produce Candidate
→ Deterministic Validation
→ Independent Verification
→ Quality Gate
→ Accept or Quarantine
→ Sample Audit
→ Final Report

Human review happens at the END of a batch.

Do NOT stop the pipeline to request human review for individual historical records.

---

# 2. Human Review Policy

The repository owner is not expected to manually verify every historical fact.

Therefore:

DO NOT require the human to decide whether every event, person, place, date, or historical claim is correct.

Human review should focus on:

* whether sources are trustworthy
* whether evidence is traceable
* whether uncertain claims are correctly marked
* whether validation rules passed
* whether sampled audits reveal systemic issues
* whether quarantined records require policy decisions

Do not ask the user questions during normal data enrichment.

Only stop for human input when:

1. a destructive repository-wide operation is required
2. a schema migration would destroy or irreversibly reinterpret existing data
3. two project-level policies conflict
4. credentials or external access are unavailable
5. continuing would risk corrupting the canonical dataset

Individual ambiguous historical facts are NOT blockers.

---

# 3. Batch Processing Rule

Never process the entire historical dataset as one uncontrolled operation.

Use batches.

Recommended starting batch size:

* Critical events: 10–20 events
* Major events: 20–50 events
* People/place enrichment: 25–100 entities depending on complexity

After each batch:

1. run deterministic validation
2. score quality
3. run independent verification
4. perform sampled audit
5. generate batch metrics
6. continue automatically if gates pass

Do not request human approval between normal batches.

---

# 4. Event-Driven Enrichment

Historical enrichment must be event-driven.

Do NOT attempt to clean or enrich every person, place, text, or source in the global knowledge store.

Instead:

Event
→ required people
→ required places
→ required claims
→ required evidence
→ supporting historical texts

Only enrich entities necessary to make important events product-ready.

Priority order:

1. Critical Events
2. Major Events
3. Important Persons linked to those events
4. Important Places linked to those events
5. Evidence and historical texts
6. Event relations
7. Stories

Do not expand the number of events unless explicitly required.

---

# 5. Agent Roles

When pi-subagents is available, separate responsibilities.

The same agent must NOT both produce a historical record and be its only verifier.

Use the following logical roles.

## Researcher

Responsibilities:

* gather reliable sources
* locate primary sources when possible
* locate authoritative secondary sources
* identify conflicting accounts
* record source provenance
* avoid unsupported synthesis

Researcher must not directly approve production records.

---

## Resolver

Responsibilities:

* person identity resolution
* historical place resolution
* aliases
* alternate names
* temporal matching
* entity deduplication
* ambiguity detection

Resolver must prefer unresolved ambiguity over incorrect merging.

---

## Producer

Responsibilities:

* create candidate structured records
* convert research into repository schema
* create claims
* attach evidence
* classify uncertainty
* preserve provenance

Producer must not self-approve its own output.

---

## Verifier

Verifier must behave as an independent reviewer.

Instructions:

* do not assume Producer is correct
* independently inspect important claims
* actively search for contradictions
* verify dates
* verify identities
* verify places
* verify source independence
* verify evidence linkage
* check whether wording overstates evidence

Verifier output:

PASS
WARN
FAIL

Every WARN or FAIL must include a reason.

---

## Auditor

Auditor reviews a random sample of already accepted records.

Auditor must:

* independently verify sampled records
* evaluate whether Producer and Verifier systematically miss problems
* report recurring error patterns
* recommend reopening a batch if necessary

Auditor must not simply repeat existing verification results.

---

# 6. Historical Claim Model

Historical statements must be classified.

Allowed types:

FACT
INTERPRETATION
DISPUTED

## FACT

A factual claim should normally require:

* at least two reliable independent sources

OR

* one strong primary source plus one authoritative secondary source

Examples:

* dynasty establishment dates
* office appointments
* documented battles
* treaty dates

---

## INTERPRETATION

Interpretive claims must not be presented as undisputed fact.

Examples:

* "The An Lushan Rebellion marked the transition from Tang prosperity to decline."
* "This reform significantly strengthened central authority."

Interpretive claims must:

* use `claim_type = interpretation`
* include supporting scholarly or authoritative secondary sources
* avoid false certainty

---

## DISPUTED

When credible sources disagree:

DO NOT select one position simply because it appears more frequently.

Preserve disagreement.

Store:

* competing views
* supporting sources
* confidence
* unresolved status

Examples:

* troop counts
* disputed birth years
* disputed battle locations
* disputed causes
* disputed historical identities

---

# 7. No Guessing Policy

Never invent missing historical data.

Never infer precise values from weak evidence.

Forbidden behavior:

* inventing coordinates
* inventing dates
* silently resolving ambiguous identities
* turning interpretation into fact
* inventing quotations
* inventing source references
* inventing chapter locations
* filling unknown fields merely to satisfy schema completeness

If reliable resolution is impossible:

status = quarantine

and record the reason.

Then continue processing.

---

# 8. Quarantine Policy

Quarantine is a valid successful pipeline outcome.

Possible reasons include:

* ambiguous
* conflicting_sources
* insufficient_evidence
* unresolved_person
* unresolved_place
* uncertain_date
* weak_source
* duplicate_candidate
* evidence_locator_missing
* schema_problem
* verifier_failure

A quarantined record must preserve:

* candidate data
* sources
* evidence collected
* reason
* confidence
* attempted resolution
* recommended next action

Do not delete useful research simply because a record cannot be accepted.

---

# 9. Source Independence

Source count and independent source count are different metrics.

Example:

* Baidu Baike
* an article copying Baidu Baike
* another website copying the same text

must NOT be counted as three independent sources.

Prefer diversity such as:

Primary historical source
+
academic / institutional source
+
authoritative modern reference

When possible.

---

# 10. Source Priority

Preferred source hierarchy:

## Tier A

* primary historical texts
* official archives
* national or major institutional databases
* academic publications
* university resources
* museum / library resources
* established scholarly projects

## Tier B

* high-quality encyclopedias
* authoritative reference works
* reputable educational resources
* carefully maintained structured datasets

## Tier C

* Wikipedia / Wikidata
* Baidu Baike
* general reference websites

Tier C may be used for:

* candidate discovery
* alias discovery
* rough cross-checking

Tier C should normally not be the sole evidence for important historical claims.

## Tier D

* blogs
* SEO pages
* unsourced reposts
* anonymous summaries
* AI-generated pages
* content farms

Tier D must not be treated as authoritative evidence.

---

# 11. Event Product Completeness

A Critical Event should ideally contain:

* canonical name
* aliases
* event type
* start/end date
* period/regime
* concise summary
* background
* trigger
* process
* result
* historical impact
* why it matters
* important people
* primary places
* related places
* predecessor events
* successor events
* factual claims
* interpretation claims
* disputed claims when applicable
* evidence
* source provenance

Not every field must always exist.

Missing fields must be preferred over invented content.

---

# 12. Place Resolution

Historical places are temporal entities.

Do not assume an ancient place name maps permanently to one modern coordinate.

Where applicable preserve:

* canonical historical name
* historical aliases
* modern name
* modern administrative area
* latitude
* longitude
* valid_from
* valid_to
* place_type
* resolution confidence
* source

If competing modern mappings exist:

mark as disputed or quarantine.

Never fabricate coordinates.

---

# 13. Person Resolution

A shared name is not sufficient evidence that two people are the same person.

Consider:

* name
* aliases
* birth/death years
* dynasty
* offices
* family relations
* locations
* event participation
* source identifiers

Prefer duplicate unresolved candidates over an incorrect merge.

---

# 14. Evidence Linking

Evidence must support specific claims when possible.

Preferred model:

Event
→ Claim
→ Evidence
→ Historical Text / Source
→ locator

Do not treat:

"This event has a source"

as equivalent to:

"This claim is supported by evidence."

Important claims should have precise evidence linkage whenever practical.

---

# 15. Deterministic Validation

LLM verification must never replace deterministic tests.

After production, run machine validation covering at least:

* schema validity
* required fields
* ID uniqueness
* foreign keys
* orphan relations
* duplicate relationships
* impossible date ranges
* birth > death checks
* event/person temporal conflicts
* event/place temporal conflicts
* missing source IDs
* invalid evidence references
* illegal enum values
* malformed URLs where applicable
* accepted records missing provenance

If existing repository validators exist, extend them rather than duplicating equivalent logic.

---

# 16. Quality Score

Use a 100 point quality score where practical.

Recommended dimensions:

Schema / FK / uniqueness: 10
Temporal consistency: 10
Person resolution: 10
Place resolution: 10
Source quality: 15
Evidence precision: 15
Independent source verification: 10
Content completeness: 10
Independent verifier: 10

Recommended thresholds:

90–100:
AUTO_ACCEPT

75–89:
QUARANTINE_MEDIUM

0–74:
QUARANTINE_LOW

A high score does not override a hard failure.

Hard failures always quarantine the record.

---

# 17. Hard Failure Conditions

Examples:

* fabricated source
* fabricated quotation
* broken evidence pointer
* unresolved identity presented as certain
* impossible chronology
* unsupported precise location
* missing required provenance
* verifier finds material contradiction
* deterministic integrity validation fails

Hard failures cannot be compensated for by quality score.

---

# 18. Sampling Audit

Do not manually audit every accepted record.

Perform random sampling.

Recommended initial strategy:

For every 20 accepted Critical Events:

audit at least 3 independently.

For larger batches:

audit approximately 5–10%.

If sampled material failure rate exceeds 5%:

* stop promotion of the affected batch
* mark batch as REOPEN
* identify systematic error pattern
* fix process
* rerun affected validation
* re-audit

Warnings that do not materially change historical correctness may be tracked separately.

---

# 19. Dataset Promotion

Never write research output directly into canonical production data when avoidable.

Preferred lifecycle:

raw
→ candidate
→ validated
→ verified
→ accepted
→ canonical

Alternative paths:

candidate
→ quarantine

candidate
→ rejected

Keep candidate and quarantine artifacts separate from accepted canonical data.

Use the repository's existing structure when equivalent concepts already exist.

Do not create duplicate parallel architectures unnecessarily.

---

# 20. Reports

Every autonomous batch must generate a review report.

The report must include:

* batch identifier
* processing scope
* total processed
* accepted
* quarantined
* rejected
* unresolved
* average quality score
* score distribution
* source coverage
* evidence coverage
* person coverage
* place coverage
* deterministic test results
* verifier results
* audit sample size
* audit pass/warn/fail
* recurring problems
* quarantined items requiring future attention

Final output should allow a human to review the SYSTEM, not every record.

---

# 21. Progress Management

When rpiv-todo is available:

Maintain visible tasks for:

* current batch
* research
* candidate generation
* validation
* verification
* auditing
* report generation

Do not create one todo per tiny field.

Use meaningful batch-level tasks.

Example:

* Critical Events 01–20 research
* Critical Events 01–20 enrichment
* Critical Events 01–20 deterministic QA
* Critical Events 01–20 independent verification
* Critical Events 01–20 sampled audit
* Critical Events 01–20 report

---

# 22. Web Research

When pi-web-access is available:

Use external research when repository data is insufficient.

Search for:

* authoritative sources
* primary texts
* institutional databases
* reputable academic references
* conflicting accounts

Always preserve source URLs or identifiers when available.

Do not use search snippets as strong evidence when the source page can be inspected.

Do not treat search ranking as evidence quality.

---

# 23. Existing Repository First

Before introducing new:

* schema
* table
* directory
* validator
* script
* status enum

inspect the existing repository.

Reuse existing concepts whenever possible.

Do NOT create:

`new_event_v2_final_really_final`

or parallel duplicate datasets because modifying the existing pipeline is inconvenient.

Prefer controlled migration.

---

# 24. Code Quality

When pi-lens or repository linters/tests are available:

Use them for:

* Python quality
* SQL correctness
* TypeScript correctness
* dead code
* unsafe patterns
* duplicated validation logic
* test coverage

Code-quality approval does NOT equal historical-data approval.

---

# 25. Autonomous Execution

Normal execution should continue without human intervention.

If an individual record cannot be resolved:

quarantine it and continue.

If a source is unavailable:

try alternatives, record the failure, and continue.

If a deterministic test fails:

attempt repair.

If repair is unsafe or impossible:

quarantine affected records and continue where possible.

Do not repeatedly ask:

"Should I continue?"

Continue until:

* the requested scope is complete
* a genuine repository-wide blocker occurs
* a configured safety/token limit is reached

---

# 26. Final Definition of Done

A batch is complete only when:

1. all queued items were attempted
2. candidates were generated where possible
3. deterministic tests completed
4. verification completed
5. quality gates were applied
6. failed/uncertain records were quarantined
7. sample audit completed
8. final metrics were generated
9. final review report was generated
10. repository tests pass or known failures are explicitly documented

Never declare success solely because files were generated.

---

# Final Principle

Do not optimize for record count.

Optimize for:

historical correctness,
evidence traceability,
uncertainty honesty,
data integrity,
and product usefulness.

When uncertain:

preserve uncertainty,
preserve evidence,
quarantine if necessary,
and continue.
