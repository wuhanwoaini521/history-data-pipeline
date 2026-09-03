# CHINA_HISTORY_BACKBONE BATCH5_SUMMARY

> China History Backbone V1 · Batch 5（北宋·辽·西夏·金·南宋·蒙古/元边界）总结。

## 结论先行

```text
SONG_LIAO_XIA_JIN_BACKBONE_READY = true
```

## 1. 新增 Event 总数

**63**（Critical 8 + Major 55）

Critical：陈桥兵变北宋建立 / 李元昊称帝西夏建立 / 金国建立 / 靖康之变北宋灭亡 /
赵构称帝南宋建立 / 蒙古建国（1206）/ 元建立（1271）/ 崖山海战南宋灭亡（1279）。

## 2. Reused Event 总数

**1**：event-guo-wei-dai-han（951 后周建立，960 代周前节点）。

## 3—5. 各时期 New / Reused / Total

| 时期段（Period） | New | Total |
|---|---:|---:|
| 北宋（period-northern-song） | 24 | 24 |
| 辽（period-liao） | 2 | 3（+契丹建国 916）|
| 西夏（period-western-xia） | 6 | 6 |
| 金（period-jin） | 6 | 6 |
| 南宋（period-southern-song） | 16 | 16 |
| 宋辽金（period-song-liao-jin，蒙元前夜段） | 8 | 8 |
| 元（period-yuan） | 1 | 1 |

## 6. Critical（8）

陈桥兵变北宋建立 / 西夏建立 / 金国建立 / 靖康之变北宋亡 / 南宋建立 / 蒙古建国 /
元建立（1271 边界）/ 崖山南宋亡。（全库 critical：25+8=**33**。）

## 7. Major

55（全库 major：321+55=**376**）。

## 8. Aggregate

**2**：北宋统一战争（6 子：灭荆南/灭后蜀/灭南汉/灭南唐/吴越纳土/灭北汉）、
宋蒙战争（3 子：蒙古灭大理/钓鱼城之战/襄樊之战）。

## 9. 新增 Regime 数

**1**：regime-mongol-empire（大蒙古国 1206–1271）；regime-yuan 挂 parent_regime_id 继承链
（不是串行）。Regime 53 → **54**。

## 10. 并行表达

- 北宋 ∥ 辽 ∥ 西夏（979–1125）：高梁河（宋×辽）、三川口/好水川/定川寨（夏×宋）；
- 南宋 ∥ 金（1127–1234）：采石之战（宋×金）、金灭辽·蔡州之战（蒙×金×宋）；
- 南宋 ∥ 蒙古/元（1234–1279）：崖山海战（元×宋）。
详见 reports/SONG_LIAO_XIA_JIN_REGIME_REVIEW.md。

## 11. 1206 ≠ 1271

regime-mongol-empire（1206–1271, period-song-liao-jin）与 regime-yuan（1271–1368, period-yuan）
两个独立 Regime 表达两阶段；测试强制"1271 前已结束的事件不得挂 regime-yuan"
（襄樊 1267–1273 跨 1271 注明例外）。

## 12. Duplicate

**0**（qa --report；"第一次/第二次围攻开封"为第X次枚举系列豁免）。

## 13. Broken Ref

**0**（4 处跨阶段关系在阶段提交时剥离、末段全量恢复）。

## 14. Invalid Date

**0**（date_precision 使用 year/range；把初稿中的"single"统一修正为"year"，与既有 7/203 分布一致）。

## 15. Source Coverage

63/63：source_reference（古代史料：宋史/辽史/金史/元史/续资治通鉴长编/三朝北盟会编/蒙古秘史/
金佗稡编等 ＋ 现代参考：白寿彝《中国通史·宋辽金元卷》、邓广铭、漆侠、王曾瑜、刘浦江、
吴天墀、韩儒林、周良霄等）＋ source_ids 100%；AI 未作事实来源。

## 16. Timeline Gap

宋辽夏金段无 coverage_gap（北宋建960→澶渊1004→西夏1038→金1115→靖康1127→
蒙古1206→金灭1234→元建1271→崖山1279 连续）。

## 17. Validation

`backbone validate` → **OK**；build gate 通过。

## 18. Tests

**94 passed**（新增 Batch5 10 测：baseline/陈桥/三政权并行/金宋蒙并行/1206≠1271/靖康/
岳飞史源审慎/崖山终点/source/timeline）。

## 19. 全库 Event 总数

**418**（Period 31 / Regime 54 / Story 3 / EventRelation 745 / Works 30）。

## 20. Timeline

- dist/json/china_history_major_timeline.json：**417 条** critical+major（-2070 → **1279**）。
- 本批关键链：960 陈桥 → 979 灭北汉 → 979 高梁河 → 1004 澶渊 → 1038 西夏 → 1040–1042 三败 →
1115 金建 → 1125 辽亡 → 1127 靖康/南宋建 → 1130 黄天荡 → 1140 郾城 → 1142 岳飞被害/绍兴和议 →
1161 采石 → 1163 隆兴北伐 → 1206 蒙古建/开禧 → 1234 金灭/端平入洛 → 1259 钓鱼城 → 1271 元建 →
1276 临安降 → 1279 崖山。

---

## 下一批（Batch 6：元 → 元末 → 明，1271–1644）

复用 元建立（event-yuan-jianguo）/ 南宋灭亡段边界；从 元定都大都、行省制度等元内部展开，
至 1644 北京陷落、崇祯自缢结束；明初禁用"juan"式皇帝流水账，政变/改革/战争为骨干。