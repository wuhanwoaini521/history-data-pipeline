# ARCHITECTURE

`history-data-pipeline` 是中国历史数据的唯一维护仓库与 Source of Truth，职责：

```text
数据采集 → 数据清洗 → 数据标准化 → 历史资料存储 → 中国历史主干维护 →
事件维护 → Story 维护 → 数据关联 → 人工审核 → 数据质量 → DuckDB 构建 →
数据导出 → 版本管理
```

本仓库**不包含 UI**，不负责 History UI。`self-tools` 或其他应用只能消费本仓库
生成的数据产物（`dist/` 或正式 Versioned Release）。

## 四层架构

```text
┌──────────────────────────────────────┐
│  Layer 4 — Product Exports           │  dist/history.duckdb
│  DuckDB / Parquet / JSON / Manifest  │  dist/parquet/ dist/json/ dist/manifest.json
├──────────────────────────────────────┤
│  Layer 3 — History Backbone          │  data/curated/history_backbone/
│  Period / Event / Story / Relations  │  taxonomy/ + events/ + stories/ + reviews/
├──────────────────────────────────────┤
│  Layer 2 — Knowledge Store           │  knowledge：people/places/works/historical_texts
│  Person / Place / Work / Text        │  sources / entity_source_mapping
├──────────────────────────────────────┤
│  Layer 1 — Source Data               │  data/raw/（不可变）+ data/staging/（解析中间）
│  CBDB / CText / NiuTrans / ...       │
└──────────────────────────────────────┘
```

## 职责边界（不可混淆）

| 层 | 是什么 | 不是什么 |
|---|---|---|
| Layer 1 | 原始 Dataset 与其解析中间结果 | 不是业务数据；UI 禁止读取 |
| Layer 2 | 「我们拥有哪些历史资料」 | 不生成历史；不能从文本关键词自动推出 Event |
| Layer 3 | 「中国历史应该如何组织」Source of Truth | 不存原始语料；只存经过人工整理的主干 |
| Layer 4 | 构建产物（不可手动编辑） | 不是 Source；禁止手动 UPDATE DuckDB |

## Pipeline

```text
Raw Dataset
     ↓
Staging
     ↓
Knowledge Normalize
     ↓
Knowledge Store                    ← Layer 2（people/places/works/texts）
     │
Curated History Backbone           ← Layer 3（taxonomy/events/stories）
     │
Backbone Validation                ← history-data backbone validate（Gate）
     ↓
Reference Resolution               ← 引用解析到 Knowledge Store（Gate）
     ↓
Final Build                        ← history-data backbone build
     ↓
dist/history.duckdb  (+parquet/json/manifest)
```

## 关键规则

1. **Event 是中华历史主干**。Person / Place / HistoricalText 只是 Event 可以引用
   的资料，禁止从海量人物和古文自动推导完整中国历史。
2. **DuckDB = Build Artifact**。所有修改必须回到 Raw / Staging / Curated /
   Review，对应 Source 修改后重新 Build。
3. **Candidates 永远不能直接进入正式 Backbone**：

   ```text
   candidate → review → accepted → history_backbone
   ```

4. **应用只读 dist/**。禁止读取 `data/raw`、`data/staging`、`data/curated`。

## 目录

```text
src/history_data_pipeline/
├── cli.py                 CLI 入口
├── backbone/              Layer 3/4：loader/validate/reference/build/migrate/coverage
├── ingest/ parsers/ staging/ normalize/ knowledge/（legacy 迁移后的入站层保留）
├── downloaders.py parsers.py real_build.py   Layer 1/2 legacy 管线
├── query_service.py       只读查询（读 dist 或 legacy 库）
└── semantic_layer.py      LEGACY：旧 Semantic Layer V1（deprecated，审计用）
```

数据目录见 `DATA_MODEL`。时期/事件/故事维护方法见 `HISTORY_BACKBONE` 与
`CONTRIBUTING_DATA`。