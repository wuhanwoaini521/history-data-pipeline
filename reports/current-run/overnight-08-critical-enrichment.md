# Overnight Queue 08 — 14 Critical Events Enrichment（Batch 01，source-backed）

> 执行方式：**按事件纵向富化**（每事件一次性补 background/process/result/impact/
> people/places/evidence），不按字段横向批处理。
> 脚本：`scripts/overnight_critical_enrichment.py`（幂等，可重跑）。
> 铁律执行：每条叙述字段均以 evidence 行回链到语料具体段落
> （`chapter_anchor#p行号` + `historical_text_id`），review_note 保留逐字引文；
> `claim_field` 标注所支持字段；无逐字引文支撑的字段一律不填（NEEDS_SOURCE）。

## 14 Critical 总览

| 事件 | before | after | 状态 |
|---|---:|---:|---|
| event-mongol-jianguo 蒙古建国 | 33.3 | **100.0** | completed |
| event-pingwang-dongqian 平王东迁 | 33.3 | **100.0** | completed |
| event-yuan-jianguo 元朝建立 | 33.3 | **100.0** | completed |
| event-chuzhuang-wang-ba 楚庄王称霸 | 11.1 | **88.9** | partial（缺 related_event） |
| event-jinwen-gong-ba 晋文公称霸 | 11.1 | **88.9** | partial（缺 related_event） |
| event-hezong-lianheng 合纵连横 | 11.1 | **88.9** | partial（缺 related_event） |
| event-jiuyiba-shibian 九一八 | 33.3 | 33.3 | **blocked：source missing** |
| event-nanjing-datusha 南京大屠杀 | 33.3 | 33.3 | **blocked：source missing** |
| event-qiqishi-bian 七七事变 | 33.3 | 33.3 | **blocked：source missing** |
| event-riben-touxiang 日本投降 | 33.3 | 33.3 | **blocked：source missing** |
| event-wusi-yundong 五四运动 | 33.3 | 33.3 | **blocked：source missing** |
| event-xian-shibian 西安事变 | 33.3 | 33.3 | **blocked：source missing** |
| event-western-xia-jianguo 西夏建国 | 33.3 | 33.3 | **blocked：source missing**（宋史·夏国传不在语料） |
| event-xinzhongguo-chengli 新中国成立 | 33.3 | 33.3 | **blocked：source missing** |

汇总：**completed 3 / partial 3 / blocked（NEEDS_SOURCE）8**。
分数带：≥90 ×3；88.9 ×3（80–89 带）；<80 ×8。

## 语料来源（每事件的提取章节）

| 事件 | 依据章节（NiuTrans 语料原文） |
|---|---|
| 蒙古建国 | 元史·本纪/卷一（行115/230/236/245 逐字引文） |
| 元朝建立 | 元史·本纪/卷七（建国号曰大元诏全文）+ 卷四（世祖即位） |
| 平王东迁 | 史记·十二本纪/周本纪（行358-366，含"政由方伯"影响原文） |
| 楚庄王称霸 | 史记·三十世家/楚世家（一鸣惊人/问鼎/围郑/败晋师河上/鄢陵） |
| 晋文公称霸 | 左传·僖公/僖公二十八年（城濮之战/践土之盟/温之会） |
| 合纵连横 | 史记·七十列传/苏秦列传（六国从合/从约长并相六国/函谷关十五年） |

## 各事件补全明细

| 事件 | background | process | result | impact | people | places | evidence(新增) |
|---|---|---|---|---|---|---|---|
| 蒙古建国 | ✅泰赤乌/汪罕/乃蛮兼并 | ✅1205征夏→1206即位→征乃蛮 | ✅大蒙古国建成/畏吾儿来归 | ✅始议伐金/转向扩张 | 屈出律 | 斡难河源、也儿的石河 | 4（claim_field 齐全） |
| 元朝建立 | ✅1260即位/开平·燕京 | ✅1271禁金律/定朝仪/下诏 | ✅国号取乾元之义 | ✅绍百王纪统/制度转向 | 刘秉忠 | 开平府、燕京 | 4 |
| 平王东迁 | ✅烽火失信/废太子 | ✅申侯联犬戎攻幽王 | ✅立平王/东迁雒邑 | ✅周室衰微政由方伯（原文） | 周平王、申侯、周幽王 | 雒邑、骊山 | 4 |
| 楚庄王称霸 | ✅一鸣惊人 | ✅问鼎/围郑/邲之战 | ✅大败晋师河上 | ✅复国陈/鄢陵拉锯 | 楚庄王、王孙满 | 洛、郑 | 4 |
| 晋文公称霸 | ✅侵曹伐卫 | ✅城濮之战 | ✅践土之盟 | ✅温之会/霸政延续 | 晋文公、得臣 | 城濮、践土 | 4 |
| 合纵连横 | ✅五倍地十倍众 | ✅六国从合/并相六国 | ✅秦兵不敢出函谷十五年 | ✅犀首离间/两策成局 | 苏秦、赵肃侯 | 函谷关 | 4 |

## remaining gaps

- **related_event ×3**（楚庄王/晋文公/合纵连横）：需要与既有事件建立可解释因果边
  （目标 event_id 必须真实存在且因果可述），属策展决策，留待人工核对事件清单后补。
- **8 个 blocked 事件**：等待 20 世纪档案类著作与宋史·夏国传的可靠章节来源（见 OVERNIGHT_FINAL Blockers）。
- 人物/地点均带 `link_status: needs_linking`（name_raw 来自原文，身份/坐标待解析，
  不伪造 person_id / place_id / coordinates）。
