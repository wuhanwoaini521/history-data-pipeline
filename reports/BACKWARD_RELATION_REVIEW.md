# BACKWARD_RELATION_REVIEW — Phase 2：62 条 backward EventRelation 人工审阅（agent-assisted）

> 审阅时间: 2026-09-05
> 前置: `reports/EVENT_RELATION_ROOT_CAUSE_AUDIT.md`（Phase 1，Preview 导出 BUG 已修复）
> 输入: `scripts/_backward_62.json`（Phase 1 QA 冻结快照，62 条）
> 工作区文件: `scripts/_analyze_backward_62.py`、`scripts/_print_review_sheet.py`、
> `scripts/_make_verdicts.py`、`scripts/_backward_62_verdicts.json`
> 模式: 只读审阅 · 逐条判定 → 经批准后执行点状 curated 修复（见 §4，7 条错误边已清理）

---

## 1. 定义与方法

Phase 1 的 backward 判定（精确命中 62 条）：

```
relation_type IN ('leads_to','precedes')
AND target.start_year < source.end_year
```

本阶段按「目标事件起点相对源事件的位置」二分：

| 类别 | 条件 | 含义 |
| --- | --- | ---: |
| A. overlap | `tgt_start >= src_start`（目标起点落在源生命周期内） | era 内边 / 同期并行 |
| B. full-reverse | `tgt_start < src_start`（目标起点早于源事件自身起点） | 真正的反向指认 |

另按回指幅度分桶：`p1 |gap|<=2`（27 条，年份精度）→ `p2 <=10`（18）→ `p3 <=50`（16）→ `p4 >50`（1）。
对每条结合 `relation_desc` 与事件 summary 做语义判定。

## 2. 判定标准

| verdict | 含义 | 数量 |
| --- | --- | ---: |
| `keep` | 时序/语义均成立（era 内边、culmination、并行、重叠期因果） | 38 |
| `keep_with_note` | 语义可读但措辞不严格（并行语境的 precedes / amid 语境 / aggregate→开端），保留并记录 | 17 |
| `recommend_reverse` | 方向与其自身 desc 或日期矛盾，建议反向 | 6 |
| `recommend_delete_or_repoint` | 无清晰语义叙事，建议删除或改指向 | 1 |

## 3. 逐条判定表

> ✅ = keep · ⚠️ = keep_with_note · 🔁 = recommend_reverse · ❌ = recommend_delete_or_repoint
> gap = `tgt_start - src_end`（负数为回指年数）

