# Overnight Queue 07 — Data Integrity Gate

> 检查对象：dist/history.duckdb（应用读取的最终库）+ knowledge store。
> 双 build 对比见 Queue 02（pre/post rebuild：730,128 = 730,128，零增长零重复）。

## dist 完整性检查（全部通过）

| 检查项 | 结果 | 判定 |
|---|---|---|
| historical_texts 行数 = 去重 id 数 | 730,128 = 730,128 | ✅ 无 duplicate |
| 空文本行（original_text NULL/空） | 0 | ✅ |
| 无 book_id/title 行 | 0 | ✅ |
| paragraph_index 非法（NULL/<1） | 0 | ✅ |
| orphan source_id（texts→sources） | 0 | ✅ |
| orphan book_id（texts→works） | 0 | ✅ |
| event_evidence duplicate id | 0 / 130 | ✅ |
| evidence→event 孤儿 | 0 | ✅ |
| **linked evidence→historical_text 孤儿** | **0** | ✅ 74 条锚点全部可解析 |
| linked 缺 chapter_anchor/link_method | 0 | ✅ |
| fuzzy 被写成 linked | **0** | ✅ 硬规则成立 |
| link_method 枚举越界 | 0 | ✅ |
| linked 行章节引用无效 | 0 | ✅ |

## knowledge store（data/normalized）

| 检查项 | 结果 |
|---|---|
| texts 730,128 / distinct 730,128 | ✅ |
| chapter_heads 3,838 | ✅ |
| 双 build 计数稳定 | ✅（Queue 02 实测） |

## 结论

无数据破坏，build deterministic —— 未触发 STOP_MUTATION。
→ 进入 Queue 8（本轮核心新增工作）。
