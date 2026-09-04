# CRITICAL_EVENT_PERSON_LINKING V1_SUMMARY

> China History Backbone V2.1 · 62 Critical Event Person Linking 总结。

```text
CRITICAL_EVENT_PERSON_LINKING_V1_READY = true
```

## 1—24（§63 逐项）

| # | 项 | 值 |
|---|---|---|
| 1 | Critical Event 总数 | **62**（Scope 冻结，reports/CRITICAL_EVENT_PERSON_LINKING_SCOPE.md） |
| 2 | 处理 Event 数 | **62/62**（均完成 candidate+review；未要求全有链接） |
| 3 | Candidate 总数 | **150** |
| 4 | Unique Person Name 数 | **134** |
| 5 | Accepted EventPerson 数 | **110** |
| 6 | Exact 数 | **89** |
| 7 | High Confidence 数 | **21** |
| 8 | Ambiguous 数 | **6**（王濬/晋愍帝×2/刘曜/梁武帝/孙武@武昌起义；未进 EventPerson） |
| 9 | Not Found 数 | **34**（未伪造 Person；详见 PERSON_KNOWLEDGE_GAPS.md） |
| 10 | Rejected 数 | **0**（时间/身份冲突以 ambiguous 保留，未强 reject） |
| 11 | 有 Accepted Person 的 Critical Event 数 | **54** |
| 12 | 无 Person 的 Critical Event 数 | **8**（商汤灭夏/九一八/西安事变/七七/南京大屠杀/日本投降/新中国成立/西晋灭亡——近代人物与个别古典人物在 CBDB 无记录，符合"宁可无，不可错"） |
| 13 | Existing Links 审核数量 | **58**（legacy；无 critical 上，身份核验 58 条正确） |
| 14 | Existing Wrong Link 数 | **0**（未发现需挂起 recheck 的旧链接） |
| 15 | Same-name conflict 数 | **6**（见 PERSON_IDENTITY_CONFLICTS.md） |
| 16 | Timeline conflict 数 | **2**（张世杰 106950=元人排除、孙武=春秋/明人非革命党；均未入错链） |
| 17 | Alias conflict 数 | 处理：帝王称谓→个人名映射 20+（唐太宗→李世民、明成祖→朱棣、康熙帝→爱新觉罗玄烨 等）；朱温/李斯/宋徽宗等 KB 无本体 → not_found |
| 18 | Knowledge Store gap 数 | **34**（not_found；报告见 PERSON_KNOWLEDGE_GAPS.md） |
| 19 | EventPerson Broken Ref | **0**（person_id 98 个唯一 id 全量存在性校验 100%） |
| 20 | Duplicate EventPerson | **0**（事件内 (event,person) 去重/canonical 消歧测试） |
| 21 | V1 Event Count 仍 618 | ✅（periods=31/regimes=64/stories=3 均不变；events/ 目录未写入任何 V2 文件） |
| 22 | Tests | **141 passed**（129 V1 原测试全部通过 + 12 V2.1 新测试） |
| 23 | Build | ✅ seed-only（tests）与 `--knowledge data/normalized/history.duckdb`（676,427 people 并入）双模式通过；dist 重建（event_person=168） |
| 24 | 需解冻 V1 的问题 | **0**（V1_BACKBONE_ISSUES_FOUND_DURING_PERSON_LINKING.md 记录：仅 KB dynasty 字段与个别史实有出入，属 Layer2 数据质量，与 V1 无关） |

## 质量指标（§62）

```text
wrong_accepted_links            = 0
accepted_links_with_provenance  = 100%（store + accepted review 完整记录 identity/event evidence）
accepted_person_ids_resolve     = 100%（98/98 unique ids → knowledge store）
accepted_event_ids_resolve      = 100%（110/110 → critical events）
ambiguous 未进入 EventPerson    = 是（6 条保留在 candidate/unlinked）
not_found 未生成 fake Person    = 是（34 条，person_id=None）
EventPerson 粒度                = min 1 / max 4 / avg 2.04 / median 2（远低于 15 上限）
```

## 流程（§1/§38-40）

Event summary/source_reference → 核心人物候选（1–8 人/事件）→ Knowledge Store
（people 676,427 / aliases 208,624 / relations 561,461 / person_place 460,402）解析 →
四级分类（exact 89 / high_confidence 21 / ambiguous 6 / not_found 34）→ 人工 review →
Accepted EventPerson Store（data/curated/history_backbone/event_person/，V1 events/ 冻结）→
Build 集成（loader 合并 + reference seed 扩展）→ QA + 报告 + 测试。

## 代表质量点

- 张世杰：排除 CBDB 元人同名记录（106950），选定宋将本体（15200，death 1279）；
- 孙武 @ 武昌起义：KB 孫武 为春秋兵家（或明记录），与共进会孙武（1880-1939）非同人 → ambiguous 不链接；
- 李自成/吴三桂/努尔哈赤/多尔衮/康熙/道光/光绪/袁世凯/溥仪/蔡元培/李大钊 等：别名(PREFERRED_ID)后的 canonical 精确消歧；
- 现代史（九一八/西安/七七/南京大屠杀/日本投降/新中国）主要人物不在 CBDB → 诚实 not_found 并出具 gap 报告，不补 fake Person。

```text
CRITICAL_EVENT_PERSON_LINKING_V1_READY = true
```

按 §65：本批到此停止。**未**开始 555 Major 链接 / Place / HistoricalText / Story V2 / UI / Graph / Vector。