# Phase Wrap-up · Q8 — History Relation Final Audit

- 关系总数：**1112**
- dangling target：**0**
- self-reference：**0**
- duplicate（同源同目标同类型）：**0**
- 无任何 relation 的事件：**5**
- 仅 1 条 relation 的事件：**174**
- ≥3 条 relation 的事件：**53**（形成历史链者）

## 类型分布

| relation_type | count |
|---|---|
| follows | 517 |
| leads_to | 295 |
| precedes | 187 |
| part_of | 99 |
| contributes_to | 5 |
| related_to | 4 |
| causes | 4 |
| caused_by | 1 |

## 结论

- 本轮未新增批量关系；仅在 Depth Sprint 02 的自然历史链上补 12 条（causes/leads_to/precedes/follows/part_of/related_to）。
- 失效目标、重复、自引用均为 0；无需修复项。
- 无关系事件 5 个（多为孤立制度/战役短事件）——**不强行补链**，留待 Source Expansion 后自然形成。