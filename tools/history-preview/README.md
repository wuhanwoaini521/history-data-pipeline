# History Data Product — 只读校验查看器 (tools/history-preview)

一个**纯只读**的 Backbone 数据产品验收查看器。它**不连接、不写入**任何数据源——只读取
`dist/history.duckdb`（Backbone 构建产物），把统计与逐条记录导出为静态 JSON，前端用
**零依赖原生 JavaScript** 渲染。

> **Gate: `HISTORY_DATA_PRODUCT_VALIDATION_READY = true`**

---

## 1. 用途

- 校验 **Backbone linked data**（基础层）而非知识库原始体量（3rd party 收录只能了解体量，
  **不作为验收证据**）。
- 按部查看 15 个代表事件（武王伐纣 → 新中国成立）并逐条"可用 / 数据不足 / 待验收"。
- 验证 **Period ≠ Regime** 设计（三国=魏蜀吴、北宋+辽、南宋+金、五代十国等）。
- 查看每事件的**全字段**细节（人物、地点、证据、关系、Source、原始 JSON）。

## 快速开始

```bash
cd tools/history-preview
python -m http.server 8080
# 浏览器打开 http://localhost:8080/
```

> 不需要任何 npm / build 步骤；前端为原生 ES (ES2020+)，直接经 HTTP 读取
> `data/*.json`。务必经由 HTTP 服务访问（`file://` 下 fetch 会被浏览器阻止）。

### 重新生成数据（只读跑批）

```bash
python tools/history-preview/build_preview.py
```

脚本只做三件事：
1. 以 `read_only=True` 打开 `dist/history.duckdb`，导出 `data/*.json`；
2. 生成自动报告 `reports/HISTORY_DATA_PRODUCT_VALIDATION.md` 与
   `reports/HISTORY_PRODUCT_DATA_ANOMALIES.md`（同时在 `data/report_*.md` 放一份，
   供前端「自动报告」页展示）；
3. **不修改任何 `data/*` 下的 Backbone/重构数据，不改写 `dist/`，不触碰 History 前端。**

## 数据资产 (data/)

| 文件 | 内容 |
| --- | --- |
| `overview.json` | 总览：Backbone vs Knowledge Store 分开、Gates、时间跨度 |
| `events.json` | 618 个事件全字段（含 persons/places/evidences/relations…） |
| `people.json` | 234 个唯一人物（CBDB / CText / Curated Supplemental） |
| `relations.json` | 1062 条 EventRelation（只读引用） |
| `periods.json` | 31 个时期 |
| `regimes.json` / `regime_tree.json` | 64 个政权，按时期分组（多政权并存） |
| `samples.json` | 15 个验收样本引用（`id` + 数组 `index`） |
| `timeline.json` | 每 100 年 / 每时期事件密度 |
| `completeness.json` | 按优先级覆盖统计、类型/来源分布 |
| `person_linking.json` | 人物关联统计 + Top 30 人物 + 有题事件 Top |
| `report_validation.md` / `report_anomalies.md` | 自动报告（见「自动报告」页） |

## 页面

- **总览**：全局 618 / Critical 62 / Major 555 / Normal 1 / Periods 31 / Regimes 64 /
  EventPerson 398（234 唯一人物）。Backbone 与 Knowledge Store **分开两表**。
- **事件时间线**：前2070 → 1949；支持「时期」与「Critical/Major/Normal」筛选 + 名称/摘要搜索；
  点行弹出全字段详情（含原始 JSON）。
- **15 验收样本**：左列列表 / 右侧详情快速切换；验收结论只存浏览器 `localStorage`，
  **不写回数据**（默认 pending）。
- **人物关联**：来源类型徽章 CBDB / CText / Curated Supplemental，Top 30 人物、
  事件-人物统计。
- **政权视图**：按时期分组的 Regimes；多政权并存期（三国、宋辽金、明后期等）以紫框标识。
- **完整性**：按优先级覆盖统计（人/地/证据/关系/source）、时期分布、每百年密度。
- **自动报告**：直接展示两份 auto-generated 报告全文。

## 人物来源类型

| 前缀 | 显示 | 说明 |
| --- | --- | --- |
| `cbdb-person-…` | CBDB | 来源数据库 CBDB（中国历代人物传记资料库） |
| `cbdb-person-…` | Person (CBDB) | 仍在 CBDB 前缀下，统一归类为 CBDB 人物 |
| `ctext-person-…` | CText | 中文基督文献库人物 |
| `curated-person-…` | Curated Supplemental | 人工补录（V2.1.1/V2.2/V2.3 补全），带独立 review 记录 |

> 所有人物显示其 `person_id`（可回溯到 `people` / 原 YAML 权责链）。Curated 补全仅在
> 有 ≥1 主来源 + ≥1 独立来源时添加；身份仅确定性匹配（无歧义）。详见
> `reports/PERSON_LINKING_V1_FINAL_SUMMARY.md`。

## Gates

| Gate | 值 |
| --- | --- |
| `CHINA_HISTORY_BACKBONE_V1_FROZEN` | `True` |
| `PERSON_LINKING_V1_READY` | `True` |
| `HISTORY_DATA_PRODUCT_VALIDATION_READY` | `True` |

## 约束 / 只读承诺

- ✅ 只读 `dist/history.duckdb`（`read_only=True`），绝不 `INSERT/UPDATE/DELETE`。
- ✅ 不修改 `data/…` 任何 Backbone/重构/候选文件，不影响 history-data-pipeline 主流程。
- ✅ 不修改 `self-tools` 的 History UI。
- ✅ 前端原生 JS，无新依赖；验收结论只存 localStorage。
- ⚠ 异常报告（如 `background` 全空、`result` 592 空、237 无 regime）**只报告不修复**，
  由后续 Backbone V3 阶段另行处理。

## 验收流程建议

1. `cd tools/history-preview && python -m http.server 8080`
2. 先看「总览」确认 Backbone 统计一致。
3. 进「事件时间线」→ 逐条点击验收，或直接用「15 验收样本」快速通道。
4. 每个样本点"✓ 可用 / ✗ 数据不足 / ⏳ 待验收"（仅存浏览器）。
5. 浏览器刷新后结论仍在（localStorage），无 `server` 状态（READ ONLY）。