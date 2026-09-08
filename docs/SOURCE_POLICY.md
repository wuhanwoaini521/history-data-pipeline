# Source Policy

> Status: **bootstrap v1**. Operational source-handling policy for autonomous
> enrichment. Extends `config/sources.yml`, `docs/DATA_SOURCES.md` and the
> provenance fields already defined in the schemas (`source_type`, `source_reference`,
> `source_ids`, `work`+`term` on evidence).

## 1. Principles

1. **Never invent a source.** A fabricated source is a hard failure (AGENTS.md §17).
2. **Search ranking is not evidence quality** and search snippets are not strong
   evidence when the source page can be inspected (AGENTS.md §22).
3. **Source count ≠ independent source count.** Baidu Baike + a site copying Baidu
   Baike + another repost = **one** source family, not three.
4. **Tier C (Wikipedia/Wikidata/Baidu Baike) is for candidate/alias discovery and
   rough cross-checks only** — never sole evidence for an important historical claim.
5. Every evidence record keeps provenance: classical text (`work` + `term` +
   `chapter_hint`) or a modern/reference citation.

## 2. Source tiers

The tier vocabulary used by `quality.py` (source-quality and
independent-source-verification dimensions):

| Tier | Examples | Role | Scoring in the 100-point model |
| --- | --- | --- | --- |
| A — Primary / institutional / academic | `左传` / `史记` / `资治通鉴` / official archives / university & museum databases / peer-reviewed lit | Primary anchor | highest evidence weight |
| B — High-quality reference | author encyclopedias, established scholarly projects, rigorously maintained datasets | corroboration | medium |
| C — General reference | Wikipedia / Wikidata / Baidu Baike / general reference websites | candidate discovery, aliases, rough cross-check | low — never sole evidence |
| D — Weak | blogs, SEO pages, unsourced reposts, AI-generated pages, content farms | never as authoritative evidence | rejected |

Existing `config/sources.yml` datasets map as follows:

* `cbdb` — institutional database (Tier A; primary structured data).
* `ctext` — primary textual corpus with established scholarly standing (Tier A/B).
* `classical-modern` (NiuTrans) — primary derived corpus; `alignment_quality =
  heuristic_unverified` must be treated as **unverified**, not human-verified (see
  README "已知边界").
* `chgis` — institutional, but manual-import only (no license in repo).
* `wikipedia` / `wikisource` — Tier C; raw snapshots only; never converted into
  authoritative claims.

## 3. Provenance requirements

A candidate record that will be accepted must satisfy at least one of:

1. `source_reference` is a non-empty string describing the primary + modern anchors,
   **or**
2. `source_ids` is a non-empty list of known source/work IDs from `knowledge.source`
   (`works` / `entity_source_mapping`), including work IDs like `work-curated-*`.

For **evidence** entries:

* `work` and `term` are required (schema `event_evidence.schema.json`).
* `evidence_role` ∈ `primary / supporting / related`.
* `link_status` is required to reflect the review stage: `linked`,
  `needs_linking`, `pending_knowledge` or `rejected`.
* A record claiming status `verified`/`reviewed`/`accepted` **must** carry a source
  provenance; missing provenance quarantines it (`no_provenance`).

## 4. Conflicts (disputed claims)

When sources disagree:

* do **not** pick the majority position just because it is more common;
* preserve both views and mark the record `ambiguous` / `conflicting_sources`
  (→ quarantine) rather than silently choosing;
* the quarantine row keeps both source hints so a human can review the conflict.

## 5. Source references must be real

The deterministic validator cannot verify a web page actually exists. Therefore the
policy is:

* only `work` + `term` + `chapter_hint` (locatable in a known work) count as an
  evidence locator;
* any order/URL that is only a domain or a generic landing page is a **weak**
  locator; score `source_quality` accordingly;
* inventing a locator (chapter, work) is a **hard failure** — quarantined row gets
  `evidence_locator_missing` / `fabricated_*`.

## 6. Enforcement point

Enforcement lives in the deterministic gates:

1. `history-data backbone validate` — considers the provenance clause (§3) and the
   real-locator clause (§5) against the curated backbone (broken references,
   accepted evidence without source, `linked` without a canonical ID).
2. `history-data backbone qa-run` — scores candidates (source quality 15 pts +
   independent source verification 10 pts) and quarantines violations of §4–§5.

No new source registry is created: `config/sources.yml` + `knowledge.source_sql` +
`schemas/event_evidence.schema.json` remain the single source model.
