# CHINA_HISTORY_BACKBONE BATCH1_SUMMARY

> China History Backbone V1 · Batch 1（先秦）完成总结。
> 数据版本：2026.09.0；完成时间：2026-09-03。

## 结论先行

```text
PRE_QIN_BACKBONE_READY = true
```

先秦 Backbone（上古/夏/商/西周/春秋/战国）已形成连续 Critical/Major 主时间线，
Validation / Build / Tests / Coverage 全部通过，可进入下一批（秦汉）。

---

## 1. 新增 Event 数

| 时期文件目录 | Phase | 新增 |
|---|---:|---:|
| `events/pre_qin/` | A：夏 / 商 / 西周 | 21 |
| `events/chunqiu_zhanguo/` | B：春秋（含吴越争霸收尾） | 26 |
| `events/chunqiu_zhanguo/` | C：战国 | 35 |
| **合计**（本批新增） | | **82** |

全库 Event：26（既有迁移）→ **108**。

## 2. Critical / Major 数（本批）

- Critical：**7**（商汤灭夏 / 武王伐纣 / 平王东迁 / 三家分晋 / 长平之战 / 秦灭六国 / 秦统一）
- Major：**75**
- 本批不引入 normal/minor（V1 主干只维护 critical + major）。

## 3. 各 Period Event 数（本批）

| Period | Critical | Major | Total |
|---|---:|---:|---:|
| 夏 | 1 | 3 | 4 |
| 商 | 1 | 3 | 4 |
| 西周 | 0 | 13 | 13 |
| 春秋 | 1 | 23 | 24 |
| 战国 | 4 | 33 | 37 |
| 先秦 | 7 | 75 | 82 |

> 口径说明：越灭吴（前 473）、三家灭智（前 453）、三家分晋（前 403）按仓库 taxonomy
> （战国起始前 475 年）归入战国；传统《春秋》叙事口径差异见
> `reports/EARLY_HISTORY_UNCERTAINTY.md`。

## 4. approximate Event 数

- `date_precision = approximate`：**24**
- `range`（多为治世/过程节点约略区间）：**20**
- 前 1000 年以前的节点一律 approximate/range（测试强制校验），未伪装精确纪年。

## 5. Source Coverage

- 82/82 Event 具有 `source_reference`（**古代史料 + 现代参考**两层链）；
- 82/82 具有 `source_ids`（work 种子，先秦典籍：史记/左传/国语/尚书/竹书纪年/战国策/春秋/资治通鉴）；
- 现代参考：断代工程《简本》、杨宽《战国史》、童书业《春秋史》、许倬云《西周史》、
  张岂之主编《中国历史·先秦卷》、白寿彝《中国通史》。
- 按“Event First, Evidence Later”（§11/§13）：本批不携带 evidence/HistoricalText 关联，
  也不强绑 person/place；Evidence Linking 作为单独阶段在 Backbone 完成后执行。

## 6. Duplicate 检查结果

- `history-data backbone qa --report` → reports/BACKBONE_REVIEW.md：
  - 未发现未解释的疑似重复/上下层事件候选（0 组）；
  - 秦灭六国下的 秦灭韩/赵/燕/魏/楚/齐 为已用 `part_of` 结构解释的姊妹子事件，不计入候选；
  - 发现的“候选对”均按人工 review 结论保持独立（不自动合并，符合 §21）。

## 7. Validation 结果

```text
history-data backbone validate  →  Validation OK（0 errors）
Broken Ref    = 0
Duplicate ID  = 0
Invalid Date  = 0
Source Missing= 0
Reference Integration broken = 0
```

## 8. Tests 结果

```text
pytest → 52 passed
```

本轮测试变更（均为适配性调整，已随本批提交）：
- `test_backbone_loads` / `test_backbone_build` / `test_manifest` / `test_exports`：事件计数 26 → 108；
- `test_event_evidence_reference`：evidence 改为**可选**（对应 §11 “Event First, Evidence Later”，
  不再强制每条 Event 携带 HistoricalText ID），已有 evidence 的规则保持严格；
- `test_raw_immutable`：环境兼容（本地已下载 gitignored 的官方快照时仍保证 raw 无构建产物）；
- 新增：先秦主干完整性基线、timeline 过滤/排序、qa duplicate/gap 校验。

## 9. 当前 Timeline 最早 / 最晚年份

- 先秦段最早：**前 2070**（夏朝建立，approximate）
- 全库主时间线（dist/json/china_history_major_timeline.json，107 条 critical+major，按 start_year 排序）：
  - 最早：前 2070（夏朝建立）
  - 最晚：763（安史之乱平定，既有隋唐批事件）

## 10. 先秦 Backbone 是否连续可用

**是。** 从夏朝建立（前2070）到秦统一（前221）的 Critical/Major 主时间线已连续，
`history-data backbone timeline --period warring` 等查询可直接消费；
`dist/json/china_history_major_timeline.json` 供 History UI 首页使用。
`reports/BACKBONE_REVIEW.md` 同时如实报告夏代中后期（约前1990→前1600）与商代早中期
（前1600→前1300）的**真实空白**（属早期史料稀疏，不自动补点，符合 §25）。

## 11. 下一批是否建议进入秦汉

**建议：是。**
- 秦汉批（`events/qin_han/` + `events/three_kingdoms/`）应**优先复用既有** 楚汉 Story（9 Event）
  与三国 Story（8 Event），补充 秦统一制度细节、汉武帝时期、王莽代汉、光武中兴、党锢之祸、黄巾起义等；
- 禁止创建 `event-hongmen-2` 式重复；新增候选仍需先入 `data/candidates/backbone_events/` 再 review；
- 秦统一（前221）与其后的 郡县/书同文/度量衡 制度事件属于秦汉批细化，本批未重复展开。

## 12. 本轮代码变更（backbone tooling，未动架构）

| 文件 | 变更 |
|---|---|
| `src/history_data_pipeline/backbone/timeline.py`（新） | `backbone timeline` 查询 + `china_history_major_timeline.json` 导出 |
| `src/history_data_pipeline/backbone/qa_report.py`（新） | duplicate / granularity / gap QA → reports/BACKBONE_REVIEW.md |
| `src/history_data_pipeline/backbone/coverage.py` | 增加按 Period 的 Critical/Major/Normal 分布表 |
| `src/history_data_pipeline/backbone/reference.py` | 增加 6 部先秦典籍 work seeds |
| `src/history_data_pipeline/backbone/build.py` | 修复知识库并入 SQL（`source.people` → ATTACH）；默认 seed-only，`--knowledge` 显式并入 |
| `src/history_data_pipeline/cli.py` | `backbone timeline` 子命令；`backbone qa --report` |
| `scripts/backbone_batch1_data.py` / `write.py`（新） | Batch1 数据源与写入器（幂等） |

架构（Layer 1/2/3/4、Knowledge Store、dist 定义、Story 数量、三个既有 Story）均未改动。