| # | V | relation (src(rel)→tgt) | gap | 判定依据 |
| ---: | - | --- | ---: | --- |
| 1 | ✅ | 班超经营西域(pre)→窦固窦宪北伐 | -2 | 同期对外经略 |
| 2 | ⚠️ | 苏峻之乱(pre)→石勒建立后赵 | -10 | 南北并立语境；precedes 仅表叙事先后 |
| 3 | ✅ | 孙恩卢循起义( leads_to)→刘裕北伐 | -2 | 重叠期内因果（声望鹊起） |
| 4 | ⚠️ | 南唐建立(pre)→石敬瑭灭后唐 | -1 | 1 年交错，政权并立语境 |
| 5 | ⚠️ | 太平天国运动( leads_to)→金田起义 | -13 | aggregate→开端子事件，宜 part_of |
| 6 | ✅ | 阿古柏割据( leads_to)→左宗棠西征 | -1 | 占地促使西征，因果成立 |
| 7 | ✅ | 契丹建国(pre)→后梁代唐 | -9 | 已验证的合法跨 period 并立 |
| 8 | ✅ | 正德朝政治(pre)→宁王之乱 | -2 | era 内边 |
| 9 | ✅ | 东林党争( leads_to)→魏忠贤专权 | -3 | 重叠期因果 |
| 10 | ✅ | 崇祯即位( leads_to)→陕西民变 | -1 | 同期展开 |
| 11 | ✅ | 宋初收兵权(pre)→北宋统一战争 | -1 | 先收权后统一，因果成立 |
| 12 | ✅ | 方腊起义(pre)→海上之盟 | -1 | 宣和二年同时期事件 |
| 13 | ✅ | 元嘉之治(pre)→元嘉北伐 | -23 | era 内边（后期转入北伐） |
| 14 | ⚠️ | 玉壁之战(pre)→西魏府兵制创建 | -3 | 府兵制(543)早于玉壁(546)；「强化」因果可读 |
| 15 | ✅ | 周武帝亲政( leads_to)→北周灭北齐 | -2 | 因果成立 |
| 16 | ✅ | 秦末起义( leads_to)→巨鹿之战 | -1 | 因果成立 |
| 17 | ✅ | 隆武永历(pre)→郑成功取台湾 | -1 | 重叠期内（依托海疆抗清） |
| 18 | ✅ | 摊丁入亩(pre)→改土归流 | -3 | 同期推行 |
| 19 | ✅ | 北伐( leads_to)→南京国民政府 | -1 | 因果成立 |
| 20 | ⚠️ | 百团大战(pre)→长沙会战 | -1 | 1 年交错，敌后/正面战场并行 |
| 21 | ✅ | 中国远征军(pre)→豫湘桂战役 | -1 | 重叠期内 |
| 22 | 🔁 | 冉魏建立(pre)→前燕崛起 | -15 | desc「冉魏亡于前燕扩张」已自证方向反了 |
| 23 | 🔁 | 苻坚即位(pre)→前燕崛起 | -20 | 无 desc；前燕(337..352)整体早于苻坚(357) |
| 24 | ✅ | 前秦瓦解( leads_to)→后燕建立 | -10 | 同年因果成立 |
| 25 | ⚠️ | 北魏建立(pre)→前秦瓦解 | -2 | amid 语境（崩溃中重建），措辞不严谨 |
| 26 | ✅ | 建炎南渡(pre)→黄天荡之战 | -8 | 重叠期内 |
| 27 | 🔁 | 崖山海战( leads_to)→宋蒙战争 | -44 | desc「宋蒙战争以南宋灭亡告终」，方向应反转 |
| 28 | ✅ | 管仲改革( leads_to)→齐桓公称霸 | -34 | era 内因果（改革成就霸业） |
| 29 | ✅ | 城濮之战( leads_to)→晋文公称霸 | -4 | culmination 型（战胜确立霸权） |
| 30 | ⚠️ | 崤之战( leads_to)→秦穆公称霸西戎 | -32 | span 大部早于崤之战；实指后期成就，事件跨度偏大所致 |
| 31 | ✅ | 开皇之治(pre)→隋文帝废太子 | -4 | era 内边 |
| 32 | 🔁 | 隋灭陈(pre)→陈霸先建陈 | -32 | desc「陈朝自557年建立，589年亡」，方向应反转 |
| 33 | ✅ | 营建东都(pre)→开凿大运河 | -1 | 同期工程群 |
| 34 | ⚠️ | 隋征吐谷浑(pre)→开凿大运河 | -4 | 西征与工程并举（政策群并行） |
| 35 | ✅ | 窦建德据河北(pre)→瓦岗军崛起 | -2 | 南北民变并立 |
| 36 | ✅ | 杜伏威据江淮(pre)→江都兵变 | -1 | 相先后叙事 |
| 37 | ⚠️ | 李渊太原起兵(pre)→瓦岗军崛起 | -1 | 隋末群雄并行语境 |
| 38 | ✅ | 唐统一全国(pre)→玄武门之变 | -2 | era 内边 |
| 39 | ✅ | 虎牢之战( leads_to)→唐统一全国 | -3 | culmination 型 |
| 40 | ✅ | 贞观之治(pre)→唐灭东突厥 | -19 | era 内边（扩张标志） |
| 41 | ⚠️ | 安西四镇格局(pre)→唐太宗征高句丽 | -3 | 「太宗末年同时经营」并行语境 |
| 42 | ⚠️ | 唐高宗即位(pre)→唐太宗征高句丽 | -4 | 「承太宗基业」承接语境，非严格先后 |
| 43 | ✅ | 废王立武(pre)→唐灭西突厥 | -2 | 重叠期内 |
| 44 | 🔁 | 唐灭高句丽(pre)→白江口之战 | -5 | desc「白江口（663）先行」，方向应反转 |
| 45 | ⚠️ | 大非川之战(pre)→唐灭高句丽 | -2 | 「战线由东转向西」转段叙事，前 2 年可接受 |
| 46 | ❌ | 武则天临朝(pre)→大非川之战 | -20 | 无 desc、无因果叙事；683 无法先于 670 |
| 47 | ✅ | 姚宋执政( leads_to)→开元盛世 | -15 | culmination 型 |
| 48 | ✅ | 开元盛世(pre)→李林甫执政 | -5 | era 尾边（由盛转衰） |
| 49 | 🔁 | 吐蕃攻入长安(pre)→大非川之战 | -93 | desc「自大非川之胜后持续东进」，方向应反转 |
| 50 | ✅ | 河朔三镇割据(pre)→两税法实施 | -1 | 财政回应因果 |
| 51 | ✅ | 元和削藩( leads_to)→元和中兴 | -14 | culmination 型 |
| 52 | ⚠️ | 元和中兴(pre)→宦官统领神策军 | -24 | desc 意为「中兴后宦官更张」，但目标(796..806)早于中兴主段；后续宜改指向更晚事件 |
| 53 | ✅ | 牛李党争(pre)→会昌灭佛 | -1 | era 尾边 |
| 54 | ⚠️ | 甘露之变(pre)→牛李党争 | -14 | 党争(821 起)早于甘露(835)；「变后继续缠斗」era 语境 |
| 55 | ✅ | 王仙芝起义( leads_to)→黄巢起义 | -3 | 因果成立 |
| 56 | ✅ | 黄巢败亡( leads_to)→朱温势力上升 | -1 | 因果成立 |
| 57 | ⚠️ | 孙权称帝(pre)→诸葛亮北伐 | -1 | 1 年交错，吴蜀并立语境 |
| 58 | ⚠️ | 高平陵之变(pre)→姜维北伐 | -2 | 姜维北伐(247 起)早于高平陵(249)，并行语境 |
| 59 | ⚠️ | 三家分晋( leads_to)→李悝变法 | -3 | 变法(-406 起)略早于分晋(-403)；desc 已注明「为其中最早者」 |
| 60 | ✅ | 文景之治(pre)→晁错削藩 | -14 | era 尾边 |
| 61 | ✅ | 阿合马理财(pre)→行省制度确立 | -6 | 同期财政政治 |
| 62 | ✅ | 海都之乱(pre)→乃颜之乱 | -14 | 1277 起兵确实先于 1287（仅因源 span 长而入选） |

