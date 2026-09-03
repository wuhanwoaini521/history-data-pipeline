# -*- coding: utf-8 -*-
"""China History Backbone V1 — Batch 8（中华民国→近现代）Data（part 3）：日本侵华 + 全面抗战/1949 + 聚合导出。"""

from __future__ import annotations

from backbone_batch8_data import MODERN, WP, _ev, _rel, PHASE_REPUBLIC_EARLY  # noqa: F401
from backbone_batch8_tail_data import PHASE_WARLORDS_MAY4TH, PHASE_NATIONAL_REV, PHASE_CPC_EARLY  # noqa: F401

# ---------------------------------------------------------------------------
# Phase 5 — 日本侵华（1931—1936）
# ---------------------------------------------------------------------------
PHASE_JAPAN_INVASION = [
    _ev("event-jiuyiba-shibian", "九一八事变（沈阳）", "war",
        1931, 1931, "year", "period-republic", "critical",
        "1931 年 9 月 18 日夜，日本关东军自行炸毁沈阳柳条湖附近南满铁路并嫁祸中国军队，"
        "随即进攻沈阳北大营，占领沈阳及东北三省大部（九一八事变）；"
        "国民政府实行\"不抵抗\"方针（具体指令及责任为史学争论点），东北全境沦陷。",
        f"档案史料：中日双方军事档案（关东军参谋部纪录）；现代研究：{MODERN['kangzhan']}",
        WP["minguo_kz"],
        ["regime-republic"],
        relations=[
            _rel("event-dongbei-yizhi", "follows", 0.7, "东北易帜后三年东北沦陷。"),
            _rel("event-manzhouguo-jianli", "leads_to", 0.95, "次年建立满洲国。"),
        ],
        review_note="柳条湖炸路与\"不抵抗\"指令的责任归属（张学良/蒋介石）是长期史学公案，"
                    "本事件记录事变经过与结果事实。"),
    _ev("event-manzhouguo-jianli", "满洲国建立（日本扶持）", "foundation",
        1932, 1932, "year", "period-republic", "major",
        "1932 年 3 月，日本关东军扶植清废帝溥仪在长春（新京）建立满洲国，"
        "以\"五族协和\"相标榜，实为日本傀儡政权，治下东北实行殖民统治；"
        "1945 年日本战败后消失。",
        f"档案史料：满洲国设立文书（关东军档案）；现代研究：{MODERN['kangzhan']}",
        WP["kz"],
        ["regime-manchukuo", "regime-republic"],
        relations=[
            _rel("event-jiuyiba-shibian", "follows", 0.95, "东北沦陷后建立的傀儡政权。"),
        ]),
    _ev("event-yi-er-ba-shibian", "一二八事变（淞沪抗战）", "war",
        1932, 1932, "year", "period-republic", "major",
        "1932 年 1 月 28 日，日军进攻上海，国民政府军第十九路军奋起抵抗（淞沪抗战），"
        "战事持续一个多月，经英美调停签订《淞沪停战协定》，"
        "上海华界部分地区日军驻留权等问题留下后患。",
        f"档案史料：淞沪停战协定文本与各方档案；现代研究：{MODERN['kangzhan']}",
        WP["minguo_kz"],
        ["regime-republic"],
        relations=[
            _rel("event-jiuyiba-shibian", "follows", 0.9, "九一八后日军进一步进犯上海。"),
        ]),
    _ev("event-huabei-shibian", "华北事变", "political",
        1935, 1935, "year", "period-republic", "major",
        "1935 年，日本策动华北五省\"自治\"运动，逼迫国民政府妥协"
        "（《何梅协定》、冀东伪政权等），华北主权危机加深，"
        "全国抗日救亡运动高涨（一二·九运动等）。",
        f"档案史料：何梅协定相关文件、日本外务省档案；现代研究：{MODERN['kangzhan']}",
        WP["minguo_kz"],
        ["regime-republic"],
        relations=[
            _rel("event-manzhouguo-jianli", "follows", 0.8, "东北之后华北再起危机。"),
            _rel("event-xian-shibian", "leads_to", 0.9, "华北危机促使张学良杨虎城逼蒋抗日。"),
        ]),
    _ev("event-xian-shibian", "西安事变", "political",
        1936, 1936, "year", "period-republic", "critical",
        "1936 年 12 月 12 日，张学良、杨虎城在西安扣留蒋介石，通电要求停止内战、一致抗日"
        "（西安事变，\"兵谏\"）；经各方调停，事变以蒋介石获释、主张停止内战转向抗日收束，"
        "成为时局转折点（史学通说）。",
        f"档案史料：西安事变谈判纪录与当事方文电；现代研究：{MODERN['kangzhan']}",
        WP["minguo_kz"],
        ["regime-republic"],
        relations=[
            _rel("event-huabei-shibian", "follows", 0.9, "华北危机与剿共并存的局面。"),
            _rel("event-changzheng", "follows", 0.8, "红军到达陕北后张杨与中共接触。"),
        ],
        review_note="事变和平解决的具体谈判过程（周恩来、宋美龄、宋子文等角色）见专门研究；"
                    "本事件记录扣留、谈判与和平解决的事实框架。"),
]


