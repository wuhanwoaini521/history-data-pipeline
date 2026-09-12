# History V2 Overnight Result

> 生成：2026-09-12 03:xx · Overnight Queue 0–11 执行完毕

## 1. Executive Summary

**PASS（带 1 类外部 BLOCKER）**

昨晚完成了整条 Knowledge → Evidence → Quarantine → Critical Events → Coverage 链路的
**验证性复核 + 第一批 Critical 事件富化**：

- 知识层（上轮已重建的 730,128 条 historical_texts）通过全部 7 项复核
  （双 build 幂等、完整性 13 项检查全绿、E2E 五样例可用）；
- **14 个 Critical 事件按纵向富化完成 6 个**（3 个到 100 分、3 个到 88.9 分），
  全部 source-backed：每条新叙述回链语料具体段落 + 逐字引文；
- **8 个事件（7 个 20 世纪 + 西夏建国）因语料缺失保持 NEEDS_SOURCE**，未编造；
- 过程/影响两维**全库破零**（0% → 1.0%，各 +6 事件）；
- 测试：Python 236 通过 / Rust 200 通过 / tsc 通过。

## 2. Git State

| 仓库 | commit |
|---|---|
| self-tools（main repo） | `403d5fd`（干净） |
| history-data-pipeline | `22158dc`（工作区有本轮未提交改动，见下） |

**未提交（按指令"不要自动提交"保留在工作区）：**

- Modified（14）：
  - `data/curated/history_backbone/events/**` ×6 —— Critical 富化（mongol/yuan/pingwang/chuzhuang/jinwen/hezong）
  - `src/history_data_pipeline/backbone/build.py` —— 跳过 person_id 为空的 needs_linking 人物（防 dist 主键崩溃 + 不伪造身份）
  - `tests/test_backbone.py`、`tests/test_backbone_build.py` —— 4 处硬编码计数更新（+11 地点 / +24 证据，见 overnight-10）
  - `reports/{BACKBONE_COVERAGE.md, PRODUCT_COVERAGE.md, ENRICHMENT_QUEUE.json, product_coverage.json, current-run/quarantine-after-knowledge-rebuild.json}` —— 富化后再生成
- Added/untracked（12）：`scripts/overnight_critical_enrichment.py` + `reports/current-run/overnight-00..10*.md` 共 11 份
- Deleted：无

## 3. Knowledge Layer

| | Before | After |
|---|---:|---:|
| dist historical_texts | 730,128 | **730,128**（复核一致） |
| chapter_heads | 3,838 | 3,838 |

- 是否真正恢复：**是**（上轮 `22158dc` 完成，本轮为验证性复核：rebuild 两次计数逐位一致）
- 数据来源：NiuTrans Classical-Modern @ `4e746ea`（MIT），快照 20240421
- 章节结构：document（书）→ section（卷类）→ chapter（篇卷）→ paragraph_index（行）
- paragraph 数：730,128 行级句对（双语 721,424 + 古文原文 8,704）

## 4. Evidence（dist event_evidence 154 条）

| 指标 | Before（昨晚起算） | After |
|---|---:|---:|
| linked | 74 | **98**（+24：6 事件 × 4 字段级证据） |
| pending_knowledge | 22 | 22（legacy 悬空 id，如实保留） |
| needs_linking | 34 | 34（27 fuzzy 候选 + 7 未命中） |
| claim_field 非空 | 0 | **24**（background/process/result/impact 各 6） |

## 5. Quarantine

| 指标 | 值 |
|---|---|
| before / after | 10 / **10**（无强制清零） |
| promoted | 0 |
| still quarantine | 10（其中蒙古/元朝 88.7 分，+1.0 来自知识层锚定） |
| needs source | 8（7 个 20 世纪 + 西夏建国） |

## 6. Critical Event Enrichment（14 total）

