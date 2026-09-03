# -*- coding: utf-8 -*-
"""China History Backbone V1 — Batch 4（隋→唐→五代十国）Curated Event Data。

写入 events/sui_tang（隋/唐）与 events/five_dynasties（五代十国/辽）。

复用（不重复建档）：
- event-yangjian-dai-beizhou（581 隋建立）/ event-sui-mie-chen（589 隋灭陈统一）
- 安史之乱 Story 9 个既有 Event（event-anlu-*，sui_tang/）
"""

from __future__ import annotations

MODERN = {
    "suitang": "岑仲勉《隋唐史》（中华书局）；吴宗国《隋唐五代简史》（北京大学出版社）；"
               "王仲荦《隋唐五代史》；张岂之主编《中国历史·隋唐辽宋金元卷》；白寿彝总主编《中国通史》",
    "tang": "吴宗国《隋唐五代简史》；陈寅恪《隋唐制度渊源略论稿》与《唐代政治史述论稿》；"
            "岑仲勉《隋唐史》；黄永年《六至九世纪中国政治史》；白寿彝《中国通史》",
    "wudai": "王仲荦《隋唐五代史》；欧阳修《新五代史》序论；陶懋炳《五代史略》；白寿彝《中国通史》",
}

W = {
    "suishu": ["work-curated-suishu"],
    "suishu_tang": ["work-curated-suishu", "work-curated-jiutangshu"],
    "jiutang": ["work-curated-jiutangshu"],
    "liangtang": ["work-curated-jiutangshu", "work-curated-xintangshu"],
    "xintang": ["work-curated-xintangshu"],
    "xintang_zizhi": ["work-curated-xintangshu", "work-curated-zizhitongjian"],
    "jiutang_zizhi": ["work-curated-jiutangshu", "work-curated-zizhitongjian"],
    "zizhi": ["work-curated-zizhitongjian"],
    "wudai": ["work-curated-jiuwudaishi", "work-curated-xinwudaishi"],
    "wudai_zizhi": ["work-curated-jiuwudaishi", "work-curated-xinwudaishi", "work-curated-zizhitongjian"],
    "liao": ["work-curated-liaoshi"],
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
    """regimes_or_relations：source_ids 之后的列表参数（同 batch3 _ev）。"""
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
# Phase 1 — 隋（复用 581 隋建立 / 589 隋灭陈）
# ---------------------------------------------------------------------------
PHASE_SUI = [
    _ev("event-kaihuang-lv", "开皇律制定", "reform",
        581, 583, "range", "period-sui", "major",
        "隋文帝开皇年间（581—583）命高颎、苏威等更定刑律，颁行《开皇律》："
        "定笞杖徒流死五刑，废枭首、鞭刑等酷刑，确立\"十恶\"重罪名目。"
        "《开皇律》是隋唐法律体系从《北周律》转向以《隋律》为范本的奠基之作，"
        "其后唐律即本于此。",
        f"古代史料：《隋书·刑法志》；现代参考：{MODERN['suitang']}",
        W["suishu"],
        [],
        review_note="《开皇律》于开皇元年（581）诏修、三年（583）完成；\"十恶\"之名始见于此（唐律沿用）。"),
    _ev("event-sui-sansheng-liubu", "隋代三省六部官制确立", "reform",
        581, 583, "range", "period-sui", "major",
        "隋文帝确立三省（尚书、门下、内史）六部（吏户礼兵刑工）官制，"
        "中书省称内史省，实行三省分权、共同辅政的中央行政框架。"
        "三省六部制为唐代承袭并完善，成为此后中国王朝中央政务的基本组织。",
        f"古代史料：《隋书·百官志》；现代参考：{MODERN['suitang']}",
        W["suishu"],
        [],
        review_note="三省六部官制为隋代制度创建节点（制度框架确立），唐代在此基础上发展（§6：记制度建立节点而非概念）。"),
    _ev("event-sui-keju-chuangjian", "科举制度开创（废九品中正、设进士科）", "reform",
        581, 605, "range", "period-sui", "major",
        "隋文帝废九品中正制（约开皇年间），以科举考试选拔人才；"
        "隋炀帝大业年间增设进士科（约605年），科举制度由此开创。"
        "这是中国选官制度由门第推荐转向公开考试的关键制度变革节点。",
        f"古代史料：《隋书·高祖纪》《炀帝纪》；现代参考：{MODERN['suitang']}",
        W["suishu"],
        [],
        review_note="废九品中正（约581—587）与设进士科（约605）为渐进过程，取 range 表述；\"科举始隋炀帝设进士科\"为通行说法。"),
    _ev("event-sui-dasuo-miaoyue", "大索貌阅、输籍定样", "reform",
        585, 585, "year", "period-sui", "major",
        "开皇五年（585年）隋文帝令\"大索貌阅\"（按貌核实户籍、清理隐漏人丁），"
        "并推行\"输籍定样\"（定户等输纳标准）。此举大量检括隐户为编户，"
        "国家户籍与赋役基础显著扩大，是开皇年间经济整顿的关键政策。",
        f"古代史料：《隋书·食货志》《高祖纪》；现代参考：{MODERN['suitang']}",
        W["suishu"],
        [],
        review_note="大索貌阅在开皇五年（585）；输籍定样为配套措施。"),
    _ev("event-kaihuang-zhizhi", "开皇之治", "political",
        581, 604, "range", "period-sui", "major",
        "隋文帝在位（581—604年）期间，统一南北、轻徭薄赋、澄清吏治，"
        "府库充实、户口倍增，史称\"开皇之治\"（属后世概括）。"
        "开皇时期的经济恢复与制度创设为隋唐盛世奠定基础。",
        f"古代史料：《隋书·高祖纪》；现代参考：{MODERN['suitang']}",
        W["suishu"],
        [_rel("event-yangjian-dai-beizhou", "follows", desc="开皇之治承接隋朝建立"),
         _rel("event-sui-fei-tai-zi-yong", "precedes", desc="开皇后期废太子引发继承危机")],
        review_note="\"开皇之治\"为后世对隋文帝在位期治世的概括，作 process 节点（同\"贞观之治\"处理）。"),
    _ev("event-sui-fei-tai-zi-yong", "隋文帝废太子杨勇", "political",
        600, 600, "year", "period-sui", "major",
        "开皇二十年（600年）隋文帝废太子杨勇，改立次子杨广为太子。"
        "废立出于晋王杨广与其党羽的构陷与文帝皇后独孤氏的推动，"
        "使皇位继承转向杨广，为日后炀帝暴政与隋亡埋下伏笔。",
        f"古代史料：《隋书·文四子传》《炀帝纪》；现代参考：{MODERN['suitang']}",
        W["suishu"],
        [_rel("event-yangguang-jiwei", "leads_to", 0.85, desc="废勇立广后，杨广于604年即位")],
        review_note="废太子杨勇在开皇二十年（600）；杨广夺嫡过程（欺父瞒母）见《隋书》。"),
    _ev("event-yangguang-jiwei", "杨广即位", "political",
        604, 604, "year", "period-sui", "major",
        "仁寿四年（604年）隋文帝病逝（有被弑之传说，史存歧见），"
        "太子杨广即位，是为隋炀帝。炀帝即位后大兴工程、频征高句丽，"
        "成为隋朝由盛转衰的关键转折。",
        f"古代史料：《隋书·炀帝纪》《高祖纪》；现代参考：{MODERN['suitang']}",
        W["suishu"],
        [_rel("event-sui-fei-tai-zi-yong", "follows"),
         _rel("event-yingjian-dongdu", "leads_to", 0.8, desc="炀帝即位后即营建东都")],
        review_note="仁寿四年（604）七月文帝崩、杨广即位；\"文帝被弑\"为《大业略记》等记载与史家争议（§49 以歧见记录）。"),
    _ev("event-yingjian-dongdu", "营建东都洛阳", "foundation",
        605, 606, "range", "period-sui", "major",
        "大业元年（605年）隋炀帝下令营建东都洛阳，每月役夫二百万人，"
        "至606年三月基本建成。洛阳由此成为隋唐两朝的重要政治中心之一，"
        "与长安并称两京。",
        f"古代史料：《隋书·炀帝纪》；现代参考：{MODERN['suitang']}",
        W["suishu"],
        [_rel("event-yangguang-jiwei", "follows"),
         _rel("event-dayunhe-kaiwa", "precedes", desc="营建东都与大运河工程同期展开")],
        review_note="营建东都洛阳（605—606）役夫规模与工期见《隋书》；\"每月役丁二百万\"为传统记载。"),
    _ev("event-dayunhe-kaiwa", "开凿大运河", "economic",
        605, 610, "range", "period-sui", "major",
        "大业元年至四年（605—610年）隋炀帝先后修凿通济渠、邗沟，"
        "疏浚永济渠，又开江南河，连接涿郡（今北京）与余杭（今杭州），"
        "形成以洛阳为中心、贯通南北的运河体系。大运河是隋代最大的交通工程，"
        "为南北经济文化交流与中央政府控制江南提供动脉（本事件按工程阶段记 range，非单日建成）。",
        f"古代史料：《隋书·炀帝纪》《食货志》；现代参考：{MODERN['suitang']}",
        W["suishu"],
        [_rel("event-yingjian-dongdu", "follows", desc="与营建东都同为炀帝前期大工程")],
        review_note="大运河系分期开凿（605 通济渠/邗沟、608 永济渠、610 江南河），取 range 不简化为单日事件（§8）；工程役夫伤亡惨重见《隋书》。"),
    _ev("event-sui-zheng-tuyuhun", "隋征吐谷浑", "war",
        609, 609, "year", "period-sui", "major",
        "大业五年（609年）隋炀帝亲征吐谷浑，破其国，"
        "置西海（今青海）等四郡，将今青海东部纳入隋朝版图。"
        "隋对吐谷浑的征服打通了通往西域的河西道路。",
        f"古代史料：《隋书·炀帝纪》；现代参考：{MODERN['suitang']}",
        W["suishu"],
        [_rel("event-dayunhe-kaiwa", "precedes", desc="炀帝前期西征与工程并举")],
        review_note="隋征吐谷浑在大业五年（609）；置西海河源等郡。"),
    _ev("event-sui-zheng-gaogouli", "隋征高句丽", "war",
        612, 614, "range", "period-sui", "major",
        "大业八年至十年（612—614年）隋炀帝三次大规模征伐高句丽："
        "首役百万大军渡辽水大败于萨水，二役因杨玄感起兵而还，"
        "三役高句丽求和。三征消耗空前的人力财力，直接激化隋末社会矛盾。",
        f"古代史料：《隋书·炀帝纪》《高丽传》；现代参考：{MODERN['suitang']}",
        W["suishu"],
        [_rel("event-sui-zheng-g1", "part_of", 0.9, desc="第一次征高句丽"),
         _rel("event-sui-zheng-g2", "part_of", 0.9, desc="第二次征高句丽"),
         _rel("event-sui-zheng-g3", "part_of", 0.9, desc="第三次征高句丽")],
        review_note="隋征高句丽（612—614）为 aggregate；隋军死亡枕籍（\"高丽未成而尸骸满路\"）为史载。"),
    _ev("event-sui-zheng-g1", "第一次征高句丽", "war",
        612, 612, "year", "period-sui", "major",
        "大业八年（612年）隋炀帝发军一百一十三万（号称二百万）攻高句丽，"
        "远征军渡辽水围攻辽东城不克，主力东渡鸭绿江在萨水（清川江）大败，"
        "约三十万军几全没。首次征伐以惨败告终。",
        f"古代史料：《隋书·炀帝纪》；现代参考：{MODERN['suitang']}",
        W["suishu"],
        [_rel("event-sui-zheng-gaogouli", "part_of", 0.95, desc="隋征高句丽第一次（萨水之败）")],
        review_note="首役在大业八年（612）；\"三十万九千\"归者仅二千七百等数字见《隋书》系年记载，或存夸饰。"),
    _ev("event-sui-zheng-g2", "第二次征高句丽", "war",
        613, 613, "year", "period-sui", "major",
        "大业九年（613年）隋炀帝再度亲征高句丽，围辽东城；"
        "六月礼部尚书杨玄感于黎阳（今河南浚县）起兵攻洛阳，"
        "炀帝闻讯回师，撤围内平，二次征伐无功而返。",
        f"古代史料：《隋书·炀帝纪》《杨玄感传》；现代参考：{MODERN['suitang']}",
        W["suishu"],
        [_rel("event-sui-zheng-gaogouli", "part_of", 0.95, desc="隋征高句丽第二次（杨玄感之乱中断）")],
        review_note="二役在大业九年（613）；杨玄感起兵（黎阳）为隋末统治动摇之始。"),
    _ev("event-sui-zheng-g3", "第三次征高句丽", "war",
        614, 614, "year", "period-sui", "major",
        "大业十年（614年）隋炀帝三度征兵攻高句丽，各地民变纷起、军粮不继，"
        "高句丽请降，隋军班师。三征高句丽基本无果，隋朝国力民力耗尽，"
        "全国性起义随即全面爆发。",
        f"古代史料：《隋书·炀帝纪》；现代参考：{MODERN['suitang']}",
        W["suishu"],
        [_rel("event-sui-zheng-gaogouli", "part_of", 0.95, desc="隋征高句丽第三次（无果而终）")],
        review_note="三役在大业十年（614）；炀帝复欲四征为群臣所谏止，隋政随之崩解。"),
    _ev("event-yangxuanggan-qibing", "杨玄感起兵", "rebellion",
        613, 613, "year", "period-sui", "major",
        "大业九年（613年）礼部尚书杨玄感趁炀帝二次征高而为留守（东都），"
        "在黎阳起兵反隋，攻洛阳不克，为宇文述等讨平被杀。"
        "杨玄感是隋代贵族中第一个起兵反炀帝者，其败亡标志隋朝统治危机的公开化。",
        f"古代史料：《隋书·杨玄感传》；现代参考：{MODERN['suitang']}",
        W["suishu"],
        [_rel("event-sui-zheng-g2", "follows", desc="杨玄感之乱直接中断二征"),
         _rel("event-wagang-jun-jueqi", "leads_to", 0.7, desc="其后天下溃乱，瓦岗等民变并起")],
        review_note="杨玄感起兵在大业九年（613）六至八月；\"杨玄感之乱\"为隋末贵族反隋首例。"),
    _ev("event-wagang-jun-jueqi", "瓦岗军崛起", "rebellion",
        616, 618, "range", "period-sui", "major",
        "大业十二年（616年）瓦岗军（翟让所创，东郡瓦岗寨）在李密领导下壮大，"
        "克兴洛仓、开仓济民，据有河南大部，成为隋末最强的民变武装之一。"
        "瓦岗军与洛阳隋军长期拉锯，618年李密为王世充所败，瓦岗瓦解。",
        f"古代史料：《隋书·李密传》《资治通鉴·隋纪》；现代参考：{MODERN['suitang']}",
        W["suishu_tang"],
        [_rel("event-yangxuanggan-qibing", "follows"),
         _rel("event-jiangdu-bingbian", "precedes", desc="瓦岗等民变与江都兵变共同终结隋运")],
        review_note="瓦岗军崛起（616—618）为过程；李密\"瓦岗\"之名另说因瓦岗寨得名。"),
    _ev("event-doujiande-shili", "窦建德据河北", "rebellion",
        616, 618, "range", "period-sui", "major",
        "窦建德自大业末年起兵河北，616年称长乐王，617年据乐寿、建都，"
        "618年改称夏王，据有今河北大部。窦建德是隋末北方最重要的民变首领之一，"
        "其势力与李渊、王世充鼎足而三。",
        f"古代史料：《旧唐书·窦建德传》；现代参考：{MODERN['suitang']}",
        W["jiutang"],
        [_rel("event-wagang-jun-jueqi", "precedes", desc="河北与河南民变并立"),
         _rel("event-hulao-zhizhan", "precedes", desc="窦建德最终败亡于虎牢之战")],
        review_note="窦建德势力（616—618为形成期，至621年虎牢败亡）为过程事件。"),
    _ev("event-dufuwei-shili", "杜伏威据江淮", "rebellion",
        616, 619, "range", "period-sui", "major",
        "大业年间杜伏威、辅公祏在江淮地区起义，616年前后据历阳（今安徽和县），"
        "占据江淮要地，618年降唐。杜伏威势力是隋末控制长江中下游的重要武装。",
        f"古代史料：《旧唐书·杜伏威传》；现代参考：{MODERN['suitang']}",
        W["jiutang"],
        [_rel("event-jiangdu-bingbian", "precedes", desc="杜伏威据江淮与隋亡相先后")],
        review_note="杜伏威据江淮（约616—619）为过程事件；其地跨江都一带，与炀帝滞留江都相影响。"),
    _ev("event-liyuan-qibing", "李渊太原起兵", "rebellion",
        617, 617, "year", "period-sui", "major",
        "大业十三年（617年）五月，太原留守李渊在次子李世民等策划下，"
        "于晋阳（今太原）起兵反隋，\"废昏立明\"号召讨平天下；"
        "七月率军三万西进，直取关中。李渊太原起兵是隋末群雄中最终胜出的起点。",
        f"古代史料：《旧唐书·高祖纪》；现代参考：{MODERN['suitang']}",
        W["jiutang_zizhi"],
        [_rel("event-wagang-jun-jueqi", "precedes", desc="隋末大乱中李渊起兵"),
         _rel("event-liyuan-ru-guan", "leads_to", 0.9, desc="太原起兵后李渊西进夺长安")],
        review_note="李渊太原起兵在大业十三年（617）五月；\"举义兵\"号召以尊隋立嫡为名。"),
    _ev("event-liyuan-ru-guan", "李渊攻占长安（杨侑即位）", "war",
        617, 617, "year", "period-sui", "major",
        "大业十三年（617年）十一月，李渊军攻占长安，立隋代王杨侑为帝（恭帝），"
        "遥尊隋炀帝为太上皇，自任大丞相、唐王。长安的攻占使李渊取得\"挟天子\"名分"
        "与关中根基，为建立唐朝铺平道路。",
        f"古代史料：《旧唐书·高祖纪》；现代参考：{MODERN['suitang']}",
        W["jiutang"],
        [_rel("event-liyuan-qibing", "follows"),
         _rel("event-tang-jianguo", "leads_to", 0.9, desc="定都长安后李渊于次年称帝建唐")],
        review_note="李渊攻长安在617年十一月、立恭帝杨侑；遥尊炀帝为\"太上皇\"。"),
    _ev("event-jiangdu-bingbian", "江都兵变、隋炀帝被杀", "political",
        618, 618, "year", "period-sui", "major",
        "大业十四年（618年）三月，炀帝滞留扬州江都（今扬州），"
        "骁果军将领宇文化及等发动兵变，缢杀隋炀帝。"
        "炀帝之死标志隋朝实质灭亡（此前李渊已控制长安并挟有恭帝）。",
        f"古代史料：《隋书·炀帝纪》；现代参考：{MODERN['suitang']}",
        W["suishu"],
        [_rel("event-wagang-jun-jueqi", "follows"),
         _rel("event-tang-jianguo", "leads_to", 0.8, desc="隋炀帝死、隋运已终，李渊在长安称帝建唐")],
        review_note="江都兵变在618年三月（大业十四年）；宇文化及弑炀帝。\"隋朝实质灭亡\"为同一节点之 outcome。"),
]

# ---------------------------------------------------------------------------
# Phase 2 — 初唐（618–683）
# ---------------------------------------------------------------------------
PHASE_EARLY_TANG = [
    _ev("event-tang-jianguo", "李渊称帝、唐朝建立", "dynastic-transition",
        618, 618, "year", "period-tang", "critical",
        "武德元年（618年）五月，李渊在长安称帝，国号唐，隋恭帝禅让，"
        "隋朝正式灭亡。唐朝建立继隋之后开启中国历史上又一个强盛王朝，"
        "并迅速展开统一全国的战争。",
        f"古代史料：《旧唐书·高祖纪》；现代参考：{MODERN['tang']}",
        W["jiutang_zizhi"],
        ["regime-tang"],
        [_rel("event-jiangdu-bingbian", "follows", desc="隋炀帝死后李渊称帝建唐"),
         _rel("event-liyuan-ru-guan", "follows")],
        review_note="李渊618年五月受禅称帝（武德元年）；\"唐朝建立\"与\"李渊称帝\"为同一节点（§48 粒度判断）。"),
    _ev("event-tang-mie-xueju", "唐灭薛举、薛仁杲", "war",
        618, 619, "range", "period-tang", "major",
        "武德元年（618年）西秦薛举在浅水原大败唐军后病卒，"
        "继位者薛仁杲于619年（武德二年）为李世民所灭，唐据陇右。"
        "薛氏之灭平定关中侧翼，是唐统一战争的第一场大捷。",
        f"古代史料：《旧唐书·高祖纪》《薛举传》；现代参考：{MODERN['tang']}",
        W["jiutang"],
        ["regime-tang"],
        [_rel("event-tang-jianguo", "follows"),
         _rel("event-hulao-zhizhan", "leads_to", 0.8, desc="经略陇右、山西后，李世民东出决战虎牢")],
        review_note="唐灭薛举（618—619）：浅水原之战（618败）与薛仁杲降唐（619，浅水原再战大捷）合为一过程节点。"),
    _ev("event-hulao-zhizhan", "虎牢之战", "war",
        620, 621, "range", "period-tang", "major",
        "武德三年至四年（620—621年），秦王李世民率军围洛阳王世充，"
        "621年四月于虎牢（今河南荥阳）大破来援的窦建德夏军，"
        "窦建德被俘、王世充出降。虎牢之战一举定河南河北，"
        "是李唐统一全国的关键会战。",
        f"古代史料：《旧唐书·太宗纪》《窦建德传》；现代参考：{MODERN['tang']}",
        W["jiutang_zizhi"],
        ["regime-tang"],
        [_rel("event-tang-mie-xueju", "follows"),
         _rel("event-tang-tongyi-quanguo", "leads_to", 0.9, desc="虎牢大捷后河北河南底定，唐完成统一")],
        review_note="虎牢之战（620—621）为\"一役定两强\"（窦建德、王世充）；窦建德败亡、王世充降唐为其 outcome（§48 行动+outcome 合一，未分设）。"),
    _ev("event-tang-tongyi-quanguo", "唐统一全国", "war",
        618, 628, "range", "period-tang", "major",
        "武德至贞观初（约618—628年），唐朝先后平定薛举、刘武周、"
        "窦建德（及余部刘黑闼）、王世充、辅公祏等割据势力，"
        "628年灭梁师都，基本完成全国统一。唐在隋末群雄混战的废墟上重建大一统。",
        f"古代史料：《旧唐书·高祖纪》《太宗纪》；现代参考：{MODERN['tang']}",
        W["jiutang_zizhi"],
        ["regime-tang"],
        [_rel("event-hulao-zhizhan", "follows"),
         _rel("event-xuanwumen-zhibian", "precedes", desc="统一战争后期发生玄武门之变")],
        review_note="唐统一全国（618—628）为 process 事件；末次平梁师都在贞观二年（628）。"),
    _ev("event-weishui-zhi-meng", "渭水之盟", "alliance",
        626, 626, "year", "period-tang", "major",
        "武德九年（626年）突厥颉利可汗趁唐政权交接之际率军进至渭水便桥，"
        "威逼长安；李世民刚即位，亲临渭水与颉利会盟（\"便桥之盟\"），"
        "厚赠财物约和退兵。渭水之盟暂缓突厥威胁，唐代以此为耻，"
        "励精图治备战，为四年后灭东突厥张本。",
        f"古代史料：《旧唐书·突厥传》《资治通鉴·唐纪》；现代参考：{MODERN['tang']}",
        W["jiutang_zizhi"],
        ["regime-tang"],
        [_rel("event-li-shimin-jiwei", "follows", desc="李世民即位后与突厥订盟"),
         _rel("event-tang-mie-dong-tujue", "leads_to", 0.8, desc="渭水之盟后唐积极备战，终灭东突厥")],
        review_note="渭水之盟在626年八月（武德九年）；\"便桥会盟\"为唐代记耻之节点，太宗自谓\"渭水之恥\"。"),
    _ev("event-xuanwumen-zhibian", "玄武门之变", "political",
        626, 626, "year", "period-tang", "critical",
        "武德九年（626年）六月初四，秦王李世民在长安宫城北门玄武门伏兵，"
        "杀太子李建成、齐王李元吉，遂被立为太子，两月后受禅即位。"
        "玄武门之变是唐初皇位继承冲突的总爆发，改变了唐朝政治走向，"
        "也是中国历史上最著名的宫廷政变之一（§12：政变与即位分列）。",
        f"古代史料：《旧唐书·太宗纪》《高祖纪》；现代参考：{MODERN['tang']}",
        W["jiutang_zizhi"],
        ["regime-tang"],
        [_rel("event-li-shimin-jiwei", "leads_to", 0.95, desc="政变后李世民被册为太子并即位")],
        review_note="玄武门之变在626年六月庚申（武德九年）；\"玄武门\"为宫城北门。政治政变与皇权交接收回分为两个 Event（§12）。"),
    _ev("event-li-shimin-jiwei", "李世民即位", "political",
        626, 626, "year", "period-tang", "major",
        "武德九年（626年）八月，李渊禅位，李世民即位，次年改元贞观。"
        "李世民（唐太宗）即位开启\"贞观之治\"，并成为唐对外扩张与制度成熟的核心推动者。",
        f"古代史料：《旧唐书·太宗纪》；现代参考：{MODERN['tang']}",
        W["jiutang"],
        ["regime-tang"],
        [_rel("event-xuanwumen-zhibian", "follows", desc="玄武门之变后太宗即帝位"),
         _rel("event-zhenguan-zhizhi", "leads_to", 0.85, desc="贞观年间天下大治（贞观之治）")],
        review_note="李世民626年八月受禅（武德九年）；贞观元年为627年。"),
    _ev("event-zhenguan-zhizhi", "贞观之治", "political",
        627, 649, "range", "period-tang", "major",
        "唐太宗贞观年间（627—649年）轻徭薄赋、任用贤能（房玄龄、杜如晦等）、"
        "虚心纳谏（魏徵），政治清明、社会安定，史称\"贞观之治\"（属后世概括）。"
        "贞观时期同时完成对东突厥、西域的经营，是唐朝强盛的第一个高峰期。",
        f"古代史料：《旧唐书·太宗纪》《资治通鉴·唐纪》；现代参考：{MODERN['tang']}",
        W["jiutang_zizhi"],
        ["regime-tang"],
        [_rel("event-li-shimin-jiwei", "follows"),
         _rel("event-tang-mie-dong-tujue", "precedes", desc="贞观对外扩张以灭东突厥为标志")],
        review_note="\"贞观之治\"为后世对太宗在位期治世的概括（historiographical summary，§49），作 process 节点，具体政策与战役见各子节点。"),
    _ev("event-tang-mie-dong-tujue", "唐灭东突厥", "war",
        630, 630, "year", "period-tang", "critical",
        "贞观四年（630年）唐将李靖率军长途奔袭，"
        "在阴山击破东突厥主力，颉利可汗被俘，东突厥汗国灭亡。"
        "唐灭东突厥解除北方最大边患，太宗被尊\"天可汗\"，"
        "西域诸国与回纥等皆奉大唐为盟主，是唐初对外战略的决定性胜利。",
        f"古代史料：《旧唐书·李靖传》《突厥传》；现代参考：{MODERN['tang']}",
        W["jiutang_zizhi"],
        ["regime-tang"],
        [_rel("event-weishui-zhi-meng", "follows", desc="渭水之盟后励精图治、四年灭东突厥"),
         _rel("event-tang-ping-gaochang-ansixi", "leads_to", 0.8, desc="灭东突厥后唐向西经营西域（安西都护府）")],
        review_note="灭东突厥在630年（贞观四年）三月；李靖夜袭阴山获捷。\"天可汗\"为称号/概念，不立 Event（§14）。"),
    _ev("event-tang-ping-gaochang-ansixi", "唐灭高昌、设安西都护府", "war",
        640, 640, "year", "period-tang", "major",
        "贞观十四年（640年）唐军灭高昌国（今新疆吐鲁番一带），"
        "以其地设西州、置安西都护府，唐的行政统治正式进入西域。"
        "安西都护府的设置是唐朝经营西域、巩固丝绸之路的战略支点。",
        f"古代史料：《旧唐书·太宗纪》《西戎传》；现代参考：{MODERN['tang']}",
        W["jiutang_zizhi"],
        ["regime-tang"],
        [_rel("event-tang-mie-dong-tujue", "follows"),
         _rel("event-tang-ping-qiuzi-sizhen", "leads_to", 0.8, desc="设安西都护府后继续西进（龟兹等）")],
        review_note="灭高昌（640）+设安西都护府为同一行动的两个环节，合一节点；阿史那社尔后平焉耆、龟兹（648）。"),
    _ev("event-tang-ping-qiuzi-sizhen", "唐灭龟兹、安西四镇格局形成", "war",
        648, 648, "year", "period-tang", "major",
        "贞观二十二年（648年）唐将阿史那社尔平龟兹，"
        "以龟兹、疏勒、于阗、焉耆（后改碎叶）为安西四镇，"
        "唐朝对西域的控制达到空前程度，丝绸之路南北道皆通。",
        f"古代史料：《旧唐书·西戎传》；现代参考：{MODERN['tang']}",
        W["jiutang_zizhi"],
        ["regime-tang"],
        [_rel("event-tang-ping-gaochang-ansixi", "follows"),
         _rel("event-tang-zheng-gaogouli", "precedes", desc="太宗末年同时经营西域与东征高句丽")],
        review_note="安西四镇布局在648年（贞观二十二年）前后；四镇组成在不同时期有调整（碎叶镇系后来移置）。"),
    _ev("event-tang-zheng-gaogouli", "唐太宗征高句丽", "war",
        645, 645, "year", "period-tang", "major",
        "贞观十九年（645年）唐太宗亲征高句丽，克辽东数城，"
        "围攻安市城不克，深秋班师，\"辽东之役\"终以未灭高句丽而返。"
        "此役震慑高句丽，为其后高宗朝最终灭高句丽（668）奠定基础。",
        f"古代史料：《旧唐书·太宗纪》《高丽传》；现代参考：{MODERN['tang']}",
        W["jiutang_zizhi"],
        ["regime-tang"],
        [_rel("event-tang-ping-qiuzi-sizhen", "precedes"),
         _rel("event-tang-mie-gaogouli", "leads_to", 0.7, desc="太宗征高句丽未成，高宗朝终灭之")],
        review_note="太宗亲征高句丽在645年（贞观十九年）；取安市城不克（延寿惠真之战则捷）。"),
]

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Phase 3 — 高宗/武周（649–705）
# ---------------------------------------------------------------------------
PHASE_GAOZONG_WUZHOU = [
    _ev("event-tang-gaozong-jiwei", "唐高宗即位", "political",
        649, 649, "year", "period-tang", "major",
        "贞观二十三年（649年）唐太宗去世，太子李治即位，是为唐高宗。"
        "高宗初期承贞观遗风（永徽之治），中期以后皇后武氏（武则天）权力上升，"
        "唐朝政治进入高宗—武周过渡阶段。",
        f"古代史料：《旧唐书·高宗纪》；现代参考：{MODERN['tang']}",
        W["jiutang"],
        ["regime-tang"],
        [_rel("event-tang-zheng-gaogouli", "precedes", desc="高宗承太宗基业即位"),
         _rel("event-gaozong-feiwang-liwu", "leads_to", 0.8, desc="高宗朝武氏地位上升，废王立武")],
        review_note="高宗即位于649年（贞观二十三年）；永徽年间为高宗前期。"),
    _ev("event-gaozong-feiwang-liwu", "高宗废王立武、长孙无忌失势", "political",
        655, 659, "range", "period-tang", "major",
        "永徽六年（655年）高宗废皇后王氏、立武昭仪为后（「废王立武」），"
        "次年改元显庆；659年长孙无忌被逐贬自杀，关陇士族集团势力受挫。"
        "此事件标志着武则天进入权力核心，也改变了唐初的朝局结构。",
        f"古代史料：《旧唐书·高宗纪》《长孙无忌传》；现代参考：{MODERN['tang']}",
        W["jiutang_zizhi"],
        ["regime-tang"],
        [_rel("event-tang-gaozong-jiwei", "follows"),
         _rel("event-tang-mie-xi-tujue", "precedes", desc="武后干政背景下的对外战争仍由高宗朝主导")],
        review_note="废王立武在永徽六年（655）；长孙无忌于显庆四年（659）被贬而死。「关陇集团」问题为陈寅恪《唐代政治史述论稿》所论。"),
    _ev("event-tang-mie-xi-tujue", "唐灭西突厥", "war",
        657, 657, "year", "period-tang", "major",
        "显庆二年（657年）唐将苏定方率军大破西突厥沙钵罗可汗，"
        "西突厥汗国灭亡，唐朝对西域的控制达到新的高度，"
        "安西、北庭两大都护逐步成形。",
        f"古代史料：《旧唐书·西突厥传》；现代参考：{MODERN['tang']}",
        W["jiutang_zizhi"],
        ["regime-tang"],
        [_rel("event-tang-ping-qiuzi-sizhen", "follows", desc="初二征对西域经营之延续"),
         _rel("event-tang-mie-gaogouli", "precedes")],
        review_note="灭西突厥在657年（显庆二年）冬；苏定方「分军乱其牙帐」。"),
    _ev("event-tang-mie-gaogouli", "唐灭高句丽", "war",
        668, 668, "year", "period-tang", "major",
        "总章元年（668年）唐将薛仁贵等攻平壤，高句丽灭亡，"
        "唐置安东都护府。自隋炀帝至唐太宗、高宗三代征伐，高句丽终为唐所灭，"
        "朝鲜半岛格局由此重定（后新罗统一半岛南部）。",
        f"古代史料：《旧唐书·高宗纪》《高丽传》；现代参考：{MODERN['tang']}",
        W["jiutang_zizhi"],
        ["regime-tang"],
        [_rel("event-tang-zheng-gaogouli", "follows", desc="继太宗亲征之后高宗朝灭高句丽"),
         _rel("event-baijiangkou-zhizhan", "precedes", desc="白江口之战（663）先行斩断日本援军")],
        review_note="灭高句丽在668年（总章元年）；白江口之战（663）已先破百济—日本联军。"),
    _ev("event-baijiangkou-zhizhan", "白江口之战", "war",
        663, 663, "year", "period-tang", "major",
        "龙朔三年（663年）唐将刘仁轨在白江口（今韩国锦江入海口）"
        "大破援助百济的日本水军，焚船四百余艘。此役确立唐对朝鲜半岛南部的控制，"
        "日本从此数百年间不再设登陆朝鲜半岛之志。",
        f"古代史料：《旧唐书·刘仁轨传》《日本书纪》等；现代参考：{MODERN['tang']}",
        W["jiutang_zizhi"],
        ["regime-tang"],
        [_rel("event-tang-mie-gaogouli", "follows", desc="白江口之胜为灭高句丽之辅"),
         _rel("event-dafeichuan-zhizhan", "precedes")],
        review_note="白江口之战在663年（龙朔三年）四至八月；日方记载（《日本书纪》）与唐方记载可互证。"),
    _ev("event-dafeichuan-zhizhan", "大非川之战", "war",
        670, 670, "year", "period-tang", "major",
        "咸亨元年（670年）唐将薛仁贵率军与吐蕃在大非川（今青海共和一带）决战，"
        "唐军大败。此役标志吐蕃在青藏高原崛起并对唐形成长期战略压力，"
        "唐蕃关系由和亲转入战争与反复争夺的格局。",
        f"古代史料：《旧唐书·薛仁贵传》《吐蕃传》；现代参考：{MODERN['tang']}",
        W["jiutang_zizhi"],
        ["regime-tang"],
        [_rel("event-tang-mie-gaogouli", "precedes", desc="唐对外战线由东转向西部吐蕃"),
         _rel("event-wu-zhao-linchao", "precedes", desc="唐蕃冲突贯穿高宗后期与武周")],
        review_note="大非川之战在670年（咸亨元年）；薛仁贵大非川之败为唐前期少有的大败仗之一（与「安西四镇」争持相关）。"),
    _ev("event-wu-zhao-linchao", "武则天临朝称制", "political",
        683, 690, "range", "period-tang", "major",
        "弘道元年（683年）高宗去世，中宗即位未二月被废，睿宗立为傀儡；"
        "武则天以太后身份临朝称制，684年改元垂拱，杀裴炎、废诸王。"
        "武则天临朝七年（683—690），实为武周代唐的前奏。",
        f"古代史料：《旧唐书·则天皇后纪》；现代参考：{MODERN['tang']}",
        W["jiutang_zizhi"],
        ["regime-tang"],
        [_rel("event-dafeichuan-zhizhan", "precedes"),
         _rel("event-wu-zhou-jianguo", "leads_to", 0.9, desc="临朝称制后武则天正式称帝建周")],
        review_note="临朝称制（683—690）跨越中宗/睿宗/武后三阶段；「废中宗、立睿宗」（684）为其间标志。"),
    _ev("event-wu-zhou-jianguo", "武则天称帝、武周建立", "dynastic-transition",
        690, 690, "year", "period-tang", "critical",
        "天授元年（690年）武则天废睿宗、自称皇帝，改国号为周（武周），"
        "迁都洛阳为神都。武则天是中国历史上唯一正式称帝的女皇帝；"
        "武周政权的建立使唐代政治出现二十余年的女性执政的特殊时期（§17："
        "独立 Regime regime-wu-zhou，Period 仍属唐）。",
        f"古代史料：《旧唐书·则天皇后纪》；现代参考：{MODERN['tang']}",
        W["jiutang_zizhi"],
        ["regime-wu-zhou"],
        [_rel("event-wu-zhao-linchao", "follows", desc="临朝称制后称帝建周"),
         _rel("event-shenlong-zhengbian", "leads_to", 0.9, desc="武周统治十五年后被神龙政变终结")],
        review_note="武则天称帝在天授元年（690）九月；国号周（武周），史界以「武周」别于周代。"),
    _ev("event-wu-zhou-zhidu", "武周政治制度变革（洛阳为神都、改制选官）", "reform",
        690, 700, "range", "period-tang", "major",
        "武周时期推行多项制度变革：以洛阳为神都、改造都城体系，"
        "开殿试、武举选拔，改革官名与朝章（改尚书省为中台等）。"
        "武周之制兼顾关东门第与科举新士人，为盛唐政治制度的重要过渡。",
        f"古代史料：《旧唐书·则天皇后纪》；现代参考：{MODERN['tang']}",
        W["jiutang"],
        ["regime-wu-zhou"],
        [_rel("event-wu-zhou-jianguo", "follows", desc="建周后推行制度改革"),
         _rel("event-shenlong-zhengbian", "precedes")],
        review_note="武周制度改革（690—700前后）为过程；「神都」改用、殿试武举等见《旧唐书》。§16 武周政治改革节点。"),
    _ev("event-shenlong-zhengbian", "神龙政变、唐中宗复位", "political",
        705, 705, "year", "period-tang", "critical",
        "神龙元年（705年）正月张柬之、崔玄暐等发动政变，迫武则天退位，"
        "中宗李显复位，复国号唐。武周政权终结，武则天不久病逝。"
        "神龙政变是唐朝恢复的关键政治事件，武周时期由此落幕。",
        f"古代史料：《旧唐书·则天皇后纪》；现代参考：{MODERN['tang']}",
        W["jiutang_zizhi"],
        ["regime-wu-zhou"],
        [_rel("event-wu-zhou-jianguo", "follows", desc="武周统治被政变终结"),
         _rel("event-tang-long-zhengbian", "leads_to", 0.8, desc="中宗复位后韦后乱政，旋有唐隆政变")],
        review_note="神龙政变在705年正月（神龙元年）；政变与「中宗复位」合一节点（§48：政变+复位为行动与 outcome）。"),
]

# ---------------------------------------------------------------------------
# Phase 4 — 开元/天宝/安史（710–763；安史 9 Event 复用）
# ---------------------------------------------------------------------------
PHASE_XUANZONG_ANLU = [
    _ev("event-tang-long-zhengbian", "唐隆政变", "political",
        710, 710, "year", "period-tang", "major",
        "景龙四年（710年）韦后毒死中宗、临朝称制；"
        "临淄王李隆基与太平公主合谋发动政变（「唐隆政变」），"
        "诛韦后与安乐公主，拥立睿宗复位。李隆基自此登上权力中心。",
        f"古代史料：《旧唐书·玄宗纪》；现代参考：{MODERN['tang']}",
        W["jiutang"],
        ["regime-tang"],
        [_rel("event-shenlong-zhengbian", "follows", desc="中宗复位后韦氏之乱引发唐隆政变"),
         _rel("event-xuanzong-jiwei", "leads_to", 0.85, desc="睿宗复位、李隆基被立为太子继而即位")],
        review_note="唐隆政变在710年（景龙四年/唐隆元年）六月；「唐隆」为李隆基拥立睿宗后年号。"),
    _ev("event-xuanzong-jiwei", "唐玄宗即位", "political",
        712, 712, "year", "period-tang", "major",
        "延和元年（712年）睿宗内禅，李隆基即位，是为唐玄宗。"
        "玄宗即位之初与太平公主矛盾尖锐，次年先天政变后始独揽大权，"
        "随即开启开元盛世。",
        f"古代史料：《旧唐书·玄宗纪》；现代参考：{MODERN['tang']}",
        W["jiutang"],
        ["regime-tang"],
        [_rel("event-tang-long-zhengbian", "follows"),
         _rel("event-xiantian-zhengbian", "leads_to", 0.85, desc="即位后清除太平公主势力")],
        review_note="玄宗即位于712年（先天元年），睿宗内禅；开元元年为713年。"),
    _ev("event-xiantian-zhengbian", "先天政变（玄宗掌权）", "political",
        713, 713, "year", "period-tang", "major",
        "开元元年（713年）玄宗诛太平公主党羽，太平公主赐死，"
        "武则天以来的宫廷政变周期结束，玄宗真正独揽朝政。"
        "先天政变为玄宗全面执政与开元盛世的真正开端。",
        f"古代史料：《旧唐书·玄宗纪》；现代参考：{MODERN['tang']}",
        W["jiutang"],
        ["regime-tang"],
        [_rel("event-xuanzong-jiwei", "follows", desc="执掌大权"),
         _rel("event-kaiyuan-zhizheng", "leads_to", 0.9, desc="掌权后励精图治，开开元之治")],
        review_note="先天政变（713年，先天二年/开元元年）诛太平公主；玄宗由此集权。"),
    _ev("event-kaiyuan-zhizheng", "开元前期政治整顿（姚崇宋璟执政）", "reform",
        713, 728, "range", "period-tang", "major",
        "开元前期（713—728年前后）玄宗先后任用姚崇、宋璟为相，"
        "罢冗官、修政事、抑豪强、移风易俗，政局清明。"
        "姚崇、宋璟并称（「姚宋」），为开元之治的主要宰辅。",
        f"古代史料：《旧唐书·姚崇宋璟传》《玄宗纪》；现代参考：{MODERN['tang']}",
        W["jiutang_zizhi"],
        ["regime-tang"],
        [_rel("event-xiantian-zhengbian", "follows"),
         _rel("event-kaiyuan-shengshi", "leads_to", 0.9, desc="姚宋整顿促成开元盛世")],
        review_note="姚崇执政（713—716/721前后）、宋璟继之（716年起），取 range 为过程节点。"),
    _ev("event-kaiyuan-shengshi", "开元盛世", "political",
        713, 741, "range", "period-tang", "major",
        "唐玄宗开元年间（713—741年）户口倍增、仓储充溢、海内晏然，"
        "文教武备皆极一时之盛，史称「开元盛世」（属后世概括）。"
        "开元盛世是唐朝以至于中国古代社会的繁盛高峰，其后期潜藏的政治军事弊端"
        "（府兵废弛、节度权重）渐次显现。",
        f"古代史料：《旧唐书·玄宗纪》《资治通鉴·唐纪》；现代参考：{MODERN['tang']}",
        W["jiutang_zizhi"],
        ["regime-tang"],
        [_rel("event-kaiyuan-zhizheng", "follows"),
         _rel("event-tianbao-li-linfu", "precedes", desc="开元末李林甫执政，天宝由盛转衰")],
        review_note="「开元盛世」为后世对开元年间治世的概括（historiographical summary，§49），作 process 节点，不伪装为单日事件。"),
    _ev("event-tianbao-li-linfu", "李林甫长期执政", "political",
        736, 752, "range", "period-tang", "major",
        "开元二十四年至天宝年间（约736—752年）李林甫任中书令长达十九年，"
        "「口有蜜，腹有剑」，专权自恣、杜绝言路、固结宠位。"
        "李林甫执政期间朝政走向腐败，玄宗晚年怠政，天宝政局由盛转衰的重要环节。",
        f"古代史料：《旧唐书·李林甫传》；现代参考：{MODERN['tang']}；黄永年《六至九世纪中国政治史》",
        W["jiutang"],
        ["regime-tang"],
        [_rel("event-kaiyuan-shengshi", "follows"),
         _rel("event-tianbao-yangguozhong", "leads_to", 0.85, desc="李林甫死后杨国忠继掌朝政")],
        review_note="李林甫为相（开元二十二年起约736年—天宝十一载752年卒）；「口蜜腹剑」为《资治通鉴》评语。"),
    _ev("event-tianbao-yangguozhong", "杨国忠执政", "political",
        752, 755, "range", "period-tang", "major",
        "天宝十一载（752年）李林甫卒后，杨贵妃从兄杨国忠继任宰相，"
        "兼领四十余使，聚敛横暴；755年与安禄山矛盾激化，"
        "成为安史之乱爆发的直接政治导火索之一。",
        f"古代史料：《旧唐书·杨国忠传》；现代参考：{MODERN['tang']}",
        W["jiutang"],
        ["regime-tang"],
        [_rel("event-tianbao-li-linfu", "follows"),
         _rel("event-anlu-uprising", "leads_to", 0.8, desc="杨国忠与安禄山交恶，促成安史之乱爆发")],
        review_note="杨国忠执政（752—755）为天宝末宰相；其与安禄山矛盾为安史之乱重要诱因。"),
    _ev("event-tang-mubing-zhuanxing", "府兵制瓦解与募兵制转变", "reform",
        722, 737, "range", "period-tang", "major",
        "府兵制至开元年间渐趋废弛，开元十年（722年）后募兵（「长征健儿」）"
        "渐成定制，国家军事力量由兵农合一之府兵转向职业募兵；"
        "同时缘边节度使集军、政、财权于一身。"
        "这一军事制度转变（§19 制度变化节点）为安史之乱与藩镇割据提供了制度条件。",
        f"古代史料：《唐会要》及《新唐书·兵志》；现代参考：{MODERN['tang']}；陈寅恪《隋唐制度渊源略论稿》",
        W["xintang"],
        ["regime-tang"],
        [_rel("event-kaiyuan-zhizheng", "follows"),
         _rel("event-anlu-three-frontiers", "leads_to", 0.7, desc="节度使权重扩张至安禄山兼领三镇")],
        review_note="府兵废弛与募兵制确立为渐进过程（约722—737年间）；节度使制度成熟为同一走向（制度节点，非概念立项）。"),
    _ev("event-suzong-jiwei", "唐肃宗灵武即位", "political",
        756, 756, "year", "period-tang", "major",
        "至德元年（756年）玄宗出逃入蜀途中，太子李亨在灵武（今宁夏灵武）即位，"
        "是为唐肃宗，遥尊玄宗为太上皇。肃宗即位重整平叛中枢，"
        "成为安史之乱中唐朝组织反攻的起点（衔接安史 Story 事件链）。",
        f"古代史料：《旧唐书·肃宗纪》；现代参考：{MODERN['tang']}",
        W["jiutang"],
        ["regime-tang"],
        [_rel("event-anlu-xuanzong-shu", "follows", desc="玄宗入蜀后太子灵武即位"),
         _rel("event-anlu-changan-recapture", "leads_to", 0.85, desc="肃宗组织平叛，收复两京")],
        review_note="肃宗灵武即位在756年（至德元年）七月；「灵武即位」为安史之乱中的权力重组节点（非重复建档，安史9 Event 原样复用）。"),
]

# ---------------------------------------------------------------------------
# Phase 5 — 中晚唐/唐末（763–904）
# ---------------------------------------------------------------------------
PHASE_LATE_TANG = [
    _ev("event-he-shuo-sanzhen", "河朔三镇割据格局形成", "political",
        763, 781, "range", "period-tang", "major",
        "安史之乱平定后（763年），唐廷以安史旧部田承嗣（魏博）、"
        "李宝臣（成德）、李怀仙（卢龙）为节度使，河朔三镇遂成「国中之国」，"
        "父子相袭、赋税自专。河朔三镇割据是藩镇格局的开端，"
        "也决定了唐中后期的政治基本盘。",
        f"古代史料：《旧唐书·田承嗣传》等藩镇诸传；现代参考：{MODERN['tang']}",
        W["jiutang"],
        ["regime-tang"],
        [_rel("event-anlu-pacification", "follows", desc="安史平定后河北藩镇化"),
         _rel("event-liangshui-fa", "precedes", desc="财政上以两税法面对藩镇分权")],
        review_note="河朔三镇格局（763—781为形成期）为 process 节点；「藩镇」问题的古今讨论见《旧唐书·藩镇传》。"),
    _ev("event-liangshui-fa", "两税法实施", "reform",
        780, 780, "year", "period-tang", "major",
        "建中元年（780年）宰相杨炎推行两税法："
        "以户税、地税取代租庸调，按资产与土地每年夏秋两征，"
        "「量出为入」。两税法是唐代财政制度的一次根本变革，"
        "自此中国赋税由人头税为主转向财产税为主，影响此后数百年。",
        f"古代史料：《旧唐书·杨炎传》《食货志》；现代参考：{MODERN['tang']}",
        W["jiutang_zizhi"],
        ["regime-tang"],
        [_rel("event-he-shuo-sanzhen", "follows"),
         _rel("event-jianzhong-zhi-luan", "precedes", desc="两税法推行与削藩并举（建中之乱）")],
        review_note="两税法颁行于建中元年（780）正月；杨炎「量出为入」思想见《杨炎传》。"),
    _ev("event-jianzhong-zhi-luan", "建中之乱（泾原兵变、奉天之难）", "rebellion",
        781, 784, "range", "period-tang", "major",
        "建中二年至兴元元年（781—784年）德宗削藩引发四镇连兵（朱滔、王武俊、"
        "田悦、李纳）与李希烈反叛，783年泾原兵变、朱泚据长安称帝（秦帝），"
        "德宗出逃奉天被围（「奉天之难」），784年发罪己诏、"
        "借李晟等收复长安。建中之乱使德宗削藩功败垂成，唐廷对藩镇转为姑息。",
        f"古代史料：《旧唐书·德宗纪》《朱泚传》；现代参考：{MODERN['tang']}",
        W["jiutang_zizhi"],
        ["regime-tang"],
        [_rel("event-liangshui-fa", "follows"),
         _rel("event-yongzhen-gexin", "precedes", desc="建中之乱后唐廷姑息藩镇，延续至顺宗永贞革新失败")],
        review_note="建中之乱（781—784）涵盖四镇之乱/泾原兵变/奉天之难/二帝之乱（朱泚、李希烈先后称帝），合一 process 事件；分段细节见 review。"),
    _ev("event-tubo-ru-changan", "吐蕃攻入长安", "war",
        763, 763, "year", "period-tang", "major",
        "广德元年（763年）吐蕃乘唐廷安史初平、兵力空虚，攻入长安，"
        "代宗出奔陕州，郭子仪等收复京城。吐蕃一度占据长安十余日，"
        "标志唐朝西部边防的严重弱化，安史之乱后吐蕃、回纥成为主要边患。",
        f"古代史料：《旧唐书·代宗纪》《吐蕃传》；现代参考：{MODERN['tang']}",
        W["jiutang_zizhi"],
        ["regime-tang"],
        [_rel("event-anlu-pacification", "follows"),
         _rel("event-dafeichuan-zhizhan", "precedes", desc="吐蕃自大非川之胜后持续东进")],
        review_note="吐蕃入长安在763年（广德元年）十月；唐代宗奔陕州，郭子仪复京城。"),
    _ev("event-yongzhen-gexin", "永贞革新", "political",
        805, 805, "year", "period-tang", "major",
        "贞元二十一年（805年）顺宗即位，以王叔文、王伾、刘禹锡、柳宗元等推行革新："
        "罢宫市、抑宦官、夺宦官兵权（谋夺神策军）等。"
        "革新遭宦官集团反击，顺宗被迫禅位宪宗，「二王八司马」被贬，"
        "革新不过半年而败。永贞革新是宦官政治背景下士人改革的第一次尝试。",
        f"古代史料：《旧唐书·顺宗纪》《王叔文传》；现代参考：{MODERN['tang']}",
        W["jiutang_zizhi"],
        ["regime-tang"],
        [_rel("event-jianzhong-zhi-luan", "follows"),
         _rel("event-yuanhe-xuefan", "precedes", desc="永贞革新失败后，宪宗元和年间主动削藩")],
        review_note="永贞革新在805年（永贞元年）；「永贞」年号沿用主线（革新实为顺宗朝）。"),
    _ev("event-yuanhe-xuefan", "元和削藩", "political-military",
        806, 820, "range", "period-tang", "major",
        "元和元年至十五年（806—820年）宪宗力主削藩："
        "平西川刘辟（806）、镇海李锜（807）、成德王承宗（受影响）、"
        "淮西吴元济（817）、淄青李师道（819）等，"
        "藩镇武力一度尽折服。元和削藩是唐中后期中央集权的一次显著强化（aggregate）。",
        f"古代史料：《旧唐书·宪宗纪》；现代参考：{MODERN['tang']}",
        W["jiutang_zizhi"],
        ["regime-tang"],
        [_rel("event-yongzhen-gexin", "follows"),
         _rel("event-yuanhe-zhongxing", "leads_to", 0.9, desc="削藩成功造就元和中兴")],
        review_note="元和削藩（806—820）为 aggregate；淮西之战（817）为其最关键战役。"),
    _ev("event-huai-xi-zhi-zhan", "淮西之战（李愬雪夜入蔡州）", "war",
        817, 817, "year", "period-tang", "major",
        "元和十二年（817年）裴度督师淮西，李愬雪夜奇袭蔡州，擒吴元济，"
        "淮西（三州）平。淮西之捷是元和削藩的决定性胜利，"
        "也是「李愬雪夜入蔡州」典故的史实来源。",
        f"古代史料：《旧唐书·李愬传》《吴元济传》；现代参考：{MODERN['tang']}",
        W["jiutang_zizhi"],
        ["regime-tang"],
        [_rel("event-yuanhe-xuefan", "part_of", 0.95, desc="淮西之战为元和削藩核心子事件")],
        review_note="淮西之役（元和九年起，817年告捷）为元和削藩中的关键战役；「雪夜入蔡州」见《李愬传》。"),
    _ev("event-yuanhe-zhongxing", "元和中兴", "political",
        806, 820, "range", "period-tang", "major",
        "宪宗元和年间平藩镇、整财政、任用贤相，唐廷权威一度重振，"
        "史称「元和中兴」（属后世概括）。宪宗晚年怠于政事、斥逐裴度，"
        "820年（元和十五年）被宦官陈弘志等所弑。",
        f"古代史料：《旧唐书·宪宗纪》；现代参考：{MODERN['tang']}",
        W["jiutang"],
        ["regime-tang"],
        [_rel("event-yuanhe-xuefan", "follows"),
         _rel("event-huanguan-shence-jun", "precedes", desc="中兴短暂，其后宦官权势更张")],
        review_note="「元和中兴」为后世概括（§49）；宪宗之死（820）与宦官关系为史家讨论（「陈宏志弑宪宗」见《旧唐书·王守澄传》）。"),
    _ev("event-huanguan-shence-jun", "宦官统领神策军（神策中尉制度确立）", "reform",
        796, 806, "range", "period-tang", "major",
        "贞元十二年（796年）德宗以宦官窦文场、霍仙鸣分任左右神策护军中尉，"
        "神策军正式由宦官统领（§24 具体制度节点）；"
        "此后宦官借神策军行废立之权，成为唐中后期政治一大支柱。",
        f"古代史料：《旧唐书·德宗纪》《宦者传》；现代参考：{MODERN['tang']}",
        W["jiutang"],
        ["regime-tang"],
        [_rel("event-jianzhong-zhi-luan", "follows", desc="泾原兵变后神策军权重、中尉制确立"),
         _rel("event-ganlu-zhi-bian", "leads_to", 0.8, desc="宦官借神策军与文宗决战（甘露之变）")],
        review_note="神策中尉制确立于贞元十二年（796）；宦官由此「示天下莫与抗」（§24：不建「宦官专权」几十年单事件，只记具体节点）。"),
    _ev("event-ganlu-zhi-bian", "甘露之变", "political",
        835, 835, "year", "period-tang", "major",
        "太和九年（835年）文宗与李训、郑注密谋诛宦官，"
        "诈称「甘露」（金吾伏甲）事败，李训、郑注及四相皆被宦官所杀，"
        "株连者千余人。甘露之变是唐代宦官与皇帝、朝臣斗争的总爆发，"
        "此后宦官把持朝政直至唐亡。",
        f"古代史料：《旧唐书·文宗纪》《李训传》；现代参考：{MODERN['tang']}",
        W["jiutang_zizhi"],
        ["regime-tang"],
        [_rel("event-huanguan-shence-jun", "follows"),
         _rel("event-niu-li-dangzheng", "precedes", desc="甘露变后朝官与宦官、牛李两党继续缠斗")],
        review_note="甘露之变在835年（太和九年）十一月；「甘露」之诈为李训所设（京兆府金吾衙内伏兵）。"),
    _ev("event-niu-li-dangzheng", "牛李党争", "political",
        821, 846, "range", "period-tang", "major",
        "长庆元年至会昌六年（约821—846年）以牛僧孺、李宗闵为首的牛党"
        "与李德裕为首的李党长期党争，科举、藩镇、对敌政策屡屡反复，"
        "宰相任免随党争更迭。牛李党争加剧晚唐政治内耗（§25 作 aggregate process，"
        "不逐宰相任免立项）。",
        f"古代史料：《旧唐书·李德裕传》；现代参考：{MODERN['tang']}；陈寅恪《唐代政治史述论稿》（关陇集团与进士科之争）",
        W["jiutang"],
        ["regime-tang"],
        [_rel("event-ganlu-zhi-bian", "follows"),
         _rel("event-huichang-miefo", "precedes", desc="党争持续至武宗会昌年间")],
        review_note="牛李党争（约821—846）为 process；起讫年份有不同口径（自长庆元年李吉甫/牛僧孺之争起算）。"),
    _ev("event-huichang-miefo", "会昌灭佛", "political",
        845, 845, "year", "period-tang", "major",
        "会昌五年（845年）武宗（会昌年间）推行大规模灭佛："
        "天下寺院拆毁、僧尼还俗，没收寺院田产，史称「会昌法难」。"
        "会昌灭佛是唐代第三次也是规模最大的一次灭佛事件，"
        "折射唐后期财政与佛教经济实力的矛盾。",
        f"古代史料：《旧唐书·武宗纪》；现代参考：{MODERN['tang']}",
        W["jiutang_zizhi"],
        ["regime-tang"],
        [_rel("event-niu-li-dangzheng", "follows"),
         _rel("event-dazhong-zhizhi", "precedes", desc="会昌灭佛次年武宗卒，宣宗时佛教复兴")],
        review_note="会昌灭佛在845年（会昌五年）；「四万四千六百寺」、还俗僧尼二十六万等为《旧唐书》记载口径。"),
    _ev("event-dazhong-zhizhi", "大中之治", "political",
        847, 859, "range", "period-tang", "major",
        "宣宗大中年间（847—859年）整顿吏治、抑制宦官、收复失地，"
        "史称「大中之治」（属后世概括，§27：不把后世评价当明确事件）。"
        "大中之治为唐亡前的短暂回光，其后懿宗、僖宗朝迅速衰败。",
        f"古代史料：《旧唐书·宣宗纪》；现代参考：{MODERN['tang']}",
        W["jiutang"],
        ["regime-tang"],
        [_rel("event-huichang-miefo", "follows"),
         _rel("event-pangxun-qiyi", "precedes", desc="大中之后懿宗朝庞勋起义，唐末大乱开启")],
        review_note="「大中之治」为后世概括（historiographical summary，§49）；宣宗之「小太宗」称誉见《旧唐书》。"),
    _ev("event-pangxun-qiyi", "庞勋起义", "rebellion",
        869, 869, "year", "period-tang", "major",
        "咸通十年（869年）桂林戍卒庞勋率众北归，攻陷徐州等地，"
        "举兵反唐，声势浩大，终为唐军所平。庞勋起义震撼东南财赋之地，"
        "是黄巢大起义的直接前奏。",
        f"古代史料：《旧唐书·懿宗纪》《庞勋传》；现代参考：{MODERN['tang']}",
        W["jiutang"],
        ["regime-tang"],
        [_rel("event-dazhong-zhizhi", "follows"),
         _rel("event-wangxianzhi-qiyi", "leads_to", 0.7, desc="庞勋虽败，为黄巢/王仙芝起义张本")],
        review_note="庞勋起义在869年（咸通十年）；「徐州贼庞勋」见《旧唐书》。"),
    _ev("event-wangxianzhi-qiyi", "王仙芝起义", "rebellion",
        875, 878, "range", "period-tang", "major",
        "乾符二年（875年）王仙芝在长垣（今河南长垣）起义，"
        "黄巢起兵响应；王仙芝活动于中原，878年在黄梅战死，"
        "余部并入黄巢。王仙芝起义是唐末民变的开端。",
        f"古代史料：《旧唐书·僖宗纪》；现代参考：{MODERN['tang']}",
        W["jiutang"],
        ["regime-tang"],
        [_rel("event-pangxun-qiyi", "follows"),
         _rel("event-huangchao-qiyi", "leads_to", 0.85, desc="王仙芝败后黄巢领其众成为唐末最大起义")],
        review_note="王仙芝起义（875—878）；黄巢与之「共保」于曹濮一带起义。"),
    _ev("event-huangchao-qiyi", "黄巢起义", "war",
        875, 884, "range", "period-tang", "critical",
        "乾符二年至中和四年（875—884年）黄巢领导唐末最大的农民起义："
        "转战大半个中国，880年攻入长安、建大齐政权，"
        "884年兵败死于泰山。黄巢起义重创唐朝统治根基，"
        "使藩镇割据彻底军阀化，直接导向唐亡（aggregate，子事件见 part_of）。",
        f"古代史料：《旧唐书·黄巢传》《僖宗纪》；现代参考：{MODERN['tang']}",
        W["jiutang_zizhi"],
        ["regime-tang"],
        [_rel("event-wangxianzhi-qiyi", "follows"),
         _rel("event-huangchao-ru-changan", "part_of", 0.95, desc="攻入长安建大齐为黄巢起义顶点"),
         _rel("event-huangchao-baiwang", "part_of", 0.9, desc="黄巢败亡为起义终结")],
        review_note="黄巢起义（875—884）为 aggregate+process；「冲天香阵透长安」等诗句非史载，「内库烧为锦绣灰」亦为后世文学化表达，本库以史实记录为准（§41 中性）。"),
    _ev("event-huangchao-ru-changan", "黄巢攻入长安、唐僖宗入蜀", "war",
        880, 881, "range", "period-tang", "major",
        "广明元年（880年）十二月黄巢军攻入长安，建大齐政权、称帝；"
        "唐僖宗仓皇出奔成都（「僖宗再幸蜀」）。"
        "长安陷落是黄巢起义的顶点，也是唐朝中枢权威崩解的标志。",
        f"古代史料：《旧唐书·黄巢传》《僖宗纪》；现代参考：{MODERN['tang']}",
        W["jiutang_zizhi"],
        ["regime-tang"],
        [_rel("event-huangchao-qiyi", "part_of", 0.95, desc="攻入长安为黄巢起义高潮")],
        review_note="黄巢入长安在880年（广明元年）十二月；大齐改元「金统」。僖宗入蜀仿玄宗故事。"),
    _ev("event-huangchao-baiwang", "黄巢败亡", "war",
        883, 884, "range", "period-tang", "major",
        "中和三年（883年）李克用等沙陀军收复长安，黄巢东撤；"
        "884年（中和四年）黄巢兵败于泰山狼虎谷，自刎（一说被杀）。"
        "黄巢败亡后唐廷名义尚存，但藩镇坐大、天下瓦解之势不可逆转。",
        f"古代史料：《旧唐书·黄巢传》；现代参考：{MODERN['tang']}",
        W["jiutang"],
        ["regime-tang"],
        [_rel("event-huangchao-qiyi", "part_of", 0.9, desc="黄巢败亡为起义终结"),
         _rel("event-zhuwen-jueshi", "leads_to", 0.7, desc="平巢诸镇中朱温等坐大，唐政归于军阀")],
        review_note="黄巢败亡（883—884）：883年李克用复长安、884年黄巢死狼虎谷。"),
    _ev("event-zhuwen-jueshi", "朱温势力上升", "political-military",
        883, 901, "range", "period-tang", "major",
        "黄巢降将朱温（赐名全忠）882年归唐，883年任宣武节度使，"
        "以汴梁为基地消灭秦宗权等，至901年前后控制中原大部、"
        "成为唐末最强藩镇，进而挟制朝廷。朱温的崛起重绘了唐末权力地图。",
        f"古代史料：《旧唐书·朱温传》；现代参考：{MODERN['wudai']}",
        W["jiutang"],
        ["regime-tang"],
        [_rel("event-huangchao-baiwang", "follows"),
         _rel("event-zhuwen-qian-du", "leads_to", 0.85, desc="朱温控制朝廷并迁都洛阳")],
        review_note="朱温势力上升（883—901）为过程；其叛黄巢归唐为882年前后，朱全忠名遂立。"),
    _ev("event-zhuwen-qian-du", "朱温控制唐廷、迁都洛阳", "political",
        903, 904, "range", "period-tang", "major",
        "天复三年至天祐元年（903—904年）朱温入关中控制昭宗，"
        "904年强迫昭宗迁都洛阳并烧毁长安宫室；同年八月弑昭宗，"
        "立昭宣帝（哀帝）。唐廷名存实亡，全然为朱温所制。",
        f"古代史料：《旧唐书·昭宗纪》《朱温传》；现代参考：{MODERN['wudai']}",
        W["jiutang"],
        ["regime-tang"],
        [_rel("event-zhuwen-jueshi", "follows"),
         _rel("event-houliang-dai-tang", "leads_to", 0.9, desc="弑昭宗、废哀帝后，朱温于907年建梁代唐")],
        review_note="迁都洛阳在904年；昭宗遇弑（同年八月）、哀帝立，为唐亡之最后两步。"),
]

# ---------------------------------------------------------------------------
# Phase 6 — 五代十国（907–959；辽并行）
# ---------------------------------------------------------------------------
PHASE_FIVE_DYNASTIES = [
    _ev("event-houliang-dai-tang", "朱温废哀帝、后梁建立、唐朝灭亡", "dynastic-transition",
        907, 907, "year", "period-five-dynasties-ten-kingdoms", "critical",
        "开平元年（907年）朱温废唐哀帝自立，国号梁（后梁），都汴州（开封），"
        "唐朝正式灭亡，中国历史进入五代十国时代。"
        "后梁代唐是唐末军阀政治的终点与五代中原政权更替的起点（§30："
        "同时体现 Regime Transition）。",
        f"古代史料：《旧五代史·梁太祖纪》；现代参考：{MODERN['wudai']}",
        W["wudai_zizhi"],
        ["regime-later-liang"],
        [_rel("event-zhuwen-qian-du", "follows"),
         _rel("event-hou-tang-jianguo", "leads_to", 0.8, desc="后梁立足中原十七年，为后唐所灭")],
        review_note="后梁建立（907年）与「唐朝灭亡」为同一节点（§48 行动+outcome 合一）；朱温弑哀帝于908年（开平二年）。"),
    _ev("event-qian-shu-jianli", "前蜀建立（王建称帝）", "dynastic-transition",
        907, 907, "year", "period-five-dynasties-ten-kingdoms", "major",
        "在朱温代唐的同时，唐末西川节度使王建于907年称帝建国（前蜀），"
        "都成都。前蜀是十国中较早建立的政权，与中原后梁并行对峙。",
        f"古代史料：《新五代史·前蜀世家》；现代参考：{MODERN['wudai']}",
        W["wudai"],
        ["regime-former-shu"],
        [_rel("event-houliang-dai-tang", "precedes", desc="前蜀与中原政权同期并存")],
        review_note="前蜀建立（907）；王建本为唐西川节度使，称帝于都成都。"),
    _ev("event-qidan-jianguo", "耶律阿保机建契丹（916称帝）", "dynastic-transition",
        907, 916, "range", "period-liao", "major",
        "耶律阿保机907年即契丹可汗位，916年（神册元年）称帝建国（契丹），"
        "是为辽朝的前身。契丹政权在五代时期崛起于漠北，"
        "成为中原政权之外的又一大政治力量，并与五代、十国并行（§35/§36）。",
        f"古代史料：《辽史·太祖纪》；现代参考：{MODERN['wudai']}",
        W["liao"],
        ["regime-liao"],
        [_rel("event-houliang-dai-tang", "precedes", desc="契丹与五代同期兴起"),
         _rel("event-yan-yun-shiliuzhou", "leads_to", 0.8, desc="后晋石敬瑭割燕云十六州予契丹")],
        review_note="阿保机916年称帝（神册元年）；907—916年为可汗位巩固期（「诸弟之乱」等为内部斗争）。"),
    _ev("event-hou-tang-jianguo", "李存勖灭后梁、后唐建立", "dynastic-transition",
        923, 923, "year", "period-five-dynasties-ten-kingdoms", "major",
        "同光元年（923年）沙陀贵族李存勖（后唐庄宗）攻灭后梁，"
        "称帝建国，国号唐（后唐），都洛阳。后唐以「中兴唐室」为号，"
        "是五代中疆域最广的政权之一。",
        f"古代史料：《旧五代史·唐庄宗纪》；现代参考：{MODERN['wudai']}",
        W["wudai_zizhi"],
        ["regime-later-tang"],
        [_rel("event-houliang-dai-tang", "follows", desc="后梁为后唐所灭"),
         _rel("event-shi-jingtang-dai-tang", "leads_to", 0.8, desc="后唐旋即又亡于后晋石敬瑭")],
        review_note="后唐灭后梁（923，同光元年）——「李存勖灭后梁、后唐建立」合一；后唐沿袭沙陀系（与后汉/后周皆太原军阀）。"),
    _ev("event-hou-shu-jianli", "后蜀建立", "dynastic-transition",
        934, 934, "year", "period-five-dynasties-ten-kingdoms", "major",
        "应顺元年（934年）孟知祥在成都称帝建国（后蜀）。"
        "后蜀继前蜀再据西川，为十国中较安定富庶的政权。",
        f"古代史料：《新五代史·后蜀世家》；现代参考：{MODERN['wudai']}",
        W["wudai"],
        ["regime-later-shu"],
        [_rel("event-qian-shu-jianli", "follows", desc="后蜀继前蜀据蜀")],
        review_note="后蜀建立（934）；孟知祥为后唐所置西川节度使，自立称帝。"),
    _ev("event-shi-jingtang-dai-tang", "石敬瑭灭后唐、后晋建立", "dynastic-transition",
        936, 936, "year", "period-five-dynasties-ten-kingdoms", "major",
        "天福元年（936年）后唐河东节度使石敬瑭勾结契丹（耶律德光），"
        "以父礼事契丹并许诺割让燕云十六州，借契丹兵灭后唐，"
        "自称皇帝建国晋（后晋），都汴州。后晋是「儿皇帝」政治关系的产物。",
        f"古代史料：《旧五代史·晋高祖纪》；现代参考：{MODERN['wudai']}",
        W["wudai_zizhi"],
        ["regime-later-jin", "regime-liao"],
        [_rel("event-hou-tang-jianguo", "follows"),
         _rel("event-yan-yun-shiliuzhou", "leads_to", 0.9, desc="称帝同时割让燕云十六州")],
        review_note="石敬瑭936年称帝（天福元年）建后晋，灭后唐；「儿皇帝」与称臣纳贡见《旧五代史》。"),
    _ev("event-yan-yun-shiliuzhou", "燕云十六州割让契丹", "treaty",
        936, 938, "range", "period-five-dynasties-ten-kingdoms", "major",
        "936年石敬瑭为借契丹之力灭后唐，允诺割让幽、蓟、瀛、莫、涿、檀、顺、"
        "新、妫、儒、武、云、应、寰、朔、蔚十六州（燕云十六州）予契丹；"
        "938年正式交割。燕云十六州之割使中原失去长城天险，"
        "对宋辽对峙格局影响深远（§34：行政区划的政治领土安排，非单次战役）。",
        f"古代史料：《旧五代史·晋高祖纪》《辽史·太宗纪》；现代参考：{MODERN['wudai']}",
        W["wudai_zizhi"],
        ["regime-later-jin", "regime-liao"],
        [_rel("event-shi-jingtang-dai-tang", "follows", desc="后晋立国即割燕云"),
         _rel("event-qidan-mie-houjin", "leads_to", 0.6, desc="后晋虽事契丹，仍终于947年为契丹所灭")],
        review_note="燕云十六州之割（936约定/938交割）为政治领土安排节点；「燕云」之称多见于宋代文献。"),
    _ev("event-nan-tang-jianli", "南唐建立（李昪代吴）", "dynastic-transition",
        937, 937, "year", "period-five-dynasties-ten-kingdoms", "major",
        "昇元元年（937年）吴国权臣李昪（徐知诰）代吴称帝，国号唐（南唐），"
        "都金陵（今南京）。南唐继吴而兴，据有江淮，为十国中最强盛的政权之一，"
        "与中原后晋、后汉、后周长期对峙。",
        f"古代史料：《新五代史·南唐世家》；现代参考：{MODERN['wudai']}",
        W["wudai"],
        ["regime-southern-tang"],
        [_rel("event-shi-jingtang-dai-tang", "precedes", desc="南唐与中原政权并存"),
         _rel("event-houzhou-nanzheng", "leads_to", 0.7, desc="南唐终为后周/北宋所削弱（958年献地）")],
        review_note="南唐建立（937）；李昪为杨吴权臣，其篡吴立唐为十国政权更替典型。"),
    _ev("event-qidan-mie-houjin", "契丹灭后晋（辽改国号大辽）", "war",
        946, 947, "range", "period-five-dynasties-ten-kingdoms", "major",
        "开运三年至四年（946—947年）后晋出帝背盟拒契丹，"
        "耶律德光大举南下，946年冬灭后晋、入开封，"
        "947年正月改国号为大辽（契丹—辽政权国号变化节点）。"
        "契丹虽旋即北返，但「契丹灭后晋」使中原政权首次被北方民族政权所灭。",
        f"古代史料：《旧五代史·晋少帝纪》《辽史·太宗纪》；现代参考：{MODERN['wudai']}",
        W["wudai_zizhi"],
        ["regime-liao", "regime-later-jin"],
        [_rel("event-yan-yun-shiliuzhou", "follows"),
         _rel("event-liuzhiyuan-jianhan", "leads_to", 0.7, desc="契丹北返后，刘知远在太原建后汉")],
        review_note="契丹灭后晋（946—947）；耶律德光在开封改国号辽（「大辽」）。「灭后晋+辽国号」合一节点（§36）。"),
    _ev("event-liuzhiyuan-jianhan", "刘知远建立后汉", "dynastic-transition",
        947, 947, "year", "period-five-dynasties-ten-kingdoms", "major",
        "天福十二年（947年）河东节度使刘知远（沙陀）在太原称帝建国汉（后汉），"
        "后入开封。后汉是五代中最短命的中原政权，951年为后周郭威所代。",
        f"古代史料：《旧五代史·汉高祖纪》；现代参考：{MODERN['wudai']}",
        W["wudai_zizhi"],
        ["regime-later-han"],
        [_rel("event-qidan-mie-houjin", "follows", desc="契丹北去后后汉代兴"),
         _rel("event-guo-wei-dai-han", "leads_to", 0.8, desc="后汉旋为郭威所代（后周）")],
        review_note="刘知远建后汉（947年，天福十二年）；后汉历两帝而亡（951）。"),
    _ev("event-beihan-jianli", "北汉建立", "dynastic-transition",
        951, 951, "year", "period-five-dynasties-ten-kingdoms", "major",
        "乾祐四年（951年）郭威代汉，后汉宗室刘崇（刘旻）在太原称帝，"
        "国号仍称汉（北汉），依附契丹。北汉是十国中唯一地处北方、"
        "与中原政权对抗的政权，也是后来宋辽冲突的直接前台。",
        f"古代史料：《新五代史·东汉世家》；现代参考：{MODERN['wudai']}",
        W["wudai"],
        ["regime-northern-han"],
        [_rel("event-guo-wei-dai-han", "follows", desc="后周代汉后北汉别立于太原")],
        review_note="北汉建立（951）；刘旻附辽称「侄皇帝」，与后晋/赵宋对峙。"),
    _ev("event-guo-wei-dai-han", "郭威代汉、后周建立", "dynastic-transition",
        951, 951, "year", "period-five-dynasties-ten-kingdoms", "critical",
        "广顺元年（951年）后汉枢密使郭威于澶州兵变后受禅称帝，国号周（后周），"
        "都开封。后周建立五代最后一个中原王朝，其后的柴荣改革"
        "为北宋统一奠定基础。",
        f"古代史料：《旧五代史·周太祖纪》；现代参考：{MODERN['wudai']}",
        W["wudai_zizhi"],
        ["regime-later-zhou"],
        [_rel("event-liuzhiyuan-jianhan", "follows", desc="郭威代汉建后周"),
         _rel("event-chai-rong-jiwei", "leads_to", 0.8, desc="郭威之后柴荣（世宗）即位改革")],
        review_note="郭威951年建后周（广顺元年）；「澶州兵变」为其契机。"),
    _ev("event-chai-rong-jiwei", "后周世宗即位", "political",
        954, 954, "year", "period-five-dynasties-ten-kingdoms", "major",
        "显德元年（954年）周太祖郭威去世，养子柴荣即位，是为后周世宗。"
        "世宗在位五六年，整军经武、励行改革，是五代最有作为的君主之一，"
        "为统一奠基。",
        f"古代史料：《旧五代史·周世宗纪》；现代参考：{MODERN['wudai']}",
        W["wudai_zizhi"],
        ["regime-later-zhou"],
        [_rel("event-guo-wei-dai-han", "follows"),
         _rel("event-chai-rong-gaige", "leads_to", 0.9, desc="世宗即位后推行改革")],
        review_note="柴荣954年即位（显德元年）；「周世宗」为五代改革之主。"),
    _ev("event-chai-rong-gaige", "柴荣改革", "reform",
        954, 959, "range", "period-five-dynasties-ten-kingdoms", "major",
        "后周世宗在位期间（954—959年）推行全面改革："
        "整顿禁军（「殿前诸班」）、整饬吏治财政、毁佛汰僧（显德二年）、"
        "均定田赋、广开科举；对外攻后蜀（955）、征南唐（956—958）、"
        "北伐契丹（959）连下三关。柴荣改革为北宋统一全国奠定了政治军事基础"
        "（§38 aggregate，子事件见 part_of）。",
        f"古代史料：《旧五代史·周世宗纪》；现代参考：{MODERN['wudai']}",
        W["wudai_zizhi"],
        ["regime-later-zhou"],
        [_rel("event-chai-rong-jiwei", "follows"),
         _rel("event-gaoping-zhizhan", "part_of", 0.9, desc="高平之战为整顿禁军之由"),
         _rel("event-houzhou-nanzheng", "part_of", 0.9, desc="征南唐为南征北伐之一环")],
        review_note="柴荣改革（954—959）为 aggregate；「毁佛汰僧」「均田赋」诸措施见《旧五代史》与《册府元龟》。"),
    _ev("event-gaoping-zhizhan", "高平之战", "war",
        954, 954, "year", "period-five-dynasties-ten-kingdoms", "major",
        "显德元年（954年）北汉联合契丹南犯，柴荣亲征，在泽州高平大破之。"
        "高平之战胜后柴荣处斩临阵脱逃的将校七十余人，整顿禁军，"
        "后周军力自此为之一振。",
        f"古代史料：《旧五代史·周世宗纪》；现代参考：{MODERN['wudai']}",
        W["wudai_zizhi"],
        ["regime-later-zhou"],
        [_rel("event-chai-rong-gaige", "part_of", 0.95, desc="高平之战为柴荣改革之开端")],
        review_note="高平之战在954年（显德元年）；柴荣「斩樊爱能等」立威。"),
    _ev("event-houzhou-nanzheng", "后周征南唐", "war",
        956, 958, "range", "period-five-dynasties-ten-kingdoms", "major",
        "显德三年至五年（956—958年）后周世宗三征南唐，"
        "克江北十四州，南唐去帝号、称臣（「去帝号，用显德年号」）。"
        "后周征南唐削弱南方最强政权，为统一江南扫清障碍。",
        f"古代史料：《旧五代史·周世宗纪》；现代参考：{MODERN['wudai']}",
        W["wudai_zizhi"],
        ["regime-later-zhou", "regime-southern-tang"],
        [_rel("event-chai-rong-gaige", "part_of", 0.9, desc="征南唐为柴荣改革之南线")],
        review_note="后周征南唐（956—958）三年三役；江北十四州之取得使南唐衰。"),
]

ALL_PHASES = [
    ("sui_tang", "Phase 1 隋", PHASE_SUI),
    ("sui_tang", "Phase 2 初唐", PHASE_EARLY_TANG),
    ("sui_tang", "Phase 3 高宗/武周", PHASE_GAOZONG_WUZHOU),
    ("sui_tang", "Phase 4 开元/天宝/安史", PHASE_XUANZONG_ANLU),
    ("sui_tang", "Phase 5 中晚唐/唐末", PHASE_LATE_TANG),
    ("five_dynasties", "Phase 6 五代十国", PHASE_FIVE_DYNASTIES),
]

PHASES = {
    "SUI": PHASE_SUI,
    "EARLY_TANG": PHASE_EARLY_TANG,
    "GAOZONG_WUZHOU": PHASE_GAOZONG_WUZHOU,
    "XUANZONG_ANLU": PHASE_XUANZONG_ANLU,
    "LATE_TANG": PHASE_LATE_TANG,
    "FIVE_DYNASTIES": PHASE_FIVE_DYNASTIES,
}


def all_events():
    return [(dir_, label, ev) for dir_, label, events in ALL_PHASES for ev in events]