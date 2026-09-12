# Batch 02 · Queue 0 — Git / Workspace State Audit

> 执行时间：2026-09-12 · 命令：`git status` / `git log -1 --oneline` / `git submodule status`（两仓库）

## 结论

**歧义已解决：两仓库均已推送，子模块工作区的未提交改动全部属于上一轮 overnight run（Queue 8–11）的合法产物，无异常、无丢失提交。**

## Main repo（self-tools）

| 项 | 值 |
|---|---|
| branch | `main`，与 `origin/main` 一致 |
| HEAD | `403d5fd` `fix: point history-data-pipeline gitlink at 22158dc` |
| clean/dirty | 除子模块指针内容变化（modified content + untracked content）外**干净**；无本地未推送提交 |

## Submodule（history-data-pipeline）

| 项 | 值 |
|---|---|
| branch | `main`，与 `origin/main` 一致（HEAD == 22158dc 已推送） |
| HEAD | `22158dc` `feat(knowledge): rebuild historical_texts knowledge layer and restore evidence chain` |
| clean/dirty | **dirty**：14 modified + 13 untracked + 0 deleted |

## Dirty 内容审计（对照上一轮 OVERNIGHT_FINAL.md 第 2 节，逐项吻合）

### Modified（14，全部为 overnight-08 Critical 富化及其再生报告）

| 文件 | 归属 | 内容 |
|---|---|---|
| `data/curated/history_backbone/events/**` ×6（mongol-jianguo / yuan-jianguo / pingwang-dongqian / chuzhuang-wang-ba / hezong-lianheng / jinwen-gong-ba） | overnight-08 | 6 个 Critical 事件的四维叙述 + people/places(needs_linking) + 24 条 source-backed evidence（`link_method: manual`，带逐字引文与段落锚） |
| `src/history_data_pipeline/backbone/build.py` | overnight-08 | `person_id` 为空的 needs_linking 人物不入 dist `event_person`（防 dist 主键崩溃、不伪造身份），+5 行 |
| `tests/test_backbone.py` / `tests/test_backbone_build.py` | overnight-08 | 4 处硬编码计数更新（places 26→37、evidence 130→154、pending_knowledge 96→120、needs_linking 23→34） |
| `reports/BACKBONE_COVERAGE.md` / `PRODUCT_COVERAGE.md` / `ENRICHMENT_QUEUE.json` / `product_coverage.json` / `current-run/quarantine-after-knowledge-rebuild.json` | overnight-09 | 富化后再生报告 |

### Untracked（13，全部为上一轮新增产物）

- `scripts/overnight_critical_enrichment.py`（overnight-08 执行脚本）
- `reports/current-run/overnight-00..10-*.md` ×11 + `OVERNIGHT_FINAL.md`

## 风险评估

- 上一轮反馈中「14 files changed / +940 -0」为近似描述；实际 `git diff --stat` 为 **14 files, +2750/−2361**（大头是 `ENRICHMENT_QUEUE.json` 全量再生 +2750/−2361 中的 4510 行 churn）。差异不构成冲突：文件清单与 OVERNIGHT_FINAL.md 完全一致。
- 改动均通过上一轮 overnight-10 测试（Python 236 / Rust 200 / tsc），无 reset/rebase/checkout/clean 需求。
- **决定：不做任何破坏性操作，保留改动继续本轮任务。** 本轮结束时统一评估是否提交。
