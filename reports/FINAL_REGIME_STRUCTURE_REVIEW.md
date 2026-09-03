# FINAL_REGIME_STRUCTURE_REVIEW

> China History Backbone V1 · 全库 Regime 并行结构审计（§72）。
> 重点：三国 / 东晋十六国 / 南北朝 / 五代十国 / 宋辽夏金 / 南宋金蒙古 的并行表达。

## 全库 Regime：64 个，全部独立行 + 继承链

| 结构域 | 并行表达方式 |
|---|---|
| 三国 | regime-cao-wei / shu-han / eastern-wu 三行并列（Period=three-kingdoms） |
| 东晋十六国 | regime-eastern-jin（南朝侧）+ 前赵后赵前燕前秦后秦后燕北凉 7 政权并列（十六国只建主线 7 政权，克制） |
| 南北朝 | 北魏（含东魏西魏 parent）+ 东魏/西魏/北齐/北周 parent 链；南朝 宋齐梁陈 并行 |
| 五代十国 | 后梁后唐后晋后汉后周（中原更替链，事件表达）+ 十国 10 行独立并存（吴/南唐/吴越/楚/闽/前蜀/后蜀/南汉/荆南/北汉）+ 契丹/辽并行 |
| 宋辽夏金 | regime-northern-song ∥ regime-liao ∥ regime-western-xia（979-1125）；regime-southern-song ∥ regime-jin（1127-1234） |
| 南宋金蒙古 | regime-southern-song ∥ regime-jin ∥ regime-mongol-empire（1206-1234）；regime-southern-song ∥ regime-yuan（1271-1279） |

## 关键约束验证

| 检查 | 结果 |
|---|---|
| 禁止"北宋→辽→西夏→金→南宋→元"串行 | ✅ 各政权独立 Regime 行 + 双政权事件（高梁河=宋×辽、三川口=夏×宋、采石=宋×金、崖山=元×宋） |
| 1206 大蒙古国 ≠ 1271 元 | ✅ regime-mongol-empire(1206-1271) 独立；regime-yuan 挂 parent_regime_id=regime-mongol-empire；测试强制 1271 前已结束事件不得挂 regime-yuan |
| 继承 vs 并行区分 | ✅ parent_regime_id 仅用于真正继承：东魏→北齐、西魏→北周、大蒙古国→元、后金→清；并行政权一律 regime_ids 并列 |
| 元末群雄并列 | ✅ regime-zhuzhang/dahan/dazhou/dasong + 元廷（鄱阳湖=朱×陈、灭张=朱×周） |
| 民国-满洲国 | ✅ regime-republic 与 regime-manchukuo 并列（满洲国为日本扶持傀儡政权，中立注明） |
| 武周 | ✅ regime-wu-zhou(690-705) 独立，period 仍属唐 |

## 数量

Period 31 / **Regime 64**（含 parent 链节点 5 处）。

## 无争议结论

**FINAL: Regime Structure Audit PASS。**