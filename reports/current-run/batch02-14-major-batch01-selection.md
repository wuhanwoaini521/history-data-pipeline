# Batch 02 · Queue 14 — Major Batch 01 Selection（只选不富化）

> 范围：从 555 个 major 中选 **30 个**进入下一轮候选；本轮不改动这些事件。
> 判据：source coverage（语料含所引史源）· ≥1 evidence · people/place 部分关系 · 优先时期（唐/明/西汉/晚清，但不为配额选缺源事件）。
> score=product_completeness_score（9 维）。

## 分组汇总

| 分组 | 数量 | 进入下一轮 |
|---|---:|---|
| READY | 16 | ✅ 全部进入 Major Batch 01 enrichment |
| PARTIAL_SOURCE | 9 | ⏸ 语料在库但证据未链接（或单条待审）——先补链接再富化 |
| NEEDS_SOURCE | 5 | ⛔ 所引史源缺库（清实录/清史稿等）——等待 source 批次 |

## READY（16）——语料 + 证据 + 人物/地点关系齐备

| event_id | event_name | period | score | source coverage | evidence | people | place | missing | readiness |
|---|---|---|---:|---|---:|---:|---:|---|---|
| event-anlu-uprising | 安禄山起兵 | 唐 | 66.7 | 旧唐书 | 1 | 2 | 1 | background,process,impact | READY |
| event-anlu-three-frontiers | 安禄山兼领三镇 | 唐 | 66.7 | 旧唐书 | 1 | 3 | 1 | background,process,impact | READY |
| event-anlu-luoyang | 洛阳失守 | 唐 | 66.7 | 旧唐书 | 1 | 2 | 1 | background,process,impact | READY |
| event-anlu-tongguan | 潼关失守 | 唐 | 66.7 | 资治通鉴 | 1 | 2 | 1 | background,process,impact | READY |
| event-anlu-changan | 长安失守 | 唐 | 66.7 | 资治通鉴 | 1 | 3 | 1 | background,process,impact | READY |
| event-anlu-xuanzong-shu | 唐玄宗入蜀 | 唐 | 66.7 | 资治通鉴 | 1 | 2 | 1 | background,process,impact | READY |
| event-anlu-shi-siming | 史思明再叛 | 唐 | 66.7 | 资治通鉴 | 1 | 2 | 1 | background,process,impact | READY |
| event-anlu-pacification | 安史之乱平定 | 唐 | 55.6 | 旧唐书 | 1 | 3 | 1 | related_event,background,process,impact | READY |
| event-chuhan-qin-revolt | 秦末起义 | 秦 | 66.7 | 史记 (+汉书) | 1 | 1 | 1 | background,process,impact | READY |
| event-chuhan-julu | 巨鹿之战 | 秦 | 66.7 | 史记 (+汉书) | 1 | 1 | 1 | background,process,impact | READY |
| event-chuhan-qin-fall | 秦朝灭亡 | 西汉 | 66.7 | 史记 (+汉书) | 1 | 1 | 1 | background,process,impact | READY |
| event-hongmen | 鸿门宴 | 西汉 | 66.7 | 史记 (+汉书) | 1 | 2 | 1 | background,process,impact | READY |
| event-chuhan-pengcheng | 彭城之战 | 西汉 | 66.7 | 史记 (+汉书) | 1 | 2 | 1 | background,process,impact | READY |
| event-chuhan-xingyang | 荥阳对峙 | 西汉 | 66.7 | 资治通鉴 (+汉书) | 1 | 2 | 1 | background,process,impact | READY |
| event-chuhan-gaixia | 垓下之战 | 西汉 | 66.7 | 资治通鉴 (+汉书) | 1 | 3 | 1 | background,process,impact | READY |
| event-chuhan-han-foundation | 刘邦建立汉朝 | 西汉 | 66.7 | 汉书 (+汉书) | 1 | 2 | 1 | background,process,impact | READY |

## PARTIAL_SOURCE（9）——语料在库、证据未链接或待审

