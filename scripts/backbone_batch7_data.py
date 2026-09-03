# -*- coding: utf-8 -*-
"""China History Backbone V1 — Batch 7（清→晚清→辛亥革命）Data（part 1）。

阶段拆分（阶段提交）：
- QING_ENTRY        清入关与统一（1626—1689）
- QING_HIGH         清前中期（1673—1804）
- OPIUM_TAIPING     鸦片战争与太平天国（1839—1864）
- WESTERN_SELF      洋务运动与边疆（1861—1888）
- SINO_JAPAN_BOXER  甲午战争与庚子（1894—1901）
- REVOLUTION        清末新政与辛亥革命（1901—1912）

复用（不重复建档）：event-houjin-jianguo（1616 后金建立）/ event-lizicheng-gong-beijing（1644 明亡）。
跨阶段关系一律前向禁引（放在后一阶段事件上 follows 指回先一阶段）。
"""

from __future__ import annotations

MODERN = {
    "qing": "孟森《清史讲义》（中华书局）；萧一山《清代通史》；白寿彝总主编《中国通史·清时期（上）》",
    "qing_gao": "肖一山《清代通史》；戴逸主编《简明清史》与《中国通史·清时期》；孟森《清史讲义》",
    "opium": "茅海建《天朝的崩溃——鸦片战争再研究》（生活·读书·新知三联书店）；"
             "郭廷以《近代中国史纲》；白寿彝《中国通史·晚清时期》",
    "taiping": "罗尔纲《太平天国史》（中华书局）；郭廷以《近代中国史纲》；茅海建《天朝的崩溃》",
    "yangwu": "夏东元《洋务运动史》（华东师范大学出版社）；罗尔纲《太平天国史》；"
              "郭廷以《近代中国史纲》",
    "late": "戚其章《甲午战争史》（人民出版社）；李剑农《中国近百年政治史》；"
            "郭廷以《近代中国史纲》",
    "xin hai": "金冲及、胡绳武《辛亥革命史稿》（上海人民出版社）；章开沅《辛亥革命史》；"
               "郭廷以《近代中国史纲》",
}

