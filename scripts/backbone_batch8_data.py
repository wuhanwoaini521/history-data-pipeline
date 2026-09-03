# -*- coding: utf-8 -*-
"""China History Backbone V1 — Batch 8（中华民国→近现代 1912—1949）Data（part 1）。

原则（§53/§65）：只做 Chronology Backbone；无价值判断/意识形态评价/英雄反派叙事；
每条事件至少 1 个档案/史料类来源 + 1 个现代权威研究；否则 quality_status=needs_review 不强行 reviewed。

复用：event-nanjing-linshi-zhengfu（1912-01-01 南京临时政府，Batch7）。

阶段拆分（阶段提交）：
- REPUBLIC_EARLY  民国初期（1912—1916）
- WARLORDS_MAY4TH 军阀混战与五四（1917—1926）
- NATIONAL_REV    国民革命与北伐（1924—1928）
- CPC_EARLY       中共早期节点（1921—1936）
- JAPAN_INVASION  日本侵华（1931—1936）
- FULL_WAR_1949   全面抗战与 1949 边界（1937—1949）
"""

from __future__ import annotations

MODERN = {
    "minguo": "张宪文主编《中华民国史》（南京大学出版社）；金冲及《二十世纪中国史纲》（社会科学文献出版社）；"
              "郭廷以《近代中国史纲》",
    "warlord": "张宪文主编《中华民国史》；金冲及《二十世纪中国史纲》；王桧林主编《中国现代史》"
               "（北京师范大学出版社）",
    "cpc": "中共中央党史研究室著《中国共产党历史》第一卷（中共党史出版社）；"
           "军事科学院《中国抗日战争史》；金冲及《二十世纪中国史纲》",
    "kangzhan": "军事科学院《中国抗日战争史》（军事科学出版社）；中央档案馆与江苏省档案馆等合编"
                "《南京大屠杀史料集》（江苏人民出版社）；张宪文主编《中华民国史》",
    "1945": "中共中央党史研究室《中国共产党历史》第一卷；张宪文主编《中华民国史》；"
            "金冲及《二十世纪中国史纲》",
}

