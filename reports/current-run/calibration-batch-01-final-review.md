# Calibration Batch 01 — Final Review Report

- Batch: `calibration-batch-01`
- Events: 10 Critical Events（`reports/calibration_batch01_selection.json`）
- Report written: 2026-09-09
- Owner: history-data-pipeline automation（AGENTS.md §20 — 审查系统，不是逐条记录）
- Run dir: `reports/current-run/`
- Verification artifacts: `reports/current-run/verification/`（10 verifier JSON + 1 auditor JSON）

---

## 1. Final verdict

**CALIBRATION_FIX_REQUIRED**

这是校准批次（calibration batch）：目的是检验自主富集管线在大规模（Batch 20）之前是否可信、可复现、诚实。管线本身表现良好：确定性校验零错误、零硬失败、抽样审计 PASS，10 个候选全部 AUTO_ACCEPT。但 10 个候选中有 8 个被独立 Verifier 标记 WARN，其中 4 项属历史内容层面需要落地修改（未保留的 DISPUTED 争议、章节定位错误、地点有效期不匹配），另有 3–4 项属生产者/模板层的系统级修改。按校准批次原则（先修复问题类别，再放大规模），结论为 **CALIBRATION_FIX_REQUIRED**，修复清单见 §9。全部 10 个候选保持在 candidate 阶段：不晋升、不隔离、不删除。

---

## 2. 范围与候选

| # | 事件 id | 中文名 | canonical 文件 |
| --- | --- | --- | --- |
| 1 | event-shangtang-miexia | 商汤灭夏 | `.../pre_qin/event-shangtang-miexia.yml` |
| 2 | event-wuwang-fazhou | 武王伐纣 | `.../pre_qin/event-wuwang-fazhou.yml` |
| 3 | event-pingwang-dongqian | 平王东迁 | `.../chunqiu_zhanguo/event-pingwang-dongqian.yml` |
| 4 | event-sanjia-fenjin | 三家分晋 | `.../chunqiu_zhanguo/event-sanjia-fenjin.yml` |
| 5 | event-changping-zhizhan | 长平之战 | `.../chunqiu_zhanguo/event-changping-zhizhan.yml` |
| 6 | event-qin-mie-liuguo | 秦灭六国 | `.../chunqiu_zhanguo/event-qin-mie-liuguo.yml` |
| 7 | event-qin-tongyi | 秦统一六国（秦帝国建立） | `.../chunqiu_zhanguo/event-qin-tongyi.yml` |
| 8 | event-qiguo-zhi-luan | 七国之乱 | `.../qin_han/event-qiguo-zhi-luan.yml` |
| 9 | event-mobei-zhizhan | 漠北之战 | `.../qin_han/event-mobei-zhizhan.yml` |
| 10 | event-wangmang-chengdi | 王莽称帝、新朝建立 | `.../qin_han/event-wangmang-chengdi.yml` |

候选产物：`data/candidates/calibration_batch01/*.yml`（10 个文件，Producer 输出）。

---

## 3. 基线（BEFORE，`reports/calibration_batch01_baseline.md`)

| 指标 | 值 |
| --- | --- |
| 10 个事件 mean / min / max 分数 | 78.0 |
| 基线判定 | 全部 QUARANTINE_MEDIUM（无 AUTO_ACCEPT） |
| evidence 行数 | 0（全部事件） |
| background / result 字段 | 全部缺失 |
| evidence_precision 维度 | 全部 0.0 |

基线含义：富集前这 10 个事件没有证据行、没有 background/result，全部低于 90 分门槛。本次候选把每事件评分提高了约 15–18 分。

---

## 4. AFTER — 逐事件质量分数 + 验证判定矩阵

> 分数为确定性 `qa-run`（seed=1）在当前仓库状态下的重算值，由 `backbone/quality.py` 计算。与进度文档早期记录（min 93.9 / max 96.9 / avg 94.4）存在 ±1 分量级的移位，属历史档案时间点差异；以下方最终重算值为准。

