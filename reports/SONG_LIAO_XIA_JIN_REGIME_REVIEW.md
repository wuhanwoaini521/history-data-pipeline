# SONG_LIAO_XIA_JIN_REGIME_REVIEW

> 宋辽夏金多政权并行结构审查（Batch 5）。
> 回答：北宋/辽/西夏是否并行表达？南宋/金/蒙古是否并行？1206 大蒙古国与 1271 元如何区分？
> 是否出现"北宋→辽→西夏→金→南宋→元"式错误串行？

## 1. 本批涉及的 Regime（全部独立行，无错误串行）

| Regime | 年代 | Period | 说明 |
|---|---|---|---|
| regime-northern-song | 960–1127 | period-northern-song | 北宋（赵匡胤） |
| regime-liao | 916–1125 | period-liao | 辽/契丹（既有，Batch4 已用） |
| regime-western-xia | 1038–1227 | period-western-xia | 西夏（李元昊称帝） |
| regime-jin | 1115–1234 | period-jin | 金（完颜阿骨打） |
| regime-southern-song | 1127–1279 | period-southern-song | 南宋（赵构） |
| regime-mongol-empire | 1206–1271 | period-song-liao-jin | **本批新增**：大蒙古国 |
| regime-yuan | 1271–1368 | period-yuan | 元（parent_regime_id = regime-mongol-empire） |

## 2. 并行表达（三个并存时段）

| 时段 | 并存政权（Regime） |
|---|---|
| 979–1125 | 北宋 ∥ 辽 ∥（西夏自 1038 起）|
| 1127–1234 | 南宋 ∥ 金 |
| 1206–1234 | 南宋 ∥ 金 ∥ 大蒙古国 |
| 1234–1271 | 南宋 ∥ 大蒙古国 |
| 1271–1279 | 南宋 ∥ 元 |

并行以事件 `regime_ids` 并列表达：
- **高梁河之战（979）** = 宋 × 辽
- **三川口/好水川/定川寨（1040–1042）** = 夏 × 宋
- **海上之盟（1120）** = 宋 × 金
- **金灭辽（1122–1125）** = 金 × 辽
- **采石之战（1161）** = 宋 × 金
- **金灭亡·蔡州之战（1232–1234）** = 蒙古 × 金 × 南宋（三方关系一次表达）
- **崖山海战（1279）** = 元 × 南宋

## 3. 1206 大蒙古国 ≠ 1271 元

| 检查 | 结果 |
|---|---|
| regime-mongol-empire 独立存在（1206–1271，period-song-liao-jin）| ✅ |
| regime-yuan 独立存在（1271–1368，period-yuan）| ✅ |
| parent_regime_id 挂在 regime-yuan → regime-mongol-empire（继承而非串行）| ✅ |
| event-mongol-jianguo（1206）挂 regime-mongol-empire，period-song-liao-jin | ✅ |
| event-yuan-jianguo（1271）挂 regime-yuan，period-yuan | ✅ |
| 整体结束于 1270 年前的事件不挂 regime-yuan（测试强制）| ✅（襄樊 1267–1273 跨 1271 为例外）|

## 4. 王朝转换用事件链而非 Regime parent 链

五代→宋转换不是 parent 链：
- event-chenqiao-bingbian `follows event-guo-wei-dai-han`（951 后周 → 960 北宋）
- 靖康之变 → 赵构称帝（北宋亡 → 南宋建，follows）
- 金灭辽 → 第一次围开封（leads_to）→ 靖康之变（leads_to）

## 5. 检查项清单

| 检查 | 结果 |
|---|---|
| 是否用 parent_regime_id 表达并行政权 | 否（parent 仅用于继承：北魏分裂系、蒙古→元）|
| 是否把五代做进宋的链 | 否（宋辽夏金期间五代已结束；951 后周仅作 960 前节点被引用）|
| 是否"1206 之后全部 regime-yuan" | 否（regime-mongol-empire + 测试强制）|
| 三大并存时段是否都有双政权事件佐证 | 是（见 §2）|
| schema 是否改动 | 否 |

## 6. 说明

- Regime 53 → **54**（仅新增 regime-mongol-empire；辽/西夏/金/宋/元均为既有种子行）。
- events 目录：`events/song_liao_xia_jin/`（宋辽夏金/南宋/蒙古 pre-元），`events/yuan/`（1271 元建立边界节点）。
- 蒙古帝国与元的关系在《元朝史》（韩儒林）等现代研究框架下表达为同一政治体的两个阶段（国号沿革），
  本库以两个 Regime 行 + 事件链记录，不作价值判断。