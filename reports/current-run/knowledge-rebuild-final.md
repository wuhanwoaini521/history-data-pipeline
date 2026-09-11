# Knowledge Rebuild Final Report — History V2 知识层重建与证据链恢复

> 生成：2026-09-11 · 本轮工作：重建 `historical_texts` 知识层 → 恢复 evidence 锚定链 →
> 重处理 QUARANTINE → 全量 linking 报告。前置审计见 `knowledge-layer-audit.md`。

---

## 一、Before / After

| 指标 | Before | After | 备注 |
|---|---:|---:|---|
| dist `historical_texts` | **0** | **730,128** | 29 部书（双语 28 + 古文原文 1），document/卷类/篇卷/行 四级 |
| dist `works` | 49 | 49 | 全部映射到 curated work id，无同名重复行 |
| event_evidence `linked` | 0 | **74** | exact 27 / content 42 / alias 5 |
| `pending_knowledge` | 26 | 22 | 原 26 中 4 条被锚定；22 条 legacy 悬空 id 如实保留 |
| `needs_linking` | 104 | 34 | 含 27 条 fuzzy 候选（仅报告，未写回） |
| knowledge 层元数据 | — | chapter_heads 3,838 | 章首行索引，供确定性内容核实 |
| QUARANTINE | 10 | 10 | 其中 2 条 +1.0 分（88.7），0 条越过 90，门槛未降 |
| `chapter_anchor` / `link_method` / `claim_field` | 无 | 已入 schema + dist + YAML | 证据可回答"哪一章、哪个字段" |

## 二、Pipeline（本轮落地）

```text
NiuTrans/Classical-Modern @ 4e746ea (MIT, 2024-04-21)
  ↓ raw 快照（data/raw/classical-modern/20240421/，gitignored，metadata+sha256 全记录）
  ↓ 逐文件 raw.githubusercontent 并行抓取（10764 文件，bitext 不需要）；断点续传脚本 /tmp/fetch_niutrans*.sh
repository/双语数据/<书>/<卷类>/<篇卷>/source.txt+target.txt
  ↓ knowledge_build.py（CLI: history-data knowledge build）
  ↓   text_id = text-niutrans-sha1(source_path:line)[:20]（与 legacy 同构 → 确定性）
  ↓   section=卷类 chapter=篇卷 paragraph_index=行号 source_path=原始路径
data/staging/knowledge/historical_texts.jsonl → data/normalized/history.duckdb（Layer 2）
  ↓ backbone build --knowledge data/normalized/history.duckdb（既有 ATTACH 拷贝路径，零改动）
  ↓ source_reference.py（引用解析）+ evidence_link.py（分级匹配）+ chapter_aliases.json（人工卷号映射）
  ↓   匹配阶梯：alias → exact → normalized_exact → content(章首行核实) → fuzzy(仅报告)
  ↓   写回规则：exact/normalized_exact/alias/content 才写回；fuzzy 一律只进候选
dist/history.duckdb（730,128 texts + 74 linked evidence）→ self-tools 桌面应用
```

**build 重复性（Gate D 实测）**：knowledge build 连续两次 → texts 730,128/730,128（COUNT=DISTINCT）；
dist 连续两次 build → texts/linked/events 计数逐位一致，无重复行。

## 三、Gate 核验

| Gate | 结果 | 证据 |
|---|---|---|
| A historical_texts > 0 且非测试数据 | ✅ | 730,128 行 / 29 书 / 3,838 章 |
| B source→chapter→paragraph→evidence→event 全链查询 | ✅ | dist SQL join 五表直查（含 license），见 §四样例 |
| C 5 个典型事件端到端 | ✅（含诚实缺口） | §四 |
| D build 可重复、无重复行 | ✅ | 上文实测 |
| E 全部测试通过 | ✅ | Python: 236 passed / 16 skipped / 0 failed（新增 30）；Rust: 200 passed / 0 failed |

## 四、Sample：5 个端到端样例（Event → Source → Chapter → Evidence text）

1. **古代 · 商汤灭夏（event-shangtang-miexia）**
   Source：《尚书·汤誓》（source-classical-modern, MIT）→ Chapter：商书/汤誓 →
   原文首段「伊尹相汤伐桀，升自陑，遂与桀战于鸣条之野，作《汤誓》。」→
   今译「伊尹辅佐商汤讨伐夏桀……」→ method=exact (1.0)。
2. **古代 · 秦灭六国（event-qin-mie-liuguo）**
   《史记·秦始皇本纪》→ 十二本纪/秦始皇本纪 → 章首段锚定，method=exact；
   同事件《资治通鉴·秦纪》→ part 级命中 → 锚 秦纪/秦纪一 首段。
3. **唐 · 李渊称帝、唐朝建立**
   《资治通鉴·唐纪》→ 唐纪/唐纪一 → method=exact (part 级)；
   同时代《旧唐书》本纪多篇经 content 核实锚定。
4. **明 · 鄱阳湖之战、陈友谅覆灭（event-poyanghu-zhizhan）**
   《明史·陈友谅传》→ content 命中 列传/卷十一，章首「陈友谅，沔阳渔家子也。」（传记开篇原文）；
   《明史·太祖纪》→ alias → 本纪/卷一（语料首行「◎太祖一太祖开天行道肇纪…讳元璋」）。
5. **晚清 / 20 世纪 · 第一次鸦片战争 / 九一八（诚实缺口展示）**
   第一次鸦片战争：《清实录·宣宗实录》《筹办夷务始末·道光朝》→ 两书不在语料 →
   保持 needs_linking（报告列为 missing knowledge）；九一八（QUARANTINE 候选）→
   中华民国史等现代史著作缺失 → 候选分值不变、保持 QUARANTINE。
   —— 端到端验证同样覆盖"知识层缺失时的正确行为"：明确缺口，不编造。

