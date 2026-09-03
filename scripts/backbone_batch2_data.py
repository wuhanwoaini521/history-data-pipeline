# -*- coding: utf-8 -*-
"""China History Backbone V1 — Batch 2（秦 → 西汉 → 新 → 东汉）Curated Event Data。

由 scripts/backbone_batch2_write.py 写入：
- data/curated/history_backbone/events/qin_han/<event_id>.yml
- data/reviews/accepted/<event_id>.review.json
- data/candidates/backbone_events/qin_han/*_candidates.yml

复用（不重复建档）：
- 秦统一系列（event-qin-tongyi / event-qin-mie-liuguo / event-qin-mie-*）→ chunqiu_zhanguo/
- 楚汉 Story 9 个 Event（event-chuhan-*）→ 直接引用，仅给其中 4 个添加 part_of → 楚汉战争
- 黄巾起义（event-three-yellow-turbans，184）→ 作为东汉主干结束节点，不新建
"""

from __future__ import annotations

MODERN = {
    "qin": "林剑鸣《秦史稿》（上海人民出版社）；翦伯赞《秦汉史》（北京大学出版社）；"
           "张岂之主编《中国历史·秦汉魏晋南北朝卷》；白寿彝总主编《中国通史》",
    "han": "翦伯赞《秦汉史》（北京大学出版社）；吕思勉《秦汉史》（上海古籍出版社）；"
           "田余庆《秦汉魏晋史探微》（北京大学出版社）；张岂之主编《中国历史·秦汉魏晋南北朝卷》",
    "xin": "翦伯赞《秦汉史》（北京大学出版社）；张岂之主编《中国历史·秦汉魏晋南北朝卷》",
    "donghan": "翦伯赞《秦汉史》（北京大学出版社）；何兹全《秦汉史略》及近人秦汉史专著；"
               "张岂之主编《中国历史·秦汉魏晋南北朝卷》",
}

W = {
    "shiji": ["work-curated-shiji"],
    "hanshu": ["work-curated-hanshu"],
    "houhanshu": ["work-curated-houhanshu"],
    "shiji_hanshu": ["work-curated-shiji", "work-curated-hanshu"],
    "hanshu_zizhi": ["work-curated-hanshu", "work-curated-zizhitongjian"],
    "houhanshu_zizhi": ["work-curated-houhanshu", "work-curated-zizhitongjian"],
    "shiji_houhanshu": ["work-curated-shiji", "work-curated-houhanshu"],
}


def _rel(target, rtype, confidence=None, desc=None):
    item = {"target_event_id": target, "relation_type": rtype}
    if confidence is not None:
        item["confidence"] = confidence
    if desc:
        item["description_zh_cn"] = desc
    return item


def _ev(id_, name, etype, start, end, precision, period, importance, summary,
        source_ref, source_ids, relations=None, review_note=None):
    return {
        "id": id_, "name_zh_cn": name, "event_type": etype,
        "start_year": start, "end_year": end, "date_precision": precision,
        "period_id": period, "importance": importance, "summary_zh_cn": summary,
        "source_ref": source_ref, "source_ids": source_ids, "relations": relations or [],
        "review_note": review_note,
    }


