# CHINA_HISTORY_BACKBONE_V1

> China History Backbone V1 —— 从夏商周到近现代中国历史的连续重大事件主干。
> 本报告为 V1 首个里程碑（Batch 1：先秦主干）完成后的盘点。
> 数据版本：`DATA_VERSION = 2026.09.0`；生成时间：2026-09-03。

## 1. 总览（全库）

| 指标 | 数量 |
|---|---:|
| Period 总数 | 31 |
| Regime 总数 | 31 |
| Event 总数 | **618**（既有迁移 26 + Batch1 82 + Batch2 70 + Batch3 89 + Batch4 88 + Batch5 63 + Batch6 82 + Batch7 66 + Batch8 52） |
| Critical Event | 62 |
| Major Event | 555 |
| Normal Event | 1 |
| Story | 3（楚汉争霸 / 三国格局形成 / 安史之乱，不变） |
| StoryEvent | 26 |
| EventRelation | 1062 |

## 2. 里程碑

- **Batch 1（先秦）**：82 个 Event（夏4/商4/西周13/春秋24/战国37）→ `PRE_QIN_BACKBONE_READY = true`
- **Batch 2（秦汉）**：70 个 Event（秦12/西汉38/新6/东汉14）+ 楚汉战争/汉匈战争 aggregate，
  复用 楚汉9 + 秦统一系列8 + 黄巾1 → `QIN_HAN_BACKBONE_READY = true`
- **Batch 3（东汉末—隋统一）**：89 个 Event + 5 aggregate（八王之乱/永嘉之乱/诸葛亮北伐/
  孝文帝改革/侯景之乱）+ Regime 31→42（三国/东晋十六国/南北朝 并行结构落地）→
  `WEI_JIN_NORTHERN_SOUTHERN_BACKBONE_READY = true`
- **Batch 4（隋—唐—五代十国）**：88 个 Event（隋21/初唐12/高宗武周10/开元天宝安史9/中晚唐唐末20/五代16）
  + 武周/十国 Regime（53）+ 契丹辽并行 → `SUI_TANG_FIVE_DYNASTIES_BACKBONE_READY = true`
- 最新报告：`reports/FIVE_DYNASTIES_REGIME_REVIEW.md`、`docs/CHINA_HISTORY_BACKBONE_BATCH4_SUMMARY.md`

### 本轮（Batch 1 先秦）交付

- Critical Event：**7**
- Major Event：**75**
- 合计：**82** 个先秦 Backbone Event

### 按 Period 分布

| Period | Critical | Major | 合计 |
|---|---:|---:|---:|
| 夏 | 1 | 3 | 4 |
| 商 | 1 | 3 | 4 |
| 西周 | 0 | 13 | 13 |
| 春秋 | 1 | 23 | 24 |
| 战国 | 4 | 33 | 37 |
| **先秦合计** | **7** | **75** | **82** |

### 目录组织

```text
data/curated/history_backbone/events/pre_qin/         21 个（夏/商/西周）
data/curated/history_backbone/events/chunqiu_zhanguo/ 61 个（春秋/战国）
data/candidates/backbone_events/                      候选清单（pre_qin / chunqiu_zhanguo）
data/reviews/accepted/event-*.review.json             每事件审核记录（82 份新增 + 26 份既有）
```

## 3. 质量 Gate

| 检查（history-data backbone validate / build） | 结果 |
|---|---|
| Validation | OK（0 错误） |
| Broken Reference | 0 |
| Duplicate ID | 0 |
| Invalid Date | 0 |
| Source Missing（source_reference） | 0 |
| Reference Resolution broken | 0 |
| pytest | **52 passed** |

## 4. 时间口径

- 前 841 年（共和元年）以前：一律 `date_precision: approximate / range`，不伪装精确纪年。
- 采用《夏商周断代工程》框架为默认年代（夏约 -2070、夏商分界约 -1600、盘庚迁殷约 -1300、
  武王伐纣 -1046 等），争议点记录于 `reports/EARLY_HISTORY_UNCERTAINTY.md`。
- Batch1 中 `date_precision` 分布：approximate 24 / range 20 / year 38。
- 春秋战国分界采用仓库 taxonomy 通行口径（前 475 年）；`越灭吴（前473）/三家灭智（前453）/三家分晋（前403）`
  按纪年归入战国 Period，传统《春秋》叙事口径差异在报告中说明。

## 5. Source Strategy（两层链）

每条 Event 均有：

```yaml
source_reference: "古代史料：《史记·…》《左传·…》…；现代参考：杨宽《战国史》…"
source_ids: [work-curated-shiji, ...]   # work 种子
```

- historical_source（古代史料）：史记 / 左传 / 尚书 / 国语 / 竹书纪年 / 战国策 / 春秋 / 资治通鉴 等；
- modern_reference（现代参考）：断代工程简本 / 杨宽《战国史》 / 童书业《春秋史》 / 许倬云《西周史》 /
  张岂之主编《中国历史·先秦卷》 / 白寿彝《中国通史》 等；
- 现代参考证明 Event 的名称、时间范围与历史定位，不等于 HistoricalText Evidence；
- Evidence Linking（Event → HistoricalText）按“Event First, Evidence Later”留待单独阶段。

## 6. 关系建设（克制原则）

- 本轮只建安全与有据关系：part_of（仅 秦灭六国 聚合 7 子事件等 7 个 aggregate）、
  precedes / follows、以及有来源支撑的 curated leads_to / contributes_to（少量）。
- 未生成“每相邻事件一条 leads_to”式全自动关系；未新增任何 Story。

## 7. 产出物

- `dist/history.duckdb`（Layer 4，可查询）
- `dist/json/china_history_major_timeline.json`（critical + major，按 start_year 排序，107 条）
- `dist/parquet/*.parquet` + `dist/json/*.json` + `dist/manifest.json`
- `reports/BACKBONE_COVERAGE.md`（含按 Period 的 Critical/Major/Normal 分布）
- `reports/BACKBONE_REVIEW.md`（duplicate / granularity / gap QA）
- `reports/EARLY_HISTORY_UNCERTAINTY.md`（早期历史不确定性专项）

## 8. Timeline 快捷查询

```bash
history-data backbone timeline              # 全库 critical+major 主时间线
history-data backbone timeline --importance critical
history-data backbone timeline --period warring
history-data backbone timeline --period 春秋 --json
```

当前主时间线最早节点：夏朝建立（前 2070）；最晚节点：安史之乱平定（763）。
先秦段最早 = 前 2070，最晚 = 前 221（秦统一）。

## 9. 下一批建议

- 建议进入 **秦汉批（qin_han / three_kingdoms）**：复用既有 楚汉 Story（9 Event）与三国 Story（8 Event），
  补充 秦统一制度（郡县/文字/度量衡）、汉武帝时期、王莽代汉、光武中兴、党锢、黄巾等节点；
- 注意复用而非重复建档（禁止 `event-hongmen-2` 式重复）；
- Evidence Linking 与 Person/Place 关联在 Backbone 主干完成后单独执行。