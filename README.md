# history-data-pipeline

**中国历史结构化数据仓库与构建 Pipeline。**

本仓库是中国历史数据的**唯一维护仓库与 Source of Truth**，负责数据采集、清洗、
标准化、历史资料存储、History Backbone（Period/Event/Story）维护、数据关联、
人工审核、DuckDB 构建与导出。

> **本仓库不包含 UI。** `self-tools` 或其他应用只能消费本仓库生成的数据产物
> （`dist/` 或正式 Versioned Release），禁止读取 `data/raw` / `data/staging` /
> `data/curated`。

```text
Source Data
    ↓
Knowledge Store（Person / Place / Work / Text）
    ↓
History Backbone（Period / Event / Story / Relations）← Source of Truth
    ↓
Validation（Gate）
    ↓
dist/（DuckDB / Parquet / JSON / Manifest）
```

核心原则：**Event 是中华历史主干**。Person / Place / HistoricalText 只是
Event 可以引用的资料，禁止从海量人物和古文自动推导完整中国历史。

## 四层

| 层 | 内容 | 位置 |
|---|---|---|
| 1 | Source Data（CBDB / CText / NiuTrans / Wikipedia / Wikisource） | `data/raw/`、`data/staging/` |
| 2 | Knowledge Store（资料仓库，不生成历史） | DuckDB `people/places/works/historical_texts/sources` 表 |
| 3 | History Backbone（人工整理的 Period/Event/Story） | `data/curated/history_backbone/` |
| 4 | Product Exports（应用只读这里） | `dist/` |

## 快速开始

```powershell
# 环境（Python 3.11+）
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt   # 或 uv sync

# 校验 Curated History Backbone（Validation Gate）
python -m src.history_data_pipeline backbone validate

# 重建数据产物
python -m src.history_data_pipeline backbone build
python -m src.history_data_pipeline backbone coverage

# 测试
python -m pytest
```

## CLI

```bash
# Layer 1/2（legacy 管线，需要本地 Raw 快照）
history-data download cbdb|ctext|niutrans|wikipedia|wikisource
history-data parse
history-data build --from-staging      # 构建 data/normalized（legacy）

# Layer 3/4（新 Backbone 管线）
history-data backbone validate         # 校验（--json 输出结构）
history-data backbone migrate          # 迁移 legacy stories.yml（--dry-run）
history-data backbone build            # dist/history.duckdb + manifest + 导出
history-data backbone coverage         # reports/BACKBONE_COVERAGE.md
history-data backbone qa               # 引用解析 QA（person/place/evidence）

# 只读查询（优先 dist/history.duckdb）
history-data query periods --json
history-data query story "楚汉争霸" --events --json
history-data query event "赤壁之战" --people --json
```

## 当前状态

- Period Taxonomy：**31** 个浏览 Period（上古→近现代，含辽/西夏/金），
  Regime：**31** 个政权。
- History Backbone：**26** 个 Event、**3** 个 Story（楚汉争霸 / 三国格局形成 /
  安史之乱），全部通过 `backbone validate` 并重新 QA。
- `dist/` Build 可重复生成，Manifest 带真实统计（见 `dist/manifest.json`）。
- 旧 Semantic Layer（V1）标记 **legacy/deprecated** 保留审计，未删除。

## 文档

- 架构：`docs/ARCHITECTURE.md`、`docs/DATA_MODEL.md`、`docs/HISTORY_BACKBONE.md`
- 数据源与质量：`docs/DATA_SOURCES.md`、`docs/DATA_QUALITY.md`
- 贡献：`docs/CONTRIBUTING_DATA.md`（新增 Event/Story 的完整工作流）
- 发布：`docs/RELEASE_PROCESS.md`
- 重构：`docs/REPOSITORY_REFACTOR_PLAN.md`、`docs/REPOSITORY_REFACTOR_SUMMARY.md`
- 旧 V1 文档：`docs/*.legacy.md`（deprecated）

## 已知边界

- 大数据集（CBDB / Wikimedia Dump 等）不入 Git；通过
  `scripts/build-local.ps1` + checksum 本机重建。
- NiuTrans 句对 `alignment_quality=heuristic_unverified`，不视为人工验证。
- 当前 EventEvidence 的 HistoricalText 链接为 `pending_knowledge`：
  已通过审核，等待知识库（NiuTrans 语料）重建后解析。
- 第一阶段未自动生成全部历史 Event；后续 **China History Backbone V1**
  阶段按 `reports/BACKBONE_COVERAGE.md` 缺口补齐 Major Event 主干。