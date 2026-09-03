# FINAL_SOURCE_COVERAGE

> China History Backbone V1 · 全库来源审计（§73）。

## 硬指标（全局扫描 backbone.events）

| 指标 | 值 |
|---|---|
| 全库 Events（含 legacy 26 + Batch1-8 592） | **618** |
| 携带 source_reference | **618 / 618（100%）** |
| 携带 source_ids（引用 seeded works） | **618 / 618（100%）** |
| AI 作为事实来源（source_reference 含 "AI"/"ChatGPT"/"Claude"） | **0** |

## 来源双层链设计

每条 source_reference = 「古代/档案史料：×」+「现代参考/研究：×」：
- 古代—近代：十三经/诸子/二十四史（宋史金史元史明史清史稿）、资治通鉴、续资治通鉴长编、
  三朝北盟会编、元史、蒙古秘史、清实录、明实录、筹办夷务始末、太平天国文书汇编、
  义和团档案史料、南京临时政府公报、中央档案馆档案 等；
- 现代参考：断代工程简本、白寿彝《中国通史》、邓广铭/漆侠/王曾瑜、韩儒林/周良霄、
  南炳文/汤纲/孟森/樊树志、茅海建/罗尔纲、戚其章/金冲及/张宪文、军事科学院《中国抗日战争史》、
  《南京大屠杀史料集》等；
- Batch8 额外强制：每事件 source_reference 显式含「档案/史料/公报/文本/纪录」字样（§65 合规层）。

## Works 种子：36

shiji…清实录 + 中华民国史 + 中国抗日战争史（全链覆盖）。所有事件引用全部落到 seeded works。

## 候选流程溯源

618 Events 全部有 data/reviews/accepted/<id>.review.json（reviewed_by=china-history-backbone-v1-curator
(batchN)），来源 candidate → review → accepted 链完整（candidates 见 data/candidates/backbone_events/）。

## 无争议结论

**FINAL: Source Coverage = 100%；AI source = 0；PASS。**