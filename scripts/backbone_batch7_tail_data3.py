# -*- coding: utf-8 -*-
"""China History Backbone V1 — Batch 7（清→晚清→辛亥革命）Data（part 3）：甲午/庚子 + 辛亥革命 + 聚合导出。"""

from __future__ import annotations

from backbone_batch7_data import MODERN, W, _ev, _rel, PHASE_QING_ENTRY, PHASE_QING_HIGH  # noqa: F401
from backbone_batch7_tail_data import PHASE_OPIUM_TAIPING, PHASE_WESTERN_SELF  # noqa: F401

# ---------------------------------------------------------------------------
# Phase 5 — 甲午战争与庚子（1894—1901）
# ---------------------------------------------------------------------------
PHASE_SINO_JAPAN_BOXER = [
    _ev("event-jiawu-zhanzheng", "甲午战争（中日战争）", "war",
        1894, 1895, "range", "period-late-qing", "critical",
        "光绪二十至二十一年（1894—1895 年），日本以朝鲜东学党起义为契机出兵朝鲜，"
        "清军与日军在朝鲜、黄海、辽东、山东交战，"
        "北洋海军在黄海海战与威海卫之战中覆没，清军全面失败；"
        "1895 年签订《马关条约》。本事件为 aggregate，"
        "子事件（黄海海战、威海卫之战、马关条约）经 part_of 关联。",
        f"古代史料：《清实录·德宗实录》；《中日战争》资料丛刊；现代参考：{MODERN['late']}",
        W["qingshigao_lu"],
        ["regime-qing"],
        relations=[
            _rel("event-zhongfa-zhanzheng", "follows", 0.7, "中法战争后十年的对外战争。"),
            _rel("event-beiyang-haijun", "follows", 0.8, "北洋海军参战并覆没。"),
        ],
        review_note="甲午战败原因（体制、指挥、装备、后勤）史学界有系统讨论，"
                    "本事件不以\"腐败必败\"式单因结论代替过程描述。"),
    _ev("event-huanghai-haizhan", "黄海海战（大东沟海战）", "war",
        1894, 1894, "year", "period-late-qing", "major",
        "光绪二十年（1894 年）9 月，北洋舰队与日本联合舰队在黄海大东沟附近激战，"
        "致远、经远等舰沉没，邓世昌等殉国，双方均有损失，"
        "此后制海权转归日本联合舰队。",
        f"古代史料：《中日战争》资料丛刊；现代参考：{MODERN['late']}",
        W["qingshigao"],
        ["regime-qing"],
        relations=[
            _rel("event-jiawu-zhanzheng", "part_of", 0.95, "海战关键节点。"),
        ]),
    _ev("event-weihaiwei-zhizhan", "威海卫之战（北洋海军覆没）", "war",
        1895, 1895, "year", "period-late-qing", "major",
        "光绪二十一年（1895 年）1—2 月，日军海陆并进攻威海卫军港，"
        "北洋海军港内舰队突围失败，提督丁汝昌自杀（刘公岛陷落），"
        "北洋舰队全军覆没，甲午战争海战告终。",
        f"古代史料：《中日战争》资料丛刊；《清实录·德宗实录》；现代参考：{MODERN['late']}",
        W["qingshigao_lu"],
        ["regime-qing"],
        relations=[
            _rel("event-jiawu-zhanzheng", "part_of", 0.95, "海军最后的覆灭。"),
        ]),
    _ev("event-maguan-tiaoyue", "《马关条约》签订", "treaty",
        1895, 1895, "year", "period-late-qing", "major",
        "光绪二十一年（1895 年）4 月，李鸿章赴日签订《马关条约》："
        "中国割让台湾、澎湖与辽东半岛（后三国干涉还辽，改由清政府加银赎回），"
        "赔款二亿两白银，增开沙市、重庆、苏州、杭州为商埠并允许设厂；"
        "甲午战败震动全国，维新思潮兴起。",
        f"古代史料：《马关条约》文本；《清实录·德宗实录》；现代参考：{MODERN['late']}",
        W["qingshigao_lu"],
        ["regime-qing"],
        relations=[
            _rel("event-jiawu-zhanzheng", "part_of", 0.95, "战争的结局条约。"),
            _rel("event-gongche-shangshu", "leads_to", 0.9, "条约刺激在京举人上书（公车上书）。"),
        ]),
    _ev("event-gongche-shangshu", "公车上书", "political",
        1895, 1895, "year", "period-late-qing", "major",
        "光绪二十一年（1895 年）4 月，《马关条约》签订消息传京，"
        "康有为、梁启超联合各省在京应试举人上书光绪帝，"
        "请拒和、迁都、变法（公车上书）；上书被拒，但变法舆论由此兴起，"
        "为维新运动之先声。",
        f"古代史料：《康有为自编年谱》；现代参考（学界对签名人数有考订）：{MODERN['late']}",
        W["qingshigao"],
        ["regime-qing"],
        relations=[
            _rel("event-maguan-tiaoyue", "follows", 0.9, "条约刺激下的请愿行动。"),
            _rel("event-wuxu-bianfa", "leads_to", 0.9, "三年后发展为百日维新。"),
        ],
        review_note="\"公车上书\"的参与者人数与康有为主导性，学界（如茅海建等）有专门考订，"
                    "本事件记录上书行动的事实与影响。"),
    _ev("event-wuxu-bianfa", "戊戌变法（百日维新与政变）", "reform",
        1898, 1898, "year", "period-late-qing", "major",
        "光绪二十四年（1898 年），光绪帝采纳康有为等维新派主张，"
        "6 月 11 日下诏定国是，先后颁行废八股、设学堂、改官制、练兵等新政百余日"
        "（史称百日维新）；9 月 21 日慈禧太后发动政变，幽禁光绪帝，"
        "诛杀谭嗣同等\"戊戌六君子\"，康梁出亡，新政罢废。",
        f"古代史料：《清实录·德宗实录》；《戊戌变法》资料丛刊；现代参考：{MODERN['late']}",
        W["qingshigao_lu"],
        ["regime-qing"],
        relations=[
            _rel("event-gongche-shangshu", "follows", 0.9, "公车上书后的变法运动。"),
        ],
        review_note="戊戌变法在史学研究中有\"激进/渐进\"路线之争与政变细节考订（戊戌政变过程众说）；"
                    "本事件按诏令与政变的时间链记录。"),
    _ev("event-lieqiang-guafen", "列强瓜分势力范围（胶州湾等租借）", "diplomatic",
        1897, 1899, "range", "period-late-qing", "major",
        "光绪二十三至二十五年（1897—1899 年），俄、德、英、法、日相继强租旅大、"
        "胶州湾、威海卫、广州湾、九龙新界等并划分铁路矿山势力范围，"
        "掀起瓜分中国的狂潮（史称\"瓜分豆剖\"）；刺激了反帝与变法思潮。",
        f"古代史料：《清实录·德宗实录》；近代中外条约集；现代参考：{MODERN['late']}",
        W["qingshigao_lu"],
        ["regime-qing"],
        relations=[
            _rel("event-maguan-tiaoyue", "follows", 0.8, "甲午后列强竞相划占势力范围。"),
        ]),
    _ev("event-yihetuan-yundong", "义和团运动与八国联军战争", "rebellion",
        1899, 1901, "range", "period-late-qing", "major",
        "光绪二十五至二十七年（1899—1901 年），山东直隶民间兴起反对教会的义和团运动，"
        "清廷一度以\"招抚\"为策；1900 年 6 月八大列强组成联军（八国联军）来华，"
        "攻占大沽、天津，8 月攻入北京；1901 年签订《辛丑条约》。"
        "本事件为 aggregate，子事件（八国联军入京、辛丑条约）经 part_of 关联。",
        f"古代史料：《清实录·德宗实录》；《义和团档案史料》；现代参考：{MODERN['late']}",
        W["qingshigao_lu"],
        ["regime-qing"],
        relations=[
            _rel("event-lieqiang-guafen", "follows", 0.7, "瓜分危机激发排外运动。"),
        ],
        review_note="义和团性质（民间反抗/排外/愚昧迷信）评价分歧大；八国联军侵华事实中外记载一致。"
                    "本事件以事实框架记录，不用带立场标签。"),
    _ev("event-baguo-lianjun-ru-jing", "八国联军攻陷北京", "war",
        1900, 1900, "year", "period-late-qing", "major",
        "光绪二十六年（1900 年）6 月，英、美、德、法、俄、日、意、奥八国联军自天津进犯，"
        "8 月 14 日攻陷北京，慈禧太后挟光绪帝西逃（西安）；"
        "联军在京畿劫掠，圆明园旧地再遭破坏（另有义和团焚毁教堂等史实）。",
        f"古代史料：《清实录·德宗实录》西巡档；西人记载（如《慈禧外纪》等）；现代参考：{MODERN['late']}",
        W["qingshigao_lu"],
        ["regime-qing"],
        relations=[
            _rel("event-yihetuan-yundong", "part_of", 0.95, "联军来华攻京。"),
            _rel("event-xinchou-tiaoyue", "leads_to", 0.95, "城破后清廷乞和。"),
        ]),
    _ev("event-dongnan-hubao", "东南互保", "diplomatic",
        1900, 1900, "year", "period-late-qing", "major",
        "光绪二十六年（1900 年），八国联军战争期间，"
        "两江总督刘坤一、湖广总督张之洞等与各国驻沪领事达成《东南保护约款》，"
        "长江流域督抚不与联军作战、维护地方秩序（东南互保）；"
        "反映清廷中央权威在地方督抚实力上升背景下的松动。",
        f"古代史料：东南互保档案（《义和团档案史料》）；现代参考：{MODERN['late']}",
        W["qingshigao"],
        ["regime-qing"],
        relations=[
            _rel("event-baguo-lianjun-ru-jing", "follows", 0.8, "与联军开战同时的东南自保。"),
        ]),
    _ev("event-xinchou-tiaoyue", "《辛丑条约》签订", "treaty",
        1901, 1901, "year", "period-late-qing", "major",
        "光绪二十七年（1901 年）清廷与十一国签订《辛丑条约》："
        "赔款四亿五千万两（分三十九年还清，本息逾九亿八千万两）、"
        "划定使馆区、拆大沽炮台、禁止反抗等；"
        "条约使中国主权与财政承受空前负担，清政府沦为列强维持秩序的\"华北当局\"称呼变化（舆论语）。",
        f"古代史料：《辛丑条约》文本；《清实录·德宗实录》；现代参考：{MODERN['late']}",
        W["qingshigao_lu"],
        ["regime-qing"],
        relations=[
            _rel("event-yihetuan-yundong", "part_of", 0.95, "战争结局条约。"),
        ],
        review_note="条约文本与赔款数额依条约档案；\"丧权辱国\"为近代史通行评价术语，"
                    "本事件用条款直陈。"),
]


