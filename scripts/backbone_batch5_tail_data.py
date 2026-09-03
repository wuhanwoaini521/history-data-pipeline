# -*- coding: utf-8 -*-
"""China History Backbone V1 — Batch 5（北宋·辽·西夏·金·南宋·蒙古/元）Data（part 2）。

含 Phase 3—5 与 PHASES / ALL_PHASES / all_events 聚合导出。
"""

from __future__ import annotations

from backbone_batch5_data import MODERN, W, _ev, _rel, PHASE_SONG_FOUNDATION, PHASE_SONG_LIAO_XIA  # noqa: F401

# ---------------------------------------------------------------------------
# Phase 3 — 熙丰·元祐·绍圣 + 金崛起（1067—1125）
# ---------------------------------------------------------------------------
PHASE_REFORM_AND_JIN = [
    _ev("event-wanganshi-bianfa", "王安石变法（熙宁新法）", "reform",
        1069, 1076, "range", "period-northern-song", "major",
        "熙宁二年至元丰前（1069—1076 年），王安石在宋神宗支持下推行新法，"
        "先后颁行均输、青苗、免役（募役）、市易、保甲、方田均税等法，"
        "并开边熙河、改革科举；因新旧党争与实施中的问题，熙宁七年、九年两度罢相，"
        "元丰年间神宗继续推行部分新法。",
        f"古代史料：《宋史·王安石传》《神宗纪》；《续资治通鉴长编》；现代参考：{MODERN['song']}",
        W["songshi_cb"],
        [],
        relations=[
            _rel("event-qingli-xinzheng", "follows", 0.6, "庆历新政失败后的又一次大规模变法。"),
            _rel("event-yuanfeng-gaizhi", "leads_to", 0.7, "熙宁新法体系后神宗元丰年间改制官制。"),
            _rel("event-yuanyou-genghua", "leads_to", 0.8, "哲宗初年高太后听政，罢新法（元祐更化）。"),
        ],
        review_note="青苗、募役、保甲、市易等为新法的主要内容，本事件作为一个政治改革进程统一记录，"
                    "不逐法单列事件（避免概念碎片化）；对旧党把新法失败归于王安石个人及"
                    "\"变法一律扰民\"的说法，学界有争议，本事件按制度颁布与罢行过程陈述。"),
    _ev("event-yuanfeng-gaizhi", "元丰改制（官制改革）", "reform",
        1080, 1082, "range", "period-northern-song", "major",
        "元丰三年至五年（1080—1082 年），宋神宗依据《唐六典》改革官制，"
        "恢复三省六部职能、以阶官寄禄，罢去使职差遣的冗制，"
        "是国家行政制度的一次系统整理。",
        f"古代史料：《宋史·神宗纪》《职官志》；现代参考：{MODERN['song']}",
        W["songshi"],
        [],
        relations=[
            _rel("event-wanganshi-bianfa", "follows", 0.7, "熙宁新法推行后神宗继续改制。"),
            _rel("event-yuanyou-genghua", "precedes", 0.6, "元丰改制后哲宗初年政治转向。"),
        ]),
    _ev("event-yuanyou-genghua", "元祐更化（司马光执政、罢新法）", "political",
        1086, 1089, "range", "period-northern-song", "major",
        "元祐元年（1086 年），哲宗年幼、高太后听政，起用司马光等旧党，"
        "尽罢熙宁新法，史称元祐更化；新旧党争自此进入反复更迭阶段。",
        f"古代史料：《宋史·哲宗纪》；《续资治通鉴长编》元祐；现代参考：{MODERN['song']}",
        W["songshi_cb"],
        [],
        relations=[
            _rel("event-wanganshi-bianfa", "follows", 0.9, "司马光执政后新法尽罢。"),
            _rel("event-shaosheng-shaoshu", "leads_to", 0.8, "哲宗亲政后绍述熙丰（绍圣绍述）。"),
        ]),
    _ev("event-shaosheng-shaoshu", "绍圣绍述（哲宗恢复熙丰新法）", "political",
        1094, 1098, "range", "period-northern-song", "major",
        "绍圣元年（1094 年），哲宗亲政，以\"绍述\"熙宁、元丰之政为名恢复新法，"
        "贬逐元祐旧党，新旧党争的报复性循环加剧，北宋中后期政局在党派反复中走向衰落。",
        f"古代史料：《宋史·哲宗纪》；现代参考：{MODERN['song']}",
        W["songshi"],
        [],
        relations=[
            _rel("event-yuanyou-genghua", "follows", 0.8, "元祐更化后哲宗亲政转而绍述新法。"),
        ]),
    _ev("event-fangla-qiyi", "方腊起义（睦州）", "rebellion",
        1120, 1121, "range", "period-northern-song", "major",
        "宣和二年至三年（1120—1121 年），两浙睦州青溪方腊聚众起义，"
        "攻占六州五十余县，后童贯率军镇压，方腊被俘遇害；"
        "起义与花石纲及东南赋役有关，是北宋末江南社会矛盾的集中爆发。",
        f"古代史料：《宋史·徽宗纪》；现代参考：{MODERN['song']}",
        W["songshi"],
        [],
        relations=[
            _rel("event-hai-shang-zhi-meng", "precedes", 0.5, "与宋金海上之盟同时期（宣和二年）。"),
        ]),
    _ev("event-wanyan-aguda-qibing", "女真完颜部起兵反辽", "war",
        1114, 1114, "year", "period-jin", "major",
        "天庆四年（1114 年），完颜阿骨打聚合女真诸部起兵反辽，"
        "先后在宁江州、出河店击败辽军，女真军事联盟形成，金国建立的直接前奏。",
        f"古代史料：《金史·太祖纪》；现代参考：{MODERN['songliao']}",
        W["jinshi"],
        ["regime-jin"],
        relations=[
            _rel("event-jin-jianguo", "leads_to", 0.9, "起兵次年阿骨打称帝建金。"),
            _rel("event-liao-miewang", "precedes", 0.6, "反辽战争最终导致辽的灭亡。"),
        ]),
    _ev("event-jin-jianguo", "金国建立（阿骨打称帝）", "foundation",
        1115, 1115, "year", "period-jin", "critical",
        "收国元年（1115 年）正月，完颜阿骨打称帝建国，国号大金，都上京会宁府（今黑龙江阿城），"
        "金成为辽后期与北宋北方并存的强大势力，随即发动灭辽战争。",
        f"古代史料：《金史·太祖纪》；现代参考：{MODERN['songliao']}",
        W["jinshi"],
        ["regime-jin"],
        relations=[
            _rel("event-wanyan-aguda-qibing", "follows", 0.9, "1114 年起兵后建国。"),
            _rel("event-hai-shang-zhi-meng", "precedes", 0.8, "金立国五年后宋遣使海路通好（海上之盟）。"),
        ]),
    _ev("event-hai-shang-zhi-meng", "海上之盟（宋金联合攻辽）", "alliance",
        1120, 1120, "year", "period-northern-song", "major",
        "宣和二年（1120 年），北宋徽宗君臣经登州海路遣使赴金，与金缔结盟约："
        "宋金夹攻辽国，灭辽后燕云十六州之地归还北宋（金取中京、宋取燕京）；"
        "盟约随后因宋军攻燕不力及金军索价而埋下宋金冲突伏笔。",
        f"古代史料：《宋史·徽宗纪》；《三朝北盟会编》；现代参考：{MODERN['songjin']}",
        W["songshi"],
        ["regime-northern-song", "regime-jin"],
        relations=[
            _rel("event-jin-jianguo", "follows", 0.7, "金立国后宋金缔约。"),
            _rel("event-liao-miewang", "leads_to", 0.9, "盟约目标为联合灭辽。"),
        ],
        review_note="海上之盟导致\"燕京空城\"与岁币增额等后续争议；燕云归属问题最终在宋金之间"
                    "以金占燕京、宋输岁币收场，详见公元 1123 年（宣和五年）燕京交割记载。"),
    _ev("event-liao-miewang", "金灭辽（天祚帝被俘）", "war",
        1122, 1125, "range", "period-liao", "major",
        "保大二年至五年（1122—1125 年），金军攻陷辽中京、南京（燕京），"
        "辽天祚帝西逃，1125 年 2 月在应州（今山西应县）附近被金军俘获，辽亡；"
        "金自此直接与北宋接壤，成为宋北方最大的威胁。",
        f"古代史料：《金史·太宗纪》；《辽史·天祚帝纪》；现代参考：{MODERN['songliao']}",
        W["jinshi"],
        ["regime-jin", "regime-liao"],
        relations=[
            _rel("event-hai-shang-zhi-meng", "follows", 0.8, "海上之盟后宋金联合灭辽。"),
            _rel("event-jin-di-yici-weikaifeng", "leads_to", 0.8, "灭辽后次年（1125 年）金攻宋第一次围开封。"),
        ]),
]


