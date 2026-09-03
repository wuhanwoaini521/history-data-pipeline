# -*- coding: utf-8 -*-
"""China History Backbone V1 — Batch 6（元→元末→明）Data（part 1）。

阶段拆分（阶段提交）：
- YUAN_EARLY  元初/元世祖朝（1260—1300）
- YUAN_MIDDLE 元中期（1300—1350）
- YUAN_LATE   元末社会危机与群雄（1350—1368）
- MING_EARLY  明初（1368—1402）
- MING_MIDDLE 明中期/永乐—嘉靖（1402—1565）
- MING_LATE   晚明/隆万—崇祯（1572—1644）

复用（不重复建档）：event-yuan-jianguo（1271 元建立）；南宋灭亡边界（1276 临安降/1279 崖山）不再重复。
跨阶段关系一律放在"后一阶段的事件上（follows 指向先一阶段）"，阶段提交无需剥离。
"""

from __future__ import annotations

MODERN = {
    "yuan": "韩儒林主编《元朝史》（人民出版社）；周良霄、顾菊英《元代史》（上海人民出版社）；"
            "萧启庆《内北国而外中国》；白寿彝总主编《中国通史·元明清卷》",
    "yuan_late": "陈高华《元末明初的江南社会》与张海瀛等元末农民战争研究；韩儒林《元朝史》；"
                 "白寿彝总主编《中国通史·元明清卷》",
    "ming": "南炳文、汤纲《明史》（上海人民出版社）；孟森《明史讲义》（中华书局）；"
            "白寿彝总主编《中国通史·元明清卷》",
    "ming_late": "樊树志《晚明史》（复旦大学出版社）；顾诚《明末农民战争史》（中国社会科学出版社）；"
                 "南炳文、汤纲《明史》；孟森《明史讲义》",
    "houjin": "稻叶岩吉《清朝全史》（中译本）与《明史·列传》；孙文良、李治亭《明清战争史略》"
              "（辽宁人民出版社）；白寿彝《中国通史·元明清卷》",
}

W = {
    "yuanshi": ["work-curated-yuanshi"],
    "yuanshi_ming": ["work-curated-yuanshi", "work-curated-mingshi"],
    "mingshi": ["work-curated-mingshi"],
    "mingshi_lu": ["work-curated-mingshi", "work-curated-mingshilu"],
    "mingshilu": ["work-curated-mingshilu"],
    "mingshi_qing": ["work-curated-mingshi"],
}


def _rel(target, rtype, confidence=None, desc=None):
    item = {"target_event_id": target, "relation_type": rtype}
    if confidence is not None:
        item["confidence"] = confidence
    if desc:
        item["description_zh_cn"] = desc
    return item


def _ev(id_, name, etype, start, end, precision, period, importance, summary,
        source_ref, source_ids, regimes_or_relations=None, relations=None, review_note=None):
    if regimes_or_relations is not None and regimes_or_relations \
            and all(isinstance(x, str) for x in regimes_or_relations):
        regime_ids = regimes_or_relations
    else:
        regime_ids = []
        relations = relations if relations is not None else (regimes_or_relations or [])
    return {
        "id": id_, "name_zh_cn": name, "event_type": etype,
        "start_year": start, "end_year": end, "date_precision": precision,
        "period_id": period, "importance": importance, "summary_zh_cn": summary,
        "source_ref": source_ref, "source_ids": source_ids,
        "regime_ids": regime_ids or [],
        "relations": relations or [],
        "review_note": review_note,
    }


