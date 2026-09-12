"""Major Batch 01 · Cluster B：秦帝国（9 事件）。"""
from __future__ import annotations
import sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
EVENTS = ROOT / "data" / "curated" / "history_backbone" / "events"

def ev(work, term, anchor, tid, field, role, quote, note=""):
    return {"work": work, "term": term, "historical_text_id": tid, "chapter_anchor": anchor,
        "claim_field": field, "evidence_role": role, "link_status": "linked",
        "link_method": "manual", "link_confidence": 1.0, "link_quality_status": "reviewed",
        "context_keywords": [],
        "review_note": f"major01-B：{work}源引文：「{quote}」；claim_field={field}；anchor=段落精确锚。{note}"}

SJ = "史记"
BLOCKS = {
 "qin_han/event-qin-junxian.yml": {
  "background_zh_cn": "秦初并天下，丞相绾等言「诸侯初破，燕、齐、荆地远，不为置王，毋以填之。请立诸子」——封建与郡县之议起于朝堂。",
  "process_zh_cn": "廷尉李斯议曰：「周文武所封子弟同姓甚众，然后属疏远，相攻击如仇雠，诸侯更相诛伐，周天子弗能禁止」——力主罢封建、置郡县。",
  "result_zh_cn": "李斯之议获纳：「今海内赖陛下神灵一统，皆为郡县，诸子功臣以公赋税重赏赐之，甚足易制」——郡县制遂行于天下。",
  "impact_zh_cn": "分天下以为三十六郡，郡置守、尉、监——郡县官僚制取代世卿封建，为此后两千年中央集权体制之模板。",
  "people": [
   {"person_name_raw": "李斯", "role": "official", "link_status": "needs_linking",
    "role_zh_cn": "廷尉：议罢封建、行郡县", "review_note": "major01-B：史记·秦始皇本纪「廷尉李斯议曰」", "person_id": None},
   {"person_name_raw": "秦始皇", "role": "monarch", "link_status": "needs_linking",
    "role_zh_cn": "纳李斯议、行郡县", "review_note": "major01-B：史记·秦始皇本纪（分天下三十六郡）", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "咸阳", "role": "capital", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "议封建郡县、颁行郡县制之都", "review_note": "major01-B：史记·秦始皇本纪（始皇二十六年廷议）"},
  ],
  "evidence": [
   ev(SJ, "秦始皇本纪", "十二本纪/秦始皇本纪#p164", "text-niutrans-bec95df3b66785519156", "background", "primary", "请立诸子，唯上幸许。"),
   ev(SJ, "秦始皇本纪", "十二本纪/秦始皇本纪#p166", "text-niutrans-ee23ca1aa3256b82f60b", "process", "primary", "廷尉李斯议曰： 周文武所封子弟同姓甚众，然后属疏远，相攻击如仇雠。"),
   ev(SJ, "秦始皇本纪", "十二本纪/秦始皇本纪#p167", "text-niutrans-f5cbece9845908d6d43b", "result", "primary", "今海内赖陛下神灵一统，皆为郡县，诸子功臣以公赋税重赏赐之，甚足易制。"),
   ev(SJ, "秦始皇本纪", "十二本纪/秦始皇本纪#p172", "text-niutrans-fe665881879c068407e2", "impact", "primary", "分天下以为三十六郡，郡置守、尉、监。"),
  ],
 },
 "qin_han/event-qin-shutongwen.yml": {
  "background_zh_cn": "秦并天下、分三十六郡，六国异文异制并存的局面亟待统一。",
  "process_zh_cn": "书同文字——以秦文为准统一天下文字。",
  "result_zh_cn": "刻石纪功之语曰「器械一量，同书文字」——文字统一列为秦制成就昭示天下。",
  "impact_zh_cn": "车同轨、书同文并举，文字与交通规制统一——中华文化共同体之基自此奠定。",
  "people": [
   {"person_name_raw": "李斯", "role": "official", "link_status": "needs_linking",
    "role_zh_cn": "丞相：主持同文字", "review_note": "major01-B：史记·秦始皇本纪「同书文字」（李斯等奏刻石）", "person_id": None},
  ],
  "places": [],
  "evidence": [
   ev(SJ, "秦始皇本纪", "十二本纪/秦始皇本纪#p172", "text-niutrans-fe665881879c068407e2", "background", "primary", "分天下以为三十六郡，郡置守、尉、监。"),
   ev(SJ, "秦始皇本纪", "十二本纪/秦始皇本纪#p178", "text-niutrans-b7610d62e29cf31d5654", "process", "primary", "书同文字。"),
   ev(SJ, "秦始皇本纪", "十二本纪/秦始皇本纪#p219", "text-niutrans-e6e89e509c0483388d37", "result", "primary", "器械一量，同书文字。"),
   ev(SJ, "秦始皇本纪", "十二本纪/秦始皇本纪#p177", "text-niutrans-1f1a13608730ab20d41c", "impact", "primary", "车同轨。"),
  ],
 },
 "qin_han/event-qin-tongyi-duliangheng.yml": {
  "background_zh_cn": "秦并天下、置郡县，六国度量衡各异，赋税、工程与贸易皆需一制。",
  "process_zh_cn": "一法度衡石丈尺——以秦制为准统一度、量、衡。",
  "result_zh_cn": "刻石曰「器械一量」——器物规格与度量随之划一，制度统一见诸铭文。",
  "impact_zh_cn": "车同轨与度量衡统一并行——全国经济与行政运行有了统一尺度，秦制为后世所承。",
  "places": [],
  "evidence": [
   ev(SJ, "秦始皇本纪", "十二本纪/秦始皇本纪#p172", "text-niutrans-fe665881879c068407e2", "background", "primary", "分天下以为三十六郡，郡置守、尉、监。"),
   ev(SJ, "秦始皇本纪", "十二本纪/秦始皇本纪#p176", "text-niutrans-215d0ddac58fddb0aad0", "process", "primary", "一法度衡石丈尺。"),
   ev(SJ, "秦始皇本纪", "十二本纪/秦始皇本纪#p219", "text-niutrans-e6e89e509c0483388d37", "result", "primary", "器械一量，同书文字。"),
   ev(SJ, "秦始皇本纪", "十二本纪/秦始皇本纪#p177", "text-niutrans-1f1a13608730ab20d41c", "impact", "primary", "车同轨。"),
  ],
 },
 "qin_han/event-qin-xiu-changcheng.yml": {
  "background_zh_cn": "秦已并天下，乃使蒙恬将三十万众北逐戎狄、收河南——北疆既拓，修筑长城以固之。",
  "process_zh_cn": "筑长城，因地形、用制险塞，起临洮、至辽东，延袤万余里。",
  "result_zh_cn": "长城「起临洮属之辽东，城巉万馀里」，北边亭障相连。",
  "impact_zh_cn": "太史公亲行其地而论之：「行观蒙恬所为秦筑长城亭障，堑山堙谷，通直道，固轻百姓力矣」——长城之役功过并见史评。",
  "people": [
   {"person_name_raw": "蒙恬", "role": "official", "link_status": "needs_linking",
    "role_zh_cn": "秦将：主持筑长城、通直道", "review_note": "major01-B：史记·蒙恬列传「筑长城，因地形，用制险塞」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "临洮", "role": "frontier", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "长城西端起点", "review_note": "major01-B：史记·蒙恬列传「起临洮，至辽东」"},
   {"place_name_raw": "辽东", "role": "frontier", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "长城东端终点", "review_note": "major01-B：史记·蒙恬列传「起临洮，至辽东」"},
  ],
  "evidence": [
   ev(SJ, "蒙恬列传", "七十列传/蒙恬列传#p14", "text-niutrans-e8a1983f2b271f8b70cc", "background", "primary", "秦已并天下，乃使蒙恬将三十万众北逐戎狄，收河南。"),
   ev(SJ, "蒙恬列传", "七十列传/蒙恬列传#p15", "text-niutrans-3071c5b3370dc9e33b2c", "process", "primary", "筑长城，因地形，用制险塞，起临洮，至辽东，延袤万馀里。"),
   ev(SJ, "蒙恬列传", "七十列传/蒙恬列传#p85", "text-niutrans-1660dc27d6d4da05e136", "result", "primary", "起临洮属之辽东，城巉万馀里。"),
   ev(SJ, "蒙恬列传", "七十列传/蒙恬列传#p88", "text-niutrans-b5986dff7eb531a6b9a8", "impact", "primary", "行观蒙恬所为秦筑长城亭障，堑山堙谷，通直道，固轻百姓力矣。"),
  ],
 },
 "qin_han/event-qin-beiji-xiongnu.yml": {
  "background_zh_cn": "秦已并天下，北边匈奴为患，乃以蒙恬统大军北征。",
  "process_zh_cn": "乃使蒙恬将三十万众北逐戎狄，收河南——河套之地尽入秦疆。",
  "result_zh_cn": "是时蒙恬威振匈奴——匈奴远遁，北边暂安。",
  "impact_zh_cn": "蒙恬暴师于外十余年、居上郡，秦以重兵长戍北边；筑长城、通直道皆自此役始。",
  "people": [
   {"person_name_raw": "蒙恬", "role": "official", "link_status": "needs_linking",
    "role_zh_cn": "秦将：将三十万众北逐匈奴", "review_note": "major01-B：史记·蒙恬列传「将三十万众北逐戎狄，收河南」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "河南", "role": "region", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "河套以南地：蒙恬收复", "review_note": "major01-B：史记·蒙恬列传「收河南」"},
   {"place_name_raw": "上郡", "role": "frontier", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "蒙恬长驻之所", "review_note": "major01-B：史记·蒙恬列传「暴师於外十馀年，居上郡」"},
  ],
  "evidence": [
   ev(SJ, "蒙恬列传", "七十列传/蒙恬列传#p14", "text-niutrans-e8a1983f2b271f8b70cc", "background", "primary", "秦已并天下，乃使蒙恬将三十万众北逐戎狄，收河南。"),
   ev(SJ, "蒙恬列传", "七十列传/蒙恬列传#p14", "text-niutrans-e8a1983f2b271f8b70cc", "process", "primary", "将三十万众北逐戎狄，收河南。"),
   ev(SJ, "蒙恬列传", "七十列传/蒙恬列传#p18", "text-niutrans-ca1e960f83127bedda9b", "result", "primary", "是时蒙恬威振匈奴。"),
   ev(SJ, "蒙恬列传", "七十列传/蒙恬列传#p17", "text-niutrans-de6d8edfd06856749ebb", "impact", "primary", "暴师於外十馀年，居上郡。"),
  ],
 },
 "qin_han/event-qin-nanzheng-baiyue.yml": {
  "background_zh_cn": "又使尉屠睢将楼船之士南攻百越，使监禄凿渠运粮——秦以楼船水师与粮道工程南征。",
  "process_zh_cn": "深入越，越人遁逃——秦军深入岭南。",
  "result_zh_cn": "三十三年，发诸尝逋亡人、赘婿、贾人略取陆梁地，为桂林、象郡、南海，以适遣戍——岭南置三郡。",
  "impact_zh_cn": "秦置三郡、以谪戍实边，岭南自此入于中国版图；其后赵佗据之，南越国由是而立。",
  "people": [
   {"person_name_raw": "屠睢", "role": "official", "link_status": "needs_linking",
    "role_zh_cn": "秦尉：将楼船之士南攻百越", "review_note": "major01-B：史记·平津侯主父列传「使尉屠睢将楼船之士南攻百越」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "桂林", "role": "region", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "秦置三郡之一", "review_note": "major01-B：史记·秦始皇本纪「为桂林、象郡、南海」"},
   {"place_name_raw": "象郡", "role": "region", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "秦置三郡之一", "review_note": "major01-B：史记·秦始皇本纪「为桂林、象郡、南海」"},
   {"place_name_raw": "南海", "role": "region", "link_status": "needs_linking", "sequence": 3,
    "description_zh_cn": "秦置三郡之一", "review_note": "major01-B：史记·秦始皇本纪「为桂林、象郡、南海」"},
  ],
  "evidence": [
   ev(SJ, "平津侯主父列传", "七十列传/平津侯主父列传#p161", "text-niutrans-2c804bef535057c54ce4", "background", "primary", "又使尉屠睢将楼船之士南攻百越，使监禄凿渠运粮。"),
   ev(SJ, "平津侯主父列传", "七十列传/平津侯主父列传#p161", "text-niutrans-2c804bef535057c54ce4", "process", "primary", "深入越，越人遁逃。"),
   ev(SJ, "秦始皇本纪", "十二本纪/秦始皇本纪#p316", "text-niutrans-f5e2cd1a3b2c6435f85d", "result", "primary", "略取陆梁地，为桂林、象郡、南海，以适遣戍。"),
   ev(SJ, "南越列传", "七十列传/南越列传#p20", "text-niutrans-a9f319637ba4486db87c", "impact", "primary", "佗因此以兵威边，财物赂遗闽越、西瓯、骆，役属焉，东西万馀里。"),
  ],
 },
 "qin_han/event-qin-shihuang-beng.yml": {
  "background_zh_cn": "始皇东巡，至平原津而病。",
  "process_zh_cn": "七月丙寅，始皇崩于沙丘平台。",
  "result_zh_cn": "丞相李斯「为上崩在外，恐诸公子及天下有变，乃秘之，不发丧」——沙丘秘丧。",
  "impact_zh_cn": "太子胡亥袭位为二世皇帝——始皇之死与继统之变，为秦末乱局之始。",
  "people": [
   {"person_name_raw": "秦始皇", "role": "monarch", "link_status": "needs_linking",
    "role_zh_cn": "东巡途中崩于沙丘平台", "review_note": "major01-B：史记·秦始皇本纪「七月丙寅，始皇崩於沙丘平台」", "person_id": None},
   {"person_name_raw": "李斯", "role": "official", "link_status": "needs_linking",
    "role_zh_cn": "丞相：主持秘不发丧", "review_note": "major01-B：史记·秦始皇本纪「乃祕之，不发丧」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "沙丘平台", "role": "location", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "始皇崩逝之地", "review_note": "major01-B：史记·秦始皇本纪「崩於沙丘平台」"},
  ],
  "evidence": [
   ev(SJ, "秦始皇本纪", "十二本纪/秦始皇本纪#p459", "text-niutrans-6c7e895d8c7d9907924e", "background", "primary", "至平原津而病。"),
   ev(SJ, "秦始皇本纪", "十二本纪/秦始皇本纪#p463", "text-niutrans-5e8b822db4b8dc3c0ccf", "process", "primary", "七月丙寅，始皇崩於沙丘平台。"),
   ev(SJ, "秦始皇本纪", "十二本纪/秦始皇本纪#p464", "text-niutrans-27cc2f54cb17e3830406", "result", "primary", "丞相斯为上崩在外，恐诸公子及天下有变，乃祕之，不发丧。"),
   ev(SJ, "秦始皇本纪", "十二本纪/秦始皇本纪#p475", "text-niutrans-7b066c589c365477a8a5", "impact", "primary", "太子胡亥袭位，为二世皇帝。"),
  ],
 },
 "qin_han/event-shaqiu-zhengbian.yml": {
  "background_zh_cn": "七月丙寅，始皇崩于沙丘平台——主上崩于巡狩途中，遗诏未定。",
  "process_zh_cn": "赵高故尝教胡亥书及狱律令法事、胡亥私幸之——赵高居中用事，与李斯合谋。",
  "result_zh_cn": "「更为书赐公子扶苏、蒙恬，数以罪，赐死」——矫诏立胡亥、诛杀长兄与边将。",
  "impact_zh_cn": "太子胡亥袭位为二世皇帝——沙丘之变以阴谋易嗣，秦政自此崩坏，天下随之瓦解。",
  "people": [
   {"person_name_raw": "赵高", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "中车府令：沙丘政变主谋", "review_note": "major01-B：史记·秦始皇本纪「赵高故尝教胡亥书及狱律令法事」", "person_id": None},
   {"person_name_raw": "秦二世", "role": "monarch", "link_status": "needs_linking",
    "role_zh_cn": "胡亥：矫诏袭位为二世皇帝", "review_note": "major01-B：史记·秦始皇本纪「太子胡亥袭位，为二世皇帝」", "person_id": None},
   {"person_name_raw": "扶苏", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "公子：矫诏赐死", "review_note": "major01-B：史记·秦始皇本纪「赐公子扶苏、蒙恬……赐死」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "沙丘平台", "role": "location", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "政变发生之地", "review_note": "major01-B：史记·秦始皇本纪（崩于沙丘、秘不发丧）"},
  ],
  "evidence": [
   ev(SJ, "秦始皇本纪", "十二本纪/秦始皇本纪#p463", "text-niutrans-5e8b822db4b8dc3c0ccf", "background", "primary", "七月丙寅，始皇崩於沙丘平台。"),
   ev(SJ, "秦始皇本纪", "十二本纪/秦始皇本纪#p468", "text-niutrans-31322c1592c434ee87c4", "process", "primary", "赵高故尝教胡亥书及狱律令法事，胡亥私幸之。"),
   ev(SJ, "秦始皇本纪", "十二本纪/秦始皇本纪#p470", "text-niutrans-c5f0aa03198abc5aec0b", "result", "primary", "更为书赐公子扶苏、蒙恬，数以罪，赐死。"),
   ev(SJ, "秦始皇本纪", "十二本纪/秦始皇本纪#p475", "text-niutrans-7b066c589c365477a8a5", "impact", "primary", "太子胡亥袭位，为二世皇帝。"),
  ],
 },
 "qin_han/event-chensheng-wuguang-qiyi.yml": {
  "background_zh_cn": "二世元年七月，发闾左適戍渔阳，九百人屯大泽乡——戍卒失期当斩，死地求生。",
  "process_zh_cn": "陈胜、吴广乃谋曰「今亡亦死，举大计亦死，等死，死国可乎」——斩木揭竿而起。",
  "result_zh_cn": "陈胜自立为将军、吴广为都尉；攻大泽乡，收而攻蕲——义军旬月间攻城略地。",
  "impact_zh_cn": "贾谊论之曰「斩木为兵，揭竿为旗，天下云集响应……山东豪俊遂并起而亡秦族矣」——大泽乡首义成为亡秦战争的起点。",
  "people": [
   {"person_name_raw": "陈胜", "role": "monarch", "link_status": "needs_linking",
    "role_zh_cn": "起义领袖：自立为将军", "review_note": "major01-B：史记·陈涉世家「陈胜自立为将军」", "person_id": None},
   {"person_name_raw": "吴广", "role": "supporter", "link_status": "needs_linking",
    "role_zh_cn": "起义共同发动者：为都尉", "review_note": "major01-B：史记·陈涉世家「吴广为都尉」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "大泽乡", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "起义爆发地", "review_note": "major01-B：史记·陈涉世家「九百人屯大泽乡」「攻大泽乡」"},
   {"place_name_raw": "蕲", "role": "battlesite", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "义军首攻之地", "review_note": "major01-B：史记·陈涉世家「收而攻蕲」"},
  ],
  "evidence": [
   ev(SJ, "陈涉世家", "三十世家/陈涉世家#p6", "text-niutrans-5aa9250c0b49bcca7916", "background", "primary", "二世元年七月，发闾左適戍渔阳，九百人屯大泽乡。"),
   ev(SJ, "陈涉世家", "三十世家/陈涉世家#p10", "text-niutrans-20d32ac4b5357eb94f28", "process", "primary", "陈胜、吴广乃谋曰： 今亡亦死，举大计亦死，等死，死国可乎？"),
   ev(SJ, "陈涉世家", "三十世家/陈涉世家#p37", "text-niutrans-e6d0ae7c0a84cdbb15ad", "result", "primary", "陈胜自立为将军，吴广为都尉。"),
   ev(SJ, "陈涉世家", "三十世家/陈涉世家#p38", "text-niutrans-2db8a87f67f569eb2f72", "result", "supporting", "攻大泽乡，收而攻蕲。"),
   ev(SJ, "陈涉世家", "三十世家/陈涉世家#p173", "text-niutrans-e9d0a16e1ab4a73f2a08", "impact", "primary", "斩木为兵，揭竿为旗，天下云集响应，赢粮而景从，山东豪俊遂并起而亡秦族矣。"),
  ],
 },
}

def main() -> int:
    applied = 0
    for rel, block in BLOCKS.items():
        path = EVENTS / rel
        if not path.exists():
            print(f"MISSING {rel}"); continue
        if yaml.safe_load(path.read_text()).get("process_zh_cn"):
            print(f"SKIP {rel}"); continue
        with path.open("a", encoding="utf-8") as s:
            s.write("\n" + yaml.safe_dump(block, allow_unicode=True, sort_keys=False, default_flow_style=False, width=10**6))
        applied += 1
        print(f"appended {rel}")
    print(f"total: {applied}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