| event_id | event_name | period | score | source coverage | evidence | people | place | missing | readiness |
|---|---|---|---:|---|---:|---:|---:|---|---|
| event-anlu-changan-recapture | 唐军收复长安 | 唐 | 66.7 | 资治通鉴 | 1 | 3 | 1 | background,process,impact | PARTIAL_SOURCE |
| event-jianwen-jiwei | 建文帝即位 | 明 | 22.2 | 明史（语料在库，249 篇卷） | 0 | 2 | 0 | people,place,evidence,background,process,result,impact | PARTIAL_SOURCE |
| event-ningwang-zhi-luan | 宁王之乱（朱宸濠起兵） | 明 | 22.2 | 明史（语料在库，249 篇卷） | 0 | 2 | 0 | people,place,evidence,background,process,result,impact | PARTIAL_SOURCE |
| event-shanxi-minbian | 陕西民变扩大（明末农民战争开端） | 明 | 22.2 | 明史（语料在库，249 篇卷） | 0 | 2 | 0 | people,place,evidence,background,process,result,impact | PARTIAL_SOURCE |
| event-huangtaiji-jiwei | 皇太极即后金汗位 | 明 | 22.2 | 明史（语料在库，249 篇卷）；缺 清实录 | 0 | 2 | 0 | people,place,evidence,background,process,result,impact | PARTIAL_SOURCE |
| event-lanyu-an | 蓝玉案（功臣清洗） | 明 | 22.2 | 明史（语料在库，249 篇卷） | 0 | 1 | 0 | people,place,evidence,background,process,result,impact | PARTIAL_SOURCE |
| event-li-zicheng-fazhan | 李自成势力发展 | 明 | 22.2 | 明史（语料在库，249 篇卷） | 0 | 1 | 0 | people,place,evidence,background,process,result,impact | PARTIAL_SOURCE |
| event-hanchu-yixingwang | 剪除异姓诸侯王 | 西汉 | 22.2 | - | 0 | 2 | 0 | people,place,evidence,background,process,result,impact | PARTIAL_SOURCE |
| event-wangmang-fuchu | 王莽复出辅政 | 西汉 | 22.2 | - | 0 | 2 | 0 | people,place,evidence,background,process,result,impact | PARTIAL_SOURCE |

## NEEDS_SOURCE（5）——史源缺库

| event_id | event_name | period | score | source coverage | evidence | people | place | missing | readiness |
|---|---|---|---:|---|---:|---:|---:|---|---|
| event-wuxu-bianfa | 戊戌变法（百日维新与政变） | 晚清 | 22.2 | -；缺 清实录 | 0 | 1 | 0 | people,place,evidence,background,process,result,impact | NEEDS_SOURCE |
| event-tongmenghui-chengli | 中国同盟会成立（东京） | 晚清 | 22.2 | - | 0 | 1 | 0 | people,place,evidence,background,process,result,impact | NEEDS_SOURCE |
| event-zuozongtang-xizheng | 左宗棠西征收复新疆 | 晚清 | 22.2 | -；缺 清实录 | 0 | 1 | 0 | people,place,evidence,background,process,result,impact | NEEDS_SOURCE |
| event-jintian-qiyi | 金田起义（太平天国建立） | 晚清 | 22.2 | -；缺 清实录 | 0 | 1 | 0 | people,place,evidence,background,process,result,impact | NEEDS_SOURCE |
| event-tianjing-xianluo | 湘军攻陷天京（太平天国结束） | 晚清 | 22.2 | -；缺 清实录 | 0 | 1 | 0 | people,place,evidence,background,process,result,impact | NEEDS_SOURCE |

## 选择理由与下一轮注入点

- **唐 8（安史之乱群，READY）+ 1（收复长安，PARTIAL_SOURCE）**：Queue 11 刚恢复的资治通鉴/旧唐书段落锚已入 evidence（ev=1）；people 2–3、place 1；
  缺 background/process/impact 三维，可在 唐纪三十三–三十九 / 旧唐书卷一百五十（章首行已核实为安禄山传）内逐段取据。
- **西汉/秦 8（楚汉群）**：史记（项羽本纪/高祖本纪/陈涉世家）、资治通鉴汉纪一–三、汉书在库；
  巨鹿/鸿门/彭城/荥阳/垓下/秦亡/汉立叙事段落均已在 Queue 11 定位。
- **明 6（PARTIAL）**：明史在库（本纪47/列传198/志4 篇卷），但 events 尚无 evidence 链接、place 全缺；
  下一轮先跑链接 + 章首核实，再进 enrichment。皇太极即后金汗位 另需清实录（缺）。
- **晚清 5（NEEDS_SOURCE）**：清实录/清史稿/光绪朝档案等均不在库；若接入清史稿（PD，维基文库全本）
  可在后续 source 批次解锁。不为时期配额强行选择缺源事件——本组明确不进下一轮。

> 本清单为**选择**结果：未修改任何被选事件（Rule 6：不提前富化 596 Major）。
