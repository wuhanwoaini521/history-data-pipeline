# -*- coding: utf-8 -*-
"""China History Backbone V1 — Batch 6（元→元末→明）Data（part 2）：元末 + 明初 + 明中期。"""

from __future__ import annotations

from backbone_batch6_data import MODERN, W, _ev, _rel  # noqa: F401

# ---------------------------------------------------------------------------
# Phase 3 — 元末社会危机与群雄（1344—1368）
# ---------------------------------------------------------------------------
PHASE_YUAN_LATE = [
    _ev("event-huanghe-juekou", "黄河决口与连年水患", "disaster",
        1344, 1348, "range", "period-yuan", "major",
        "至正四年（1344 年）黄河在白茅堤、金堤等处决口，山东、河南一带水患连年，"
        "河道南徙、灾民流离，治河方略（堵口还是疏浚）成为朝野争议焦点，"
        "为元末全面社会危机的重要诱因。",
        f"古代史料：《元史·顺帝纪》河渠志；现代参考：{MODERN['yuan']}",
        W["yuanshi"],
        ["regime-yuan"],
        relations=[
            _rel("event-tuotuo-genghua", "follows", 0.6, "脱脱更化后期黄河问题凸显。"),
            _rel("event-jialu-zhihe", "leads_to", 0.9, "水患催生贾鲁治河工程。"),
            _rel("event-hongjin-jun-qiyi", "leads_to", 0.7, "治河征夫与灾民成为红巾起义的社会基础。"),
        ]),
    _ev("event-jialu-zhihe", "贾鲁治河", "economic",
        1351, 1351, "year", "period-yuan", "major",
        "至正十一年（1351 年）四月，工部尚书贾鲁主持黄河堵口治河，八月决口合龙；"
        "工程征调民夫数十万，加重民众负担，与同年红巾军起义（颍州）先后发生。",
        f"古代史料：《元史·顺帝纪》河渠志；现代参考：{MODERN['yuan']}",
        W["yuanshi"],
        ["regime-yuan"],
        relations=[
            _rel("event-huanghe-juekou", "follows", 0.9, "治河针对至正四年以来的决口灾情。"),
            _rel("event-hongjin-jun-qiyi", "follows", 0.6, "治河征夫与红巾起义同年。"),
        ]),
    _ev("event-yuan-zhizheng-chao", "至正钞改制与通货膨胀", "economic",
        1350, 1350, "year", "period-yuan", "major",
        "至正十年（1350 年）元廷变更钞法，铸造至正通宝铜钱并发行新纸钞（至正交钞），"
        "新钞一贯当旧钞两贯，引发恶性通货膨胀，纸币信用崩溃，财政危机与民间经济动荡加剧。",
        f"古代史料：《元史·顺帝纪》食货志；现代参考：{MODERN['yuan']}",
        W["yuanshi"],
        ["regime-yuan"],
        relations=[
            _rel("event-tuotuo-genghua", "follows", 0.7, "脱脱执政晚期的财政举措。"),
            _rel("event-hongjin-jun-qiyi", "leads_to", 0.6, "通货膨胀与民变同年展开。"),
        ]),
    _ev("event-hongjin-jun-qiyi", "红巾军起义（刘福通等起兵反元）", "rebellion",
        1351, 1351, "year", "period-yuan", "major",
        "至正十一年（1351 年），白莲教首领韩山童、刘福通等以\"明王出世、弥勒降生\"为号召"
        "在颍州（今安徽阜阳）起兵，以红巾为号，史称红巾军；"
        "同年徐寿辉（蕲黄）、郭子兴（濠州）等相继起兵，元末农民战争全面爆发。",
        f"古代史料：《元史·顺帝纪》；《明史·太祖纪》追述；现代参考：{MODERN['yuan_late']}",
        W["yuanshi_ming"],
        ["regime-yuan"],
        relations=[
            _rel("event-jialu-zhihe", "follows", 0.7, "治河与钞法危机背景下爆发。"),
            _rel("event-guo-zixing-qibing", "leads_to", 0.8, "郭子兴等响应起兵。"),
            _rel("event-han-liner-chengdi", "leads_to", 0.9, "刘福通拥立韩林儿（龙凤政权）。"),
        ]),
    _ev("event-guo-zixing-qibing", "郭子兴起兵濠州", "rebellion",
        1352, 1352, "year", "period-yuan", "major",
        "至正十二年（1352 年），郭子兴响应红巾在濠州（今安徽凤阳）起兵，"
        "占据濠州城，成为淮西反元武装之一，朱元璋即于是年投其麾下。",
        f"古代史料：《明史·太祖纪》；《国初事迹》相关记载；现代参考：{MODERN['yuan_late']}",
        W["mingshi"],
        [],
        relations=[
            _rel("event-hongjin-jun-qiyi", "follows", 0.8, "红巾起义后濠州响应。"),
            _rel("event-zhuyuanzhang-toujun", "leads_to", 0.9, "朱元璋投郭子兴部。"),
        ]),
    _ev("event-zhuyuanzhang-toujun", "朱元璋加入起义军（投郭子兴）", "political",
        1352, 1352, "year", "period-yuan", "major",
        "至正十二年（1352 年），朱元璋（原名朱重八，皇觉寺出身）投濠州郭子兴部为亲兵，"
        "以战功擢升，娶郭子兴养女马氏，此后数年内逐渐掌握濠州势力实权。",
        f"古代史料：《明史·太祖纪》；现代参考：{MODERN['yuan_late']}",
        W["mingshi"],
        ["regime-zhuzhang"],
        relations=[
            _rel("event-guo-zixing-qibing", "follows", 0.9, "投身郭子兴部。"),
            _rel("event-zhuyuanzhang-qu-jqing", "leads_to", 0.8, "数年后渡江取集庆建立根据地。"),
        ]),
    _ev("event-zhangshichen-ju-gaoyou", "张士诚据高邮、称诚王（大周）", "foundation",
        1353, 1353, "year", "period-yuan", "major",
        "至正十三年（1353 年），盐贩出身的张士诚率众在泰州-高邮一带起兵，"
        "据高邮称诚王，国号大周，控制两淮盐利，与朱元璋、陈友谅并列为元末三大势力。",
        f"古代史料：《明史·张士诚传》；现代参考：{MODERN['yuan_late']}",
        W["mingshi"],
        ["regime-dazhou"],
        relations=[
            _rel("event-hongjin-jun-qiyi", "follows", 0.7, "红巾起事后江淮各地起兵。"),
            _rel("event-zhuyuanzhang-mie-zhang", "precedes", 0.7, "1366 年被朱元璋攻灭。"),
        ]),
    _ev("event-han-liner-chengdi", "韩林儿称帝（小明王、龙凤政权）", "foundation",
        1355, 1355, "year", "period-yuan", "major",
        "至正十五年（1355 年），刘福通迎立韩山童之子韩林儿在亳州称帝，"
        "国号大宋，年号龙凤，史称小明王；各地红巾（包括朱元璋部）名义上奉其正朔，"
        "龙凤政权后期名存实亡（1366 年韩林儿卒）。",
        f"古代史料：《元史·顺帝纪》；《明史·太祖纪》；现代参考：{MODERN['yuan_late']}",
        W["yuanshi_ming"],
        ["regime-dasong"],
        relations=[
            _rel("event-hongjin-jun-qiyi", "follows", 0.9, "红巾军建立的政权性组织。"),
        ]),
    _ev("event-zhuyuanzhang-qu-jqing", "朱元璋渡江取集庆（应天府）", "war",
        1356, 1356, "year", "period-yuan", "major",
        "至正十六年（1356 年），朱元璋率部渡长江攻占集庆（今南京），"
        "改称应天府，以之为根据地向江南扩展，建立\"高筑墙、广积粮、缓称王\"战略下"
        "的稳固基地。",
        f"古代史料：《明史·太祖纪》；现代参考：{MODERN['yuan_late']}",
        W["mingshi"],
        ["regime-zhuzhang"],
        relations=[
            _rel("event-zhuyuanzhang-toujun", "follows", 0.8, "投军后数年发展。"),
            _rel("event-chenyouliang-dai-han", "precedes", 0.8, "江南争夺战随之展开。"),
        ]),
    _ev("event-chenyouliang-dai-han", "陈友谅代汉称帝", "foundation",
        1360, 1360, "year", "period-yuan", "major",
        "至正二十年（1360 年），陈友谅杀徐寿辉，在江州称帝，国号大汉，"
        "控制长江中游（江西、湖广大部），拥众最盛，与朱元璋争夺长江流域主导权。",
        f"古代史料：《明史·陈友谅传》；现代参考：{MODERN['yuan_late']}",
        W["mingshi"],
        ["regime-dahan"],
        relations=[
            _rel("event-zhuyuanzhang-qu-jqing", "follows", 0.7, "朱元璋据集庆后，双方争长江。"),
            _rel("event-poyanghu-zhizhan", "leads_to", 0.9, "三年后爆发鄱阳湖决战。"),
        ]),
    _ev("event-poyanghu-zhizhan", "鄱阳湖之战、陈友谅覆灭", "war",
        1363, 1363, "year", "period-yuan", "critical",
        "至正二十三年（1363 年）秋，朱元璋与陈友谅在鄱阳湖展开水军大会战，"
        "陈友谅中流矢死，汉军溃败，次年其子陈理降，长江中游尽归朱元璋；"
        "此战奠定朱元璋在南方群雄中的决定优势。",
        f"古代史料：《明史·太祖纪》《陈友谅传》；现代参考：{MODERN['yuan_late']}",
        W["mingshi"],
        ["regime-zhuzhang", "regime-dahan"],
        relations=[
            _rel("event-chenyouliang-dai-han", "follows", 0.9, "陈友谅倾国来攻，朱元璋决战。"),
            _rel("event-zhuyuanzhang-mie-zhang", "leads_to", 0.9, "灭陈后转向攻张士诚。"),
        ]),
    _ev("event-zhuyuanzhang-mie-zhang", "朱元璋灭张士诚", "war",
        1366, 1367, "range", "period-yuan", "major",
        "至正二十六年至二十七年（1366—1367 年），朱元璋命徐达、常遇春攻张士诚，"
        "围平江（苏州）十月，城破，张士诚被俘自缢，大周灭亡，两淮江浙尽入朱元璋之手。",
        f"古代史料：《明史·太祖纪》《张士诚传》；现代参考：{MODERN['yuan_late']}",
        W["mingshi"],
        ["regime-zhuzhang", "regime-dazhou"],
        relations=[
            _rel("event-poyanghu-zhizhan", "follows", 0.9, "鄱阳湖战后统一江南。"),
            _rel("event-fangguozhen-jiang", "leads_to", 0.7, "张士诚灭后浙东方国珍降。"),
        ]),
    _ev("event-fangguozhen-jiang", "方国珍降朱元璋", "political",
        1367, 1367, "year", "period-yuan", "major",
        "至正二十七年（1367 年），割据浙东沿海二十年的方国珍（未称帝，以行省平章名义据守）"
        "在朱元璋大军进逼下请降，南方群雄只剩福建陈友定、云南梁王等零星势力。",
        f"古代史料：《明史·方国珍传》；现代参考：{MODERN['yuan_late']}",
        W["mingshi"],
        ["regime-zhuzhang"],
        relations=[
            _rel("event-zhuyuanzhang-mie-zhang", "follows", 0.7, "张士诚灭后兵锋东指浙东。"),
        ]),
]