W = {
    "qingshigao": ["work-curated-qingshigao"],
    "qingshigao_lu": ["work-curated-qingshigao", "work-curated-qingshilu"],
    "qingshilu": ["work-curated-qingshilu"],
    "qingshigao_ming": ["work-curated-qingshigao", "work-curated-mingshi"],
    "qing_ming": ["work-curated-mingshi", "work-curated-qingshigao"],
    "qingshigao_taiping": ["work-curated-qingshigao"],
    "taiping": ["work-curated-qingshigao"],
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
# Phase 1 — 清入关与统一（1626—1689）
# ---------------------------------------------------------------------------
PHASE_QING_ENTRY = [
    _ev("event-huangtaiji-jiwei", "皇太极即后金汗位", "succession",
        1626, 1626, "year", "period-ming", "major",
        "天命十一年（1626 年），努尔哈赤去世，皇太极继后金汗位，"
        "改元天聪；皇太极在位期间改革女真制度、强化集权，并推进对明战争。",
        f"古代史料：《清实录·太宗实录》；现代参考：{MODERN['qing']}",
        W["qingshigao_lu"],
        ["regime-houjin"],
        relations=[
            _rel("event-houjin-jianguo", "follows", 0.9, "继努尔哈赤之后执掌后金。"),
            _rel("event-gaiguohao-qing", "leads_to", 0.9, "皇太极在位时改国号大清。"),
        ]),
    _ev("event-gaiguohao-qing", "改国号大清（皇太极称帝）", "foundation",
        1636, 1636, "year", "period-ming", "major",
        "崇德元年（1636 年），皇太极在沈阳称帝，改国号大金为“大清”，建元崇德，"
        "并改族称为满洲；清朝作为新国号的政权由此确立（后金阶段结束）。",
        f"古代史料：《清实录·太宗实录》；现代参考：{MODERN['qing']}",
        W["qingshigao_lu"],
        ["regime-qing"],
        relations=[
            _rel("event-huangtaiji-jiwei", "follows", 0.9, "皇太极即位后改国号。"),
            _rel("event-songjin-zhizhan", "leads_to", 0.8, "改国号后发动松锦决战。"),
        ],
        review_note="族称满洲的确立与国号大清同年（1636），本事件按《清实录》记载记录。"),
    _ev("event-songjin-zhizhan", "松锦之战（明清辽西决战）", "war",
        1640, 1642, "range", "period-ming", "major",
        "崇德五年至七年（1640—1642 年），清军围困锦州、松山，与明军（洪承畴督师）大战，"
        "明军主力溃败，松山、锦州相继失守，洪承畴被俘降清；"
        "明在山海关外的防线仅存宁远孤城，清军入关的通道基本打开。",
        f"古代史料：《清实录·太宗实录》；《明史·洪承畴传》；现代参考：{MODERN['qing']}",
        W["qingshigao_lu"],
        ["regime-qing", "regime-ming"],
        relations=[
            _rel("event-gaiguohao-qing", "follows", 0.9, "改国号后的辽西决战。"),
            _rel("event-qingjun-ru-guan", "leads_to", 0.9, "松锦战后两年清军入关。"),
        ]),
    _ev("event-qingjun-ru-guan", "清军入关、定鼎北京（山海关之战）", "dynastic-transition",
        1644, 1644, "year", "period-qing", "critical",
        "顺治元年（1644 年）四月，吴三桂引清军入关，在山海关与大顺军李自成部交战，"
        "大顺军败退，清军随即进入北京；同年十月顺治帝迁都北京，"
        "清朝定鼎中原，明清易代完成。",
        f"古代史料：《清实录·世祖实录》；《明史·庄烈帝纪》；现代参考：{MODERN['qing']}",
        W["qingshigao_lu"],
        ["regime-qing", "regime-ming"],
        relations=[
            _rel("event-lizicheng-gong-beijing", "follows", 0.9, "李自成入京后吴三桂引清军入关。"),
            _rel("event-songjin-zhizhan", "follows", 0.8, "松锦决战扫清入关障碍。"),
            _rel("event-nanming-hongguang", "leads_to", 0.8, "明宗室在南京建立南明。"),
        ],
        review_note="\"吴三桂引清兵入关\"情节按《清实录》与明清双方文献记录；对吴三桂个人动机"
                    "（联清还是降清的名分问题）史家有分歧，本事件记录入关与定鼎的事实进程。"),
    _ev("event-tifa-yifu", "清廷推行剃发易服令", "political",
        1645, 1645, "year", "period-qing", "major",
        "顺治二年（1645 年），清廷下令全国军民剃发易服（发式与衣冠改从满俗），"
        "以摄政王多尔衮名义重申\"剃发令\"；在江南引发大规模反抗并影响此后政治认同，"
        "为清初高压政策的组成部分。",
        f"古代史料：《清实录·世祖实录》；现代参考：{MODERN['qing']}",
        W["qingshigao_lu"],
        ["regime-qing"],
        relations=[
            _rel("event-qingjun-ru-guan", "follows", 0.9, "入关后次年颁行剃发令。"),
        ],
        review_note="剃发令属历史事实；学界对其执行过程（如\"留发不留头\"等说法）有细节辨析，"
                    "本事件按《清实录》诏令与执行事实记录，不作民族主义情绪化表述。"),
    _ev("event-nanming-hongguang", "南明弘光政权建立", "foundation",
        1644, 1645, "range", "period-qing", "major",
        "顺治元年（1644 年）五月，明福王朱由崧在南京称帝，建元弘光，"
        "是为第一个南明政权；弘光朝为党争所困，未及经营防务，"
        "顺治二年（1645 年）即告覆亡。",
        f"古代史料：《明史·福王传》（诸王传）；现代参考：{MODERN['qing']}",
        W["qing_ming"],
        ["regime-nanming"],
        relations=[
            _rel("event-qingjun-ru-guan", "follows", 0.8, "明亡后宗室南渡建国。"),
            _rel("event-qing-nanxia-jiangnan", "leads_to", 0.9, "清军南下攻灭弘光。"),
        ]),
    _ev("event-qing-nanxia-jiangnan", "清军南下、扬州之战与南京失守", "war",
        1645, 1645, "year", "period-qing", "major",
        "顺治二年（1645 年），清军多铎部南下，四月围攻扬州，史可法督守城破殉难，"
        "清军入城（扬州屠城说见时人记载，学界对死亡人数有不同估计）；"
        "五月清军克南京，弘光帝被俘，弘光政权灭亡。",
        f"古代史料：《清实录·世祖实录》；《扬州十日记》等时人记载；现代参考：{MODERN['qing']}",
        W["qingshigao_lu"],
        ["regime-qing", "regime-nanming"],
        relations=[
            _rel("event-nanming-hongguang", "follows", 0.9, "清军南下灭弘光。"),
            _rel("event-nanming-longwu-yongli", "leads_to", 0.8, "南方继续拥立隆武、永历。"),
        ],
        review_note="扬州围城中死亡人数各记载出入大（\"扬州十日\"之说源自《扬州十日记》，"
                    "现代研究对其具体数字有保留）；本事件记录城破与政权覆亡的事实。"),
    _ev("event-nanming-longwu-yongli", "南明隆武、永历政权（至南明灭亡）", "political",
        1645, 1662, "range", "period-qing", "major",
        "顺治二年至康熙元年（1645—1662 年），明宗室先后建立隆武（福州，1645—1646）、"
        "绍武、永历（肇庆/云贵，1646—1662）等政权，与清军周旋于东南与西南；"
        "康熙元年（1662 年）永历帝在昆明被吴三桂杀害，南明主要政权灭亡",
        f"古代史料：《明史》诸王传；《清实录·世祖实录》；现代参考：{MODERN['qing']}",
        W["qingshigao_lu"],
        ["regime-nanming"],
        relations=[
            _rel("event-qing-nanxia-jiangnan", "follows", 0.8, "弘光亡后南方继续抗清。"),
            _rel("event-zhengchenggong-qu-taiwan", "precedes", 0.6, "郑成功等依托海疆继续抗清。"),
        ]),
    _ev("event-zhengchenggong-qu-taiwan", "郑成功攻取台湾", "war",
        1661, 1662, "range", "period-qing", "major",
        "永历十五年（1661 年），郑成功率军自金厦渡海攻台湾，"
        "围困荷兰殖民者据守的热兰遮城，1662 年荷兰人投降，台湾纳入明郑政权统治；"
        "郑成功同年病逝，其子郑经继领台湾。",
        f"古代史料：《清史稿》郑成功传；荷兰东印度公司档案（《热兰遮城日志》）；现代参考：{MODERN['qing']}",
        W["qingshigao"],
        ["regime-nanming"],
        relations=[
            _rel("event-nanming-longwu-yongli", "follows", 0.7, "大陆抗清受挫后东渡台湾。"),
            _rel("event-qing-tongyi-taiwan", "leads_to", 0.9, "二十余年后清军攻台。"),
        ],
        review_note="郑成功收复台湾是中国海岛史重大节点；本事件按军事征台与荷兰投降的事实进程记录，"
                    "不作民族主义情绪渲染。"),
    _ev("event-sanfan-xingcheng", "三藩局面形成（吴三桂等镇守南疆）", "political",
        1662, 1673, "range", "period-qing", "major",
        "康熙元年以后（1662 年起），吴三桂镇云南贵州、尚可喜镇广东、耿精忠镇福建，"
        "并握有兵权财权，形成\"三藩\"割据局面；康熙帝亲政后筹划削藩，"
        "康熙十二年（1673 年）吴三桂举兵，三藩之乱爆发。",
        f"古代史料：《清史稿》吴三桂传；现代参考：{MODERN['qing']}",
        W["qingshigao"],
        ["regime-qing"],
        relations=[
            _rel("event-qingjun-ru-guan", "follows", 0.7, "入关后功臣镇边形成藩镇。"),
        ]),
    _ev("event-qing-tongyi-taiwan", "清统一台湾（澎湖海战、郑氏投降）", "war",
        1683, 1683, "year", "period-qing", "major",
        "康熙二十二年（1683 年），清军施琅率水师在澎湖海战大败郑军，"
        "郑克塽（郑成功之孙）降清，台湾纳入清朝版图，设台湾府隶属福建；"
        "清统一台湾完成。",
        f"古代史料：《清史稿》施琅传；《清实录·圣祖实录》；现代参考：{MODERN['qing']}",
        W["qingshigao_lu"],
        ["regime-qing", "regime-nanming"],
        relations=[
            _rel("event-zhengchenggong-qu-taiwan", "follows", 0.9, "明郑政权终结，台湾入清。"),
            _rel("event-yaquesha-zhizhan", "precedes", 0.6, "同年对俄雅克萨战争。"),
        ]),
    _ev("event-yaquesha-zhizhan", "雅克萨之战", "war",
        1685, 1686, "range", "period-qing", "major",
        "康熙二十四至二十五年（1685—1686 年），清军两次进攻俄军盘踞的雅克萨城（黑龙江），"
        "俄军受重创后求和，清朝在黑龙江流域的军事行动取得胜利，为尼布楚谈判奠定基础。",
        f"古代史料：《清实录·圣祖实录》；现代参考：{MODERN['qing']}",
        W["qingshigao_lu"],
        ["regime-qing"],
        relations=[
            _rel("event-qing-tongyi-taiwan", "follows", 0.7, "同期处理东北边疆对俄问题。"),
            _rel("event-nibuchu-tiaoyue", "leads_to", 0.95, "战后签订中俄尼布楚条约。"),
        ]),
    _ev("event-nibuchu-tiaoyue", "中俄尼布楚条约", "treaty",
        1689, 1689, "year", "period-qing", "major",
        "康熙二十八年（1689 年），清朝与俄国签订《尼布楚条约》，"
        "划定中俄东段边界（以外兴安岭为界），两国首次以条约确立边界关系，"
        "为中国近代以来与西方列强签订的第一个平等条约。",
        f"古代史料：《清实录·圣祖实录》；《中俄尼布楚条约》文本；现代参考：{MODERN['qing']}",
        W["qingshigao_lu"],
        ["regime-qing"],
        relations=[
            _rel("event-yaquesha-zhizhan", "follows", 0.95, "雅克萨之战后的和约。"),
        ],
        review_note="《尼布楚条约》勘界与文本（满、俄、拉丁文）研究见中西档案整理；"
                    "\"平等条约\"为学界常用中性表述（双方对等谈判），非政治化修饰。"),
]


# ---------------------------------------------------------------------------
# Phase 2 — 清前中期（1673—1804）
# ---------------------------------------------------------------------------
PHASE_QING_HIGH = [
    _ev("event-sanfan-zhi-luan", "三藩之乱与平定", "war",
        1673, 1681, "range", "period-qing", "critical",
        "康熙十二年至二十年（1673—1681 年），吴三桂等三藩举兵反清，"
        "一度控制南方大部；康熙帝力主平叛，历时八年，"
        "康熙二十年（1681 年）清军攻入昆明，三藩之乱平定，清朝完成统一。",
        f"古代史料：《清史稿》吴三桂传；《清实录·圣祖实录》；现代参考：{MODERN['qing']}",
        W["qingshigao_lu"],
        ["regime-qing"],
        relations=[
            _rel("event-sanfan-xingcheng", "follows", 0.95, "康熙削藩直接引发之乱。"),
        ]),
    _ev("event-kangxi-zheng-galdan", "康熙亲征噶尔丹（准噶尔战争）", "war",
        1690, 1697, "range", "period-qing", "major",
        "康熙二十九年至三十六年（1690—1697 年），康熙帝三次亲征漠西蒙古准噶尔部噶尔丹，"
        "先后在乌兰布通、昭莫多等地大败噶尔丹军，噶尔丹败亡；"
        "清朝遏制准噶尔东扩的战争取得阶段性胜利。",
        f"古代史料：《清实录·圣祖实录》；现代参考：{MODERN['qing']}",
        W["qingshigao_lu"],
        ["regime-qing"],
        relations=[
            _rel("event-nibuchu-tiaoyue", "follows", 0.7, "东北边约定后转向西北准噶尔问题。"),
            _rel("event-qianlong-ping-jun", "leads_to", 0.8, "准噶尔问题至乾隆朝最终解决。"),
        ]),
    _ev("event-yongzheng-jiwei", "雍正帝即位", "succession",
        1722, 1722, "year", "period-qing", "major",
        "康熙六十一年（1722 年）康熙帝去世，皇四子胤禛即位，是为雍正帝；"
        "雍正朝整顿吏治、强化皇权，是清中期制度调整的关键阶段"
        "（\"夺嫡\"说为清代宫廷史学公案，两说并存）。",
        f"古代史料：《清实录·世宗实录》；现代参考：{MODERN['qing']}",
        W["qingshigao_lu"],
        ["regime-qing"],
        relations=[
            _rel("event-kangxi-zheng-galdan", "follows", 0.6, "康熙晚年权力交接。"),
        ],
        review_note="雍正继承存在\"遗诏合法\"与\"矫诏夺位\"两种说法（《大义觉迷录》相关公案），"
                    "本事件记录即位事实，不采单一下断。"),
    _ev("event-tanding-rumu", "摊丁入亩与耗羡归公（雍正财政改革）", "reform",
        1723, 1729, "range", "period-qing", "major",
        "雍正元年至七年（1723—1729 年），雍正帝推行\"摊丁入亩\"（将丁银并入田赋征收）"
        "与\"耗羡归公\"（火耗统一上缴并发放养廉银），简化赋役、整顿地方财政，"
        "为清代税收制度的重要变革。",
        f"古代史料：《清实录·世宗实录》；现代参考：{MODERN['qing']}",
        W["qingshigao_lu"],
        ["regime-qing"],
        relations=[
            _rel("event-yongzheng-jiwei", "follows", 0.8, "雍正朝财政改革。"),
            _rel("event-gaituguiliu", "precedes", 0.6, "同期推行改土归流。"),
        ]),
    _ev("event-gaituguiliu", "改土归流（雍正朝西南改流）", "reform",
        1726, 1731, "range", "period-qing", "major",
        "雍正四至九年（1726—1731 年），清廷在西南（云贵桂川等）大规模推行改土归流："
        "废除世袭土司，改设流官，中央直接治理；为统一边疆的重要政治举措，"
        "过程中伴随武力镇抚。",
        f"古代史料：《清实录·世宗实录》；现代参考：{MODERN['qing']}",
        W["qingshigao_lu"],
        ["regime-qing"],
        relations=[
            _rel("event-yongzheng-jiwei", "follows", 0.7, "雍正朝的边疆治理改革。"),
        ],
        review_note="改土归流涉及民族地区治理，学界对其利弊（统一与民生代价）评价不一；"
                    "本事件按制度推行与流官设置的事实进程记录。"),
    _ev("event-junjichu", "军机处设立", "reform",
        1729, 1732, "range", "period-qing", "major",
        "雍正七年（1729 年）因西北用兵设军机处（初为军需房），"
        "后演变为辅佐皇帝处理军国要务的常设机构；"
        "军机处制度使清朝皇权行使达到此前历代之最集中形态，并沿至清末。",
        f"古代史料：《清史稿·职官志》；现代参考：{MODERN['qing']}",
        W["qingshigao"],
        ["regime-qing"],
        relations=[
            _rel("event-yongzheng-jiwei", "follows", 0.8, "雍正朝设立的中枢机构。"),
        ]),
    _ev("event-qianlong-ping-jun", "乾隆平定准噶尔、统一新疆", "war",
        1755, 1759, "range", "period-qing", "major",
        "乾隆二十年至二十四年（1755—1759 年），清军进军伊犁，"
        "先后平定准噶尔汗国（达瓦齐、阿睦尔撒纳）与大小和卓叛乱，"
        "设伊犁将军等统辖天山南北，新疆纳入清朝版图（清统一西北）。",
        f"古代史料：《清实录·高宗实录》；现代参考：{MODERN['qing']}",
        W["qingshigao_lu"],
        ["regime-qing"],
        relations=[
            _rel("event-kangxi-zheng-galdan", "follows", 0.9, "准噶尔问题最终解决。"),
        ],
        review_note="乾隆朝对准噶尔用兵的过程与后果（包括大规模动迁与人口损失）是清史研究重要课题，"
                    "各当事人文献与后世研究记载不一；本事件记录军事进程与政区建置事实，"
                    "对伤亡与\"绝灭\"类叙述不作未经考订的断言。"),
    _ev("event-tuerhute-donggui", "土尔扈特部东归", "migration",
        1771, 1771, "year", "period-qing", "major",
        "乾隆三十六年（1771 年），滞留伏尔加河下游近一个半世纪的土尔扈特部"
        "在渥巴锡率领下万里东归，返回伊犁，清廷予以安置；"
        "为清中期民族迁徙与边疆治理的重要事件。",
        f"古代史料：《清实录·高宗实录》土尔扈特归附档；现代参考：{MODERN['qing']}",
        W["qingshigao_lu"],
        ["regime-qing"],
        relations=[
            _rel("event-qianlong-ping-jun", "follows", 0.9, "新疆平定后土尔扈特东归归清。"),
        ]),
    _ev("event-siku-quanshu", "《四库全书》编纂", "cultural",
        1773, 1782, "range", "period-qing", "major",
        "乾隆三十八年至四十七年（1773—1782 年），乾隆帝组织编纂《四库全书》，"
        "辑录古今典籍三万四千余种，抄成七部藏于文渊、文澜等阁；"
        "编纂过程同时伴随大规模禁毁书目（四库禁毁书），为文献整理与文化管制并存事件。",
        f"古代史料：《四库全书总目》；《清实录·高宗实录》；现代参考：{MODERN['qing']}",
        W["qingshigao_lu"],
        ["regime-qing"],
        relations=[
            _rel("event-qianlong-ping-jun", "follows", 0.6, "乾隆中期文治工程。"),
        ],
        review_note="四库全书兼具\"整理文献\"与\"寓禁于征\"两面，学界已考订禁毁书籍数量；"
                    "本事件两面如实记录。"),
    _ev("event-macartney-shi-tuan", "马戛尔尼使团来华", "diplomatic",
        1793, 1793, "year", "period-qing", "major",
        "乾隆五十八年（1793 年），英国派遣马戛尔尼使团来华，"
        "在热河觐见乾隆帝，提出通商与使节驻京等要求，清廷以\"天朝体制\"为由拒绝，"
        "中英首次正式外交接触以无果告终，为鸦片战争前中西关系的标志性节点。",
        f"古代史料：《清实录·高宗实录》英吉利来使档；马戛尔尼使团纪录（《英使谒见乾隆纪实》）；现代参考：{MODERN['qing']}",
        W["qingshigao_lu"],
        ["regime-qing"],
        relations=[
            _rel("event-siku-quanshu", "follows", 0.5, "乾隆盛世后期的中西接触。"),
            _rel("event-bailianjiao-qiyi", "precedes", 0.6, "三年后白莲教起义爆发。"),
        ],
        review_note="关于马戛尔尼使团是否行跪拜礼及其含义，中英记载与研究者有不同解读；"
                    "本事件记录使团行程与交涉结果的事实。"),
    _ev("event-bailianjiao-qiyi", "川楚白莲教起义", "rebellion",
        1796, 1804, "range", "period-qing", "major",
        "嘉庆元年至九年（1796—1804 年），川、楚、陕三省白莲教教徒因赋役与流民问题聚合起义，"
        "清廷调集重兵历时九年方基本平定；"
        "起义耗费巨帑、暴露八旗与绿营颓势，成为清朝由盛转衰的重要转折（清中期分水岭）。",
        f"古代史料：《清史稿》仁宗纪；《清实录·仁宗实录》；现代参考：{MODERN['qing']}",
        W["qingshigao_lu"],
        ["regime-qing"],
        relations=[
            _rel("event-macartney-shi-tuan", "follows", 0.6, "乾隆末年-嘉庆初年社会矛盾爆发。"),
        ]),
]