# ---------------------------------------------------------------------------
# Phase 6 — 清末新政与辛亥革命（1901—1912）
# ---------------------------------------------------------------------------
PHASE_REVOLUTION = [
    _ev("event-qingmo-xinzheng", "清末新政（庚子后改革）", "reform",
        1901, 1905, "range", "period-late-qing", "major",
        "光绪二十七年至三十一年（1901—1905 年），清廷在八国联军之役后推行新政："
        "设督办政务处、改革官制、练新军、办学堂、废科举、派留学生、"
        "设商部等，为清末预备立宪前的系统改革；"
        "新政扩大社会流动与舆论空间，客观上催生革命与立宪两派力量。",
        f"古代史料：《清实录·德宗实录》；《清末筹备立宪档案史料》；现代参考：{MODERN['xin hai']}",
        W["qingshigao_lu"],
        ["regime-qing"],
        relations=[
            _rel("event-xinchou-tiaoyue", "follows", 0.95, "庚子惨败后清廷自救。"),
            _rel("event-feichu-keju", "leads_to", 0.9, "1905 年废除科举为新政重要内容。"),
        ]),
    _ev("event-tongmenghui-chengli", "中国同盟会成立（东京）", "political",
        1905, 1905, "year", "period-late-qing", "major",
        "光绪三十一年（1905 年）8 月，孙中山在日本东京联合兴中会、华兴会、光复会等"
        "成立中国同盟会，提出\"驱除鞑虏，恢复中华，创立民国，平均地权\"纲领，"
        "出版《民报》，革命运动有了全国性组织与纲领。",
        f"古代史料：同盟会档案（《中国同盟会革命史料》）；现代参考：{MODERN['xin hai']}",
        W["qingshigao"],
        ["regime-qing"],
        relations=[
            _rel("event-qingmo-xinzheng", "follows", 0.6, "新政时期革命组织迅速发展。"),
            _rel("event-wuchang-qiyi", "leads_to", 0.9, "同盟会组织发动起义，最终武昌首义。"),
        ],
        review_note="同盟会纲领语言为历史文献原文引用（史实记录），本事件不承载其后的价值评价。"),
    _ev("event-feichu-keju", "废除科举制", "reform",
        1905, 1905, "year", "period-late-qing", "major",
        "光绪三十一年（1905 年）9 月，清廷颁布上谕停罢科举，"
        "在中国延续千余年的科举取士制度结束；"
        "教育体系转向学堂与留学，读书人出路与社会结构剧变。",
        f"古代史料：《清实录·德宗实录》；现代参考：{MODERN['xin hai']}",
        W["qingshigao_lu"],
        ["regime-qing"],
        relations=[
            _rel("event-qingmo-xinzheng", "follows", 0.9, "新政中的重要教育变革。"),
        ]),
    _ev("event-yubei-lixian", "预备立宪", "reform",
        1906, 1911, "range", "period-late-qing", "major",
        "光绪三十二年至宣统三年（1906—1911 年），清廷宣布\"仿行宪政\"："
        "改设资政院与各省咨议局（1909—1910 年），宣布九年预备立宪（后缩短年限），"
        "1911 年成立\"皇族内阁\"；"
        "预备立宪进程缓慢且皇族集权，促使立宪派倒向革命。",
        f"古代史料：《清末筹备立宪档案史料》；《清实录·德宗实录》；现代参考：{MODERN['xin hai']}",
        W["qingshigao_lu"],
        ["regime-qing"],
        relations=[
            _rel("event-qingmo-xinzheng", "follows", 0.9, "新政后期转入宪政改革。"),
            _rel("event-baolu-yundong", "leads_to", 0.9, "皇族内阁与铁路国有激化矛盾。"),
        ]),
    _ev("event-baolu-yundong", "铁路国有与保路运动（四川）", "rebellion",
        1911, 1911, "year", "period-late-qing", "major",
        "宣统三年（1911 年）5 月，清廷宣布铁路干线国有政策，收回商办铁路并举借外债，"
        "激起川汉、粤汉铁路股东与民众反对，四川保路运动声势浩大，"
        "清政府调湖北新军入川镇压，为武昌起义创造了有利时机。",
        f"古代史料：《清实录·宣统政纪》相关；《四川保路运动史料》；现代参考：{MODERN['xin hai']}",
        W["qingshigao"],
        ["regime-qing"],
        relations=[
            _rel("event-yubei-lixian", "follows", 0.9, "新政后期经济政策的激化。"),
            _rel("event-wuchang-qiyi", "leads_to", 0.9, "湖北新军调离，武昌空虚。"),
        ]),
    _ev("event-wuchang-qiyi", "武昌起义", "rebellion",
        1911, 1911, "year", "period-late-qing", "critical",
        "宣统三年（1911 年）10 月 10 日，湖北新军中的革命党人在武昌发动起义，"
        "攻占湖广总督衙门，成立湖北军政府；"
        "随后各省相继宣告独立（响应），清朝统治迅速瓦解。",
        f"古代史料：《辛亥革命回忆录》等当事人记载；《清史稿·宣统本纪》；现代参考：{MODERN['xin hai']}",
        W["qingshigao"],
        ["regime-qing"],
        relations=[
            _rel("event-baolu-yundong", "follows", 0.9, "保路运动牵制清军。"),
            _rel("event-tongmenghui-chengli", "follows", 0.7, "同盟会多年起义组织的结果。"),
            _rel("event-nanjing-linshi-zhengfu", "leads_to", 0.9, "各省响应后在南京建立临时政府。"),
        ]),
    _ev("event-nanjing-linshi-zhengfu", "中华民国临时政府成立（孙中山任临时大总统）", "foundation",
        1912, 1912, "year", "period-republic", "major",
        "1912 年 1 月 1 日，中华民国临时政府在南京成立，"
        "孙中山就任临时大总统，定国号为中华民国，改用公历；"
        "临时政府以革命派为主体并容纳各派，旋即面临南北和议。",
        f"古代史料：南京临时政府公报；《孙中山全集》；现代参考：{MODERN['xin hai']}",
        W["qingshigao"],
        ["regime-republic"],
        relations=[
            _rel("event-wuchang-qiyi", "follows", 0.9, "武昌起义后各省光复，建立中央政权。"),
            _rel("event-qingdi-tuiwei", "leads_to", 0.9, "南北议和后清帝退位，临时大总统让位袁世凯。"),
        ]),
    _ev("event-qingdi-tuiwei", "南北议和与清帝退位（清朝结束）", "political",
        1912, 1912, "year", "period-republic", "critical",
        "1912 年 1 月中旬起，南北议和（袁世凯、伍廷芳等）达成协议，"
        "以清帝退位换取袁世凯出任临时大总统；"
        "1912 年 2 月 12 日宣统帝溥仪下诏退位，清朝结束，"
        "中国两千余年的帝制时代（国内史学通行表述）随之终结。",
        f"古代史料：《清实录·宣统政纪》退位诏；《辛亥革命》资料丛刊；现代参考：{MODERN['xin hai']}",
        W["qingshigao"],
        ["regime-qing", "regime-republic"],
        relations=[
            _rel("event-nanjing-linshi-zhengfu", "follows", 0.9, "南京临时政府成立后的和议。"),
            _rel("event-wuchang-qiyi", "follows", 0.95, "武昌起义引发的政权更迭。"),
        ],
        review_note="退位诏书文本（含\"由袁世凯以全权组织临时共和政府\"句）为历史文献；"
                    "\"帝制终结\"为史学通说。本批（Batch7）终点，民国之后续（Batch8）另行展开。"),
]


PHASES = {
    "QING_ENTRY": PHASE_QING_ENTRY,
    "QING_HIGH": PHASE_QING_HIGH,
    "OPIUM_TAIPING": PHASE_OPIUM_TAIPING,
    "WESTERN_SELF": PHASE_WESTERN_SELF,
    "SINO_JAPAN_BOXER": PHASE_SINO_JAPAN_BOXER,
    "REVOLUTION": PHASE_REVOLUTION,
}

ALL_PHASES = ["QING_ENTRY", "QING_HIGH", "OPIUM_TAIPING", "WESTERN_SELF",
              "SINO_JAPAN_BOXER", "REVOLUTION"]

_FLA = [PHASE_QING_ENTRY, PHASE_QING_HIGH, PHASE_OPIUM_TAIPING, PHASE_WESTERN_SELF,
        PHASE_SINO_JAPAN_BOXER, PHASE_REVOLUTION]
all_events = [ev for _phase in _FLA for ev in _phase]