# ---------------------------------------------------------------------------
# Phase 4 — 靖康之变 + 南宋建立 + 宋金战争（1126—1165）
# ---------------------------------------------------------------------------
PHASE_JINGKANG_NANSONG = [
    _ev("event-jin-di-yici-weikaifeng", "金军第一次围攻开封", "war",
        1126, 1126, "year", "period-northern-song", "major",
        "靖康元年正月（1126 年），金军东、西两路南下，围困北宋都城开封，"
        "宋钦宗起用李纲守城，金军攻城不利，宋廷割太原、中山、河间三镇并许增岁币求和，"
        "金军北撤；求和过程中主战与主和两派反复，北宋朝政动荡。",
        f"古代史料：《宋史·钦宗纪》；《三朝北盟会编》；现代参考：{MODERN['songjin']}",
        W["songshi"],
        ["regime-jin", "regime-northern-song"],
        relations=[
            _rel("event-liao-miewang", "follows", 0.9, "金灭辽后借口背盟南侵。"),
            _rel("event-jin-di-erci-weikaifeng", "leads_to", 0.9, "金军北撤后同年秋冬再围开封。"),
        ]),
    _ev("event-jin-di-erci-weikaifeng", "金军第二次围攻开封、城陷", "war",
        1126, 1126, "year", "period-northern-song", "major",
        "靖康元年闰十一月（1126 年），金军再度南下围攻开封，"
        "十一月二十五日开封外城被攻破，宋钦宗出降，北宋都城陷落。",
        f"古代史料：《宋史·钦宗纪》；《三朝北盟会编》；现代参考：{MODERN['songjin']}",
        W["songshi"],
        ["regime-jin", "regime-northern-song"],
        relations=[
            _rel("event-jin-di-yici-weikaifeng", "follows", 0.9, "第一次围城退兵后金军再度南下。"),
            _rel("event-jingkang-zhi-bian", "leads_to", 0.95, "城陷后徽钦二帝被俘（靖康之变）。"),
        ]),
    _ev("event-jingkang-zhi-bian", "靖康之变、北宋灭亡", "dynastic-transition",
        1127, 1127, "year", "period-northern-song", "critical",
        "靖康二年（1127 年），金军掳宋徽宗、钦宗二帝及后妃宗室大臣北去，"
        "北宋灭亡；史称靖康之变（靖康之难）。此前金已在开封册立伪楚（张邦昌），"
        "中原政权易主，宋朝宗室南迁。",
        f"古代史料：《宋史·钦宗纪》；《三朝北盟会编》；现代参考：{MODERN['songjin']}",
        W["songshi"],
        ["regime-jin", "regime-northern-song"],
        relations=[
            _rel("event-jin-di-erci-weikaifeng", "follows", 0.95, "开封城陷后二帝被俘。"),
            _rel("event-zhao-gou-nansong-jianguo", "leads_to", 0.9, "康王赵构南渡即位，建立南宋。"),
        ]),
    _ev("event-zhao-gou-nansong-jianguo", "赵构称帝、南宋建立", "foundation",
        1127, 1127, "year", "period-southern-song", "critical",
        "建炎元年五月初一（1127 年），康王赵构在南京应天府（今河南商丘）即位，"
        "史称宋高宗，重建宋政权，史称南宋；南宋承袭北宋法统，但江南为统治重心。",
        f"古代史料：《宋史·高宗纪》；《续资治通鉴长编》后卷（建炎以来系年要录）：；现代参考：{MODERN['songjin']}",
        W["songshi"],
        ["regime-southern-song"],
        relations=[
            _rel("event-jingkang-zhi-bian", "follows", 0.95, "北宋灭亡后高宗即位延续宋统。"),
            _rel("event-jianyan-nandu", "leads_to", 0.9, "即位后随即南渡。"),
        ]),
    _ev("event-jianyan-nandu", "建炎南渡（宋廷南迁临安）", "migration",
        1127, 1138, "range", "period-southern-song", "major",
        "建炎元年至绍兴八年（1127—1138 年），宋高宗经历扬州之难（1129 年）后渡江南逃，"
        "辗转江淮浙闽，绍兴八年（1138 年）正式定都临安（今杭州），南宋政权趋于稳定。",
        f"古代史料：《宋史·高宗纪》；现代参考：{MODERN['songjin']}",
        W["songshi"],
        ["regime-southern-song"],
        relations=[
            _rel("event-zhao-gou-nansong-jianguo", "follows", 0.9, "即位后南渡定都。"),
            _rel("event-huangtiandang-zhizhan", "precedes", 0.6, "南渡期间宋金在长江沿线交战（黄天荡）。"),
        ]),
    _ev("event-huangtiandang-zhizhan", "黄天荡之战", "war",
        1130, 1130, "year", "period-southern-song", "major",
        "建炎四年（1130 年），金军完颜宗弼（兀术）南下追宋高宗，北返时在镇江黄天荡"
        "被韩世忠部堵截四十余日，金军开渠决堤突围退走；"
        "此战标志南宋军事实力足以依托江淮防线与金对峙，亦展示宋金在长江沿岸的拉锯。",
        f"古代史料：《宋史·韩世忠传》；《三朝北盟会编》；现代参考：{MODERN['songjin']}",
        W["songshi"],
        ["regime-southern-song", "regime-jin"],
        relations=[
            _rel("event-jianyan-nandu", "follows", 0.7, "南渡期间宋金长江沿线交战。"),
            _rel("event-shunchang-zhizhan", "precedes", 0.7, "此后宋金战争转向中原方向（绍兴十年）。"),
        ]),
    _ev("event-shunchang-zhizhan", "顺昌之战", "war",
        1140, 1140, "year", "period-southern-song", "major",
        "绍兴十年（1140 年）五月，金军毁约南下，刘锜率八字军坚守顺昌（今安徽阜阳），"
        "以少胜多击退金军，为宋军反攻拉开序幕。",
        f"古代史料：《宋史·刘锜传》；现代参考：{MODERN['songjin']}",
        W["songshi"],
        ["regime-southern-song", "regime-jin"],
        relations=[
            _rel("event-huangtiandang-zhizhan", "follows", 0.6, "宋金和议破裂前后（绍兴十年）的守卫战。"),
            _rel("event-yancheng-zhizhan", "precedes", 0.8, "顺昌之战当月，岳飞部在河南方向反攻（郾城）。"),
        ]),
    _ev("event-yancheng-zhizhan", "郾城之战（岳飞北伐）", "war",
        1140, 1140, "year", "period-southern-song", "major",
        "绍兴十年（1140 年）七月，岳飞率部在郾城（今属河南漯河）与金军主力决战，"
        "以背嵬军等击退金军重甲骑兵，取得北伐中的关键胜利，"
        "其后宋廷一日十二道金字牌催令班师（史料见《建炎以来系年要录》等，学界对金牌说尚有考订）。",
        f"古代史料：《宋史·岳飞传》；现代参考：{MODERN['songjin']}",
        W["songshi"],
        ["regime-southern-song", "regime-jin"],
        relations=[
            _rel("event-shunchang-zhizhan", "follows", 0.8, "绍兴十年宋军全线反攻中的主战场。"),
            _rel("event-yuefei-banshi", "leads_to", 0.9, "郾城大捷后宋廷令班师。"),
        ]),
    _ev("event-yuefei-banshi", "岳飞班师（北伐中止、解除兵权）", "political",
        1140, 1141, "range", "period-southern-song", "major",
        "绍兴十年至十一年（1140—1141 年），前线宋军奉令班师，岳飞北伐中止；"
        "绍兴十一年春，岳飞、韩世忠等被解除兵权，宋廷转向与金议和。",
        f"古代史料：《宋史·岳飞传》；现代参考：{MODERN['songjin']}",
        W["songshi"],
        ["regime-southern-song"],
        relations=[
            _rel("event-yancheng-zhizhan", "follows", 0.9, "郾城大捷后奉诏班师。"),
            _rel("event-shaoxing-heyi", "leads_to", 0.9, "罢兵权后宋金订立绍兴和议。"),
        ],
        review_note="\"十二道金牌\"为后世叙事；现存较直接史源为班师诏令（《金佗稡编》载）与"
                    "\"撼山易，撼岳家军难\"等时人语。\"直捣黄龙\"为岳飞班师时之志向表述，"
                    "属言行记载，不作为既成事实写入主干。"),
    _ev("event-shaoxing-heyi", "绍兴和议（宋金划淮为界）", "treaty",
        1141, 1142, "range", "period-southern-song", "major",
        "绍兴十一年至十二年（1141—1142 年），宋金订立和议：宋向金称臣纳贡，"
        "以淮水—大散关一线为界，南宋放弃北方领土，双方各守疆界，"
        "宋金第一次和议确立了两国长期对峙的基本格局。",
        f"古代史料：《宋史·高宗纪》；《金史·熙宗纪》；现代参考：{MODERN['songjin']}",
        W["songshi_jinshi"],
        ["regime-southern-song", "regime-jin"],
        relations=[
            _rel("event-yuefei-banshi", "follows", 0.9, "班师与解除兵权后和议达成。"),
            _rel("event-yuefei-beisha", "precedes", 0.8, "和议期间岳飞被处死（绍兴十一年岁末）。"),
        ]),
    _ev("event-yuefei-beisha", "岳飞被害（大理寺狱）", "political",
        1142, 1142, "year", "period-southern-song", "major",
        "绍兴十一年十二月二十九日（公历 1142 年 1 月 27 日），岳飞在大理寺狱中被处死，"
        "其子岳云、部将张宪同遇害；孝宗朝追复岳飞官爵，宁宗朝追封鄂王、谥武穆，"
        "岳飞经南宋中后期追崇成为抗金象征人物。",
        f"古代史料：《宋史·岳飞传》；现代参考：{MODERN['songjin']}",
        W["songshi"],
        ["regime-southern-song"],
        relations=[
            _rel("event-shaoxing-heyi", "follows", 0.85, "绍兴和议签订期间岳飞遇害。"),
        ],
        review_note="岳飞狱案诏狱罪名由南宋朝廷议定，后世对其冤情及高宗、秦桧各自责任有大量研究，"
                    "存在不同评价；本事件记录处死与日后平反追崇的事实进程，不作煽情价值判断。"),
    _ev("event-hailing-nanzheng", "海陵王南征（完颜亮攻宋）", "war",
        1158, 1161, "range", "period-jin", "major",
        "正隆三年至六年（1158—1161 年），金海陵王完颜亮迁都燕京、大举征调兵民，"
        "1161 年亲率大军分路南攻南宋，意图统一南北；",
        f"古代史料：《金史·海陵纪》；现代参考：{MODERN['songjin']}",
        W["jinshi"],
        ["regime-jin", "regime-southern-song"],
        relations=[
            _rel("event-shaoxing-heyi", "follows", 0.7, "绍兴和议二十年后金毁约南侵。"),
            _rel("event-caishi-zhizhan", "leads_to", 0.9, "南征军在采石渡江失败。"),
        ]),
    _ev("event-caishi-zhizhan", "采石之战", "war",
        1161, 1161, "year", "period-southern-song", "major",
        "绍兴三十一年（1161 年）十一月，金军主力在采石（今安徽马鞍山）渡江，"
        "宋中书舍人虞允文督战于采石矶，以水军击败金军，金军渡江失败，"
        "完颜亮在扬州军中被废杀，金军北撤。",
        f"古代史料：《宋史·虞允文传》；《金史·海陵纪》；现代参考：{MODERN['songjin']}",
        W["songshi_jinshi"],
        ["regime-southern-song", "regime-jin"],
        relations=[
            _rel("event-hailing-nanzheng", "follows", 0.9, "海陵南征军渡江受挫。"),
            _rel("event-jin-shizong-jiwei", "precedes", 0.8, "金世宗已于十月在辽阳即位，采石败后海陵被废杀。"),
        ]),
    _ev("event-jin-shizong-jiwei", "金世宗即位（东京辽阳）", "succession",
        1161, 1162, "range", "period-jin", "major",
        "正隆六年（1161 年）十月，金东京留守完颜雍（世宗）在辽阳即位，"
        "废海陵王；海陵南征失败后在扬州被杀，世宗政权稳定，金转入守势与重建（大定之治背景）。",
        f"古代史料：《金史·世宗纪》；现代参考：{MODERN['songjin']}",
        W["jinshi"],
        ["regime-jin"],
        relations=[
            _rel("event-caishi-zhizhan", "follows", 0.85, "世宗即位与海陵南征失败同年。"),
            _rel("event-longxing-beifa", "precedes", 0.8, "金世宗初年，南宋孝宗发动隆兴北伐。"),
        ],
        review_note="世宗朝相对安定被称为\"大定之治\"（后世概括），本事件只记权力交接及其直接政治后果，"
                    "不把\"治世\"评价当事件。"),
    _ev("event-longxing-beifa", "隆兴北伐", "war",
        1163, 1163, "year", "period-southern-song", "major",
        "隆兴元年（1163 年），宋孝宗起用张浚北伐，宋军一度收复部分州县，"
        "后在符离之战惨败，北伐失败，南宋转入议和。",
        f"古代史料：《宋史·孝宗纪》；现代参考：{MODERN['songjin']}",
        W["songshi"],
        ["regime-southern-song", "regime-jin"],
        relations=[
            _rel("event-jin-shizong-jiwei", "follows", 0.8, "金世宗初年南宋乘机北伐。"),
            _rel("event-longxing-heyi", "leads_to", 0.95, "符离之败后议和（隆兴和议）。"),
        ]),
    _ev("event-longxing-heyi", "隆兴和议（宋金改名分、减岁币）", "treaty",
        1164, 1165, "range", "period-southern-song", "major",
        "隆兴二年至乾道元年（1164—1165 年），宋金订立和议：宋对金关系由\"称臣\"改为\"叔侄\"，"
        "岁贡改称岁币并较绍兴和议减十万之数，疆界仍以淮水—大散关为界；"
        "宋金格局长期稳定。",
        f"古代史料：《宋史·孝宗纪》；《金史·世宗纪》；现代参考：{MODERN['songjin']}",
        W["songshi_jinshi"],
        ["regime-southern-song", "regime-jin"],
        relations=[
            _rel("event-longxing-beifa", "follows", 0.95, "北伐失败后达成的和议。"),
            _rel("event-kaixi-beifa", "precedes", 0.8, "四十余年后南宋再启北伐（开禧北伐）。"),
        ]),
]