WP = {
    "minguo": ["work-curated-minguoshi"],
    "minguo_kz": ["work-curated-minguoshi", "work-curated-kangzhanshi"],
    "kz": ["work-curated-kangzhanshi"],
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
# Phase 1 — 民国初期（1912—1916）
# ---------------------------------------------------------------------------
PHASE_REPUBLIC_EARLY = [
    _ev("event-yuanshikai-jiuwei", "袁世凯就任临时大总统（北京政府形成）", "succession",
        1912, 1912, "year", "period-republic", "major",
        "1912 年 2 月清帝退位后，南京临时参议院选举袁世凯为临时大总统，"
        "3 月袁世凯在北京就职，临时政府北迁，北京政府（北洋政府）时期开始。",
        f"档案史料：南京临时政府公报、《临时约法》提案；现代研究：{MODERN['minguo']}",
        WP["minguo"],
        ["regime-republic"],
        relations=[
            _rel("event-nanjing-linshi-zhengfu", "follows", 0.9, "南北和议以让位换职后袁世凯就任。"),
            _rel("event-linshi-yuefa", "precedes", 0.6, "临时约法同期颁布。"),
        ]),
    _ev("event-linshi-yuefa", "《中华民国临时约法》颁布", "treaty",
        1912, 1912, "year", "period-republic", "major",
        "1912 年 3 月 11 日，孙中山以临时大总统名义公布《中华民国临时约法》，"
        "确立主权在民、三权分立等原则，为民国初年之宪法性文件；"
        "袁世凯就任后曾谋求修改约法。",
        f"档案史料：临时约法文本（南京临时政府公报）；现代研究：{MODERN['minguo']}",
        WP["minguo"],
        ["regime-republic"],
        relations=[
            _rel("event-yuanshikai-jiuwei", "follows", 0.6, "与袁世凯就任同期颁布。"),
        ]),
    _ev("event-songjiaoren-yuci", "宋教仁遇刺", "political",
        1913, 1913, "year", "period-republic", "major",
        "1913 年 3 月，国民党代理理事长宋教仁在上海火车站遇刺身亡，"
        "舆论指向袁世凯政府；“宋案”成为二次革命的直接导火索。",
        f"档案史料：宋案各报报道与庭审材料；现代研究：{MODERN['minguo']}",
        WP["minguo"],
        ["regime-republic"],
        relations=[
            _rel("event-linshi-yuefa", "follows", 0.7, "约法体制下政党政治受挫。"),
            _rel("event-erci-geming", "leads_to", 0.9, "宋案引发二次革命。"),
        ],
        review_note="宋案凶手与幕后指使（应桂馨、洪述祖与袁世凯的关系）是民国初年著名公案，"
                    "史界对指使层级有不同考证；本事件记录遇刺事实与政治后果。"),
    _ev("event-erci-geming", "二次革命（讨袁战争）", "war",
        1913, 1913, "year", "period-republic", "major",
        "1913 年 7 月，孙中山、黄兴等发动武装讨袁（二次革命），"
        "江西李烈钧、南京黄兴等相继宣布独立，因准备不足与实力悬殊，"
        "月余即告失败，国民党势力大受打击，袁世凯强化控制。",
        f"档案史料：二次革命各省通电与政府公报；现代研究：{MODERN['minguo']}",
        WP["minguo"],
        ["regime-republic"],
        relations=[
            _rel("event-songjiaoren-yuci", "follows", 0.9, "宋案后的武装讨袁。"),
            _rel("event-yuanshikai-chendi", "leads_to", 0.8, "二次革命后袁世凯进一步集权称帝。"),
        ]),
    _ev("event-yuanshikai-chendi", "袁世凯称帝（洪宪帝制）", "political",
        1915, 1915, "year", "period-republic", "major",
        "1915 年 12 月，袁世凯接受帝制复辟称谓，改国号为中华帝国，建元洪宪；"
        "此举激起全国反对，护国战争随即爆发。",
        f"档案史料：洪宪帝制相关令文与各省通电；现代研究：{MODERN['minguo']}",
        WP["minguo"],
        ["regime-republic"],
        relations=[
            _rel("event-erci-geming", "follows", 0.8, "二次革命后袁世凯力图恢复帝制。"),
            _rel("event-huguo-zhanzheng", "leads_to", 0.95, "称帝引发护国战争。"),
        ]),
    _ev("event-huguo-zhanzheng", "护国战争", "war",
        1915, 1916, "range", "period-republic", "major",
        "1915 年 12 月至 1916 年 6 月，蔡锷等在云南起兵讨袁（护国战争），"
        "滇黔桂粤相继响应，袁世凯被迫于 1916 年 3 月取消帝制，"
        "战争以袁世凯取消帝制与去世告终。",
        f"档案史料：护国军通电与战报；现代研究：{MODERN['minguo']}",
        WP["minguo"],
        ["regime-republic"],
        relations=[
            _rel("event-yuanshikai-chendi", "follows", 0.95, "起兵讨伐洪宪帝制。"),
            _rel("event-yuanshikai-qushi", "leads_to", 0.9, "取消帝制后袁世凯去世。"),
        ]),
    _ev("event-yuanshikai-qushi", "袁世凯取消帝制与去世", "political",
        1916, 1916, "year", "period-republic", "major",
        "1916 年 3 月 22 日袁世凯下令取消帝制，恢复民国纪年，"
        "6 月 6 日袁世凯病逝，北京政府进入北洋军阀各派系交替掌权的时期。",
        f"档案史料：袁氏称帝取消令与《政府公报》；现代研究：{MODERN['minguo']}",
        WP["minguo"],
        ["regime-republic"],
        relations=[
            _rel("event-huguo-zhanzheng", "follows", 0.9, "护国战争迫使取消帝制。"),
        ]),
]