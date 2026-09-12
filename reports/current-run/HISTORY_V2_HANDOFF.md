# HISTORY V2 — DEVELOPER HANDOFF（回来先读这个）

## Current commits

- self-tools: 见父仓库 `chore: bump history-data-pipeline` 最新提交
- history-data-pipeline: 见 `git -C history-data-pipeline log -1`（Phase 1 收尾提交）

## Current data metrics

- events **618** | FULL **181** | STRONG **86** | LOW **0** | mean **47.5**
- evidence **1177** | places(event_place) **308** | relations **1112** | historical_texts **733372**
- depth classes: HIGH 24 / MID 36 / NATURAL 34 / SOURCE_LIMITED 1

## Build command

```bash
cd history-data-pipeline
PY=/home/hans/.local/share/uv/python/cpython-3.11.14-linux-x86_64-gnu/bin/python3
export PYTHONPATH="src:.venv-batch02/lib/python3.11/site-packages"
$PY -m history_data_pipeline.cli backbone --knowledge data/normalized/history.duckdb build
```

## Validate command

```bash
$PY -m history_data_pipeline.cli backbone validate
```

## Test commands

```bash
$PY -m pytest tests/ -q                 # Python（测试会重建 dist → 之后必须重跑 build）
cd .. && cargo test -p devtoolbox-infrastructure --lib   # Rust
```

## Important directories

- `data/curated/history_backbone/events/<period>/event-*.yml` — canonical 事件数据（唯一可写层）
- `data/raw/` — **immutable**，禁止手改
- `data/normalized/history.duckdb` — 知识层（文本/章节/段落）
- `dist/history.duckdb` — 派生产物（build 生成，不入库的目录按 gitignore）
- `scripts/` — 簇富化脚本、门禁、锚点工具（anchor_lookup.py / para_dump.py / _depth_util.py）
- `reports/current-run/` — 本轮与阶段报告

## Important reports

- `HISTORY_V2_PHASE_FINAL.md`（阶段总报告）
- `HISTORY_V2_PHASE_SCORECARD.md`（验收对照）
- `DEPTH_BACKLOG_V2.json`（下一阶段深度队列）
- `HISTORY_V2_BLOCKERS.md`（遗留债务）
- `HISTORY_V2_NEXT_ROADMAP.md`（路线）

## DO NOT BREAK Rules

1. SOURCE-BACKED FIRST（无来源不写内容）
2. fuzzy never auto-link（fuzzy = candidate only）
3. raw data immutable（data/raw 只读）
4. canonical facts must have provenance（每条 evidence 有锚）
5. do not conflate historical place with modern place（历史地名不与现代地名混用）
6. coverage_score != content_depth（不混用两个指标）
7. do not inflate STRONG via text length（禁止无信息扩写）
8. submodule push before main gitlink update（先推子模块再更新 gitlink）

## Next recommended task

- Depth Sprint 03：清 **ADEQUATE_HIGH 24 个（P1）**（多为只差 1 维），或
- Content Production：从 `reports/ENRICHMENT_QUEUE.json` 取下一批 30 个 READY 事件。