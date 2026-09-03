# RELEASE_PROCESS

## 版本

数据版本号在仓库根 `DATA_VERSION`，格式 `YYYY.MM.N`（如 `2026.09.0`）。
正式构建读取该文件写入 `dist/manifest.json`。

## 构建

```bash
# 校验（Validation Gate：broken reference / duplicate id / invalid date 会失败）
history-data backbone validate

# 正式构建：dist/history.duckdb + dist/parquet/ + dist/json/ + dist/manifest.json
history-data backbone build

# 覆盖率报告
history-data backbone coverage

# QA
history-data backbone qa
pytest
```

`backbone build` 是幂等的；旧产物保留为 `history.previous.duckdb` / 归档快照。

## 产物

```text
dist/
├── history.duckdb      # 应用唯一入口（或正式 Versioned Release）
├── manifest.json       # 当前版本
├── manifests/
│   └── manifest-<version>.json   # 版本归档
├── parquet/            # 各表 Parquet（ZSTD）
└── json/               # periods/regimes/events/event_relations/stories/
                        # story_events/event_people/event_places/event_evidence/
                        # people/places/works/historical_texts
```

`manifest.json` 示例：

```json
{
  "version": "2026.09.0",
  "built_at": "...",
  "git_commit": "...",
  "counts": { "people": 18, "events": 26, "stories": 3, "historical_texts": 0, "...": "..." },
  "reference_resolution": { "persons": {...}, "places": {...}, "evidences": {...}, "broken": 0 }
}
```

## 消费方约束（self-tools 等）

- 只允许读取 `dist/`（`history.duckdb`）或正式 Versioned Release；
- 禁止读取 `data/raw` / `data/staging` / `data/curated`；
- 展示时必须保留来源、License 与质量标记（`quality_status`、
  `alignment_quality=heuristic_unverified` 等）。

## 修改数据必须回到 Source

禁止：

```text
手动 UPDATE dist/history.duckdb
```

流程：

```text
Raw / Staging / Curated / Review 修改
        ↓
history-data backbone validate
        ↓
history-data backbone build
        ↓
dist 产物更新
```

## 大数据集管理

- `data/raw/`、`data/staging/`、`data/normalized/`、`dist/` 不入 Git。
- 拉取代码后执行 `scripts/build-local.ps1`（或等价 shell）下载并重建
  CBDB/CText/Classical-Modern 本地快照；
- 每个快照的 URL/版本/大小/校验和写入 `data/raw/<dataset>/<version>/metadata.json`；
- 发布 Release 时附带 `dist/` 构建产物与 `DATA_VERSION`。

## 本阶段停止条件

完成架构重构、三个 Story 迁移与 Backbone Build 后即停止；不自动生成
全部历史 Event、不建 Neo4j/Vector DB、不改 self-tools History UI。
下一阶段单独进行 **China History Backbone V1**（按时期补齐 Major Event 主干）。