# Major Batch 01 · Queue 1 — Freeze Blocked Critical

> 决策：**冻结**以下 2 个 Critical，本轮不再投入 source 搜寻；状态保持合法结果，不降门槛。

| event_id | event_name | 状态 | 原因 |
|---|---|---|---|
| event-jiuyiba-shibian | 九一八事变（沈阳） | **LICENSE_BLOCKED / NEEDS_SOURCE** | 可靠 source 候选仅「中央关于日本帝国主义强占满洲事变的决议」（政党决议），是否属著作权法第 5 条「国家机关官方文件」存在解释空间；日方档案与民国档案无公开机读公版版本。**不能合法纳入 canonical corpus。** |
| event-xian-shibian | 西安事变 | **LICENSE_BLOCKED / NEEDS_SOURCE** | 首选文献（张学良、杨虎城对时局通电）维基文库无页面；张学良（卒 2001）署名文献保护期至 2052 未满；当事方回忆与档案无公开公版机读版本。 |

## 冻结规则（本轮生效）

1. 两者不进入 Major Batch 01 选择池，不参与任何 enrichment 候选。
2. 若后续出现许可明确的一手文献（如影印本进入公有领域、官方文献全文公开且许可清晰），解除冻结的路径为：
   `source acquisition（Queue 4 政策）→ parser → quality gate → evidence 锚定 → enrichment`，与常规事件完全同流程。
3. 当前状态在 ENRICHMENT_QUEUE 中仍显示为 Critical 待办——这是**如实状态**，不删除、不降级、不伪装完成（Rule 4：NEEDS_SOURCE 是合法结果）。

## Critical 汇总（冻结后）

| 指标 | 值 |
|---|---|
| critical 总数 | 62 |
| 已完成（≥90） | **60** |
| 冻结（本轮起） | 2 |
| critical 均分 | 97.8 |