# ---------------------------------------------------------------------------
# Phase Q — 秦（含楚汉战争 aggregate；复用 event-qin-tongyi 等）
# ---------------------------------------------------------------------------
PHASE_QIN = [
    # ---- 秦帝国制度（-221 年起）----
    _ev("event-qin-junxian", "秦推行郡县制", "reform",
        -221, -221, "year", "period-qin", "major",
        "秦始皇二十六年（前221年）丞相王绾等主张分封诸子，廷尉李斯力主郡县制，始皇帝从之，"
        "废分封、行郡县，全国设三十六郡（后增至四十余郡）。郡县制是秦强化中央集权、"
        "代替世卿贵族分封的关键制度变革，成为中国此后两千余年地方行政的基本框架。",
        f"古代史料：《史记·秦始皇本纪》；现代参考：{MODERN['qin']}",
        W["shiji"],
        [_rel("event-qin-tongyi", "follows", desc="统一后随即推行郡县制")],
        review_note="郡县数（三十六郡）与初置时间有细节讨论，不影响事件本身。"),
    _ev("event-qin-shutongwen", "书同文（统一文字）", "cultural",
        -221, -221, "year", "period-qin", "major",
        "秦始皇统一文字，以秦小篆为正字标准推行全国，废除六国异体文字；"
        "同时程邈所整理之隶书亦在实际使用中普及。书同文结束了战国文字异形的状态，"
        "是秦统一文化制度的标志性措施之一。",
        f"古代史料：《史记·秦始皇本纪》；现代参考：{MODERN['qin']}",
        W["shiji"],
        [_rel("event-qin-junxian", "follows", desc="与郡县制同期推行的统一措施")],
        review_note="统一文字为渐进实施过程；小篆标准与隶书普及的细节（如程邈造隶书传说）为后世记载。"),
    _ev("event-qin-tongyi-duliangheng", "统一度量衡", "reform",
        -221, -221, "year", "period-qin", "major",
        "秦始皇下令统一度量衡制度：明令度量衡沿秦国商鞅之法推广全国，"
        "在衡器上刻诏书铭文，确立统一的权衡、尺与量制。此举为全国征税、贸易与工程提供统一标准。",
        f"古代史料：《史记·秦始皇本纪》、出土秦权量铭文；现代参考：{MODERN['qin']}",
        W["shiji"],
        [_rel("event-qin-shutongwen", "follows", desc="与书同文同为秦大统一措施")],
        review_note="铭文诏书为实物证据；贯彻程度存在地区差异。"),
    _ev("event-qin-tongyi-bihuo", "统一货币", "economic",
        -221, -221, "year", "period-qin", "major",
        "秦始皇统一货币：黄金为上币（以镒为单位），铜钱（圆形方孔半两钱）为下币，"
        "废除六国旧币。圆形方孔钱由此成为此后中国两千余年铜钱的基本形制。",
        f"古代史料：《史记·平准书》；现代参考：{MODERN['qin']}",
        W["shiji"],
        [_rel("event-qin-tongyi-duliangheng", "follows", desc="统一度量衡后的又一统一经济措施")],
        review_note="半两钱实际流通与铸行时间有地域差异，属制度统一的基本叙事。"),
    _ev("event-qin-chidao", "修建驰道", "economic",
        -220, -220, "year", "period-qin", "major",
        "秦始皇二十七年（前220年）起修筑驰道，以都城咸阳为中心通往全国，"
        "东至燕齐、南达吴楚，道广五十步、树以青松，形成全国性道路交通骨干，"
        "并为军事调动与巡游统治提供支撑（后又有直道等干道工程）。",
        f"古代史料：《史记·秦始皇本纪》；现代参考：{MODERN['qin']}",
        W["shiji"],
        [_rel("event-qin-tongyi-bihuo", "follows", desc="统一后大规模交通建设")],
        review_note="驰道具体路线与里程依托文献与考古复原，细节有讨论。"),
    _ev("event-qin-beiji-xiongnu", "北击匈奴（蒙恬却匈奴）", "war",
        -215, -214, "range", "period-qin", "major",
        "秦始皇三十二年（前215年）遣蒙恬率三十万大军北击匈奴，"
        "前214年前后收复河南地（今河套一带），逐匈奴七百余里，"
        "置九原郡并沿黄河设塞，匈奴退居阴山以北。",
        f"古代史料：《史记·蒙恬列传》《秦始皇本纪》；现代参考：{MODERN['qin']}",
        W["shiji"],
        [_rel("event-qin-chidao", "follows", desc="北防匈奴的军事行动")],
        review_note="蒙恬北征与置郡年代（前215—前214）采用《史记》系年；匈奴早期游牧实力有地域记载差异。"),
    _ev("event-qin-xiu-changcheng", "修筑长城", "economic",
        -214, -213, "range", "period-qin", "major",
        "秦始皇命蒙恬连接并修筑西起临洮、东至辽东的万里长城，"
        "利用原秦、赵、燕三国边城，筑障塞以御匈奴。秦长城是空前规模的国防工程，"
        "但征发大量民力，加重百姓负担。",
        f"古代史料：《史记·蒙恬列传》《秦始皇本纪》；现代参考：{MODERN['qin']}",
        W["shiji"],
        [_rel("event-qin-beiji-xiongnu", "follows", desc="全面筑塞的国防工程")],
        review_note="秦长城修筑约前214年（又有前213年说）；\"万里\"为后世概括说法，考古所见秦长城与后代长城并非同一墙体。"),
    _ev("event-qin-nanzheng-baiyue", "南征百越", "war",
        -218, -214, "range", "period-qin", "major",
        "秦始皇二十八年（前219年）后发兵五十万征南越，经数年征战，"
        "约前214年平岭南，置桂林、南海、象三郡，并开凿灵渠沟通湘漓水系。"
        "百越之地自此纳入秦郡县体系，中原与岭南联系加强。",
        f"古代史料：《史记·南越列传》《秦始皇本纪》；现代参考：{MODERN['qin']}",
        W["shiji"],
        [_rel("event-qin-chidao", "follows", desc="南服百越的军事行动")],
        review_note="南征时间（约前219—前214）各记载略有出入；灵渠开凿年代亦依附于此过程。"),
    # ---- 秦末 ----
    _ev("event-qin-shihuang-beng", "秦始皇去世", "political",
        -210, -210, "year", "period-qin", "major",
        "秦始皇三十七年（前210年）七月，始皇帝东巡途中病死于沙丘平台（今河北广宗一带）。"
        "其去世使帝国权力交接骤然展开，为赵高矫诏政变提供了前提。",
        f"古代史料：《史记·秦始皇本纪》；现代参考：{MODERN['qin']}",
        W["shiji"],
        [_rel("event-shaqiu-zhengbian", "leads_to", 0.95, desc="始皇帝猝死直接引发沙丘矫诏之变")],
        review_note="死亡时间前210年为《史记》系年；沙丘地望在河北广宗一带为通行说法。"),
    _ev("event-shaqiu-zhengbian", "沙丘政变（赵高矫诏、胡亥即位）", "political",
        -210, -210, "year", "period-qin", "major",
        "前210年秦始皇病逝沙丘，临终诏令长子扶苏继位并主持丧事；"
        "中车府令赵高与丞相李斯合谋隐匿死讯，矫诏赐死扶苏、蒙恬，立少子胡亥为二世皇帝。"
        "此后赵高掌权，秦廷内部迅速失去稳定性，加速了秦政权的崩溃。",
        f"古代史料：《史记·秦始皇本纪》《李斯列传》；现代参考：{MODERN['qin']}",
        W["shiji"],
        [_rel("event-qin-shihuang-beng", "follows"),
         _rel("event-chensheng-wuguang-qiyi", "leads_to", 0.7,
              desc="胡亥赵高暴政激化社会矛盾，直接导向大泽乡起义")],
        review_note="沙丘政变为公认的重大政治事件；李斯是否完全被动参与存在记载与史评差异。"),
    _ev("event-chensheng-wuguang-qiyi", "陈胜吴广起义", "rebellion",
        -209, -209, "year", "period-qin", "major",
        "秦二世元年（前209年）七月，戍卒陈胜、吴广在蕲县大泽乡（今安徽宿州一带）揭竿起义，"
        "提出\"王侯将相宁有种乎\"，建立张楚政权，各地反秦力量纷纷响应。"
        "这是中国历史上第一次大规模农民起义，拉开了秦末战争的序幕。",
        f"古代史料：《史记·陈涉世家》；现代参考：{MODERN['qin']}",
        W["shiji"],
        [_rel("event-shaqiu-zhengbian", "follows"),
         _rel("event-chuhan-qin-revolt", "part_of", 0.9, desc="陈胜吴广起义为秦末起义（前209—前206）的开端", )],
        review_note="大泽乡起义年代前209年为通行纪年；项羽、刘邦等反秦力量随后兴起（见秦末起义）。"),
    _ev("event-liubang-ru-guan", "刘邦入关", "political-military",
        -207, -207, "year", "period-qin", "major",
        "前207年，刘邦率军自武关攻入关中，十月至霸上，秦王子婴出降，秦亡。"
        "因刘邦先入关、后项羽入关，\"先入定关中者王之\"之约成为楚汉相争的导火索之一。",
        f"古代史料：《史记·高祖本纪》；现代参考：{MODERN['qin']}",
        W["shiji"],
        [_rel("event-chuhan-qin-revolt", "part_of", 0.8, desc="刘邦西进为秦末反秦战争的一部分"),
         _rel("event-chuhan-qin-fall", "leads_to", 0.9, desc="刘邦入关、子婴出降，秦朝灭亡")],
        review_note="刘邦入关在前207年（以十月为岁首，史书或记入汉元年即前206年），本库采用纪年-207并与既有秦亡事件（-206）衔接。"),
    # ---- 楚汉战争（aggregate，reuse 楚汉 Story Event）----
    _ev("event-chuhan-war", "楚汉战争", "political-military",
        -206, -202, "range", "period-western-han", "major",
        "楚汉战争指前206年至前202年项羽楚政权与刘邦汉政权争夺天下的战争过程："
        "自鸿门宴后的政治对抗、彭城之战、荥阳对峙至垓下决战，刘邦最终获胜。"
        "本事件为 aggregate，子事件（鸿门宴/彭城之战/荥阳对峙/垓下之战）通过 part_of 关联；"
        "各子事件沿用已审核的楚汉 Story Event，不重复建档。",
        f"古代史料：《史记·项羽本纪》《高祖本纪》；现代参考：{MODERN['qin']}",
        W["shiji"],
        [_rel("event-chuhan-qin-fall", "follows", desc="秦亡后进入楚汉相争"),
         _rel("event-chuhan-han-foundation", "leads_to", 0.85, desc="楚汉战争以刘邦建立汉朝告终")],
        review_note="楚汉战争起讫（前206—前202）为通行口径；作为 aggregate 事件，子事件沿用既有已审核 Event（event-hongmen / event-chuhan-pengcheng / event-chuhan-xingyang / event-chuhan-gaixia）。"),
]