# ---------------------------------------------------------------------------
# Phase 5 — 开禧嘉定 + 蒙古灭夏金 + 宋蒙战争 + 元建立/南宋亡（1206—1279）
# ---------------------------------------------------------------------------
PHASE_SOUTHERN_SONG_LATE = [
    _ev("event-kaixi-beifa", "开禧北伐", "war",
        1206, 1207, "range", "period-southern-song", "major",
        "开禧二年（1206 年），南宋权臣韩侂胄发动北伐，志在恢复中原，"
        "因准备不足，宋军全线受挫，金军反攻淮南，开禧三年（1207 年）韩侂胄被杀求和。",
        f"古代史料：《宋史·宁宗纪》；《金史·章宗纪》；现代参考：{MODERN['songjin']}",
        W["songshi_jinshi"],
        ["regime-southern-song", "regime-jin"],
        relations=[
            _rel("event-longxing-heyi", "follows", 0.8, "隆兴和议四十余年后南宋再度北伐。"),
            _rel("event-jiading-heyi", "leads_to", 0.95, "北伐失败后订立嘉定和议。"),
        ]),
    _ev("event-jiading-heyi", "嘉定和议（宋金增岁币）", "treaty",
        1208, 1208, "year", "period-southern-song", "major",
        "嘉定元年（1208 年），宋金订立和议：岁币由绢银各二十万增至三十万两匹，"
        "宋与金维持叔侄关系，函韩侂胄之首以谢罪（另偿金犒军银三百万两）；"
        "此后宋金均积弱，北方蒙古崛起改变格局。",
        f"古代史料：《宋史·宁宗纪》；《金史·章宗纪》；现代参考：{MODERN['songjin']}",
        W["songshi_jinshi"],
        ["regime-southern-song", "regime-jin"],
        relations=[
            _rel("event-kaixi-beifa", "follows", 0.95, "开禧北伐失败后的和议。"),
        ]),
    _ev("event-mongol-jianguo", "铁木真统一蒙古、建立大蒙古国", "foundation",
        1206, 1206, "year", "period-song-liao-jin", "critical",
        "开禧二年（1206 年），铁木真统一蒙古诸部，在斡难河源即大汗位，称成吉思汗，"
        "建立大蒙古国（Yeke Mongghol Ulus）；此为蒙古帝国的开端，"
        "与 1271 年改国号\"大元\"（regime-yuan）为两个不同政权阶段。",
        f"古代史料：《元史·太祖纪》；《蒙古秘史》；现代参考：{MODERN['yuan']}",
        W["yuanshi"],
        ["regime-mongol-empire"],
        relations=[
            _rel("event-yefengling-zhizhan", "leads_to", 0.9, "蒙古建国五年后发动对金战争。"),
            _rel("event-yuan-jianguo", "precedes", 0.7, "1206 年大蒙古国 1271 年改国号大元。"),
        ],
        review_note="1206 年建国与 1271 年元朝建立之间为大蒙古国阶段（regime-mongol-empire），"
                    "两者并列而非同一政权行化（§7 禁止\"1206 之后全部 regime-yuan\"）。"),
    _ev("event-yefengling-zhizhan", "野狐岭之战", "war",
        1211, 1211, "year", "period-song-liao-jin", "major",
        "大安三年（1211 年），成吉思汗亲率蒙古军攻金，在野狐岭（今河北万全一带）"
        "歼灭金军主力，金国北方防线崩溃，此后金军只能依托中都（北京）与黄河防守。",
        f"古代史料：《元史·太祖纪》；《金史·章宗纪》；现代参考：{MODERN['yuan']}",
        W["yuanshi"],
        ["regime-mongol-empire", "regime-jin"],
        relations=[
            _rel("event-mongol-jianguo", "follows", 0.9, "建蒙古国后首攻金国。"),
            _rel("event-jin-qian-du-bian", "leads_to", 0.8, "中都受威胁，金宣宗迁都开封。"),
        ]),
    _ev("event-jin-qian-du-bian", "金迁都开封（中都陷蒙古）", "political",
        1214, 1215, "range", "period-jin", "major",
        "贞祐二年（1214 年），金宣宗迫于蒙古军压力迁都南京（汴京开封）；"
        "次年（1215 年）蒙古军攻占中都（今北京），金国黄河以北领土丧失大半，"
        "政权退守河南，蒙古攻金进入第二阶段。",
        f"古代史料：《金史·宣宗纪》；《元史·太祖纪》；现代参考：{MODERN['yuan']}",
        W["yuanshi_jinshi"],
        ["regime-jin", "regime-mongol-empire"],
        relations=[
            _rel("event-yefengling-zhizhan", "follows", 0.9, "野狐岭之败后金退守河南。"),
            _rel("event-mongol-mie-xia", "precedes", 0.6, "迁都期间蒙古转向攻西夏。"),
        ]),
    _ev("event-mongol-mie-xia", "蒙古灭西夏", "war",
        1226, 1227, "range", "period-western-xia", "major",
        "宝庆二年（1226 年），成吉思汗亲率大军攻夏，次年（1227 年）围中兴府（今银川），"
        "夏末帝李睍出降（一说城降后被屠），西夏亡；成吉思汗当年在六盘山地区去世，"
        "蒙古遂以全力攻金。",
        f"古代史料：《元史·太祖纪》；《宋史·夏国传》；现代参考：{MODERN['yuan']}",
        W["yuanshi"],
        ["regime-mongol-empire", "regime-western-xia"],
        relations=[
            _rel("event-yefengling-zhizhan", "follows", 0.7, "蒙古伐金同时先灭西夏剪除侧翼。"),
            _rel("event-mongol-mie-jin", "leads_to", 0.9, "灭夏后蒙古全力攻金。"),
        ],
        review_note="西夏亡国具体经过（末帝出降及屠城说）史源间存在出入，"
                    "本事件按《元史·太祖纪》《宋史·夏国传》的灭夏时间框架记录。"),
    _ev("event-mongol-mie-jin", "蒙古灭金（蔡州之战）", "war",
        1232, 1234, "range", "period-jin", "major",
        "绍定五年至端平元年（1232—1234 年），蒙古军大举攻金，金哀宗弃汴京南走蔡州；"
        "1234 年正月，蒙古与南宋联军会攻蔡州，城破，金哀宗自缢（末帝承麟被杀），金亡。"
        "灭金是蒙古与南宋三方（蒙古+南宋+金）关系的终结节点。",
        f"古代史料：《元史·太宗纪》；《金史·哀宗纪》；《宋史·理宗纪》；现代参考：{MODERN['yuan']}",
        W["yuanshi_jinshi"],
        ["regime-mongol-empire", "regime-jin", "regime-southern-song"],
        relations=[
            _rel("event-mongol-mie-xia", "follows", 0.8, "灭夏后蒙古与宋联合灭金。"),
            _rel("event-duanping-ru-luo", "leads_to", 0.9, "灭金后宋军入洛引发宋蒙冲突。"),
        ]),
    _ev("event-duanping-ru-luo", "端平入洛（宋蒙冲突开端）", "war",
        1234, 1235, "range", "period-song-liao-jin", "major",
        "端平元年（1234 年）六月，南宋理宗乘金亡之机派兵收复三京（东京开封、西京洛阳、南京归德），"
        "宋军入洛遭蒙古军回击大败而还（端平入洛），宋蒙关系由此破裂，"
        "蒙古随即以征宋为目标发动全面战争。",
        f"古代史料：《宋史·理宗纪》；《元史·太宗纪》；现代参考：{MODERN['yuan']}",
        W["songshi_yuan"],
        ["regime-southern-song", "regime-mongol-empire"],
        relations=[
            _rel("event-mongol-mie-jin", "follows", 0.9, "金亡当年宋军北上入洛。"),
            _rel("event-song-meng-zhanzheng", "leads_to", 0.9, "冲突升级为宋蒙全面战争。"),
        ]),
    _ev("event-song-meng-zhanzheng", "宋蒙战争", "war",
        1235, 1279, "range", "period-song-liao-jin", "major",
        "端平二年至祥兴二年（1235—1279 年），蒙古（后期为元）对南宋发动持续战争，"
        "分四川、京湖、两淮三个战场，历时四十余年，最终以元灭南宋结束。"
        "本事件为 aggregate，子事件（蒙古灭大理、钓鱼城之战、襄樊之战）经 part_of 关联。",
        f"古代史料：《宋史·理宗纪》；《元史·世祖纪》；现代参考：{MODERN['yuan']}",
        W["songshi_yuan"],
        ["regime-southern-song", "regime-mongol-empire"],
        relations=[
            _rel("event-duanping-ru-luo", "follows", 0.9, "端平入洛后宋蒙全面开战。"),
            _rel("event-yanya-haizhan", "leads_to", 0.95, "战争以 1279 年崖山海战南宋灭亡告终。"),
        ]),
    _ev("event-mongol-mie-dali", "蒙古灭大理（征宋西南）", "war",
        1253, 1254, "range", "period-song-liao-jin", "major",
        "宝祐元年至二年（1253—1254 年），忽必烈率蒙古军绕道西南征大理，"
        "灭大理国（段氏），大理并入蒙古，南宋西南方面被迂回包围，"
        "为后来元灭宋的战略完成一环。",
        f"古代史料：《元史·世祖纪》；现代参考：{MODERN['yuan']}",
        W["yuanshi"],
        ["regime-mongol-empire", "regime-southern-song"],
        relations=[
            _rel("event-song-meng-zhanzheng", "part_of", 0.9, "宋蒙战争西南战区的战略行动。"),
        ]),
    _ev("event-diaoyucheng-zhizhan", "钓鱼城之战（蒙哥去世）", "war",
        1258, 1259, "range", "period-song-liao-jin", "major",
        "宝祐六年至开庆元年（1258—1259 年），蒙古大汗蒙哥亲征四川，"
        "围攻合州钓鱼城（今重庆合川）半年不下，1259 年七月蒙哥死于军中（病卒或中炮说，史源有出入），"
        "蒙古军北撤；南宋川防得以延续，蒙哥之死也使蒙古汗位继承悬而未决。",
        f"古代史料：《元史·宪宗纪》；《宋史·理宗纪》；现代参考：{MODERN['yuan']}",
        W["yuanshi"],
        ["regime-mongol-empire", "regime-southern-song"],
        relations=[
            _rel("event-song-meng-zhanzheng", "part_of", 0.9, "宋蒙战争四川战场的关键要塞攻防。"),
            _rel("event-hubilie-chenghan", "leads_to", 0.8, "蒙哥卒后忽必烈与阿里不哥争位，忽必烈称汗。"),
        ],
        review_note="蒙哥死因（病逝或中箭/中炮说）各史源记载不一，学界未有定论；"
                    "本事件按死于钓鱼城下军中、蒙古军北撤的事实框架记录。"),
    _ev("event-hubilie-chenghan", "忽必烈称汗（与阿里不哥争位）", "succession",
        1260, 1260, "year", "period-song-liao-jin", "major",
        "中统元年（1260 年）三月，忽必烈在开平（今内蒙古正蓝旗）即蒙古大汗位，"
        "其弟阿里不哥同年在和林称汗，爆发争位内战；"
        "至元元年（1264 年）阿里不哥降附，忽必烈巩固汗位，蒙古政治重心渐向中原转移。",
        f"古代史料：《元史·世祖纪》；现代参考：{MODERN['yuan']}",
        W["yuanshi"],
        ["regime-mongol-empire"],
        relations=[
            _rel("event-diaoyucheng-zhizhan", "follows", 0.8, "蒙哥死后汗位继承之争。"),
            _rel("event-yuan-jianguo", "leads_to", 0.9, "巩固汗位后改国号大元。"),
        ]),
    _ev("event-xiangfan-zhizhan", "襄樊之战（襄阳失守）", "war",
        1267, 1273, "range", "period-song-liao-jin", "major",
        "咸淳三年至九年（1267—1273 年），元军围困襄阳、樊城六年，"
        "1273 年 2 月樊城先破，襄阳守将吕文焕降元，"
        "南宋长江中游门户洞开，元军遂顺江而下攻临安。",
        f"古代史料：《元史·世祖纪》；《宋史·理宗纪》；现代参考：{MODERN['yuan']}",
        W["songshi_yuan"],
        ["regime-yuan", "regime-southern-song"],
        relations=[
            _rel("event-song-meng-zhanzheng", "part_of", 0.9, "宋蒙战争京湖战场决战。"),
            _rel("event-linan-touxiang", "leads_to", 0.95, "襄阳失守后元军南下，临安投降。"),
        ]),
    _ev("event-yuan-jianguo", "元朝建立（改国号大元）", "foundation",
        1271, 1271, "year", "period-yuan", "critical",
        "至元八年（1271 年）十一月，忽必烈采纳刘秉忠等建议，"
        "取《易经》\"大哉乾元\"之义改国号为\"大元\"；"
        "大蒙古国（1206—1271，regime-mongol-empire）至此以\"元\"为国号，"
        "1279 年灭南宋后成为统治全中国的王朝。",
        f"古代史料：《元史·世祖纪》；现代参考：{MODERN['yuan']}",
        W["yuanshi"],
        ["regime-yuan"],
        relations=[
            _rel("event-hubilie-chenghan", "follows", 0.8, "忽必烈巩固汗位后改国号。"),
            _rel("event-linan-touxiang", "leads_to", 0.9, "元军攻灭南宋（1276 临安降、1279 崖山）。"),
        ],
        review_note="1271 年改国号大元为元朝建立标志（§6 允许建立 1271 元建立作边界 Event）；"
                    "元朝内部（制度、行政）展开留待 Batch 6。"),
    _ev("event-linan-touxiang", "元军攻陷临安、南宋恭帝出降", "war",
        1275, 1276, "range", "period-southern-song", "major",
        "德祐元年至二年（1275—1276 年），元丞相伯颜统军自建康东下，"
        "于丁家洲大败宋军，进围临安；1276 年正月，宋恭帝赵㬎奉表出降，"
        "临安城陷落，南宋大批宗室、百官随之北迁。",
        f"古代史料：《宋史·瀛国公纪》；《元史·世祖纪》；现代参考：{MODERN['yuan']}",
        W["songshi_yuan"],
        ["regime-yuan", "regime-southern-song"],
        relations=[
            _rel("event-xiangfan-zhizhan", "follows", 0.95, "襄阳失守后元军顺江而下。"),
            _rel("event-wentianxiang-kangyuan", "precedes", 0.7, "临安降后南宋流亡朝廷继续抵抗（文天祥等）。"),
            _rel("event-yanya-haizhan", "leads_to", 0.9, "临安降后南宋余部转战闽广，至崖山覆亡。"),
        ]),
    _ev("event-wentianxiang-kangyuan", "文天祥抗元与就义", "political",
        1276, 1283, "range", "period-southern-song", "major",
        "德祐二年至至元二十年（1276—1283 年），南宋右相文天祥在临安降后组织抗元，"
        "于循州五坡岭（1278 年）被俘，坚拒劝降，1283 年 1 月 9 日在大都（今北京）就义；"
        "文天祥被俘期间所写《过零丁洋》《正气歌》等成为后世传诵的忠义书写。",
        f"古代史料：《宋史·文天祥传》；现代参考：{MODERN['yuan']}",
        W["songshi"],
        ["regime-southern-song", "regime-yuan"],
        relations=[
            _rel("event-linan-touxiang", "follows", 0.9, "临安降后文天祥继续抗元。"),
            _rel("event-yanya-haizhan", "follows", 0.7, "崖山亡宋（1279）后文天祥不就义于大都。"),
        ]),
    _ev("event-yanya-haizhan", "崖山海战、南宋灭亡", "war",
        1279, 1279, "year", "period-southern-song", "critical",
        "祥兴二年（1279 年）二月，宋元在崖山（今广东新会南海中）展开海战，"
        "宋军大败，陆秀夫负帝昺蹈海，南宋灭亡；"
        "元朝至此统一中国，中国历史上最后一次大规模海战歼亡的汉族王朝政权结束。",
        f"古代史料：《宋史·瀛国公纪》；《元史·世祖纪》；现代参考：{MODERN['yuan']}",
        W["songshi_yuan"],
        ["regime-yuan", "regime-southern-song"],
        relations=[
            _rel("event-linan-touxiang", "follows", 0.9, "临安降后南宋流亡朝廷的最后一战。"),
            _rel("event-wentianxiang-kangyuan", "follows", 0.6, "崖山覆亡后文天祥仍系大都狱中。"),
            _rel("event-song-meng-zhanzheng", "leads_to", 0.95, "宋蒙战争以南宋灭亡告终（aggregate 结束）。"),
        ],
        review_note="崖山殉国的具体人数与细节有不同记载；本事件按元灭宋、南宋政权终结的事实框架记录，"
                    "不渲染\"十万人殉国\"等未经严格考订的说法。"),
]


PHASES = {
    "SONG_FOUNDATION": PHASE_SONG_FOUNDATION,
    "SONG_LIAO_XIA": PHASE_SONG_LIAO_XIA,
    "REFORM_AND_JIN": PHASE_REFORM_AND_JIN,
    "JINGKANG_NANSONG": PHASE_JINGKANG_NANSONG,
    "SOUTHERN_SONG_LATE": PHASE_SOUTHERN_SONG_LATE,
}

ALL_PHASES = ["SONG_FOUNDATION", "SONG_LIAO_XIA", "REFORM_AND_JIN",
              "JINGKANG_NANSONG", "SOUTHERN_SONG_LATE"]

_FLA = [PHASE_SONG_FOUNDATION, PHASE_SONG_LIAO_XIA, PHASE_REFORM_AND_JIN,
        PHASE_JINGKANG_NANSONG, PHASE_SOUTHERN_SONG_LATE]
all_events = [ev for _phase in _FLA for ev in _phase]