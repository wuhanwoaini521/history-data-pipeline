# Overnight Queue 03 — Source Reference → Chapter Mapping

> 映射系统已在 commit `22158dc` 落地（`backbone/source_reference.py` +
> `backbone/evidence_link.py` + `data/curated/knowledge/chapter_aliases.json`）。
> 本报告为 overnight 快照：机制、分级、当前分布、测试覆盖。

## 章节写法归一化（支持的形态）

| 输入形态 | 解析结果 |
|---|---|
| 第十二章 / 第12章 | ('章', 12) |
| 十二章 / 一百九十三 | 中文数字 → int（'十二'→12） |
| 卷十二 / 卷12 / 十二卷 | ('卷', 12)，双向归一（卷12 ↔ 卷十二） |
| Chapter 12 / chapter 3 | ('章', N) |
| 《书名·篇章》 | work + term 拆分（全角/半角分隔符统一） |
| 三段引用《三国志·魏书·文帝纪》 | 多段 term：末段作章名、前段作卷类 |

## 匹配分级（match_method + confidence）

| method | confidence | 自动写回 | 机制 |
|---|---:|---|---|
| exact | 1.0 | ✅ | term 与语料篇卷/卷类名精确一致 |
| normalized_exact | 0.9 | ✅ | 卷号形式归一后一致（卷12 ↔ 卷十二） |
| alias | 0.85 | ✅ | 人工映射表，每条附语料内容核实证据（如 元史·太祖纪 → 本纪/卷一，依据卷一首行「◎太祖太祖法天启运圣武皇帝，讳铁木真」） |
| content | 0.95 | ✅ | 语料章首行前缀核实（确定性；多章同名锚定首章，防误配的 tail 白名单 + token 复现规则） |
| fuzzy | 0.6 | ❌ 永不 | 只产出 candidates + 报告（NEEDS_REVIEW），带坐标也不写回（有回归测试） |
| manual | 1.0 | ✅（人工驱动） | 预留给人工复核后的写回 |

## 当前分布（130 条 canonical evidence）

```text
linked 74 = exact 27 + content 42 + alias 5
fuzzy_candidate 27（NEEDS_REVIEW，仅报告）
unmatched 29（missing knowledge：语料缺著作/缺卷覆盖）
legacy 悬空 id 22（pending_knowledge，旧库构建 id 在新语料 0/22 解析，不冒认）
```

## 测试覆盖

`tests/test_source_reference.py`（14 例）+ `tests/test_evidence_link.py`（12 例）：
数字互转、全部定位符形态、引文解析、四级匹配、跨卷锚定、
**fuzzy 带坐标也不写回（回归）**、YAML 写回保头尾注释。

→ 进入 Queue 4。