| 状态 | 数量 | 事件 |
|---|---:|---|
| completed（≥90） | 3 | 蒙古建国 100 / 元朝建立 100 / 平王东迁 100 |
| partial（80–89） | 3 | 楚庄王 88.9 / 晋文公 88.9 / 合纵连横 88.9（均缺 related_event，需策展定因果边） |
| blocked | 8 | 九一八/南京大屠杀/七七/日本投降/五四/西安事变/西夏建国/新中国成立（source missing） |

## 7. Product Coverage（618 事件）

| 指标 | Before | After |
|---|---:|---:|
| 平均分 | 30.9 | **31.6** |
| ≥90 条目 | 0 | **3（0.5%）** |
| 背景 | 8.3% | **9.2%** |
| 过程 | **0%** | **1.0%（破零）** |
| 结果 | 12.5% | **13.4%** |
| 影响 | **0%** | **1.0%（破零）** |
| 人物 | 42.2% | 42.7% |
| 地点 | 4.2% | **5.2%** |
| 证据 | 12.5% | **13.4%** |

ENRICHMENT_QUEUE：Critical 14 → **8**（剩余 8 个全部是 source-missing 事件）。

## 8. Tests

| 套件 | 命令 | 结果 |
|---|---|---|
| Python | `pytest tests/ -q` | 236 passed / 16 skipped / 0 failed |
| Rust | `cargo test --workspace` | 200 passed / 0 failed |
| 前端 | `npx tsc --noEmit`（apps/desktop/ui） | exit 0 |

本轮修了 4 处过时计数断言（+11 地点 / +24 证据行的合法增长，逐条注释说明）；
修了 1 个实现 bug（build.py needs_linking 人物触发 dist 主键约束 → 跳过未解析身份行）。

## 9. Files Changed（逐文件理由见 overnight-08/10 报告正文）

见 §2；核心：6 个事件 YAML（source-backed 富化）、build.py（person_id 防线）、
2 个测试文件（计数）、脚本 `overnight_critical_enrichment.py`（可重跑的富化器）、
11 份 overnight 报告、3 份再生成的 coverage 报告。

## 10. Blockers

1. **外部来源缺失（核心阻塞）**：剩余 8 个 Critical（九一八/南京大屠杀/七七/日本投降/五四/
   西安事变/西夏建国/新中国成立）依赖的著作——中华民国史、中国抗日战争史、南京大屠杀史料集、
   中国共产党历史、二十世纪中国史纲、清实录、清史稿、明实录、续资治通鉴长编、筹办夷务始末、
   蒙古秘史、元朝史、宋史·夏国传——**不在 NiuTrans 语料**。需人工提供可信章节目录/文本后推进。
   在此之前这些事件的背景/过程/结果/影响/地点/证据一律 NEEDS_SOURCE。
2. **related_event ×3**（楚庄王/晋文公/合纵连横 88.9 分卡点）：需要策展决策建立到既有事件的因果边。
3. **人物/地点身份解析**：本轮新增的 10 个人物、11 个地点均为 name_raw + needs_linking
   （不伪造 id/坐标）；如需 linked 状态，需进入 knowledge store 建 canonical 实体。

## 11. Recommended Next Queue

1. **Critical 残余 8 事件的来源获取**（人工协作）：逐部落实 20 世纪著作的章节目录，
   按转写规则入库 —— 这是 Critical 队列清零的唯一路径。
2. **related_event 补全**（楚庄王/晋文公/合纵连横 → 100 分）：对照事件清单建立可解释因果边。
3. **新增人物/地点 canonical 化**：把 10 人物/11 地点升格为 knowledge store 实体（含外部 id 解析）。
4. **Major Batch 01**（队列头部，约 30–50 个事件）：重复本夜"纵向富化"流程
   （脚本已参数化，改数据即用）——只处理语料覆盖的 Major，缺语料的跳过并记录。
5. **段级 fuzzy 人工复核**：27 条带候选段落的 NEEDS_REVIEW 证据，确认 quote 后升级为段级锚定。
