# Person Linking V1 Final Summary（含 V2.3 正式化）

- **events** = 618
- **critical_events** = 62
- **major_events** = 555
- **formal_links_base** = 200
- **formal_links_v23** = 208
- **formal_links_net_new** = 198
- **formal_links_total** = 398

## 26 项审计要点（摘要版）

- Q1 事件总数: 618（冻结，V1/V2.1 不变）
- Q2 关键事件: 62；主要事件: 555
- Q3 正式 person-link 总数: 398（基础 200 + V2.3 净新增 198；V2.3 裁决接受 208 条，与 V1 内联重复自动去重 10 条）
- Q4 链接精确度 resolution: exact（机器筛 + identity evidence）
- Q5 身份正确率: 无 KNOWN_WRONG_IDENTITY（V2.2 排除误链全部在决策层）
- Q6-8 事件名/别名/日期口径: 录入 people/person_aliases；补充 Person 全部带 source_reference
- Q9 遗存风险: 见 PERSON_LINKING_V1_RISK_REVIEW（A集：仅 agent 复核；V2.4 人核未执行）
- Q10 链接去重: 同一 (event_id,person_id) 不重复；reject 不写正式层
- Q11 引用完整性: 每次正式 person 均带 identity_evidence + event_reference
- Q12 知识门禁: gate=Person Linking V1 READY（见下）
- Q13-26 详见风险报告与各事件 review 记录（data/reviews/formal/event_person_v2_3/）

## 门禁

- `gate: PERSON_LINKING_V1_READY=true`（V2.3 agent 复核层完成；机器候选未混入正式 Backbone）
- `gate: V2_3_FORMAL_REVIEW_COVERAGE=100%`
- 注: 本总结不声称 `human_reviewed`；人工逐条复核作为 V2.4 门保留。
