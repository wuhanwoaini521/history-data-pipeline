# Overnight Queue 06 — Knowledge Layer E2E Validation

> 目的：证明知识链真的可用（Event → Evidence → Historical Text → Chapter → Paragraph → Source）。
> 查询对象：dist/history.duckdb（应用真实读取的库）。每条含 title/source/chapter/paragraph excerpt/链路字段。

## 样例 1 · 古代 —— 商汤灭夏（event-shangtang-miexia，前1600）

| 字段 | 值 |
|---|---|
| Source | 尚书（source-classical-modern, MIT） |
| Chapter | 商书 / 汤誓 |
| Paragraph | p1：「伊尹相汤伐桀，升自陑，遂与桀战于鸣条之野，作《汤誓》。」 |
| 今译 | 「伊尹辅佐商汤讨伐夏桀，队伍开拔到山西永济一带，于是与夏桀在鸣条之野展开大战。战前作动员令…」 |
| link method / conf | exact / 1.0 |

另：同事件《史记·殷本纪》（十二本纪/殷本纪 p1，exact 1.0）双源互证。

## 样例 2 · 古代 —— 秦灭六国（event-qin-mie-liuguo，前230）

| 字段 | 值 |
|---|---|
| Source / Chapter | 史记 / 十二本纪·秦始皇本纪 p1「秦始皇帝者，秦庄襄王子也。」 |
| Source / Chapter | 资治通鉴 / 秦纪·秦纪一 p1（part 级命中 → 首章锚定） |
| method / conf | exact / 1.0（双源） |

## 样例 3 · 唐 —— 李渊称帝、唐朝建立（event-tang-jianguo，618）

| 字段 | 值 |
|---|---|
| Source / Chapter | 旧唐书 / 本纪·卷一 p1「高祖高祖神尧大圣大光孝皇帝姓李氏，讳渊。」 |
| method / conf | **content / 0.95**（章首行核实：term 高祖纪 ↔ 章首「高祖…」） |
| 另 | 资治通鉴 / 唐纪·唐纪一（exact 1.0） |

## 样例 4 · 明 —— 鄱阳湖之战、陈友谅覆灭（event-poyanghu-zhizhan，1363）

| 字段 | 值 |
|---|---|
| Source / Chapter | 明史 / 列传·卷十一 p1「陈友谅，沔阳渔家子也。」（传记开篇原文） |
| method / conf | **content / 0.95** |
| 另 | 明史·太祖纪 → **alias 0.85** → 本纪/卷一 p1「◎太祖一太祖开天行道肇纪…讳元璋」 |

## 样例 5 · 晚清 —— 第一次鸦片战争 / 甲午战争 / 武昌起义（诚实缺口）

| 事件 | 证据 work·term | 状态 |
|---|---|---|
| 第一次鸦片战争 | 清实录·宣宗实录；筹办夷务始末·道光朝 | needs_linking（两书不在语料，NEEDS_SOURCE） |
| 甲午战争 | 清实录·德宗实录；清史稿·德宗本纪 | needs_linking |
| 武昌起义 | 清史稿·宣统本纪；辛亥革命回忆录·武昌起义 | needs_linking |

**这组样例验证的是"知识层缺失时的正确行为"**：链路明确报告缺口、状态如实、
绝不以模型常识冒认锚定 —— 与 SOURCE-BACKED FIRST 原则一致。

## 结论

古代/唐/明全链可用且字段齐备；晚清/20 世纪等待外部来源（见 OVERNIGHT_FINAL Blockers）。
→ 进入 Queue 7。
