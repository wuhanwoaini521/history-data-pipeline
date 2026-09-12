# HISTORY V2 NEXT ROADMAP（只写路线，不执行）

## Next Phase A — Content Production

- 目标序列：FULL 181 → 200 → 250 → 300。
- 输入：`reports/ENRICHMENT_QUEUE.json`（READY 池）+ `DEPTH_BACKLOG_V2.json` 的 P1。
- 方法：Major 簇批量富化（复用 `scripts/major02_cluster_*` 与 `_depth_util.apply` 模式）；每簇 1 提交。

## Next Phase B — Depth

- 优先处理 **ADEQUATE_HIGH 24 个（P1）**：多数只差 1 个弱维即可 STRONG。
- 其次 **ADEQUATE_MID 36 个（P2）**：按 period 批量补锚。
- **ADEQUATE_NATURAL 34 个不进入常规队列**（避免无止境扩写）。

## Next Phase C — Source Expansion

- 优先级：清实录 → 民国文书 → 晚清档案 → 元史缺卷（顺帝纪/河渠志）→ 续资治通鉴长编 → 日本书纪。
- 入库流程：raw（immutable）→ wikisource/官方文本快照 → chapter/paragraph 解析 → knowledge build → 重跑 evidence relink（manual 锚不动）。

## Next Phase D — Product / UI

- 内容规模足够（FULL ≥200）后按序接入：Timeline → Event Detail → Related Events → Source View → Knowledge Graph → Map。
- depth_status / depth_class 为 audit-only JSON，可直接供 UI 筛选（不动 canonical schema）。

## 约束

- 任何阶段都不得破坏 DO NOT BREAK 规则（见 HISTORY_V2_HANDOFF.md）。