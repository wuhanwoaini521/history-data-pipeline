# Knowledge Layer Audit — historical_texts 重建前置审计

> 生成：2026-09-11（History V2 · 知识层重建第一轮）
> 范围：`history-data-pipeline` 子仓库全部代码调用链 + 本机数据目录实况 + NiuTrans 上游仓库实测。
> 方法：所有结论来自代码调用链（file:line）与真实仓库/目录核实，非文件名推断。

---

## 1. 现状（Before）

| 指标 | 值 | 出处 |
|---|---|---|
| dist `historical_texts` | **0** | manifest / build 默认 seed-only |
| dist `event_evidence` | 130 条（linked=0） | manifest counts |
| evidence `pending_knowledge` | 26 | manifest reference_resolution |
| evidence `needs_linking` | 104 | 同上 |
| Layer 2 知识库 `data/normalized/history.duckdb` | **不存在**（本机无文件） | `ls data/` |
| `data/raw` / `data/staging` | **空目录**（gitignored，从未落盘） | `find data/raw data/staging` → 空 |
| works（curated seeds） | 49 部 | `backbone/reference.py:270-328` |
| 完整度 | 618 事件平均 30.9 分，≥90 分 0 个 | PRODUCT_COVERAGE.md |

## 2. 设计上的数据流（应然链路）

```text
NiuTrans/Classical-Modern (GitHub, MIT)
   ↓ downloaders.py: resolve_niutrans() → _download_one(extract=True)
data/raw/classical-modern/<version>/Classical-Modern-<branch>.zip
   ↓ 解包到 <snapshot>/repository/（downloaders.py:141-145）
repository/双语数据/<书>/<卷类>/<篇卷>/source.txt|target.txt   ← 句对齐双语
repository/古文原文/<书>/<卷>/text.txt                        ← 仅文言原文
   ↓ parsers.py: iter_classical_modern()（读 source/target 行对）
data/staging/classical-modern/*.jsonl（source_path, line_number, original_text, translation_zh_cn）
   ↓ real_build.py: build_from_staging() → data/normalized/history.duckdb（Layer 2）
historical_texts（chapter=篇卷目录名, section=None）+ works（书级）
   ↓ backbone build --knowledge data/normalized/history.duckdb
   ↓ build.py:187-198 ATTACH (READ_ONLY) + INSERT OR REPLACE 六表
dist/history.duckdb → self-tools 桌面应用
```

## 3. 缺失位置（按链路顺序）

| # | 环节 | 现状 | 定位 |
|---|---|---|---|
| 1 | raw 快照 | 无（未下载） | `data/raw/` 空 |
| 2 | staging 解析 | 无 | `data/staging/` 空 |
| 3 | Layer 2 知识库 | 不存在 | `data/normalized/` 缺失 |
| 4 | dist 并入 | **默认关闭** | `cli.py:389-392` 注释明确"Knowledge Store（Layer 2）等待 V2 重建"，仅显式 `--knowledge` 才 ATTACH（`build.py:187-198`） |

## 4. 根因

**不是 build 阶段丢弃，而是上游数据从未进入管道。**

1. NiuTrans 原始数据（GitHub ~410MB）从未在本机下载（raw 快照 gitignored 且当前为空）。
2. Layer 2 知识库因此无法构建。
3. dist 构建自 V2 重构起改为 seed-only 默认（`cli.py:389-392`），`historical_texts` 只有 seeds 途径可进来，而 seed rows（`reference.py:knowledge_seed_rows`）只含 people/places/works，**没有 texts**。
4. 结论：链路代码完整存在（§2 全链都有实现），缺的只是"喂入数据 + 执行"。

## 5. 可恢复的数据（上游实测，2026-09-11）

NiuTrans/Classical-Modern @ `main` = `4e746ea9fa99c3c0d7051c45397330bef7b0962d`
（最后推送 2024-04-21T16:20:37Z，~410MB，MIT License，仓库结构三层：`双语数据/`、`古文原文/`、`复现/`）。

