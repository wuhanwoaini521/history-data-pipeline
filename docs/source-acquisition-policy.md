# Source Acquisition Policy

> Status: **Batch 02 v1（2026-09-12）**。对 `docs/SOURCE_POLICY.md` 的采集环节细则化；
> 不取代其层级（Tier A–D）与证据规则，冲突时以 SOURCE_POLICY 为准。

## 1. 六原则

History V2 的任何新 source 接入必须同时满足：

1. **Source-backed first** — 先有底本与出处，后有字段写入；不得先写事实再找依据。
2. **Reproducible** — 给定同一 manifest 与 snapshot，任何人在任何机器可重建相同的
   historical_texts 行（含 id）。
3. **Versioned** — 每次采集生成独立快照目录（`data/raw/<dataset>/<snapshot_version>/`），
   旧快照永不覆盖、永不删除。
4. **Traceable** — 每条入库行可通过 `source_id + source_path` 回到 raw 快照的字节。
5. **License-aware** — 许可按**底本（underlying work）**判定，载体（hosting site）只记录不决定。
6. **Offline rebuildable** — 快照入库后，知识层重建不依赖网络。

## 2. 载体与底本（carrier vs. underlying work）判定

现有 `SOURCE_POLICY.md` 将 wikisource 列为 Tier C（指其作为「检索论断」的一般参考用途）。
本政策进一步规定：**当 wikisource 等载体承载的是公有领域一手文献时，入库内容的层级随底本**：

| 底本类型 | 例 | Tier | 说明 |
|---|---|---|---|
| 古籍（PD） | 《宋史》卷485/486 | A（随底本） | 维基文库仅为载体；content tier = 二十四史正史 |
| 条约/投降文书 | 《降伏文书》1945 | A（一手文书） | 国际文书，不享著作权 |
| 国家机关公文/司法判决 | 《中央人民政府公告》《谷寿夫案判决书》 | A（一手文书） | 著作权法第5条官方文件 |
| 已过保护期个人文献 | 蒋介石 1937 文告（卒1975，2026 起 PD）、罗家伦宣言（卒1969，2020 起 PD） | A-/B | 一手，但需逐篇核署名与保护期 |
| 载体自身的叙述/摘要/整理者注释 | wikisource 导语、跨页导航 | 不入库 | 与 SOURCE_POLICY Tier C 一致 |
| 现代整理汇编（《中华民国史》《南京大屠杀史料集》等） | — | 仅 reference | 整体受版权保护，不作 canonical |

**禁止**：以「百科/维基叙述」形式采信 wikisource 页面上的解释性内容；只采信底本正文。

## 3. 采集链（唯一合法链路）

```text
remote source（manifest 逐页列出）
    ↓  MediaWiki API / 直链下载，带 User-Agent 与抓取时间
raw snapshot（data/raw/<dataset>/<version>/，原始字节 immutable）
    ↓  sha256（逐文件 + manifest 汇总）
checksum
    ↓  parser（deterministic，纯函数：raw bytes → 结构化行）
normalized（原文保留 + 规范化字段分离，如 original_simplified）
    ↓  knowledge build
historical_texts（source_id 指向 knowledge.source 新行）
    ↓  backbone build
dist
```

跳过任何一步（例如抓网页直接写 DuckDB）都是硬失败。

## 4. 每个 source 的必录 metadata（写入 `knowledge.source` + 快照 metadata.json）

`source_id`、`title`、`author/editor`、`edition`、`source_url`、`download_url`、
`license`、`license_url`、`acquired_at`、`snapshot_version`、逐文件 `sha256`、
`file size`、`format`、`encoding`、`parser`（代码路径）、`normalizer`（如 OpenCC t2s）、
`notes`（含逐页 manifest：页名、底本、作者卒年/文书性质、PD 判定与理由）。

`config/sources.yml` 为注册表：新 dataset 先注册（official_page / mode / license），
快照 metadata.json 记录实际采集细节。

## 5. 底本许可判定清单（每页必须回答）

1. 底本是什么？（古籍 / 官方文书 / 个人作品 / 现代汇编）
2. 作者（自然人）卒年？机构文书？→ 保护期判定（中国：个人 = 卒后 50 年；无主文献 =
   发表后 50 年；官方文件第5条不保护；条约不保护）。
3. 若「载体排版权」（如维基 CC BY-SA）与「底本 PD」并存 → 以底本为准，记录载体信息。
4. 保护期未满或判定置信 <高 → 该页只可作 raw snapshot 留档（lead），**不得**用于 canonical
   字段写入。
5. 判定与理由逐页写入 manifest（审查可复核）。

## 6. Parser 要求（Queue 6 实施依据）

- raw immutable：parser 不得改写快照字节。
- deterministic：同一输入 → 同一输出（无时间戳、无随机、无网络调用）。
- stable ids：行 id 由内容/路径派生（如 `text-<dataset>-<sha前20>`），重跑不变。
- 层级保留：document / volume / chapter / section / paragraph 按底本真实层级映射
  （古籍为 卷/纪/传/志；单篇文书 volume/chapter 允许 null）；段落顺序 = 底本顺序。
- 原文与规范化分离：`original_text` 保留底本原貌（含繁体），`original_simplified`
  由 OpenCC t2s 派生；不混写。

## 7. Quality gate（Queue 7 实施依据）

document/volume/chapter/paragraph 计数、空文本、重复段落、重复 ID、层级断裂/孤儿节点、
编码损坏、HTML/模板残留（wikitext 清理遗漏）、OCR 风险（本轮来源非 OCR，n/a）。
任一项不达标 → `QUARANTINE_SOURCE`，不写入 canonical 知识层，快照保留待修复。

## 8. 禁止来源（重申 SOURCE_POLICY §2 Tier D）

百度百科 / 知乎 / 公众号 / 随机博客 / SEO 历史站 / 无出处短文 / AI 生成内容 —— 一律不得
作为 canonical historical_text source，最多作 discovery lead。
