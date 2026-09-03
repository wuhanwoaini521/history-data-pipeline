# -*- coding: utf-8 -*-
"""China History Backbone V1 — Batch 1（先秦）Curated Event Data。

本文件是 Batch 1（上古/夏/商/西周/春秋/战国，约 82 个 critical/major Event）的
curated 数据源。由 scripts/backbone_batch1_write.py 写入：
- data/curated/history_backbone/events/pre_qin/        （Phase A）
- data/curated/history_backbone/events/chunqiu_zhanguo/（Phase B/C）
- data/reviews/accepted/<event_id>.review.json         （审核记录）
- data/candidates/backbone_events/*_candidates.yml     （候选清单）

原则（见项目 China History Backbone V1 说明）：
- Event First, Evidence Later：本批不填写 people/places/evidence 关联，
  只维护 source_reference（古代史料 + 现代参考两层）。
- 夏商周早期纪年一律 date_precision=approximate，不伪装精确年代；
  具体争议见 reports/EARLY_HISTORY_UNCERTAINTY.md。
- 关系只使用安全关系（precedes/follows）与有来源的 curated 因果
  （leads_to / contributes_to / part_of）。
"""

from __future__ import annotations

# 现代参考资料池（source_reference 内引用；source_ids 内的 work 见下）
MODERN_REF = {
    "requirements": "夏商周断代工程专家组《夏商周断代工程1996—2000年阶段成果报告·简本》（世界图书出版公司，2000）；"
                    "张岂之主编《中国历史·先秦卷》（高等教育出版社，2001）；白寿彝总主编《中国通史》",
    "xia_shang_zhou": "夏商周断代工程专家组《夏商周断代工程1996—2000年阶段成果报告·简本》；许倬云《西周史（增订本）》（三联书店）；"
                      "张岂之主编《中国历史·先秦卷》",
    "chunqiu": "童书业《春秋史》（上海人民出版社）；张岂之主编《中国历史·先秦卷》；白寿彝总主编《中国通史》",
    "zhanguo": "杨宽《战国史（增订本）》（上海人民出版社，2016）；张岂之主编《中国历史·先秦卷》；白寿彝总主编《中国通史》",
}

# 每条 Event 的 source_ids：可用 work 种子（reference.knowledge_seed_rows 已登记）
# work-curated-shiji / zuozhuan / shangshu / guoyu / zhushu-jinian / zhanguoce / chunqiu
W = {
    "shiji": ["work-curated-shiji"],
    "zuozhuan": ["work-curated-zuozhuan"],
    "shiji_zuozhuan": ["work-curated-shiji", "work-curated-zuozhuan"],
    "shiji_shangshu": ["work-curated-shiji", "work-curated-shangshu"],
    "shiji_zhushu": ["work-curated-shiji", "work-curated-zhushu-jinian"],
    "zuozhuan_guoyu": ["work-curated-zuozhuan", "work-curated-guoyu"],
    "zhanguoce": ["work-curated-zhanguoce"],
    "shiji_zhanguoce": ["work-curated-shiji", "work-curated-zhanguoce"],
    "zuozhuan_shiji": ["work-curated-zuozhuan", "work-curated-shiji"],
}

_M = MODERN_REF


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
        "id": id_,
        "name_zh_cn": name,
        "event_type": etype,
        "start_year": start,
        "end_year": end,
        "date_precision": precision,
        "period_id": period,
        "importance": importance,
        "summary_zh_cn": summary,
        "source_ref": source_ref,
        "source_ids": source_ids,
        "relations": relations or [],
        "review_note": review_note,
    }


