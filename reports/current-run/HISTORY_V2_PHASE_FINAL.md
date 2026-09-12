# HISTORY V2 PHASE FINAL — Phase Wrap-up 总报告

## 1. Status

**PASS**

（架构 / 知识层 / 证据层 / 门禁 / 覆盖率 / 测试 / Git 全部达标；唯一未闭合项为许可受限的 2 个事件，属登记在案的 BLOCKED 项，不影响 Phase 1 关闭。）

## 2. Phase Summary

History V2 当前已具备：

- **可复制的生产管线**：source → chapter → paragraph → evidence（段落锚 `#pN` + text_id）→ claim_field → 四段叙事 → validation → dist build，全链路脚本化（`anchor_lookup.py` / `para_dump.py` / `_depth_util.py` / 各簇脚本）。
- **稳定的知识层**：733,372 条历史文本（NiuTrans 正史 + wikisource 快照），构建确定性（连续两次 build 计数完全一致）。
- **健康的证据层**：1,177 条 evidence 全部可回溯到具体段落；0 dangling / 0 重复 / 0 非法 claim_field；fuzzy 链接 0（硬规则成立）。
- **可解释的内容深度门禁**：Content Depth Gate V1（12 分制，audit-only），把「完成度（coverage）」与「内容深度（depth）」彻底分开；并把 ADEQUATE 进一步分为 HIGH / MID / NATURAL / SOURCE_LIMITED 四档，避免后续无止境扩写。
- **规模与质量基线**：618 事件中 181 个 FULL（100 分），86 个 STRONG，LOW 归零；Critical 60/62。

## 3. Final Metrics

| 指标 | 数值 |
|---|---|
| events | **618** |
| FULL（100 分） | **181**（比率 29.3%） |
| STRONG | **86** |
| STRONG / FULL | **86/181 = 47.5%** |
| STRONG / ALL | **86/618 = 13.9%** |
| ADEQUATE_HIGH | **24**（P1，差一维即可 STRONG） |
| ADEQUATE_MID | **36**（P2） |
| ADEQUATE_NATURAL | **34**（P4，不再常规扩写） |
| SOURCE_LIMITED | **1**（吴起变法） |
| CONTENT_DEPTH_LOW | **0** |
| INCOMPLETE（coverage<100） | 437（由 ENRICHMENT_QUEUE 管理） |
| average score | **47.5** |
| historical_texts | **733,372** |
| evidence | **1,177**（linked 1,163 / needs_linking 14） |
| places（event_place） | **308** |
| relations | **1,112** |

## 4. Critical

**60 / 62** complete

blocked（LICENSE_BLOCKED，非内容失败）：
- 九一八事变
- 西安事变

## 5. Depth Sprint 02（selected = 19）

| 结果 | 数量 | 明细 |
|---|---|---|
| → STRONG | **16** | guiling-zhizhan, likui-bianfa, lizicheng-gong-beijing, zhuyuanzhang-chendi, han-dingdu-changan, qin-beiji-xiongnu, qin-nanzheng-baiyue, qin-shihuang-beng, qin-shutongwen, qin-tongyi-duliangheng, qin-xiu-changcheng, shaqiu-zhengbian, anlu-shi-siming, anlu-xuanzong-shu, three-guandu, three-north-consolidation |
| → ADEQUATE_NATURAL | **2** | hanwudi-jiwei（即位类短事件）、han-yuandi-jiwei（即位类短事件） |
| → SOURCE_LIMITED | **1** | wuqi-bianfa（史记仅 4 处短引，不硬推 STRONG） |
| still LOW | **0** | — |

处理方式：诊断 → 既有语料检索 → 段落锚补强/重写阶段化四段 → 补自然 relations（18 条）→ 复评。全程 SOURCE-BACKED FIRST，无 summary 拆句、无空话 impact。

## 6. Integrity

| 检查 | 结果 |
|---|---|
| broken links（dangling evidence / relations / event_text） | **0** |
| duplicate IDs（event） | **0** |
| duplicate places（同事件同名 + 规范表重复） | **0** |
| invalid anchors（historical_text_id 不可解析） | **0** |
| invalid claim_field | **0** |
| fuzzy linked | **0** |
| self relations | **0** |
| backbone validate | **Validation OK** |
| build determinism（连续两次 build 计数一致） | **YES** |

## 7. Tests

| 项 | 结果 |
|---|---|
| Python（`pytest tests/ -q`） | **249 passed, 16 skipped, 0 failed**（5:12） |
| Rust（`cargo test -p devtoolbox-infrastructure --lib`） | **99 passed, 0 failed** |
| tsc（apps/desktop） | **SKIPPED_WITH_REASON**：无 node_modules（未安装依赖），非 code failure；本轮未改 TS 代码 |
| pipeline validate | PASS |
| dist integrity（Q18 脚本） | 全项 0 |

## 8. Git

| 项 | 值 |
|---|---|
| submodule final commit | 见 `git -C history-data-pipeline log -1`（本轮收尾提交） |
| main final commit | 见父仓库 `chore: bump history-data-pipeline` 最新 |
| pushed | **yes**（先子模块后 gitlink；未 force push） |
| workspace clean | **yes**（main 与子模块均 clean） |

## 9. Remaining Debt

- **License blockers**：九一八事变、西安事变（LICENSE_BLOCKED）
- **Source blockers**：清实录 / 明实录 / 长编 / 民国文书 / 晚清档案 / 元史缺卷（顺帝纪、河渠志）——详见 `HISTORY_V2_BLOCKERS.md`
- **needs_linking**：evidence 14 条（语料缺著作）；地点/人物 needs_linking 为合法状态
- **Depth backlog**：`DEPTH_BACKLOG_V2.json`（P1 24 / P2 36 / P3 1 / P4 34；P0 已清零）
- **Coverage backlog**：437 个 INCOMPLETE 事件 → `reports/ENRICHMENT_QUEUE.json`

## 10. Resume Point

未来回来时：

1. 先读 **`reports/current-run/HISTORY_V2_HANDOFF.md`**（含 build/validate/test 命令与 DO NOT BREAK 规则）
2. 再读 **`reports/current-run/DEPTH_BACKLOG_V2.json`**（深度队列）
3. 然后读 **`reports/current-run/HISTORY_V2_NEXT_ROADMAP.md`**（路线）

---

**History V2 Phase 1 = CLOSED.**
