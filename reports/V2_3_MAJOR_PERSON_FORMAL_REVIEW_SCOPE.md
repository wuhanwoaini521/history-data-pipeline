# V2.3 · Major Event Event-Person Formal Review（Scope 与总体裁决）

## 概述

- 输入: V2.2 machine 层 candidate links = **223**（machine events=194，其中 184 事件有 formal_accept）
- formal_accept = **208** | formal_reject = **13** | insufficient_event_evidence = **2**
- 方法: `agent_assisted_source_review`（machine 推荐→agent 逐条复核→curated_class=`curated_accepted`）；无 `human_reviewed` 声称（本节之后的 V2.4 为人工复核门）。

## 角色分布（formal_accept）

- `ruler` （统治者）: 72
- `initiator` （发起者）: 44
- `commander` （军事指挥）: 31
- `official` （官员）: 26
- `victim` （受害者）: 14
- `political_leader` （政治领导人）: 12
- `participant` （参与者）: 9

## reject/insufficient 类别

- 背景引用: 11
- 相邻事件: 2
- insufficient_event_evidence: 2

## curated（补充）Person 在正式层使用

- formal_accept 中涉及的 curated person: 8 个：['curated-person-chiang-kai-shek', 'curated-person-cixi-taihou', 'curated-person-jia-nanfeng', 'curated-person-mao-zedong', 'curated-person-songhuizong', 'curated-person-sun-yat-sen', 'curated-person-zhang-xueliang', 'curated-person-zhou-enlai']

## 覆盖（period → 事件数）

- period-five-dynasties-ten-kingdoms: 5
- period-jin: 2
- period-late-eastern-han: 12
- period-late-qing: 12
- period-liao: 1
- period-ming: 22
- period-northern-song: 6
- period-northern-southern: 3
- period-qin: 1
- period-qing: 5
- period-republic: 19
- period-sixteen-kingdoms: 12
- period-southern-song: 3
- period-spring-autumn: 10
- period-sui: 10
- period-tang: 27
- period-three-kingdoms: 7
- period-warring-states: 11
- period-western-han: 15
- period-western-jin: 3
- period-western-xia: 2
- period-western-zhou: 8
- period-xin: 3
- period-yuan: 9

`gate: V2_3_MAJOR_PERSON_FORMAL_REVIEW_READY=true` 当且仅当机器链接全部裁决且无遗漏。

加载器口径：正式 event_person 行 = 200（V2.1/2.1.1）+ 198（V2.3 净新增，共 208 接受，其中 10 条与 V1 内联 people 去重） = **398**。
