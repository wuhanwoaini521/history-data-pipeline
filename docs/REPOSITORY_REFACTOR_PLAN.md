# REPOSITORY_REFACTOR_PLAN

> 仓库：`history-data-pipeline`
> 任务：从「旧 V1 离线数据管线 + Semantic Layer」重构为「四层中国历史数据仓库」。
> 本文档先于重构执行，基于对当前仓库的完整扫描（2026-09-03）。

---

## 1. 当前仓库实际状态（扫描结果）

### 1.1 目录

```text
history-data-pipeline/
├── README.md / DATA_MODEL.md / DATA_QUALITY.md / DATA_SOURCES.md
│   / HISTORY_SEMANTIC_QUERY_CONTRACT.md / LICENSE_NOTES.md / DATA_INVENTORY.md
├── pyproject.toml / requirements.txt / uv.lock / .gitignore
├── config/                  sources.yml、normalization.yml、mappings/
├── metadata/licenses.json
├── sample/seed.json
├── scripts/build-local.ps1
├── src/history_data_pipeline/   21 个 Python 模块，约 4300 行
├── data/
│   └── curated/            periods.yml / regimes.yml / stories.yml
└── tests/                  test_pipeline.py / test_query_service.py / test_semantic_layer.py
```

### 1.2 关键事实

| 项目 | 现状 |
|---|---|
| `data/raw` / `data/staging` / `data/normalized` / `data/exports` / `data/reports` | 均为 gitignore，本机当前未落盘（无真实 CBDB/CText/NiuTrans 数据快照） |
| `data/curated/periods.yml` | 27 个 Period（缺 `上古`、独立 `辽`/`西夏`/`金` Period） |
| `data/curated/regimes.yml` | 28 个 Regime |
| `data/curated/stories.yml` | 3 个 Story：楚汉争霸 / 三国格局形成 / 安史之乱，内嵌 26 个 Event |
| Semantic Layer | `semantic_layer.py`（1002 行）构建 `data/normalized/history.duckdb`，含 period/regime/stories/events/event_person/event_place/event_text(candidates)/story_person/story_place，QA 已确认 |
| Query 层 | `HistoryQueryService` + CLI `query` 子命令，读 `data/normalized/history.duckdb` |
| 测试 | 3 个测试文件；`test_query_service` / `test_semantic_layer` 在正式库不存在时自动 skip |
| 包管理 | uv + requirements.txt；环境已有 duckdb/PyYAML |

### 1.3 存在的问题（本次重构要解决的）

1. **只有 stories.yml 一个文件承载三层职责**：Story / Event / EventPerson / EventPlace / EventText / EventRelation 全部内嵌，没有独立 Event 模型，无法支撑「Event 是主干」。
2. **Period 与 Regime 职责颗粒度不足**：`宋辽金时期` 同时是 Period 又承载辽/西夏/金 Regime；缺 `上古`、独立 `辽/西夏/金` 浏览 Period。
3. **Event 依赖 Story 存在**：没有 Story 时无法组织 Event；与「Event > Story」原则相反。
4. **DuckDB 是唯一的正式产物，但没有版本、Manifest 和 Export 层**：自应用只能读 `data/normalized/` 内部文件，违反「应用只读 dist/」边界。
5. **Schema 全部散落在 Python 建表 SQL 与 QA 测试里**：没有独立 `schemas/`。
6. **EventText 命名混淆**：语义上应改为 EventEvidence（evidence_role：primary/supporting/related）。
7. **无 Candidate / Review 独立目录**：自动关联结果与正式 Backbone 混在同一个库中。
8. **Story 迁移后没有新的独立验证入口**：缺少 `backbone validate` 与 Validation Gate。

---

## 2. 目标架构（四层）

```text
┌──────────────────────────────────────┐
│  Layer 4 — Product Exports           │  dist/history.duckdb
│  DuckDB / Parquet / JSON / Manifest  │  dist/parquet/ dist/json/ dist/manifest.json
├──────────────────────────────────────┤
│  Layer 3 — History Backbone          │  data/curated/history_backbone/
│  Period / Regime / Event / Story     │  taxonomy/ + events/ + stories/
│  EventRelation / StoryEvent          │  (+ 引用 resolution → 桥接表)
├──────────────────────────────────────┤
│  Layer 2 — Knowledge Store           │  knowledge.people/places/works/historical_texts
│  Person / Place / Work / Text        │  sources / entity_source_mapping
├──────────────────────────────────────┤
│  Layer 1 — Source Data               │  data/raw/（不可变）+ data/staging/（解析中间）
│  CBDB / CText / NiuTrans / ...       │
└──────────────────────────────────────┘
```