# ---------------------------------------------------------------------------
# Phase WH — 西汉
# ---------------------------------------------------------------------------
PHASE_WESTERN_HAN = [
    _ev("event-han-dingdu-changan", "汉定都长安", "foundation",
        -202, -200, "range", "period-western-han", "major",
        "刘邦初都洛阳，经娄敬（刘敬）谏言与张良支持，前202年起定都关中；"
        "前200年未央宫落成，长安正式成为汉朝都城。长安自此为西汉政治中心二百余年，"
        "并发展为当时东亚最大都市。",
        f"古代史料：《史记·高祖本纪》《刘敬列传》；现代参考：{MODERN['han']}",
        W["shiji"],
        [_rel("event-chuhan-han-foundation", "follows", desc="汉朝建立后定都关中")],
        review_note="定都决策在前202年、未央宫成在前200年，取 range 表述。"),
    _ev("event-baideng-zhiwei", "白登之围", "war",
        -200, -200, "year", "period-western-han", "major",
        "前200年冬，刘邦亲率大军伐韩王信（叛投匈奴），在平城白登山（今山西大同东北）"
        "被匈奴冒顿单于四十万骑围困七日，靠陈平计脱围。白登之围使汉廷认识到"
        "无力以武力制服匈奴，直接促成汉匈和亲政策。",
        f"古代史料：《史记·匈奴列传》《高祖本纪》；现代参考：{MODERN['han']}",
        W["shiji"],
        [_rel("event-han-dingdu-changan", "follows"),
         _rel("event-hanhan-heqin", "leads_to", 0.85, desc="白登之围后汉朝确立和亲战略")],
        review_note="白登之围前200年（汉高帝七年）为通行纪年；\"七日解围\"细节依赖《史记》记载。"),
    _ev("event-hanhan-heqin", "汉匈和亲政策确立", "alliance",
        -198, -198, "year", "period-western-han", "major",
        "前198年（一说前199年），刘敬出使匈奴缔结和亲，汉以宗室女嫁单于、岁奉絮缯酒食，"
        "约以长城为界。和亲成为汉初六七十年对匈奴的基本政策，至汉武帝马邑之谋（前133）才被打破。",
        f"古代史料：《史记·刘敬列传》《匈奴列传》；现代参考：{MODERN['han']}",
        W["shiji"],
        [_rel("event-baideng-zhiwei", "follows"),
         _rel("event-mayi-zhi-mou", "precedes", desc="和亲政策持续至汉武帝马邑之谋")],
        review_note="首行和亲约前198年（高帝九年），史载年份略有出入；\"和亲\"为长期政策，此处登记其确立节点。"),
    _ev("event-hanchu-yixingwang", "剪除异姓诸侯王", "political-military",
        -202, -195, "range", "period-western-han", "major",
        "汉高帝在楚汉战争中封授韩彭英等异姓诸侯王，战后逐年剪除：燕王臧荼（-202）、"
        "楚王韩信与韩王信（-201）、赵相陈豨（-197）、梁王彭越（-196）、淮南王英布（-196）等先后被灭，"
        "至前195年刘邦去世前，异姓王基本清除，并盟誓\"非刘氏而王，天下共击之\"。",
        f"古代史料：《史记·高祖本纪》《淮阴侯列传》；现代参考：{MODERN['han']}",
        W["shiji"],
        [_rel("event-chuhan-han-foundation", "follows"),
         _rel("event-baima-zhi-meng", "leads_to", 0.8, desc="剪除异姓王后以白马之盟确定非刘氏不王")],
        review_note="剪除异姓王为逐年进行的过程事件（前202—前195）；韩信、彭越、英布之死的时间与细节见《史记》各传。"),
    _ev("event-baima-zhi-meng", "白马之盟", "treaty",
        -195, -195, "year", "period-western-han", "major",
        "前195年，汉高帝与群臣杀白马盟誓：\"非刘氏而王，天下共击之；非有功而侯，天下共击之\"，"
        "史称白马之盟。此盟约成为西汉'郡国并行'体制下诸侯王国刘氏化的制度性声明，"
        "后来吕后封诸吕为王即为违背此盟。",
        f"古代史料：《史记·吕太后本纪》；现代参考：{MODERN['han']}",
        W["shiji"],
        [_rel("event-hanchu-yixingwang", "follows"),
         _rel("event-luhou-linchao", "precedes", desc="吕后封诸吕为王与白马之盟相冲突")],
        review_note="白马之盟前195年（高帝十二年）；盟约内容据《史记》《汉书》，后世政治话语中反复援引。"),
    _ev("event-liubang-si", "汉高祖刘邦去世", "political",
        -195, -195, "year", "period-western-han", "major",
        "前195年四月，汉高帝刘邦病逝于长乐宫，太子刘盈继位（汉惠帝）。"
        "刘邦去世后吕后实际控制朝政，功臣集团与刘氏宗室的权力平衡进入新阶段。",
        f"古代史料：《史记·高祖本纪》《吕太后本纪》；现代参考：{MODERN['han']}",
        W["shiji"],
        [_rel("event-baima-zhi-meng", "follows"),
         _rel("event-luhou-linchao", "leads_to", 0.85, desc="刘邦死后吕后逐渐掌握朝政")],
        review_note="前195年四月病逝为《史记》系年；惠帝继位属平稳交接。"),
    _ev("event-luhou-linchao", "吕后临朝称制", "political",
        -188, -180, "range", "period-western-han", "major",
        "惠帝在位七年间吕后已执掌实权；前188年惠帝去世后，吕后临朝称制，"
        "先后立两少帝，并违背白马之盟分封吕氏诸王，诸吕势力达到顶峰。"
        "吕后是中国历史上第一位临朝称制的女性统治者。",
        f"古代史料：《史记·吕太后本纪》；现代参考：{MODERN['han']}",
        W["shiji"],
        [_rel("event-liubang-si", "follows"),
         _rel("event-zhulv", "leads_to", 0.8, desc="吕后死后诸吕谋乱，随即被诛除")],
        review_note="吕后临朝称制（前188—前180）期间\"诸吕封王\"为主要政治事件；称制之权亦受到功臣集团制约。"),
    _ev("event-zhulv", "诛诸吕", "political",
        -180, -180, "year", "period-western-han", "major",
        "前180年吕后去世，诸吕紧张图谋作乱；齐王刘襄举兵，太尉周勃、丞相陈平与朱虚侯刘章等"
        "合谋诛灭吕产、吕禄等诸吕，尽废吕氏所立，随后迎立代王刘恒为帝。"
        "诛诸吕结束了吕氏外戚专权，也是功臣集团与宗室联合重建朝局的关键政变。",
        f"古代史料：《史记·吕太后本纪》《孝文本纪》；现代参考：{MODERN['han']}",
        W["shiji"],
        [_rel("event-luhou-linchao", "follows"),
         _rel("event-hanwendi-jiwei", "leads_to", 0.9, desc="诛诸吕后迎立代王刘恒为汉文帝")],
        review_note="诛诸吕在前180年（高后八年九月十月间，以秦历岁首计或入前179年）；功臣、宗室、外戚三方博弈细节见《史记》。"),
    _ev("event-hanwendi-jiwei", "汉文帝即位", "political",
        -180, -180, "year", "period-western-han", "major",
        "前180年，代王刘恒在诛诸吕后被迎立为帝，是为汉文帝。"
        "汉文帝轻徭薄赋、约法省禁，开启汉初休养生息政策的进一步落实，"
        "与后来的汉景帝并称'文景'时期，奠定西汉国力恢复的基础。",
        f"古代史料：《史记·孝文本纪》；现代参考：{MODERN['han']}",
        W["shiji"],
        [_rel("event-zhulv", "follows"),
         _rel("event-wenjing-zhizhi", "leads_to", 0.85, desc="文帝即位后开启文景之治")],
        review_note="代王即位在前180年（文帝元年即前179年，以嵗首计有出入）；本库按通行在位纪年记-180。"),
    _ev("event-wenjing-zhizhi", "文景之治", "political",
        -179, -141, "range", "period-western-han", "major",
        "汉文帝、汉景帝两朝（约前179—前141年）轻徭薄赋、与民休息，"
        "社会富庶、仓廪充实，史家后世概括为\"文景之治\"（属后世历史概括）。"
        "本事件为治世过程节点，具体制度与政变见 削藩/七国之乱 等具体 Event。",
        f"古代史料：《汉书·食货志》及《文帝纪》《景帝纪》；现代参考：{MODERN['han']}",
        W["hanshu"],
        [_rel("event-hanwendi-jiwei", "follows"),
         _rel("event-chaocuo-xuefan", "precedes", desc="文景后期削藩问题浮出")],
        review_note="\"文景之治\"为后世对文帝景帝两朝治世的概括（同\"成康之治\"处理），不作为单一精确事件。"),
    _ev("event-chaocuo-xuefan", "晁错削藩", "political",
        -155, -154, "range", "period-western-han", "major",
        "汉景帝即位后，御史大夫晁错力主\"削藩\"以强干弱枝，"
        "前155年起议削诸王封地，前154年正式削楚、赵、胶西诸王部分郡县。"
        "削藩引发诸侯强烈反弹，成为七国之乱的直接导火索。",
        f"古代史料：《汉书·晁错传》《景帝纪》；现代参考：{MODERN['han']}",
        W["hanshu"],
        [_rel("event-wenjing-zhizhi", "follows"),
         _rel("event-qiguo-zhi-luan", "leads_to", 0.9, desc="削藩激化矛盾，直接引发七国之乱")],
        review_note="晁错上《削藩策》约在前155年，削藩令实施在前154年；\"清君侧\"名号亦为七国之乱口号。"),
    _ev("event-qiguo-zhi-luan", "七国之乱", "war",
        -154, -154, "year", "period-western-han", "critical",
        "前154年正月，吴王刘濞联合楚、赵、胶西、胶东、菑川、济南六国起兵叛乱，"
        "以\"诛晁错、清君侧\"为名；景帝杀晁错而乱不止，遣周亚夫平定，三月乱平。"
        "七国之乱是郡国并行体制下中央与诸侯王国矛盾的总爆发，"
        "战后诸侯王权力被大幅削弱，中央集权显著加强。",
        f"古代史料：《汉书·景帝纪》《吴王濞传》；现代参考：{MODERN['han']}",
        W["hanshu"],
        [_rel("event-chaocuo-xuefan", "follows"),
         _rel("event-hanwudi-jiwei", "precedes", desc="平乱后中央集权加强，为武帝时期集权奠定基础")],
        review_note="七国之乱前154年（景帝三年）为通行纪年；\"诛晁错\"与平乱经过见《汉书》。"),
    _ev("event-hanwudi-jiwei", "汉武帝即位", "political",
        -141, -141, "year", "period-western-han", "major",
        "前141年正月，汉景帝去世，太子刘彻即位，是为汉武帝（建元元年即前140年）。"
        "汉武帝在位五十四年，全面强化中央集权、开拓疆域，"
        "是中国历史上在位时间最长的皇帝之一，也是西汉由守成转向积极扩张的关键节点。",
        f"古代史料：《汉书·武帝纪》；现代参考：{MODERN['han']}",
        W["hanshu"],
        [_rel("event-qiguo-zhi-luan", "follows")],
        review_note="武帝即位于前141年（景帝后元三年正月）；本节点因开启武帝时期全局性变革而入主干（按§42判断）。"),
    _ev("event-han-xiongnu-war", "汉武帝对匈奴战争", "war",
        -133, -89, "range", "period-western-han", "major",
        "汉武帝时期汉匈由和亲转入大规模战争（约前133—前89年）："
        "马邑之谋始启战端，经卫青、霍去病多次出击，至漠北之战后匈奴主力远遁。"
        "本事件为 aggregate，子事件（马邑之谋/卫青首击/河南之战/河西之战/漠北之战）通过 part_of 关联。",
        f"古代史料：《史记·匈奴列传》《卫将军骠骑列传》、《汉书·匈奴传》；现代参考：{MODERN['han']}",
        W["shiji_hanshu"],
        [_rel("event-hanwudi-jiwei", "follows"),
         _rel("event-luntai-zhao", "precedes", desc="战争至轮台诏（前89）后休兵")],
        review_note="汉匈战争为约前133—前89年的长期进程（aggregate，起止取概略）；子事件见 part_of 关联。"),
    _ev("event-mayi-zhi-mou", "马邑之谋", "war",
        -133, -133, "year", "period-western-han", "major",
        "前133年，汉武帝采纳王恢之议，在马邑（今山西朔州）设伏诱击匈奴单于，"
        "因计划泄露未遂。马邑之谋虽未成功，却标志着汉匈和亲关系的终结，"
        "拉开双方大规模战争的序幕。",
        f"古代史料：《史记·韩长孺列传》《匈奴列传》；现代参考：{MODERN['han']}",
        W["shiji"],
        [_rel("event-han-xiongnu-war", "part_of", 0.9, desc="马邑之谋为汉匈战争开端"),
         _rel("event-hanhan-heqin", "follows", desc="和亲政策自此终结")],
        review_note="马邑之谋前133年（元光二年）为通行纪年；诱敌未遂细节见《史记》。"),
    _ev("event-weiqing-ji-longcheng", "卫青首战龙城", "war",
        -129, -129, "year", "period-western-han", "major",
        "前129年（元光六年），汉武帝派卫青、公孙敖等四路出击匈奴，"
        "其余三路多失利，唯卫青出上谷直捣龙城（匈奴祭天圣地）获捷。"
        "这是汉朝对匈奴的首次主动进攻并取胜，卫青自此崛起为抗匈主将。",
        f"古代史料：《史记·卫将军骠骑列传》；现代参考：{MODERN['han']}",
        W["shiji"],
        [_rel("event-han-xiongnu-war", "part_of", 0.9, desc="汉匈战争中的早期反击"),
         _rel("event-mayi-zhi-mou", "follows")],
        review_note="龙城之战前129年为《史记》系年；四路并出仅卫青一路有斩获。"),
    _ev("event-henan-zhizhan", "河南之战（收复河套）", "war",
        -127, -127, "year", "period-western-han", "major",
        "前127年（元朔二年），卫青率军出云中以西，攻取黄河以南（河南地）并修筑朔方城，"
        "置朔方郡。河南之战是汉匈战争首次大规模收复失地的战役，"
        "河套国防线南移，为后续反击提供前进基地。",
        f"古代史料：《史记·卫将军骠骑列传》《匈奴列传》；现代参考：{MODERN['han']}",
        W["shiji"],
        [_rel("event-han-xiongnu-war", "part_of", 0.9, desc="汉匈战争的重要战役"),
         _rel("event-weiqing-ji-longcheng", "follows")],
        review_note="河南之战前127年为《史记》系年；置朔方郡与筑城为同年措施。"),
    _ev("event-hexi-zhizhan", "河西之战（霍去病）", "war",
        -121, -121, "year", "period-western-han", "major",
        "前121年（元狩二年），霍去病两次出击河西走廊，大败匈奴，"
        "同年秋浑邪王降汉，汉朝将河西走廊收入版图，"
        "随后依次设置武威、张掖、酒泉、敦煌诸郡（约前121—前111年渐次完成）。",
        f"古代史料：《史记·卫将军骠骑列传》《匈奴列传》；现代参考：{MODERN['han']}",
        W["shiji"],
        [_rel("event-han-xiongnu-war", "part_of", 0.9, desc="汉匈战争的关键战役"),
         _rel("event-henan-zhizhan", "follows")],
        review_note="河西之战（前121）为两次战役与浑邪王降汉；河西四郡设郡时间有先后（约前121—前111），在 summary 内说明，不单列（避免碎片化，见 §22）。"),
    _ev("event-mobei-zhizhan", "漠北之战", "war",
        -119, -119, "year", "period-western-han", "critical",
        "前119年（元狩四年），汉军分两路深入漠北：卫青败单于主力，霍去病封狼居胥山，"
        "共斩俘匈奴八九万，匈奴主力远遁，\"漠南无王庭\"。"
        "漠北之战是汉匈战争决定性一役，标志汉对匈奴由防御转入全面反攻并取得战略优势，"
        "是汉武帝对匈奴战争的重要转折节点。",
        f"古代史料：《史记·卫将军骠骑列传》《匈奴列传》、《汉书·武帝纪》；现代参考：{MODERN['han']}",
        W["shiji_hanshu"],
        [_rel("event-han-xiongnu-war", "part_of", 0.9, desc="汉匈战争的决定性战役"),
         _rel("event-hexi-zhizhan", "follows")],
        review_note="漠北之战前119年为《史记》《汉书》系年；\"封狼居胥\"见于《史记》，斩俘数有记载口径差异。"),
    _ev("event-tui-en-ling", "推恩令", "reform",
        -127, -127, "year", "period-western-han", "major",
        "前127年（元朔二年），汉武帝采纳主父偃之策颁行推恩令，"
        "令诸侯王将封地析分子弟为侯国，由朝廷划定，名义上是施恩、实质是分封诸侯王势力。"
        "此后王国地权不断缩小，\"蕃国自析\"，诸侯王无力与中央对抗。",
        f"古代史料：《汉书·武帝纪》《主父偃传》；现代参考：{MODERN['han']}",
        W["hanshu"],
        [_rel("event-hanwudi-jiwei", "follows", desc="武帝集权措施之一")],
        review_note="推恩令前127年（元朔二年）为通行纪年；逐步化解诸侯的做法也为后世沿用。"),
    _ev("event-zhangqian-chuxi-1", "张骞第一次出使西域", "diplomatic",
        -138, -126, "range", "period-western-han", "major",
        "前138年（建元三年），汉武帝遣张骞出使西域联络大月氏共击匈奴，"
        "途中被匈奴扣留十余年，前126年方归汉。"
        "虽未达成军事联盟，但张骞带回西域诸国情势，\"凿空\"西域，为汉朝经营西域奠基。",
        f"古代史料：《史记·大宛列传》；现代参考：{MODERN['han']}",
        W["shiji"],
        [_rel("event-hanwudi-jiwei", "follows", desc="武帝对外战略的组成部分")],
        review_note="张骞首次出使（前138—前126）历时十三载，\"凿空\"为《史记》用语；所历路线与见闻见《大宛列传》。"),
    _ev("event-zhangqian-chuxi-2", "张骞第二次出使西域", "diplomatic",
        -119, -115, "range", "period-western-han", "major",
        "前119年（元狩四年），张骞奉命二次出使西域，"
        "携大量金币出使乌孙及大宛、大夏、安息诸国，前115年归汉。"
        "此次出使扩大汉与西域诸国外交联系，丝绸之路自此更为通畅。",
        f"古代史料：《史记·大宛列传》；现代参考：{MODERN['han']}",
        W["shiji"],
        [_rel("event-zhangqian-chuxi-1", "follows", desc="第二次出使西域")],
        review_note="二次出使（约前119—前115）；乌孙\"昆莫\"等邦国关系为汉朝经营西域的关键环节。"),
    _ev("event-hanwudi-caizheng", "汉武帝财政集权（盐铁官营、均输平准、算缗告缗）", "economic",
        -119, -110, "range", "period-western-han", "major",
        "为支撑连年战争，汉武帝推行系列财政集权政策：约前119年起盐铁官营、行算缗，"
        "前114年前后杨可告缗贯行，前110年前后桑弘羊主持均输平准，"
        "将铸币、盐铁、贸易利润收归中央。这些政策大幅增加国库收入，"
        "也造成工商业受挫与民力过度征调。",
        f"古代史料：《史记·平准书》《汉书·食货志》；现代参考：{MODERN['han']}",
        W["shiji_hanshu"],
        [_rel("event-mobei-zhizhan", "follows", desc="战争需求推动财政集权"),
         _rel("event-cishi-jiancha", "precedes", desc="财政与监察改革同属武帝集权进程")],
        review_note="盐铁官营、算缗告缗、均输平准为逐个推出的系列政策（约前119—前110），各分项年代有细微出入，聚合为事件并标注 range。"),
    _ev("event-cishi-jiancha", "设置十三州刺史", "reform",
        -106, -106, "year", "period-western-han", "major",
        "前106年（元封五年），汉武帝除京师附近七郡外，分全国为十三州（部），"
        "各置刺史一人，以'六条问事'监察地方二千石长吏。"
        "刺史制度是中央监察地方的专职化设置，汉代监察体系由此制度化。",
        f"古代史料：《汉书·武帝纪》；现代参考：{MODERN['han']}",
        W["hanshu"],
        [_rel("event-hanwudi-caizheng", "follows", desc="武帝集权制度建设的组成部分")],
        review_note="十三州刺史部前106年设置；刺史初为监察官，其后渐成州牧地方官（变化发生在东汉），此处记录设立节点。"),
    _ev("event-taichu-gaili", "太初改历", "reform",
        -104, -104, "year", "period-western-han", "major",
        "前104年（太初元年），汉武帝采纳公孙卿等建议改用新历（太初历），"
        "正月为岁首、以元封七年改为太初元年，并施行史记纪年体系。"
        "太初历（邓平、落下闳等所制）是当时较精密的历法，其后长期沿用。",
        f"古代史料：《汉书·律历志》《武帝纪》；现代参考：{MODERN['han']}",
        W["hanshu"],
        [_rel("event-cishi-jiancha", "follows", desc="武帝时期制度建设的组成部分")],
        review_note="太初改历前104年；改历为天文历法领域重大事件，其精度与施行有专门研究。"),
    _ev("event-dongzhongshu-cedui", "董仲舒贤良对策", "political",
        -140, -134, "approximate", "period-western-han", "major",
        "汉武帝诏举贤良方正，董仲舒上'天人三策'，主张\"罢黜百家，表章六经\"、"
        "以儒学统一思想并设立太学以养士（对策年代有建元元年/元光元年二说）。"
        "此对策为儒学由私学进入官方意识形态的重要环节，但儒学官学化是一个长期过程。",
        f"古代史料：《汉书·董仲舒传》；现代参考：{MODERN['han']}；另见田余庆《秦汉魏晋史探微》相关讨论",
        W["hanshu"],
        [_rel("event-wujing-boshi", "follows", desc="五经博士先设、对策继之，为儒学官学化进程"),
         _rel("event-hanwudi-jiwei", "follows")],
        review_note="《汉书·董仲舒传》对策年代有建元元年（前140）与元光元年（前134）两说，学界仍有讨论；本库取通行线索并标 approximate（详见 QIN_HAN_BACKBONE_REVIEW.md）。\"罢黜百家，独尊儒术\"为后世概括语，不按精确日期立项。"),
    _ev("event-wujing-boshi", "设置五经博士", "reform",
        -136, -136, "year", "period-western-han", "major",
        "前136年（建元五年），汉武帝设置五经（诗、书、礼、易、春秋）博士，"
        "取代此前杂学博士，儒经研习由此列入朝廷官学。"
        "这是汉初'罢黜百家'潮流中儒学官学化的制度性标志。",
        f"古代史料：《汉书·武帝纪》《儒林传》；现代参考：{MODERN['han']}",
        W["hanshu"],
        [_rel("event-hanwudi-jiwei", "follows", desc="武帝初年儒学官学化的制度措施")],
        review_note="建元五年（前136）设置五经博士为通行纪年；博士官制由诸子学转向经学的过程在武帝时期完成。"),
    _ev("event-wugu-zhi-huo", "巫蛊之祸", "political",
        -91, -91, "year", "period-western-han", "major",
        "前91年（征和二年），汉武帝晚年巫蛊案扩大，江充构陷太子刘据，"
        "太子起兵诛江充后兵败自杀，皇后卫子夫亦死，牵连甚广，"
        "史称巫蛊之祸。此案是武帝晚年最大政治悲剧，动摇储位并深刻影响其后政局。",
        f"古代史料：《汉书·武帝纪》《戾太子传》；现代参考：{MODERN['han']}；田余庆《汉魏之际的眼光与史实》相关讨论",
        W["hanshu"],
        [_rel("event-taichu-gaili", "follows", desc="武帝后期政治危机"),
         _rel("event-luntai-zhao", "leads_to", 0.8, desc="巫蛊之祸后汉武帝反思，晚年政策转向（轮台诏）")],
        review_note="巫蛊之祸前91年为《汉书》系年；巫蛊案政治背景（储位之争、酷吏政治）为学界长期讨论对象。"),
    _ev("event-luntai-zhao", "轮台诏", "political",
        -89, -89, "year", "period-western-han", "major",
        "前89年（征和四年），汉武帝颁布轮台诏（《轮台诏》），"
        "罪己悔过，罢罢轮台屯田，宣布\"当今务在禁苛暴、止擅赋、力本农\"，政策转向休养。"
        "轮台诏标志着武帝晚年对连年征伐与酷政的反思，为昭宣时期的政策基调定下方向。",
        f"古代史料：《汉书·西域传》《武帝纪》；现代参考：{MODERN['han']}",
        W["hanshu"],
        [_rel("event-wugu-zhi-huo", "follows", desc="武帝晚年政策转向"),
         _rel("event-wudi-si-huoguang", "precedes", desc="轮台诏后两年武帝去世，霍光辅政")],
        review_note="轮台诏之'罪己'性质与具体措施（罢轮台屯田）为学界公认；其政策转向意义在昭宣时期体现（田余庆《轮台诏与汉帝国的转折》）。"),
    _ev("event-wudi-si-huoguang", "汉武帝去世与霍光辅政", "political",
        -87, -87, "year", "period-western-han", "major",
        "前87年（后元二年），汉武帝临终立少子弗陵（汉昭帝），"
        "以霍光、金日磾、上官桀等为辅政大臣，以霍光为首。"
        "武帝去世后，西汉进入昭宣时期，霍光长期执掌朝政。",
        f"古代史料：《汉书·武帝纪》《霍光传》；现代参考：{MODERN['han']}",
        W["hanshu"],
        [_rel("event-luntai-zhao", "follows"),
         _rel("event-changyi-wang-feili", "leads_to", 0.85, desc="霍光辅政延续至昭帝崩后的废立")],
        review_note="武帝崩于前87年（后元二年二月）；托孤辅政体制自此确立。"),
    _ev("event-changyi-wang-feili", "昌邑王废立（霍光废昌邑王、立汉宣帝）", "political",
        -74, -74, "year", "period-western-han", "major",
        "前74年（元平元年），汉昭帝去世无嗣，霍光等迎立昌邑王刘贺即位；"
        "刘贺在位仅二十七日，霍光以荒淫无道为由奏废之，改立戾太子之孙刘询（汉宣帝）。"
        "此事件展现霍光对皇位继承的主导权，也是西汉中期权力交接的标志性节点。",
        f"古代史料：《汉书·霍光传》《宣帝纪》；现代参考：{MODERN['han']}",
        W["hanshu"],
        [_rel("event-wudi-si-huoguang", "follows"),
         _rel("event-huo-shi-fumie", "leads_to", 0.7, desc="霍氏权势顶峰后于宣帝时期被诛灭")],
        review_note="刘贺在位二十七日被废（元平元年），近年海昏侯墓出土刘贺相关文物；废立理由存在不同解读。"),
    _ev("event-huo-shi-fumie", "霍氏集团覆灭", "political",
        -66, -66, "year", "period-western-han", "major",
        "前68年霍光去世，汉宣帝逐渐收权；前66年（地节四年），"
        "宣帝以谋反罪族诛霍氏，废皇后霍氏，霍氏当权时代终结。"
        "此后皇权回归，宣帝亲政，出现\"中兴\"局面。",
        f"古代史料：《汉书·霍光传》《宣帝纪》；现代参考：{MODERN['han']}",
        W["hanshu"],
        [_rel("event-changyi-wang-feili", "follows")],
        review_note="霍光卒于前68年、族诛在前66年；\"霍氏之祸始于骖乘\"之论见《汉书》。"),
    _ev("event-xiyu-duhu", "西域都护设置", "diplomatic",
        -60, -60, "year", "period-western-han", "major",
        "前60年（神爵二年），匈奴日逐王降汉，汉朝以郑吉为西域都护，"
        "立幕府于乌垒城，管辖西域三十六国，西域自此正式纳入汉朝行政统辖体系。"
        "西域都护为汉朝管理西域的最高长官制度，一直延续到西汉末。",
        f"古代史料：《汉书·西域传》《郑吉传》；现代参考：{MODERN['han']}",
        W["hanshu"],
        [_rel("event-huo-shi-fumie", "follows", desc="昭宣时期西域经营成果")],
        review_note="西域都护设置时间通行取神爵二年（前60）；偶见前68、前59年等说，详见 QIN_HAN_BACKBONE_REVIEW.md。"),
    _ev("event-han-yuandi-jiwei", "汉元帝即位", "political",
        -48, -48, "year", "period-western-han", "major",
        "前48年，汉宣帝去世，太子刘奭即位，是为汉元帝。"
        "元帝朝重用宦官石显、外戚王氏势力渐起，"
        "西汉由昭宣中兴转入中后期，外戚与宦官政治影响开始显现。",
        f"古代史料：《汉书·元帝纪》；现代参考：{MODERN['han']}",
        W["hanshu"],
        [_rel("event-xiyu-duhu", "follows", desc="西汉转入中后期")],
        review_note="元帝即位于前48年（黄龙元年十二月/初元元年）；\"柔仁好儒\"与宦官用事之史料见《汉书》。"),
    _ev("event-wangfeng-waigi", "王凤辅政与王氏外戚崛起", "political",
        -33, -33, "year", "period-western-han", "major",
        "前33年汉元帝去世，成帝即位，太后王政君之兄王凤任大司马大将军领尚书事，"
        "王氏外戚自此执掌朝政，一门十侯，王莽亦由此家族登上政治舞台。"
        "王氏家族崛起是西汉末年权力中枢转移的关键节点。",
        f"古代史料：《汉书·元后传》《王莽传》；现代参考：{MODERN['han']}",
        W["hanshu"],
        [_rel("event-han-yuandi-jiwei", "follows", desc="外戚政治进入中枢")],
        review_note="王凤辅政始于前33年（元帝崩、成帝即位）；王氏\"一门五将十侯\"为《汉书》记载。"),
    _ev("event-wangmang-fuchu", "王莽复出辅政", "political",
        -1, -1, "year", "period-western-han", "major",
        "汉哀帝去世（前1年）后无嗣，太后王政君与王莽共立中山王（汉平帝），"
        "王莽复任大司马、录尚书事，重新执掌朝政，遂成西汉末年的实际掌权者。"
        "王莽此后声望日隆，逐步走向居摄与禅代。",
        f"古代史料：《汉书·王莽传》《平帝纪》；现代参考：{MODERN['han']}",
        W["hanshu"],
        [_rel("event-wangfeng-waigi", "follows", desc="王氏外戚势力在哀帝死后重新掌权")],
        review_note="平帝九岁即位，王莽以大司马辅政；\"安汉公\"等新封号陆续加于王莽。"),
    _ev("event-wangmang-jushe", "王莽居摄", "political",
        6, 8, "range", "period-western-han", "major",
        "公元6年，汉平帝去世后王莽立孺子婴为皇太子，自任\"假皇帝\"、居摄践祚，"
        "改元居摄、初始，至公元8年（初始元年）十一月正式接受禅让称帝。"
        "居摄是王莽由辅政到代汉的关键过渡阶段。",
        f"古代史料：《汉书·王莽传》；现代参考：{MODERN['han']}",
        W["hanshu"],
        [_rel("event-wangmang-fuchu", "follows", desc="由辅政进而居摄"),
         _rel("event-wangmang-chengdi", "leads_to", 0.95, desc="居摄三年后王莽正式代汉称帝")],
        review_note="居摄元年为公元6年（居摄三载至初始元年即公元8年）；\"假皇帝\"称号与禅让程序见《汉书》。"),
]