# ---------------------------------------------------------------------------
# Phase 1 — 元初/元世祖朝（1260—1300）
# ---------------------------------------------------------------------------
PHASE_YUAN_EARLY = [
    _ev("event-yuan-zhongshusheng", "元初中书省设立（中央政务中枢）", "reform",
        1260, 1260, "year", "period-song-liao-jin", "major",
        "中统元年（1260 年），忽必烈在开平即位后设中书省统理政务，"
        "其后不断完善中书省—枢密院—御史台的中枢架构；"
        "中书省与地方行省共同构成元代行政体制的骨干。",
        f"古代史料：《元史·百官志》；现代参考：{MODERN['yuan']}",
        W["yuanshi"],
        ["regime-mongol-empire"],
        relations=[
            _rel("event-yuan-xingsheng-zhidu", "leads_to", 0.8, "中枢中书省制度延伸出地方行省制度。"),
        ]),
    _ev("event-yuan-dingdu-dadu", "元定都大都（营建新城）", "political",
        1267, 1276, "range", "period-yuan", "major",
        "至元四年至十三年（1267—1276 年），忽必烈在金中都旧城东北营建新城，"
        "至元九年（1272 年）命曰大都，至元十三年城成；"
        "大都（今北京）自此成为元朝都城，直至 1368 年明军攻克。",
        f"古代史料：《元史·世祖纪》《地理志》；现代参考：{MODERN['yuan']}",
        W["yuanshi"],
        ["regime-yuan"],
        relations=[
            _rel("event-hubilie-chenghan", "follows", 0.7, "忽必烈即位后营建都城。"),
            _rel("event-yuan-zhongshusheng", "follows", 0.6, "中枢确立后都城营建同步进行。"),
        ]),
    _ev("event-yuan-xingsheng-zhidu", "行省制度确立（分置行中书省）", "reform",
        1276, 1280, "range", "period-yuan", "major",
        "灭南宋前后，元廷在中书省之外于大地区分设行中书省（行省）统领地方军政，"
        "至元年间渐次确立岭北、辽阳、河南江北、陕西、四川、云南、湖广、江西、江浙、甘肃等行省；"
        "行省由朝廷派出机构演变为常设行政区，元代确立的地方行政制度为后世沿用。",
        f"古代史料：《元史·百官志》；现代参考：{MODERN['yuan']}",
        W["yuanshi"],
        ["regime-yuan"],
        relations=[
            _rel("event-yuan-zhongshusheng", "follows", 0.8, "行省为中书省的派出与地方化。"),
            _rel("event-yuan-jianguo", "follows", 0.7, "国号大元后行省制度在灭宋进程中定型。"),
        ],
        review_note="行省制度的具体定型时间各说（至元中后期—大德年间）；本事件取至元年间分置行省"
                    "这一制度建立进程，不作单一日期断言。"),
    _ev("event-yuan-zhongtong-chao", "中统钞发行（元初纸币制度建立）", "economic",
        1260, 1260, "year", "period-song-liao-jin", "major",
        "中统元年（1260 年）发行中统元宝交钞，以银为本位（各钞以银计价），"
        "通行全国并逐步禁止金银铜钱流通，大蒙古国—元朝的纸币制度由此建立。",
        f"古代史料：《元史·食货志》；现代参考：{MODERN['yuan']}",
        W["yuanshi"],
        ["regime-mongol-empire"],
        relations=[
            _rel("event-yuan-zhiyuan-chao", "precedes", 0.7, "中统钞之后的币制调整（至元钞）。"),
        ]),
    _ev("event-yuan-zhiyuan-chao", "至元钞发行与币制调整", "economic",
        1287, 1287, "year", "period-yuan", "major",
        "至元二十四年（1287 年）发行至元通行宝钞，与中统钞以一兑五并行，"
        "钞法自此常有变更，纸币贬值与物价上涨问题成为元代财政长期话题。",
        f"古代史料：《元史·食货志》；现代参考：{MODERN['yuan']}",
        W["yuanshi"],
        ["regime-yuan"],
        relations=[
            _rel("event-yuan-zhongtong-chao", "follows", 0.7, "中统钞基础上的币制改革。"),
        ]),
    _ev("event-yuan-zheng-ri-yi", "元朝第一次征日（文永之役）", "war",
        1274, 1274, "year", "period-yuan", "major",
        "至元十一年（1274 年），元军水陆渡海攻日本，在九州博多湾登陆作战，"
        "遭日军抵抗并因台风受损而撤军（日本方面称文永之役）。",
        f"古代史料：《元史·世祖纪》；《高丽史》相关记载；现代参考：{MODERN['yuan']}",
        W["yuanshi"],
        ["regime-yuan"],
        relations=[
            _rel("event-yuan-zheng-ri-er", "leads_to", 0.8, "第一次征日未成，忽必烈再谋东征。"),
        ]),
    _ev("event-yuan-zheng-ri-er", "元朝第二次征日（弘安之役）", "war",
        1281, 1281, "year", "period-yuan", "major",
        "至元十八年（1281 年），元军两路大军（东路军、江南军）约十万人再度渡海攻日，"
        "在九州、对马等岛登陆作战，遭台风袭击与日军抵抗，元军大部覆没，此后元朝不再征日。",
        f"古代史料：《元史·世祖纪》；现代参考：{MODERN['yuan']}",
        W["yuanshi"],
        ["regime-yuan"],
        relations=[
            _rel("event-yuan-zheng-ri-yi", "follows", 0.9, "第二次更大规模的征日行动。"),
            _rel("event-yuan-zheng-zhuawa", "precedes", 0.6, "征日失败后十余年元军远征爪哇。"),
        ],
        review_note="台风（\"神风\"为日本方面称谓）是元军失败的关键战史因素之一，"
                    "学界亦讨论后勤、飓风时机与指挥问题；不做\"天佑日本\"式渲染。"),
    _ev("event-yuan-aluohe-licai", "阿合马理财与财政之争", "political",
        1262, 1282, "range", "period-yuan", "major",
        "中统三年至至元十九年（1262—1282 年），阿合马长期主持理财"
        "（盐铁榷算、钩考钱谷等），扩充财政收入，遭儒臣集团批评，"
        "至元十九年（1282 年）阿合马在宫廷政变中被刺杀，理财政策随即调整。",
        f"古代史料：《元史·阿合马传》；现代参考：{MODERN['yuan']}",
        W["yuanshi"],
        ["regime-yuan"],
        relations=[
            _rel("event-yuan-xingsheng-zhidu", "precedes", 0.5, "理财扩张与行省体制同时期的财政政治。"),
        ],
        review_note="阿合马理财与桑哥理财常合称\"权臣理财\"；学界对其财政作用评价分歧大，"
                    "本事件记录举措与政争进程，不作单一价值判断。"),
    _ev("event-yuan-naiyan-zhi-luan", "乃颜之乱（辽东宗王反元）", "rebellion",
        1287, 1287, "year", "period-yuan", "major",
        "至元二十四年（1287 年），辽东宗王乃颜联结诸王举兵反元，"
        "忽必烈亲征辽东讨平乃颜；与西北海都战争并行的诸王叛乱冲击元朝统治秩序。",
        f"古代史料：《元史·世祖纪》《乃颜传》相关；现代参考：{MODERN['yuan']}",
        W["yuanshi"],
        ["regime-yuan"],
        relations=[
            _rel("event-yuan-haidu-zhi-luan", "follows", 0.7, "西北海都战事同时期的东北宗王叛乱。"),
        ]),
    _ev("event-yuan-haidu-zhi-luan", "海都之乱（西北诸王战争）", "war",
        1277, 1301, "range", "period-yuan", "major",
        "至元十四年至大德五年（1277—1301 年），窝阔台系海都与察合台系诸王联合，"
        "在阿尔泰山以西长期与元廷作战，忽必烈及其后继者多次遣军征讨，"
        "至 1301 年海都败亡后西北战事方渐平息。",
        f"古代史料：《元史·世祖纪》《成宗纪》；现代参考：{MODERN['yuan']}",
        W["yuanshi"],
        ["regime-yuan"],
        relations=[
            _rel("event-yuan-naiyan-zhi-luan", "precedes", 0.7, "西北诸王战争先于乃颜之乱爆发。"),
        ]),
    _ev("event-yuan-zheng-zhuawa", "元朝远征爪哇", "war",
        1292, 1293, "range", "period-yuan", "major",
        "至元二十九至三十年（1292—1293 年），元朝水师远征爪哇，登陆后应爪哇王伪降"
        "并遭当地势力反攻，元军失利退兵；元朝海外扩张由盛转衰的标志事件。",
        f"古代史料：《元史·外夷传》；现代参考：{MODERN['yuan']}",
        W["yuanshi"],
        ["regime-yuan"],
        relations=[
            _rel("event-yuan-zheng-ri-er", "follows", 0.6, "征日之后的又一次大规模海外远征。"),
        ]),
]


