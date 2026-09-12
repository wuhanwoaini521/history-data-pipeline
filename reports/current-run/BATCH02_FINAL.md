# History V2 Batch 02 Result

> 主题：Source Expansion & Critical Closure Batch 02 · 执行日 2026-09-12
> 原则：SOURCE-BACKED FIRST；新增事实均可回答「来自哪里/哪一卷/哪一段/为何支持该字段」。

## Status

**PASS**（2 个 Critical 因许可/文献缺口保持 NEEDS_SOURCE —— 属合法结果，非失败）

## Git State

| 仓库 | 值 |
|---|---|
| self-tools（main repo） | `main` @ `403d5fd`，与 origin 一致；除子模块指针外 clean |
| history-data-pipeline（submodule） | `main` @ `22158dc`（已推送）；工作区 **dirty（本轮全部产物，未提交）** |
| dirty 明细 | 37 modified（33 curated event YAML + build.py + evidence_link.py + knowledge_build.py + coverage 报告×5）+ 33 untracked（batch02 报告×15 + 脚本×4 + parser×1 + tests×1 + overnight 遗留×12） |

未做任何 reset/rebase/checkout/clean。上一轮 overnight 未提交改动（审计确认合法）已随本轮一起保留在工作区。

## Critical Closure（Queue 2）

| event | Before | After | relation_added |
|---|---:|---:|---:|
| event-chuzhuang-wang-ba 楚庄王称霸 | 88.9 | **100.0** | 2（follows 晋文公 / follows 城濮之战） |
| event-jinwen-gong-ba 晋文公称霸 | 88.9 | **100.0** | 3（follows 齐桓公 / caused_by 城濮 / precedes 楚庄王） |
| event-hezong-lianheng 合纵连横 | 88.9 | **100.0** | 3（follows 商鞅变法 / precedes 张仪欺楚 / leads_to 秦灭六国） |

8 条新边全部为 schema 白名单内策展关系，附语料引文（如 商君列传#p88「秦人富彊，天子致胙」、鲁仲连列传#p169「晋文公亲其雠，彊霸诸侯；齐桓公用其仇，而一匡天下」）；
语料无据的候选（楚庄王→鄢陵之战等）主动放弃，未硬加。

## Source Expansion（Queue 4–8）

