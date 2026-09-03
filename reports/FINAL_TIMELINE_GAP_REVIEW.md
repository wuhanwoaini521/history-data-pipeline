# FINAL_TIMELINE_GAP_REVIEW

> China History Backbone V1 · 全时间轴 Gap 审计（§69）。
> 方法：每个 Period 内 critical+major 事件按 start_year 排序，统计相邻间隔；gap_years>100 列出。
> 原则（§69）：不为了消灭 Gap 添加假事件；真实空白保留。

## 全轴范围

**约前 2070（夏朝建立）→ 1949（中华人民共和国成立 boundary）**，主 timeline 617 条（critical+major，其余 1 条 legacy normal 不含）。

## 按 Period：Duration / Critical / Major / Largest Gap

| Period | 事件数 | Critical | Major | largest gap | 说明 |
|---|---:|---:|---:|---:|---|
| 夏 | 4 | 1 | 3 | 390y | **真实空白**：少康中兴(-1990)→商汤灭夏(-1600)；前 841 前年代为断代工程框架，不硬补 |
| 商 | 4 | 2 | 2 | 300y/204y | 商建(-1600)→盘庚迁殷(-1300)；武丁中兴→武王伐纣；同上 |
| 西周 | 13 | 1 | 12 | 118y | 穆王西征→国人暴动；真实间隔（西周中期史料稀疏） |
| 西夏 | 6 | 1 | 5 | 182y | 庆历和议(1044)→蒙古灭西夏(1226)；西夏中后期无政权级大事，真实空白 |
| 辽 | 3 | 0 | 3 | 135y | 契丹建国(916)→重熙增币(1042)；宋辽双政权事件（澶渊/高梁河）归档于 period-northern-song（主导方宋侧），辽期线稀疏属归档策略而非漏点 |
| 其余 25 Period | — | — | — | 0 | 无 >100y 间隔（西汉/唐/明/民国等主干密集） |

## 无争议结论

- **0 个"疑似遗漏"级 gap 需要补事件**（夏商西周的间隔为史前-青铜早期史料与断代工程框架的真实空白；西夏中后期为政权衰落期之真实空白）；
- period-antiquity（上古）无事件（未建档上古神话传说不入主干，属设计决定）。

## 与原 qa_report coverage_gaps 对照

`backbone qa --report` 的 coverage_gaps（antiquity empty / xia 390 / shang 300）与本审计一致，
均为已知真实空白，维持现状。**FINAL: Timeline Gap Audit PASS。**