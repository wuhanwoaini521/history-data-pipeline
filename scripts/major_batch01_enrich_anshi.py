"""Major Batch 01 · 安史之乱群 enrichment（9 个 READY/PARTIAL 事件）。

- 补 background/process/impact 三维 + 四字段证据锚（manual 段落锚 + 逐字引文）；
- 现有 legacy result_zh_cn 保留不覆盖，另加 result 字段锚；
- event-anlu-changan-recapture 的 1 条 pending_knowledge（资治通鉴·郭子仪）本轮关闭：
  锚定 唐纪三十六#p26「贼弃城走矣」（收复长安之证）。
- 写入 append-only。
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
EVENTS = ROOT / "data" / "curated" / "history_backbone" / "events"


def ev(work, term, tid, anchor, field, role, quote, extra=""):
    return {
        "work": work, "term": term, "historical_text_id": tid, "chapter_anchor": anchor,
        "claim_field": field, "evidence_role": role, "link_status": "linked",
        "link_method": "manual", "link_confidence": 1.0, "link_quality_status": "reviewed",
        "context_keywords": [],
        "review_note": f"major-batch01：source-grounded（资治通鉴/旧唐书）引文：「{quote}」；"
                       f"claim_field={field}；anchor=段落精确锚。{extra}",
    }


BLOCKS = {
    "sui_tang/event-anlu-uprising.yml": {
        "background_zh_cn": "禄山诈为敕书，悉召诸将示之曰「有密旨，令禄山将兵入朝讨杨国忠，诸君宜即从军」——以「清君侧」为名发动叛乱。",
        "process_zh_cn": "禄山乘铁舆，步骑精锐，烟尘千里，鼓噪震地；范阳节度使安禄山率蕃、汉之兵十余万，自幽州南向诣阙，以诛杨国忠为名，先杀太原尹杨光翙于博陵郡。",
        "impact_zh_cn": "唐廷仓促应变：遣特进毕思琛诣东京、金吾将军程千里诣河东，各简募数万人随便团结以拒之——安史之乱全面爆发。",
        "people": [
            {"person_name_raw": "颜真卿", "role": "supporter", "link_status": "needs_linking",
             "role_zh_cn": "平原太守：禄山反后以平原、博平兵防河津",
             "review_note": "major-batch01：唐纪三十三「及禄山反，牒真卿以平原、博平兵七千人防河津」", "person_id": None},
        ],
        "evidence": [
            ev("资治通鉴", "唐纪三十三", "text-niutrans-2944efc9cf410c85e5f2", "唐纪/唐纪三十三#p119",
               "background", "primary", "禄山诈为敕书，悉召诸将示之曰： 有密旨，令禄山将兵入朝讨杨国忠，诸君宜即从军。"),
            ev("资治通鉴", "唐纪三十三", "text-niutrans-c0175f42331a240bd278", "唐纪/唐纪三十三#p125",
               "process", "primary", "禄山乘铁舆，步骑精锐，烟尘千里，鼓噪震地。"),
            ev("旧唐书", "卷九", "text-niutrans-a7eadbd9573bc3bf039b", "本纪/卷九#p376",
               "result", "primary", "丙寅，范阳节度使安禄山率蕃、汉之兵十余万，自幽州南向诣阙，以诛杨国忠为名。"),
            ev("资治通鉴", "唐纪三十三", "text-niutrans-e8cdcf5c55cf2dec75fa", "唐纪/唐纪三十三#p136",
               "impact", "primary", "上遣特进毕思琛诣东京，金吾将军程千里诣河东，各简募数万人，随便团结以拒之。"),
        ],
    },
    "sui_tang/event-anlu-three-frontiers.yml": {
        "background_zh_cn": "天宝元年，以平卢为节度，以禄山摄中丞为使——安禄山由营州杂胡军官起步，渐掌方面。",
        "process_zh_cn": "三载，代裴宽为范阳节度、河北采访、平卢军等使如故；十载入朝，又求为河东节度，因拜之。",
        "impact_zh_cn": "兼三道节度，进奏无不允——安禄山以平卢、范阳、河东三镇之兵与财赋，成为唐廷北方最强大的军事-政治集团，为起兵奠定基础。",
        "evidence": [
            ev("旧唐书", "安禄山传", "text-niutrans-357b996f74936fd7ee2c", "列传/卷一百五十#p19",
               "background", "primary", "天宝元年，以平卢为节度，以禄山摄中丞为使。"),
            ev("旧唐书", "安禄山传", "text-niutrans-fdf57a816f057a9f844e", "列传/卷一百五十#p21",
               "process", "primary", "三载，代裴宽为范阳节度，河北采访、平卢军等使如故。"),
            ev("旧唐书", "安禄山传", "text-niutrans-01a333457c24b9845804", "列传/卷一百五十#p40",
               "result", "primary", "十载入朝，又求为河东节度，因拜之。"),
            ev("旧唐书", "安禄山传", "text-niutrans-928b1cd55141795ed818", "列传/卷一百五十#p44",
               "impact", "primary", "兼三道节度，进奏无不允。"),
        ],
    },
    "sui_tang/event-anlu-luoyang.yml": {
        "background_zh_cn": "封常清即日乘驿诣东京募兵，旬日得六万人，乃断河阳桥，为守御之备——唐廷以东都防线迎击叛军。",
        "process_zh_cn": "丁酉，禄山陷东京，贼鼓噪自四门入，纵兵杀掠；杀留守李憕、中丞卢奕、判官蒋清。",
        "impact_zh_cn": "叛军以洛阳为基地继续扩张：蔡希德至洛阳，安禄山复使将步骑二万人北就思明，又使牛廷玠发范阳等郡兵万馀人助之，合五万馀人——东都陷落使唐廷东西两线同时告急。",
        "people": [
            {"person_name_raw": "封常清", "role": "opponent", "link_status": "needs_linking",
             "role_zh_cn": "安西节度使：入东京募兵守御，兵败",
             "review_note": "major-batch01：唐纪三十三「常清即日乘驿诣东京募兵……为守御之备」", "person_id": None},
        ],
        "evidence": [
            ev("资治通鉴", "唐纪三十三", "text-niutrans-3b646ae2806e58af7b39", "唐纪/唐纪三十三#p141",
               "background", "primary", "常清即日乘驿诣东京募兵，旬日，得六万人；乃断河阳桥，为守御之备。"),
            ev("资治通鉴", "唐纪三十三", "text-niutrans-de5b69527dee43b3ee19", "唐纪/唐纪三十三#p180",
               "process", "primary", "丁酉，禄山陷东京，贼鼓噪自四门入，纵兵杀掠。"),
            ev("旧唐书", "卷九", "text-niutrans-3d334bb7fa0ce5c821fd", "本纪/卷九#p388",
               "result", "primary", "丁酉，禄山陷东京，杀留守李憕、中丞卢奕、判官蒋清。"),
            ev("资治通鉴", "唐纪三十四", "text-niutrans-ca347c9043a904770304", "唐纪/唐纪三十四#p13",
               "impact", "primary", "蔡希德至洛阳，安禄山复使将步骑二万人北就思明，又使牛廷玠发范阳等郡兵万馀人助思明，合五万馀人。"),
        ],
    },
    "sui_tang/event-anlu-tongguan.yml": {
        "background_zh_cn": "唐军守潼关、数月不能进；北路已绝、诸军四合，叛军所占止汴、郑数州——双方在潼关一线对峙。",
        "process_zh_cn": "乾祐据险以待之，南薄山、北阻河，隘道七十里；贼伏兵于险，官军望其兵少而进。",
        "impact_zh_cn": "先是四方闻潼关失守，莫知上所之，及是制下，始知乘舆所在——潼关陷落使长安门户洞开、天下震动，唐廷信息与号令一时中断。",
        "people": [
            {"person_name_raw": "哥舒翰", "role": "opponent", "link_status": "needs_linking",
             "role_zh_cn": "唐军主帅：守潼关兵败被擒",
             "review_note": "major-batch01：唐纪三十四「安禄山问翰曰：汝常轻我，今定何如？」（翰被俘之证）", "person_id": None},
            {"person_name_raw": "崔乾祐", "role": "opponent", "link_status": "needs_linking",
             "role_zh_cn": "叛军将领：据险设伏大破官军于潼关隘道",
             "review_note": "major-batch01：唐纪三十四「乾祐据险以待之，南薄山，北阻河，隘道七十里」", "person_id": None},
        ],
        "evidence": [
            ev("资治通鉴", "唐纪三十四", "text-niutrans-954521afe14dcf226ae4", "唐纪/唐纪三十四#p21",
               "background", "primary", "今守潼关，数月不能进，北路已绝，诸军四合，吾所有者止汴、郑数州而已，万全何在？"),
            ev("资治通鉴", "唐纪三十四", "text-niutrans-821be43d2b46f8abe510", "唐纪/唐纪三十四#p54",
               "process", "primary", "乾祐据险以待之，南薄山，北阻河，隘道七十里。"),
            ev("资治通鉴", "唐纪三十四", "text-niutrans-e1d4ee180fef82c39a3a", "唐纪/唐纪三十四#p61",
               "result", "primary", "须臾，伏兵发，贼乘高下木石，击杀士卒甚众。"),
            ev("资治通鉴", "唐纪三十四", "text-niutrans-5019a005d06ed9111b68", "唐纪/唐纪三十四#p298",
               "impact", "primary", "先是四方闻潼关失守，莫知上所之，及是制下，始知乘舆所在。"),
        ],
    },
    "sui_tang/event-anlu-changan.yml": {
        "background_zh_cn": "乙未，黎明，上独与贵妃姊妹、皇子、妃、主、皇孙、杨国忠、韦见素、魏方进、陈玄礼及亲近宦官、宫人出延秋门——潼关失守后玄宗密行西出。",
        "process_zh_cn": "贼入长安方虏掠，未暇徇地——叛军进入长安后纵兵掠夺。",
        "impact_zh_cn": "由是诸道始知上即位于灵武，徇国之心益坚矣——长安失守与肃宗即位后，唐廷以灵武为中枢重聚号令。",
        "people": [
            {"person_name_raw": "唐肃宗", "role": "monarch", "link_status": "needs_linking",
             "role_zh_cn": "太子李亨：长安失守后即位于灵武",
             "review_note": "major-batch01：唐纪三十四「是日，肃宗即位于灵武城南楼」", "person_id": None},
        ],
        "evidence": [
            ev("资治通鉴", "唐纪三十四", "text-niutrans-b7f8fdd603a6b981b8bf", "唐纪/唐纪三十四#p104",
               "background", "primary", "乙未，黎明，上独与贵妃姊妹、皇子、妃、主、皇孙、杨国忠、韦见素、魏方进、陈玄礼及亲近宦官、宫人出延秋门。"),
            ev("资治通鉴", "唐纪三十四", "text-niutrans-eb9af9eebf6d1cd71636", "唐纪/唐纪三十四#p204",
               "process", "primary", "贼入长安方虏掠，未暇徇地。"),
            ev("资治通鉴", "唐纪三十四", "text-niutrans-bd8c9eb00dd002fd7f76", "唐纪/唐纪三十四#p271",
               "result", "primary", "是日，肃宗即位于灵武城南楼，群臣舞蹈，上流涕歔欷。"),
            ev("资治通鉴", "唐纪三十四", "text-niutrans-92f4254585a02712963b", "唐纪/唐纪三十四#p368",
               "impact", "primary", "由是诸道始知上即位于灵武，徇国之心益坚矣。"),
        ],
    },
    "sui_tang/event-anlu-xuanzong-shu.yml": {
        "background_zh_cn": "杨国忠自以身领剑南，闻安禄山反，即令副使崔圆阴具储偫，以备有急投之，至是首唱幸蜀之策。",
        "process_zh_cn": "丙申，至马嵬驿，将士饥疲、皆愤怒——马嵬驿之变后玄宗一行继续西行。",
        "impact_zh_cn": "庚辰，上皇至成都，从官及六军至者千三百人而已——玄宗入蜀后其随行力量大为缩减，唐廷中枢实际转入肃宗灵武集团。",
        "people": [
            {"person_name_raw": "杨国忠", "role": "opponent", "link_status": "needs_linking",
             "role_zh_cn": "宰相：首唱幸蜀之策",
             "review_note": "major-batch01：唐纪三十四「至是首唱幸蜀之策」", "person_id": None},
        ],
        "evidence": [
            ev("资治通鉴", "唐纪三十四", "text-niutrans-60545dbc44bbb963083f", "唐纪/唐纪三十四#p91",
               "background", "primary", "杨国忠自以身领剑南，闻安禄山反，即令副使崔圆阴具储偫，以备有急投之，至是首唱幸蜀之策。"),
            ev("资治通鉴", "唐纪三十四", "text-niutrans-60170da0c721234bc011", "唐纪/唐纪三十四#p132",
               "process", "primary", "丙申，至马嵬驿，将士饥疲，皆愤怒。"),
            ev("资治通鉴", "唐纪三十四", "text-niutrans-df4433eb84de829f2bcd", "唐纪/唐纪三十四#p190",
               "result", "primary", "上命悉陈之于庭，召将士入，临轩谕之曰： 朕比来衰耄，托任失人，致逆胡乱常，须远避其锋。"),
            ev("资治通鉴", "唐纪三十四", "text-niutrans-d4c7bfd38e9d7c7d0065", "唐纪/唐纪三十四#p330",
               "impact", "primary", "庚辰，上皇至成都，从官及六军至者千三百人而已。"),
        ],
    },
    "sui_tang/event-anlu-changan-recapture.yml": {
        "background_zh_cn": "李嗣业为前军，郭子仪为中军，王思礼为后军——唐军会合回纥、诸道之兵列阵长安城西。",
        "process_zh_cn": "李嗣业肉袒执长刀立于阵前，大呼奋击，当其刀者人马俱碎，阵乃稍定；嗣业帅前军各执长刀如墙而进，所向摧靡。",
        "impact_zh_cn": "贼遂大溃、馀众走入城；仆固怀恩言于广平王「贼弃城走矣，请以二百骑追之」——叛军弃长安而走，唐廷收复都城。",
        "people": [
            {"person_name_raw": "李嗣业", "role": "supporter", "link_status": "needs_linking",
             "role_zh_cn": "唐军前军主将：香积寺之战肉袒执刀破阵",
             "review_note": "major-batch01：唐纪三十六「乃肉袒，执长刀，立于阵前，大呼奋击」", "person_id": None},
        ],
        "evidence": [
            ev("资治通鉴", "唐纪三十六", "text-niutrans-872168780f703dff040e", "唐纪/唐纪三十六#p16",
               "background", "primary", "李嗣业为前军，郭子仪为中军，王思礼为后军。"),
            ev("资治通鉴", "唐纪三十六", "text-niutrans-6f871808314e9df8a621", "唐纪/唐纪三十六#p19",
               "process", "primary", "乃肉袒，执长刀，立于阵前，大呼奋击，当其刀者，人马俱碎，杀数十人，阵乃稍定。"),
            ev("资治通鉴", "唐纪三十六", "text-niutrans-16738435827118de66ab", "唐纪/唐纪三十六#p24",
               "result", "primary", "李嗣业又与回纥出贼阵后，与大军交击，自午及酉，斩首六万级……贼遂大溃。"),
            ev("资治通鉴", "唐纪三十六", "text-niutrans-7f583ac3fa0eee240354", "唐纪/唐纪三十六#p26",
               "impact", "primary", "仆固怀恩言于广平王俶曰： 贼弃城走矣，请以二百骑追之。"),
        ],
    },
    "sui_tang/event-anlu-shi-siming.yml": {
        "background_zh_cn": "及安庆绪败，承恩说思明降唐——史思明一度降唐，旋复叛自立。",
        "process_zh_cn": "春正月己巳朔，史思明筑坛于魏州城北，自称大圣燕王，以周挚为行军司马。",
        "impact_zh_cn": "史思明手疏唁庆绪而不称臣，曰「愿为兄弟之国，更作籓篱之援」——安庆绪收粮拒守、思明与庆绪决裂，叛乱由安禄山集团转入史思明主导阶段。",
        "people": [
            {"person_name_raw": "安庆绪", "role": "opponent", "link_status": "needs_linking",
             "role_zh_cn": "安禄山之子：继掌叛军，后与思明决裂",
             "review_note": "major-batch01：唐纪三十七「安庆绪收子仪等营中粮……谋闭门更拒思明」", "person_id": None},
        ],
        "evidence": [
            ev("资治通鉴", "唐纪三十六", "text-niutrans-4b0ee4c7d862ddc22d82", "唐纪/唐纪三十六#p338",
               "background", "primary", "及安庆绪败，承恩说思明降唐。"),
            ev("资治通鉴", "唐纪三十七", "text-niutrans-0ace3ebee9c2275397cf", "唐纪/唐纪三十七#p4",
               "process", "primary", "春，正月，己巳朔，史思明筑坛于魏州城北，自称大圣燕王。"),
            ev("资治通鉴", "唐纪三十七", "text-niutrans-1abb3f671bbdbde79cac", "唐纪/唐纪三十七#p47",
               "result", "primary", "安庆绪收子仪等营中粮，得六七万石，与孙孝哲、崔乾祐谋闭门更拒思明。"),
            ev("资治通鉴", "唐纪三十七", "text-niutrans-acafa9078ac2cef59064", "唐纪/唐纪三十七#p57",
               "impact", "primary", "乃手疏唁庆绪而不称臣，且曰： 愿为兄弟之国，更作籓篱之援。"),
        ],
    },
    "sui_tang/event-anlu-pacification.yml": {
        "background_zh_cn": "上遣中使刘清潭使于回纥，修旧好，且征兵讨史朝义——唐廷借回纥与诸道之兵发起最后反攻。",
        "process_zh_cn": "史朝义闻官军将至，谋于诸将；东奔广阳不受，欲北入奚、契丹，至温泉栅，李怀仙兵追及之，朝义穷蹙，缢于林中，怀仙取其首以献。",
        "impact_zh_cn": "以史朝义下降将李宝臣为成德军节度使、薛嵩为相卫等州节度使、李怀仙为卢龙节度使等——叛乱虽平，河北降将分授藩镇，唐廷中央权威下降、藩镇格局自此埋下。",
        "people": [
            {"person_name_raw": "史朝义", "role": "opponent", "link_status": "needs_linking",
             "role_zh_cn": "史思明之子：叛军末代首领，穷蹙自缢",
             "review_note": "major-batch01：唐纪三十八「朝义穷蹙，缢于林中，怀仙取其首以献」", "person_id": None},
            {"person_name_raw": "李怀仙", "role": "opponent", "link_status": "needs_linking",
             "role_zh_cn": "叛军降将：追杀朝义、献其首",
             "review_note": "major-batch01：唐纪三十八「至温泉栅，李怀仙兵追及之」", "person_id": None},
        ],
        "evidence": [
            ev("资治通鉴", "唐纪三十八", "text-niutrans-54c2ac3a45c999228f05", "唐纪/唐纪三十八#p291",
               "background", "primary", "上遣中使刘清潭使于回纥，修旧好，且征兵讨史朝义。"),
            ev("资治通鉴", "唐纪三十八", "text-niutrans-bafb12908447d37aab68", "唐纪/唐纪三十八#p375",
               "process", "primary", "东奔广阳，广阳不受；欲北入奚、契丹，至温泉栅，李怀仙兵追及之；朝义穷蹙，缢于林中，怀仙取其首以献。"),
            ev("旧唐书", "卷十一", "text-niutrans-2e5651d41a2967b20284", "本纪/卷十一#p92",
               "result", "primary", "以史朝义下降将李宝臣为检校礼部尚书、兼御史大夫、恆州刺史、清河郡王，充成德军节度使。"),
            ev("资治通鉴", "唐纪三十九", "text-niutrans-102bd1d9cee1891a590b", "唐纪/唐纪三十九#p5",
               "impact", "primary", "诸将讨史朝义者进官阶、加爵邑有差。"),
        ],
    },
}


def close_last_pending() -> int:
    """event-anlu-changan-recapture 的 pending 行（资治通鉴·郭子仪）锚定到唐纪三十六#p26。"""
    import sys as _sys
    _sys.path.insert(0, str(ROOT / "src"))
    from history_data_pipeline.backbone.evidence_link import _load_event_yaml
    path = EVENTS / "sui_tang" / "event-anlu-changan-recapture.yml"
    doc, (head, tail) = _load_event_yaml(path)
    changed = 0
    for evidence in doc.get("evidence") or []:
        if evidence.get("link_status") == "pending_knowledge" and evidence.get("work") == "资治通鉴":
            evidence["historical_text_id"] = "text-niutrans-7f583ac3fa0eee240354"
            evidence["chapter_anchor"] = "唐纪/唐纪三十六#p26"
            evidence["link_method"] = "manual"
            evidence["link_status"] = "linked"
            evidence["link_confidence"] = 0.85
            evidence["link_quality_status"] = "reviewed"
            evidence["review_note"] = (
                "major-batch01：legacy 悬空锚重定位——唐军收复长安核心段（广平王止追、"
                "叛军弃城）。引文：「贼弃城走矣，请以二百骑追之。」；anchor=段落精确锚。")
            changed += 1
    if changed:
        path.write_text(head + yaml.safe_dump(doc, allow_unicode=True, sort_keys=False,
                                               default_flow_style=False, width=10**6) + tail,
                        encoding="utf-8")
    return changed


def main() -> int:
    applied = 0
    for rel, block in BLOCKS.items():
        path = EVENTS / rel
        existing = yaml.safe_load(path.read_text())
        for key in ("background_zh_cn", "process_zh_cn", "impact_zh_cn"):
            if existing.get(key):
                print(f"SKIP {rel}: already has {key}")
                return 1
        appended = yaml.safe_dump(block, allow_unicode=True, sort_keys=False,
                                  default_flow_style=False, width=10**6)
        with path.open("a", encoding="utf-8") as stream:
            stream.write("\n" + appended)
        applied += 1
        print(f"appended {rel}")
    closed = close_last_pending()
    print(f"total appended: {applied} | pending closed: {closed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