# ---------------------------------------------------------------------------
# Phase 6 — 全面抗战与 1949 边界（1937—1949）
# ---------------------------------------------------------------------------
PHASE_FULL_WAR_1949 = [
    _ev("event-qiqishi-bian", "七七事变（卢沟桥事变）", "war",
        1937, 1937, "year", "period-republic", "critical",
        "1937 年 7 月 7 日夜，日军在北平西南卢沟桥演习时借口士兵失踪要求入城搜查，"
        "遭拒后进攻宛平城（七七事变），日军旋即丰台、北平、天津相继失守；"
        "七七事变标志着日本全面侵华战争开始，中国全国性抗战由此展开。",
        f"档案史料：事变双方军事纪录、日内瓦中国代表团陈报；现代研究：{MODERN['kangzhan']}",
        WP["minguo_kz"],
        ["regime-republic"],
        relations=[
            _rel("event-xian-shibian", "follows", 0.9, "西安事变后七个月全面抗战爆发。"),
            _rel("event-songhu-huizhan", "leads_to", 0.9, "随后淞沪会战打响。"),
        ]),
    _ev("event-songhu-huizhan", "淞沪会战（八一三战役）", "war",
        1937, 1937, "range", "period-republic", "major",
        "1937 年 8 月 13 日至 11 月，中日两军在淞沪地区展开大会战，"
        "中国军队投入主力约七十余个师，坚守三个月后撤退（11 月 12 日上海失守），"
        "于上海：役中中国空军有首次空战战果（史实细节见专史）。",
        f"档案史料：淞沪会战战斗详报；现代研究：{MODERN['kangzhan']}",
        WP["kz"],
        ["regime-republic"],
        relations=[
            _rel("event-qiqishi-bian", "follows", 0.9, "七七事变后的大规模会战。"),
            _rel("event-nanjing-baoweizhan", "leads_to", 0.9, "上海失守后日军进攻南京。"),
        ]),
    _ev("event-nanjing-baoweizhan", "南京保卫战与失守", "war",
        1937, 1937, "year", "period-republic", "major",
        "1937 年 11—12 月，日军侵占上海后分路进攻南京，"
        "中国军队在南京外围及城垣抵抗（南京保卫战），12 月 13 日南京陷落，"
        "国民政府已于此前西迁重庆（11 月 20 日宣布迁都）。",
        f"档案史料：南京保卫战战斗详报；现代研究：{MODERN['kangzhan']}",
        WP["kz"],
        ["regime-republic"],
        relations=[
            _rel("event-songhu-huizhan", "follows", 0.9, "淞沪失利后日军进犯南京。"),
            _rel("event-nanjing-datusha", "leads_to", 0.95, "城陷后日军在南京实施大规模暴行。"),
        ]),
    _ev("event-nanjing-datusha", "南京大屠杀", "war",
        1937, 1938, "range", "period-republic", "critical",
        "1937 年 12 月 13 日南京陷落后，侵华日军在南京城区及周边持续数周"
        "大规模屠杀中国平民与战俘、强暴妇女并抢劫纵火（南京大屠杀）；"
        "关于遇难人数，中日与国际学界及战后审判档案存在不同统计口径"
        "（通行约 30 万，具体数字仍是研究课题）；1946—1948 年南京审判/"
        "东京审判对此罪行予以认定。",
        f"档案史料：战后南京军事法庭审判档案、《南京大屠杀史料集》（张宪文主编，江苏人民出版社）；"
        f"现代研究：{MODERN['kangzhan']}",
        WP["kz"],
        ["regime-republic"],
        relations=[
            _rel("event-nanjing-baoweizhan", "follows", 0.95, "南京陷落后的暴行。"),
        ],
        review_note="遇难人数统计口径（如\"三十万\"为通行表述，亦有二十余万—三十万的不同估计）"
                    "均以史料与审判档案为据；本事件不淡化事实、不作情绪化修辞，"
                    "接受学界对口径差异的讨论（见《南京大屠杀史料集》编者说明）。"),
    _ev("event-wuhan-huizhan", "武汉会战", "war",
        1938, 1938, "range", "period-republic", "major",
        "1938 年 6—10 月，中日双方展开武汉会战（中国军队约百万人参战），"
        "日军攻占武汉（10 月 25 日），国民政府继续西移重庆，"
        "抗战转入相持阶段（史学通说）。",
        f"档案史料：武汉会战战斗详报；现代研究：{MODERN['kangzhan']}",
        WP["kz"],
        ["regime-republic"],
        relations=[
            _rel("event-nanjing-datusha", "follows", 0.8, "南京失守后中日沿江激战。"),
        ]),
    _ev("event-changsha-huizhan", "长沙会战（三次大会战）", "war",
        1939, 1942, "range", "period-republic", "major",
        "1939 年 9 月至 1942 年 1 月，中日军队在长沙地区展开三次大会战，"
        "中国军队均击退日军进攻（第九战区），长沙保卫战为相持阶段的重要战例。",
        f"档案史料：长沙会战战斗详报；现代研究：{MODERN['kangzhan']}",
        WP["kz"],
        ["regime-republic"],
        relations=[
            _rel("event-wuhan-huizhan", "follows", 0.8, "相持阶段的长沙拉锯战。"),
        ]),
    _ev("event-baidatuan", "百团大战", "war",
        1940, 1940, "range", "period-republic", "major",
        "1940 年 8 月至 12 月，中共领导的八路军在华北发动百团大战"
        "（因兵力约一百零五个团得名），破袭日军交通线与据点，"
        "为敌后战场规模最大的攻势作战（战斗数据与评价见专史，两方文献记载有差异）。",
        f"档案史料：八路军作战纪录；现代研究：《中国共产党历史》第一卷、{MODERN['kangzhan']}",
        WP["minguo_kz"],
        [],
        relations=[
            _rel("event-changsha-huizhan", "precedes", 0.5, "同一时期敌后战场的攻势。"),
        ]),
    _ev("event-yuanzhengjun", "中国远征军（滇缅战场）", "war",
        1942, 1945, "range", "period-republic", "major",
        "1942 年日军攻占缅甸后，中国组建远征军入缅作战（第一次入缅失利），"
        "1943—1945 年驻印军与滇西远征军反攻（缅北滇西反攻战），"
        "配合盟军打通中印公路，为世界反法西斯战争中国战场的海外作战部分。",
        f"档案史料：远征军作战档案；现代研究：{MODERN['kangzhan']}",
        WP["kz"],
        ["regime-republic"],
        relations=[
            _rel("event-wuhan-huizhan", "follows", 0.7, "相持阶段海外战场开辟。"),
            _rel("event-yuxianggui", "precedes", 0.6, "1944 年反攻期间豫湘桂战役发生。"),
        ]),
    _ev("event-yuxianggui", "豫湘桂战役", "war",
        1944, 1944, "range", "period-republic", "major",
        "1944 年 4—12 月，日军发动打通大陆交通线的\"一号作战\"（豫湘桂战役），"
        "攻占河南、湖南、广西大部，中国军队正面战场出现大溃退（损失巨大，数据见专史）；"
        "是为中国战场后期规模最大的一次反攻性进攻。",
        f"档案史料：豫湘桂战役战斗详报（中方）与日军作战纪录；现代研究：{MODERN['kangzhan']}",
        WP["kz"],
        ["regime-republic"],
        relations=[
            _rel("event-changsha-huizhan", "follows", 0.7, "长沙三次会战后的又一次大会战。"),
        ]),
    _ev("event-riben-touxiang", "日本宣布投降（抗日战争胜利）", "treaty",
        1945, 1945, "year", "period-republic", "critical",
        "1945 年 8 月 15 日，日本天皇广播《终战诏书》宣布接受《波茨坦公告》并无条件投降；"
        "9 月 2 日日本签署投降书，9 月 9 日中国战区受降（南京）；"
        "中国抗日战争取得胜利，是世界反法西斯战争胜利的组成部分。",
        f"档案史料：终战诏书文本、中国战区受降档案；现代研究：{MODERN['kangzhan']}",
        WP["minguo_kz"],
        ["regime-republic"],
        relations=[
            _rel("event-yuxianggui", "follows", 0.8, "1945 年日军崩溃投降。"),
            _rel("event-taiwan-guangfu", "leads_to", 0.95, "台湾于同年光复。"),
            _rel("event-chongqing-tanpan", "leads_to", 0.9, "胜利后国共重庆谈判。"),
        ]),
    _ev("event-taiwan-guangfu", "台湾光复", "political",
        1945, 1945, "year", "period-republic", "major",
        "1945 年 10 月 25 日，中国战区台湾省受降仪式在台北举行，"
        "台湾及澎湖结束日本殖民统治（50 年），重归中国版图（台湾光复）。",
        f"档案史料：中国战区台湾省受降档案；现代研究：{MODERN['kangzhan']}",
        WP["minguo_kz"],
        ["regime-republic"],
        relations=[
            _rel("event-riben-touxiang", "follows", 0.95, "日本投降后台湾归还中国。"),
        ]),
    _ev("event-chongqing-tanpan", "重庆谈判（国共和谈）", "diplomatic",
        1945, 1945, "range", "period-republic", "major",
        "1945 年 8—10 月，毛泽东应蒋介石之邀赴重庆与国民政府谈判，"
        "10 月 10 日签署《双十协定》（和平建国、召开政协等原则），"
        "但军事冲突并未停止，和谈成果有限。",
        f"档案史料：《双十协定》文本与随行记录；现代研究：{MODERN['1945']}",
        WP["minguo"],
        [],
        relations=[
            _rel("event-riben-touxiang", "follows", 0.9, "胜利后国共最高层会谈。"),
            _rel("event-zhengzhi-xieshang-huiyi", "leads_to", 0.9, "按协定召开政治协商会议。"),
        ]),
    _ev("event-zhengzhi-xieshang-huiyi", "政治协商会议（旧政协）", "diplomatic",
        1946, 1946, "year", "period-republic", "major",
        "1946 年 1 月，政治协商会议在重庆召开（国共、民盟、青年党等参加），"
        "通过政府改组、和平建国纲领等五项决议；决议因国民党六届二中全会"
        "与内战的扩大而未切实执行（政协决议之争为史学议题）。",
        f"档案史料：政治协商会议纪录；现代研究：{MODERN['1945']}",
        WP["minguo"],
        [],
        relations=[
            _rel("event-chongqing-tanpan", "follows", 0.9, "双十协定后的协商会议。"),
            _rel("event-quanmian-neizhan", "leads_to", 0.9, "政协决议未执行，内战全面爆发。"),
        ]),
    _ev("event-quanmian-neizhan", "全面内战爆发", "war",
        1946, 1946, "year", "period-republic", "major",
        "1946 年 6 月，国民政府军进攻中原解放区，国共全面内战爆发；"
        "此后战局历经战略防御、战略反攻与战略决战（1948 年秋起）三阶段。",
        f"档案史料：双方军事档案；现代研究：{MODERN['1945']}",
        WP["minguo"],
        [],
        relations=[
            _rel("event-zhengzhi-xieshang-huiyi", "follows", 0.9, "和谈破裂后全面战争。"),
            _rel("event-liaoshen-zhanyi", "leads_to", 0.9, "1948 年起三大战役决战。"),
        ]),
    _ev("event-liaoshen-zhanyi", "辽沈战役", "war",
        1948, 1948, "range", "period-republic", "major",
        "1948 年 9 月 12 日至 11 月 2 日，人民解放军在东北发动辽沈战役，"
        "攻占锦州、长春、沈阳等地，国民党军东北战场主力被歼（约四十七万人），"
        "东北全境易手。",
        f"档案史料：战役作战纪录；现代研究：{MODERN['1945']}",
        WP["minguo"],
        [],
        relations=[
            _rel("event-quanmian-neizhan", "follows", 0.9, "战略决战第一役。"),
            _rel("event-huaihai-zhanyi", "leads_to", 0.9, "辽沈后华北、华东决战。"),
            _rel("event-pingjin-zhanyi", "leads_to", 0.9, "辽沈后平津战役。"),
        ]),
    _ev("event-huaihai-zhanyi", "淮海战役", "war",
        1948, 1949, "range", "period-republic", "major",
        "1948 年 11 月 6 日至 1949 年 1 月 10 日，人民解放军华东、中原野战军"
        "在淮海地区决战，全歼国民党军徐州集团主力约五十五万余人，"
        "国民党在华东的统治基本瓦解。",
        f"档案史料：战役作战纪录；现代研究：{MODERN['1945']}",
        WP["minguo"],
        [],
        relations=[
            _rel("event-liaoshen-zhanyi", "follows", 0.9, "继辽沈之后的中原决战。"),
        ]),
    _ev("event-pingjin-zhanyi", "平津战役（北平和平改编）", "war",
        1948, 1949, "range", "period-republic", "major",
        "1948 年 11 月 29 日至 1949 年 1 月 31 日，人民解放军华北野战军等发动平津战役，"
        "攻克天津，促成傅作义接受和平改编，北平和平解放（1949 年 1 月 31 日），"
        "华北全境基本解放。",
        f"档案史料：平津战役与北平谈判纪录；现代研究：{MODERN['1945']}",
        WP["minguo"],
        [],
        relations=[
            _rel("event-liaoshen-zhanyi", "follows", 0.9, "辽沈胜利促成平津局面。"),
        ]),
    _ev("event-dujiang-nanjing", "渡江战役与南京易手（国民政府南迁）", "war",
        1949, 1949, "year", "period-republic", "major",
        "1949 年 4 月 20—23 日，人民解放军百万大军渡长江，4 月 23 日占领南京；"
        "国民政府此前迁广州，后迁台北；10 月 1 日中华人民共和国成立"
        "（中华民国在大陆的统治结束，海峡两岸分治局面形成，中性表述）。",
        f"档案史料：渡江战役作战纪录、国民政府西迁档案；现代研究：{MODERN['1945']}",
        WP["minguo"],
        ["regime-republic"],
        relations=[
            _rel("event-pingjin-zhanyi", "follows", 0.9, "三大战役后进行渡江战役。"),
            _rel("event-xinzhongguo-chengli", "leads_to", 0.95, "占领南京后中华人民共和国成立。"),
        ]),
    _ev("event-xinzhongguo-chengli", "中华人民共和国成立", "foundation",
        1949, 1949, "year", "period-modern", "critical",
        "1949 年 10 月 1 日，毛泽东在北京天安门宣布中华人民共和国中央人民政府成立；"
        "本事件为现代 China 史主干之边界点（modern boundary event，§64），"
        "1950 年代以后的历史留待 Modern China Backbone V2 另行建设。",
        f"档案史料：开国大典档案与《人民日报》首刊；现代研究：《中国共产党历史》第一卷、{MODERN['1945']}",
        WP["minguo"],
        ["regime-republic"],
        relations=[
            _rel("event-dujiang-nanjing", "follows", 0.95, "大陆战事结束后建政。"),
        ],
        review_note="1949 年 10 月 1 日具体以公元纪年记录；此后（1950—2026）不在本任务范围（§64）。"),
]


PHASES = {
    "REPUBLIC_EARLY": PHASE_REPUBLIC_EARLY,
    "WARLORDS_MAY4TH": PHASE_WARLORDS_MAY4TH,
    "NATIONAL_REV": PHASE_NATIONAL_REV,
    "CPC_EARLY": PHASE_CPC_EARLY,
    "JAPAN_INVASION": PHASE_JAPAN_INVASION,
    "FULL_WAR_1949": PHASE_FULL_WAR_1949,
}

ALL_PHASES = ["REPUBLIC_EARLY", "WARLORDS_MAY4TH", "NATIONAL_REV", "CPC_EARLY",
              "JAPAN_INVASION", "FULL_WAR_1949"]

_FLA = [PHASE_REPUBLIC_EARLY, PHASE_WARLORDS_MAY4TH, PHASE_NATIONAL_REV, PHASE_CPC_EARLY,
        PHASE_JAPAN_INVASION, PHASE_FULL_WAR_1949]
all_events = [ev for _phase in _FLA for ev in _phase]