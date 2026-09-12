# Batch 02 · Queue 11 — Legacy Evidence Cleanup

> 对象：dist `event_evidence` 中 22 条 `pending_knowledge`（legacy 悬空 text id）。
> 机制保持：fuzzy 只报告、永不写回；不做字符串相似度自动绑定。

## 11.1 Legacy text id recovery 结果

| 分级 | 数量 | 说明 |
|---|---:|---|
| exact（id 等价） | 0 | 22 条旧 id（`text-niutrans-*`）在新知识层全部悬空：旧 id 由上一代快照的 `source_path:line` 散列而来，**不可逆**，不存在 id 等价恢复路径 |
| content（章节+内容双核实，已绑定） | **21** | 在对应 work 内定位事件核心叙事段落，逐条人工复核英文（见下表），写回 `link_method: manual` 段落精确锚 + 逐字引文 |
| alias | 0 | chapter_aliases 表不含这些主题词 |
| manual_candidate（仅报告，未绑定） | **1** | event-anlu-changan-recapture（语料未见「收复长安」核心段；最佳候选 唐纪三十八#p62 为旁述，不足以绑定） |
| unresolved | 0 | — |

**24 → 结论：pending_knowledge 22 → 1；linked 98 → 149；段落级锚（#p）24 → 75。**

## 恢复明细（21 条，全部可回查）

| event | legacy work·term | 新锚 | conf | 引文 |
|---|---|---|---:|---|
| event-anlu-changan | 资治通鉴·长安 | 唐纪三十四#p204 | 0.85 | 「贼入长安方虏掠…」 |
| event-anlu-changan-recapture | 资治通鉴·郭子仪 | —（manual_candidate） | — | 未绑定 |
| event-anlu-luoyang | 旧唐书·洛阳 | 本纪/卷九#p388 | 0.90 | 「丁酉，禄山陷东京，杀留守李憕…」 |
| event-anlu-pacification | 旧唐书·思明 | 本纪/卷十一#p92 | 0.85 | 「以史朝义下降将李宝臣为…成德军节度使」 |
| event-anlu-shi-siming | 资治通鉴·史思明 | 唐纪三十七#p4 | 0.90 | 「史思明筑坛于魏州城北，自称大圣燕王」 |
| event-anlu-three-frontiers | 旧唐书·禄山 | 列传/卷一百五十#p44 | 0.95 | 「兼三道节度，进奏无不允。」 |
| event-anlu-tongguan | 资治通鉴·潼关 | 唐纪三十四#p21 | 0.85 | 「今守潼关，数月不能进…」 |
| event-anlu-xuanzong-shu | 资治通鉴·蜀 | 唐纪三十四#p132 | 0.90 | 「丙申，至马嵬驿，将士饥疲，皆愤怒。」 |
| event-chuhan-gaixia | 资治通鉴·垓下 | 汉纪三#p15 | 0.90 | 「十二月，项王至垓下，兵少，食尽…」 |
| event-chuhan-julu | 史记·巨鹿 | 项羽本纪#p149 | 0.90 | 「项羽乃悉引兵渡河，皆沉船，破釜甑…」 |
| event-chuhan-pengcheng | 史记·彭城 | 高祖本纪#p291 | 0.90 | 「汉王以故得劫五诸侯兵，遂入彭城。」 |
| event-chuhan-qin-fall | 史记·子婴 | 高祖本纪#p186 | 0.90 | 「秦王子婴素车白马…降轵道旁。」 |
| event-chuhan-qin-revolt | 史记·陈胜 | 陈涉世家#p32 | 0.90 | 「王侯将相宁有种乎！」 |
| event-chuhan-xingyang | 资治通鉴·荥阳 | 汉纪二#p67 | 0.90 | 「还守成皋、荥阳…深沟壁垒」 |
| event-hongmen | 史记·鸿门 | 项羽本纪#p199 | 0.90 | 「项羽兵四十万，在新丰鸿门」 |
| event-three-chibi | 三国志·赤壁 | 吴主传#p32 | 0.90 | 「遇於赤壁，大破曹公军。」 |
| event-three-dong-zhuo | 资治通鉴·董卓 | 汉纪五十一#p219 | 0.90 | 「董卓至显阳苑…奉迎于北芒阪下。」 |
| event-three-guandu | 资治通鉴·官渡 | 汉纪五十五#p324 | 0.90 | 「袁氏辎重…在故市、乌巢…燔其积聚」 |
| event-three-jingzhou-change | 三国志·荆州 | 先主传#p84 | 0.90 | 「曹公南征表，会表卒，子琮代立，遣使请降。」 |
| event-three-north-consolidation | 三国志·曹操 | 武帝纪#p387 | 0.85 | 「康即斩尚、熙…传其首。」 |
| event-three-regime-formation | 三国志·黄初 | 先主传#p225 | 0.90 | 「即皇帝位於成都武担之南。」 |
| event-three-yellow-turbans | 后汉书·黄巾 | 皇甫嵩朱俊列传#p20 | 0.90 | 「皆着黄巾为标帜，时人谓之黄巾」 |

**方法说明**：绑定判据 = work 内定位段落 + 章节语义核实（如安禄山传=旧唐书卷一百五十经章首行「安禄山，营州柳城杂种胡人也」确认）+ 逐字引文回查；
非单纯字符串相似度。3 条 work 不符（legacy 标注 旧唐书）的行改在旧唐书内重定位，未改写 legacy 的 work/term 声明。

## 11.2 Fuzzy policy

- 全部候选路径先经段级检索（`search_paragraphs`）生成候选，仅用于**人工复核输入**；
  未产生任何 fuzzy 写回（Rule 5 保持；dist `link_method=fuzzy` 仍为 0）。
- `event-anlu-changan-recapture` 保持 `pending_knowledge` + 报告候选（唐纪三十八#p62 等 3 段），待后续批次处理。

## 11.3 附带修复（防止债务复发）

- `evidence_link.apply_links` 增加跳过规则：`link_method == 'manual'` 的行不再被自动重算
  （Batch 02 Queue 9 曾发生 24 条 manual 段落锚被降级为章首锚的事故；该修复使其不可复发）。

## 输出统计（dist）

| 指标 | Before | After |
|---|---:|---:|
| linked | 98 | **149** |
| needs_linking | 34 | 34（全部为语料缺失著作，见 batch02-03） |
| pending_knowledge | 22 | **1** |
| link_method=manual | 24 | **75** |
| chapter_anchor 含 #p（段落级） | 24 | **75** |