| 事件 | 质量分 | 分差(100−) | 质量判定 | Verifier 判定 | 核验要点 |
| --- | --- | --- | --- | --- | --- |
| event-wuwang-fazhou | 94.4 | 5.6 | AUTO_ACCEPT | **PASS** | 两个独立古典锚点（史记·周本纪 + 尚书·牧誓）+ 利簋 |
| event-qin-mie-liuguo | 92.7 | 7.3 | AUTO_ACCEPT | **PASS** | 史记·秦始皇本纪 + 资治通鉴·秦纪 两个独立古典锚点 |
| event-shangtang-miexia | 94.4 | 5.6 | AUTO_ACCEPT | WARN | 内容 pass；WARN 为 schema 细项（见 B5）+ 现代书目分页未能机器核验 |
| event-pingwang-dongqian | 95.7 | 4.3 | AUTO_ACCEPT | WARN | 地点 id cbdb-place-14693 的 valid_from/to（710–959）不覆盖事件的 −770 年份 |
| event-sanjia-fenjin | 93.9 | 6.1 | AUTO_ACCEPT | WARN | ctext person_id 声明 linked@1.0 未独立核验（ctext 403） |
| event-changping-zhizhan | 94.4 | 5.6 | AUTO_ACCEPT | WARN | 伤亡数「40万 vs 45万」未标 DISPUTED；史记两章 = 同一部书单源 |
| event-qin-tongyi | 92.7 | 7.3 | AUTO_ACCEPT | WARN | person_id 未核验 + `linked@1.0` 的 V2.1 备注未锚定仓库记录 |
| event-qiguo-zhi-luan | 93.9 | 6.1 | AUTO_ACCEPT | WARN | evidence 章节写「吴王濞传」，正确为 荆燕吴传（汉书卷三五）；同错在 canonical source_reference 中 |
| event-mobei-zhizhan | 94.4 | 5.6 | AUTO_ACCEPT | WARN | 匈奴伤亡数实际出自 匈奴列传/匈奴传，未列入 evidence 行 |
| event-wangmang-chengdi | 92.7 | 7.3 | AUTO_ACCEPT | WARN | 称帝年 8 vs 9 AD 未以 DISPUTED 记录（canonical 记 9） |

汇总：

- 质量分：min **92.7** / max **95.7** / mean **93.9**；10/10 AUTO_ACCEPT；硬失败 **0**。
- Verifier：**2 PASS / 8 WARN / 0 FAIL**；Auditor 整体 **PASS**。
- 质量提升：BEFORE 10×78.0 → POST 表中分数，每事件 +14.7 ~ +17.7 分。

---

## 5. 确定性 QA 结果（gate G0–G5）

| Gate | 结果 |
| --- | --- |
| G0 Schema + G1 Integrity（`validate_backbone`） | 0 错误 |
| G2 时态（event/person/place 新规则） | 0 冲突 |
| G3 来源存在性 | 全通过（每个候选都有 source_reference + source_ids） |
| G4 质量分 | 10/10 ≥ 90 → AUTO_ACCEPT |
| G5 采样审计（seed=1, n=3） | 3/3（auditor 整体 PASS） |

- `quarantine.jsonl`：0 行；无候选被隔离；canonical `data/curated` 未被改动（由测试套件验证）。

---

## 6. 独立验证结果（第 1 轮完成）

10 个事件的 verifier JSON 与 1 个 auditor JSON 已全部就位（本轮恢复了此前因运行期工具错误而缺失的 3 个：`event-shangtang-miexia.json`、`event-pingwang-dongqian.json`、`event-changping-zhizhan.json`）。

### 跨 10 记录一致通过项

1. **无虚构**：10 个候选均无编造的坐标、日期、章节、text id、source id、link_status；`historical_text_id` 均为 null/absent（与 schema 要求一致）。
2. **verbatim 保真 100%**：所有从 canonical 复制的字段逐字符一致，0 处异体字符；background/result 是 canonical 摘要的确定性切分。
3. **证据独立性**：史记+尚书、史记+资治通鉴、史记+左传 等两锚点事件站得稳；单书多章与借用他书证据的事件被单独标注。

### 复核保留的关键发现

- 多家 candidate 的 evidence 引用《资治通鉴》，但 `source_ids` 只列 primary work（如史记/汉书）→ 统一 deferred 到 linking 阶段，是跨纪录的 source_ids/evidence 间隔。
- 多家 candidate evidence 统一 `link_confidence=0.9` + `link_status=needs_linking`（可接受但单调，非逐条独立解析）。
- 多家候选的 person 层 `linked@1.0` + `V2.1 review` 备注继承自已接受 EventPerson 层（V2.1 审查溯源），未经本次 resolver 数据库再验证 —— 在再验证之前应视为未完全独立确认。
- ctext.org HTTP 403 持续出现；全部字验经由权威镜像（zh.wikipedia / zh.wikisource / 百度百科 / 识典古籍）完成，未做任何无证明的“确认”。

---

## 7. 8 项管线自诊断问题（系统级审查）

