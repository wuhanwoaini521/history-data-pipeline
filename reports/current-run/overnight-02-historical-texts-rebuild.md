# Overnight Queue 02 — historical_texts Pipeline 重建（验证复核）

> 重建已在 commit `22158dc` 落地。本轮 overnight 做验证性复核（含一次全新 rebuild）。

## 管道形态

```text
raw source（data/raw/classical-modern/20240421，只读）
  → parser（knowledge_build.iter_bilingual_texts / iter_classical_texts）
  → normalized dataset（data/staging/knowledge/historical_texts.jsonl）
  → knowledge store（data/normalized/history.duckdb）
  → backbone build --knowledge（ATTACH 拷贝，既有路径零改动）
  → dist/history.duckdb
```

从未直接手改 dist；全程只读 raw、确定性派生。

## 知识粒度（document → chapter → paragraph）

| 语义层 | 物理落点 | 语料来源 |
|---|---|---|
| document | `works`（book_id；优先复用 curated work id，避免同名重复行） | 目录一级（书名） |
| 卷类 part | `historical_texts.section` | 目录二级（本纪/列传/秦纪…） |
| chapter | `historical_texts.chapter` | 目录三级（卷一/秦始皇本纪/秦纪一…） |
| paragraph | `paragraph_index`（= source.txt 行号，与 ID 生成同源） | 行级句对 |

非整篇全文存储：一行 = 一个段落级句对（原文 + 简体 + 今译 + 来源 + license 透传）。

## 必须实现的六项（全部满足）

| 要求 | 实现/证据 |
|---|---|
| 稳定 ID | `text-niutrans-sha1(source_path:line_number)[:20]`，路径锁定快照版本 |
| 可重复 build | 见下实测：连续 rebuild 计数逐位一致 |
| 来源信息 | `source_id=source-classical-modern` + sources 表（license: MIT + 各目录 数据来源.txt 保留于 notes_zh_cn） |
| chapter 信息 | chapter + section 双列（含 chapter_heads 章首行索引 3,838 条） |
| paragraph 顺序 | paragraph_index 1 起连续 |
| license/source metadata | dist SQL 可直接 join sources.license（E2E 样例已验证） |

## 重复执行实测（本轮复跑）

```text
pre  rebuild: (730128, 730128)     # COUNT = COUNT(DISTINCT id)
rebuild #1 ok
post rebuild: (730128, 730128)     # 无增长、无 duplicate
dist rebuild ok → dist texts (730128, 730128)
dist evidence: linked 74 / needs_linking 34 / pending_knowledge 22
knowledge_available: True
```

## 结论

`backbone build` 后 `historical_texts = 730,128 > 0`（Gate 达成）→ 进入 Queue 3。