## 五、Tests

| 层 | 文件 | 覆盖 |
|---|---|---|
| pipeline | tests/test_knowledge_build.py（4） | 层级解析/ID 确定性/双 build 幂等（Gate D）/curated work 去重映射 |
| normalizer | tests/test_source_reference.py（14） | 中文数字互转、第十二章/第12章/十二章/卷十二/卷12/Chapter 12 全形态、引文解析、分级匹配（exact/alias/normalized/unmatched） |
| linker | tests/test_evidence_link.py（12） | exact/alias/content/跨卷锚定/段级 fuzzy/带坐标 fuzzy 不写回（回归）/YAML 写回与注释保留 |
| schema | 既有 + 扩展 | event_evidence 新字段枚举（content 可自动写回，fuzzy 排除） |
| 全量 | 236 passed / 16 skipped | 16 skips = legacy 全量 Layer-2 测试（需 CBDB/CText raw，缺数据时跳过，skip 条件由"文件存在"收紧为"存在且有 people"） |
| Rust | cargo test 200 passed | infrastructure 语义套件 + 缺失文件显式报错 + 导航往返，全绿 |

本轮修复的既有测试（环境前提变化，非逻辑回归）：
`test_resolution_no_broken`（seed-only 下 linked evidence 无法核实 → 降级 pending 而非 broken）、
`test_query_service` / `test_semantic_layer`（skip 条件收紧）、
`test_v22_*`（NameIndex 无 legacy 库时回落 dist people 种子；排除表测试注入 stub 不再依赖真实噪声人名）。

## 六、Git changes（逐文件）

**src/history_data_pipeline/**（pipeline 核心）
- `knowledge_build.py`（新增）：Layer 2 构建器（双语+古文解析、章首表、works 去重、确定性 ID）
- `backbone/source_reference.py`（新增）：引文解析 + 中文数字/卷号归一 + CitationResolver 分级匹配
- `backbone/evidence_link.py`（新增）：KnowledgeIndex、四级匹配阶梯、段级 fuzzy 检索、YAML 写回（保头尾注释）
- `backbone/reference.py`：works 种子表提升为 `CURATED_WORK_SEEDS` 常量；seed-only 下 linked evidence 降级 pending（不再 broken）
- `backbone/build.py`：dist `event_evidence` 增加 chapter_anchor / claim_field / link_method 三列并透传
- `database.py`：`historical_texts` 增加 paragraph_index / source_path
- `real_build.py`：legacy 文本迭代器同步补两列
- `cli.py`：`knowledge build` 命令组；`backbone link-evidence`（--apply）；补 `__main__` 入口

**schemas/**：`event_evidence.schema.json` + `event.schema.json` 内联 evidence 增加
chapter_anchor / claim_field / link_method（additionalProperties 同步放开）

**data/curated/history_backbone/events/**（47 事件 YAML）：74 条 evidence 写回
`historical_text_id + chapter_anchor + link_method + link_status=linked`（文件头尾注释保留）

**data/candidates/batch04,06,07/**（10 个 QUARANTINE 候选）：知识层锚定写回（3 条命中）

**data/curated/knowledge/chapter_aliases.json**（新增）：4 条人工卷号映射，每条附语料内容核实证据

**tests/**：新增 test_knowledge_build / test_source_reference / test_evidence_link；
修正 test_backbone / test_query_service / test_semantic_layer / test_v22_major_person_links 的环境前提

**scripts/**：`quarantine_rescore_after_knowledge.py`（新增，可重跑）；`v22_major_person_links.py`（KB 空层回落 dist）

**reports/current-run/**：knowledge-layer-audit.md、quarantine-after-knowledge-rebuild.md(+json)、
evidence-linking-report.md、本报告；BACKBONE_COVERAGE.md 再生成

**data/raw/classical-modern/20240421/**（gitignored，不入库）：NiuTrans 快照
11,017 文件 + metadata.json（commit 4e746ea）+ checksum.sha256

## 七、Remaining blockers（因缺乏可靠 source 无法解决）

1. **20 世纪档案类著作整部缺失**：中华民国史 / 中国抗日战争史 / 南京大屠杀史料集 / 中国共产党历史 /
   二十世纪中国史纲 / 清实录 / 清史稿 / 明实录 / 续资治通鉴长编 / 筹办夷务始末 / 辛亥革命回忆录 /
   蒙古秘史 / 元朝史 —— 不在 NiuTrans。需人工提供可信章节目录（目录页/电子文本），按转写规则补录；
   在此之前相关 evidence 保持 NEEDS_SOURCE，相关 QUARANTINE 保持 QUARANTINE。
2. **语料卷覆盖不全**：晋书 47/130、旧唐书 120/200 等 —— 段级/列传级证据锚定受限于语料；
   若后续换用更全的语料源（如 ctext 官方文本），需重新评估许可（CC BY-NC-SA 3.0，非商用）。
3. **22 条 legacy 悬空 text id**：旧知识库构建产物已不可复原，需人工按 work+term 重认
   （本工具链已给出可复核候选）。
4. **主题词型 term 的段级锚定**（27 条 fuzzy）：已给出候选段落，待人工确认 quote 后升级
   —— 按本轮铁律不自动写回。

## 八、下一阶段入口

按既定计划：`reports/ENRICHMENT_QUEUE.json` 的 **14 个 Critical**（同步补
background/process/result/impact/people/places/evidence）——现在每一条新补内容都可以走
`source → chapter → paragraph → evidence → event` 全链背书。
