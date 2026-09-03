# CHINA_HISTORY_BACKBONE BATCH2_SUMMARY

> China History Backbone V1 · Batch 2（秦 → 西汉 → 新 → 东汉）完成总结。
> 数据版本：2026.09.0；完成时间：2026-09-03。

## 结论先行

```text
QIN_HAN_BACKBONE_READY = true
```

满足 §55 Gate：秦/西汉/新/东汉均有 Backbone，Critical+Major 时间线连续可理解，
已有楚汉 Event 与黄巾 Event 成功复用，Duplicate=0 / Broken Ref=0 / Invalid Date=0 /
Source Missing=0 / Validation OK / Tests 全部通过。

---

## 1. 本批新增 Event 总数

**70**（秦 12 + 西汉 38 + 新 6 + 东汉 14）

## 2. 秦 Event 数

**14**（含既有 巨鹿之战/秦末起义 复用：19 在 qin_han 目录；本批新增 12，
另复用 Chunqiu_zhanguo 秦统一系列——event-qin-tongyi + event-qin-mie-liuguo 及 7 子事件）

本批新增秦节点：秦推行郡县制 / 书同文 / 统一度量衡 / 统一货币 / 修建驰道 / 北击匈奴 /
修筑长城 / 南征百越 / 秦始皇去世 / 沙丘政变（胡亥即位/赵高） / 陈胜吴广起义（part_of 秦末起义）/
刘邦入关。

## 3. 西汉 Event 数

**38 新增**（含 楚汉战争 aggregate）：郡国与和亲（定都长安/白登之围/汉匈和亲/剪除异姓王/
白马之盟）、吕后朝（刘邦去世/吕后临朝/诛诸吕/文帝即位）、文景（文景之治(标注后世概括)/
晁错削藩/七国之乱）、武帝（即位/推恩令/汉匈战争aggregate 5 战役/张骞两度出使/财政集权/
刺史/太初改历/董仲舒对策/五经博士/巫蛊之祸/轮台诏）、昭宣（武帝去世霍光辅政/昌邑王废立/
霍氏覆灭/西域都护）、后期（元帝即位/王凤辅政/王莽复出/王莽居摄）。

## 4. 新 Event 数

**6**：王莽称帝新朝建立 / 王莽改制 / 绿林起义 / 赤眉起义 / 昆阳之战 / 新朝灭亡。

## 5. 东汉 Event 数

**14 新增**：刘秀称帝东汉建立 / 光武统一战争 / 光武帝度田 / 汉明帝即位 / 佛教传入(approximate)/
班超经营西域 / 窦宪北伐(燕然勒石) / 和帝诛灭窦氏 / 邓太后临朝 / 宦官拥立汉顺帝 / 梁冀专权 /
汉羌战争 / 第一次党锢之祸 / 第二次党锢之祸；并以既有 `event-three-yellow-turbans`（黄巾起义 184）
作为主干结束节点（复用，非新建）。

## 6. Critical 数（本批新增）

**5**：七国之乱 / 漠北之战（汉武帝对匈奴战争转折）/ 王莽称帝新朝建立 / 新朝灭亡 / 刘秀称帝东汉建立。
（全库 critical 现共 **12**：Batch1 7 + Batch2 5。）

## 7. Major 数（本批新增）

**65**（全库 major 165）。

## 8. Aggregate Event 数（本批相关）

- 新增：`event-chuhan-war`（楚汉战争，4 子）、`event-han-xiongnu-war`（汉武帝对匈奴战争，5 子）；
- 复用为父：`event-chuhan-qin-revolt`（秦末起义，新增 2 子：陈胜吴广/刘邦入关）；
- 全库 aggregate 现共 10 个（含 Batch1 秦灭六国等）。
- 均通过既有 Schema 的 `part_of` 表达，未修改 Schema。

## 9. existing Event 复用数量

- 楚汉 Story：**9** 个既有 Event 全部复用（event-chuhan-*），仅给 鸿门宴/彭城/荥阳/垓下
  补充 `part_of → 楚汉战争` 关系；
- 秦统一系列：**8** 个既有 Event 复用（秦灭六国 aggregate + 7 子事件 + 秦统一）——0 重复建档；
- 黄巾起义：**1** 个既有 Event 复用（event-three-yellow-turbans）；
- 合计复用既有 Event **18** 个。

## 10. 是否产生重复 Event

