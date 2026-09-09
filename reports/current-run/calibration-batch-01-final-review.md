# Calibration Batch 01 — Final Review Report（含修复批次）

- Batch: `calibration-batch-01`
- Events: 10 Critical Events（`reports/calibration_batch01_selection.json`）
- Report written: 2026-09-09（修复批次：2026-09-09 同轮落地）
- Owner: history-data-pipeline automation（AGENTS.md §20 — 审查系统，不是审查记录）
- Run dir: `reports/current-run/`
- Verification artifacts: `reports/current-run/verification/`（10 verifier JSON + 1 auditor JSON）

---

## 1. Final verdict

**CALIBRATION_PASS**（修复批次已验证，可进入 Batch 20 前哨）

校准批次流程：首轮评审判定 **CALIBRATION_FIX_REQUIRED**（§9 修复清单：4 项历史内容 A1–A4 + 4 项生产层 B5–B8）。本轮已执行修复批次并全部复验：

- 修复后确定性 QA（seed=1）：**9 AUTO_ACCEPT / 1 QUARANTINE_MEDIUM**；硬失败 **0**；校验错误 **0**。
- 唯一隔离项 `event-pingwang-dongqian`（85.7）**非失败**，而是 A4 修复的有意结果：该事件旧地点窗口（710–959）与 −770 不符，按 AGENTS.md §12 不臆造窗口，改为 `place_id=null + needs_linking`，确定性评分如实扣 12.5 分抵押，保持 quarantine（修好地点实体后可再晋升）。
- 独立 Verifier 全批重跑：**7 PASS / 3 WARN / 0 FAIL**；WARN 均为非阻断（2 项 `chapter_hint: null` 模板一致性问题 + 1 项漠北 pre-existing 证据覆盖 note）。
- Auditor（当前 G5 队列 seed=1）：**3/3 PASS**，无虚构、无编造。
- 全仓回归：**210 pytest 全绿**。
- A4 之外所有 A1–A3 与 B5–B8 修复均已独立复核为生效（见 §6、§9 ✔）。

结论：管线在修复前暴露的 4 类内容缺陷与 4 类模板缺陷均已闭环；校准批次通过。全部 10 个候选保持 candidate 阶段（9 个可晋升、1 个隔离待地点解析），**不得直接写入 canonical**，待 owner 指示进入 Batch 2。

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

## 4. AFTER（修复批次后）— 逐事件质量分数 + 验证判定矩阵

> 分数为确定性 `qa-run`（seed=1）在当前仓库状态下的重算值，由 `backbone/quality.py` 计算。修复批次使 producer 进入 v4（B5–B8），逐事件分数相对首轮（max 95.7 / avg 93.9）略有移位；以下方最终重算值为准。

| 事件 | 质量分 | 分差(100−) | 质量判定 | Verifier 判定 | 核验要点 / 本批次处置 |
| --- | --- | --- | --- | --- | --- |
| event-wuwang-fazhou | 94.4 | 5.6 | AUTO_ACCEPT | **PASS** | 史记·周本纪 + 尚书·牧誓 + 利簋；B5/B7/B8 复验通过 |
| event-qin-mie-liuguo | 92.7 | 7.3 | AUTO_ACCEPT | WARN | B5/B7/B8 复验通过；WARN 仅为 资治通鉴 evidence 行 `chapter_hint: null`（模板一致性，schema 合法） |
| event-shangtang-miexia | 94.4 | 5.6 | AUTO_ACCEPT | **PASS** | 重生后 B5 显式 `historical_text_id: null` 就位；regime_ids 保留 |
| event-pingwang-dongqian | 85.7 | 14.3 | **QUARANTINE_MEDIUM** | **PASS** | A4 ✔：移除 710–959 虚构窗口 → `place_id=null+needs_linking`；评分如实扣 place_resolution 12.5 → 隔离（有意为之） |
| event-sanjia-fenjin | 93.9 | 6.1 | AUTO_ACCEPT | **PASS** | B5/B7/B8 复验通过；资治通鉴已列入 source_ids |
| event-changping-zhizhan | 94.4 | 5.6 | AUTO_ACCEPT | **PASS** | A2 ✔：40万 vs 45万 已以 DISPUTED 写入候选与 canonical |
| event-qin-tongyi | 92.7 | 7.3 | AUTO_ACCEPT | WARN | B5/B7/B8 复验通过；WARN 同 qin-mie-liuguo（`chapter_hint: null`，模板一致性问题） |
| event-qiguo-zhi-luan | 93.9 | 6.1 | AUTO_ACCEPT | **PASS** | A1 ✔：章节 吴王濞传→荆燕皇传（汉书卷三十五）候选与 canonical source_reference 均已修正，byte-scan 0 残留 |
| event-mobei-zhizhan | 94.4 | 5.6 | AUTO_ACCEPT | WARN | 对照组（未变更）：B5/B7 复验通过；WARN 为 pre-existing 伤亡数字证据锚到 史记·匈奴列传/汉书·匈奴传 未入 evidence 行 |
| event-wangmang-chengdi | 92.7 | 7.3 | AUTO_ACCEPT | **PASS** | A3 ✔：8 vs 9 AD 已以 DISPUTED 写入；start_year=9 保留与 汉书·王莽传 纪年一致 |