# ---------------------------------------------------------------------------
# Phase X — 新
# ---------------------------------------------------------------------------
PHASE_XIN = [
    _ev("event-wangmang-chengdi", "王莽称帝、新朝建立", "dynastic-transition",
        9, 9, "year", "period-xin", "critical",
        "公元9年（初始元年十二月/始建国元年），王莽接受刘氏禅让称帝，"
        "改国号曰\"新\"，废汉朝年号，西汉刘氏统治终结。"
        "王莽代汉是中国历史上第一次以外戚身份通过禅让程序改朝换代，"
        "也是西汉外戚政治的终局。",
        f"古代史料：《汉书·王莽传》；现代参考：{MODERN['xin']}",
        W["hanshu"],
        [_rel("event-wangmang-jushe", "follows", desc="居摄三年后禅代"),
         _rel("event-xin-gaizhi", "leads_to", 0.85, desc="建立新朝后全面推行改制")],
        review_note="王莽称帝在初始元年末（公元9年1月，通行记公元9年）；\"禅让\"性质的争议（篡位或禅代）为后世史评话题。"),
    _ev("event-xin-gaizhi", "王莽改制（新朝制度变革）", "reform",
        9, 17, "range", "period-xin", "major",
        "王莽称帝后推行大规模制度变革：始建国元年（9年）行王田、私属制，"
        "禁奴婢买卖，行五均六筦、盐铁专卖；屡次改革币制（四十八品），"
        "并大改官制、郡县与地名，改制周边邦国名号。"
        "改制触动广泛利益且政令繁苛，激化社会矛盾，是导致新朝迅速动荡的主要原因。",
        f"古代史料：《汉书·王莽传》《食货志》；现代参考：{MODERN['xin']}",
        W["hanshu"],
        [_rel("event-wangmang-chengdi", "follows", desc="新朝建立后随即改制"),
         _rel("event-lvlin-qiyi", "leads_to", 0.7, desc="改制失败与社会矛盾激化导向绿林赤眉起义")],
        review_note="王莽改制为一系列政策的总称（约公元9—17年），王田、币改、官制改名等各有具体年份；"
                    "按 §18 原则聚合为单事件，不逐条单列。改制的得失与动因为长期学术课题。"),
    _ev("event-lvlin-qiyi", "绿林起义", "rebellion",
        17, 17, "year", "period-xin", "major",
        "公元17年（天凤四年），荆州饥民在王匡、王凤等率领下聚于绿林山（今湖北大洪山一带）起义，"
        "号\"绿林军\"。绿林军后来成为反新主力，公元22年遭王莽军重创后分路活动，"
        "更始政权与刘秀势力皆由绿林部曲发展而来。",
        f"古代史料：《后汉书·刘玄传》及《光武帝纪》；现代参考：{MODERN['xin']}",
        W["houhanshu"],
        [_rel("event-xin-gaizhi", "follows", desc="改制失败后社会动荡"),
         _rel("event-kunyang-zhizhan", "leads_to", 0.85, desc="绿林军发展为反新主力，与新军决战于昆阳")],
        review_note="绿林起义公元17年（天凤四年）为通行纪年；\"绿林\"一词由此成为义军代称。"),
    _ev("event-chimei-qiyi", "赤眉起义", "rebellion",
        18, 18, "year", "period-xin", "major",
        "公元18年（天凤五年），樊崇等聚众于泰山一带起义，"
        "以朱色涂眉为号，故称\"赤眉军\"。赤眉军与绿林军并行为新末两大起义力量，"
        "与新朝官军反复交战，后成为关东地区的强大反新势力。",
        f"古代史料：《后汉书·刘盆子传》；现代参考：{MODERN['xin']}",
        W["houhanshu"],
        [_rel("event-lvlin-qiyi", "follows", desc="与新末其他起义并举"),
         _rel("event-xin-mie", "precedes", desc="赤眉军亦参与推翻新朝之战")],
        review_note="赤眉起义公元18年（天凤五年）；\"赤眉\"为起义军标志称谓。"),
    _ev("event-kunyang-zhizhan", "昆阳之战", "war",
        23, 23, "year", "period-xin", "major",
        "公元23年（更始元年）三月，绿林军建立更始政权；王莽遣王邑、王寻率号称四十二万大军围攻昆阳（今河南叶县一带），"
        "刘秀率数千守军以奇袭大破之，新军主力溃败。"
        "昆阳之战是新莽政权的决定性军事失败，直接导致新朝灭亡。",
        f"古代史料：《后汉书·光武帝纪》；现代参考：{MODERN['xin']}",
        W["houhanshu"],
        [_rel("event-lvlin-qiyi", "follows"),
         _rel("event-xin-mie", "leads_to", 0.9, desc="昆阳大捷后更始军进长安，王莽被杀，新朝灭亡"),
         _rel("event-guangwu-chengdi", "contributes_to", 0.7, desc="刘秀因昆阳之战声望大增，为其后称帝奠定基础")],
        review_note="昆阳之战公元23年六月（更始元年）；\"四十二万\"为新军规模的传统记载，实际兵力有讨论。"),
    _ev("event-xin-mie", "新朝灭亡", "dynastic-transition",
        23, 23, "year", "period-xin", "critical",
        "公元23年十月，更始军攻入长安，王莽被杀于渐台，新朝灭亡。"
        "新朝的失败结束了王莽改制试验，中国历史进入更始与群雄争夺、"
        "刘秀重建汉室的东汉建立阶段。",
        f"古代史料：《汉书·王莽传》《后汉书·光武帝纪》；现代参考：{MODERN['xin']}",
        W["houhanshu"],
        [_rel("event-kunyang-zhizhan", "follows", desc="昆阳战后新朝迅速崩溃"),
         _rel("event-guangwu-chengdi", "leads_to", 0.8, desc="新亡后群雄并起，刘秀于公元25年称帝建立东汉")],
        review_note="王莽被杀于公元23年十月（地皇四年/更始元年）；\"绿林赤眉并举、更始入长安\"为通行叙事。"),
]