### 5.1 双语数据（可翻译对照，97 部书 / 7,304 个篇章文件 / 1,990 个篇章目录）

目录层级：`双语数据/<书名>/<卷类>/<篇卷>/source.txt + target.txt + bitext.txt + 数据来源.txt`
（如 `双语数据/史记/十二本纪/秦始皇本纪/`、`双语数据/元史/本纪/卷一/`、`双语数据/资治通鉴/秦纪/秦纪一/`）

**每部书天然具备 document（书名）→ part（卷类：本纪/列传/志/某纪）→ chapter（篇卷）→ 行级句对 三级结构** —— 旧构建把"篇卷"目录名写入 `chapter`、`section` 恒为 null（`real_build.py:66`），卷类层级被丢弃，本轮恢复时可以补全。

### 5.2 古文原文（无对照翻译，190 部书 / 13,913 个 text.txt）

层级：`古文原文/<书名>/<卷>/text.txt`。含 `三朝北盟会编`（双语数据中没有）。

### 5.3 与 curated works 注册表的重合（49 部中 28 部有语料）

- ✅ 覆盖（28）：史记、汉书、后汉书、三国志、资治通鉴、旧唐书、新唐书、左传、国语、尚书、战国策、晋书、宋书、梁书、陈书、魏书、北齐书、周书、南史、北史、隋书、旧五代史、新五代史、辽史、宋史、金史、元史、明史 —— **全部前近代正史主干齐备**。
- ❌ 无语料（21）：春秋、竹书纪年、续资治通鉴长编、明实录、清史稿、清实录、筹办夷务始末、中华民国史、中国抗日战争史、三朝北盟会编（仅古文原文）、蒙古秘史、元朝史、东晋门阀政治、元末明初的江南社会、辛亥革命回忆录、南京大屠杀史料集、中国共产党历史、二十世纪中国史纲、中国现代史、秦汉史、秦汉史略。

### 5.4 与 10 个 QUARANTINE 事件的直接关系

| 事件 | 证据 work | NiuTrans 覆盖 | 章节映射路径 |
|---|---|---|---|
| event-mongol-jianguo | 元史·太祖纪 | ✅ 元史/本纪/卷一…卷三十七 | 需"卷一=太祖"卷号映射（见 §7） |
| event-western-xia-jianguo | 宋史·夏国传 | ✅ 宋史/列传（198 文件） | 需核对列传篇名是否含"夏国传" |
| event-yuan-jianguo | 元史·世祖纪 | ✅ 元史/本纪 | 需"卷X=世祖"卷号映射 |
| 九一八/南京大屠杀/五四/西安事变/日本投降/新中国成立 | 中华民国史、中国抗日战争史、南京大史料集等 | ❌ 全部不在语料 | 知识层无法解锁，保持 NEEDS_SOURCE（§7） |

即：**知识层重建可直接验证/解锁 3 个前近代 QUARANTINE 事件的章节核实，7 个 20 世纪事件仍然需要独立来源**——本轮目标因此调整为"验证链路可用"，不是清零 quarantine。

## 6. 需要新增的数据

1. **纪传体卷号 ↔ 纪名映射**（元史卷一=太祖、卷四=世祖前的忽必烈用卷四？等）——以可靠通行版本（《元史》中华书局点校本目录）为准，建立 curated alias 表并注明依据，属于人工可解释映射，不是 fuzzy。
2. **20 世纪现代史著作的章节目录**（7 个 QUARANTINE 事件阻塞项）——本轮**不虚构**，状态保持 NEEDS_SOURCE；后续由人工提供可信目录页后补充。
3. 无其他必须新增的上游数据源（CBDB/CText 与本轮无关，不下载）。

## 7. 风险

