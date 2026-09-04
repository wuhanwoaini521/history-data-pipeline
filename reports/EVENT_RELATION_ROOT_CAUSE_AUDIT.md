# EVENT_RELATION_ROOT_CAUSE_AUDIT — 赤壁之战跨时代 Relation 根因审计

> 生成时间: 2026-09-04
> 触发: Viewer 显示 `护法运动 → 赤壁之战 → 府院之争`（均为 1917 民国事件）
> 模式: 先调查后修改 · 全程逐层只读追溯 · 最小修复

## 0. 冻结状态

- HEAD: `5cb1e386d098e0974dd436bfec521d2c29d49b3e`
- 审计开始时工作区仅 3 个「报告时间戳」文件有变更（`reports/HISTORY_DATA_PRODUCT_VALIDATION.md`、
  `tools/history-preview/data/overview.json`、`tools/history-preview/data/report_validation.md`），
  diff 只涉及 `generated_at` 时间戳，无数据内容变化。
- 冻结计数（manifest + dist DB）:
  - Events = 618
  - EventRelation = 1062
  - EventPerson = 398
- 本任务未修改任何 `data/curated/history_backbone/events/` 或 `event_person/` 文件。

---

## 1. 赤壁 Curated Relation 是什么（真实数据）

`data/curated/history_backbone/events/three_kingdoms/event-three-chibi.yml`:

```yaml
relations:
- target_event_id: event-three-regime-formation
  relation_type: leads_to
  confidence: 0.85
```

`data/curated/history_backbone/events/three_kingdoms/event-three-sun-liu-alliance.yml`:

```yaml
relations:
- target_event_id: event-three-chibi
  relation_type: leads_to
  confidence: 0.9
```

**Curated = 干净。** 全仓 grep 无任何 `event-three-chibi` 与民国事件的关系。

---

## 2. 赤壁 DuckDB EventRelation （JOIN 后）

| source id | source name | year | rel | target id | target name | year |
| --- | --- | ---: | --- | --- | --- | ---: |
| event-three-sun-liu-alliance | 孙刘联盟 | 208 | leads_to | event-three-chibi | 赤壁之战 | 208 |
| event-three-chibi | 赤壁之战 | 208 | leads_to | event-three-regime-formation | 三国鼎立格局逐渐形成 | 220 |

`event_relations` 表结构：`source_event_id / target_event_id` 为 VARCHAR canonical id。
赤壁无民国连接。

**DUCKDB_RELATION_CORRUPTED = false**（DuckDB 干净）

---

## 3. Preview JSON 为什么出现 573 / 574（根因）

在 `tools/history-preview/build_preview.py`（修复前）：

```python
idx_of = {e["id"]: i for i, e in enumerate(events)}               # ① 排序前编号
for r in relations:
    events[idx_of[s]]["relations_out"].append({"target": idx_of[t], ...})  # ② 写入「排序前序号」
    events[idx_of[t]]["relations_in" ].append({"source": idx_of[s], ...})
...
events.sort(key=lambda e: (e["start"] is None, e["start"] or 0))  # ③ 排序（重排数组！）
idx_of = {e["id"]: i for i, e in enumerate(events)}               # ④ 重算（已无关系引用）
```

复现（预排序 enumerate）：
- `event-three-regime-formation` 在**排序前** enumerate = **573** → 被写入 chibi `relations_out.target`
- `event-three-sun-liu-alliance` 在**排序前** enumerate = **574** → 被写入 chibi `relations_in.source`

排序后（按 start 升序）：
- `events[573]` = **府院之争**（1917）
- `events[574]` = **护法运动**（1917）

Viewer `app.js` 旧逻辑 `DATA.events[r.source]` 按数组下标取 → 渲染出
`护法运动 → 赤壁之战 → 府院之争`。

**573/574 是「排序前的 enumerate 数组下标」，不是 surrogate id、不是 DB row id、
不是 relation 表内部 id、不是 event id。** BUG 首次出现在 `build_preview.py` 的关系导出循环
（保存在正确 canonical id 的步骤里误用了 `idx_of[...]`）。

---

## 4. ID Mapping Trace（全链路）

```
Curated event id         event-three-chibi（canonical）
↓
DuckDB event pk          event-three-chibi（VARCHAR canonical）
↓
DuckDB relation 字段     source_event_id / target_event_id（canonical）
↓
Preview exporter 中间值  idx_of[t] = 574 / idx_of[s] = 573   ← BUG 在这里（数组下标）
↓
JSON relations_in/out    574 / 573（raw JSON 原样输出，数值已错）
↓
Viewer resolved event    574 → 护法运动(1917) / 573 → 府院之争(1917)   ← 跨时代显示
```

**首次出现的层级：** `tools/history-preview/build_preview.py`（Preview Exporter）。
`app.js` Viewer 也有设计缺陷（依赖数组下标），但根因在 exporter。

→ **PREVIEW_RELATION_MAPPING_BUG = true**
→ **Backbone / DuckDB 未受污染** → 1062 条 Relation 无需重建。

---

## 5. 修复

1. **build_preview.py**：关系导出改为直接使用 canonical event_id
   ```python
   events_by_id[s]["relations_out"].append({"target": t, "rel": r["rel"]})
   events_by_id[t]["relations_in"].append({"source": s, "rel": r["rel"]})
   ```
   即使在 `events.sort()` 之后仍可稳定解析，不再依赖排序前/后的数组下标。

2. **app.js**: `relationHTML` 及其他数组下标引用改为通过 `DATA.eventsById[canonical_id]` 解析；
   samples 详情改用 `eventsById[s.id]`；同时完成 #19/#20 的展示文案分离
   （「数据来源 / Provenance」与「史料线索 / Historical Evidence」两段标题，
   EventEvidence 缺省时提示「正式原文证据尚未建立」而不是生硬“无 EventEvidence”）。