# ---------------------------------------------------------------------------
# Phase A — 上古 / 夏 / 商 / 西周（events/pre_qin/）
# ---------------------------------------------------------------------------
PHASE_A = [
    # ---- 夏（traditional 框架：-2070 ~ -1600，approximate）----
    _ev("event-xia-jianguo", "夏朝建立（家天下）", "dynastic-transition",
        -2070, -2070, "approximate", "period-xia", "major",
        "传统纪年称禹传位于启，王位世袭的\"家天下\"秩序由此确立，中国历史上第一个王朝夏朝开始形成。"
        "年代依据《夏商周断代工程》框架与传统文献（《史记·夏本纪》《竹书纪年》），属于推算纪年，不视为精确断代。",
        f"古代史料：《史记·夏本纪》、古本《竹书纪年》；现代参考：{_M['xia_shang_zhou']}",
        W["shiji_zhushu"],
        [_rel("event-shangtang-miexia", "precedes", desc="自夏朝建立至商汤灭夏的时段主干")],
        review_note="夏代存在的性质与绝对纪年存在学术争议（二里头文化对应关系未完全定论），" 
                    "年代采用断代工程近似框架前2070年。"),
    _ev("event-xia-taikang-shiguo", "太康失国", "political",
        -2050, -2050, "approximate", "period-xia", "major",
        "传统纪年称夏王太康耽于游乐，被东夷首领后羿（有穷氏）夺权，夏朝一度失国，史称\"太康失国\"。"
        "属于《史记》《竹书纪年》记载的传统叙事，绝对年代无考，此年份为按传统积年推算的约数。",
        f"古代史料：《史记·夏本纪》《左传·襄公四年》；现代参考：{_M['xia_shang_zhou']}",
        W["shiji_zuozhuan"],
        [_rel("event-xia-jianguo", "follows"), _rel("event-xia-shaokang-zhongxing", "leads_to", 0.8,
                                                    desc="太康失国后经后羿、寒浞之乱，最终由少康复国中兴")],
        review_note="太康失国为传统叙事，年代为推算约数（约前2050年），无考古精确证据。"),
    _ev("event-xia-shaokang-zhongxing", "少康中兴", "political-military",
        -1990, -1990, "approximate", "period-xia", "major",
        "传统纪年称夏王少康在寒浞代夏后复国，恢复夏朝统治，史称\"少康中兴\"。"
        "事件反映夏代中期政权更迭与重建，绝对年代无考，此年份为约数。",
        f"古代史料：《左传·哀公元年》《史记·夏本纪》；现代参考：{_M['xia_shang_zhou']}",
        W["zuozhuan_shiji"],
        [_rel("event-xia-taikang-shiguo", "follows"), _rel("event-shangtang-miexia", "precedes")],
        review_note="少康中兴为传统叙事，年代为推算约数（约前1990年）。"),
    _ev("event-shangtang-miexia", "商汤灭夏", "dynastic-transition",
        -1600, -1600, "approximate", "period-xia", "critical",
        "夏朝末年商汤起兵伐夏，在鸣条（今河南一带，具体地望有争议）击败夏桀，夏朝灭亡，史称\"商汤革命\"。"
        "这是中国历史上有明确文献记载的第一次王朝更替，标志夏商年代分界。"
        "年代采用《夏商周断代工程》约前1600年框架，另有学者主张前1556年前后，存在分歧。",
        f"古代史料：《史记·殷本纪》《尚书·汤誓》；现代参考：{_M['xia_shang_zhou']}",
        W["shiji_shangshu"],
        [_rel("event-shang-jianguo", "leads_to", 0.9, desc="灭夏后商政权建立")],
        review_note="商汤灭夏为中国历史上第一次文献明确记载的王朝更替；断代工程取约前1600年，"
                    "亦有前1556年等说（详见 EARLY_HISTORY_UNCERTAINTY.md）。"),
    # ---- 商（traditional 框架：-1600 ~ -1046，approximate）----
    _ev("event-shang-jianguo", "商朝建立", "dynastic-transition",
        -1600, -1600, "approximate", "period-shang", "major",
        "商汤灭夏后建立商朝，都亳（地望有争议，一说今河南郑州一带）。商朝成为中国历史上第二个王朝。"
        "年代与夏商分界同为断代工程框架值。",
        f"古代史料：《史记·殷本纪》；现代参考：{_M['xia_shang_zhou']}",
        W["shiji"],
        [_rel("event-shangtang-miexia", "follows"), _rel("event-pangeng-qianyin", "precedes")],
        review_note="商代早期都城亳的地望存在学术争议（郑州商城与偃师商城诸说）。"),
    _ev("event-pangeng-qianyin", "盘庚迁殷", "migration",
        -1300, -1300, "approximate", "period-shang", "major",
        "商王盘庚将都城迁至殷（今河南安阳殷墟），此后商朝都城长期稳定在殷，故商后期又称\"殷商\"。"
        "断代工程据《竹书纪年》\"盘庚迁殷至纣之灭273年\"推定为约前1300年。",
        f"古代史料：《史记·殷本纪》《尚书·盘庚》；现代参考：{_M['xia_shang_zhou']}",
        W["shiji_shangshu"],
        [_rel("event-shang-jianguo", "follows"), _rel("event-wuding-zhongxing", "leads_to", 0.7,
                                                      desc="迁殷后商政权稳定，为武丁中兴提供基础")],
        review_note="盘庚迁殷约前1300年为断代工程推定，学界有约前1290等相近说法。"),
    _ev("event-wuding-zhongxing", "武丁中兴", "political-military",
        -1250, -1192, "approximate", "period-shang", "major",
        "商王武丁在位约59年，任用傅说等贤臣，征伐四方，商朝国力达到鼎盛，史称\"武丁中兴\"。"
        "甲骨文卜辞与殷墟考古为这一时期提供了直接证据。在位年断代工程从甲骨月食记录推定为前1250—前1192年。",
        f"古代史料：殷墟甲骨卜辞、《史记·殷本纪》；现代参考：{_M['xia_shang_zhou']}",
        W["shiji"],
        [_rel("event-pangeng-qianyin", "follows"), _rel("event-wuwang-fazhou", "precedes")],
        review_note="武丁纪元（前1250—前1192）为断代工程据甲骨月食记录推定，学界认同度较高但仍有讨论。"),
    _ev("event-wuwang-fazhou", "武王伐纣", "war",
        -1046, -1046, "approximate", "period-shang", "critical",
        "周武王姬发率诸侯联军伐商，与商军战于牧野（今河南淇县南），商纣王自焚，商朝灭亡，史称\"武王伐纣\"或\"牧野之战\"。"
        "这是商周分界的标志性节点。断代工程经多方推定为前1046年，另有前1027年（《竹书纪年》系统）等四十余种异说。",
        f"古代史料：《史记·周本纪》《尚书·牧誓》、青铜利簋铭文；现代参考：{_M['xia_shang_zhou']}",
        W["shiji_shangshu"],
        [_rel("event-xizhou-jianguo", "leads_to", 0.9, desc="克商后周人建立西周政权")],
        review_note="武王伐纣年代有44—45种异说（前1130—前1018），断代工程取前1046年；"
                    "《竹书纪年》系统主张前1027年。详见 EARLY_HISTORY_UNCERTAINTY.md。"),
    # ---- 西周（-1046 ~ -771）----
    _ev("event-xizhou-jianguo", "西周建立", "dynastic-transition",
        -1046, -1046, "approximate", "period-western-zhou", "major",
        "武王克商灭商建周，定都镐京（今陕西西安一带），史称西周。周人以宗法分封构建统治体系，"
        "西周成为中国早期国家制度建设的关键阶段。起始年与武王伐纣同为前1046年。",
        f"古代史料：《史记·周本纪》；现代参考：{_M['xia_shang_zhou']}",
        W["shiji"],
        [_rel("event-wuwang-fazhou", "follows"), _rel("event-sanjian-zhiluan", "precedes")],
        review_note="西周建立年代沿用断代工程克商之年（前1046年）。"),
    _ev("event-sanjian-zhiluan", "三监之乱", "rebellion",
        -1042, -1042, "approximate", "period-western-zhou", "major",
        "武王死后成王年幼，周公旦摄政，管叔、蔡叔联合商纣之子武庚发动叛乱，史称\"三监之乱\"。"
        "叛乱是西周初年政权继承危机的集中爆发，最终由周公东征平定。",
        f"古代史料：《史记·周本纪》《尚书·大诰》；现代参考：{_M['xia_shang_zhou']}",
        W["shiji_shangshu"],
        [_rel("event-xizhou-jianguo", "follows"), _rel("event-zhougong-dongzheng", "leads_to", 0.9,
                                                      desc="叛乱引发周公东征平叛")],
        review_note="三监之乱年代约成王初年（约前1042年前后），为断代工程年代框架内的推定。"),
    _ev("event-zhougong-dongzheng", "周公东征", "war",
        -1042, -1040, "approximate", "period-western-zhou", "major",
        "周公旦率军东征，讨平武庚与三监之乱，并继续东拓，灭徐、奄等东夷方国，巩固了周人对东方的统治。"
        "东征是西周稳定政权、推行分封的重要军事前提。",
        f"古代史料：《尚书·大诰》《史记·鲁周公世家》；现代参考：{_M['xia_shang_zhou']}",
        W["shiji_shangshu"],
        [_rel("event-sanjian-zhiluan", "follows"), _rel("event-zhougong-shezheng", "part_of", 0.8,
                                                        desc="东征为周公摄政时期的军事行动")],
        review_note="周公东征年代与三监之乱相邻（约前1042—前1040），为推定值。"),
    _ev("event-zhougong-shezheng", "周公摄政", "political",
        -1042, -1035, "approximate", "period-western-zhou", "major",
        "成王年幼，周公旦摄政称王，稳定初建政权，史称\"周公摄政\"（一说另立由周召二公共和辅政）。"
        "摄政期间平定叛乱、营建洛邑、推行制礼作乐，被誉为西周制度文化奠基的关键期。",
        f"古代史料：《史记·周本纪》；现代参考：{_M['xia_shang_zhou']}",
        W["shiji"],
        [_rel("event-chengkang-zhizhi", "leads_to", 0.8,
              desc="周公摄政与制礼作乐为成康之治奠基")],
        review_note="周公摄政一说是否\"践祚称王\"存在学界分歧；年代约前1042—前1035（摄政七年）。"),
    _ev("event-zhougong-jianluoyi", "周公营建洛邑", "foundation",
        -1035, -1035, "approximate", "period-western-zhou", "major",
        "周公在成王支持下营建东都洛邑（成周，今河南洛阳），作为控制东方的政治中心与\"天下之中\"。"
        "洛邑的营建是西周两都制国家格局形成的标志。",
        f"古代史料：《尚书·洛诰》《逸周书·作雒》；现代参考：{_M['xia_shang_zhou']}",
        W["shiji_shangshu"],
        [_rel("event-zhougong-shezheng", "follows"), _rel("event-chengkang-zhizhi", "precedes")],
        review_note="洛邑营建年代约在周公摄政后期（约前1035年），为传统纪年推算。"),
    _ev("event-chengkang-zhizhi", "成康之治", "political",
        -1035, -996, "approximate", "period-western-zhou", "major",
        "成王、康王时期，周公所定制度渐趋稳定，史称\"成康之治\"，为西周盛世。"
        "《史记》载\"成康之际，天下安宁，刑错四十余年不用\"。年代为断代工程框架值。",
        f"古代史料：《史记·周本纪》；现代参考：{_M['xia_shang_zhou']}",
        W["shiji"],
        [_rel("event-zhougong-shezheng", "follows"), _rel("event-zhaowang-nanzheng", "precedes")],
        review_note="\"成康之治\"为后世对成王康王时期治世的概括，属阶段性治世节点，年份为框架值。"),
    _ev("event-zhaowang-nanzheng", "昭王南征", "war",
        -977, -977, "approximate", "period-western-zhou", "major",
        "周昭王南征荆楚，卒于汉水之滨，\"南征而不复\"，周人对南方扩展受挫。"
        "据《竹书纪年》昭王十九年南征记载推定为约前977年，具体年代无确考。",
        f"古代史料：古本《竹书纪年》《史记·周本纪》；现代参考：{_M['xia_shang_zhou']}",
        W["shiji_zhushu"],
        [_rel("event-chengkang-zhizhi", "follows"), _rel("event-muwang-xizheng", "precedes")],
        review_note="昭王南征年代约前977年（昭王十九年），为传统纪年推算，存在不确定性。"),
    _ev("event-muwang-xizheng", "穆王西征", "war",
        -960, -960, "approximate", "period-western-zhou", "major",
        "周穆王西征犬戎、巡游西方，史载\"穆王西征犬戎，得四白狼四白鹿以归\"。"
        "反映西周中期对西北方向的经营与王权巡狩传统。年代约前10世纪中叶，无精确纪年。",
        f"古代史料：古本《竹书纪年》《史记·周本纪》；现代参考：{_M['xia_shang_zhou']}",
        W["shiji_zhushu"],
        [_rel("event-zhaowang-nanzheng", "follows"), _rel("event-guoren-baodong", "precedes")],
        review_note="穆王西征约前960年前后，为传统纪年推算；穆王在位年代断代工程定为前976—前922。"),
    _ev("event-guoren-baodong", "国人暴动", "rebellion",
        -842, -841, "approximate", "period-western-zhou", "major",
        "周厉王专利敛财、弭谤高压，激起镐京\"国人\"武装暴动，厉王出奔于彘（今山西霍州）。"
        "这次暴动终结了厉王统治，是西周第一次大规模民众反抗。一说在前841年（一说前842年）。",
        f"古代史料：《史记·周本纪》《国语·周语》；现代参考：{_M['xia_shang_zhou']}",
        W["shiji_shangshu"],
        [_rel("event-muwang-xizheng", "follows"), _rel("event-gonghe-xingzheng", "leads_to", 0.9,
                                                       desc="厉王出奔后进入共和行政时期")],
        review_note="国人暴动年代通常记前841年（一说前842年）；共和元年（前841年）为中国历史确切纪年的开端。"),
    _ev("event-gonghe-xingzheng", "共和行政", "political",
        -841, -828, "range", "period-western-zhou", "major",
        "厉王流亡后，由周定公、召穆公二相共同执政（一说共伯和摄行天子事），史称\"共和行政\"。"
        "共和元年（前841年）是中国历史上有确切纪年的开始。共和凡十四年，至前828年止。",
        f"古代史料：《史记·周本纪》（周召共和）与古本《竹书纪年》（共伯和）；现代参考：{_M['xia_shang_zhou']}",
        W["shiji_zhushu"],
        [_rel("event-guoren-baodong", "follows"), _rel("event-xuanwang-zhongxing", "leads_to", 0.8,
                                                       desc="共和结束，宣王即位，开启宣王中兴")],
        review_note="共和行政存在\"周召共和\"与\"共伯和\"两种解释，均为史源记载，学界多从《竹书纪年》共伯和说；"
                    "前841年为中国确切纪年起点。"),
    _ev("event-xuanwang-zhongxing", "宣王中兴", "political-military",
        -827, -782, "range", "period-western-zhou", "major",
        "周宣王在位期间（前827—前782年），征伐猃狁、淮夷，诸侯复朝，西周一度复兴，史称\"宣王中兴\"。"
        "这是西周王权在衰败前的最后一次振作。",
        f"古代史料：《诗经》相关篇章、《史记·周本纪》；现代参考：{_M['xia_shang_zhou']}",
        W["shiji_shangshu"],
        [_rel("event-gonghe-xingzheng", "follows"), _rel("event-youwang-zhi-luan", "leads_to", 0.7,
                                                         desc="宣王晚年政衰，其后的幽王时期西周走向灭亡")],
        review_note="宣王元年（前827年）与共和纪年相接，属可信纪年（《史记》年表体系）。"),
    _ev("event-youwang-zhi-luan", "幽王之乱", "political",
        -781, -771, "approximate", "period-western-zhou", "major",
        "周幽王废申后与太子宜臼，立褒姒及其子伯服，王朝内乱加速；\"烽火戏诸侯\"的传说亦见于后世记载（传说成分需辨析）。"
        "此乱导致申侯联合犬戎攻周，西周灭亡于前771年。",
        f"古代史料：《史记·周本纪》（含\"烽火\"传说记载）；现代参考：{_M['xia_shang_zhou']}",
        W["shiji"],
        [_rel("event-xuanwang-zhongxing", "follows"), _rel("event-quanrong-mie-xizhou", "leads_to", 0.9,
                                                           desc="幽王之乱直接导致犬戎攻破镐京")],
        review_note="\"烽火戏诸侯\"多见于《史记》以来记载，现代研究对其真实性有讨论；宜臼被废、申侯引犬戎为史源共识。"),
    _ev("event-quanrong-mie-xizhou", "犬戎灭西周", "war",
        -771, -771, "year", "period-western-zhou", "major",
        "前771年，申侯联合缯国、犬戎攻破镐京，周幽王被杀于骊山之下，宗周被毁，西周灭亡。"
        "这是中国早期王朝第一次\"亡国\"事件，标志两周之际政治格局的剧变。",
        f"古代史料：《史记·周本纪》；现代参考：{_M['xia_shang_zhou']}",
        W["shiji"],
        [_rel("event-youwang-zhi-luan", "follows")],
        review_note="前771年犬戎攻破镐京为通行纪年，属相对可靠的传统记载。"),
]

