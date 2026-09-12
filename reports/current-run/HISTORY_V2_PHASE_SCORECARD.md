# HISTORY V2 PHASE SCORECARD

## Architecture — **PASS**
- source → chapter → paragraph → evidence → claim → enrichment → validation 全链路贯通；`backbone validate` OK；dist 可重建。

## Knowledge Layer — **PASS**
- historical_texts：**733372**；sources：多快照（NiuTrans + wikisource 20260912/20260912b）；build deterministic（两次构建一致，见 Q18）。

## Evidence Layer — **PASS**
- evidence total：**1177**（linked 1163 / needs_linking 14）；dangling **0**；fuzzy linked **0**。

## Event Coverage — **PASS（批次目标内）**
- FULL **181 / 618**（29.3%）。

## Content Quality — **PASS**
- STRONG / FULL：**86/181**（47.5%）；STRONG / ALL：**13.9%**；LOW **0**。

## Critical — **PASS（除 LICENSE_BLOCKED）**
- **60 / 62**；blocked：九一八事变、西安事变（许可限制，非内容失败）。

## Places — **PASS**
- event_place：**308**；同名重复 0。

## Relations — **PASS**
- relations：**1112**；dangling 0 / duplicate 0 / self-ref 0。

## Integrity — **PASS**
- 0 broken links；0 duplicate IDs；0 duplicate places；0 invalid anchors；0 invalid claim_field。

## Tests — **PASS**
- Python 249 passed / 16 skipped；Rust 99 passed；tsc SKIPPED_WITH_REASON。
