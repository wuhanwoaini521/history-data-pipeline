# CHINA_HISTORY_BACKBONE BATCH3_SUMMARY

> China History Backbone V1 · Batch 3（东汉末 → 三国 → 西晋 → 东晋/十六国 → 南北朝 → 隋统一）总结。
> 数据版本：2026.09.0；完成时间：2026-09-03。

## 结论先行

```text
WEI_JIN_NORTHERN_SOUTHERN_BACKBONE_READY = true
```

§60 Gate 全部满足：黄巾/三国 Story Event 复用、三国/东晋十六国/南北朝 并行 Regime 正确、
西晋统一与灭亡、淝水之战、北魏统一北方、北魏分裂、北周灭北齐、隋建立、隋灭陈均在位；
Duplicate=0 / Broken Ref=0 / Invalid Date=0 / Source Missing=0 / Validation OK / Tests 全通过。

---

## 1. 本批新增 Event 总数

**89**（Critical 13 + Major 76）

## 2. Existing Event 复用总数

**8**：event-three-yellow-turbans（184）/ event-three-dong-zhuo（189）/ event-three-guandu（200）/
event-three-north-consolidation（200—207）/ event-three-jingzhou-change（208）/
event-three-sun-liu-alliance（208）/ event-three-chibi（208）/ event-three-regime-formation（220—229）
（三国 Story 全部 8 个既有 Event 原样复用，无重复建档）

## 3—9. 各时期 New / Reused / Total

| 时期段（Period/组） | New | Reused | Total（critical+major） |
|---|---:|---:|---:|
| 东汉末（period-late-eastern-han） | 15 | 4（黄巾/董卓进京/官渡/北固，另荆州/孙刘/赤壁 208 同组） | 19+ |
| 三国（period-three-kingdoms） | 13 | 1（三国鼎立格局逐渐形成） | 14 |
| 西晋（period-western-jin） | 12 | 0 | 12 |
| 东晋（period-eastern-jin） | 8 | 0 | 8 |
| 十六国（period-sixteen-kingdoms） | 13 | 0 | 13 |
| 南北朝（period-northern-southern） | 25 | 0 | 25 |
| 隋统一阶段（period-sui） | 3 | 0 | 3 |

> 注：东汉末行"Reused"含 黄巾（184）/董卓进京（189）/官渡（200）/曹操北固（200—207）4 个既有
> critical+major 事件（208 年 荆州局势变化/孙刘联盟/赤壁 亦同组，属 7 个）；总数以
> `reports/BACKBONE_COVERAGE.md`（New/Reused/Total 列）为准。

## 10. Critical 数

本批新增 **13**：曹丕代汉/西晋统一（晋灭吴）/八王之乱/永嘉之乱/西晋灭亡/东晋建立/
淝水之战/北魏统一北方/北魏分裂/侯景之乱/北周灭北齐/隋建立/隋灭陈。
（全库 critical 现共 **25**：Batch1 7 + Batch2 5 + Batch3 13。）

## 11. Major 数

本批新增 **76**（全库 major **241**）。

## 12. Aggregate Event 数

本批新增 **5**：诸葛亮北伐（2 子）/八王之乱（3 子）/永嘉之乱（2 子）/北魏孝文帝改革（2 子）/
侯景之乱（1 子）；全库 aggregate（有 part_of 子事件）现共 15+。

## 13. Regime 总数是否变化

31 → **42**（新增 11：前赵/后赵/前燕/前秦/后秦/后燕/北凉 + 刘宋/南齐/梁/陈；
并为 东魏/西魏→北魏、北齐→东魏、北周→西魏 设置 parent_regime_id 继承链）。

## 14. 三国并行 Regime 是否正确

**是**：曹魏/蜀汉/东吴 同属 period-three-kingdoms；夷陵=蜀+吴、魏灭蜀=魏+蜀（regime_ids 并列）。

## 15. 东晋/十六国并行关系是否正确

**是**：东晋 ∥ 前赵/后赵/前燕/前秦/后燕/后秦/北凉；淝水之战=东晋+前秦、北魏灭后燕=北魏+后燕、
北魏统一=北魏+北凉；十六国仅维护主线 7 政权（未全收录）。

## 16. 南北朝并行关系是否正确

**是**：南朝（刘宋/南齐/梁/陈）∥ 北朝（北魏/东魏/西魏/北齐/北周）；钟离=梁+魏、
玉壁=东魏+西魏、北周灭北齐=周+齐；东魏∥西魏、北齐∥北周 均为并行（时间重叠），
继承由 parent_regime_id 表达（非串行 Dynasty Chain）。

## 17. Duplicate 数

**0**（qa --report 0 候选；§48 语义近邻 7 组均按"行动+outcome 合一"处理）。

## 18. Broken Ref

**0**（阶段提交采用跨阶段关系剥离→落位恢复机制，最终态与每阶段态均无 dangling ref）。

## 19. Invalid Date

**0**（1 处早期数据参数顺序错误与 1 处 start>end 已修复；date_precision 无 exact 滥用）。

## 20. Source Coverage

89/89 新增 Event：`source_reference`（古代史料 + 现代参考两层链）+ `source_ids` 100%；
正史引用含 三国志/晋书/宋书/梁书/陈书/魏书/北齐书/周书/南史/北史/资治通鉴/后汉书；
新增 10 部 works seeds（works 13→23）。AI 未作历史事实来源（测试强制）。

## 21. Timeline Gap

东汉末/三国/西晋/东晋/十六国/南北朝 coverage_gap = **0**；
全库余 gap 属 Batch1 夏商周早期与未建批 Period（如实报告，不自动补点）。

## 22. Validation

`history-data backbone validate` → **OK**（0 errors）；build gate 通过（dist 已重建）。

## 23. Tests

**72 passed**（新增 11 个 Batch3 测试文件 test_backbone_batch3.py：baseline/三国复用/黄巾复用/
官渡赤壁无重复/三国并行/东晋十六国并行/南北朝并行/北魏分裂结构/隋统一边界/source/时间线）。

## 24. 全库 Event 总数

**267**（Period 31 / Regime 42 / Story 3 / EventRelation 466 / Works 23）。

## 25. Timeline 当前最早 / 最晚年份

- dist/json/china_history_major_timeline.json（266 条 critical+major）：
  最早 **前 2070**（夏朝建立）、最晚 **763**（安史之乱平定）；
- Batch3 关键链：184 黄巾 → 189 董卓进京 → 208 赤壁 → 220 曹丕代汉 → 280 晋灭吴统一 →
  311 永嘉之乱 → 317 东晋建立 → 383 淝水之战 → 439 北魏统一北方 → 534 北魏分裂 →
  577 北周灭北齐 → 581 隋建立 → 589 隋灭陈统一（§58 目标链全部实现）。

---

## 下一批建议（Batch 4，本批不执行）

- 隋（隋炀帝/三征高句丽/隋末农民战争/李渊起兵/唐朝建立/玄武门之变/贞观/武周/开元/安史之乱扩展）
  → 唐 → 五代十国（§61 明列内容本批均未创建，测试 test_sui_unification_boundary 强制校验）。