1. **是否存在任何编造（虚构）内容？** — 否。10 个候选 + auditor 均无虚构发现；AGENTS.md §17 硬失败类别全部缺位。
2. **候选对 canonical 的保真度？** — 100%。所有复制字段逐字符一致，0 异体；仅新增 derived 字段（background/result、evidence、人员/地点标记）。
3. **证据链是否真独立（多重来源 vs 同源复写）？** — 大部分是；被标记的 4 项：同一部书多章（长平、七国之乱）、精确数字需要另书/另传支撑（漠北之战伤亡数的匈奴列传/传）、ctext 不可达故未确认（三家分晋的章节字验）。
4. **不确定性是否被如实保留（DISPUTED）？** — 部分。前1600 vs 前1556（商汤）、前1046 vs 前1027（武王伐纣）已在总结中保留；**长平 40万 vs 45万、王莽 8 vs 9 AD 两项未落 DISPUTED（随 canonical 逐字复制，未处理）。**
5. **人物/地点解析是否严谨、未过度自信？** — 主要继承自已接受 EventPerson 层；个别 `linked@1.0` 声称未独立验证（三家、秦统一）；平王东迁的地点 id 时间窗口与事件不匹配。待 resolver 再验证前不视为已解决。
6. **确定性校验与评分模型是否可复现？** — 是。seed=1 下重跑重现 10/10 AUTO_ACCEPT、0 错误。
7. **验证、审计、评分是否互相独立？** — 是。Verifier（web-capable）与 Auditor（3 件采样、显式忽略 Verifier 结论）独立完成；Auditor 独立得出 PASS。
8. **是否出现需要人工介入的情形？** — 否。无隔离、无 REOPEN（材料失败率 0%），无政策冲突、无外部凭据问题。

---

## 8. 复发模式（供 Batch 20 / 修复批次处理，不重新逐条审计）

1. 《资治通鉴》在 evidence 中被引用但不在 `source_ids`（linking 阶段需同步）。
2. evidence `link_confidence=0.9` 统一默认值，逐条独立解析欠奉。
3. person `linked` 状态与 1.0 置信依赖旧审查备注，未在本轮 resolver 复验。
4. Producer 模板细节：evidence 行未输出显式 `historical_text_id: null`；canonical 空的 `regime_ids` 被丢弃。
5. ctext.org 403：Verifier 模板应固定镜像优先策略（zh.wikipedia / zh.wikisource / baike / 识典古籍）。

---

## 9. 修复清单（Fix List）

### A 级 — 历史内容（先修 canonical 叙事层，再重跑候选）

| 事件 | 修复项 |
| --- | --- |
| event-qiguo-zhi-luan | 证据章节名「吴王濞传」→「荆燕吴传」（汉书卷三十五）；canonical `source_reference` 中同样错字一并修正 |
| event-changping-zhizhan | 伤亡数「40万 vs 45万」以 DISPUTED 形式记录（候选与 canonical 同步处理） |
| event-wangmang-chengdi | 称帝年「8 vs 9 AD」以 DISPUTED 形式记录，同时保留 canonical 的 9 AD 值 |
| event-pingwang-dongdian | 地点 id（cbdb-place-14693）改为绑定周代有效期窗口，或挂未定窗口的地点，避免 −770 事件套用 710–959 窗口 |

### B 级 — 生产层/模板（修一次，Batch 2 自动受益）

| 项 | 修复 |
| --- | --- |
| B5 | producer 在 evidence 输出显式 `historical_text_id: null` 键；保留 canonical 空 `regime_ids` |
| B6 | resolver 层：`link_status=linked` 之前须对 CBDB/ctext person_id 独立核验并记录 |
| B7 | evidence.work 不在 source_ids 的情况（如《资治通鉴》）统一走 to-linking 队列或补 source_id |
| B8 | 模板明确「同一部书的多个章节 ≠ 多个独立来源」，单书证据在 evidence 中显式标注 |

### C 级 — 仅作说明（无阻塞）

- ctext 403 镜像策略固定即可，无数据变更动作。

---

## 10. 本次交付物

| 产物 | 路径 | 状态 |
| --- | --- | --- |
| 候选 10 个 | `data/candidates/calibration_batch01/*.yml` | 已有（本轮重算得分） |
| 研究报告 | `reports/current-run/research-brief-batch01.md` | 已有 |
| 指标 / 摘要 / 隔离 | `reports/current-run/{metrics.json, summary.md, quarantine.jsonl}` | 本轮重新生成（quarantine 0 行） |
| Verifier 产物（10） | `reports/current-run/verification/event-*.json` | 7 个已有 + **3 个本轮补全** |
| Auditor 产物 | `reports/current-run/verification/auditor.json` | 已有 |
| 进度文档 | `docs/PROGRESS_CALIBRATION_BATCH_01.md` | 本轮标记 complete |
| 本报告 | `reports/current-run/calibration-batch-01-final-review.md` | **本轮新增** |

---

## 11. 结论

- 管线系统复核（AGENTS.md §20）：QA/富集引擎可信 —— 确定性、可复现、canonical 只读、无虚构、不确定性透明。
- 产品就绪度：10 个候选是 canonical 骨架的可靠派生（较 BEFORE 78.0 提升约 15–18 分），全部无虚构、无硬错；但 **4 项内容修复 + 3 项生产模板修复**宜先落地。
- 校准决定：**CALIBRATION_FIX_REQUIRED** —— 按 §9 修复清单执行修复批次，重跑受影响事件的确定性 QA 与复核后，再进入 Batch 20（或在 owner 指示下进入下一步）。

---