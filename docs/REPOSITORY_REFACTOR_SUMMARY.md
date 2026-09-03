# REPOSITORY_REFACTOR_SUMMARY

> 完成时间：2026-09-03
> 重构任务：`docs/REPOSITORY_REFACTOR_PLAN.md`
> 数据版本：`DATA_VERSION = 2026.09.0`

本仓库从「旧 V1 离线数据管线 + Semantic Layer」重构为四层中国历史数据仓库，
并完成三个 Story 的迁移与 Backbone Build。以下是针对第十六部分 16 个问题的回答。

---

## 1. 原仓库结构有什么问题？

- 只有 `data/curated/stories.yml` 一个文件承载三层职责：Story / Event /
  EventPerson / EventPlace / EventText / EventRelation 全部内嵌，没有独立
  Event 模型，无法支撑「Event 是主干」。
- Period / Regime 颗粒度不足：缺 `上古`、独立 `辽/西夏/金` 浏览 Period。
- Event 依赖 Story 存在（events 只能通过 story 内嵌），与「Event > Story」原则相反。
- 正式产物只有 `data/normalized/history.duckdb`，无版本、无 Manifest、无导出层；
  应用被迫读取仓库内部文件。
- 无 `schemas/`、无 Candidate/Review 目录、无 `backbone validate` 独立入口；
  EventText 命名与语义不符（应为 EventEvidence）。

## 2. 修改了哪些目录？

