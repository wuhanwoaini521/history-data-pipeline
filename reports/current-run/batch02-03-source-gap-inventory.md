# Batch 02 · Queue 3 — Source Gap Inventory

> 目标：只盘点、不下载。逐事件列出缺失字段 → 首选/备选 source → 获取与许可现状 → 优先级。
> 知识层现状核对（dist/history.duckdb 实查）：29 部书；宋史含 本纪47/列传198/志4（夏国传=卷485/486 **不在**）；
> 晋书仅 20 章（NiuTrans 为现代章节化结构，非 130 卷原制，覆盖严重不全）；旧唐书 109 卷（原书 200 卷）；
> 语料中「南京大屠杀/五四运动/西安事变」0 段，「九一八」仅 2 段偶然提及，「卢沟桥」18 段均系桥梁/地名语境。
> 8 个 Critical（62 个 importance=critical 中尚缺字段的）：全部 NEEDS_SOURCE。
> 中文维基文库（zh.wikisource）API 探测（2026-09-12）：标题存在性见各行标注。

## A. 逐事件缺口（8 Critical）

### A1. event-western-xia-jianguo 李元昊称帝、西夏建立（score 76.2）

| 项 | 值 |
|---|---|
| missing_field | place, evidence, background, process, result, impact |
| preferred_source | **《宋史》卷485、卷486（夏国传上/下）** — wikisource 探测：**存在**（宋史/卷485 OK、宋史/卷486 OK） |
| alternative_source | 《续资治通鉴长编》卷122前后（元昊称帝段）；ctext.org 宋史（CC BY-NC-SA，仅 discovery/reference） |
| required chapter/volume | 宋史·卷485 夏国传上、卷486 夏国传下 |
| period | 北宋（1038 年称帝） |
| source_type | 古籍正史（纪传体外国传） |
| copyright/license | 元代官修（脱脱等，作者卒于 1353 后）→ **public domain（全域）**；wikisource 页面文本 PD，维基排版 CC BY-SA（排版不影响文本 PD 判定） |
| public domain | ✅ |
| known digital edition | zh.wikisource「宋史/卷485」「宋史/卷486」；ctext.org「宋史」；国学导航（许可不明，仅 lead） |
| machine-readable | ✅ MediaWiki API 单页抓取，可离线 snapshot + sha256 |
| confidence | 高 |
| priority | **P0（Batch 01 必收）** |

### A2. event-qiqishi-bian 七七事变（卢沟桥事变）（score 81.2）

| 项 | 值 |
|---|---|
| missing_field | place, evidence, background, process, result, impact |
| preferred_source | **蒋介石《对于卢沟桥事件之严正表示》（1937-07-08）与《对卢沟桥事件之严正声明》（1937-07-17 庐山谈话）** — wikisource 探测：**两页均存在** |
| alternative_source | 《中国抗日战争史》（军事科学院，现代著作→仅 reference）；第二历史档案馆档案（无公开机读） |
| required chapter/volume | 独立官方文告（单篇） |
| period | 晚清后/中华民国（1937） |
| source_type | 官方文告/时局声明（一手政治文献） |
| copyright/license | 作者蒋介石卒于 1975 → 中国著作权（死后 50 年）**2026-01-01 起进入公有领域**；官方文告属性进一步弱化权利主张。美国 URAA 期限同步于 2026 到期 |
| public domain | ✅（2026 起，恰在本轮时间窗内） |
| known digital edition | zh.wikisource「對於蘆溝橋事件之嚴正表示」（6.7KB）、「對盧溝橋事件之嚴正聲明」（6.0KB） |
| machine-readable | ✅ |
| confidence | 高 |
| priority | **P0** |

### A3. event-riben-touxiang 日本宣布投降（抗日战争胜利）（score 81.2）

