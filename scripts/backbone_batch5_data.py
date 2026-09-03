# -*- coding: utf-8 -*-
"""China History Backbone V1 — Batch 5（北宋·辽·西夏·金·南宋·蒙古/元边界）Data（part 1）。

阶段拆分（阶段提交）：
- SONG_FOUNDATION  北宋建立（960—979）
- SONG_LIAO_XIA    宋辽/宋夏/庆历（979—1100）
- REFORM_AND_JIN   熙丰元祐 + 金崛起（1067—1125）
- JINGKANG_NANSONG 靖康 + 南宋初 + 宋金战争（1126—1165）
- SOUTHERN_SONG_LATE 开禧嘉定 + 蒙古灭夏金 + 宋蒙 + 元建立/南宋亡（1206—1279）

复用（不重复建档）：event-guo-wei-dai-han（951 后周建立，作为 960 代周的前节点）。
"""

from __future__ import annotations

MODERN = {
    "song": "白寿彝总主编《中国通史·宋辽金元卷》" 
            "；邓广铭《北宋政治改革家王安石》（生活·读书·新知三联书店）"
            "；漆侠《王安石变法》（河北人民出版社）；王曾瑜《岳飞新传》（上海古籍出版社）",
    "songliao": "白寿彝总主编《中国通史·宋辽金元卷》"
                "；刘浦江《辽金史论》（辽宁大学出版社）"
                "；吴天墀《西夏史稿》（四川人民出版社）；李焘《续资治通鉴长编》点校本校点本身为现代整理",
    "songjin": "徐梦莘《三朝北盟会编》所存宋金交涉史料；王曾瑜《岳飞新传》；"
               "白寿彝总主编《中国通史·宋辽金元卷》；邓广铭《岳飞传》（三联书店）",
    "yuan": "韩儒林主编《元朝史》（人民出版社）；周良霄、顾菊英《元代史》（上海人民出版社）；"
            "白寿彝总主编《中国通史·宋辽金元卷》；萧启庆《内北国而外中国》（中华书局）",
}