| 目录 | 动作 |
|---|---|
| `data/curated/history_backbone/` | 新建：taxonomy/（5 个 YAML）、events/（12 时期目录）、stories/、reviews/ |
| `schemas/` | 新建：8 个 JSON Schema（period/regime/event/story/event_relation/event_person/event_place/event_evidence） |
| `data/candidates/` | 新建：event_person/ event_place/ event_evidence/（自动算法只能进这里） |
| `data/reviews/` | 新建：pending/accepted/rejected（26 条迁移审核记录在 accepted/） |
| `dist/` | 新建：history.duckdb + parquet/ + json/ + manifest.json + manifests/ |
| `src/history_data_pipeline/backbone/` | 新建：loader/validate/schema/reference/build/migrate/coverage |
| `docs/` | 新建：7 篇目标文档；旧根文档移入 docs/*.legacy.md |
| `reports/BACKBONE_COVERAGE.md` | 新建（解除 /reports/ 忽略） |
| `metadata/sources.yml`、`metadata/licenses.yml` | 新建 |
| `src/history_data_pipeline/config.py` | 扩展：backbone/candidates/reviews/dist 路径 |
| `src/history_data_pipeline/cli.py` | 新增 `backbone validate/migrate/build/coverage/qa` |
| `.gitignore` | dist/、data/normalized/ 等构建产物忽略；reports/ 恢复跟踪 |
| `README.md`、`pyproject.toml`、`requirements.txt` | 重写/更新 |

## 3. 哪些旧代码被保留？

- `downloaders.py` / `parsers.py` / `real_build.py` / `normalization.py` /
  `database.py` / `query_service.py` / `phase_reports.py` / `quality_reports.py` /
  `review.py` / `stats.py` / `export.py` / `sample.py` / `http.py` /
  `snapshots.py`：全部保留（Layer 1/2 管线与只读查询）。
- 旧 CLI 命令（download/parse/build --from-staging/validate/stats/export/query）
  全部保留。
- `data/curated/periods.yml`、`regimes.yml`、`stories.yml`：保留
  （stories.yml 为 legacy 审计源）。
- 旧测试文件 `test_pipeline.py` / `test_query_service.py` / `test_semantic_layer.py`：
  保留不动。

## 4. 哪些代码被标记 Legacy？

- `src/history_data_pipeline/semantic_layer.py`：模块头标记
  `[LEGACY / DEPRECATED]`，仅审计与平滑迁移用。
- `data/curated/stories.yml`：legacy Semantic V1 审计源（迁移记录标记
  source-curated-semantic-v1）。
- `docs/*.legacy.md`（6 篇旧文档）：头部标记 LEGACY DOC（deprecated）。
- 数据行中 `sources` 表登记 `source-curated-semantic-legacy`，
  quality_status=`legacy`。
- 全部保留，未删除；等新 Backbone Build 稳定后再决定清理。

## 5. Knowledge Store 当前有哪些表？

Layer 2（表沿用 `SCHEMA_SQL` 命名）：

```text
sources  people  person_aliases  places  works  historical_texts
entity_source_mapping  person_relations  person_place  relation_type_dictionary
text_alignments  fact_assertions  data_review
```

当前 dist 中（无本地 Raw 快照）：people=18（curated canonical identity）、
places=3、works=7、historical_texts=0（NiuTrans 语料待重建）。

## 6. History Backbone 当前有哪些表？

Layer 3：

```text
periods  regimes  events  stories  story_events
event_relations  event_person  event_place  event_evidence（新，原 event_text）
event_evidence_candidates（空）
```

`event_text` 表保留为 legacy 兼容镜像（由 event_evidence 物化）。

## 7. Period 有多少？

**31**（上古、夏、商、西周、春秋、战国、秦、西汉、新、东汉、东汉末、三国、
西晋、东晋、十六国、南北朝、隋、唐、五代十国、北宋、辽、西夏、金、南宋、
宋辽金时期、元、明、清、晚清、中华民国、近现代）。

## 8. Event 有多少？

**26**（分布：qin_han 9、three_kingdoms 8、sui_tang 9；全部 `reviewed`，
Schema 校验与引用校验通过）。

## 9. Story 有多少？

**3**（楚汉争霸 / 三国格局形成 / 安史之乱），story_events=26，
event_relations=23。

## 10. 三个已有 Story 是否迁移成功？

**是。** `backbone migrate` 将 legacy `stories.yml` 拆分为
`events/<时期>/<event>.yml`（26 个，含 people/places/evidence/relations 独立结构）
+ `stories/<时期>/<story>.yml`（3 个），并在 `data/reviews/accepted/` 写入 26 条
审核记录。迁移后 `backbone validate` 与 24 个新测试全部通过，legacy 文件保留。

## 11. Validator 是否通过？

**是。** `history-data backbone validate` 输出
`Backbone: periods=31 regimes=31 events=26 stories=3 / Validation OK`。
Gate 测试（重复 ID、broken story ref、非法日期）确认会阻断构建。

## 12. DuckDB 是否可以重新 Build？

**是。** `history-data backbone build` 幂等重建
`dist/history.duckdb`（+ parquet/json/manifest），
参考解析 broken=0，pending=0；旧产物自动归档为 `history.previous.duckdb`。

## 13. 所有 Tests 是否通过？

**是。** `pytest -q` → `33 passed, 16 skipped`。
跳过项全部是 legacy 测试（需要本机 CBDB/CText/NiuTrans Raw 快照构建的
`data/normalized/history.duckdb`，当前 checkout 无大文件，符合设计）；
新 Backbone 测试 24 个全部通过。

## 14. 大型 Dataset 当前如何管理？

- `data/raw/`、`data/staging/`、`data/normalized/`、`dist/` 全部 gitignore；
  仓库保持可 Clone（当前含 curated backbone + schemas + 代码 + 文档）。
- 重建入口：`scripts/build-local.ps1`（下载 → parse → legacy build →
  backbone validate → backbone build --knowledge → coverage → pytest）。
- 每个快照 URL/版本/大小/SHA-256 写入
  `data/raw/<dataset>/<version>/metadata.json`（未知即 unknown，不猜）。
- 保留 `.venv/` 本地环境；未启用 Git LFS（当前无必要）。

## 15. self-tools 应该消费哪个产物？

**`dist/history.duckdb`**（只读）+ `dist/parquet/` + `dist/json/` +
`dist/manifest.json`（版本与统计）。禁止读取 `data/raw` / `data/staging` /
`data/curated`。发布正式 Release 时附带 `dist/` 与 `DATA_VERSION`。

## 16. 下一阶段应该从哪个时期开始补 History Backbone？

按 `reports/BACKBONE_COVERAGE.md`，当前 0 Event 的时期组：

```text
夏商周 / 春秋战国 / 魏晋南北朝 / 五代十国 / 宋辽金夏 / 元 / 明 / 清 / 近现代
```

建议下一阶段（China History Backbone V1）按时间顺序从**夏商周 → 春秋战国**开始，
只整理 critical + major Event 主干；秦汉/三国/隋唐已有关键节点样例可作模板。

---

## 最终状态

```text
RAW DATA → STAGING → KNOWLEDGE STORE → HISTORY BACKBONE → VALIDATION
→ BUILD → dist/history.duckdb → self-tools
```

- Layer 3 是纯人工整理（curated_backbone YAML），Schema 由 `schemas/` 权威定义；
- Event 引用层只指向 Knowledge Store ID，错误链接比 NULL 更严重；
- Candidate → Review → Accepted → Backbone 流程独立成目录；
- 本阶段已按范围停止：未自动生成 1500 个 Event、未下载新数据源、
  未建 Neo4j/Vector DB、未大规模跑 LLM、未修改 self-tools UI。