# ---------------------------------------------------------------------------
# Phase B — 春秋（-770 ~ -476；events/chunqiu_zhanguo/）
# ---------------------------------------------------------------------------
PHASE_B = [
    _ev("event-pingwang-dongqian", "平王东迁", "migration",
        -770, -770, "year", "period-spring-autumn", "critical",
        "前770年，周平王在申侯等拥立下东迁都于洛邑（成周），史称\"平王东迁\"，东周自此开始，春秋时代开启。"
        "迁都后王室权威跌落，诸侯坐大，中国历史进入列国争霸格局。"
        "《左传》所记\"王入于成周\"经天文历法考证兑为前770年1月11日。",
        f"古代史料：《史记·周本纪》《左传》；现代参考：{_M['chunqiu']}",
        W["shiji_zuozhuan"],
        [_rel("event-quanrong-mie-xizhou", "follows"), _rel("event-zheng-zhuanggong-xiaoba", "leads_to", 0.7,
                                                            desc="王室权威进一步衰落，郑等国率先坐大")],
        review_note="平王东迁年代前770为通行纪年（据《左传》干支日食可校准）；个别学者主张前771年。"),
    _ev("event-zheng-zhuanggong-xiaoba", "郑庄公小霸", "political-military",
        -743, -701, "range", "period-spring-autumn", "major",
        "郑庄公在位（前743—前701年）期间，内平共叔段之乱，外联齐鲁，多次与周王室冲突并一度击败王师，"
        "郑国成为春秋初年最强诸侯，史称\"郑庄公小霸\"。此阶段标志王室与诸侯力量对比的逆转。",
        f"古代史料：《左传·隐公元年至桓公十一年》；现代参考：{_M['chunqiu']}",
        W["zuozhuan"],
        [_rel("event-pingwang-dongqian", "follows")],
        review_note="\"郑庄公小霸\"为后世史家对郑庄公在位时期（前743—前701）的概括，以繻葛之战为顶点。"),
    _ev("event-xuge-zhizhan", "繻葛之战", "war",
        -707, -707, "year", "period-spring-autumn", "major",
        "前707年，周桓王亲率诸侯伐郑，郑庄公在繻葛（今河南长葛一带）击败王师，箭中王肩，史载\"王卒大败\"。"
        "此役是周王室权威崩溃的标志性事件，此后王师再无力征讨诸侯。",
        f"古代史料：《左传·桓公五年》；现代参考：{_M['chunqiu']}",
        W["zuozhuan"],
        [_rel("event-zheng-zhuanggong-xiaoba", "part_of", 0.9, desc="繻葛之战为郑庄公对抗王权的高潮"),
         _rel("event-guanzhong-gaige", "precedes")],
        review_note="繻葛之战前707年（鲁桓公五年）为《春秋》系年，年代无争议。"),
    _ev("event-guanzhong-gaige", "管仲改革", "reform",
        -685, -645, "range", "period-spring-autumn", "major",
        "齐桓公即位后任用管仲为相，推行\"通货积财\"、四民分业、三选等内政改革与\"尊王攘夷\"方针，"
        "齐国迅速富强，为齐桓公称霸奠定基础。管仲辅政约前685—前645年。",
        f"古代史料：《史记·齐太公世家》《管子》（托名）；现代参考：{_M['chunqiu']}",
        W["shiji"],
        [_rel("event-xuge-zhizhan", "follows"), _rel("event-qihuan-gong-ba", "leads_to", 0.85,
                                                     desc="管仲改革成就齐桓公霸业")],
        review_note="管仲改革的起始年代无确年年表，以其相齐（约前685年）为起点。"),
    _ev("event-qihuan-gong-ba", "齐桓公称霸", "political-military",
        -679, -643, "range", "period-spring-autumn", "major",
        "齐桓公以\"尊王攘夷\"为旗号会盟诸侯，北御戎狄、南阻楚国，成为春秋第一位霸主，"
        "葵丘之会（前651年）达到霸业顶点。齐桓公霸权奠定了春秋\"霸主政治\"的基本格局。",
        f"古代史料：《左传》《史记·齐太公世家》；现代参考：{_M['chunqiu']}",
        W["shiji_zuozhuan"],
        [_rel("event-guanzhong-gaige", "follows"),
         _rel("event-hong-zhizhan", "precedes")],
        review_note="齐桓公称霸取前679年始合诸侯至前643年桓公卒，属归纳性时段节点。"),
    _ev("event-zhaoling-zhi-meng", "召陵之盟", "treaty",
        -656, -656, "year", "period-spring-autumn", "major",
        "前656年，齐桓公率齐、宋、陈、卫、郑、许、曹联军伐楚，与楚在召陵（今河南郾城一带）结盟，"
        "楚北上势头被阻。此役是齐桓公\"尊王攘夷\"霸业中与强楚正面对抗的重要事件。",
        f"古代史料：《左传·僖公四年》；现代参考：{_M['chunqiu']}",
        W["zuozhuan"],
        [_rel("event-qihuan-gong-ba", "part_of", 0.9, desc="召陵之盟为齐桓公霸权下对楚外交的成果"),
         _rel("event-kuiqiu-zhi-hui", "precedes")],
        review_note="召陵之盟前656年（鲁僖公四年）为《春秋》系年，无争议。"),
    _ev("event-kuiqiu-zhi-hui", "葵丘之会", "treaty",
        -651, -651, "year", "period-spring-autumn", "major",
        "前651年，齐桓公在葵丘（今河南民权一带）会盟鲁、宋、卫、郑、许、曹诸国，周襄王亦遣使赐胙，"
        "齐桓公霸业达到顶峰，史称\"葵丘之会\"。此后齐桓公的影响力逐渐衰退。",
        f"古代史料：《左传·僖公九年》《孟子·告子》；现代参考：{_M['chunqiu']}",
        W["zuozhuan"],
        [_rel("event-zhaoling-zhi-meng", "follows"), _rel("event-hong-zhizhan", "precedes"),
         _rel("event-qihuan-gong-ba", "part_of", 0.9, desc="葵丘之会为齐桓公霸业顶点")],
        review_note="葵丘之会前651年为《春秋》系年，无争议。"),
    _ev("event-hong-zhizhan", "泓之战", "war",
        -638, -638, "year", "period-spring-autumn", "major",
        "前638年，宋襄公与楚军在泓水（今河南柘城一带）交战，宋襄公恪守\"不鼓不成列\"的旧礼而战败受伤，"
        "宋国称霸企图破产。此役常被用作\"礼崩乐坏\"时代军事观念转变的标志。",
        f"古代史料：《左传·僖公二十二年》；现代参考：{_M['chunqiu']}",
        W["zuozhuan"],
        [_rel("event-kuiqiu-zhi-hui", "follows"), _rel("event-chengpu-zhizhan", "precedes")],
        review_note="泓之战前638年为《春秋》系年，无争议。"),
    _ev("event-jinwen-gong-ba", "晋文公称霸", "political-military",
        -636, -628, "range", "period-spring-autumn", "major",
        "晋文公重耳流亡十九年后回国即位（前636年），改革内政、整顿军制，"
        "经城濮之战（前632年）败楚、践土之盟受天子策命，成为齐桓公之后第二位公认的霸主。",
        f"古代史料：《左传·僖公二十三至二十八年》；现代参考：{_M['chunqiu']}",
        W["zuozhuan"],
        [],
        review_note="晋文公称霸以在位期间（前636—前628）概括，城濮之战与践土之盟（前632）为标志节点。"),
    _ev("event-chengpu-zhizhan", "城濮之战", "war",
        -632, -632, "year", "period-spring-autumn", "major",
        "前632年，晋文公率晋、宋、齐、秦联军在城濮（今山东鄄城一带）大败楚军，"
        "楚成王北进受阻。此役奠定晋国霸权，是春秋时代规模最大、影响最深的会战之一，"
        "战后晋文公在践土会盟诸侯、受周天子册命。",
        f"古代史料：《左传·僖公二十八年》；现代参考：{_M['chunqiu']}",
        W["zuozhuan"],
        [_rel("event-jinwen-gong-ba", "leads_to", 0.9, desc="城濮之战胜后晋文公践土盟诸侯、确立霸权"),
         _rel("event-xiao-zhizhan", "precedes")],
        review_note="城濮之战前632年（鲁僖公二十八年）为《春秋》系年，无争议。"),
    _ev("event-chuwuwang-chengwang", "楚武王称王", "political",
        -704, -704, "year", "period-spring-autumn", "major",
        "前704年，楚君熊通自立为王，成为春秋时期第一个僭号称王的诸侯，打破周天子独尊的名分秩序。"
        "楚国由此以\"王\"号独立于诸侯体系，是南方大国崛起的标志性节点。",
        f"古代史料：《左传·桓公八年》《史记·楚世家》；现代参考：{_M['chunqiu']}",
        W["zuozhuan_shiji"],
        [_rel("event-wending-zhongyuan", "precedes"), _rel("event-chuzhuang-wang-ba", "precedes")],
        review_note="楚武王称王前704年为《春秋》系年；\"熊通自立为王\"的记载见于《史记·楚世家》。"),
    _ev("event-qinmu-gong-ba-xirong", "秦穆公称霸西戎", "political-military",
        -659, -621, "range", "period-spring-autumn", "major",
        "秦穆公在位（前659—前621年）期间，任用百里奚、蹇叔等贤臣，向东争霸受阻于晋（崤之战后），"
        "遂转向经营西方，\"益国十二，开地千里，遂霸西戎\"，奠定秦国的西部根基。",
        f"古代史料：《史记·秦本纪》；现代参考：{_M['chunqiu']}",
        W["shiji"],
        [_rel("event-xiao-zhizhan", "follows"), _rel("event-yue-mie-wu", "precedes")],
        review_note="秦穆公\"霸西戎\"以穆公在位期（前659—前621）概括，崤之战（前627）为其东进受挫的关键。"),
    _ev("event-xiao-zhizhan", "崤之战", "war",
        -627, -627, "year", "period-spring-autumn", "major",
        "前627年，秦军东袭郑国未果而返，晋襄公在崤山（今河南三门峡一带）伏击全歼秦军，"
        "秦穆公东进战略受挫，秦晋冲突加剧。此役强化了\"秦晋阻隔\"的格局。",
        f"古代史料：《左传·僖公三十三至三十二年》所记崤之战；现代参考：{_M['chunqiu']}",
        W["zuozhuan"],
        [_rel("event-chengpu-zhizhan", "follows"), _rel("event-qinmu-gong-ba-xirong", "leads_to", 0.8,
                                                        desc="东进受阻后秦穆公转向霸西戎")],
        review_note="崤之战前627年（鲁僖公三十三年）为《春秋》系年，无争议。"),
    _ev("event-bi-zhizhan", "邲之战", "war",
        -597, -597, "year", "period-spring-autumn", "major",
        "前597年，晋楚在邲（今河南荥阳东北）交战，楚庄王大败晋军，史称\"邲之战\"。"
        "此役是晋楚争霸的转折点：楚国确立南方霸权，晋国霸权暂衰。",
        f"古代史料：《左传·宣公十二年》；现代参考：{_M['chunqiu']}",
        W["zuozhuan"],
        [_rel("event-jinwen-gong-ba", "follows"), _rel("event-yanling-zhizhan", "precedes"),
         _rel("event-chuzhuang-wang-ba", "part_of", 0.85, desc="邲之战胜晋为楚庄王霸业确立的关键")],
        review_note="邲之战前597年（鲁宣公十二年）为《春秋》系年，无争议。"),
    _ev("event-yanling-zhizhan", "鄢陵之战", "war",
        -575, -575, "year", "period-spring-autumn", "major",
        "前575年，晋厉公率军在鄢陵（今河南鄢陵一带）击败楚共王与郑国联军，"
        "晋国重夺中原霸权，楚军北进再次受阻。此役为晋楚争霸中的第三次大战。",
        f"古代史料：《左传·成公十六年》；现代参考：{_M['chunqiu']}",
        W["zuozhuan"],
        [_rel("event-bi-zhizhan", "follows"), _rel("event-xiangxu-mibing", "precedes")],
        review_note="鄢陵之战前575年（鲁成公十六年）为《春秋》系年，无争议。"),
    _ev("event-jindaogong-fuba", "晋悼公复霸", "political-military",
        -573, -558, "range", "period-spring-autumn", "major",
        "晋悼公即位（前573年）后，整顿内政、和戎政策并举，恢复晋国霸权，史称\"晋悼公复霸\"。"
        "晋国霸权延续至其逝世（前558年）后逐渐让于弭兵格局。",
        f"古代史料：《左传·成公十八年至襄公十五年》；现代参考：{_M['chunqiu']}",
        W["zuozhuan"],
        [_rel("event-yanling-zhizhan", "follows"), _rel("event-xiangxu-mibing", "precedes")],
        review_note="晋悼公复霸以其在位期（前573—前558）概括，属阶段性节点。"),
    _ev("event-xiangxu-mibing", "向戌弭兵", "treaty",
        -546, -546, "year", "period-spring-autumn", "major",
        "前546年，宋大夫向戌促成晋、楚、齐、秦等十四国在宋都结盟弭兵，"
        "晋楚平分霸权，中原战场暂时休战。弭兵之会开启春秋后期相对和平的格局，各国内政问题上升。",
        f"古代史料：《左传·襄公二十七年》；现代参考：{_M['chunqiu']}",
        W["zuozhuan"],
        [_rel("event-jindaogong-fuba", "follows"), _rel("event-wu-guo-jueqi", "precedes")],
        review_note="向戌弭兵前546年（鲁襄公二十七年）为《春秋》系年，无争议。"),
    _ev("event-chuzhuang-wang-ba", "楚庄王称霸", "political-military",
        -613, -591, "range", "period-spring-autumn", "major",
        "楚庄王在位（前613—前591年）期间，\"一鸣惊人\"整顿内政，问鼎中原、败晋于邲，"
        "成为继齐桓、晋文后第三代霸主，楚国势力达到鼎盛。",
        f"古代史料：《史记·楚世家》《左传》；现代参考：{_M['chunqiu']}",
        W["shiji_zuozhuan"],
        [],
        review_note="楚庄王称霸以在位期（前613—前591）概括；\"一鸣惊人\"、问鼎中原为史载故事。"),
    _ev("event-wending-zhongyuan", "问鼎中原", "diplomatic",
        -606, -606, "year", "period-spring-autumn", "major",
        "前606年，楚庄王北伐陆浑之戎、陈兵周疆，向周大夫王孙满问九鼎之轻重，彰显取代周天子的野心，"
        "史称\"问鼎中原\"。此事件为楚庄王霸权与周王室权威衰落的标志。",
        f"古代史料：《左传·宣公三年》；现代参考：{_M['chunqiu']}",
        W["zuozhuan"],
        [_rel("event-chuzhuang-wang-ba", "part_of", 0.9, desc="问鼎中原为楚庄王时期标志性外交事件"),
         _rel("event-zichan-xingshu", "precedes")],
        review_note="问鼎中原前606年（鲁宣公三年）为《春秋》系年，无争议。"),
    _ev("event-zichan-xingshu", "子产铸刑书", "reform",
        -536, -536, "year", "period-spring-autumn", "major",
        "前536年，郑国执政子产将刑书铸于鼎上公之于众，史称\"子产铸刑书\"，是中国历史上第一次公布成文法。"
        "此举打破贵族秘刑传统，是春秋后期礼制变革与法治萌发的重要标志。",
        f"古代史料：《左传·昭公六年》；现代参考：{_M['chunqiu']}",
        W["zuozhuan"],
        [_rel("event-wending-zhongyuan", "follows"), _rel("event-wu-guo-jueqi", "precedes")],
        review_note="子产铸刑书前536年（鲁昭公六年）为《春秋》系年，无争议。"),
    _ev("event-wu-guo-jueqi", "吴国崛起", "political-military",
        -514, -506, "range", "period-spring-autumn", "major",
        "吴王阖闾即位（前514年）后，任用孙武、伍子胥整顿军政，吴国崛起为南方强国，"
        "经柏举之战（前506年）攻破楚都郢，一度成为争霸主角。",
        f"古代史料：《史记·吴太伯世家》《孙子兵法·序》；现代参考：{_M['chunqiu']}",
        W["shiji_zuozhuan"],
        [_rel("event-xiangxu-mibing", "follows"),
         _rel("event-fujiao-zhizhan", "precedes")],
        review_note="吴国崛起以阖闾图强至柏举破郢（前514—前506）概括，属阶段性节点。"),
    _ev("event-boju-zhizhan", "柏举之战", "war",
        -506, -506, "year", "period-spring-autumn", "major",
        "前506年，吴王阖闾率孙武、伍子胥等攻楚，在柏举（今湖北麻城一带）大败楚军，"
        "五战入郢（楚国都）。楚几乎灭亡，后赖秦救得复国。此役为春秋末期最大规模战争之一。",
        f"古代史料：《左传·定公四年》；现代参考：{_M['chunqiu']}",
        W["zuozhuan"],
        [_rel("event-wu-guo-jueqi", "part_of", 0.9, desc="柏举之战为吴国崛起的标志性战役"),
         _rel("event-fujiao-zhizhan", "precedes")],
        review_note="柏举之战前506年（鲁定公四年）为《春秋》系年，无争议。"),
    _ev("event-fujiao-zhizhan", "夫椒之战", "war",
        -494, -494, "year", "period-spring-autumn", "major",
        "前494年，吴王夫差在夫椒（今江苏太湖一带）大败越军，越王勾践遣使求和，屈身为奴，"
        "越国暂时臣服于吴。此役为吴越争霸的转折点。",
        f"古代史料：《史记·越王勾践世家》《左传·哀公元年》；现代参考：{_M['chunqiu']}",
        W["shiji_zuozhuan"],
        [_rel("event-boju-zhizhan", "follows"), _rel("event-huangchi-zhi-hui", "leads_to", 0.85,
                                                     desc="越国臣服后吴北上争霸，最终在黄池之会期间遭越偷袭")],
        review_note="夫椒之战前494年为通行纪年（吴王夫差二年），无争议。"),
    _ev("event-huangchi-zhi-hui", "黄池之会", "diplomatic",
        -482, -482, "year", "period-spring-autumn", "major",
        "前482年，吴王夫差率精锐北上黄池（今河南封丘一带）与晋争盟主，越王勾践趁机袭吴，"
        "吴国腹背受敌。黄池之会虽使夫差夺得盟主名号，却是吴国王权由盛转衰的转折点。",
        f"古代史料：《左传·哀公十三年》《史记·吴太伯世家》；现代参考：{_M['chunqiu']}",
        W["zuozhuan_shiji"],
        [_rel("event-fujiao-zhizhan", "follows"), _rel("event-yue-mie-wu", "leads_to", 0.85,
                                                       desc="黄池之会期间越国袭吴，吴国自此衰亡")],
        review_note="黄池之会前482年（鲁哀公十三年）为《春秋》系年，无争议。"),
    _ev("event-yue-mie-wu", "越灭吴", "war",
        -473, -473, "year", "period-warring-states", "major",
        "前473年，越王勾践经\"十年生聚、十年教训\"后灭吴，吴王夫差自杀，吴国灭亡。"
        "越军随后北略齐、晋，会盟诸侯，勾践成为春秋最后一位霸主。"
        "本事件为吴越争霸的收尾节点，按项目 taxonomy（战国起始前475年）归属战国初段，"
        "传统《春秋》叙事多将其并入春秋末期主题。",
        f"古代史料：《史记·越王勾践世家》《国语·吴语》（吴越争霸记载）；现代参考：{_M['chunqiu']}、{_M['zhanguo']}",
        W["shiji"],
        [_rel("event-huangchi-zhi-hui", "follows"), _rel("event-jin-mie-zhi", "precedes")],
        review_note="越灭吴前473年为通行纪年；因晚于 taxonomy 战国起始（前475），period_id 记为 period-warring-states，"
                    "分期口径差异见 EARLY_HISTORY_UNCERTAINTY.md。"),
    _ev("event-jin-mie-zhi", "三家灭智", "war",
        -453, -453, "year", "period-warring-states", "major",
        "前453年，晋国韩、赵、魏三家联合灭掉执政的智氏，三分其地，晋公室名存实亡。"
        "三家灭智是\"三家分晋\"的前奏，为战国七雄格局的形成埋下伏笔。",
        f"古代史料：《史记·晋世家》《资治通鉴·周纪一》追述；现代参考：{_M['chunqiu']}、{_M['zhanguo']}",
        W["shiji"],
        [_rel("event-yue-mie-wu", "follows")],
        review_note="三家灭智前453年为通行纪年；按分期口径，本事件已在战国初段（项目 taxonomy 战国起前475年），"
                    "归属 period-warring-states。"),
]