# ---------------------------------------------------------------------------
# Phase EH — 东汉
# ---------------------------------------------------------------------------
PHASE_EASTERN_HAN = [
    _ev("event-guangwu-chengdi", "刘秀称帝、东汉建立", "dynastic-transition",
        25, 25, "year", "period-eastern-han", "critical",
        "公元25年（更始三年/建武元年）六月，刘秀在鄗县（今河北柏乡一带）称帝，"
        "仍用\"汉\"国号，史称后汉或东汉；随后定都洛阳。"
        "东汉的建立结束了新莽以来的政治混乱，中国历史进入东汉时代。",
        f"古代史料：《后汉书·光武帝纪》；现代参考：{MODERN['donghan']}",
        W["houhanshu"],
        [_rel("event-xin-mie", "follows", desc="新亡后群雄争鼎，刘秀重建汉室"),
         _rel("event-kunyang-zhizhan", "follows", desc="昆阳之战的威望助刘秀在河北立足称帝")],
        review_note="刘秀称帝于公元25年六月（鄗南），定都洛阳；更始政权（刘玄）随后被赤眉攻灭。"),
    _ev("event-guangwu-tongyi", "光武统一战争", "war",
        25, 36, "range", "period-eastern-han", "major",
        "刘秀称帝后继续扫平割据势力：先后击灭更始余部与赤眉（27年）、"
        "平定刘永、彭宠、卢芳等，至建武十二年（36年）灭公孙述（成家政权），"
        "重新完成全国统一。光武统一战争历时十余年，史称\"光武中兴\"的基础。",
        f"古代史料：《后汉书·光武帝纪》及诸传记；现代参考：{MODERN['donghan']}",
        W["houhanshu"],
        [_rel("event-guangwu-chengdi", "follows", desc="称帝后继续统一战争"),
         _rel("event-guangwu-dutian", "precedes", desc="统一后转入制度建设（度田等）")],
        review_note="光武统一战争（公元25—36年）为过程事件；灭公孙述在建武十二年（36年）。\"光武中兴\"为后世概括。"),
    _ev("event-guangwu-dutian", "光武帝度田", "political",
        39, 40, "range", "period-eastern-han", "major",
        "建武十五年（39年），光武帝下令度田（清核全国垦田数）以整顿赋税，"
        "地方豪强阻挠、刺史太守贪赃枉法，建武十六年（40年）青徐幽冀等州爆发反抗；"
        "光武帝严厉处治失职官员并安抚郡国，度田最终以不了了之收场。"
        "度田反映了东汉初年政府与豪强势力在土地、赋役问题上的矛盾。",
        f"古代史料：《后汉书·光武帝纪》；现代参考：{MODERN['donghan']}；另见田余庆《秦汉魏晋史探微》",
        W["houhanshu"],
        [_rel("event-guangwu-tongyi", "follows", desc="统一后整顿田制"),
         _rel("event-hanmingdi-jiwei", "precedes", desc="度田及其余波后光武朝转入稳定")],
        review_note="度田年限为建武十五年（39）至十六年（40）；其成效与失败点（豪强阻力）为东汉史重要课题。"),
    _ev("event-hanmingdi-jiwei", "汉明帝即位", "political",
        57, 57, "year", "period-eastern-han", "major",
        "公元57年光武帝去世，太子刘庄即位，是为汉明帝。"
        "明帝朝继承光武政策，吏治严明，对外经营西域（窦固北征、班超出使），"
        "并诏令迎佛经（\"永平求法\"），东汉由此进入明章时期。",
        f"古代史料：《后汉书·光武帝纪》《明帝纪》；现代参考：{MODERN['donghan']}",
        W["houhanshu"],
        [_rel("event-guangwu-dutian", "follows", desc="东汉前期权力交接"),
         _rel("event-banchao-jingying-xiyu", "leads_to", 0.7, desc="明帝朝重开对西域的经略")],
        review_note="明帝即位于公元57年；\"永平求法\"之传统记载与 佛教传入 事件相衔接（见该事件 review_note）。"),
    _ev("event-fojiao-chuanru", "佛教传入与早期佛教活动", "cultural",
        67, 67, "approximate", "period-eastern-han", "major",
        "传统记载称汉明帝永平年间（一说永平十年，公元67年）遣使往西域取经，"
        "白马驮经归洛阳，敕建白马寺供养，佛教自此正式传入中国并译经渐兴；"
        "另据近年研究，佛教通过丝绸之路零星传入中国或早于此时，传入是一个过程而非单一事件。",
        f"古代史料：《后汉书》相关记载与《牟子理惑论》等传统叙述；现代参考：{MODERN['donghan']}",
        W["houhanshu"],
        [_rel("event-hanmingdi-jiwei", "follows", desc="传统记载\"永平求法\"系于明帝朝")],
        review_note="\"白马寺/永平求法\"为传统说法，属后世追述成分居多（《后汉书》未载白马寺建寺细节）；"
                    "学界普遍认为佛教传入为渐进过程、时间早于或晚于永平十年均有讨论，故标 approximate 并如实在 review_note 说明，不按传说伪装精确事实（§21/§49）。"),
    _ev("event-banchao-jingying-xiyu", "班超经营西域", "diplomatic",
        73, 91, "range", "period-eastern-han", "major",
        "永平十六年（73年）窦固北征匈奴时，班超随军出使西域，"
        "以\"不入虎穴，焉得虎子\"之胆识杀匈奴使者镇抚鄯善、于阗、疏勒诸国，"
        "此后数十年经营西域，重建汉朝在西域的统治；"
        "永元三年（91年）班超任西域都护，永元九年（97年）遣甘英出使大秦（罗马）方向。",
        f"古代史料：《后汉书·班超传》《西域传》；现代参考：{MODERN['donghan']}",
        W["houhanshu"],
        [_rel("event-hanmingdi-jiwei", "follows", desc="明帝朝重开西域经略"),
         _rel("event-dougu-beixiong", "precedes", desc="窦固北伐为同期对外经略")],
        review_note="班超经营西域（73—91）；甘英使大秦止于安息（波斯），未达罗马本土，\"大秦\"方位为当时认知。"),
    _ev("event-dougu-beixiong", "窦固窦宪北伐匈奴（燕然勒石）", "war",
        89, 91, "range", "period-eastern-han", "major",
        "永元元年（89年），车骑将军窦宪与耿秉等大破北匈奴于稽落山，"
        "登燕然山刻石纪功（燕然勒石）；90年再破之，91年北匈奴单于西遁，"
        "北匈奴政权瓦解。此役为东汉对北方匈奴的最后决定性胜利，"
        "但窦宪班师后权倾朝野，旋被和帝诛灭。",
        f"古代史料：《后汉书·窦宪传》《南匈奴传》；现代参考：{MODERN['donghan']}",
        W["houhanshu"],
        [_rel("event-banchao-jingying-xiyu", "follows", desc="同期对北族的军事经略"),
         _rel("event-he-di-zhu-dou", "leads_to", 0.9, desc="窦宪功高震主，和帝与宦官诛灭窦氏")],
        review_note="燕然勒石（89年）为《后汉书》记载；近年燕然山铭摩崖出土为其印证。北匈奴之后的去向与影响为专门课题。"),
    _ev("event-he-di-zhu-dou", "和帝诛灭窦氏", "political",
        92, 92, "year", "period-eastern-han", "major",
        "永元四年（92年），汉和帝与外兄宦官郑众等合谋，收捕窦宪及其党羽，"
        "窦宪自杀，窦氏外戚集团覆灭。此事件中宦官首次参与废立式政治行动并获封侯，"
        "东汉\"外戚—宦官\"交替掌权的政治格局自此展开。",
        f"古代史料：《后汉书·窦宪传》《宦者列传》；现代参考：{MODERN['donghan']}",
        W["houhanshu"],
        [_rel("event-dougu-beixiong", "follows", desc="窦宪北伐后权倾朝野"),
         _rel("event-deng-taihou", "precedes", desc="和帝后外戚政治继续以临朝形式延续")],
        review_note="和帝诛窦氏于永元四年（92年）；郑众以功封侯，宦官由此进入东汉政治核心。"),
    _ev("event-deng-taihou", "邓太后临朝", "political",
        105, 121, "range", "period-eastern-han", "major",
        "元兴元年（105年）和帝去世，邓太后与兄邓骘迎立殇帝、安帝，"
        "邓太后临朝称制近二十年（105—121年），邓氏一门贵宠，"
        "朝政大体得以维持而豪强、羌乱等矛盾积聚。邓太后去世后邓氏旋即被清算。",
        f"古代史料：《后汉书·和熹邓皇后纪》；现代参考：{MODERN['donghan']}",
        W["houhanshu"],
        [_rel("event-he-di-zhu-dou", "follows", desc="和帝后外戚临朝延续"),
         _rel("event-huangguan-li-shundi", "leads_to", 0.7, desc="邓后去世、安帝亲政后，宦官在继承危机中再度崛起")],
        review_note="邓太后临朝（105—121）为东汉中期外戚政治的典型阶段；其执政功过（灾荒应对与羌乱应对）见诸史评。"),
    _ev("event-huangguan-li-shundi", "宦官拥立汉顺帝", "political",
        125, 125, "year", "period-eastern-han", "major",
        "延光四年（125年），汉安帝去世，阎皇后临朝废太子（济阴王）；"
        "宦官孙程等十九人合谋诛阎显集团，拥立济阴王即位，是为汉顺帝。"
        "这是宦官集团首次拥立皇帝，宦官政治由此正式进入东汉权力核心。",
        f"古代史料：《后汉书·宦者列传》《顺帝纪》；现代参考：{MODERN['donghan']}",
        W["houhanshu"],
        [_rel("event-deng-taihou", "follows", desc="外戚与宦官交替的典型节点"),
         _rel("event-liangji-zhuanquan", "leads_to", 0.7, desc="顺帝朝梁氏外戚梁冀权势上升")],
        review_note="宦官拥立顺帝于延光四年（125年）十一月；\"十九侯\"为《后汉书》记载，宦官政治自此制度化。"),
    _ev("event-liangji-zhuanquan", "梁冀专权", "political",
        144, 159, "range", "period-eastern-han", "major",
        "顺帝、冲帝、质帝、桓帝前期，梁冀以外戚为大将军执掌朝政十余年（约144—159年），"
        "废立冲质桓三帝、毒杀质帝，权倾天下；"
        "延熹二年（159年）汉桓帝与宦官单超等合谋收捕梁冀，梁氏被族灭，"
        "梁冀家产没入官府，宦官五侯自此掌权。",
        f"古代史料：《后汉书·梁冀传》《宦者列传》；现代参考：{MODERN['donghan']}",
        W["houhanshu"],
        [_rel("event-huangguan-li-shundi", "follows", desc="梁氏外戚自顺帝朝崛起"),
         _rel("event-danggu-1", "leads_to", 0.8, desc="诛梁冀后宦官专权，士人清议与宦官冲突酿成党锢之祸")],
        review_note="梁冀专权（约144—159）为过程事件；\"跋扈将军\"毒杀质帝之记载见《梁冀传》。"),
    _ev("event-hanqiang-zhanzheng", "汉羌战争", "war",
        107, 169, "range", "period-eastern-han", "major",
        "东汉中后期与羌人连年战争（较大规模约107—118、135—145、159—169三阶段），"
        "汉朝耗费巨额军费、迁民避羌，关中、凉州残破，"
        "\"百年羌祸\"成为东汉财政与边防的沉重负担，间接影响东汉末年的政治格局。",
        f"古代史料：《后汉书·西羌传》；现代参考：{MODERN['donghan']}",
        W["houhanshu"],
        [_rel("event-deng-taihou", "follows", desc="永初年间首轮大规模羌乱"),
         _rel("event-danggu-2", "precedes", desc="羌乱耗费与党锢同为东汉中后期衰象")],
        review_note="汉羌战争为长期低烈度战争（分期与起讫有不同口径），本事件按 §27 作为\"羌乱\"主干节点，细分战役未单列。"),
    _ev("event-danggu-1", "第一次党锢之祸", "political",
        166, 167, "range", "period-eastern-han", "major",
        "延熹九年（166年），宦官集团以\"结党诽谤朝政\"之名逮捕李膺、陈蕃、杜密等二百余人，"
        "是为第一次党锢；次年（167年）在窦武等请求下赦还田里，但禁锢终身不得仕。"
        "党锢是东汉后期士人（清流）与宦官斗争的总爆发，也是东汉政治危机的标志。",
        f"古代史料：《后汉书·党锢列传》；现代参考：{MODERN['donghan']}；另见田余庆《秦汉魏晋史探微》",
        W["houhanshu"],
        [_rel("event-liangji-zhuanquan", "follows", desc="诛除梁冀后宦官独大，士人清议遂遭党锢"),
         _rel("event-danggu-2", "leads_to", 0.9, desc="第一次党锢未息士人斗志，十年后祸再起")],
        review_note="第一次党锢（166—167年）与第二次党锢（169年）为不同阶段，分列两事件（§26）；\"党人\"名单与株连见《党锢列传》。"),
    _ev("event-danggu-2", "第二次党锢之祸", "political",
        169, 169, "year", "period-eastern-han", "major",
        "建宁二年（169年），宦官侯览等借张俭事案大兴党狱，"
        "李膺、范滂等百余人被下狱处死或自杀，妻子徙边，天下士人被禁锢者六七百人，"
        "党锢之祸达于极盛；直到中平元年（184年）黄巾起义爆发才大赦党人。"
        "第二次党锢使士大夫政治力量受到毁灭性打击，东汉政局进一步恶化。",
        f"古代史料：《后汉书·党锢列传》；现代参考：{MODERN['donghan']}",
        W["houhanshu"],
        [_rel("event-danggu-1", "follows", desc="第一次党锢后的再度大狱"),
         _rel("event-three-yellow-turbans", "precedes", desc="黄巾起义（184）爆发后朝廷大赦党人，党锢终结")],
        review_note="第二次党锢（169年，延至184年赦党人）；\"党人\"死徙之惨烈与比例见《党锢列传》。与黄巾起义（复用既有 event-three-yellow-turbans）衔接为东汉主干结尾。"),
]

ALL_PHASES = [
    ("qin_han", "Phase Q（秦/楚汉）", PHASE_QIN),
    ("qin_han", "Phase WH（西汉）", PHASE_WESTERN_HAN),
    ("qin_han", "Phase X（新）", PHASE_XIN),
    ("qin_han", "Phase EH（东汉）", PHASE_EASTERN_HAN),
]

PHASE_BY_NAME = {"QIN": PHASE_QIN, "WESTERN_HAN": PHASE_WESTERN_HAN, "XIN": PHASE_XIN, "EASTERN_HAN": PHASE_EASTERN_HAN}


def all_events():
    return [(dir_, label, ev) for dir_, label, events in ALL_PHASES for ev in events]