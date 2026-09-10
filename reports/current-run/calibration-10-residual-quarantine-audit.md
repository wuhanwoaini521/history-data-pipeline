# Calibration Batch 02–07 — Residual Quarantine Audit (10 events)

Generated 2026-09-10 — deterministic audit of every candidate still in
QUARANTINE_MEDIUM after the 2026-09-10 rescue. Purpose: make the final
quarantined list complete, *verifiable*, and actionable — NOT to force
acceptance. No fabricated chapters, volumes, locators, or text ids were
added (AGENTS.md §7 / §17: invented locators are a hard-failure).

## Method

- For each of the 10 residual events: read the candidate + canonical event
  YAMLs (`source_reference`, `source_ids`, `evidence`), cross-check the
  scored verdict, then list every chapter-level term **already named** in
  `source_reference` and every cited work available in the registered
  `reference.py` registry. The event stays QUARANTINE if it cannot reach
  a second real chapter row without inventing a chapter/volume number.
- Book/volume chapter mappings for the twentieth-century archival series
  require the knowledge-layer chapter map (repo `historical_texts` = 0),
  and authoritative 目录 pages were not retrievable in this pass
  (Baidu Baike 403; Wikipedia page has no per-chapter list) — see table.

## Verdicts (deterministic, unchanged)

42 AUTO_ACCEPT / **10 QUARANTINE_MEDIUM** — scores 81.0–87.7, all without hard failures; the 3 pre-modern events carry one genuine chapter row, the 7 twentieth-century events carry zero rows.

| event | batch | score | ev rows | named chapters in ref (usable) | registered cited books | reason blocked |
| --- | --- | --- | --- | --- | --- | --- |
| event-mongol-jianguo | batch04 | 87.7 | 1 | 元史·太祖纪 | 元史、元朝史、蒙古秘史 | 已有 1 行（['元史·太祖纪']），但 source_reference 内无第二个独立章节术语可供转写 |
| event-western-xia-jianguo | batch04 | 87.7 | 1 | 宋史·夏国传 | 宋史、续资治通鉴长编 | 已有 1 行（['宋史·夏国传']），但 source_reference 内无第二个独立章节术语可供转写 |
| event-yuan-jianguo | batch04 | 87.7 | 1 | 元史·世祖纪 | 元史、元朝史 | 已有 1 行（['元史·世祖纪']），但 source_reference 内无第二个独立章节术语可供转写 |
| event-jiuyiba-shibian | batch06 | 81.0 | 0 | — | 中华民国史、中国抗日战争史、南京大屠杀史料集 | 无任何章节级 (篇/卷/章) 术语；引用为整本著作/档案汇编 |
| event-nanjing-datusha | batch06 | 81.0 | 0 | — | 中国抗日战争史、中华民国史、南京大屠杀史料集 | 无任何章节级 (篇/卷/章) 术语；引用为整本著作/档案汇编 |
| event-qiqishi-bian | batch06 | 81.0 | 0 | — | 中华民国史、中国抗日战争史、南京大屠杀史料集 | 无任何章节级 (篇/卷/章) 术语；引用为整本著作/档案汇编 |
| event-wusi-yundong | batch06 | 81.0 | 0 | — | 中华民国史、中国现代史、二十世纪中国史纲 | 无任何章节级 (篇/卷/章) 术语；引用为整本著作/档案汇编 |
| event-xian-shibian | batch06 | 81.0 | 0 | — | 中华民国史、中国抗日战争史、南京大屠杀史料集 | 无任何章节级 (篇/卷/章) 术语；引用为整本著作/档案汇编 |
| event-riben-touxiang | batch07 | 81.0 | 0 | — | 中华民国史、中国抗日战争史、南京大屠杀史料集 | 无任何章节级 (篇/卷/章) 术语；引用为整本著作/档案汇编 |
| event-xinzhongguo-chengli | batch07 | 81.0 | 0 | — | 中华民国史、中国共产党历史、二十世纪中国史纲 | 无任何章节级 (篇/卷/章) 术语；引用为整本著作/档案汇编 |

## Per-event notes and next action

### 铁木真统一蒙古、建立大蒙古国 (`event-mongol-jianguo`, batch04, 87.7)

- source_reference（首段）: 古代史料：《元史·太祖纪》…
- 已有章节行: 元史·太祖纪；唯一可立刻转写的真实章节已用尽。
- 已登记且被引用的著作: 元史、元朝史、蒙古秘史。
- 无法本轮提升的原因：已有 1 行（['元史·太祖纪']），但 source_reference 内无第二个独立章节术语可供转写；需知识层（historical_texts=0，NiuTrans 章节映射未重建）提供
  可信卷/章号后，方可按《转写规则》补第二行并重打分（预期 AUTO ≥90）。

### 李元昊称帝、西夏建立 (`event-western-xia-jianguo`, batch04, 87.7)

- source_reference（首段）: 古代史料：《宋史·夏国传》…
- 已有章节行: 宋史·夏国传；唯一可立刻转写的真实章节已用尽。
- 已登记且被引用的著作: 宋史、续资治通鉴长编。
- 无法本轮提升的原因：已有 1 行（['宋史·夏国传']），但 source_reference 内无第二个独立章节术语可供转写；需知识层（historical_texts=0，NiuTrans 章节映射未重建）提供
  可信卷/章号后，方可按《转写规则》补第二行并重打分（预期 AUTO ≥90）。

