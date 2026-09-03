# CHINA_HISTORY_BACKBONE V1 FINAL_REPORT

> China History Backbone V1（约前 2070 → 1949）最终交付报告。

```text
CHINA_HISTORY_BACKBONE_V1_READY = true
```

## 1. Period 总数

**31**（夏/商/西周/春秋/战国/秦/西汉/新/东汉/东汉末/三国/西晋/东晋/十六国/南北朝/隋/唐/五代十国/
北宋/辽/西夏/金/南宋/宋辽金/元/明/清/晚清/中华民国/近现代 + 上古）。

## 2. Regime 总数

**64**（含 parent 继承链：东魏→北齐、西魏→北周、大蒙古国→元、后金→清；武周/十国/元末群雄/
满洲国等并行政权独立成行）。

## 3. Event 总数

**618**（legacy 迁移 26 + Batch1 82 + Batch2 70 + Batch3 89 + Batch4 88 + Batch5 63 + Batch6 82 + Batch7 66 + Batch8 52）。

## 4. Critical 总数

**62**。

## 5. Major 总数

**555**（另 1 条 legacy normal）。

## 6. Aggregate Event 总数

**45**（含 ≥1 个 part_of 子事件；最大为 秦灭六国 7 子、北宋统一战争 6 子）。

## 7. Story 总数

**3**（楚汉 / 三国 / 安史之乱）。

## 8. Timeline 起点

**约前 2070**（夏朝建立，event-xia-jianguo；前 841 前一律 approximate 断代工程框架）。

## 9. Timeline 终点

**1949**（中华人民共和国成立，event-xinzhongguo-chengli，modern boundary）。

## 10. 各 Batch Event 数

| Batch | 范围 | New |
|---|---|---|
| B1 | 先秦 | 82 |
| B2 | 秦—东汉 | 70 |
| B3 | 东汉末—隋统一 | 89 |
| B4 | 隋—唐—五代十国 | 88 |
| B5 | 北宋—南宋/元边界 | 63 |
| B6 | 元—明 | 82 |
| B7 | 清—晚清—辛亥 | 66 |
| B8 | 民国—1949 | 52 |

## 11. 各 Period Event 数

| Period | n | Period | n |
|---|---:|---|---:|
| 唐 | 60 | 西汉 | 44 |
| 明 | 54 | 晚清 | 40 |
| 民国 | 53 | 战国 | 37 |
| 元 | 30 | 南北朝 | 25 |
| 春秋 | 24 | 隋 | 24 |
| 北宋 | 24 | 东汉末 | 22 |
| 清 | 21 | 南宋 | 16 |
| 五代十国 | 15 | 秦 | 14 |
| 东汉 | 14 | 三国 | 14 |
| 十六国 | 13 | 西周 | 13 |
| 西晋 | 12 | 其余 | ≤10 |

## 12. Source Coverage

**100%**（618/618 带 source_reference + source_ids；Batch8 强化档案/史料双层）。
AI 作为事实来源 **0**。

## 13. Duplicate

**0**（qa --report duplicate_candidates=0）。

## 14. Broken Ref

**0**（validate OK；跨阶段关系经剥离—恢复流程收敛）。

## 15. Invalid Date

**0**（start>end=0；date_precision 全合法——year/range/approximate；前 841 一律不伪造精确年）。

## 16. Timeline Gap

仅真实空白：夏（390y）/商（300y/204y）/西周（118y）——前 841 前史料真实稀疏；
西夏中后期（182y）/辽线（135y）为政权衰落与双政权事件归档策略所至；
其余 Period largest gap=0。未为消灭 gap 添加假事件（见 FINAL_TIMELINE_GAP_REVIEW）。

## 17. Regime Parallelism QA

PASS（三国/十六国/南北朝/五代∥十国/宋辽夏金/南宋∥金∥蒙古/元末群雄/民国-满洲国；
无"北宋→辽→西夏→金→南宋→元"串行；1206≠1271 由测试强制，见 FINAL_REGIME_STRUCTURE_REVIEW）。

## 18. Granularity QA

PASS（Period/Concept/Story 不作为事件；45 个 aggregate 均有真实子事件；
Action/Outcome 合一无重复；无皇帝即位流水账，见 FINAL_GRANULARITY_REVIEW）。

## 19. Tests

**129 passed**（test_backbone / test_backbone_build / test_backbone_batch3—8；
每批强化 gate：计数、边界（Batch 交接处不得串批）、source、timeline 顺序、1206≠1271 等）。

## 20. dist 是否成功重建

**是**：
- `dist/history.duckdb`（11,022,336 B）；
- `dist/json/china_history_major_timeline.json`（394,423 B，**617 条** critical+major，-2070→1949）；
- `dist/manifest.json`（含 §75 summary_counts：period_count=31 / regime_count=64 / event_count=618 /
  critical_count=62 / major_count=555 / story_count=3 / relation_count=1062 / source_count=7 /
  data_version=2026.09.0 / build_commit / built_at）。

---

## Gate 汇总

| Gate | 状态 |
|---|---|
| Batch1 PRE_QIN | ✅ true |
| Batch2 QIN_HAN | ✅ true |
| Batch3 WEI_JIN_NORTHERN_SOUTHERN | ✅ true |
| Batch4 SUI_TANG_FIVE_DYNASTIES | ✅ true |
| Batch5 SONG_LIAO_XIA_JIN | ✅ true |
| Batch6 YUAN_MING | ✅ true |
| Batch7 QING_LATE_QING | ✅ true |
| Batch8 REPUBLICAN_CHINA | ✅ true |
| Duplicate=0 / Broken Ref=0 / Invalid Date=0 / Source Missing=0 | ✅ |
| Validation OK / Tests PASS / Final Build PASS | ✅ |

```text
CHINA_HISTORY_BACKBONE_V1_READY = true
```

---

## 停止状态（§78）

V1 到此为止。**未**继续：Person/Place/HistoricalText Evidence Linking、Story 自动生成、
Knowledge Graph/Vector Search/Neo4j/History UI、1950—2026 现代史大规模扩展。
后续建议按 V1 → Person Linking → Place Linking → HistoricalText Evidence Linking →
Story Building V2 → History UI V2 分阶段进行；现代史扩展请按 reports/MANUAL_REVIEW_REQUIRED.md 的
V2 起点清单推进。