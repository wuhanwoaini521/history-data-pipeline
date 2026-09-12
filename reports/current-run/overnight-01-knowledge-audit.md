# Overnight Queue 01 — Knowledge Layer Audit

> 结论先行：根因已在知识层重建（commit `22158dc`）中查明并修复。本报告为 overnight 快照，
> 完整审计见 `reports/current-run/knowledge-layer-audit.md`。

## 八问八答

| 问题 | 答案 |
|---|---|
| NiuTrans 原始数据在哪里 | GitHub `NiuTrans/Classical-Modern` @ `4e746ea`（2024-04-21，MIT，~410MB）；`双语数据/` 97 书句对齐 + `古文原文/` 190 书 |
| 是否已进入 raw | **已进入**：`data/raw/classical-modern/20240421/`（gitignored，11,017 文件，metadata.json 记录 commit 与 sha256 清单） |
| 是否已 normalization | **已进入**：`data/staging/knowledge/historical_texts.jsonl` → `data/normalized/history.duckdb`（Layer 2） |
| 章节信息是否存在 | **存在**：语料目录即 `书/卷类/篇卷` 三级 + 行级句对；另建 `chapter_heads`（3,838 条章首行） |
| 历史实现是否存在 | `real_build.py`（legacy Layer-2 全量构建）+ `parsers.iter_classical_modern` 均可复用；ID 方案 `text-niutrans-sha1(source_path:line)` 与文档示例一致 |
| 在哪个 stage 丢失 | **不丢在任何转换 stage** —— 数据从未进入管道（raw 快照空），叠加 dist 构建默认 seed-only（`cli.py` 仅显式 `--knowledge` 才并入知识层） |
| 为什么最终 DuckDB 为 0 | 上游 raw 缺失 + seed-only 默认 + `knowledge_seed_rows` 本身不含 texts（三因叠加） |

## 数据链（现况，全链已通）

```text
raw/classical-modern/20240421/repository/双语数据/**
  → knowledge_build.iter_bilingual_texts（parser）
  → data/staging/knowledge/historical_texts.jsonl（normalized dataset）
  → data/normalized/history.duckdb（knowledge store；sources/works/historical_texts/chapter_heads）
  → backbone build --knowledge（dist 并入，既有 ATTACH 路径零改动）
  → dist/history.duckdb（historical_texts=730,128）
  → event_evidence（74 条 linked，经 source_reference normalizer 锚定）
```

明确根因 → 按指令直接进入 Queue 2（重建已落地，本轮做验证性复核）。
