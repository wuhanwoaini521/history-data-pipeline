# Batch 02 · Queue 7 — Source Quality Gate（wikisource Batch 01）

> 数据库：data/normalized/history.duckdb · source：`source-wikisource`

## 检查结果

| 检查 | 结果 | 说明 |
|---|---|---|
| document_count | ✅ | 12 documents（12 部/文书名：batch01 9 + 清史稿/晋书/旧唐书 3） |
| chapter_count | ✅ | 30 chapters（batch01 宋史 2 卷 + batch02 28 卷） |
| empty_text | ✅ | 空文本 0 行 |
| duplicate_ids | ✅ | 重复 ID 0 个 |
| duplicate_paragraphs | ✅ | 长文本（≥30 字）同章重复 >2 次：0 组；短套语重复 8 组（编年体例，正常，仅记录） |
| html_template_residue | ✅ | 无残留 |
| encoding_corruption | ✅ | replacement-char 行 0 |
| hierarchy_consistency | ✅ | section/chapter 半空行 0（古籍须齐全；文书须全 null） |
| orphan_book_ids | ✅ | 无孤儿（works 表 ∪ curated seeds） |
| paragraph_ordering | ✅ | 各文档/卷 paragraph_index 1..N 连续 |
| ocr_risk | ➖ n/a | 本轮来源均为原生数字文本（wikitext/渲染 HTML），无 OCR 环节 → OCR 风险检查不适用（n/a） |

## 文档计费（document/段计数）

| document | paragraphs | distinct section | distinct chapter |
|---|---:|---:|---:|
| 中國人民政治協商會議共同綱領 | 81 | 0 | 0 |
| 中華人民共和國中央人民政府公告 | 9 | 0 | 0 |
| 五四運動宣言 | 6 | 0 | 0 |
| 國防部審判戰犯軍事法庭判決三十六年度審字第十三號 | 12 | 0 | 0 |
| 國防部審判戰犯軍事法庭判決三十六年度審字第壹號 | 9 | 0 | 0 |
| 宋史 | 177 | 1 | 2 |
| 對於蘆溝橋事件之嚴正表示 | 22 | 0 | 0 |
| 對盧溝橋事件之嚴正聲明 | 12 | 0 | 0 |
| 旧唐书 | 254 | 2 | 3 |
| 晋书 | 823 | 3 | 9 |
| 清史稿 | 1805 | 2 | 16 |
| 降伏文書 | 34 | 0 | 0 |

**合计 paragraphs：3244**

## 结论：**PASS**

全部检查通过，允许进入 canonical 知识层。