# ---------------------------------------------------------------------------
# Phase C — 战国（-475 ~ -221；events/chunqiu_zhanguo/）
# ---------------------------------------------------------------------------
PHASE_C = [
    _ev("event-sanjia-fenjin", "三家分晋", "dynastic-transition",
        -403, -403, "year", "period-warring-states", "critical",
        "前403年，周威烈王正式册命韩、赵、魏三家为诸侯，晋国分裂为三国，史称\"三家分晋\"。"
        "《资治通鉴》以此为战国时代的开端。此事件标志世卿执政卿大夫夺权的制度性完成，"
        "列国兼并战争的新格局自此全面展开。",
        f"古代史料：《史记·晋世家》《资治通鉴·周纪一》；现代参考：{_M['zhanguo']}",
        W["shiji"],
        [_rel("event-jin-mie-zhi", "follows"), _rel("event-tianshi-dai-qi", "precedes"),
         _rel("event-likui-bianfa", "leads_to", 0.7, desc="三家分晋标志世卿执政的完成，列国变法图强浪潮随之展开，魏国李悝变法为其中最早者")],
        review_note="三家分晋前403年（周威烈王二十三年）为通行纪年；战国起始另有前481/前476/前473/前453等说，"
                    "项目 taxonomy 采用史识通行的前475年。详见 EARLY_HISTORY_UNCERTAINTY.md。"),
    _ev("event-tianshi-dai-qi", "田氏代齐", "dynastic-transition",
        -386, -386, "year", "period-warring-states", "major",
        "前386年，齐相田和经周安王册命列为诸侯，姜氏齐国为田氏齐国取代，史称\"田氏代齐\"。"
        "与三家分晋并列为战国初年\"大夫夺权\"的两大标志性事件。",
        f"古代史料：《史记·齐太公世家》；现代参考：{_M['zhanguo']}",
        W["shiji"],
        [_rel("event-sanjia-fenjin", "follows"), _rel("event-jixia-xuegong", "leads_to", 0.7,
                                                      desc="田氏代齐后田齐君主兴办稷下学宫以固统治")],
        review_note="田氏代齐前386年（田和列为诸侯）为通行纪年；田氏完全吞并齐地、齐康公卒在前379年。"),
    _ev("event-likui-bianfa", "李悝变法", "reform",
        -406, -396, "approximate", "period-warring-states", "major",
        "魏文侯任用李悝，推行\"尽地力之教\"与\"平籴法\"，并编撰《法经》，魏国率先富强，"
        "是为战国变法之始。具体年代无确考，约在魏文侯在位后期（约前406—前396年间）。",
        f"古代史料：《汉书·艺文志》著录《法经》（亡佚）、《史记》司马穰苴等篇涉及；现代参考：{_M['zhanguo']}",
        W["shiji"],
        [_rel("event-wuqi-bianfa", "precedes"),
         _rel("event-guiling-zhizhan", "precedes")],
        review_note="李悝变法无确年年表，约在魏文侯在位后期（约前400年前后），取约前406—前396为约略范围。"),
    _ev("event-wuqi-bianfa", "吴起变法", "reform",
        -386, -381, "range", "period-warring-states", "major",
        "楚悼王任用吴起变法，明法审令、裁撤冗官、强兵拓土，楚国一度强盛；"
        "前381年悼王卒，吴起被旧贵族射杀，变法失败。吴起变法为楚国后期国势的关键变量。",
        f"古代史料：《史记·孙子吴起列传》；现代参考：{_M['zhanguo']}",
        W["shiji"],
        [_rel("event-likui-bianfa", "follows"), _rel("event-guiling-zhizhan", "precedes")],
        review_note="吴起变法约前386—前381年（楚悼王在位后期），变法因悼王去世而终止。"),
    _ev("event-guiling-zhizhan", "桂陵之战", "war",
        -354, -353, "range", "period-warring-states", "major",
        "前354年魏军围困赵都邯郸，前353年齐将田忌、军师孙膑以\"围魏救赵\"之策截击魏军于桂陵"
        "（今河南长垣一带），大败魏军。此役为\"围魏救赵\"战法经典，齐国开始挑战魏国霸权。",
        f"古代史料：《史记·孙子吴起列传》《孙膑兵法》（出土文献）；现代参考：{_M['zhanguo']}",
        W["shiji"],
        [_rel("event-likui-bianfa", "follows"), _rel("event-maling-zhizhan", "leads_to", 0.8,
                                                     desc="桂陵之战后魏国国力受损，齐魏再战于马陵")],
        review_note="桂陵之战年代：前354年魏围邯郸、前353年齐军于桂陵截击获胜；个别著作径记前354年一战。"),
    _ev("event-maling-zhizhan", "马陵之战", "war",
        -341, -341, "approximate", "period-warring-states", "major",
        "齐魏再战于马陵（今山东郯城一带），孙膑以\"减灶示弱\"之计诱敌，魏将庞涓败死，魏军主力覆没。"
        "此役后魏国霸权彻底丧失，齐国崛起为东方强国。年代有前341年（《史记》系年）与前342年（《竹书纪年》系年）两说。",
        f"古代史料：《史记·孙子吴起列传》、古本《竹书纪年》；现代参考：{_M['zhanguo']}",
        W["shiji_zhushu"],
        [_rel("event-guiling-zhizhan", "follows"),
         _rel("event-shangyang-bianfa", "follows", desc="马陵之战晚于商鞅变法完成之年（前350）")],
        review_note="马陵之战年代存在前341（史记系年）与前342（竹书纪年系年）两说，本记录采用通行前341年并标记 approximate。"),
    _ev("event-shangyang-bianfa", "商鞅变法", "reform",
        -356, -350, "range", "period-warring-states", "major",
        "秦孝公任用商鞅两次变法（前356年、前350年）：废井田、开阡陌，推行县制、军功爵制，"
        "统一度量衡并迁都咸阳，秦国自此建立耕战强国体制。商鞅变法是战国影响最深远的制度变革，"
        "为秦统一奠定根本基础。",
        f"古代史料：《史记·商君列传》；现代参考：{_M['zhanguo']}",
        W["shiji"],
        [_rel("event-maling-zhizhan", "follows"), _rel("event-yique-zhizhan", "leads_to", 0.8,
                                                       desc="商鞅变法使秦国军力跃居列国之上，开启东出之路"),
         _rel("event-zizhi-zhi-luan", "precedes")],
        review_note="商鞅变法分前356（初变法）、前350（二变法）两次；前338年孝公卒后商鞅遭车裂，但新法延续。"),
    _ev("event-zizhi-zhi-luan", "子之之乱", "political",
        -316, -314, "range", "period-warring-states", "major",
        "燕王哙约前316年让位于相国子之，引发燕国内乱，齐军乘机伐燕（前314年），燕国几亡，"
        "靠燕人反抗与诸侯干预得复国。此事件暴露列国变法与权力继承的激烈矛盾。",
        f"古代史料：《史记·燕召公世家》《战国策·燕策》；现代参考：{_M['zhanguo']}",
        W["shiji_zhanguoce"],
        [_rel("event-shangyang-bianfa", "follows"), _rel("event-qi-mie-song", "precedes")],
        review_note="子之之乱约前316—前314年（燕王哙让位至齐破燕），年代源自《史记》与《战国策》系年。"),
    _ev("event-qin-bing-bashu", "秦并巴蜀", "war",
        -316, -316, "year", "period-warring-states", "major",
        "前316年，秦惠文王纳司马错之议，派兵灭蜀、取巴，将富庶的巴蜀纳入秦国版图。"
        "巴蜀成为秦国粮仓与战略后方，为秦统一战争提供巨大资源支撑。",
        f"古代史料：《史记·秦本纪》《华阳国志》追述；现代参考：{_M['zhanguo']}",
        W["shiji"],
        [_rel("event-shangyang-bianfa", "follows"), _rel("event-zhangyi-po-chu", "precedes"),
         _rel("event-qin-mie-liuguo", "contributes_to", 0.7, desc="巴蜀粮仓为秦统一六国提供经济支撑")],
        review_note="秦并巴蜀前316年为《史记》系年；都江堰（前256年）即在巴蜀经营基础上修建。"),
    _ev("event-zhangyi-po-chu", "张仪欺楚", "diplomatic",
        -313, -311, "range", "period-warring-states", "major",
        "秦相张仪以外交欺诈拆散齐楚联盟：许诺割地诱楚怀王绝齐，随即毁约，"
        "楚秦交恶，秦军在丹阳、蓝田大败楚军（约前312年），楚国元气大伤。"
        "此事件为\"连横\"战略的典型案例。",
        f"古代史料：《史记·张仪列传》《战国策·秦策》；现代参考：{_M['zhanguo']}",
        W["shiji_zhanguoce"],
        [_rel("event-qin-bing-bashu", "follows"), _rel("event-hezong-lianheng", "part_of", 0.8,
                                                       desc="张仪连横外交为合纵连横格局中的\"连横\"代表")],
        review_note="张仪欺楚约前313年（楚怀王十六年前后）、丹阳蓝田之战约前312年，各书记载略有出入。"),
    _ev("event-hezong-lianheng", "合纵连横", "alliance",
        -334, -247, "approximate", "period-warring-states", "major",
        "战国中后期，苏秦倡导\"合纵\"（关东诸国联兵抗秦）与张仪推行\"连横\"（事秦以自保攻他国）交替运用，"
        "形成列国间纵横捭阖的外交格局。合纵连横时期是秦与关东诸国力量博弈的关键阶段。",
        f"古代史料：《史记·苏秦列传》《张仪列传》《战国策》；现代参考：{_M['zhanguo']}",
        W["shiji_zhanguoce"],
        [],
        review_note="\"合纵连横\"为战国中后期长期外交格局，起止为概括性约数（约前334—前247）；"
                    "苏秦张仪事迹部分见诸《战国策》与银雀山出土文献，细节有传异。"),
    _ev("event-jixia-xuegong", "稷下学宫兴办", "cultural",
        -374, -357, "approximate", "period-warring-states", "major",
        "田齐桓公（田午）在位（约前374—前357年）期间在临淄稷门设学宫，招揽诸子讲学议政，"
        "其后威王、宣王时极盛。稷下学宫是战国百家争鸣的中心场所，"
        "收录、论辩各家学说，为齐文化与诸子思想繁荣提供制度平台。",
        f"古代史料：《史记·田敬仲完世家》《盐铁论》追述；现代参考：{_M['zhanguo']}",
        W["shiji"],
        [_rel("event-tianshi-dai-qi", "follows"), _rel("event-hufu-qishe", "precedes")],
        review_note="稷下学宫创始年代以田齐桓公在位期（约前374—前357）估定，为概括性约数。"),
    _ev("event-hufu-qishe", "胡服骑射", "reform",
        -307, -302, "range", "period-warring-states", "major",
        "前307年起，赵武灵王推行\"胡服骑射\"，改穿胡服、建立骑兵，赵军战力大增，"
        "相继开拓北方与中山等国土地。胡服骑射是中国军事史上骑兵化、服装变革的里程碑。",
        f"古代史料：《史记·赵世家》；现代参考：{_M['zhanguo']}",
        W["shiji"],
        [_rel("event-jixia-xuegong", "follows"), _rel("event-shaqiu-gongbian", "precedes"),
         _rel("event-yuanmen-zhizhan", "leads_to", 0.7, desc="胡服骑射后赵军强盛，阏与之战即为赵军战力的体现")],
        review_note="胡服骑射始于前307年（赵武灵王十九年），至前302年前后完成，为阶段性改革。"),
    _ev("event-shaqiu-gongbian", "沙丘宫变", "political",
        -295, -295, "year", "period-warring-states", "major",
        "前295年，赵惠文王与公子成等围困退位的主父赵武灵王于沙丘宫，武灵王饿死，"
        "赵国权力交接以血腥政变完成。此事件体现赵国内部继承矛盾的激烈。",
        f"古代史料：《史记·赵世家》；现代参考：{_M['zhanguo']}",
        W["shiji"],
        [_rel("event-hufu-qishe", "follows"), _rel("event-yuanmen-zhizhan", "precedes")],
        review_note="沙丘宫变前295年为《史记》系年，无争议。"),
    _ev("event-yique-zhizhan", "伊阙之战", "war",
        -293, -293, "year", "period-warring-states", "major",
        "前293年，秦将白起在伊阙（今河南洛阳南）大败韩、魏联军，斩首二十四万，"
        "韩魏主力基本被歼。此役是白起成名之战，秦对关东的军事优势全面确立。",
        f"古代史料：《史记·白起王翦列传》；现代参考：{_M['zhanguo']}",
        W["shiji"],
        [_rel("event-shangyang-bianfa", "follows"), _rel("event-qi-mie-song", "precedes"),
         _rel("event-changping-zhizhan", "precedes")],
        review_note="伊阙之战前293年（秦昭襄王十四年）为《史记》系年，无争议。"),
    _ev("event-qi-mie-song", "齐灭宋", "war",
        -286, -286, "year", "period-warring-states", "major",
        "前286年，齐湣王出兵灭宋，齐国疆域骤扩，声势震动列国，"
        "但招致韩、赵、魏、燕、秦五国联合讨伐，为两年后的五国伐齐埋下伏笔。",
        f"古代史料：《史记·田敬仲完世家》《战国策》；现代参考：{_M['zhanguo']}",
        W["shiji_zhanguoce"],
        [_rel("event-zizhi-zhi-luan", "follows"), _rel("event-wuguo-fa-qi", "leads_to", 0.85,
                                                       desc="齐灭宋扩张激怒诸侯，直接促成五国伐齐")],
        review_note="齐灭宋前286年（齐湣王十五年）为通行纪年，无争议。"),
    _ev("event-wuguo-fa-qi", "五国伐齐（乐毅破齐）", "war",
        -284, -284, "year", "period-warring-states", "major",
        "前284年，燕昭王以乐毅为将，联合秦、赵、韩、魏五国伐齐，连下七十余城，"
        "齐湣王被杀，齐国仅存莒、即墨二城。齐从此由东方最强沦为二等国家，列国均势剧变。",
        f"古代史料：《史记·乐毅列传》《田单列传》；现代参考：{_M['zhanguo']}",
        W["shiji"],
        [_rel("event-qi-mie-song", "follows"), _rel("event-tiandan-fu-qi", "leads_to", 0.85,
                                                    desc="齐仅存即墨、莒两城，田单据此复国")],
        review_note="五国伐齐前284年为《史记》系年，无争议。"),
    _ev("event-tiandan-fu-qi", "田单复齐", "war",
        -279, -279, "year", "period-warring-states", "major",
        "前279年，齐将田单以\"火牛阵\"大破燕军于即墨，陆续收复七十余城，齐襄王复位，"
        "齐国复国。但齐国元气大伤，从此无力与秦争衡。",
        f"古代史料：《史记·田单列传》；现代参考：{_M['zhanguo']}",
        W["shiji"],
        [_rel("event-wuguo-fa-qi", "follows"), _rel("event-yuanmen-zhizhan", "precedes")],
        review_note="田单复齐前279年为《史记》系年，无争议。"),
    _ev("event-chu-mie-yue", "楚灭越", "war",
        -333, -333, "year", "period-warring-states", "major",
        "前333年，楚威王出兵伐越，杀越王无强，越国灭亡，吴越之争最终以楚收场。"
        "楚国将势力深入东南，但其后楚与秦的冲突日趋不利。",
        f"古代史料：《史记·越王勾践世家》；现代参考：{_M['zhanguo']}",
        W["shiji"],
        [_rel("event-zhangyi-po-chu", "precedes"), _rel("event-yique-zhizhan", "precedes")],
        review_note="楚灭越前333年为《史记》系年；越覆亡年代个别记载有出入。"),
    _ev("event-yuanmen-zhizhan", "阏与之战", "war",
        -269, -269, "year", "period-warring-states", "major",
        "前269年，秦军围攻赵地阏与（今山西和顺一带），赵将赵奢率军疾进，大破秦军。"
        "此役是胡服骑射后赵国对秦的少数胜仗之一，延迟了秦灭赵的进程。",
        f"古代史料：《史记·廉颇蔺相如列传》；现代参考：{_M['zhanguo']}",
        W["shiji"],
        [_rel("event-tiandan-fu-qi", "follows"), _rel("event-changping-zhizhan", "precedes")],
        review_note="阏与之战前269年（赵惠文王三十八年）为《史记》系年，无争议。"),
    _ev("event-changping-zhizhan", "长平之战", "war",
        -260, -260, "year", "period-warring-states", "critical",
        "前260年，秦将白起与赵括在长平（今山西高平一带）决战，赵军四十五万主力被围歼，"
        "赵国从此一蹶不振。此役是战国战争烈度巅峰，消灭了关东唯一可与秦抗衡的军事力量，"
        "秦统一六国的格局由此基本锁定。",
        f"古代史料：《史记·白起王翦列传》《廉颇蔺相如列传》；现代参考：{_M['zhanguo']}",
        W["shiji"],
        [_rel("event-yuanmen-zhizhan", "follows"), _rel("event-handan-zhizhan", "leads_to", 0.85,
                                                        desc="长平战后秦乘胜围邯郸，爆发邯郸之战"),
         _rel("event-qin-mie-liuguo", "leads_to", 0.8, desc="长平之战后关东再无力量阻挡秦的统一进程")],
        review_note="长平之战前260年为《史记》系年；\"坑杀（降卒）\"数量与考古证据（尸骨坑）存在学术讨论。"),
    _ev("event-handan-zhizhan", "邯郸之战", "war",
        -259, -257, "range", "period-warring-states", "major",
        "前259年至前257年，秦军长期围攻赵都邯郸，赵无力支撑，魏信陵君窃符救赵、楚春申君来援，"
        "秦军大败而还。邯郸之战使秦的统一推迟了近三十年，也是\"窃符救赵\"故事的史实背景。",
        f"古代史料：《史记·魏公子列传》《白起王翦列传》；现代参考：{_M['zhanguo']}",
        W["shiji"],
        [_rel("event-changping-zhizhan", "follows"), _rel("event-xinlingjun-hezong", "leads_to", 0.8,
                                                          desc="邯郸之围后信陵君威名大振，其再度合纵诸侯救他国")],
        review_note="邯郸之战前259—前257年；\"窃符救赵\"故事见《史记·魏公子列传》，属史载故事。"),
    _ev("event-xinlingjun-hezong", "信陵君合纵", "war",
        -247, -247, "year", "period-warring-states", "major",
        "前247年，魏信陵君（魏无忌）合纵韩、赵、魏、燕、楚五国联军，大败秦将蒙骜，"
        "直追至函谷关。这是合纵运动对秦难得的大胜，但未能从根本上阻止秦的统一进程。",
        f"古代史料：《史记·魏公子列传》；现代参考：{_M['zhanguo']}",
        W["shiji"],
        [_rel("event-handan-zhizhan", "follows"), _rel("event-qin-mie-liuguo", "precedes"),
         _rel("event-hezong-lianheng", "part_of", 0.7, desc="信陵君合纵为合纵格局后期代表行动")],
        review_note="信陵君合纵前247年为《史记》系年，无争议。"),
    _ev("event-qin-mie-dongzhou", "秦灭东周", "dynastic-transition",
        -256, -256, "year", "period-warring-states", "major",
        "前256年，秦昭襄王派兵灭西周（周赧王所居之周），取九鼎宝器；前249年秦又灭东周。"
        "延续约八百年的周王朝至此彻底终结，\"天下共主\"的名分体系消亡，"
        "秦的统一只剩军事收尾。",
        f"古代史料：《史记·周本纪》《秦本纪》；现代参考：{_M['zhanguo']}",
        W["shiji"],
        [_rel("event-handan-zhizhan", "follows"), _rel("event-qin-mie-liuguo", "precedes")],
        review_note="秦灭西周前256年、灭东周前249年；\"九鼎\"下落传说多在《史记》记载之外。"),
    _ev("event-dujiangyan-xiuzhu", "都江堰修筑", "economic",
        -256, -256, "approximate", "period-warring-states", "major",
        "秦昭襄王晚年，蜀郡守李冰组织修筑都江堰，使成都平原成为\"天府之国\"，"
        "为秦国提供稳定粮源，并沿用两千余年至今。修筑年代约前256年（亦有前277—前250诸说）。",
        f"古代史料：《史记·河渠书》《华阳国志》追述；现代参考：{_M['zhanguo']}",
        W["shiji"],
        [_rel("event-qin-bing-bashu", "follows"), _rel("event-qin-mie-liuguo", "contributes_to", 0.7,
                                                       desc="成都平原粮仓为秦统一提供物资支撑")],
        review_note="都江堰修筑年代约前256年（一说李冰任蜀守在秦昭襄王后期），属约略纪年。"),
    _ev("event-zheng-guoqu-xiuzhu", "郑国渠修筑", "economic",
        -246, -237, "approximate", "period-warring-states", "major",
        "秦王政元年（约前246年），韩国遣水工郑国入秦修渠，本为\"疲秦\"之计，"
        "反使关中灌溉四万余顷，秦国力大增。郑国渠与都江堰并列为秦统一的经济基石。",
        f"古代史料：《史记·河渠书》；现代参考：{_M['zhanguo']}",
        W["shiji"],
        [_rel("event-qin-mie-dongzhou", "follows"), _rel("event-qin-mie-liuguo", "contributes_to", 0.7,
                                                         desc="郑国渠使关中沃野千里，支撑秦的战争机器")],
        review_note="郑国渠约前246年开工、约前237年前后建成，各记载年代略有出入，属约略纪年。"),
    _ev("event-qin-mie-liuguo", "秦灭六国", "unification",
        -230, -221, "range", "period-warring-states", "critical",
        "秦王政自前230年灭韩起，历经十年，先后灭韩、赵、燕、魏、楚、齐，至前221年完成统一。"
        "秦灭六国结束战国数百年的兼并局面，是秦统一战争的总体进程（aggregate event，"
        "各阶段灭国节点见其 part_of 子事件）。",
        f"古代史料：《史记·秦始皇本纪》；现代参考：{_M['zhanguo']}",
        W["shiji"],
        [_rel("event-changping-zhizhan", "follows"), _rel("event-qin-tongyi", "leads_to", 0.95,
                                                          desc="灭六国直接导向秦帝国的建立")],
        review_note="秦灭六国为覆盖前230—前221年的过程事件（aggregate），各子事件按《史记·秦始皇本纪》系年。"),
    _ev("event-qin-mie-han", "秦灭韩", "war",
        -230, -230, "year", "period-warring-states", "major",
        "前230年，秦派内史腾攻韩，俘韩王安，韩国灭亡。韩国为秦统一战争首个被灭之国。",
        f"古代史料：《史记·秦始皇本纪》《韩世家》；现代参考：{_M['zhanguo']}",
        W["shiji"],
        [_rel("event-qin-mie-liuguo", "part_of", 0.95, desc="秦灭韩为秦灭六国进程第一步")],
        review_note="前230年灭韩为《史记》系年，无争议。"),
    _ev("event-qin-mie-zhao", "秦灭赵", "war",
        -228, -228, "year", "period-warring-states", "major",
        "前228年，秦将王翦攻占邯郸，俘赵王迁，赵国灭亡（公子嘉奔代地自立，前222年亦亡）。"
        "赵国为长平战后唯一仍有抵抗力的关东大国。",
        f"古代史料：《史记·秦始皇本纪》《赵世家》；现代参考：{_M['zhanguo']}",
        W["shiji"],
        [_rel("event-qin-mie-liuguo", "part_of", 0.95, desc="秦灭赵为秦灭六国进程的第二步")],
        review_note="前228年秦灭赵（前222年代亡）为《史记》系年。"),
    _ev("event-jingke-ci-qin", "荆轲刺秦", "political",
        -227, -227, "year", "period-warring-states", "major",
        "前227年，燕太子丹遣荆轲携樊於期首级与督亢地图入秦，图穷匕见刺秦王政未遂，"
        "荆轲被杀。刺秦失败加速秦攻燕，\"荆轲刺秦\"成为后世传颂的著名悲剧事件。",
        f"古代史料：《史记·刺客列传》；现代参考：{_M['zhanguo']}",
        W["shiji"],
        [_rel("event-qin-mie-liuguo", "part_of", 0.8, desc="荆轲刺秦为秦灭燕过程中的著名插曲")],
        review_note="荆轲刺秦前227年为《史记》系年；其事迹见于《史记·刺客列传》，文学化记载鲜明。"),
    _ev("event-qin-mie-yan", "秦灭燕", "war",
        -226, -222, "range", "period-warring-states", "major",
        "前226年，秦将王贲攻取燕都蓟，燕王喜迁辽东；前222年秦军再攻辽东，俘燕王喜，燕国灭亡。",
        f"古代史料：《史记·秦始皇本纪》《燕召公世家》；现代参考：{_M['zhanguo']}",
        W["shiji"],
        [_rel("event-qin-mie-liuguo", "part_of", 0.95, desc="秦灭燕为秦灭六国进程的一部分")],
        review_note="秦灭燕（前226年克蓟、前222年灭辽东）为《史记》系年。"),
    _ev("event-qin-mie-wei", "秦灭魏", "war",
        -225, -225, "year", "period-warring-states", "major",
        "前225年，秦将王贲引黄河、鸿沟之水灌魏都大梁，城坏，魏王假出降，魏国灭亡。",
        f"古代史料：《史记·秦始皇本纪》《魏世家》；现代参考：{_M['zhanguo']}",
        W["shiji"],
        [_rel("event-qin-mie-liuguo", "part_of", 0.95, desc="秦灭魏为秦灭六国进程的一部分")],
        review_note="前225年灭魏为《史记》系年。"),
    _ev("event-qin-mie-chu", "秦灭楚", "war",
        -224, -223, "range", "period-warring-states", "major",
        "前224年，秦王政起用王翦率六十万大军伐楚；前223年攻破寿春，俘楚王负刍，楚国灭亡。"
        "楚国为灭国战争中抵抗最烈、耗时最长的大国。",
        f"古代史料：《史记·秦始皇本纪》《楚世家》《白起王翦列传》；现代参考：{_M['zhanguo']}",
        W["shiji"],
        [_rel("event-qin-mie-liuguo", "part_of", 0.95, desc="秦灭楚为秦灭六国进程的一部分")],
        review_note="秦灭楚（前224年大举伐楚、前223年灭楚）为《史记》系年。"),
    _ev("event-qin-mie-qi", "秦灭齐", "war",
        -221, -221, "year", "period-warring-states", "major",
        "前221年，秦将王贲自燕南攻齐，齐王建不战而降，齐国灭亡。齐为六国中最后被灭者，"
        "秦统一战争至此完成。",
        f"古代史料：《史记·秦始皇本纪》《田敬仲完世家》；现代参考：{_M['zhanguo']}",
        W["shiji"],
        [_rel("event-qin-mie-liuguo", "part_of", 0.95, desc="秦灭齐完成秦灭六国的最后一步")],
        review_note="前221年灭齐为《史记》系年。"),
    _ev("event-qin-tongyi", "秦统一六国（秦帝国建立）", "unification",
        -221, -221, "year", "period-warring-states", "critical",
        "前221年，秦王政兼并六国后自称\"始皇帝\"，建立中国历史上第一个中央集权的统一帝国，"
        "行郡县、书同文、车同轨、统一度量衡（制度层面细节另见秦汉批）。"
        "秦统一是先秦历史的终结，也是中国大一统格局的开端。",
        f"古代史料：《史记·秦始皇本纪》；现代参考：{_M['zhanguo']}",
        W["shiji"],
        [_rel("event-qin-mie-liuguo", "follows")],
        review_note="秦统一前221年为确定纪年；统一后各项制度变革（郡县/文字/度量衡）留待秦汉批详细展开。"),
]

ALL_PHASES = [
    ("pre_qin", "Phase A（上古/夏/商/西周）", PHASE_A),
    ("chunqiu_zhanguo", "Phase B（春秋）", PHASE_B),
    ("chunqiu_zhanguo", "Phase C（战国）", PHASE_C),
]


def all_events():
    """返回全部 (目录, phase_label, event_dict) 列表。"""
    return [(directory, label, ev) for directory, label, events in ALL_PHASES for ev in events]