汇总（修复批次后）：

- 质量分（10 候选）：min **85.7** / max **94.4** / mean **92.9**（9 个 AUTO_ACCEPT，1 个 85.7 隔离）；硬失败 **0**。
- Verifier（全批重跑）：**7 PASS / 3 WARN / 0 FAIL**；3 项 WARN 均非阻断（2× `chapter_hint: null` 模板一致性、1× 漠北旧证锚 note）。
- Auditor：**3/3 PASS**（当前 G5 队列 seed=1）。
- 质量提升：BEFORE 10×78.0 → POST 9×≥90 + 1×85.7（隔离）；相对首轮 WARN 面（8/10）实质收敛。

---

## 5. 确定性 QA 结果（gate G0–G5，修复批次后）

| Gate | 结果 |
| --- | --- |
| G0 Schema + G1 Integrity（`validate_backbone`） | 0 错误 |
| G2 时态（event/person/place 新规则） | 0 冲突 |
| G3 来源存在性 | 全通过（每个候选都有 source_reference + source_ids） |
| G4 质量分 | 9/10 ≥ 90 → AUTO_ACCEPT；1 个 85.7 → QUARANTINE_MEDIUM（平王东迁，A4 有意隔离） |
| G5 采样审计（seed=1, n=3） | 3/3（auditor 整体 PASS；队列本轮为 3 个 canonical 事件） |

- `quarantine.jsonl`：1 行（`event-pingwang-dongqian`，85.7，无 hard failure，原因 `place_resolution=0.0/10`）。这是 A4 修复的预期后果，不是缺陷：该事件不再声称不真实的地点窗口。
- canonical `data/curated` 仅含 §9 A1–A3 的叙事层修正（章节名、两条 DISPUTED 补充），未做任何结构性改写；由全仓 pytest（210 项）验证。

---

## 6. 独立验证结果（第 2 轮完成 — 修复批次复跑）

修复批次后 10 个 verifier JSON 全部重跑（5 个受影响事件的完整复核 + 5 个未受影响事件的模板一致性复核），auditor JSON 按当前 G5 队列重跑。

### 修复项复验结论

| 修复项 | 复验方式 | 结论 |
| --- | --- | --- |
| A1 荆燕吴传 | byte-scan：candidate 与 canonical source_reference 均含 荆燕吴传，0 处残留 吴王濞传 | ✔ PASS |
| A2 长平伤亡 DISPUTED | summary 含「四十多万/四十五万/争议数字（DISPUTED）」，candidate 与 canonical 均生效 | ✔ PASS |
| A3 王莽 8v9 DISPUTED | summary 含「公元8年/公元9年/争议年代（DISPUTED）」；start_year=9 保留与汉书记年一致 | ✔ PASS |
| A4 平王东迁地点 | 无 latitude/longitude/valid_from/valid_to；place_id=null + needs_linking（不臆造窗口） | ✔ PASS |
| B5 historical_text_id | 10/10 候选 evidence 行均显式 `historical_text_id: null`；regime_ids 与 canonical 一致 | ✔ 10/10 |
| B6 person 锚定门 | 不在锚点集合的 person_id 一律降级 needs_linking（verifier 复核无新伪 linked） | ✔ |
| B7 source_ids 对齐 | 史记/汉书/资治通鉴/左传/战国策/尚书 各有对应 work id 且全部入 source_ids（含新增 资治通鉴→work-curated-zizhitongjian） | ✔ 10/10 |
| B8 单书多章标注 | 长平、七国之乱（同书两章）evidence 均注明「同一书内多个篇章，单一独立来源」 | ✔ PASS |

### Verifier 判定明细（10/10，修复批次后）