# ---------------------------------------------------------------------------
# Phase 2 — 元中期（1300—1350）
# ---------------------------------------------------------------------------
PHASE_YUAN_MIDDLE = [
    _ev("event-yanyou-kaike", "延祐开科（元代恢复科举）", "reform",
        1313, 1315, "range", "period-yuan", "major",
        "皇庆二年（1313 年）下诏恢复科举，延祐二年（1315 年）举行首科，"
        "分蒙古色目、汉人南人两榜取士，元代科举制度由此建立并延续至元末。",
        f"古代史料：《元史·仁宗纪》选举志；现代参考：{MODERN['yuan']}",
        W["yuanshi"],
        ["regime-yuan"],
        relations=[
            _rel("event-boyan-ba-keju", "leads_to", 0.8, "1335 年伯颜专权时一度罢废科举。"),
        ]),
    _ev("event-yanyou-jingli", "延祐经理（清查田土）", "economic",
        1314, 1315, "range", "period-yuan", "major",
        "延祐元年至二年（1314—1315 年），元廷在江浙、江西、河南等处清查田土（延祐经理），"
        "本意整顿赋役，因地方弊端扰民而中止，暴露元代财政治理困境。",
        f"古代史料：《元史·仁宗纪》食货志；现代参考：{MODERN['yuan']}",
        W["yuanshi"],
        ["regime-yuan"],
        relations=[
            _rel("event-yanyou-kaike", "follows", 0.6, "仁宗朝整顿朝政的配套举措。"),
            _rel("event-zhizhi-xinzheng", "precedes", 0.5, "延祐经理问题延续至英宗朝改革。"),
        ]),
    _ev("event-zhizhi-xinzheng", "至治新政（英宗朝改革）", "reform",
        1321, 1323, "range", "period-yuan", "major",
        "至治元年至三年（1321—1323 年），元英宗与拜住推行新政（减冗费、革弊政、整顿吏治），"
        "触动既得利益集团，至治三年（1323 年）在南坡事变中被弑，新政中止。",
        f"古代史料：《元史·英宗纪》；现代参考：{MODERN['yuan']}",
        W["yuanshi"],
        ["regime-yuan"],
        relations=[
            _rel("event-nanpo-zhi-bian", "leads_to", 0.9, "新政触发的政变。"),
        ]),
    _ev("event-nanpo-zhi-bian", "南坡之变（英宗遇弑）", "political",
        1323, 1323, "year", "period-yuan", "major",
        "至治三年（1323 年）八月，元英宗自上都南还大都途中在南坡驿被御史大夫铁失等弑杀，"
        "随行宰相拜住同遇害；铁失党立泰定帝，英宗新政随之中止，"
        "元朝宫廷政治进入动荡期。",
        f"古代史料：《元史·英宗纪》《泰定帝纪》；现代参考：{MODERN['yuan']}",
        W["yuanshi"],
        ["regime-yuan"],
        relations=[
            _rel("event-zhizhi-xinzheng", "follows", 0.9, "至治新政触发的宫廷政变。"),
            _rel("event-liangdu-zhizhan", "precedes", 0.8, "五年后爆发两都之战（皇位争夺）。"),
        ]),
    _ev("event-liangdu-zhizhan", "两都之战（皇位之争内战）", "war",
        1328, 1328, "year", "period-yuan", "major",
        "泰定帝于致和元年（1328 年）死后，上都集团拥立幼主阿速吉八，"
        "大都集团（燕帖木儿等）拥立图帖睦尔，两都之间爆发内战，"
        "大都集团获胜，图帖睦尔即帝位（文宗），元朝皇权纷争加剧。",
        f"古代史料：《元史·文宗纪》《泰定帝纪》；现代参考：{MODERN['yuan']}",
        W["yuanshi"],
        ["regime-yuan"],
        relations=[
            _rel("event-nanpo-zhi-bian", "follows", 0.8, "泰定帝死后皇位继承之争引发内战。"),
            _rel("event-boyan-ba-keju", "leads_to", 0.7, "文宗朝之后权臣伯颜专权。"),
        ]),
    _ev("event-boyan-ba-keju", "伯颜专权、罢废科举", "political",
        1333, 1340, "range", "period-yuan", "major",
        "元统元年至至元六年（1333—1340 年），权臣伯颜（蔑儿乞伯颜）专权，"
        "至元元年（1335 年）奏请罢科举（后至元元年恢复讨论，1337 年又以\"儒士无用\"再罢），"
        "垄断朝政并压制儒臣，至元六年（1340 年）伯颜被罢黜。",
        f"古代史料：《元史·顺帝纪》；现代参考：{MODERN['yuan']}",
        W["yuanshi"],
        ["regime-yuan"],
        relations=[
            _rel("event-yanyou-kaike", "follows", 0.9, "仁宗开科后被伯颜罢废。"),
            _rel("event-tuotuo-genghua", "leads_to", 0.9, "伯颜罢黜后脱脱执政（脱脱更化）。"),
        ],
        review_note="伯颜专权时间跨度 1333—1340 年；科举罢废的两次诏令时间（1335/1337）史源记载不一，"
                    "本事件按专权与罢科进程记录。"),
    _ev("event-tuotuo-genghua", "脱脱更化（顺帝朝新政）", "reform",
        1340, 1344, "range", "period-yuan", "major",
        "至元六年（1340 年）伯颜罢黜后，脱脱执政推行新政：恢复科举、开经筵、"
        "修辽金宋三史（至正三年至五年，1343—1345 年）等，"
        "元末短暂的政治整理期（脱脱更化）。",
        f"古代史料：《元史·顺帝纪》《脱脱传》；现代参考：{MODERN['yuan']}",
        W["yuanshi"],
        ["regime-yuan"],
        relations=[
            _rel("event-boyan-ba-keju", "follows", 0.9, "伯颜倒台后的政治调整。"),
        ]),
]