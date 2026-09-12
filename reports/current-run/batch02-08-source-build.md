# Batch 02 · Queue 8 — Knowledge Layer Rebuild（Source Expansion Batch 01 接入）

> 新 source：`source-wikisource`（zh.wikisource，9 页 manifest，7 页 canonical_use=allowed 入库）
> 政策：docs/source-acquisition-policy.md · 采集：scripts/acquire_wikisource_batch01.py
> Parser：src/history_data_pipeline/knowledge_wikisource.py · Gate：scripts/source_quality_gate_wikisource.py

## 构建结果

| 项 | 值 |
|---|---:|
| texts_bilingual（NiuTrans 双语） | 721,424 |
| texts_classical（NiuTrans 古文原文） | 8,704 |
| **texts_wikisource（新增）** | **350** |
| **historical_texts 合计** | **730,478**（Before 730,128，+350，零扰动） |
| works | 知识库 6 个新文书行；dist 合并后 55（49 + 6） |
| chapter_heads | 3,840（+2：宋史卷485/卷486） |
| sources | dist 注册 `source-wikisource`（snapshot_version=20260912，license=底本逐页判定） |

## 入库文档（7）

| document | section/chapter | paragraphs |
|---|---|---:|
| 宋史（卷四百八十五 夏国传上） | 列传 / 卷四百八十五 | 79 |
| 宋史（卷四百八十六 夏国传下） | 列传 / 卷四百八十六 | 100 |
| 降伏文書（1945-09-02 投降书） | — | 36 |
| 對於蘆溝橋事件之嚴正表示（1937-07-17 庐山谈话要旨+全文） | — | 23 |
| 對盧溝橋事件之嚴正聲明（同场谈话另一版本） | — | 12 |
| 國防部審判戰犯軍事法庭判決 三十六年度審字第十三號（谷寿夫案） | — | 12 |
| 中華人民共和國中央人民政府公告（1949-10-01） | — | 9 |
| 中國人民政治協商會議共同綱領（1949-09-29） | — | 81 |

- 九一八/西安事变首选文献未入库（manifest A7/A8：许可不明/文献缺失），见 batch02-03。
- 「五四運動宣言」（罗家伦，PD）manifest 标注 gated_pending_review 已在取回后核实署名，
  更新判定走 Queue 10（当前 build 未含该页，下轮 build 接入）。

## 双次重建确定性（Gate D）

| 项 | build#1 | build#2 |
|---|---|---|
| historical_texts | 730,478 | 730,478 |
| DISTINCT id | 730,478 | 730,478 |
| id 集合 SHA1 摘要 | `beaf13401c111535` | `beaf13401c111535` |
| works / sources / chapter_heads | 6 / 2 / 3,840 | 同左 |

text_id 规则：`text-wikisource-` + sha1(`{page_file}#{paragraph_index}`)[:20]（重跑不变）。

## Backbone 并入 dist

- `backbone --knowledge data/normalized/history.duckdb build`（默认 seed-only，必须显式 --knowledge）。
- dist：historical_texts 730,478 · event_relations 1,065（+8 本轮策展关系）·
  event_evidence 154（linked 98 / needs_linking 34 / pending 22，等 Queue 9 relink）。
- 注意事项（已验证）：`backbone build` 不带 `--knowledge` 会产出 seed-only dist（historical_texts=0）；
  本轮一次误构建已被带 `--knowledge` 的重建覆盖，dist 备份链（history.previous.*）未动。

## 质量门禁

scripts/source_quality_gate_wikisource.py：**PASS**（9 项检查全绿，报告 batch02-07-source-quality-gate.md）。
