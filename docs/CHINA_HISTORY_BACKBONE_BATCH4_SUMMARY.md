# CHINA_HISTORY_BACKBONE BATCH4_SUMMARY

> China History Backbone V1 · Batch 4（隋→唐→五代十国）总结。
> 数据版本：2026.09.0；完成时间：2026-09-03。

## 结论先行

```text
SUI_TANG_FIVE_DYNASTIES_BACKBONE_READY = true
```

§58 Gate 全部满足：589 隋统一复用、隋→唐转换清楚、唐建/玄武门/唐初扩张/武周 Regime/
开元天宝主线/安史 9 Event 复用/中晚唐非空白/黄巢/唐亡/五代结构/十国并行/辽并行/后周阶段均在位；
Duplicate=0 / Broken Ref=0 / Invalid Date=0 / Source Missing=0 / Validation OK / Tests 全通过。

---

## 1. 新增 Event 总数

**88**（Critical 8 + Major 80）

## 2. Reused Event 总数

**11**：event-yangjian-dai-beizhou（581 隋建立）/ event-sui-mie-chen（589 隋灭陈统一）2 个
＋ 安史之乱 Story 9 个既有 Event（event-anlu-*：兼领三镇751/起兵755/洛阳756/潼关756/长安756/
玄宗入蜀756/收复长安757/史思明再叛759-761/平定763）——全部原样复用，无重复建档。

## 3—5. 各时期 New / Reused / Total

| 时期段（Period） | New | Reused | Total |
|---|---:|---:|---:|
| 隋（period-sui） | 21 | 2（581 隋建/589 隋灭陈，加江都兵变亦在期） | 24 |
| 唐（period-tang） | 51 | 9（安史 9 Event） | 60 |
| 五代十国（period-five-dynasties-ten-kingdoms） | 15 | 0 | 15 |
| 辽（period-liao） | 1 | 0 | 1 |

> 说明：唐 60 = 9 安史复用 + 51 新增（其中 4 个唐前期 events 注释以「period-tang」为期；
> 「隋」行含既有 581/589 两节点与 隋炀帝 等 21 新节点）。New/Reused 由 review provenance 自动区分
> （见 reports/BACKBONE_COVERAGE.md）。

## 6. Critical（本批新增 8）

李渊称帝唐朝建立 / 玄武门之变 / 唐灭东突厥 / 武则天称帝武周建立 / 神龙政变中宗复位 /
黄巢起义 / 朱温废哀帝后梁建立唐朝灭亡 / 郭威代汉后周建立。
（全库 critical 现共 **33**：Batch1 7 + Batch2 5 + Batch3 13 + Batch4 8。）

## 7. Major

本批 **80**（全库 major **321**）。

## 8. Aggregate

本批新增 **3**：隋征高句丽（3 子）/ 元和削藩（1 子：淮西之战）/ 黄巢起义（2 子）/
柴荣改革（2 子：高平之战/征南唐）——共 4 个（含柴荣改革）。
（全库 aggregate 现共 19+。）

## 9. 新增 Regime 数

**11**（武周 regime-wu-zhou ＋ 十国 吴/南唐/吴越/楚/闽/前蜀/后蜀/南汉/荆南/北汉），42 → **53**。
（五代五 Regime 与辽为既有，未重复创建。）

## 10. 武周是否正确表达

**是**：`regime-wu-zhou`（690–705）独立 Regime，period_id=period-tang（§17 Period 不另建）；
武则天称帝（690）/武周制度变革（690–700）/神龙政变（705）事件均挂 regime-wu-zhou。

## 11. 五代是否正确表达

**是**：后梁/后唐/后晋/后汉/后周 5 Regime 存在；政权更替以事件链表达（非 parent 链，
后者仅用于北魏分裂系）；907 后梁代唐（critical）→ 923 后唐 → 936 后晋 → 947 后汉 → 951 后周。

## 12. 十国并行是否正确

**是**：10 个十国 Regime 独立并存（同期并行，见 FIVE_DYNASTIES_REGIME_REVIEW.md）；
后周征南唐 = 后周+南唐 双政权并列。

## 13. 辽与五代并行是否正确

**是**：regime-liao 与五代并行；契丹建国（916）/燕云十六州割让（936-938 后晋×辽）/
契丹灭后晋+辽国号（946-947 辽×后晋）事件均双政权表达。

## 14. Existing 安史 Event 是否全部复用

**是**：9/9 原样复用（quality_status=reviewed），无 event-anlu-*-v2/-new 重复（§20/§21；
安史不另建 aggregate，沿用 Story + 既有事件链）。

## 15. Duplicate

**0**（qa --report 0 候选；§48 语义近邻：唐朝建立/李渊称帝、唐统一/虎牢、
武则天称帝/武周建立、神龙政变/中宗复位、唐亡/后梁建立、后唐建立/后梁亡等均按
"行动+outcome 合一"处理）。

## 16. Broken Ref

**0**（阶段提交跨阶段关系剥离→落位恢复，最终态无 dangling ref）。

## 17. Invalid Date

**0**（早期 1 处 start>end 与 45 处 relation 参数顺序错误已修复；大运河按 605-610 range 分期，非单日）。

## 18. Source Coverage

88/88 新增：`source_reference`（古代史料：隋书/旧唐书/新唐书/资治通鉴/旧五代史/新五代史/辽史/后汉书等
＋现代参考：岑仲勉《隋唐史》、吴宗国《隋唐五代简史》、陈寅恪《唐代政治史述论稿》、
黄永年《六至九世纪中国政治史》、王仲荦《隋唐五代史》等）＋ source_ids 100%；AI 未作事实来源。

## 19. Timeline Gap

隋/唐/五代十国 coverage_gap = **0**（主时间线 589→904→907→…→959 无异常空档；
唐：618→626→630→…→763→875→904；五代：907→923→936→947→951→954→959）。

## 20. Validation

`history-data backbone validate` → **OK**（0 errors）；build gate 通过。

## 21. Tests

**84 passed**（新增 12 个 Batch4 测试 test_backbone_batch4.py：
baseline/隋统一复用/安史复用/无安史重复/唐建/武周 Regime/唐亡/五代序列/十国并行/辽并行/source/timeline）。

## 22. 全库 Event 总数

**355**（Period 31 / Regime 53 / Story 3 / EventRelation 622 / Works 26）。

## 23. 全库 Regime 总数

**53**。

## 24. Timeline 最早 / 最晚

- dist/json/china_history_major_timeline.json（354 条 critical+major）：
  最早 **前 2070**（夏朝建立）、最晚 **956**（后周征南唐，五代段终点 959 前）；
- Batch4 关键链：589 隋统一 → 604 杨广即位 → 618 唐建立 → 626 玄武门 → 630 灭东突厥 →
  690 武周 → 705 神龙政变 → 755 安禄山起兵 → 763 安史平定 → 875+ 黄巢 → 907 唐亡/后梁 →
  923 后唐 → 936 后晋 → 947 后汉 → 951 后周 → 后周改革（§56 目标链全部实现）。

---

## 下一批建议（Batch 5，本批不执行）

- 北宋（陈桥兵变 960）＋ 辽（已有 Regime，宋代深化）＋ 西夏 ＋ 金 ＋ 靖康之变 ＋ 南宋；
  本批按 §59 已停止，未进入宋（test_sui_unification_boundary 已更新为校验 Batch5 边界）。