| 项 | 值 |
|---|---|
| new source | **`source-wikisource`（zh.wikisource）**，1 个（预算 1–3） |
| 接入方式 | page manifest（`config/wikisource_batch01_manifest.json`，10 页）→ raw snapshot → checksum → parser → normalized → historical_texts |
| snapshot | `data/raw/wikisource/20260912/`（原始字节 immutable） |
| license | 底本逐页判定：宋史（元代官修，PD）/ 降伏文書（国际文书不保护）/ 中央人民政府公告・共同纲领（著作权法§5 官方文件）/ 两份判决书（司法文件）/ 蒋介石文告（卒 1975 → 2026-01-01 起 PD）/ 五四宣言（罗家伦卒 1969 → 2020 起 PD）。载体现行排版 CC BY-SA 不改变底本判定 |
| checksum | `checksum.sha256` 10/10 verified；metadata.json 含逐文件 sha256/size/URL/acquired_at |
| parser | `src/history_data_pipeline/knowledge_wikisource.py`（确定性；text_id=`text-wikisource-`+sha1(file#pN)[:20]）；tests ×13 |
| quality gate | `scripts/source_quality_gate_wikisource.py` → **PASS**（9 项检查：计数/空文本/重复段落/重复 ID/层级/孤儿/编码/残留/顺序） |

入库文档：9（宋史卷485・486 夏国传上下；降伏文書；卢沟桥谈话×2；谷寿夫主判决+百人斩判决；中央人民政府公告；共同纲领；五四宣言）。
体积：**0 volumes（不适用）· 2 chapters（宋史卷485/486）· 9 documents · 362 paragraphs**（原文保留繁体，简化为派生列）。

禁止来源（百度百科/知乎/自媒体/AI 生成等）零使用；许可不明页（九一八政党决议）仅留档不入 canonical。

## Knowledge Layer

| | Before | After |
|---|---:|---:|
| historical_texts | 730,128 | **730,490**（+362，零扰动） |
| DISTINCT id | 730,128 | 730,490 |
| 双次构建一致性 | — | texts/distinct/id-digest 两次相同（id 集合 SHA1 `beaf13401c111535`） |
| works | 49 | 55（+6 独立文书） |

## Evidence

| | Before | After |
|---|---:|---:|
| event_evidence total | 154 | **184** |
| linked | 98 | **149** |
| — manual（段落精确锚） | 24 | **75** |
| — content | 42 | 42 |
| — exact | 27 | 27 |
| — alias | 5 | 5 |
| needs_linking | 34 | 34 |
| pending_knowledge | 22 | **1** |
| fuzzy 写回 | 0 | **0**（永远 candidate-only） |
| chapter_anchor 含 #p | 24 | **75** |

Queue 11 legacy cleanup：22 条 → **21 recovered**（旧 id 全部悬空不可逆，按「章节+内容双核实」重定位到新段落锚，逐条引文可回查）、**1 manual_candidate**（收复长安，语料无核心段）、0 fuzzy 写回、0 unresolved。
事故与恢复：`link-evidence --apply` 曾把 24 条 manual 段落锚降级为章首锚 → 已从备份精确恢复，并修复 apply_links（跳过 manual 行），不可复发。

## Critical

| | Before | After |
|---|---:|---:|
| queue 优先级 Critical | 8 | **2**（九一八事变、西安事变） |
| importance=critical 完整（≥90） | 3 | **9** |
| 全部 ≥90 完整条目 | 3（0.5%） | **12（1.9%）** |
| 6 个新关闭 | — | 西夏建国 / 七七事变 / 日本投降 / 南京大屠杀 / 新中国成立 / 五四运动，全部 22.2 → **100.0**，evidence 全部 manual 段落锚 + 逐字引文 |

## Legacy Cleanup

legacy total **22** · recovered **21**（content 级 21）· manual_candidate 1 · unresolved 0 · fuzzy 写回 0。

## Places

Before 37（linked 3 / needs_linking 34）→ After **52**（linked 3 / needs_linking 49）。新增 15 条全部为 Critical 事件必要地点，按历史属性登记（宋边路分/城门/海湾/和谈标的等），未强映射现代城市，**未猜任何坐标**。

## Product Coverage

| 指标 | Before | After |
|---|---:|---:|
| average | 31.6 | 32.3 |
| critical 平均 | 63.8 | 70.3 |
| 背景 % | 9.2 | 10.2 |
| 过程 % | 1.0 | 1.9 |
| 结果 % | 13.4 | 14.4 |
| 影响 % | 1.0 | 1.9 |
| 人物 % | 42.7 | 42.7 |
| 地点 % | 5.2 | 6.1 |
| 证据 % | 13.4 | 14.4 |
| 关联事件 % | 98.2 | 98.7 |

（平均分只 +0.7：555 个 Major 本轮明确未动；成功标准是供应链扩张而非平均分。）

## Major Batch 01（只选不富化 · 30 个）

**READY 16（进入下一轮）**：安史之乱群 8（uprising/兼领三镇/洛阳/潼关/长安/玄宗入蜀/史思明/平定）+ 楚汉群 8（秦末起义/巨鹿/秦亡/鸿门/彭城/荥阳/垓下/刘邦建汉）。
**PARTIAL_SOURCE 9（先补链接）**：唐 1（收复长安，evidence 待审）+ 明 6（建文即位/宁王之乱/陕西民变/皇太极继位/蓝玉案/李自成发展，明史在库）+ 西汉 2（剪除异姓王/王莽复出）。
**NEEDS_SOURCE 5（等待 source 批次）**：晚清（戊戌变法/同盟会/左宗棠西征/金田起义/天京陷落——清实录・清史稿缺库）。

## Tests

| 命令 | passed | failed | skipped |
|---|---:|---:|---:|
| `pytest tests/ -q` | **249** | 0 | 16 |
| `cargo test --workspace` | **200**（31+70+99） | 0 | 0 |
| `npx tsc --noEmit` | exit 0 | — | — |

新增 parser 测试 13；4 处硬编码计数按数据合法增长更新并注明。测试后已按 `backbone --knowledge` 重建 dist（integrity：dangling anchors=0、dangling relations=0、ID 全域唯一、checksum 10/10）。

## Blockers（明确列出，不做模糊表述）

1. **九一八事变**：唯一候选文献为政党决议（1931-09-22），许可解释不明 → 不能写入 canonical。需要：许可明确的公版影印档案或官方文献集。
2. **西安事变**：张学良杨虎城通电在中文维基文库无页面；张学良（卒 2001）署名文献保护期未满（2052）→ NEEDS_SOURCE。需要：影印本公版文献或已过保护期的当事方文本。
3. **安史之乱·收复长安 evidence**：新语料无「收复长安」核心段（唐纪三十八搜索无果）→ 保持 1 条 pending/manual_candidate。需要：通鉴唐纪三十七「复两京」段或旧唐书郭子仪传补入。
4. **清实录 / 清史稿**：晚清 5 个选择事件与整个晚清 Major 群无法推进。清史稿（PD，维基文库全本 529 卷）可获取——建议列为下一 source 批次 P1。
5. **明实录 / 晋书缺卷 / 旧唐书缺卷 / 续资治通鉴长编 / 筹办夷务始末 / 辛亥革命回忆录**：34 条 needs_linking 的史源缺库（batch02-03 B 组）。其中 晋书/旧唐书 可经维基文库补卷（P1）。
6. **现代著作（中华民国史/中国抗日战争史/南京大屠杀史料集）受版权保护** → 永久只作 reference 引证，不得全文入库（政策既定，非本轮新增约束）。
7. **Fuzzy 27 条候选**（段级相似）按政策保持报告态，不写回——不是债务，是设计。

## 本轮新增运行纪律（已入 Queue 15 报告）

`pytest` 的 build 测试会把 dist 重建为 seed-only（历史行为）→ 运行清单固定为
**tests → `backbone --knowledge` 重建 → coverage 报告**，否则 dist 会停留在无知识层状态。

## 报告索引

batch02-00（git）· 01（baseline）· 02（critical closure）· 03（source gap inventory）· 07（quality gate）· 08（source build）· 09（evidence relink）· 10（critical recheck）· 11（legacy cleanup）· 12（places）· 13（coverage）· 14（major selection）· 15（tests）· 本文件。
政策：docs/source-acquisition-policy.md。

---

## 补记（Batch 02 收尾后继续执行：Major Batch 01 Enrichment）

用户确认继续后，执行了 batch02-14 所选的下一轮正式 enrichment（含补链接后的收复长安）：

- **17/17 READY 事件全部达到 100.0**（楚汉群 8 + 安史之乱群 9）：补 background/process/impact
  三维 + 71 条 manual 段落锚证据（逐字引文），legacy result 短句保留并补锚。
- **pending_knowledge 清零（1 → 0）**：收复长安的 legacy 悬空锚以「贼弃城走矣」段落关闭。
- dist：event_evidence **255**（linked 221 / needs_linking 34）· event_relations **1,067** ·
  historical_texts 730,490 不变 · 完整性 dangling=0 / checksum 10/10。
- 产品覆盖：**≥90 从 12 → 29**（major 3 → 20）；average 32.3 → **33.2**；
  过程/影响维度 1.9% → **4.7%**、背景 → **12.9%**、关联事件 → **98.9%**。
- 事故与修复：append 富化在 17 个既有 `people:`/`evidence:` 文件产生重复顶层键（PyYAML last-wins
  遮蔽旧行，dist 一度丢 17 条 evidence）→ `scripts/fix_duplicate_top_keys.py` 合并修复，
  0 重复键、旧行全部保留（event_person 398 不变）；脚本保留供后续预检。
- 测试：`pytest tests/ -q` **249 passed / 16 skipped / 0 failed**（计数更新：pending 221、
  relations 1067、evidence 255）。
- 报告：`reports/current-run/major-batch01-enrichment.md`。

**Batch 02 最终状态：≥90 = 29 / 618；Critical（queue 优先级）= 2（九一八、西安事变，许可/文献缺口）；
pending=0；后续队列：明 6 + 西汉 2（PARTIAL，明史在库待链接）、晚清 5（NEEDS_SOURCE，待清史稿接入）。**

---

## 补记二（Source Batch 02：清史稿/晋书/旧唐书补卷 + 29 事件富化）

- **新 source 扩容**：清史稿 16 卷 + 晋书 9 卷 + 旧唐书 3 卷（快照 `20260912b`，checksum 28/28，gate PASS）；
  多快照 parser 支持；historical_texts 730,490 → **733,372**。
- **needs_linking 30 → 14**（16 条重定位：晋书群/旧唐书/后汉书/旧五代史/魏书/明史）。
- **29 事件富化全部 100.0**：晚清/清初 10（含金田/天京/戊戌/退位/甲午/左宗棠）+ 明 5 西汉 2 + 晋书群 12。
- **完整条目（≥90）：29 → 58（9.4%）**；平均 33.2 → **35.4**；critical 完整 20 → 26（平均 79.6）；
  地点维度 6.1% → 10.8%、过程/影响 4.7% → 9.4%。
- 测试 **249 passed / 16 skipped / 0 failed**；完整性 0 dangling、checksum 双批 10/10 + 28/28。
- 详细报告：`reports/current-run/source-batch02-result.md`。

**当前 History V2 状态：618 事件中 58 个 ≥90；Critical（queue 优先级）2（九一八、西安事变）；
evidence 373（linked 359）；剩余 needs_linking 14 条均有明确缺源清单。**

---

## 补记三（Ready-43 Critical 冲刺）

- 六个 cluster 共 **43 事件全部 100.0**（先秦秦汉 12 / 唐 4 / 宋辽金 5 / 魏晋南北朝 6 / 明 8 / 三国 8），
  新增 196 条 manual 锚证据 + 4 条关系。
- **≥90：58 → 101（16.3%）**；平均分 35.4 → **37.8**；**critical 60/62**（仅九一八、西安事变因许可受阻）。
- 修复 5 处地点重复条目（validate 归零）；测试计数同步更新。
- 报告：`reports/current-run/ready43-batch-result.md`。

**History V2 当前状态：618 事件 / 101 个 ≥90 / critical 60/62 / evidence 569（linked 555）/ 14 条 needs_linking 待补源。**