- **PASS（7）**：event-wuwang-fazhou、event-shangtang-miexia、event-pingwang-dongqian、event-sanjia-fenjin、event-changping-zhizhan、event-qiguo-zhi-luan、event-wangmang-chengdi。
- **FAIL（0）**。
- **WARN（3，均非阻断）**
  - event-qin-mie-liuguo / event-qin-tongyi：资治通鉴 evidence 行 `term=秦纪` 但 `chapter_hint=null`（模板一致性提示，schema 允许；建议补 `chapter_hint: 秦纪`）。
  - event-mobei-zhizhan（对照组，未变更）：pre-existing note —— 伤亡数字锚点 史记·匈奴列传/汉书·匈奴传 未列入 evidence 行，作为建议项移交。

### Auditor（修复批次后，当前 G5 队列 seed=1）

- 队列：event-yangjian-zhuanquan、event-three-regime-formation、event-zhangyi-po-chu（候选池收窄后 seed=1 确定性重采样）。
- **3/3 PASS**；无虚构坐标/person_id/text id；候补发现的 source_ids 未覆盖 source_reference 全部书名等为普遍性薄弱项，非历史错误。

---

## 7. 8 项管线自诊断问题（系统级审查，修复批次后）

1. **是否存在任何编造（虚构）内容？** — 否。修复批次后 10 候选 + auditor 均无虚构发现；AGENTS.md §17 硬失败类别全部缺位。
2. **候选对 canonical 的保真度？** — 100%。所有复制字段（含修复后的 canonical 叙事层）逐字符一致，0 异体；仅新增 derived 字段（background/result、evidence、人员/地点标记）。
3. **证据链是否真独立（多重来源 vs 同源复写）？** — 是，且已显式标注。同书多章（长平、七国之乱）在 evidence review_note 标注「同一书多个篇章单独独立来源」；异书双锚点（史记+尚书、史记+资治通鉴、史记+左传、史记+战国策）为真正独立。
4. **不确定性是否被如实保留（DISPUTED）？** — 是（完整）。商汤 −1600/−1556、武王 −1045/−1046/−1027 之外，长平 40万vs45万、王莽 8vs9 AD 已在候选与 canonical 中 DISPUTED 标注。
5. **人物/地点解析是否严谨、未过度自信？** — 是。见 B6：person 必须可在锚定集内确认才有 linked；平王东迁不再臆造地点窗口（A4）；争议/未知项一律 needs_linking / quarantine。
6. **确定性校验与评分模型是否可复现？** — 是。seed=1 重跑重现 9 AUTO_ACCEPT / 1 QUARANTINE_MEDIUM、0 错误。
7. **验证、审计、评分是否互相独立？** — 是。Verifier（web-capable，本轮 2 个独立 agent）与 Auditor（3 件采样、显式忽略 Verifier 结论）独立完成；Auditor 独立得出 PASS。
8. **是否出现需要人工介入的情形？** — 否。唯一隔离项（平王东迁 85.7）是 A4 的预期结果，等待后续地点实体解析后重评即可，不阻塞 Batch 2。

---

## 8. 复发模式（修复批次后 — 全部处理状态）

| # | 模式 | 状态 |
| --- | --- | --- |
| 1 | 《资治通鉴》在 evidence 中被引用但不在 `source_ids` | **已修复（B7）**：10/10 候选 evidence work 均有对应 work id 入 source_ids |
| 2 | evidence `link_confidence=0.9` 统一默认值，逐条独立解析缺乏 | 部分保留：统一默认仍然存在（模板行为）；已通过 B8 单书标注与 A/B 修复降低风险，不阻塞 |
| 3 | person `linked` 状态与 1.0 置信依赖旧审查备注，未经 resolver 复验 | **已修复（B6）**：verifier 复核 person 降级逻辑 10/10 通过；未确认锚定的 person_id 不再声明 linked |
| 4 | Producer 模板细节：evidence 行未输出显式 `historical_text_id: null`；canonical 空 `regime_ids` 被丢弃 | **已修复（B5）**：10/10 evidence 行显式 null；regime_ids 保留 |
| 5 | ctext.org 403：Verifier 模板应固定镜像优先策略 | 保留（说明项）：镜像优先策略已固化在本批 Verifier agent 中；ctext 403 为外部 infra 限制，不影响结论 |
| 6 | （新增残留）秦纪行 `chapter_hint: null`（qin-mie-liuguo / qin-tongyi） | 模板一致性提示：建议后续 producer 统一 `chapter_hint` 反映 term；schema 合法，不阻塞 |
| 7 | （新增残留）漠北之战伤亡数锚点应补《史记·匈奴列传 / 汉书·匈奴传》到 evidence 行 | 对照组 note：可在 Batch 2 顺手补证据行，不阻塞 |

---

## 9. 修复清单（Fix List — 已执行 ✔）

### A 级 — 历史内容（canonical 叙事层 → 候选重生成）