### 2.1 目录迁移清单

| 动作 | 路径 |
|---|---|
| 保留（标记 legacy/deprecated） | `data/curated/stories.yml`、`semantic_layer.py`、`data/normalized/` 旧构建路径 |
| 新建 | `data/curated/history_backbone/{taxonomy,events,stories,reviews}/` |
| 新建 | `schemas/*.schema.json`（Period/Regime/Event/Story/EventRelation/EventPerson/EventPlace/EventEvidence） |
| 新建 | `data/candidates/{event_person,event_place,event_evidence}/` |
| 新建 | `data/reviews/{pending,accepted,rejected}/` |
| 新建 | `dist/`（history.duckdb / parquet / json / manifest.json / manifests/） |
| 新建 | `docs/`（7 篇目标文档） |
| 新建 | `reports/BACKBONE_COVERAGE.md`（解除 `/reports/` 的 gitignore） |
| 新建 | `metadata/sources.yml`、`metadata/licenses.yml` |
| 新建 | `src/history_data_pipeline/backbone/`（models/schema/loader/validate/reference/build/migrate/coverage）|
| 删除 | 无（旧东西全部保留或标记 legacy） |

---

## 3. 执行步骤

1. **Taxonomy 先完整**：`taxonomy/periods.yml` 补齐 上古/辽/西夏/金；`regimes.yml`；新增 `event_types.yml` / `relation_types.yml`（只允许 8 种关系）/ `quality_status.yml`。
2. **Schema 落地**：`schemas/` 9 个 JSON Schema（用 jsonschema 校验）。
3. **迁移 26 个 Event + 3 个 Story**：从 `data/curated/stories.yml` 拆出：
   - `events/<period_dir>/<event>.yml`（含 EventPerson / EventPlace / EventEvidence / EventRelation 独立结构）
   - `stories/<period_dir>/<story>.yml`（只存 StoryEvent 顺序）
   - importance 映射：legacy high→major、medium→normal
   - 文本链接：保留 `historical_text_id` + work/term，`link_status=pending_knowledge`（真实文本语料不在本 checkout，等知识库重建）；人与地点沿用 legacy QA 的 linked/needs_linking 结论
   - 迁移同时写 `data/reviews/accepted/` 审核记录
4. **Backbone 模块**：`models.py` / `loader.py` / `schema.py` / `validate.py` / `reference.py` / `build.py` / `migrate.py` / `coverage.py`。
5. **CLI**：新增 `history-data backbone {validate,migrate,build,coverage,qa}`；旧命令全部保留。
6. **Validation Gate**：ID 重复、孤儿引用、无效日期、重复 sequence、accepted evidence 缺 source → build 失败。
7. **Final Build**：`dist/history.duckdb` + `dist/manifest.json`（DATA_VERSION=2026.09.0）+ parquet/json 导出；知识库引用已解决/待重建计数进入 manifest。
8. **测试**：保留旧 3 个测试文件（不破坏），新增 15+ backbone 测试。
9. **文档**：README 重写 + docs/ 7 篇 + reports/BACKBONE_COVERAGE.md。
10. **停**：不自动生成 1500 个 Event，不建 Neo4j/Vector DB，不改 self-tools UI。

---

## 4. 边界与不变量

- `data/raw/` 永不可修改；`data/staging/` 只是解析中间产物，UI 不得读取。
- Knowledge Store 不自动生成 Event / Story（禁止「关键词匹配 → Event」）。
- Backbone 内 Event 只允许引用 `knowledge.person.id`；不确定就 `person_name_raw + person_id: null + link_status: needs_linking`。错误链接比 NULL 更严重。
- EventRelation 第一版只允许 8 类；`precedes` ≠ `causes`。
- DuckDB 是 Build Artifact，禁止手动 UPDATE；所有修改回到 Raw/Staging/Curated/Review 后重新构建。
- self-tools 只消费 `dist/`（history.duckdb / 正式 Versioned Release）。
- 大数据集（CBDB/Wikipedia dump 等）不入 Git：gitignore + 下载脚本 + checksum 重建。

---

## 5. 完成判定（DoD）

- [ ] `docs/REPOSITORY_REFACTOR_SUMMARY.md` 回答问题 1–16
- [ ] `history-data backbone validate` 通过
- [ ] `history-data backbone build` 生成 `dist/history.duckdb` + manifest（真实统计）
- [ ] 三个 Story 迁移成功且重新 QA 通过
- [ ] 新增 + 旧有全部测试运行通过
- [ ] 旧 Semantic Layer 标记 legacy 但未删除