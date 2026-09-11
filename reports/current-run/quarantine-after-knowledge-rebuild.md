# QUARANTINE 事件知识层重处理报告（阶段三）

> 生成：2026-09-11 · 知识层重建后对 10 个 QUARANTINE_MEDIUM 候选的重打分。
> 数据来源：`reports/current-run/quarantine-after-knowledge-rebuild.json`（脚本
> `scripts/quarantine_rescore_after_knowledge.py`，确定性、可重跑）。
> 目的：验证 `knowledge → evidence → event` 整条链真正可用——不是清零 quarantine。

## 一、总表（原分数 → 新分数）

| 事件 | 批次 | 原分数 | 新分数 | 结论 | 知识层贡献 |
|---|---|---:|---:|---|---|
| event-mongol-jianguo 蒙古建国 | batch04 | 87.7 | **88.7** | 仍 QUARANTINE | 元史·太祖纪 → alias 锚定 本纪/卷一 |
| event-yuan-jianguo 元朝建立 | batch04 | 87.7 | **88.7** | 仍 QUARANTINE | 元史·世祖纪 → alias 锚定 本纪/卷四 |
| event-western-xia-jianguo 西夏建国 | batch04 | 87.7 | 87.7 | 仍 QUARANTINE | 宋史·夏国传 语料无此章，无法核实 |
| event-jiuyiba-shibian 九一八 | batch06 | 81.0 | 81.0 | 仍 QUARANTINE | 中华民国史等不在语料 |
| event-nanjing-datusha 南京大屠杀 | batch06 | 81.0 | 81.0 | 仍 QUARANTINE | 同上（含南京大屠杀史料集） |
| event-qiqishi-bian 七七事变 | batch06 | 81.0 | 81.0 | 仍 QUARANTINE | 同上 |
| event-wusi-yundong 五四运动 | batch06 | 81.0 | 81.0 | 仍 QUARANTINE | 同上 |
| event-xian-shibian 西安事变 | batch06 | 81.0 | 81.0 | 仍 QUARANTINE | 同上 |
| event-riben-touxiang 日本投降 | batch07 | 81.0 | 81.0 | 仍 QUARANTINE | 同上 |
| event-xinzhongguo-chengli 新中国成立 | batch07 | 81.0 | 81.0 | 仍 QUARANTINE | 同上 |

无人越过 90（AUTO_ACCEPT 阈值）→ **全部如实保留 QUARANTINE**，未降低任何门槛。

## 二、链路验证结论（本轮真正要证明的事）

`source → historical_texts → chapter → evidence → event` 全链已打通：

1. **元史·太祖纪 → historical_texts 本纪/卷一**：alias 映射由语料内容核实
   （`双语数据/元史/本纪/卷一` 首行「◎太祖太祖法天启运圣武皇帝，讳铁木真」），
   锚点行 `text-niutrans-ac7d2777eb8bd1839a67`（卷一首段，真实存在的行，非虚构 id）。
2. **元史·世祖纪 → 本纪/卷四**：同一机制（卷四首行「◎世祖一世祖圣德神功文武皇帝，讳忽必烈」）。
3. 候选 YAML 已写回 `historical_text_id + chapter_anchor + link_method`，
   future promotion 时 dist 的 event_evidence → historical_texts join 即刻可用。

## 三、仍然缺失（需要新增数据，不是流程问题）

| 缺口 | 阻塞事件 | 需要什么 |
|---|---|---|
| 宋史·夏国传（卷485-486，外国传）不在语料 | 西夏建国 | 宋史外国传各卷文本（或任一可信电子版逐卷文本） |
| 蒙古秘史 / 元朝史 无第二证据章节 | 蒙古建国 | 两书任一的可信章节目录+文本 |
| 20 世纪现代史著作整部缺失（中华民国史/中国抗日战争史/南京大屠杀史料集/中国共产党历史/二十世纪中国史纲） | 7 个 batch06/07 事件 | 档案类著作的章节映射（人工提供可信目录页后按转写规则补录） |

以上全部维持 QUARANTINE / NEEDS_SOURCE，等待可靠来源；不存在编造的章节号或文本 id。
