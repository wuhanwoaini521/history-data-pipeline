# DATA_SOURCES

> 入口与许可中心：`metadata/sources.yml` + `metadata/licenses.yml`。
> 版本化 URL、大小、SHA-256 与检索时间一律以 `data/raw/<dataset>/<version>/metadata.json`
> 为准（运行时动态解析官方入口，代码不写死版本 URL）。

## Layer 1 数据源

| 名称 | 用途 | License | 状态 |
|---|---|---|---|
| CBDB | 人物、籍贯、官职、关系 | 见快照随附说明（默认 unknown） | 已接入 download/parse/build |
| CText Data Wiki | 实体、古籍、地点 | CC BY-NC-SA 3.0（非商业） | 已接入 download/parse |
| NiuTrans Classical-Modern | 古文/现代文平行语料 | 仓库 MIT + 各目录数据来源.txt | 已接入；`alignment_quality=heuristic_unverified` |
| CHGIS V4 | 历史行政区与地点 | 复旦许可（非商业，禁再分发） | 仅手动导入 |
| 中文 Wikipedia Dump | 现代介绍候选 | CC BY-SA 4.0 + GFDL 1.3 | 快照已下载，未解析 |
| 中文 Wikisource Dump | 原始史料候选 | Wikimedia 文本许可（页面级复核） | 快照已下载，未解析 |

## 原则

- **未知就是 unknown，不猜**：`redistribution` / `commercial_use` 未知的
  数据不进入公开导出包。
- 大数据集**不入 Git**（raw/staging/duckdb 均忽略），通过 manifest +
  download script + checksum 重建。
- Raw 快照只追加、不覆盖；任何中间结果都可从 Raw 重新生成。

## Curated（本仓库产出）

- History Backbone（Layer 3）位于 `data/curated/history_backbone/`，入 Git。
- 属于项目人工整理，`source_type: curated_reference`，不冒充 CBDB/CText
  原始数据；Event/关系的史料依据必须回溯到 HistoricalText 与 Source。