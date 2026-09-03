# BACKBONE_REVIEW

> Backbone QA 报告：Duplicate Check + Granularity QA + Timeline Gap Detection。
> 由 `history-data backbone qa --report` 生成；Duplicate 候选不自动合并，Gap 不自动补点。

## 1. Duplicate Check（候选，不自动 Merge）

未发现疑似重复/上下层事件候选。

## 2. Granularity QA

- 事件类型分布：{"war": 53, "political": 35, "political-military": 18, "reform": 13, "dynastic-transition": 9, "rebellion": 9, "economic": 6, "diplomatic": 6, "treaty": 4, "alliance": 3, "cultural": 2, "migration": 2, "unification": 2, "foundation": 2}

- Aggregate（有子事件 part_of）数量：10
  - event-qin-mie-liuguo：7 个子事件
  - event-han-xiongnu-war：5 个子事件
  - event-chuhan-war：4 个子事件
  - event-chuzhuang-wang-ba：2 个子事件
  - event-qihuan-gong-ba：2 个子事件
  - event-hezong-lianheng：2 个子事件
  - event-chuhan-qin-revolt：2 个子事件
  - event-wu-guo-jueqi：1 个子事件
  - event-zheng-zhuanggong-xiaoba：1 个子事件
  - event-zhougong-shezheng：1 个子事件

- 长跨度事件（>80 年，需注意与单点事件粒度区分）：
  - 合纵连横（event-hezong-lianheng）：-334~-247 approximate

## 3. Timeline Gap Detection

- 阈值：相邻 critical/major 事件间隔 > 150 年（且 > 该 Period 跨度的 25%）
- 共 23 处：

| Period | 类型 | 明细 |
|---|---|---|
| 上古 | 空白 | 该 Period 尚无 critical/major Event。 |
| 夏 | 间隔过大 | 少康中兴（-1990）→ 商汤灭夏（-1600）：间隔 390 年。相邻 critical/major 事件间隔 390 年（阈值 150 年），可能遗漏重要节点；是否补点需人工判断。 |
| 商 | 间隔过大 | 商朝建立（-1600）→ 盘庚迁殷（-1300）：间隔 300 年。相邻 critical/major 事件间隔 300 年（阈值 150 年），可能遗漏重要节点；是否补点需人工判断。 |
| 商 | 间隔过大 | 武丁中兴（-1250）→ 武王伐纣（-1046）：间隔 204 年。相邻 critical/major 事件间隔 204 年（阈值 150 年），可能遗漏重要节点；是否补点需人工判断。 |
| 东汉 | 空白 | 该 Period 尚无 critical/major Event。 |
| 西晋 | 空白 | 该 Period 尚无 critical/major Event。 |
| 东晋 | 空白 | 该 Period 尚无 critical/major Event。 |
| 十六国 | 空白 | 该 Period 尚无 critical/major Event。 |
| 南北朝 | 空白 | 该 Period 尚无 critical/major Event。 |
| 隋 | 空白 | 该 Period 尚无 critical/major Event。 |
| 五代十国 | 空白 | 该 Period 尚无 critical/major Event。 |
| 北宋 | 空白 | 该 Period 尚无 critical/major Event。 |
| 辽 | 空白 | 该 Period 尚无 critical/major Event。 |
| 西夏 | 空白 | 该 Period 尚无 critical/major Event。 |
| 金 | 空白 | 该 Period 尚无 critical/major Event。 |
| 南宋 | 空白 | 该 Period 尚无 critical/major Event。 |
| 宋辽金时期 | 空白 | 该 Period 尚无 critical/major Event。 |
| 元 | 空白 | 该 Period 尚无 critical/major Event。 |
| 明 | 空白 | 该 Period 尚无 critical/major Event。 |
| 清 | 空白 | 该 Period 尚无 critical/major Event。 |
| 晚清 | 空白 | 该 Period 尚无 critical/major Event。 |
| 中华民国 | 空白 | 该 Period 尚无 critical/major Event。 |
| 近现代 | 空白 | 该 Period 尚无 critical/major Event。 |

> 注意：此处仅报告，不自动补造 Event；是否补点由人工依据真实历史粒度判断。

---