| 项 | 值 |
|---|---|
| missing_field | place, evidence, background, process, result, impact |
| preferred_source | **《降伏文书》（日本向同盟国投降书，1945-09-02）** — wikisource 探测：**存在** |
| alternative_source | 《终战诏书》（裕仁，1945-08-15；日本官方文书，机构文件不享著作权，但裕仁卒于 1989 → 依作者路径未满 50 年，**只以「官方文书例外」路径评估，置信中**）；中国战区受降档案（未公开机读） |
| required chapter/volume | 独立条约文书（单篇） |
| period | 中华民国（1945） |
| source_type | 国际条约/投降文书（一手） |
| copyright/license | 条约与国际文书属官方文件，**不受著作权保护**（中国著作权法第5条精神；国际惯例同） |
| public domain | ✅ |
| known digital edition | zh.wikisource「降伏文書」 |
| machine-readable | ✅ |
| confidence | 高 |
| priority | **P0** |

### A4. event-xinzhongguo-chengli 中华人民共和国成立（score 75.7）

| 项 | 值 |
|---|---|
| missing_field | place, evidence, background, process, result, impact |
| preferred_source | **《中华人民共和国中央人民政府公告》（1949-10-01）** — wikisource 探测：**存在** |
| alternative_source | 《中国人民政治协商会议共同纲领》（1949-09-29，wikisource **存在**）作 background/process 佐证 |
| required chapter/volume | 独立官方公告（单篇） |
| period | 近现代（1949） |
| source_type | 国家机关公告（具有行政性质的官方文件） |
| copyright/license | 中国著作权法第5条：国家机关决议、决定、命令等官方文件**不受著作权保护** |
| public domain | ✅ |
| known digital edition | zh.wikisource「中華人民共和國中央人民政府公告」「中國人民政治協商會議共同綱領」 |
| machine-readable | ✅ |
| confidence | 高 |
| priority | **P0** |

### A5. event-nanjing-datusha 南京大屠杀（score 81.2）

| 项 | 值 |
|---|---|
| missing_field | place, evidence, background, process, result, impact |
| preferred_source | **《国防部审判战犯军事法庭判决 三十六年度审字第十三号》（谷寿夫案判决书，1947）** — wikisource 探测：**存在**（6.3KB）；另有「关于谷寿夫、松井石根和南京大屠杀事件」（44KB，出自《南京大屠杀史料集》整理稿，需辨析整理者权利，仅作 lead） |
| alternative_source | 《南京大屠杀史料集》（张宪文主编 72 卷，现代整理著作 → **整体受版权保护，仅 reference/引证**）；远东国际军事法庭判决书（wikisource **未检出**全本） |
| required chapter/volume | 司法判决书全文（单篇） |
| period | 中华民国（1937 事件 / 1947 判决） |
| source_type | 司法判决书（国家机关司法性质文件） |
| copyright/license | 司法判决属著作权法第5条官方文件 → **不受著作权保护**（事实认定部分引用亦无碍） |
| public domain | ✅ |
| known digital edition | zh.wikisource「國防部審判戰犯軍事法庭判決三十六年度審字第十三號」 |
| machine-readable | ✅ |
| confidence | 高（判决书本体） |
| priority | **P0** |

### A6. event-wusi-yundong 五四运动（score 81.2）

| 项 | 值 |
|---|---|
| missing_field | place, evidence, background, process, result, impact |
| preferred_source | **「五四运动宣言」页** — wikisource 探测：**存在**（1.5KB，需取回后核对署名与正文：若为罗家伦《北京学界全体宣言》→ 罗卒于 1969，2020 起 PD；若为无主集体文献/1919 刊发 → 发表 50 年即 PD） |
| alternative_source | 陈独秀/李大钊相关文章（陈卒 1942、李卒 1927 → 均 PD）；《晨报》1919 报道（报刊无主文献 PD） |
| required chapter/volume | 单篇宣言/文告 |
| period | 中华民国（1919） |
| source_type | 一手政治宣言 |
| copyright/license | 视署名而定：无主/集体 1919 文献 → PD；罗家伦署名 → PD（2020 起）；**若核出为许德珩手笔（卒 1990）→ 未满期，仅作 lead，不入 canonical** |
| public domain | 视核对结果（大概率 ✅） |
| known digital edition | zh.wikisource「五四運動宣言」 |
| machine-readable | ✅ |
| confidence | 中（待取回核署名） |
| priority | **P0** |

### A7. event-jiuyiba-shibian 九一八事变（沈阳）（score 81.2）