# ---------------------------------------------------------------------------
# Phase 4 — 明初（1368—1402）
# ---------------------------------------------------------------------------
PHASE_MING_EARLY = [
    _ev("event-zhuyuanzhang-chendi", "朱元璋称帝、明朝建立", "foundation",
        1368, 1368, "year", "period-ming", "critical",
        "洪武元年正月初四（1368 年 1 月 23 日），朱元璋在应天（南京）即皇帝位，"
        "国号大明，年号洪武，明朝建立；朱元璋由元末农民战争中的一方群雄"
        "转变为全国性政权的缔造者。",
        f"古代史料：《明史·太祖纪》；现代参考：{MODERN['ming']}",
        W["mingshi"],
        ["regime-ming"],
        relations=[
            _rel("event-zhuyuanzhang-mie-zhang", "follows", 0.9, "灭张士诚、平江南后称帝建明。"),
            _rel("event-xuda-beifa", "leads_to", 0.9, "建明后即命徐达北伐。"),
        ]),
    _ev("event-xuda-beifa", "徐达北伐、攻克大都（元退出中原）", "war",
        1368, 1368, "year", "period-ming", "major",
        "洪武元年（1368 年），明军徐达、常遇春等北伐，八月攻克元大都，"
        "元顺帝北走上都，元朝在中原的统治结束；蒙古汗廷北徙，"
        "史称\"北元\"（蒙古政治实体仍存续，明初多次北征即针对之）。",
        f"古代史料：《明史·太祖纪》；《元史·顺帝纪》；现代参考：{MODERN['ming']}",
        W["yuanshi_ming"],
        ["regime-ming", "regime-yuan"],
        relations=[
            _rel("event-zhuyuanzhang-chendi", "follows", 0.9, "建明当年攻克大都。"),
            _rel("event-ming-chu-beizheng", "leads_to", 0.8, "元廷北撤后明军持续北征。"),
        ],
        review_note="元在中原统治结束不等于蒙古政治实体消逝（北元）；本事件用中性表述记录政权更迭，"
                    "不渲染\"驱逐胡虏\"等叙事。"),
    _ev("event-ming-ping-yunnan", "明军平定云南", "war",
        1381, 1382, "range", "period-ming", "major",
        "洪武十四年至十五年（1381—1382 年），明军征讨元云南梁王把匝剌瓦尔密，"
        "克昆明，梁王死，云南并入明朝版图，设云南布政司，沐英留镇云南。",
        f"古代史料：《明史·太祖纪》；现代参考：{MODERN['ming']}",
        W["mingshi"],
        ["regime-ming"],
        relations=[
            _rel("event-zhuyuanzhang-chendi", "follows", 0.7, "统一战争推进至西南。"),
        ]),
    _ev("event-ming-wei-suo", "卫所制度建立", "reform",
        1368, 1382, "range", "period-ming", "major",
        "洪武年间，明廷确立卫所军制：一卫五千六百人，下设千户所、百户所，"
        "军籍世袭、屯田自给，洪武二十六年（1393 年）前后编定天下卫所规模；"
        "卫所制是明代军事与军户制度的基础。",
        f"古代史料：《明史·兵志》；现代参考：{MODERN['ming']}",
        W["mingshi"],
        ["regime-ming"],
        relations=[
            _rel("event-zhuyuanzhang-chendi", "follows", 0.7, "明初建国的军事制度安排。"),
        ]),
    _ev("event-ming-li-jia", "里甲制与赋役黄册编造", "reform",
        1381, 1381, "year", "period-ming", "major",
        "洪武十四年（1381 年），诏编赋役黄册并推行里甲制：以一百一十户为一里、"
        "推丁粮多者十户为里长，十年一轮服役；黄册作为全国户籍与赋役依据，"
        "构成明代基层治理的基本框架。",
        f"古代史料：《明史·食货志》；现代参考：{MODERN['ming']}",
        W["mingshi"],
        ["regime-ming"],
        relations=[
            _rel("event-zhuyuanzhang-chendi", "follows", 0.7, "明初户口赋役整顿。"),
        ]),
    _ev("event-hu-weiyong-an", "胡惟庸案、废中书省罢丞相", "political",
        1380, 1380, "year", "period-ming", "critical",
        "洪武十三年（1380 年），朱元璋以谋反罪族诛左丞相胡惟庸，"
        "随即罢中书省、废丞相制度，六部尚书直接对皇帝负责；"
        "此后内阁制逐步形成，皇权空前集中，是中国古代中枢制度的结构性变革。",
        f"古代史料：《明史·太祖纪》《胡惟庸传》；现代参考：{MODERN['ming']}",
        W["mingshi"],
        ["regime-ming"],
        relations=[
            _rel("event-zhuyuanzhang-chendi", "follows", 0.8, "建国后十余年废除丞相。"),
            _rel("event-lanyu-an", "precedes", 0.8, "十三年后的又一次大规模清洗（蓝玉案）。"),
        ]),
    _ev("event-lanyu-an", "蓝玉案（功臣清洗）", "political",
        1393, 1393, "year", "period-ming", "major",
        "洪武二十六年（1393 年），朱元璋以谋逆罪诛凉国公蓝玉，"
        "连坐诛杀功臣宿将，与胡惟庸案同为洪武朝两次大规模功臣清洗；"
        "开国勋贵集团自此凋零。",
        f"古代史料：《明史·太祖纪》《蓝玉传》；现代参考：{MODERN['ming']}",
        W["mingshi"],
        ["regime-ming"],
        relations=[
            _rel("event-hu-weiyong-an", "follows", 0.8, "继胡惟庸案后的又一次大清洗。"),
        ]),
    _ev("event-ming-chu-beizheng", "明初北征蒙古（捕鱼儿海之战）", "war",
        1387, 1388, "range", "period-ming", "major",
        "洪武二十至二十一年（1387—1388 年），明军经略辽东并北征北元，"
        "蓝玉率军在捕鱼儿海（今贝尔湖）大破北元脱古思帖木儿汗廷，"
        "北元汗廷东走，明初北征取得决定战果。",
        f"古代史料：《明史·太祖纪》；现代参考：{MODERN['ming']}",
        W["mingshi"],
        ["regime-ming", "regime-yuan"],
        relations=[
            _rel("event-xuda-beifa", "follows", 0.9, "克大都后对北元持续用兵。"),
        ]),
    _ev("event-ming-feng-zhuzhuwang", "明初分封诸王", "political",
        1370, 1391, "range", "period-ming", "major",
        "洪武三年起（1370 年），朱元璋陆续分封诸子为王（秦王、晋王、燕王、宁王等），"
        "以亲王守边领藩；藩王拥兵与中央集权的矛盾成为建文朝削藩、靖难之役的直接背景。",
        f"古代史料：《明史·诸王传》；现代参考：{MODERN['ming']}",
        W["mingshi"],
        ["regime-ming"],
        relations=[
            _rel("event-jianwen-jiwei", "precedes", 0.8, "藩王问题在建文帝削藩时爆发。"),
        ]),
    _ev("event-jianwen-jiwei", "建文帝即位", "succession",
        1398, 1398, "year", "period-ming", "major",
        "洪武三十一年（1398 年）闰五月，朱元璋卒，皇太孙朱允炆即位，是为建文帝，"
        "次年改元建文；建文帝尊儒重文，急于削藩以巩固皇权。",
        f"古代史料：《明史·恭闵帝纪》；现代参考：{MODERN['ming']}",
        W["mingshi"],
        ["regime-ming"],
        relations=[
            _rel("event-lanyu-an", "follows", 0.6, "洪武末年功臣集团消退后皇太孙即位。"),
            _rel("event-jianwen-xuefan", "leads_to", 0.9, "即位后随即削藩。"),
        ]),
    _ev("event-jianwen-xuefan", "建文帝削藩", "political",
        1399, 1399, "year", "period-ming", "major",
        "建文元年（1399 年），建文帝用齐泰、黄子澄、方孝孺等议，"
        "先后废削周、齐、湘、代、岷诸王，矛头指向坐镇北平、拥兵十万的燕王朱棣，"
        "直接触发靖难之役。",
        f"古代史料：《明史·恭闵帝纪》；现代参考：{MODERN['ming']}",
        W["mingshi"],
        ["regime-ming"],
        relations=[
            _rel("event-jianwen-jiwei", "follows", 0.9, "即位当年即行削藩。"),
            _rel("event-jingnan-zhizhan", "leads_to", 0.95, "削藩逼反燕王。"),
        ]),
    _ev("event-jingnan-zhizhan", "靖难之役", "war",
        1399, 1402, "range", "period-ming", "critical",
        "建文元年至四年（1399—1402 年），燕王朱棣以\"清君侧、靖难\"为名起兵，"
        "历三年余南下攻入南京，建文帝下落不明，朱棣即位（明成祖）。"
        "本事件为 aggregate，子事件（靖难起兵、燕军入南京）经 part_of 关联。",
        f"古代史料：《明史·成祖纪》《恭闵帝纪》；现代参考：{MODERN['ming']}",
        W["mingshi"],
        ["regime-ming"],
        relations=[
            _rel("event-jianwen-xuefan", "follows", 0.95, "削藩引发靖难。"),
        ]),
    _ev("event-jingnan-qibing", "靖难起兵（燕王举兵北平）", "war",
        1399, 1399, "year", "period-ming", "major",
        "建文元年（1399 年），朱棣在北平誓师起兵，先诛北平都指挥使司张昺、谢贵，"
        "靖难战争开始；此后燕军与建文军在山东、河北拉锯三年。",
        f"古代史料：《明史·成祖纪》；现代参考：{MODERN['ming']}",
        W["mingshi"],
        ["regime-ming"],
        relations=[
            _rel("event-jingnan-zhizhan", "part_of", 0.95, "靖难之役的起始。"),
        ]),
    _ev("event-yanjun-ru-jing", "燕军攻入南京、永乐帝即位", "political",
        1402, 1402, "year", "period-ming", "major",
        "建文四年（1402 年）六月，燕军渡江攻入南京，宫中火灾，建文帝下落不明"
        "（焚死或出亡，诸说并存），朱棣即皇帝位，是为明成祖，次年改元永乐。",
        f"古代史料：《明史·成祖纪》；现代参考：{MODERN['ming']}",
        W["mingshi"],
        ["regime-ming"],
        relations=[
            _rel("event-jingnan-zhizhan", "part_of", 0.9, "靖难之役的结局。"),
            _rel("event-jingnan-qibing", "follows", 0.9, "起兵三年后攻克南京。"),
        ],
        review_note="建文帝结局（焚死/出亡）为明清史学公案，本事件两说并录，不下定论。"),
]