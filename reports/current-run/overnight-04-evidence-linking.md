# Overnight Queue 04 — Event Evidence Linking（130 条）

> 本轮 dry-run 重跑结果与写回状态一致（idempotent）。

## 状态总账（total=130）

| 指标 | 数量 | 说明 |
|---|---:|---|
| total | 130 | canonical event_evidence |
| **linked** | **74** | 已写回 YAML + dist（method 均记录） |
| exact_linked | 27 | conf 1.0 |
| content_linked（章首核实） | 42 | conf 0.95 |
| alias_linked | 5 | conf 0.85 |
| normalized_exact | 0 | 当前无命中（卷号归一路径可用，见测试） |
| fuzzy_candidates | 27 | NEEDS_REVIEW；段级候选（chapter#paragraph + excerpt）仅报告 |
| unmatched（missing knowledge） | 29 | 语料缺著作/缺卷覆盖 |
| needs_linking（终态） | 34 | 27 fuzzy + 7 unmatched |
| pending_knowledge（终态） | 22 | legacy 悬空 text id，0/22 在新语料解析，不冒认 |
| needs_review（人工队列） | 27 | = fuzzy candidates |

## 真实链路

```text
event → evidence → historical_text → chapter → paragraph
```
74 条 linked 全部带 `chapter_anchor`（卷类/篇卷）+ 锚点行 `historical_text_id`
（章首段，真实存在的行）；`event_text` legacy 镜像 96 行（74 新锚定 + 22 legacy id 行）。

## claim_field 支持

dist `event_evidence.claim_field` 列已就位（YAML/schema 同步，
enum: background/process/result/impact/people/places/null）。
**当前 74 条 linked 的 claim_field 均为 null（事件级证据）** —— 保持诚实：
现有证据原本就未声明字段级支持，不回填猜测值。
Queue 8 的新增证据将使用 claim_field 标注所支持字段。

→ 进入 Queue 5。
