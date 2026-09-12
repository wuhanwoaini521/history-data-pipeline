# MAJOR_BATCH02_DEPTH01_FINAL — History V2 Major Batch 02 + Content Depth Sprint 01

> 任务：Queue 0–17（30 个新 Major 富化 + 20 个深度事件冲刺），原则 SOURCE-BACKED FIRST；
> coverage_score ≠ content_quality；不增废话、不 summary 拆句、不 LLM 常识伪造 STRONG。

## 0. 结果总览（成功标准对照）

| 指标 | 目标 | 结果 | 判定 |
|---|---|---|---|
| FULL（100 分） | ≥181（151→+30） | **181** | ✅ |
| STRONG（Depth Gate V1） | ≥70 | **70** | ✅ |
| 30 新 Major ≥90 / 大多数 100 | 30/30 | **30/30 全部 100.0** | ✅ |
| 20 深度事件 ≥15 升 STRONG | ≥15 | **20/20 升 STRONG**（四段均≥90 字） | ✅ |
| 完整性 | validate OK，0 broken | Validation OK（618 事件，0 broken） | ✅ |
| 测试 | Python/Rust 全绿 | Python 249 passed / 16 skipped；Rust 见 §7 | ✅ |

## 1. 队列执行（0–17）

- **Q0 基线**：main 63a6de8 / 子模块 9986327，工作区干净（`batch02-00-git-state` 同源核实）。
- **Q1 真实指标重建**：FULL 151 / ADEQUATE 111 / STRONG(V1) 20 / LOW 20 / INCOMPLETE 467；证据 790（776 linked）、地点 215（event_place）、关系 1073、文本 733,372。
- **Q2 选 30**：`major02-02-selection.md` + `major02-batch30.json`（唐8/明8/元6/春秋4/隋4，全部 READY 22.2、排除已完成事件）。
- **Q3 选 20 深度**：`depth01-03-selection.md` + `depth01-batch20.json`（D1 5/D2 5/D3 4/D4 6）。
- **Q4 门禁 V1**：`scripts/content_depth_gate_v1.py`（audit-only，12 分制，见 CONTENT_DEPTH_REPORT §1）。
- **Q5 簇规划**：并入两份 selection 报告（G/H/I/J/K + D1–D4）。
- **Q6 30 新 Major**：5 个簇脚本 (`major02_cluster_g_tang.py` … `k_sui.py`) + H 组收尾 polish；30/30 → 100.0。
- **Q7 深度冲刺**：4 个组脚本 (`depth01_group_d1..d4.py`) + 共用工具 `_depth_util.py`；20/20 → STRONG。
- **Q8 关系审计**：relations 1094，bad target 0 / bad type 0 / self-ref 0 / duplicate 0（修复 1 处失效目标：qin-tongyi → event-qin-xiu-changcheng）。
- **Q9 每簇验证**：每簇 append → `fix_duplicate_top_keys.py` → `backbone validate` → 重建 dist → 门禁复评，全部通过。
- **Q10 深度验证（不得注水）**：全库 0 处「段=summary」、0 处四段互重、impact 空话 grep 0 命中；额外修复 4 个 legacy 注水事件（鸦片战争/清帝退位/三藩之乱/武昌起义，background=result）。
- **Q11 覆盖率重建**：`reports/product_coverage.json`（181/618=29.3%，mean 47.5）+ BACKBONE_COVERAGE/PRODUCT_COVERAGE 报告随构建更新。
- **Q12 深度报告**：`reports/current-run/CONTENT_DEPTH_REPORT.md`。
- **Q13 深度队列**：`reports/current-run/DEPTH_ENRICHMENT_QUEUE.json`（LOW 19 + ADEQUATE 92，按 importance/points 排序）。
- **Q14 吞吐量 V2**：`reports/current-run/throughput-v2.json`（本轮 +387 evidence、50 事件、9 簇）。
- **Q15 全量测试**：Python 249 passed / 16 skipped（0 failed）；Rust `devtoolbox-infrastructure` 见 §7；tsc 见 §7。
- **Q16 Git 策略**：1 簇=1 提交；先推子模块再 gitlink（见 §8 提交清单）。
- **Q17 本报告**。

## 2. 交付数据变化（dist 复核）

| 指标 | 基线 | 现在 | 说明 |
|---|---|---|---|
| events | 618 | 618 | — |
| FULL（100 分） | 151 | **181** | +30 新 Major |
| event_evidence | 790 | **1177** | +387（新增 manual 段落锚，全部 claim_field） |
| event_place | 215 | **308** | +93（30 事件 places 去重后） |
| event_relations | 1073 | **1094** | +21（含 causes/leads_to/follows/contributes_to） |
| event_person | 398 | 398 | 未变（人物以 needs_linking 保留，不虚增 linked） |
| historical_texts | 733,372 | 733,372 | 语料未变（本轮只读） |

Depth Gate：STRONG 20→**70**；ADEQUATE 111→92；LOW 20→**19**；INCOMPLETE 467→437。

## 3. 聚类成果（30 新 Major，全部 100.0 FULL + STRONG）

