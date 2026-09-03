# -*- coding: utf-8 -*-
"""China History Backbone V1 — Batch 6（元→元末→明）Data（part 3）：明中期 + 晚明 + 聚合导出。"""

from __future__ import annotations

from backbone_batch6_data import MODERN, W, _ev, _rel, PHASE_YUAN_EARLY, PHASE_YUAN_MIDDLE  # noqa: F401
from backbone_batch6_tail_data import PHASE_YUAN_LATE, PHASE_MING_EARLY  # noqa: F401

# ---------------------------------------------------------------------------
# Phase 5 — 明中期（永乐—嘉靖，1402—1565）
# ---------------------------------------------------------------------------
PHASE_MING_MIDDLE = [
    _ev("event-zhenghe-xiaxiyang", "郑和下西洋", "cultural",
        1405, 1433, "range", "period-ming", "major",
        "永乐三年至宣德八年（1405—1433 年），明廷先后七次派遣郑和率庞大船队远航，"
        "历东南亚、印度洋至东非，开展朝贡贸易与外交（\"厚往薄来\"），"
        "为世界航海史上规模空前的远洋活动，宣德后停止。"
        "本事件为 aggregate，子事件（第一次下西洋、最后一次下西洋与停止远航）经 part_of 关联。",
        f"古代史料：《明史·郑和传》；《明实录》永乐至宣德诸纪；现代参考：{MODERN['ming']}",
        W["mingshi_lu"],
        ["regime-ming"],
        relations=[
            _rel("event-yanjun-ru-jing", "follows", 0.8, "永乐帝即位后启动远航。"),
        ]),
    _ev("event-zhenghe-di-yici", "郑和第一次下西洋", "cultural",
        1405, 1407, "range", "period-ming", "major",
        "永乐三年（1405 年）郑和率兵卒二万七千余人、宝船数十艘自江苏太仓刘家港出海，"
        "历爪哇、苏门答腊、古里等，永乐五年（1407 年）返京，首航确立航路格局。",
        f"古代史料：《明实录·太宗实录》；现代参考：{MODERN['ming']}",
        W["mingshilu"],
        ["regime-ming"],
        relations=[
            _rel("event-zhenghe-xiaxiyang", "part_of", 0.95, "七下西洋之首航。"),
        ]),
    _ev("event-zhenghe-zui-hou", "郑和最后一次下西洋与停止远航", "cultural",
        1430, 1433, "range", "period-ming", "major",
        "宣德五年至八年（1430—1433 年）郑和第七次（最后一次）下西洋，"
        "郑和卒于途中（1433 年，古里）；此后明朝不再组织大规模远洋航行，"
        "远洋航海长期中止。",
        f"古代史料：《明实录·宣宗实录》；现代参考：{MODERN['ming']}",
        W["mingshilu"],
        ["regime-ming"],
        relations=[
            _rel("event-zhenghe-xiaxiyang", "part_of", 0.95, "七下西洋之末次。"),
        ]),
    _ev("event-ming-zheng-annan", "明征安南、设交趾布政司", "war",
        1406, 1407, "range", "period-ming", "major",
        "永乐四年至五年（1406—1407 年），明成祖以安南胡朝篡位为由发兵讨伐，"
        "灭胡朝，设交趾布政司直接统治安南（越南北部），"
        "永乐朝在东南亚的领土扩张达到顶点。",
        f"古代史料：《明史·安南传》（外国传）；现代参考：{MODERN['ming']}",
        W["mingshi"],
        ["regime-ming"],
        relations=[
            _rel("event-yanjun-ru-jing", "follows", 0.7, "永乐初年的对外用兵。"),
            _rel("event-ming-qi-jiaozhi", "leads_to", 0.8, "二十年后放弃交趾。"),
        ]),
    _ev("event-ming-qi-jiaozhi", "明弃交趾（撤军还安南）", "political",
        1427, 1427, "year", "period-ming", "major",
        "宣德二年（1427 年），明廷因交趾叛乱不断、驻军负担沉重，"
        "撤出交趾，交趾布政司罢废，安南恢复独立政权（黎氏后黎朝）。",
        f"古代史料：《明史·安南传》（外国传）；现代参考：{MODERN['ming']}",
        W["mingshi"],
        ["regime-ming"],
        relations=[
            _rel("event-ming-zheng-annan", "follows", 0.8, "设治二十年后的战略收缩。"),
        ]),
    _ev("event-yongle-beizheng", "明成祖五征漠北", "war",
        1410, 1424, "range", "period-ming", "major",
        "永乐八年至二十二年（1410—1424 年），明成祖先后五次亲征漠北蒙古"
        "（本雅失里、阿鲁台、马哈木等部），各有胜负，"
        "第五次班师途中于榆木川病逝；北元—蒙古诸部受创但未被根本解决。",
        f"古代史料：《明史·成祖纪》《鞑靼传》（外国传）；现代参考：{MODERN['ming']}",
        W["mingshi"],
        ["regime-ming"],
        relations=[
            _rel("event-ming-chu-beizheng", "follows", 0.8, "继洪武北征后的对蒙用兵。"),
            _rel("event-yanjun-ru-jing", "follows", 0.7, "永乐朝亲征蒙古。"),
        ]),
    _ev("event-qian-du-beijing", "迁都北京", "political",
        1421, 1421, "year", "period-ming", "critical",
        "永乐十九年（1421 年），明成祖正式迁都北京（永乐元年升北平为北京、"
        "四年起营建宫殿城池），南京为留都；北京自此成为明清两代都城，"
        "影响国家政治版图数百年。",
        f"古代史料：《明史·成祖纪》《地理志》；现代参考：{MODERN['ming']}",
        W["mingshi"],
        ["regime-ming"],
        relations=[
            _rel("event-yanjun-ru-jing", "follows", 0.8, "朱棣以北平起家，定都北京。"),
            _rel("event-tumu-bao-zhibian", "precedes", 0.7, "北京为都后二十余年发生土木堡之变。"),
        ]),
    _ev("event-tumu-bao-zhibian", "土木堡之变", "war",
        1449, 1449, "year", "period-ming", "critical",
        "正统十四年（1449 年），瓦剌（蒙古西部）也先率军南犯，"
        "明英宗在宦官王振鼓动下亲征，八月于土木堡（今河北怀来东）被瓦剌军围歼，"
        "英宗被俘，明军精锐损失惨重，明朝由盛转衰的标志性事件。",
        f"古代史料：《明史·英宗纪》；现代参考：{MODERN['ming']}",
        W["mingshi_lu"],
        ["regime-ming"],
        relations=[
            _rel("event-qian-du-beijing", "follows", 0.7, "迁都北京后蒙古瓦剌南侵。"),
            _rel("event-jingtai-jiwei", "leads_to", 0.9, "英宗被俘后郕王即位（景泰）。"),
            _rel("event-beijing-baoweizhan", "leads_to", 0.9, "瓦剌随即兵临北京。"),
        ]),
    _ev("event-jingtai-jiwei", "景泰帝即位（英宗北狩）", "succession",
        1449, 1449, "year", "period-ming", "major",
        "正统十四年（1449 年）九月，兵部侍郎于谦等拥立监国郕王朱祁钰即皇帝位"
        "（景泰帝），尊被俘英宗为太上皇，稳定朝局以应瓦剌之兵。",
        f"古代史料：《明史·英宗纪》《景帝纪》；现代参考：{MODERN['ming']}",
        W["mingshi"],
        ["regime-ming"],
        relations=[
            _rel("event-tumu-bao-zhibian", "follows", 0.95, "英宗被俘后另立新君。"),
            _rel("event-beijing-baoweizhan", "leads_to", 0.8, "新君即位后组织北京防御。"),
        ]),
    _ev("event-beijing-baoweizhan", "北京保卫战", "war",
        1449, 1449, "year", "period-ming", "major",
        "正统十四年（1449 年）十月，瓦剌也先挟英宗至北京城下，"
        "于谦组织京师军民闭城坚守，发炮击退瓦剌军，也先退兵，北京解围，"
        "明朝转危为安。",
        f"古代史料：《明史·于谦传》《英宗纪》；现代参考：{MODERN['ming']}",
        W["mingshi"],
        ["regime-ming"],
        relations=[
            _rel("event-jingtai-jiwei", "follows", 0.9, "景泰朝组织京师防御。"),
            _rel("event-duomen-zhibian", "precedes", 0.8, "北京保卫战八年后的夺门之变。"),
        ]),
    _ev("event-duomen-zhibian", "夺门之变、英宗复位", "political",
        1457, 1457, "year", "period-ming", "major",
        "景泰八年（1457 年）正月，景泰帝病重，石亨、徐有贞、曹吉祥等发动政变，"
        "迎英宗自南宫复位（南宫复辟），改元天顺；景泰帝旋卒，"
        "于谦以\"谋逆\"罪名被杀（后获平反），政局随之反复。",
        f"古代史料：《明史·英宗纪》《于谦传》；现代参考：{MODERN['ming']}",
        W["mingshi"],
        ["regime-ming"],
        relations=[
            _rel("event-beijing-baoweizhan", "follows", 0.8, "北京保卫战之后英宗复位。"),
        ]),
    _ev("event-daliyi", "大礼议（嘉靖即位与礼制之争）", "political",
        1521, 1524, "range", "period-ming", "major",
        "正德十六年（1521 年），明世宗朱厚熜以兴献王世子入继大统，"
        "围绕生父尊号（皇考还是皇叔考）与廷臣展开\"大礼之议\"，"
        "历数年反复，议礼派在嘉靖三年（1524 年）胜出，世宗追尊兴献帝为皇考，"
        "朝局重新洗牌。",
        f"古代史料：《明史·世宗纪》；现代参考：{MODERN['ming']}",
        W["mingshi"],
        ["regime-ming"],
        relations=[
            _rel("event-duomen-zhibian", "follows", 0.5, "大礼议为嘉靖朝初年政治核心议题。"),
        ]),
    _ev("event-ningwang-zhi-luan", "宁王之乱（朱宸濠起兵）", "rebellion",
        1519, 1519, "year", "period-ming", "major",
        "正德十四年（1519 年），宁王朱宸濠在南昌起兵叛乱，"
        "王守仁（王阳明）不待朝命募集乡兵讨平，前后四十三天。",
        f"古代史料：《明史·王守仁传》《宁王传》（诸王传）；现代参考：{MODERN['ming']}",
        W["mingshi"],
        ["regime-ming"],
        relations=[
            _rel("event-daliyi", "precedes", 0.4, "正德朝藩王问题与武宗无嗣背景相关。"),
        ]),
    _ev("event-dongnan-wokou", "东南沿海倭患", "war",
        1552, 1565, "range", "period-ming", "major",
        "嘉靖三十一年至四十四年（1552—1565 年），东南沿海倭患（与中国沿海海商集团、"
        "走私及日本武士有关）严重，明廷整顿海防，胡宗宪、戚继光、俞大猷等抗倭，"
        "嘉靖末年基本平定。本事件为 aggregate，子事件（诱诛王直、台州大捷）经 part_of 关联。",
        f"古代史料：《明史·世宗纪》日本传；现代参考：{MODERN['ming']}",
        W["mingshi"],
        ["regime-ming"],
        relations=[
            _rel("event-ningwang-zhi-luan", "follows", 0.5, "正德嘉靖间的海防与内部动乱交织。"),
        ]),
    _ev("event-wangzhi-yousha", "胡宗宪诱诛王直", "political",
        1557, 1558, "range", "period-ming", "major",
        "嘉靖三十六至三十七年（1557—1558 年），浙直总督胡宗宪设计诱捕"
        "盘踞五岛的徽州海商集团首领王直，次年正月斩于杭州，抗倭形势由此转折。",
        f"古代史料：《明史·胡宗宪传》日本传；现代参考：{MODERN['ming']}",
        W["mingshi"],
        ["regime-ming"],
        relations=[
            _rel("event-dongnan-wokou", "part_of", 0.9, "倭患治理的关键节点。"),
        ]),
    _ev("event-taizhou-dajie", "戚继光台州大捷", "war",
        1561, 1561, "year", "period-ming", "major",
        "嘉靖四十年（1561 年），戚继光率义乌募练的新军在台州连战连捷（九战九捷），"
        "基本肃清浙东倭患，新军（戚家军）战法成为明后期练兵样板。",
        f"古代史料：《明史·戚继光传》；现代参考：{MODERN['ming']}",
        W["mingshi"],
        ["regime-ming"],
        relations=[
            _rel("event-dongnan-wokou", "part_of", 0.9, "倭患平定中的决定性战役。"),
        ]),
    _ev("event-zhengde-zhengzhi", "正德朝政治起伏（豹房与刘瑾）", "political",
        1505, 1521, "range", "period-ming", "major",
        "正德一朝（1505—1521 年），明武宗朱厚照在位十六年，宠信宦官刘瑾（正德五年倒台）、"
        "自称\"威武大将军\"多次巡边，朝政废弛，边患与藩王问题（宁王乱）随之而来，"
        "为嘉靖朝整顿的政治背景。",
        f"古代史料：《明史·武宗纪》；现代参考：{MODERN['ming']}",
        W["mingshi"],
        ["regime-ming"],
        relations=[
            _rel("event-ningwang-zhi-luan", "precedes", 0.6, "正德朝政失序下宁王起兵。"),
            _rel("event-daliyi", "leads_to", 0.6, "武宗无嗣，世宗以小宗入继引发大礼议。"),
        ],
        review_note="正德朝不称\"治\"亦不称\"乱世\"；本事件记录武宗朝政治运行的基本事实，"
                    "不作道德评价。"),
]