**否。**
- 秦统一/秦统一六国/秦灭六国 语义近邻核对：唯一建档（Chunqiu_zhanguo）；
- 王莽代汉/新朝建立/王莽称帝：居摄→称帝 两级推进，无混用重复；
- 无 `event-hongmen-2` / `event-julu-new` 式后缀重复；
- 黄巾起义仅 1 个；
- 党锢一/党锢二为 §26 规定分列（qa duplicate 检测器已识别“第X次”枚举系列，报告 0 候选）。

## 11. Source Coverage

- 70/70 新 Event：100% `source_reference`（**古代史料 + 现代参考**两层链）+ `source_ids`；
- 古代史料：史记 / 汉书 / 后汉书 / 资治通鉴；现代参考：林剑鸣《秦史稿》、翦伯赞《秦汉史》、
  吕思勉《秦汉史》、田余庆《秦汉魏晋史探微》、张岂之主编《中国历史·秦汉魏晋南北朝卷》、
  白寿彝《中国通史》；
- 未使用 AI 作为历史事实来源（测试强制校验）。

## 12. approximate/range 数（本批）

- `approximate`：**2**（董仲舒对策 -140~-134；佛教传入 67——两者为年代有争议/传统说法节点）
- `range`：**23**（过程/政策跨度节点）
- `year`：**45**（秦汉纪年总体可靠，仅过程节点用 range/approximate）

## 13. Validation

```text
history-data backbone validate → Validation OK（0 errors）
Broken Ref = 0 / Duplicate ID = 0 / Invalid Date = 0 / Source Missing = 0
```

（每阶段批次 build gate 均通过；“王莽居摄→王莽称帝”等跨阶段关系在目标事件落位批次中恢复，
最终态与每阶段提交态均无 dangling ref。）

## 14. QA

- `backbone qa --report`：duplicate 候选 **0**；秦/西汉/新/东汉 coverage_gap **0**；
- `reports/QIN_HAN_BACKBONE_REVIEW.md`：Duplicate/Granularity/Aggregate/Gap/UncertainDates/
  ContestedInterpretations 六节（§48/§49），并记录：罢黜百家系年二说、西域都护设置时间、
  佛教传入口径、汉羌战争分期、昌邑废立解读差异等争议点。

## 15. Tests

```text
pytest → 60 passed
```

新增 Batch2 测试（§51）：test_qin_han_backbone_baseline / test_qin_han_event_ids_unique /
test_qin_han_period_refs / test_qin_han_timeline_order / test_existing_chu_han_events_reused /
test_huangjin_event_reused / test_qin_unification_no_duplicate / test_qin_han_source_coverage。
全库计数：事件 108→178、关系 175→297（测试逐阶段更新）。

## 16. Timeline 最早 / 最晚

- 全库主时间线（dist/json/china_history_major_timeline.json，177 条 critical+major）：
  最早 **前 2070**（夏朝建立）、最晚 **763**（安史之乱平定）；
- 秦汉段：**前 221**（秦推行郡县制；同年 秦统一）→ **184**（黄巾起义）；
- 查询验证（§45）：
  `backbone timeline --period qin`（14 条）/ `--period western-han`（44 条）/
  `--period xin`（6 条）/ `--period eastern-han`（含 late-eastern-han 的 7 条黄巾段）均可用。

## 17. 秦→东汉是否连续

**是。** 秦统一(-221)→郡县制(-221)→…→沙丘政变(-210)→陈胜吴广(-209)→巨鹿(-207)（复用）→
秦亡(-206)（复用）→楚汉战争(-206~-202)→汉建立(-202)（复用）→…→王莽居摄(6)→王莽称帝(9)→
改制(9)→绿林(17)→赤眉(18)→昆阳(23)→新亡(23)→刘秀称帝(25)→…→党锢二(169)→黄巾(184)（复用），
critical/major 主干逐节点相接，无异常空档。

## 18. 当前全库 Event 数

**178**（Period 31 / Regime 31 / Story 3 / EventRelation 297 / Works 13；dist/history.duckdb 已重建）。

---

## 下一批建议（Batch 3，本批不执行）

- 东汉末（董卓进京，189）→ 三国（复用三国 Story 8 Event）→ 西晋 → 东晋/十六国 → 南北朝：
  - 董卓进京为 Batch3 起点，本批未建；
  - 三国 Story 8 个既有 Event 可继续复用（官渡/赤壁/夷陵等），与 Batch2 黄巾(184) 无缝衔接。