| 项 | 值 |
|---|---|
| missing_field | place, evidence, background, process, result, impact |
| preferred_source | wikisource 检出「中央关于日本帝国主义强占满洲事变的决议」（1931-09-22，12.7KB）——**但为政党决议，是否落入著作权法第5条「国家机关官方文件」存在解释空间，license 置信中等** |
| alternative_source | 国民政府/张学良方面文电（wikisource 未检出合适页）；日方关东军纪录（无公开机读版本）；《中国抗日战争史》（现代著作 → 仅 reference） |
| required chapter/volume | 单篇决议/文电 |
| period | 中华民国（1931） |
| source_type | 政党决议（类官方文件） |
| copyright/license | **不明确** → 按「license 不明确不得进入 canonical」规则，本轮**不据此写入事实字段** |
| public domain | ⚠️ 存疑 |
| known digital edition | zh.wikisource（见上） |
| machine-readable | ✅ |
| confidence | 低（许可维度） |
| priority | P2（保持 NEEDS_SOURCE，待获得许可明确的文献） |

### A8. event-xian-shibian 西安事变（score 81.2）

| 项 | 值 |
|---|---|
| missing_field | place, evidence, background, process, result, impact |
| preferred_source | 张学良、杨虎城对时局通电（1936-12-12）——wikisource 多轮检索**未检出**该页 |
| alternative_source | 《中国抗日战争史》《中华民国史》（现代著作 → 仅 reference）；第二历史档案馆藏电文（无公开机读） |
| required chapter/volume | 单篇通电 |
| period | 中华民国（1936） |
| source_type | 军政通电（一手） |
| copyright/license | 张学良卒于 2001 → 死后 50 年未满（2052）；通电虽具公电性质但非国家机关文件，**不宜按官方文件例外处理** |
| public domain | ❌（张学良署名维度） |
| known digital edition | 无稳定机读公开版本 |
| machine-readable | ❌ |
| confidence | 低 |
| priority | P2（保持 NEEDS_SOURCE） |

## B. 已知整部/成片缺失（非 Critical 直接解锁，排队后续批次）

| 缺失著作 | 影响 | 许可/获取判断 | priority |
|---|---|---|---|
| 宋史·夏国传相关卷 | 西夏 6 事件 | 同 A1，wikisource 可得 | **P0（随 A1 一并）** |
| 清史稿（赵尔巽等，1928） | 清/晚清 Major 群 | 著者卒 1927 → PD；wikisource 有全本 529 卷，机读可行，卷册量大 | P1 |
| 清实录 | 清/晚清 Major | 古籍正文 PD；现代影印/点校本有整理者权利；wikisource 覆盖不全，需逐卷核 | P1 |
| 明实录 | 明 Major 群 | 原文 PD；公开机读全本未见稳定版本；中研院校本有权利 | P2 |
| 蒙古秘史 | 元/蒙古建国相关 | 元代 → PD；wikisource「元朝秘史」/ctext 均有 | P1 |
| 中华民国史（张宪文主编） | 民国 Major 群 | 现代著作**受版权保护** → 仅作 reference 引证，不全文入库 | —（不入库） |
| 中国抗日战争史（军事科学院） | 抗战 Major 群 | 同上，仅 reference | —（不入库） |
| 南京大屠杀史料集（72 卷） | 南京大屠杀等 | 现代整理汇编**受版权保护** → 仅 reference；其中单件原始档案可个案评估 | —（不入库） |
| 晋书（语料仅 20 章且为现代章节化结构） | 两晋 Major 群 | 唐修 → PD；wikisource 有 130 卷全本，可补 | P1 |
| 旧唐书（语料 109/200 卷） | 唐 Major 群（60 事件） | 五代修 → PD；wikisource 可补缺卷 | P1 |

## C. 结论

- **本轮 Source Expansion Batch 01 取 1 个新 source：zh.wikisource（维基文库）**，以「页面清单（page manifest）+ 原始快照 + 校验和」方式接入，覆盖 A1–A6（6/8 Critical 的首选文献）。
- A7（九一八）、A8（西安事变）本轮**保持 NEEDS_SOURCE**：前者许可不明，后者首选文献不存在/作者权利未满期。不硬凑。
- B 组整部缺失进入后续批次（清史稿优先，服务唐/明/晚清 Major 群）。