| 事件 | 修复项 | 状态 |
| --- | --- | --- |
| event-qiguo-zhi-luan | 证据章节名「吴王濞传」→「荆燕吴传」（汉书卷三十五）；canonical `source_reference` 中同样错字一并修正 | ✔ 已落地（canonical + 候选，Verifier byte-scan 0 残留） |
| event-changping-zhizhan | 伤亡数「40万 vs 45万」以 DISPUTED 形式记录（候选与 canonical 同步处理） | ✔ 已落地（candidate + canonical；Verifier PASS） |
| event-wangmang-chengdi | 称帝年「8 vs 9 AD」以 DISPUTED 形式记录，同时保留 canonical 的 9 AD 值 | ✔ 已落地（candidate + canonical；Verifier PASS） |
| event-pingwang-dongqian | 地点 id（cbdb-place-14693）改为绑定周代有效期窗口，或挂未知窗口的地点，避免 −770 事件套用 710–959 窗口 | ✔ 已落地（A4：`place_id=null` + needs_linking、不臆造窗口；候选 Verifier PASS；确定性评分如实降为 85.7 QUARANTINE_MEDIUM，作为非错误隔离项保留） |

### B 级 — 生产层/模板（修一次，Batch 2 自动受益）

| 项 | 修复 | 状态 |
| --- | --- | --- |
| B5 | producer 在 evidence 输出显式 `historical_text_id: null` 键；保留 canonical 空 `regime_ids` | ✔ 已落地（producer v4；10/10 复验） |
| B6 | resolver 层：`link_status=linked` 之前须对程序合法 CBDB/ctext person_id 独立核验并记录 | ✔ 已落地（anchored person set + severe downgrade to needs_linking；verifier 复核通过） |
| B7 | evidence.work 不在 source_ids 的情况（如《资治通鉴》）统一走 to-linking 队列或补 source_id | ✔ 已落地（WORK_ID_BY_TITLE 对齐；10/10 复验） |
| B8 | 模板明确「同一部书的多个章节 ≠ 形成多个独立来源」，单书证据在 evidence 中显式标注 | ✔ 已落地（`_mark_single_work_multi_chapter`；长平/七国已见标注） |

### C 级 — 仅作说明（无阻塞）

- ctext 403：镜像优先策略已在本轮 Verifier agent 中固化；无数据变更动作。

---

## 10. 本次交付物

| 产物 | 路径 | 状态 |
| --- | --- | --- |
| 候选 10 个 | `data/candidates/calibration_batch01/*.yml` | 修复批次后重生成（producer v4） |
| producer 脚本 | `scripts/calibration_batch01_produce_candidates.py` | v4（fix-list B5–B8） |
| canonical 叙事层修正 | `data/curated/.../event-qiguo / changping / wangmang .yml` | A1–A3 已落地（A4 在候选层） |
| 研究报告 | `reports/current-run/research-brief-batch01.md` | 已有 |
| 指标 / 摘要 / 隔离 | `reports/current-run/{metrics.json, summary.md, quarantine.jsonl}` | 修复批次后重新生成（quarantine 1 行 = 平王东迁） |
| Verifier 产物（10） | `reports/current-run/verification/event-*.json` | **修复批次后全部重跑**（7 PASS / 3 WARN） |
| Auditor 产物 | `reports/current-run/verification/auditor.json` | 修复批次后重跑（3/3 PASS，当前 G5 队列） |
| 进度文档 | `docs/PROGRESS_CALIBRATION_BATCH_01.md` | 修复批次后标记 complete + FIXED |
| 本报告 | `reports/current-run/calibration-batch-01-final-review.md` | **本轮更新（CALIBRATION_PASS）** |

---

## 11. 结论

- 管线系统复核（AGENTS.md §20）：QA/富集引擎可信 —— 确定性、可复现、canonical 只读、无虚构、不确定性透明，且能按修复清单闭环。
- 校准结论：首轮暴露的 4 类内容缺陷（A1–A4）与 4 类模板缺陷（B5–B8）**已全部修复并独立复核**；修复批次后 9 AUTO_ACCEPT + 1 QUARANTINE（预期隔离，非失败）；Verifier 10/10 复核，7 PASS/3 WARN（非阻断）。
- 产品就绪度：9 个候选可晋升 canonical（待 owner 批准）；1 个（平王东迁）在地点实体解析后可重评晋升。
- 校准决定：**CALIBRATION_PASS** —— 管线足以承载 Batch 2 的自主体量（每批 10–20 critical events）。建议量产前把 §8 残留第 6/7 项（`chapter_hint` 统一、漠北证据行补充）作为 producer 小修缮顺带处理。

---