3. 重新运行 `tools/history-preview/build_preview.py` 生成 JSON。

---

## 6. 全量 QA（12–14, 16 节）

对 dist/history.duckdb 全部 1062 条 EventRelation 只读检查：

| 检查 | 结果 |
| --- | --- |
| source 存在 | 0 dangling |
| target 存在 | 0 dangling |
| source == target | 0 |
| duplicate (s,t,type) | 0 |
| >500 年强语义 gap | 0 |
| >100 年强语义 gap | 6（先秦跨度，如 夏—商 470y，semantic 合理） |
| backward (target.start < source.end) | 62（多为 year 精度 ±1~2；个别语义反向如 `崖山海战1279→宋蒙战争1235`） |
| period 交叉 | 104（全部为合法跨 period 边界，如 晚汉→三国、明清、宋辽并存等，无跨时代乱指） |

**审计信号（不自动删除）**: suspicious backward 62 / cross-period 104 /
大量跨度高—— 详细清单在 QA 已生成，全量浏览。

---

## 8. 10 样本重新检查（从已修复 preview JSON 逐条验证）

| 事件 | year | incoming（前序来源） | outgoing（后继去向） | 状态 |
| --- | ---: | --- | --- | --- |
| 赤壁之战 | 208 | 孙刘联盟(208) | 三国鼎立格局逐渐形成(220) | ✅ |
| 玄武门之变 | 626 | 李世民即位(626)、唐统一全国(618) | 李世民即位(626) | ✅ |
| 安禄山起兵(安史) | 755 | 安禄山兼领三镇(751)、杨国忠执政(752) | 洛阳失守(756) | ✅ |
| 靖康之变 | 1127 | 金军第二次围攻开封(1126)、赵构称帝南宋建立(1127) | 金军二次围开封(1126)、赵构称帝(1127) | ✅ |
| 崖山海战 | 1279 | 元军陷临安(1275)、宋蒙战争(1276)、文天祥抗元(1276) | 临安降(1275)、文天祥(1276)、宋蒙战争(1235) | ✅ |
| 土木堡之变 | 1449 | 景泰帝即位(1449)、迁都北京(1421) | 迁都北京(1421)、景泰帝即位(1449)、北京保卫战(1449) | ✅ |
| 鸦片战争 | 1840 | 林则徐禁烟(1838)、太平天国(1842)、鸦片战争(1856) | 林则徐禁烟(1838)、定海条约(1842) | ✅ |
| 武昌起义 | 1911 | 孙临时政府(1912)、清帝退位(1912)、同盟会(1905)、保路(1911) | 保路(1911)、同盟会(1905)、孙临时政府(1912) | ✅ |
| 九一八事变 | 1931 | 满洲国(1932)、一二八变(1932) | 东北易帜(1928)、满洲国(1932) | ✅ |
| 建国 | 1949 | 渡江战役(1949) | 渡江战役(1949) | ✅ |

**EVENT_RELATION_SAMPLE_VALIDATION = PASS** —— 无跨时代串台；两端同代/合法边界。

> 数据语义瑕疵（不做自动修复，仅列入 QA 审计）：`event-yanya-haizhan[1279]` 以
> `follows` 连到 `event-song-meng-zhanzheng[1235]` 方向存疑；全库另有 62 条 backward
> （多为年份 ±1~2）待人工审阅，均不影响本任务结论。

---

## 9. 测试

新增 `tests/test_preview_relations.py`：

- `test_preview_relation_uses_canonical_event_id`
- `test_chibi_relation_not_republican`
- `test_relation_source_target_exist`
- `test_relation_no_surrogate_id_export`
- `test_relation_cross_era_audit`
- `test_preview_source_and_historical_evidence_separated`

**全部通过，全量回归 `170 passed`（基线 164 + 新增 6），Events=618 / EventPerson=398 不变。**

---

## 10. 报告问答（23 节）

| # | 问题 | 回答 |
|---|------|------|
| 1 | 赤壁 Curated Relation | `孙刘联盟(208)→赤壁→三国鼎立(220)`，正确 |
| 2 | 赤壁 DuckDB Relation | 同上，canonical id，正确 |
| 3 | Preview 为什么 573/574 | `build_preview.py` 用排序前 `enumerate` 序号（idx_of）写入关系 target/source |
| 4 | BUG 首次出现层 | **build_preview.py**（Preview Exporter） |
| 5 | Backbone 污染 | 否 |
| 6 | DuckDB 污染 | 否 |
| 7 | Preview 污染 | 是（已修复） |
| 8 | 1062 Relation 重建 | **不需要** |
| 9 | 跨时代异常数 | >100y gap 6（合理）、>500y 0 |
| 10 | Broken Relation 数 | 0 |
| 11 | Duplicate Relation 数 | 0 |
| 12 | 影响 V1 Freeze | 否（冻结点的数据本身没坏） |

---

## 最终结论

```
RELATION_DATA_HEALTHY = true
PREVIEW_RELATION_BUG_FIXED = true
```

即「方案 A」：Backbone 与 DuckDB 关系数据完全健康，纯粹是 Preview 导出/Viewer
把「数组下标」当成了实体引用（并在排序后错位），导致赤壁被渲染成连到 1917 的假象。
已修复 build_preview.py + app.js，重新生成数据，新增 6 项回归测试，全部通过。

按任务约定停止：不进行 Place / Story / UI 正式开发，等待用户重新打开 Viewer 验收。