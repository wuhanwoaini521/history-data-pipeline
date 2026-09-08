# DATA_MODEL

> 本文描述 V2 数据模型。旧 V1 模型见 `docs/DATA_MODEL.legacy.md`（legacy）。

## 逻辑 Schema（四层）

```text
knowledge.period / knowledge.regime            ← Layer 3 taxonomy（浏览单位）
knowledge.person / person_alias                ← Layer 2
knowledge.person_relation / person_place       ← Layer 2
knowledge.place                                ← Layer 2
knowledge.work / historical_text               ← Layer 2
knowledge.source / entity_source_mapping       ← Layer 2（可追溯性）
curated.event / story / story_event            ← Layer 3 backbone
curated.event_person / event_place             ← Layer 3 桥接
curated.event_evidence（原 event_text）         ← Layer 3 证据桥接
curated.event_relation                         ← Layer 3 事件关系
```

V2 第一阶段保持原有 DuckDB 无 Schema 表名（表即 `periods`、`people`、`events`、
`event_evidence`…），通过 `docs/ARCHITECTURE.md` 与代码结构明确 Knowledge /
Backbone 边界；后续如需逻辑命名，用 `VIEW` 建立 `knowledge.*` / `curated.*` 映射，
不做大规模重命名。

## 实体

| 表 | 核心字段 | 层 |
| --- | --- | --- |
| `periods` | `id, name_zh_cn, start_year, end_year, date_precision, description_zh_cn` | 3 taxonomy |
| `regimes` | `id, name_zh_cn, 年代, period_id, date_precision` | 3 taxonomy |
| `events` | `id, name_zh_cn, event_type, 起止年, date_precision, period_id, regime_ids, importance, quality_status` | 3 |
| `stories` | `id, title_zh_cn, 年代, story_type, importance, period_id` | 3（阅读组织层） |
| `story_events` | `story_id, event_id, sequence` | 3 |
| `event_relations` | `source_event_id, target_event_id, relation_type, confidence` | 3 |
| `event_person` | `event_id, person_id, role, side, link_*` | 3 桥接 |
| `event_place` | `event_id, place_id, place_name_raw, link_status` | 3 桥接 |
| `event_evidence` | `event_id, historical_text_id, evidence_role, link_status, review_note` | 3 证据桥接 |
| `event_text` | 同 event_evidence 内容（LEGACY 兼容镜像） | legacy |
| `people` | `id, canonical_name_zh_cn, 生卒年, created_from_source` | 2 |
| `places` | `id, canonical_name_zh_cn, historical_name, 坐标, 有效年代` | 2 |
| `works` | `id, title, title_zh_cn` | 2 |
| `historical_texts` | `id, original_text, original_simplified, translation_zh_cn, alignment_quality` | 2 |
| `sources` | `id, dataset, license, snapshot_version, raw_path` | 2 |
| `entity_source_mapping` | `entity_type, entity_id, source_id, external_id, match_type` | 2 |

## 引用规则（错误链接比 NULL 更严重）

- Event 只允许引用 `knowledge.person.id` / `knowledge.place.id` /
  `knowledge.historical_text.id`。
- 无法确认时：保留 `person_name_raw` / `place_name_raw`、`person_id: null`、
  `link_status: needs_linking`。
- `link_status`：`linked`（已解析）/ `needs_linking`（待人工关联）/
  `pending_knowledge`（已审核，等待知识库重建）/ `rejected`。

## 时间规则

- 公元前统一负整数：公元前 221 = `-221`；公元 208 = `208`。
- `date_precision`：`exact / year / range / approximate / before / after / unknown`。
- 夏、商、西周等早期只能 `approximate`/`range`，不得伪造精确年代。

## EventRelation 白名单（第一版）

`precedes / follows / causes / caused_by / leads_to / contributes_to / part_of / related_to`

严格区分 `precedes`（时间先后）与 `causes`（因果，必须史料支持）。

## importanace

`critical / major / normal / minor`。未来 UI 可只加载 `critical + major` 形成
中国历史主时间线。

## 不可变规则

- `original_text` 永远保留 Raw 原文；OpenCC 只写 `original_simplified`。
- DuckDB 是 Build Artifact：手动 UPDATE 被禁止；修改必须回到
  Raw/Staging/Curated/Review 后重新 `history-data backbone build`。

## Schema 等价映射（不建平行 schema）

框架不再引入 `event_content.schema.json` / `claim.schema.json`，等价物已存在：

- `event_content` ↔ `schemas/event.schema.json`（事件完整属性模型）。
- `claim` ↔ `schemas/event_evidence.schema.json` + `taxonomy/quality_status.yml`
  （证据/主张桥接 + 状态词表）。

新增属性或证据类型一律落进现有 schema，禁止建平行文件。详见
`docs/DATA_ENRICHMENT_POLICY.md` §8 与 `docs/QUALITY_GATES.md`。