# ---------------------------------------------------------------------------
# Phase 6 — 晚明（隆万—崇祯，1572—1644）
# ---------------------------------------------------------------------------
PHASE_MING_LATE = [
    _ev("event-zhangjuzheng-gaige", "张居正改革", "reform",
        1572, 1582, "range", "period-ming", "major",
        "隆庆六年至万历十年（1572—1582 年），内阁首辅张居正主持改革："
        "考成法整顿吏治、清丈田亩、推广一条鞭法、整顿边防与河工，"
        "财政与行政效率明显改善；张居正死后遭清算，改革多被废罢或存废反复。"
        "本事件为 aggregate，子事件（考成法、一条鞭法推广、改革受挫）经 part_of 关联。",
        f"古代史料：《明史·张居正传》《神宗纪》；现代参考：{MODERN['ming_late']}",
        W["mingshi"],
        ["regime-ming"],
        relations=[
            _rel("event-taizhou-dajie", "follows", 0.5, "嘉靖末抗倭后至万历初张居正执政。"),
            _rel("event-wanli-chaoxian", "leads_to", 0.6, "张居正死后万历朝进入抗战与怠政时期。"),
        ]),
    _ev("event-kaocheng-fa", "考成法（张居正整顿吏治）", "reform",
        1573, 1573, "year", "period-ming", "major",
        "万历元年（1573 年），张居正推行考成法：公文办理以六科稽查六部、"
        "内阁稽查六科，限期考核、厘清责任，嘉靖以来低效的官僚行政明显改观。",
        f"古代史料：《明史·张居正传》；现代参考：{MODERN['ming_late']}",
        W["mingshi"],
        ["regime-ming"],
        relations=[
            _rel("event-zhangjuzheng-gaige", "part_of", 0.95, "改革总纲的第一步。"),
        ]),
    _ev("event-yitiao-bianfa", "一条鞭法推广（赋役折银）", "reform",
        1581, 1581, "year", "period-ming", "major",
        "万历九年（1581 年），张居正将嘉靖以来各地试行的一条鞭法推向全国："
        "赋役合并、计亩征银、由官府统一征收，简化税制，"
        "为明清赋役制度划时代的变革。",
        f"古代史料：《明史·食货志》《张居正传》；现代参考：{MODERN['ming_late']}",
        W["mingshi"],
        ["regime-ming"],
        relations=[
            _rel("event-zhangjuzheng-gaige", "part_of", 0.95, "改革中最具制度意义的一环。"),
        ]),
    _ev("event-zhangjuzheng-shoucuo", "张居正病逝与改革受挫", "political",
        1582, 1584, "range", "period-ming", "major",
        "万历十年（1582 年）张居正病逝，旋即遭御史弹劾，家产被抄没，"
        "考成法、清丈等举措多被废罢，万历帝转入长期怠政；"
        "张居正改革以人亡政息告终。",
        f"古代史料：《明史·张居正传》《神宗纪》；现代参考：{MODERN['ming_late']}",
        W["mingshi"],
        ["regime-ming"],
        relations=[
            _rel("event-zhangjuzheng-gaige", "part_of", 0.95, "改革终结。"),
            _rel("event-wanli-chaoxian", "leads_to", 0.7, "张居正死后十年万历朝开始援朝战争。"),
        ]),
    _ev("event-wanli-chaoxian", "万历朝鲜战争（援朝抗倭）", "war",
        1592, 1598, "range", "period-ming", "major",
        "万历二十年至二十六年（1592—1598 年），日本丰臣秀吉两次侵朝，"
        "明军两次入朝救援，最后于万历二十六年（1598 年）与朝鲜军联合击退日军。"
        "本事件为 aggregate，子事件（壬辰之役、丁酉再乱）经 part_of 关联；"
        "本库核心为中国史视角，明介入与援朝为主线。",
        f"古代史料：《明史·神宗纪》朝鲜传（外国传）；现代参考：{MODERN['ming_late']}",
        W["mingshi"],
        ["regime-ming"],
        relations=[
            _rel("event-kaocheng-fa", "follows", 0.5, "张居正整顿后的国力用于援朝战争。"),
        ]),
    _ev("event-renchen-yizhan", "壬辰之役（第一次援朝、平壤大捷）", "war",
        1592, 1593, "range", "period-ming", "major",
        "万历二十年（1592 年），日军主力渡海攻朝鲜，朝鲜军溃败，明军入朝救援，"
        "次年（1593 年）李如松部在平壤击败日军，收复平壤；此后议和搁置战争（和谈期）。",
        f"古代史料：《明史·神宗纪》朝鲜传；现代参考：{MODERN['ming_late']}",
        W["mingshi"],
        ["regime-ming"],
        relations=[
            _rel("event-wanli-chaoxian", "part_of", 0.95, "第一次援朝战争。"),
        ]),
    _ev("event-dingyou-zailuan", "丁酉再乱（第二次战争与结束）", "war",
        1597, 1598, "range", "period-ming", "major",
        "万历二十五年至二十六年（1597—1598 年），和谈破裂后日军再侵，明军再援；"
        "万历二十六年丰臣秀吉死，日军撤，明鲜联军海军（李舜臣、陈璘）"
        "在露梁海战重创撤退日军，战争结束。",
        f"古代史料：《明史·神宗纪》朝鲜传；现代参考：{MODERN['ming_late']}",
        W["mingshi"],
        ["regime-ming"],
        relations=[
            _rel("event-wanli-chaoxian", "part_of", 0.95, "第二次援朝战争。"),
        ]),
    _ev("event-donglin-dangzheng", "东林党争", "political",
        1604, 1627, "range", "period-ming", "major",
        "万历三十二年至天启末（1604—1627 年），顾宪成等以东林书院议政，"
        "与齐楚浙诸党及宦官集团反复争斗，党争贯穿万历、泰昌、天启三朝，"
        "加深明末政治内耗。",
        f"古代史料：《明史·顾宪成传》等列传；现代参考：{MODERN['ming_late']}",
        W["mingshi"],
        ["regime-ming"],
        relations=[
            _rel("event-zhangjuzheng-shoucuo", "follows", 0.6, "张居正死后党派纷争渐起。"),
            _rel("event-weizhongxian-zhuanquan", "leads_to", 0.8, "天启朝宦官魏忠贤与东林争斗。"),
        ]),
    _ev("event-weizhongxian-zhuanquan", "魏忠贤专权（天启朝政治）", "political",
        1624, 1627, "range", "period-ming", "major",
        "天启四年至七年（1624—1627 年），宦官魏忠贤受天启帝宠信专权，"
        "号\"九千岁\"，打击东林党人，阉党遍布台谏，加上辽东战事与民变并起，"
        "明末政治危机全面显化。",
        f"古代史料：《明史·魏忠贤传》《熹宗纪》；现代参考：{MODERN['ming_late']}",
        W["mingshi"],
        ["regime-ming"],
        relations=[
            _rel("event-donglin-dangzheng", "follows", 0.8, "党争推向阉党专权。"),
            _rel("event-chongzhen-jiwei", "leads_to", 0.9, "天启帝死，崇祯即位清除魏忠贤。"),
        ]),
    _ev("event-chongzhen-jiwei", "崇祯帝即位、清除魏忠贤集团", "political",
        1627, 1628, "range", "period-ming", "major",
        "天启七年（1627 年），崇祯帝朱由检即位，随即贬逐魏忠贤并赐死，"
        "清算阉党（崇祯元年二月钦定逆案）；但明末党争、财政、边患与民变四重危机"
        "并未因此缓解。",
        f"古代史料：《明史·庄烈帝纪》《魏忠贤传》；现代参考：{MODERN['ming_late']}",
        W["mingshi"],
        ["regime-ming"],
        relations=[
            _rel("event-weizhongxian-zhuanquan", "follows", 0.9, "即位后肃清阉党。"),
            _rel("event-shanxi-minbian", "leads_to", 0.7, "同一时期陕西民变扩大。"),
        ]),
    _ev("event-shanxi-minbian", "陕西民变扩大（明末农民战争开端）", "rebellion",
        1627, 1631, "range", "period-ming", "major",
        "天启七年至崇祯四年（1627—1631 年），陕西连年旱灾、驿卒与边兵欠饷，"
        "王二、高迎祥、李自成等相继聚众起义，民变蔓延陕甘，"
        "明朝将全力剿抚，农民战争进入长期化。",
        f"古代史料：《明史·庄烈帝纪》；现代参考：{MODERN['ming_late']}",
        W["mingshi"],
        ["regime-ming"],
        relations=[
            _rel("event-chongzhen-jiwei", "follows", 0.7, "崇祯初年陕西民变即已扩大。"),
            _rel("event-li-zicheng-fazhan", "leads_to", 0.8, "李自成等势力在民变中崛起。"),
        ]),
    _ev("event-nuerhachi-tongyi-nvzhen", "努尔哈赤统一女真诸部", "political",
        1583, 1616, "range", "period-ming", "major",
        "万历十一年至四十四年（1583—1616 年），建州女真首领努尔哈赤以父祖被误杀"
        "为起兵之由，逐步统一建州、海西、野人女真诸部，创制八旗制度与满文，"
        "1616 年在赫图阿拉建立政权（后金）。",
        f"古代史料：《清太祖武皇帝实录》（崇德本）；《明史·神宗纪》相关；现代参考：{MODERN['houjin']}",
        W["mingshi"],
        [],
        relations=[
            _rel("event-houjin-jianguo", "leads_to", 0.95, "统一女真后建国。"),
        ]),
    _ev("event-houjin-jianguo", "后金建立（努尔哈赤称汗）", "foundation",
        1616, 1616, "year", "period-ming", "major",
        "天命元年（1616 年）正月，努尔哈赤在赫图阿拉（今辽宁新宾）称汗建国，"
        "国号大金（史称后金），建元天命；后金是清朝的前身政权，"
        "与明朝并存，1618 年以\"七大恨\"对明宣战。",
        f"古代史料：《清太祖武皇帝实录》；现代参考：{MODERN['houjin']}",
        W["mingshi"],
        ["regime-houjin"],
        relations=[
            _rel("event-nuerhachi-tongyi-nvzhen", "follows", 0.95, "统一女真后建国。"),
            _rel("event-qidahen", "leads_to", 0.9, "两年后发布七大恨并攻明。"),
        ]),
    _ev("event-qidahen", "七大恨（后金对明宣战）", "political",
        1618, 1618, "year", "period-ming", "major",
        "天命三年（1618 年）四月，努尔哈赤以\"七大恨\"告天，历数明廷杀父祖、"
        "偏袒叶赫等七事，随即攻占抚顺，对明战争公开化，辽东局势骤变。",
        f"古代史料：《清太祖武皇帝实录》；现代参考：{MODERN['houjin']}",
        W["mingshi"],
        ["regime-houjin"],
        relations=[
            _rel("event-houjin-jianguo", "follows", 0.9, "建金后对明宣战。"),
            _rel("event-saerhu-zhizhan", "leads_to", 0.9, "次年明军四路征讨，萨尔浒决战。"),
        ]),
    _ev("event-saerhu-zhizhan", "萨尔浒之战", "war",
        1619, 1619, "year", "period-ming", "critical",
        "天命四年（1619 年），明辽东经略杨镐督四路大军征伐后金，"
        "努尔哈赤采取\"凭尔几路来，我只一路去\"之策，在萨尔浒（今辽宁抚顺东）"
        "先后各个击破明军，明军主力受创，辽东攻守之势倒转，"
        "明朝自此转入辽事防御。",
        f"古代史料：《明史·杨镐传》；《清太祖武皇帝实录》；现代参考：{MODERN['houjin']}",
        W["mingshi"],
        ["regime-ming", "regime-houjin"],
        relations=[
            _rel("event-qidahen", "follows", 0.9, "宣战后明军四路来攻被各个击破。"),
            _rel("event-liaoshen-shixian", "leads_to", 0.9, "萨尔浒后后金转守为攻，占领辽沈。"),
        ]),
    _ev("event-liaoshen-shixian", "辽沈失守（辽东格局变化）", "war",
        1621, 1621, "year", "period-ming", "major",
        "天启元年（1621 年），后金军攻占沈阳、辽阳，辽河以东尽失，"
        "后金迁都辽阳（天启五年再迁沈阳，改名盛京）；明朝经略辽东的防线崩溃，"
        "辽西走廊成为此后对峙前线。",
        f"古代史料：《明史·熹宗纪》；《清太祖武皇帝实录》；现代参考：{MODERN['houjin']}",
        W["mingshi"],
        ["regime-houjin", "regime-ming"],
        relations=[
            _rel("event-saerhu-zhizhan", "follows", 0.9, "萨尔浒后的战略转折。"),
        ]),
    _ev("event-li-zicheng-fazhan", "李自成势力发展", "political",
        1633, 1643, "range", "period-ming", "major",
        "崇祯六年至十六年（1633—1643 年），农民军反复聚散，"
        "李自成转战陕豫湖广，崇祯十六年（1643 年）据襄阳称新顺王，"
        "次年（1644 年）正月在西安称帝建大顺。",
        f"古代史料：《明史·庄烈帝纪》《流贼传》；现代参考：{MODERN['ming_late']}",
        W["mingshi"],
        ["regime-ming"],
        relations=[
            _rel("event-shanxi-minbian", "follows", 0.8, "陕西民变中李自成势力逐步壮大。"),
            _rel("event-li-zicheng-jian-dashun", "leads_to", 0.9, "称帝建大顺。"),
        ]),
    _ev("event-zhang-xianzhong-fazhan", "张献忠势力发展", "political",
        1633, 1644, "range", "period-ming", "major",
        "崇祯六年至十七年（1633—1644 年），张献忠转战楚蜀，"
        "崇祯十六年（1643 年）攻克武昌称大西王，次年（1644 年）在成都称帝建大西；"
        "与李自成大顺并行的两支明末农民军势力。",
        f"古代史料：《明史·流贼传》；现代参考：{MODERN['ming_late']}",
        W["mingshi"],
        ["regime-ming"],
        relations=[
            _rel("event-shanxi-minbian", "follows", 0.8, "与李自成并起的另一支主力。"),
        ]),
    _ev("event-li-zicheng-jian-dashun", "李自成称帝、建立大顺", "foundation",
        1644, 1644, "year", "period-ming", "major",
        "崇祯十七年（1644 年）正月，李自成在西安称帝，国号大顺，建元永昌，"
        "随后率大军东征，直指北京。",
        f"古代史料：《明史·流贼传》；现代参考：{MODERN['ming_late']}",
        W["mingshi"],
        ["regime-ming"],
        relations=[
            _rel("event-li-zicheng-fazhan", "follows", 0.9, "势力发展的顶点。"),
            _rel("event-lizicheng-gong-beijing", "leads_to", 0.95, "称帝后东征北京。"),
        ]),
    _ev("event-lizicheng-gong-beijing", "李自成攻入北京、明朝灭亡", "dynastic-transition",
        1644, 1644, "year", "period-ming", "critical",
        "崇祯十七年（1644 年）三月十九日，大顺军攻入北京，"
        "崇祯帝在煤山自缢，明朝中央政权覆亡；"
        "此后明朝宗室在南方建立南明诸政权（另有专记），清朝于同年入关。",
        f"古代史料：《明史·庄烈帝纪》；现代参考：{MODERN['ming_late']}",
        W["mingshi"],
        ["regime-ming"],
        relations=[
            _rel("event-li-zicheng-jian-dashun", "follows", 0.95, "大顺军攻灭明中央政权。"),
        ],
        review_note="本事件为本批终点（§29）；南明诸政权（弘光/隆武/永历）与清军入关等在 Batch7 展开。"),
]


PHASES = {
    "YUAN_EARLY": PHASE_YUAN_EARLY,
    "YUAN_MIDDLE": PHASE_YUAN_MIDDLE,
    "YUAN_LATE": PHASE_YUAN_LATE,
    "MING_EARLY": PHASE_MING_EARLY,
    "MING_MIDDLE": PHASE_MING_MIDDLE,
    "MING_LATE": PHASE_MING_LATE,
}

ALL_PHASES = ["YUAN_EARLY", "YUAN_MIDDLE", "YUAN_LATE", "MING_EARLY", "MING_MIDDLE", "MING_LATE"]

_FLA = [PHASE_YUAN_EARLY, PHASE_YUAN_MIDDLE, PHASE_YUAN_LATE,
        PHASE_MING_EARLY, PHASE_MING_MIDDLE, PHASE_MING_LATE]
all_events = [ev for _phase in _FLA for ev in _phase]