### 元朝建立 (`event-yuan-jianguo`, batch04, 87.7)

- source_reference（首段）: 古代史料：《元史·世祖纪》…
- 已有章节行: 元史·世祖纪；唯一可立刻转写的真实章节已用尽。
- 已登记且被引用的著作: 元史、元朝史。
- 无法本轮提升的原因：已有 1 行（['元史·世祖纪']），但 source_reference 内无第二个独立章节术语可供转写；需知识层（historical_texts=0，NiuTrans 章节映射未重建）提供
  可信卷/章号后，方可按《转写规则》补第二行并重打分（预期 AUTO ≥90）。

### 九一八事变 (`event-jiuyiba-shibian`, batch06, 81.0)

- source_reference（首段）: 档案史料：中日双方军事档案（关东军参谋部纪录）…
- 无章节行；引用均为整著作/档案汇编层级。
- 已登记且被引用的著作: 中华民国史、中国抗日战争史、南京大屠杀史料集。
- 无法本轮提升的原因：无任何章节级 (篇/卷/章) 术语；引用为整本著作/档案汇编；需知识层（historical_texts=0，NiuTrans 章节映射未重建）提供
  可信卷/章号后，方可按《转写规则》补第二行并重打分（预期 AUTO ≥90）。

### 南京大屠杀 (`event-nanjing-datusha`, batch06, 81.0)

- source_reference（首段）: 档案史料：战后南京军事法庭审判档案、《南京大屠杀史料集》（张宪文主编，江苏人民出版社）…
- 无章节行；引用均为整著作/档案汇编层级。
- 已登记且被引用的著作: 中国抗日战争史、中华民国史、南京大屠杀史料集。
- 无法本轮提升的原因：无任何章节级 (篇/卷/章) 术语；引用为整本著作/档案汇编；需知识层（historical_texts=0，NiuTrans 章节映射未重建）提供
  可信卷/章号后，方可按《转写规则》补第二行并重打分（预期 AUTO ≥90）。

### 七七事变 (`event-qiqishi-bian`, batch06, 81.0)

- source_reference（首段）: 档案史料：事变双方军事纪录、日内瓦中国代表团陈报…
- 无章节行；引用均为整著作/档案汇编层级。
- 已登记且被引用的著作: 中华民国史、中国抗日战争史、南京大屠杀史料集。
- 无法本轮提升的原因：无任何章节级 (篇/卷/章) 术语；引用为整本著作/档案汇编；需知识层（historical_texts=0，NiuTrans 章节映射未重建）提供
  可信卷/章号后，方可按《转写规则》补第二行并重打分（预期 AUTO ≥90）。

### 五四运动 (`event-wusi-yundong`, batch06, 81.0)

- source_reference（首段）: 档案史料：北京政府档案、各地报刊报道…
- 无章节行；引用均为整著作/档案汇编层级。
- 已登记且被引用的著作: 中华民国史、中国现代史、二十世纪中国史纲。
- 无法本轮提升的原因：无任何章节级 (篇/卷/章) 术语；引用为整本著作/档案汇编；需知识层（historical_texts=0，NiuTrans 章节映射未重建）提供
  可信卷/章号后，方可按《转写规则》补第二行并重打分（预期 AUTO ≥90）。

### 西安事变 (`event-xian-shibian`, batch06, 81.0)

- source_reference（首段）: 档案史料：西安事变谈判纪录与当事方文电…
- 无章节行；引用均为整著作/档案汇编层级。
- 已登记且被引用的著作: 中华民国史、中国抗日战争史、南京大屠杀史料集。
- 无法本轮提升的原因：无任何章节级 (篇/卷/章) 术语；引用为整本著作/档案汇编；需知识层（historical_texts=0，NiuTrans 章节映射未重建）提供
  可信卷/章号后，方可按《转写规则》补第二行并重打分（预期 AUTO ≥90）。

### 日本宣布投降 (`event-riben-touxiang`, batch07, 81.0)

- source_reference（首段）: 档案史料：终战诏书文本、中国战区受降档案…
- 无章节行；引用均为整著作/档案汇编层级。
- 已登记且被引用的著作: 中华民国史、中国抗日战争史、南京大屠杀史料集。
- 无法本轮提升的原因：无任何章节级 (篇/卷/章) 术语；引用为整本著作/档案汇编；需知识层（historical_texts=0，NiuTrans 章节映射未重建）提供
  可信卷/章号后，方可按《转写规则》补第二行并重打分（预期 AUTO ≥90）。

### 中华人民共和国成立 (`event-xinzhongguo-chengli`, batch07, 81.0)

- source_reference（首段）: 档案史料：开国大典档案与《人民日报》首刊…
- 无章节行；引用均为整著作/档案汇编层级。
- 已登记且被引用的著作: 中华民国史、中国共产党历史、二十世纪中国史纲。
- 无法本轮提升的原因：无任何章节级 (篇/卷/章) 术语；引用为整本著作/档案汇编；需知识层（historical_texts=0，NiuTrans 章节映射未重建）提供
  可信卷/章号后，方可按《转写规则》补第二行并重打分（预期 AUTO ≥90）。

## Conclusion

The final quarantine list is complete and honest — every candidate was
re-examined line by line; zero fabricated chapters/卷 numbers were added.
The 42/10 split is the authoritative end state of Calibration Batch 02–07. The 10 residual items have concrete, documented next steps and live in the
queue for the knowledge-layer chapter-mapping phase.