| 风险 | 缓解 |
|---|---|
| text_id 稳定性：ID=sha1(source_path:line_number)，路径漂移会改变 ID | 锁定快照版本 `20240421`（commit 4e746ea，2024-04 后仓库无更新）；raw 快照永不覆盖；解析层不做路径重写 |
| dist 体积膨胀（legacy 全语料曾 575MB） | 导入范围 = curated 证据实际引用的 works（28 部双语书 + 命中的古文原文书），而非全量 287 部；规则确定性、可重建 |
| 运行时互联网依赖（禁止项） | 下载是独立的 raw 快照步骤（downloaders 既有设计）；build/link 全程只读本地文件 |
| 重复行 / 不可重复 build | id 确定性 + INSERT OR REPLACE；Gate D 连续两次 build 计数校验 |
| fuzzy 误链（错误链接比 NULL 更严重——reference.py 文头原则） | match_method/confidence 分级，fuzzy 只进 candidates 与报告，不写 linked；exact/normalized_exact 之外的自动写入一律禁止 |
| schema `additionalProperties:false` | YAML/dist/schema/loader 四处同步扩展，先改 schema 再写数据 |
| 20 世纪证据缺口 | 明确输出 NEEDS_SOURCE 清单，不编造章节号（对齐 AGENTS.md §7/§17 硬性失败条款） |

## 8. 推荐实现（阶段二设计，待执行）

1. **知识层构建器**（新模块 `knowledge_build.py`，复用 `real_build.py` 的 ID/工作表方案并补全层级）：
   `raw/classical-modern/20240421/repository/双语数据/**/source.txt(+target.txt)` →
   `staging/knowledge/historical_texts.jsonl`（含 document/part/chapter/paragraph_index/数据来源）→
   `data/normalized/history.duckdb`（SCHEMA_SQL；只建 sources/works/historical_texts，不再全量 CBDB/CText）。
2. **dist 并入零改动**：现成的 `backbone build --knowledge data/normalized/history.duckdb`（`build.py:193-197` 已拷贝 works/historical_texts）。
3. **schema 扩展**（最小增量，复用现有体系）：
   - `historical_texts`：现有列沿用（`title_zh_cn`=document, `chapter`=篇卷, `section`=卷类 part）；新增 `paragraph_index INTEGER`（行号）、`source_path VARCHAR`（原始路径可追溯）。旧语义变更需在 schema 注释说明（dist 从未含 texts，无兼容负担）。
   - `event_evidence`：新增 `chapter_anchor`（章级定位 "卷类/篇卷"）、`claim_field`（background/process/result/impact/people/places，可空）、`link_method`（exact/normalized_exact/alias/fuzzy/manual）。YAML 同步扩 `event_evidence.schema.json`。
4. **source_reference_normalizer**（新模块 `backbone/source_reference.py`）：解析 `《作品·篇章》`、`卷十二/卷12/第十二章/Chapter 12` 等形态 → (work, part, chapter)；输出 confidence + match_method（exact/normalized_exact/alias/fuzzy/manual）；不过度模糊。
5. **证据锚定**（新模块 `backbone/evidence_link.py`）：event evidence (work, term, chapter_hint) → 章级 anchor（章首行 text_id 为代表行 + `chapter_anchor` 记全路径）；exact/normalized_exact 自动写回，fuzzy 仅 candidates+报告。
6. **CLI**：`history-data knowledge build`；`history-data backbone link-evidence --dry-run|--apply`。
7. **测试**：解析器层级/ID 稳定、重复 build 幂等（Gate D）、归一化器枚举用例（§六 prompt 列出的全部形态）、fuzzy 不自动进正式链、现有 343+ 全部测试保持绿。

## 9. 环境事实（本次执行相关）

- 上游仓库可下载（codeload 直链可用；GitHub API 有限流，`resolve_niutrans` 的 API 依赖在限流时段需按 §8.1 以固定版本手动落快照，metadata/checksum 与 `_download_one` 输出格式一致）。
- 本机带宽实测 ~300KB/s（410MB ≈ 25 分钟）。
- 运行环境：uv + Python 3.12 venv（`.venv`），依赖 duckdb/PyYAML/jsonschema/pytest。