## 4. 修复执行（已实施，2026-09-05）

实际执行与 §4 原计划的差异：核对 curated YAML 发现其中 5 条错误边的**反向边已存在**
（`song-meng-zhanzheng leads_to yanya-haizhan`、`chenbaxian precedes sui-mie-chen`、
`baijiangkou follows tang-mie-gaogouli`、`qian-yan-qiang follows ran-wei`、
`dafeichuan precedes wu-zhao-linchao`），因此这些条目只需删除错误边，无需重复添加：

| # | 执行动作 | 文件（data/curated/history_backbone/events/…） |
| ---: | --- | --- |
| 22 | 删除错误边（反向 follows 边已存在于 qian-yan-qiang） | `jin_southern_northern/event-ran-wei.yml` |
| 23 | 删除错误边 + 新增 `qian-yan-qiang --precedes--> fu-jian-wangmeng`（conf 0.6，秦燕先后崛起对峙） | `jin_southern_northern/event-fu-jian-wangmeng.yml`、`event-qian-yan-qiang.yml` |
| 27 | 删除错误边（反向 leads_to 边已存在于 song-meng-zhanzheng） | `song_liao_xia_jin/event-yanya-haizhan.yml` |
| 32 | 删除错误边（反向 precedes 边已存在于 chenbaxian-jianzhen） | `jin_southern_northern/event-sui-mie-chen.yml` |
| 44 | 删除错误边（反向 follows 边已存在于 baijiangkou-zhizhan） | `sui_tang/event-tang-mie-gaogouli.yml` |
| 49 | 删除错误边 + 新增 `dafeichuan --precedes--> tubo-ru-changan`（conf 0.7，自大非川之胜后持续东进） | `sui_tang/event-tubo-ru-changan.yml`、`event-dafeichuan-zhizhan.yml` |
| 46 | 删除错误边（反向 precedes 边已存在于 dafeichuan-zhizhan，desc「唐蕃冲突贯穿高宗后期与武周」） | `sui_tang/event-wu-zhao-linchao.yml` |

## 5. 修复后 QA（实际结果，dist 重建后）

- `event_relations`：1062 → **1057**（-7 +2），`test_backbone_build.py` 基数已同步更新
- **backward(leads_to/precedes)：62 → 55**
- dangling source / dangling target / self-loop / duplicate(s,t,type) 全部 **0**
- 7 条错误边全部确认移除，2 条新增方向边确认存在（`scripts/_qa_after_fix.py`）
- `tests/test_backbone_build.py` + `tests/test_preview_relations.py`：11 passed；全量
  `1 failed → 已修复`、5 errors（`data/normalized/history.duckdb` 未在本机构建，环境性问题，与本次修改无关）

## 6. 结论

```
BACKWARD_62_REVIEWED = true
KEEP = 38  ·  KEEP_WITH_NOTE = 17  ·  RECOMMEND_REVERSE = 6  ·  RECOMMEND_DELETE_OR_REPOINT = 1
FIXED = 7（-7 wrong edges +2 corrected direction edges）
BACKWARD_AFTER = 55  ·  EVENT_RELATIONS_AFTER = 1057
VALIDATION_OK = true  ·  QA_ALL_ZERO_DANGLING_DUP = true
```

62 条 backward 中 **91.9%**（38+17）为 era 内边/并行语境/culmination 型的合理表达，
真正的方向错误为 7 条（11.3%… 按条目计 7/62），全部有 desc 或日期自证，修复方案见 §4。
与 Phase 1 结论一致：**Backbone 数据本身健康，无需重建 1062 条 Relation**；
7 条方向修复属于点状 curated 修订。
