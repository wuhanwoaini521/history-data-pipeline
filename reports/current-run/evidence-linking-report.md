# Evidence Linking Report（阶段四 · 130 条 event_evidence 重新 linking）

> 生成：2026-09-11 · 知识层重建（historical_texts=730,128）后的证据锚定统计。
> 工具：`backbone link-evidence`（dry-run 统计与 --apply 写回一致）。
> 铁律：fuzzy 永不写回（含带篇章坐标的 fuzzy）；写回仅限 exact / normalized_exact / alias / content。

## 一、总账（total=130）

| 状态 | 数量 | 说明 |
|---|---:|---|
| **linked** | **74** | 已锚定到语料真实章首段行（写回 YAML + dist） |
| needs_linking | 34 | 27 条为 fuzzy 候选所在行 + 7 条语料未命中行（原状态保持） |
| pending_knowledge | 22 | 携带 legacy 时期 text id（旧知识库产物，新语料中 id 不存在，保持 pending 待人工复核，不冒认） |

### linked 按匹配方式

| match_method | 数量 | confidence | 说明 |
|---|---:|---:|---|
| exact | 27 | 1.0 | term 与语料篇卷名/卷类名精确一致（如 史记·秦始皇本纪） |
| content | 42 | 0.95 | 语料章首行核实（如 明史·陈友谅传 → 章首「陈友谅，沔阳渔家子也。」） |
| alias | 5 | 0.85 | 人工卷号映射表（语料内容已核实），见 data/curated/knowledge/chapter_aliases.json |

### 需要人工评审 / 缺失知识

- **fuzzy candidates：27**（仅报告，未写回）。主要是"主题词"型 term
  （史记·鸿门 / 资治通鉴·官渡 / 三国志·赤壁）——段级内容检索给出候选段落
  （含 chapter#paragraph 锚点与 excerpt），需人工确认 quote 后才可升级为段级锚定。
- **missing knowledge（unmatched）：29**，构成：
  - 语料缺失著作（约 15 条）：清实录 ×5、清史稿 ×3、明实录 ×2、续资治通鉴长编 ×1、
    筹办夷务始末 ×1、辛亥革命回忆录 ×1、三朝北盟会编内嵌《岳飞新传》×2
    ——整部不在 NiuTrans，保持 NEEDS_SOURCE；
  - 语料卷覆盖不全（约 14 条）：晋书（帝纪 10/列传 17/志 20，全书 130 卷仅覆盖 47）、
    旧唐书（120/200）、明史志缺地理志、周书缺静帝纪、魏书无"载记"体例（term 转写问题）等。
- **legacy 悬空 id：22 条**：dist 中 `historical_text_id` 非 linked 的 22 条
  （楚汉系列等 legacy QA 迁移行）指向旧知识库构建的 text id，在 20240421 快照语料中
  均不存在（0/22 解析）。如实保留 pending_knowledge，不伪造新 id 冒认旧链接。

## 二、linked 的著作分布

| 著作 | linked | | 著作 | linked |
|---|---:|---|---|---:|
| 明史 | 14 | | 旧五代史 | 2 |
| 资治通鉴 | 12 | | 魏书 | 2 |
| 史记 | 8 | | 周书 | 2 |
| 汉书 | 7 | | 梁书 | 2 |
| 旧唐书 | 7 | | 隋书 | 2 |
| 晋书 | 6 | | 尚书 | 2 |
| 宋史 | 4 | | 三国志 | 2 |
| 后汉书 | 3 | | 北齐书/陈书/金史/辽史/元史 | 各 1 |

## 三、Before / After

| 指标 | Before（知识层=0） | After |
|---|---:|---:|
| historical_texts | 0 | 730,128 |
| event_evidence linked | 0 | **74** |
| pending_knowledge | 26 | 22 |
| needs_linking | 104 | 34 |
| 章级锚点（chapter_anchor） | 无此字段 | 74 条全带 |
| link_method / claim_field 字段 | 无 | 已入 schema+dist |

> 注：上一行 pending_knowledge 26 → 22 的变化 = 原 26 中 4 条在本轮被 exact/content 锚定；
> 22 条 legacy 悬空 id 仍归入 pending 口径（见上）。
