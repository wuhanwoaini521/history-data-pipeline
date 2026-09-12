# Batch 02 · Queue 2 — Critical Closure（三个 88.9 → ≥90）

> 任务性质：事件关系策展（related_event curation），非内容生成。
> 处理对象：event-chuzhuang-wang-ba / event-jinwen-gong-ba / event-hezong-lianheng。
> Before：三者均 88.9，唯一缺失维度 = **related_event**（YAML `relations: []`）。

## 2.1 related_event 模型审计（结论：沿用现有 schema，未做任何重设计）

| 项 | 结论 |
|---|---|
| 存储模型 | curated event YAML `relations:` 出边列表 → build 写入 dist `event_relations`（source_event_id = 本事件）。**不是**独立 relation 表驱动，实体/关系同表异列 |
| 合法 relation_type | `precedes / follows / causes / caused_by / leads_to / contributes_to / part_of / related_to`（validate.py 白名单 + schemas/event_relation.schema.json enum，taxonomy/relation_types.yml 定义含 inverse 配对） |
| 方向 | 出边语义：`A --type--> B`；`part_of` 由子事件指向大事件（现有惯例：邲之战→楚庄王、问鼎→楚庄王均为 part_of 出边） |
| 字段约束 | event.schema.json：仅允许 `target_event_id / relation_type / confidence / description_zh_cn`（additionalProperties: false）→ relation_reason 与 curation_note 只能记录于本报告，不得写入 YAML |
| 校验门禁 | validate.py：目标事件必须存在、类型白名单、confidence∈[0,1]、禁止自引用；`history-data backbone validate` 通过 |
| 计分规则 | product_completeness: `related_event = bool(event.relations)`，9 维等权 |
| UI 消费 | dist event_relations 由 Rust/前端关系图与事件详情直接读取（schema 未变，无需 UI 改动） |

## 2.2 建立关系的标准（本轮执行版）

仅当满足以下之一才建边：明确历史因果 / 同一历史进程 / 直接前后继承 / 明确政治军事制度关联。
「同时代」「同国」「同一人物出现」不建边。语料中无直接记载的候选（如楚庄王→鄢陵之战，语料检索「鄢陵」无春秋相关段落）**主动放弃**，未因过线需求硬加。

## 2.3 结果明细

### event-chuzhuang-wang-ba 楚庄王称霸（88.9 → **100.0**）

| relation_added | relation_type | reason | evidence（语料锚点，均已 link 于对应事件 YAML） |
|---|---|---|---|
| → event-jinwen-gong-ba | follows (0.8) | 同一历史进程（晋楚争霸）+ 直接前后继承：城濮晋胜 → 邲之战楚胜，霸权易手 | 史记·楚世家#p172「夏六月，晋救郑，与楚战，大败晋师河上」（本事件已链）；左传·僖公二十八年#p6「晋侯…及楚人战于城濮，楚师败绩」（晋文公事件已链） |
| → event-chengpu-zhizhan | follows (0.8) | 楚庄王霸业是对城濮之败的再起与翻转，属同一晋楚争霸进程 | 同上两条锚点互证 |

### event-jinwen-gong-ba 晋文公称霸（88.9 → **100.0**）

| relation_added | relation_type | reason | evidence |
|---|---|---|---|
| → event-qihuan-gong-ba | follows (0.7) | 同一历史进程（春秋霸主政治）：齐桓首创霸政模式（尊王攘夷、会盟诸侯），晋文公践土会盟接续主盟 | 史记·鲁仲连邹阳列传#p169「晋文公亲其雠，彊霸诸侯；齐桓公用其仇，而一匡天下」（语料实查，桓文并称霸政原型）；左传僖28#p9「盟于践土」（本事件已链） |
| → event-chengpu-zhizhan | caused_by (0.9) | 明确因果：城濮之胜直接确立霸业（践土之盟由此而成）；同时是既有 chengpu→jinwen leads_to(0.9) 的规范逆边 | 左传僖28#p6「战于城濮，楚师败绩」→ #p9「盟于践土」（本事件已链） |
| → event-chuzhuang-wang-ba | precedes (0.7) | 直接前后继承：晋文公霸业（前636—628）先于楚庄王霸业（前613—591），晋楚争霸前后两章；与楚庄王→本事件 follows 互为规范逆边 | 同「楚庄王→晋文公」双锚点 |

### event-hezong-lianheng 合纵连横（88.9 → **100.0**）

| relation_added | relation_type | reason | evidence |
|---|---|---|---|
| → event-shangyang-bianfa | follows (0.7) | 明确历史关联：合纵因秦强而生——变法后秦富强，力量对比促六国并力西向 | 史记·商君列传#p88「居五年，秦人富彊，天子致胙於孝公，诸侯毕贺」（语料实查）；史记·苏秦列传#p69「诸侯之地五倍於秦…并力西乡而攻秦」（本事件已链 background 锚点） |
| → event-zhangyi-po-chu | precedes (0.7) | 同一历史进程（纵横外交）：合纵既成，秦以连横破从相抗；张仪欺楚为连横代表行动（与既有 zhangyi→hezong part_of 出边一致） | 史记·苏秦列传#p186「其後秦使犀首欺齐、魏，与共伐赵，欲败从约」（本事件已链 impact 锚点，破从进程直接文本）；语料含战国策·张仪诸篇 |
| → event-qin-mie-liuguo | leads_to (0.5) | 历史编排关系：合纵最终被秦瓦解、六国各个击破，秦统一为该外交博弈终局（confidence 0.5，属长程结构判断） | 无单句锚点 → curation_note：本边为进程级编排，两端事件叙述均为既有 curated/reviewed 内容，未新增任何事实 |

## 2.4 重新评分

| event | before_score | after_score | relation_added | status |
|---|---:|---:|---:|---|
| event-chuzhuang-wang-ba 楚庄王称霸 | 88.9 | **100.0** | 2 | ✅ closed（≥90） |
| event-jinwen-gong-ba 晋文公称霸 | 88.9 | **100.0** | 3 | ✅ closed（≥90） |
| event-hezong-lianheng 合纵连横 | 88.9 | **100.0** | 3 | ✅ closed（≥90） |

- `history-data backbone validate`：**Validation OK**（periods=31 regimes=64 events=618 stories=3）。
- 全部 8 条新边均为策展关系（precedes/follows/caused_by/leads_to），不发明新 relation_type，不改 schema。
- 放弃项（诚实记录）：楚庄王→鄢陵之战（语料无春秋鄢陵段落，仅元史/明史地名巧合；不凭模型常识建边）；
  合纵连横→信陵君合纵 pre-edge（既有 part_of 逆边即可，避免弱时序边凑数）。