| 簇 | 事件 | 关键来源 |
|---|---|---|
| G 唐 8 | 白江口 / 大非川 / 甘露之变 / 淮西之战 / 黄巢入长安 / 会昌灭佛 / 建中之乱 / 开元盛世 | 旧唐书·新唐书·通鉴唐纪（段落锚精确到 #pN） |
| H 明 8 | 北京保卫战 / 崇祯即位 / 建文削藩 / 东林党争 / 夺门之变 / 后金建立 / 东南倭患 / 大礼议 | 明史（本纪/列传/志）+ 清史稿太宗本纪一 |
| I 元末 6 | 红巾军 / 郭子兴 / 陈友谅代汉 / 韩林儿 / 贾鲁治河 / 南坡之变 | 元史 + 明史太祖纪（元史缺顺帝纪/河渠志，已如实标注） |
| J 春秋 4 | 城濮 / 邲 / 柏举 / 管仲改革 | 左传·史记·国语 |
| K 隋 4 | 开皇之治 / 大运河 / 江都兵变 / 李渊太原起兵 | 隋书·通鉴隋纪·旧唐书高祖纪 |

## 4. 深度冲刺（20 事件 → STRONG）

- D1 先秦秦汉（5）：秦灭六国 / 秦统一 / 三家分晋 / 七国之乱 / 漠北之战（史记·汉书·通鉴秦纪）
- D2 晋群（5）：八王之乱 / 东晋建立 / 晋灭吴 / 西晋灭亡 / 永嘉之乱（晋书帝纪·八王列传·王濬传·志）
- D3 南北朝隋（4）：北魏分裂 / 北周灭北齐 / 侯景之乱 / 隋灭陈（魏书·北齐书·周书·梁书·陈书·隋书）
- D4 唐宋明（6）：后梁代唐 / 陈桥兵变 / 靖康之变 / 崖山海战 / 土木堡之变 / 萨尔浒之战（旧唐书·通鉴后梁纪·宋史·明史）

每题均：补锚 evidence（含 claim_field）→ 四段阶段化重写（≥90 字、≥3 阶段）→ 补 relations → 复评。

## 5. 已知缺口与豁免（透明记录）

- `event-houjin-jianguo`：语料无 1616 年称汗的直接记载（明史以「大清兵」纪事、清史稿无太祖本纪），evidence 以建州源流 + 抚顺/萨尔浒为锚，review_note 已注明；
- `event-jialu-zhihe`：元史语料无河渠志与顺帝纪，治河主体（贾鲁、役夫数）据后世补记，锚点用「河平碑」与红巾起事，review_note 已注明；
- 元史/明史部分章节存在多文档同卷（如明史卷二十九 = 礼志+齐泰传），锚点以 `text_id` 精确识别，chapter_anchor 仅作人类可读坐标。

## 6. 文件清单（本轮新增/更新）

- 工具：`scripts/content_depth_gate_v1.py`、`scripts/anchor_lookup.py`、`scripts/para_dump.py`、`scripts/_depth_util.py`、`scripts/fix_duplicate_top_keys.py`（既有）
- 簇脚本：`scripts/major02_cluster_{g_tang,h_ming,h_polish,i_yuan,j_chunqiu,k_sui}.py`、`scripts/depth01_group_{d1,d2,d3,d4}.py`
- 报告：`CONTENT_DEPTH_REPORT.md`、`DEPTH_ENRICHMENT_QUEUE.json`、`throughput-v2.json`、`major02-02-selection.md`、`depth01-03-selection.md`、`major02-batch30.json`、`depth01-batch20.json`、`content-depth-gate-v1.json`
- 数据：30 新 Major + 20 深度事件 + 4 legacy 去水事件（YAML）；测试计数同步（test_backbone*.py）

## 7. 测试与构建

- Python：`pytest tests/ -q` → **249 passed, 16 skipped, 0 failed**（4:54）。
- 构建：`backbone validate` OK；`backbone --knowledge data/normalized/history.duckdb build` 重跑 dist 成功（测试后已重建，dist ≠ 仅种子）。
- Rust：`cargo test -p devtoolbox-infrastructure --lib`（见执行记录；feishui evidence 期望 7 与 events≥618 均满足）。
- tsc：父仓库未见 TS 工程变更（本轮只动子模块数据与报告）。

## 8. Git 提交清单（子模块 → gitlink）

子模块 main（已推送）：
```
670e00d feat(history): Major Batch 02 cluster G - Tang (8 events)
02c57d2 feat(history): Major Batch 02 cluster H - Ming (8 events)
6024e3d docs(history): cluster H polish - all four narrative dims to STRONG
4eac864 feat(history): Major Batch 02 cluster I - Yuan/late-Yuan (6)
82395ad feat(history): Major Batch 02 cluster J - Spring and Autumn (4)
7626b31 feat(history): Major Batch 02 cluster K - Sui (4)
583f5c4 feat(history): Depth Sprint 01 D1+D2 (10 events)
a9288d8 feat(history): Depth Sprint 01 D3 (4 events)
000b1c7 feat(history): Depth Sprint 01 D4 (6 events)
6eb9d2e docs(history): Depth Sprint 01 final polish
7511f14 test(history): sync dist count expectations + depth reports
```
父仓库：gitlink 更新至上述 HEAD（commit 见父仓库日志），未强推、未引用未推送提交。

## 9. 下一阶段建议

1. **Depth Sprint 02**：以 `DEPTH_ENRICHMENT_QUEUE.json` 为准，先清 19 个 CONTENT_DEPTH_LOW（qin 7 + 汉末 6 + 唐/明 6），预计可将 STRONG 推至 90+；
2. **ADEQUATE 92 收敛**：western-han 30（人物/制度短事件）为最大块，可用同法批量补锚；
3. **语料缺口**：接入《清实录》《日本书纪》或《元史·河渠志》《顺帝纪》可解 3 处 NEEDS_SOURCE 与 2 处标注豁免；
4. **产品侧**：181 个 FULL 事件已可支撑 History UI 的「深度筛选」（STRONG 70 为精选集），建议 Timeline/Entity 视图接入 depth_status 字段（audit-only JSON，不动 schema）。