W = {
    "songshi": ["work-curated-songshi"],
    "songshi_cb": ["work-curated-songshi", "work-curated-xuzizhitongjianchangbian"],
    "cb": ["work-curated-xuzizhitongjianchangbian"],
    "jinshi": ["work-curated-jinshi"],
    "songshi_jinshi": ["work-curated-songshi", "work-curated-jinshi"],
    "liaoshi_song": ["work-curated-liaoshi", "work-curated-songshi"],
    "yuanshi": ["work-curated-yuanshi"],
    "yuanshi_jinshi": ["work-curated-yuanshi", "work-curated-jinshi"],
    "songshi_yuan": ["work-curated-songshi", "work-curated-yuanshi"],
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
# Phase 1 — 北宋建立（960—979）
# ---------------------------------------------------------------------------
PHASE_SONG_FOUNDATION = [
    _ev("event-chenqiao-bingbian", "陈桥兵变、赵匡胤称帝、北宋建立", "foundation",
        960, 960, "year", "period-northern-song", "critical",
        "建隆元年正月（960 年），后周殿前都点检赵匡胤在陈桥驿发动兵变，回京代周称帝，"
        "改国号为宋，定都开封（东京），史称北宋。五代十国局面结束，"
        "后周诸州军政多不战而降，北宋开启统一战争。",
        f"古代史料：《宋史·太祖纪》；《续资治通鉴长编》建隆元年；现代参考：{MODERN['song']}",
        W["songshi_cb"],
        ["regime-northern-song"],
        relations=[
            _rel("event-guo-wei-dai-han", "follows", 0.8,
                 "951 年郭威代汉建立后周；960 年赵匡胤陈桥兵变代周建宋（政权转换）。"),
            _rel("event-song-tongyi-zhanzheng", "leads_to", 0.9, "北宋建国后随即开始统一战争。"),
        ],
        review_note="陈桥兵变与\"黄袍加身\"的直接细节以《续资治通鉴长编》等较晚史源记载为主，"
                    "本事件记录 960 年代周称帝这一既成事实；后周恭帝年幼是政变背景而非单一原因。"),
    _ev("event-song-shou-bingquan", "宋初收兵权（罢宿将典禁兵）", "reform",
        961, 963, "range", "period-northern-song", "major",
        "建隆二年至乾德元年（961—963 年），宋太祖罢去石守信、王审琦等宿将的禁军统帅职务，"
        "以\"三衙\"（殿前司、侍卫马军司、侍卫步军司）分掌禁军、枢密院掌军政，"
        "形成强干弱枝、兵权集于中央的军事制度安排，北宋开国\"杯酒释兵权\"即指此一过程。",
        f"古代史料：《续资治通鉴长编》建隆二年七月；现代参考：{MODERN['song']}",
        W["cb"],
        [],
        relations=[
            _rel("event-chenqiao-bingbian", "follows", 0.7, "建国后随即调整禁军统帅权。"),
            _rel("event-song-tongyi-zhanzheng", "precedes", 0.6, "收兵权先于大规模统一作战展开。"),
        ],
        review_note="\"杯酒释兵权\"见于《续资治通鉴长编》等较晚史源，早期文献未载，"
                    "学者对其是否以设宴方式举行有争议；本事件记录罢宿将典禁兵的事实进程。"),
    _ev("event-song-tongyi-zhanzheng", "北宋统一战争", "unification",
        962, 979, "range", "period-northern-song", "major",
        "建隆三年至太平兴国四年（962—979 年），北宋先后平定荆南（963）、后蜀（965）、"
        "南汉（971）、南唐（975），吴越纳土（978），收复北汉（979），统一中原与南方大部。"
        "本事件为 aggregate，子事件（灭荆南、灭后蜀、灭南汉、灭南唐、吴越纳土、灭北汉）"
        "经 part_of 关联。",
        f"古代史料：《宋史·太祖纪》《太宗纪》；《续资治通鉴长编》；现代参考：{MODERN['song']}",
        W["songshi_cb"],
        ["regime-northern-song"],
        relations=[
            _rel("event-chenqiao-bingbian", "follows", 0.8, "960 年建国后开始统一进程。"),
        ]),
    _ev("event-song-mie-jingnan", "北宋灭荆南（平荆湖）", "war",
        963, 963, "year", "period-northern-song", "major",
        "乾德元年（963 年），北宋以讨伐张文表为名假道荆南，一举收降荆南高氏并与湖南周行逢势力"
        "合并处置，随即进取湖南，是为统一战争第一步（平荆湖）。",
        f"古代史料：《宋史·太祖纪》；《续资治通鉴长编》乾德元年；现代参考：{MODERN['song']}",
        W["songshi_cb"],
        ["regime-northern-song", "regime-jingnan"],
        relations=[
            _rel("event-song-tongyi-zhanzheng", "part_of", 0.9, "统一战争第一阶段。"),
            _rel("event-song-mie-houshu", "precedes", 0.6, "荆湖平定后西进攻蜀。"),
        ]),
    _ev("event-song-mie-houshu", "北宋灭后蜀", "war",
        965, 965, "year", "period-northern-song", "major",
        "乾德三年（965 年），北宋两路大军攻蜀，孟昶投降，后蜀灭亡；"
        "宋军自剑门、三峡两路入川，历时约两个月。",
        f"古代史料：《宋史·太祖纪》；现代参考：{MODERN['song']}",
        W["songshi_cb"],
        ["regime-northern-song", "regime-later-shu"],
        relations=[
            _rel("event-song-tongyi-zhanzheng", "part_of", 0.9, "统一战争第二阶段。"),
            _rel("event-song-mie-jingnan", "follows", 0.6, "963 年平荆湖后取蜀。"),
            _rel("event-song-mie-nanhan", "precedes", 0.6, "平蜀后转向南汉。"),
        ]),
    _ev("event-song-mie-nanhan", "北宋灭南汉", "war",
        971, 971, "year", "period-northern-song", "major",
        "开宝四年（971 年），北宋大军南下，南汉刘鋹出降，南汉灭亡，岭南并入北宋版图。",
        f"古代史料：《宋史·太祖纪》；现代参考：{MODERN['song']}",
        W["songshi_cb"],
        ["regime-northern-song", "regime-southern-han"],
        relations=[
            _rel("event-song-tongyi-zhanzheng", "part_of", 0.9, "统一战争第三阶段。"),
            _rel("event-song-mie-houshu", "follows", 0.6, "965 年灭后蜀后南进。"),
            _rel("event-song-mie-nantang", "precedes", 0.6, "灭南汉后攻南唐。"),
        ]),
    _ev("event-song-mie-nantang", "北宋灭南唐", "war",
        975, 975, "year", "period-northern-song", "major",
        "开宝八年（975 年），北宋曹彬率军攻金陵（江宁府），南唐后主李煜出降，南唐灭亡；"
        "灭南唐之战决定性地结束了五代十国南方割据格局。",
        f"古代史料：《宋史·太祖纪》；《续资治通鉴长编》开宝八年；现代参考：{MODERN['song']}",
        W["songshi_cb"],
        ["regime-northern-song", "regime-southern-tang"],
        relations=[
            _rel("event-song-tongyi-zhanzheng", "part_of", 0.9, "统一战争第四阶段。"),
            _rel("event-song-mie-nanhan", "follows", 0.6, "971 年灭南汉后攻南唐（跨江作战）。"),
            _rel("event-wuyue-natu", "precedes", 0.5, "南唐灭亡后吴越失去依托。"),
        ],
        review_note="王安石《桂枝香》等文学书写与史实分属不同层；本事件按《续资治通鉴长编》"
                    "记载的开宝七年冬—八年十一月围城与降服过程记录。"),
    _ev("event-wuyue-natu", "吴越纳土归宋", "war",
        978, 978, "year", "period-northern-song", "major",
        "太平兴国三年（978 年），吴越王钱俶入朝，主动献纳两浙十三州之地，吴越国结束，"
        "五代十国最后的江南割据政权以和平方式并入北宋。",
        f"古代史料：《宋史·世家》；《续资治通鉴长编》太平兴国三年；现代参考：{MODERN['song']}",
        W["songshi_cb"],
        ["regime-northern-song", "regime-wuyue"],
        relations=[
            _rel("event-song-tongyi-zhanzheng", "part_of", 0.9, "统一战争第五阶段（和平纳土）。"),
            _rel("event-song-mie-nantang", "follows", 0.6, "975 年灭南唐后吴越纳土。"),
            _rel("event-song-mie-beihan", "precedes", 0.6, "纳土后北宋北攻北汉。"),
        ]),
    _ev("event-song-mie-beihan", "北宋收复北汉", "war",
        979, 979, "year", "period-northern-song", "major",
        "太平兴国四年（979 年），宋太宗亲征，围太原，北汉主刘继元出降，"
        "北汉灭亡（此为中国历史上一统王朝统一的收尾之战，其后契丹/辽成为主要对手）。",
        f"古代史料：《宋史·太宗纪》；《续资治通鉴长编》太平兴国四年；现代参考：{MODERN['song']}",
        W["songshi_cb"],
        ["regime-northern-song", "regime-northern-han"],
        relations=[
            _rel("event-song-tongyi-zhanzheng", "part_of", 0.9, "统一战争最后阶段。"),
            _rel("event-wuyue-natu", "follows", 0.6, "978 年吴越纳土后北攻。"),
            _rel("event-gaolianghe-zhizhan", "precedes", 0.8, "灭北汉同年夏，宋军转攻燕云败于高梁河。"),
        ]),
]


# ---------------------------------------------------------------------------
# Phase 2 — 宋辽 / 宋夏 / 庆历（979—1100）
# ---------------------------------------------------------------------------
PHASE_SONG_LIAO_XIA = [
    _ev("event-gaolianghe-zhizhan", "高梁河之战", "war",
        979, 979, "year", "period-northern-song", "major",
        "太平兴国四年（979 年），宋太宗灭北汉后随即亲率大军攻辽南京（幽州），"
        "在高梁河（今北京西郊一带）被辽军与援军内外夹击大败，宋太宗受伤南逃，"
        "北宋第一次伐辽（收复燕云）尝试失败，此后宋辽进入长期对峙。",
        f"古代史料：《宋史·太宗纪》；《辽史·景宗纪》；现代参考：{MODERN['songliao']}",
        W["liaoshi_song"],
        ["regime-northern-song", "regime-liao"],
        relations=[
            _rel("event-song-mie-beihan", "follows", 0.8, "灭北汉同年攻辽失败。"),
            _rel("event-yongxi-beifa", "precedes", 0.7, "高梁河之败后七年北宋再伐（雍熙北伐）。"),
        ]),
    _ev("event-yongxi-beifa", "雍熙北伐", "war",
        986, 987, "range", "period-northern-song", "major",
        "雍熙三年（986 年），宋太宗分东中西三路大举北伐辽国，东路曹彬在岐沟关败北，"
        "全线溃退，西路杨业（杨继业）在陈家谷口被俘绝食而死，北伐以失败告终，"
        "北宋自此放弃大规模收复燕云的军事行动。",
        f"古代史料：《宋史·太宗纪》；《辽史·圣宗纪》；现代参考：{MODERN['songliao']}",
        W["liaoshi_song"],
        ["regime-northern-song", "regime-liao"],
        relations=[
            _rel("event-gaolianghe-zhizhan", "follows", 0.8, "继高梁河之战后的第二次大规模北伐。"),
            _rel("event-chanyuan-zhi-meng", "precedes", 0.8, "北伐失败后宋辽转入守势与和议。"),
        ]),
    _ev("event-wangxiaobo-li-shun-qiyi", "王小波、李顺起义（四川）", "rebellion",
        993, 995, "range", "period-northern-song", "major",
        "淳化四年至五年（993—995 年），四川王小波、李顺先后领导民变，"
        "提出\"均贫富\"口号，攻占成都，建国号大蜀，后被北宋官军镇压，"
        "宋代规模最大的一次境内民变。",
        f"古代史料：《宋史·太宗纪》；现代参考：{MODERN['song']}",
        W["songshi"],
        [],
        relations=[
            _rel("event-yongxi-beifa", "follows", 0.5, "北伐失败后数年四川发生大规模民变。"),
        ]),
    _ev("event-li-jiqian-juxia", "李继迁据夏州、党项势力兴起", "political",
        985, 997, "range", "period-northern-song", "major",
        "雍熙二年至至道三年（985—997 年），党项首领李继迁起兵据银、夏等州，"
        "一度降辽受封，后向宋称臣受封夏州定难军节度使，"
        "奠定此后西夏政权割据西北的基础。",
        f"古代史料：《宋史·夏国传》；《续资治通鉴长编》；现代参考：{MODERN['songliao']}",
        W["songshi_cb"],
        ["regime-northern-song", "regime-liao"],
        relations=[
            _rel("event-western-xia-jianguo", "leads_to", 0.7, "李继迁系党项势力数十年后由李元昊建立西夏。"),
        ]),
    _ev("event-chanyuan-zhi-meng", "澶州之战与澶渊之盟", "treaty",
        1004, 1005, "range", "period-northern-song", "major",
        "景德元年（1004 年）辽圣宗大举南侵，宋真宗亲征至澶州（今河南濮阳），"
        "辽军主帅萧挞凛被宋军射杀，双方罢兵议和，次年（1005 年）正月订立澶渊之盟："
        "宋辽约为兄弟之国，宋岁输银绢，边境开榷场互市，维持约百年和平。",
        f"古代史料：《宋史·真宗纪》；《辽史·圣宗纪》；现代参考：{MODERN['songliao']}",
        W["liaoshi_song"],
        ["regime-northern-song", "regime-liao"],
        relations=[
            _rel("event-yongxi-beifa", "follows", 0.8, "雍熙北伐失败后宋辽攻守转换，澶渊之盟终结了大规模战争。"),
            _rel("event-chongxi-zengbi", "leads_to", 0.7, "1042 年辽索关南地，宋增岁币（重熙增币）。"),
        ],
        review_note="澶州之战与澶渊之盟为同一和平进程的两阶段，合并建一事件避免 Action/Outcome 重复；"
                    "\"澶渊之盟\"为传统称谓（澶渊即澶州）。"),
    _ev("event-sanchuankou-zhizhan", "三川口之战", "war",
        1040, 1040, "year", "period-western-xia", "major",
        "康定元年（1040 年），西夏李元昊攻宋延州，宋军在三川口战败，"
        "宋夏战争第一阶段（宋军连战皆败）开始。",
        f"古代史料：《宋史·仁宗纪》；现代参考：{MODERN['songliao']}",
        W["songshi"],
        ["regime-western-xia", "regime-northern-song"],
        relations=[
            _rel("event-western-xia-jianguo", "follows", 0.8, "西夏建国（1038）后随即爆发宋夏战争。"),
            _rel("event-haoshuichuan-zhizhan", "follows", 0.7, "三川口之战次年好水川之战。"),
        ]),
    _ev("event-haoshuichuan-zhizhan", "好水川之战", "war",
        1041, 1041, "year", "period-western-xia", "major",
        "庆历元年（1041 年），宋军任福部在好水川（今宁夏隆德境）遭西夏军设伏全军覆没，"
        "宋夏战争第二大战役以宋军惨败告终。",
        f"古代史料：《宋史·仁宗纪》；现代参考：{MODERN['songliao']}",
        W["songshi"],
        ["regime-western-xia", "regime-northern-song"],
        relations=[
            _rel("event-sanchuankou-zhizhan", "follows", 0.8, "三川口之败后宋军再败。"),
            _rel("event-dingchuanzhai-zhizhan", "precedes", 0.8, "好水川之战后次年定川寨之战。"),
        ]),
    _ev("event-dingchuanzhai-zhizhan", "定川寨之战", "war",
        1042, 1042, "year", "period-western-xia", "major",
        "庆历二年（1042 年），西夏军再攻宋泾原路，宋将葛怀敏战死，"
        "宋军在定川寨遭遇第三次大败，此后宋夏双方皆疲，转向议和。",
        f"古代史料：《宋史·仁宗纪》；现代参考：{MODERN['songliao']}",
        W["songshi"],
        ["regime-western-xia", "regime-northern-song"],
        relations=[
            _rel("event-haoshuichuan-zhizhan", "follows", 0.8, "第三次大会战。"),
            _rel("event-qingli-heyi", "leads_to", 0.8, "三川口、好水川、定川寨三败后宋夏议和。"),
        ]),
    _ev("event-chongxi-zengbi", "重熙增币（辽索关南地、宋增岁币）", "treaty",
        1042, 1042, "year", "period-liao", "major",
        "庆历二年（1042 年，辽重熙十一年），辽兴宗以索晋阳及瓦桥关以南十县地为名南压，"
        "北宋遣富弼使辽，最终以增岁币银绢各十万两匹（在澶渊之盟基础上增纳）换和，"
        "宋辽关系维持，但北宋财政负担加重。",
        f"古代史料：《宋史·仁宗纪》《富弼传》；《辽史·兴宗纪》；现代参考：{MODERN['songliao']}",
        W["liaoshi_song"],
        ["regime-northern-song", "regime-liao"],
        relations=[
            _rel("event-chanyuan-zhi-meng", "follows", 0.8, "澶渊之盟后宋辽关系的增币调整。"),
        ]),
    _ev("event-qingli-heyi", "庆历和议（宋夏议和）", "treaty",
        1044, 1044, "year", "period-western-xia", "major",
        "庆历四年（1044 年），宋夏订立和约：西夏向宋称臣（名义），"
        "宋册封李元昊为夏国主、岁赐银绢茶等，重开榷场贸易，"
        "宋夏战争第一阶段结束。",
        f"古代史料：《宋史·仁宗纪》；《宋史·夏国传》；现代参考：{MODERN['songliao']}",
        W["songshi"],
        ["regime-western-xia", "regime-northern-song"],
        relations=[
            _rel("event-dingchuanzhai-zhizhan", "follows", 0.9, "三战三败后达成的和议。"),
        ]),
    _ev("event-qingli-xinzheng", "庆历新政", "reform",
        1043, 1044, "range", "period-northern-song", "major",
        "庆历三年（1043 年）范仲淹出任参知政事，提出明黜陟、抑侥幸、精贡举等十事改革方案，"
        "史称庆历新政；因遭保守势力反对，一年多后即告失败，范仲淹等相继去职，"
        "为北宋中期政治改革（后之王安石变法）的先声。",
        f"古代史料：《宋史·范仲淹传》；《续资治通鉴长编》庆历三年至四年；现代参考：{MODERN['song']}",
        W["songshi_cb"],
        [],
        relations=[
            _rel("event-wanganshi-bianfa", "precedes", 0.6, "庆历新政失败二十余年后王安石变法（先声）。"),
        ]),
    _ev("event-western-xia-jianguo", "李元昊称帝、西夏建立", "foundation",
        1038, 1038, "year", "period-western-xia", "critical",
        "宝元元年（1038 年）十月，夏国王李元昊称帝建国，国号大夏（史称西夏），"
        "定都兴庆府（今宁夏银川），与北宋、辽成鼎足之势；"
        "此前元昊父祖（李继迁、李德明）已割据夏州、灵州一带。",
        f"古代史料：《宋史·夏国传》；《续资治通鉴长编》；现代参考：{MODERN['songliao']}",
        W["songshi_cb"],
        ["regime-western-xia"],
        relations=[
            _rel("event-li-jiqian-juxia", "follows", 0.8, "李继迁以来的党项割据势力发展为独立政权。"),
            _rel("event-sanchuankou-zhizhan", "leads_to", 0.9, "称帝建国后宋夏战争爆发。"),
        ],
        review_note="西夏建国时间以元昊称帝（1038）计；\"西夏\"为后世称谓，当时国号为大夏。"),
]