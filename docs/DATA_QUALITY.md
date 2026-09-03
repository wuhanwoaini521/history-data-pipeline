# DATA_QUALITY

## 状态枚举（taxonomy/quality_status.yml）

`verified` / `reviewed` / `accepted` / `candidate` / `needs_review` /
`needs_linking` / `pending_knowledge` / `rejected` / `pending` / `legacy` / `deprecated`

- `candidate` 永不直接进入正式 Backbone。
- `pending_knowledge`：审核已通过但 Knowledge Store 尚未在本环境重建
  （当前迁移的 Evidence 属于此类）。
- `legacy / deprecated`：旧 Semantic Layer 数据标记，仅供审计。

## 自动规则

- **主实体 ID 唯一且不可为空**；所有桥接目标必须存在（孤引用 → 失败）。
- **Event 时间合法**：`start_year <= end_year`；早期 Period 只允许
  approximate/range。
- **Story sequence 唯一且有序**。
- **引用 Gate**：`linked` 引用必须在 Knowledge Store 中存在；
  明确链接错误的 Person/Place（如临时冲突、名称冲突）拒绝写入为 linked。
- `original_text` 非空且永远保留原文；OpenCC 只写 `original_simplified`。
- 任何合并必须有 `entity_source_mapping` + 置信度；同名不自动合并。
- `translation_zh_cn == original_simplified` 只报告分析，不自动判错。

## Validation Gate

`backbone validate` / `backbone build` 遇到以下问题**必须失败**（不是 Warning）：

```text
broken person reference      （linked 但实体缺失）
broken event reference       （Story/Relation 指向不存在的事件）
duplicate event id
invalid date                 （start > end 或非法 precision）
accepted evidence missing source（缺 work/term 依据）
孤儿关系
```

## 链接质量（Link QA）

- Person：需要 canonical ID；有生卒年时须与 Event 时间重叠；
  缺少生卒年只能 `reviewed`，不能伪装成已验证年代。
- Place：需要名称匹配与有效年代重叠；无法可靠匹配时
  `place_id=null` + `link_status=needs_linking`，不强行匹配。
- Evidence：`evidence_role = primary / supporting / related`；
  `link_quality_status` 与 `source_quality_status` 分开解释
  （候选被拒不等于来源不存在）。

运行：`history-data backbone validate --json`、`history-data backbone qa`。