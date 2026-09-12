"""Major Batch 01 · Cluster F：东汉（7 事件）。"""
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
        "review_note": f"major01-F：{work}源引文：「{quote}」；claim_field={field}；anchor=段落精确锚。{note}"}

HS = "后汉书"
BLOCKS = {
 "qin_han/event-guangwu-tongyi.yml": {
  "background_zh_cn": "赤眉杀更始，而隗嚣据陇右、卢芳起安定——更始既亡，天下复归割据。",
  "process_zh_cn": "光武以推心置腹收降铜马之众：「降者犹不自安，光武知其意，敕令各归营勒兵，乃自乘轻骑按行部陈」——降者更相语曰「萧王推赤心置人腹中，安得不投死乎」，由是皆服。",
  "result_zh_cn": "王元降、陇右瓦解——光武次第削平群雄，至建武十二年巴蜀平定，天下复归一统。",
  "impact_zh_cn": "由是皆服：光武以恩信收众、以柔道治国，东汉立国之势自此定，洛阳中兴之局与西汉迥异。",
  "people": [
   {"person_name_raw": "刘秀", "role": "monarch", "link_status": "needs_linking",
    "role_zh_cn": "光武帝：统一战争主导者", "review_note": "major01-F：后汉书·光武帝纪「自乘轻骑按行部陈」", "person_id": None},
   {"person_name_raw": "隗嚣", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "陇右割据者：据陇右抗汉", "review_note": "major01-F：后汉书·光武帝纪「隗嚣据陇右」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "陇右", "role": "region", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "隗嚣割据之地，统一战争最后战场之一", "review_note": "major01-F：后汉书·光武帝纪「隗嚣据陇右」"},
  ],
  "evidence": [
   ev(HS, "光武帝纪", "本纪/光武帝纪上#p191", "text-niutrans-360299c5b3e9837b713e", "background", "primary", "赤眉杀更始，而隗嚣据陇右，卢芳起安定。"),
   ev(HS, "光武帝纪", "本纪/光武帝纪上#p122", "text-niutrans-728aaa4573695eb4c88c", "process", "primary", "降者犹不自安，光武知其意，敕令各归营勒兵，乃自乘轻骑按行部陈。"),
   ev(HS, "光武帝纪", "本纪/光武帝纪上#p123", "text-niutrans-fe3d6cf8d8ca8d699741", "process", "supporting", "萧王推赤心置人腹中，安得不投死乎！ 由是皆服。"),
   ev(HS, "光武帝纪", "本纪/光武帝纪下#p107", "text-niutrans-2cbea56a50585e75dbbb", "result", "primary", "王元降。"),
   ev(HS, "光武帝纪", "本纪/光武帝纪上#p123", "text-niutrans-fe3d6cf8d8ca8d699741", "impact", "primary", "由是皆服。", "恩信收众，东汉立国之基"),
  ],
 },
 "qin_han/event-guangwu-dutian.yml": {
  "background_zh_cn": "「是时，天下垦田多不以实，又户口年纪互有增减」——豪强隐匿田产人口，国家赋役失据。",
  "process_zh_cn": "诏下州郡检核垦田顷亩及户口年纪，又考实二千石长吏阿枉不平者——度田之政全国推行。",
  "result_zh_cn": "秋九月，河南尹张伋及诸郡守十余人，坐度田不实，皆下狱死——严法整肃。",
  "impact_zh_cn": "度田以严法核实编户：「在职五岁，户口增倍」——东汉国家户籍与赋役基础由此奠定，为明章之治的前提。",
  "people": [
   {"person_name_raw": "刘秀", "role": "monarch", "link_status": "needs_linking",
    "role_zh_cn": "光武帝：下度田之诏", "review_note": "major01-F：后汉书·光武帝纪「诏下州郡检核垦田顷亩及户口年纪」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "洛阳", "role": "capital", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "度田诏令所出", "review_note": "major01-F：后汉书·光武帝纪下（度田诏）"},
  ],
  "evidence": [
   ev(HS, "朱景王杜马刘傅坚马列", "传/朱景王杜马刘傅坚马列#p154", "text-niutrans-9924dc3eb70317e3501b", "background", "primary", "是时，天下垦田多不以实，又户口年纪互有增减。"),
   ev(HS, "光武帝纪", "本纪/光武帝纪下#p186", "text-niutrans-d722e3d75d76a2cbb48f", "process", "primary", "诏下州郡检核垦田顷亩及户口年纪，又考实二千石长吏阿枉不平者。"),
   ev(HS, "光武帝纪", "本纪/光武帝纪下#p194", "text-niutrans-a4a7a7927c162648a59e", "result", "primary", "秋九月，河南尹张伋及诸郡守十余人，坐度田不实，皆下狱死。"),
   ev(HS, "郭杜孔张廉王苏羊贾陆", "传/郭杜孔张廉王苏羊贾陆#p15", "text-niutrans-65bba91ad005b03de6b1", "impact", "primary", "在职五岁，户口增倍。"),
  ],
 },
 "qin_han/event-hanmingdi-jiwei.yml": {
  "background_zh_cn": "中元二年二月戊戌，光武帝崩于南宫前殿，年六十二——东汉开国之君既没，储君继统。",
  "process_zh_cn": "中元二年二月戊戌，太子即皇帝位，年三十——是为汉明帝。",
  "result_zh_cn": "「是岁，天下安平，人无徭役，岁比登稔，百姓殷富，粟斛三十，牛羊被野」——明帝之世仓廪充实。",
  "impact_zh_cn": "史论明帝「善刑理，法令分明，日晏坐朝，幽枉必达」——明章之治以明帝严明之政开局，东汉进入全盛。",
  "people": [
   {"person_name_raw": "汉明帝", "role": "monarch", "link_status": "needs_linking",
    "role_zh_cn": "太子刘庄：即皇帝位", "review_note": "major01-F：后汉书·显宗孝明帝纪「即皇帝位，年三十」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "洛阳", "role": "capital", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "东汉国都：光武崩、明帝即位之地", "review_note": "major01-F：后汉书·光武帝纪「帝崩于南宫前殿」"},
  ],
  "evidence": [
   ev(HS, "光武帝纪", "本纪/光武帝纪下#p401", "text-niutrans-74b632810d22aea22cac", "background", "primary", "二月戊戌，帝崩于南宫前殿，年六十二。"),
   ev(HS, "显宗孝明帝纪", "本纪/显宗孝明帝纪#p5", "text-niutrans-e132e34dc9aed4bcada9", "process", "primary", "中元二年二月戊戌，即皇帝位，年三十。"),
   ev(HS, "显宗孝明帝纪", "本纪/显宗孝明帝纪#p192", "text-niutrans-923077aff079b6d6501a", "result", "primary", "是岁，天下安平，人无徭役，岁比登稔，百姓殷富，粟斛三十，牛羊被野。"),
   ev(HS, "显宗孝明帝纪", "本纪/显宗孝明帝纪#p284", "text-niutrans-5cf5c2e2e0ff5dd38401", "impact", "primary", "明帝善刑理，法令分明。日晏坐朝，幽枉必达。"),
  ],
 },
 "qin_han/event-banchao-jingying-xiyu.yml": {
  "background_zh_cn": "先是，公卿多以为宜闭玉门关、遂弃西域——西域去留之议起于朝堂。",
  "process_zh_cn": "班超定计袭鄯善：「不入虎穴，不得虎子」「灭此虏，则鄯善破胆，功成事立矣」——夜袭匈奴使，鄯善纳质归汉。",
  "result_zh_cn": "「于是西域五十余国悉皆纳质内属焉」——班超经营三十一年，西域复通。",
  "impact_zh_cn": "班超经营之策「兵可不费中国而粮食自足」——以西域之财养西域之兵，都护体制延续，丝路再通。",
  "people": [
   {"person_name_raw": "班超", "role": "official", "link_status": "needs_linking",
    "role_zh_cn": "西域都护：经营西域三十一年", "review_note": "major01-F：后汉书·班梁列传「不入虎穴，不得虎子」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "鄯善", "role": "region", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "班超首功之地（夜袭匈奴使）", "review_note": "major01-F：后汉书·班梁列传「如令鄯善收吾属送匈奴」"},
   {"place_name_raw": "西域", "role": "region", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "五十余国纳质内属之地", "review_note": "major01-F：后汉书·班梁列传「西域五十余国悉皆纳质内属焉」"},
  ],
  "evidence": [
   ev(HS, "班梁列传", "传/班梁列传#p241", "text-niutrans-9339cc0fa5bae85ed692", "background", "primary", "先是，公卿多以为宜闭玉门关，遂弃西域。"),
   ev(HS, "班梁列传", "传/班梁列传#p27", "text-niutrans-de48b88e1f2e4d76b99b", "process", "primary", "超曰： 不入虎穴，不得虎子。"),
   ev(HS, "班梁列传", "传/班梁列传#p29", "text-niutrans-5ea85e8674f3493b399c", "process", "supporting", "灭此虏，则鄯善破胆，功成事立矣。"),
   ev(HS, "班梁列传", "传/班梁列传#p171", "text-niutrans-093f28eb6167c9a80a1b", "result", "primary", "于是西域五十余国悉皆纳质内属焉。"),
   ev(HS, "班梁列传", "传/班梁列传#p89", "text-niutrans-7b1df539e4a35800fbb3", "impact", "primary", "兵可不费中国而粮食自足。"),
  ],
 },
 "qin_han/event-dougu-beixiong.yml": {
  "background_zh_cn": "五年冬，北匈奴六七千骑入于五原塞、遂寇云中，南单于击却之——北边未靖。",
  "process_zh_cn": "窦宪「惶恐，白太后求出击北匈奴以赎罪」——以赎罪之身统军北伐；九月，以车骑将军窦宪为大将军。",
  "result_zh_cn": "窦宪遂登燕然山，刻石勒功而还——燕然勒石，北匈奴远遁。",
  "impact_zh_cn": "诏曰「北狄破灭，名王仍降，西域诸国，纳质内附」——北匈奴破灭使东汉北疆与西域局面一新，然窦宪专权亦自此坐大（后果为「潜图弑逆」）。",
  "people": [
   {"person_name_raw": "窦宪", "role": "official", "link_status": "needs_linking",
    "role_zh_cn": "车骑将军→大将军：北伐北匈奴、燕然勒石", "review_note": "major01-F：后汉书·孝和孝殇帝纪「窦宪遂登燕然山，刻石勒功而还」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "燕然山", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "窦宪刻石勒功之地", "review_note": "major01-F：后汉书·孝和孝殇帝纪「登燕然山，刻石勒功」"},
  ],
  "evidence": [
   ev(HS, "南匈奴列传", "传/南匈奴列传#p123", "text-niutrans-177fcf45606531febf2d", "background", "primary", "五年冬，北匈奴六七千骑入于五原塞，遂寇云中，至原阳。"),
   ev(HS, "袁张韩周列传", "传/袁张韩周列传#p176", "text-niutrans-9f3b0b803856d92d95fc", "process", "primary", "宪惶恐，白太后求出击北匈奴以赎罪。"),
   ev(HS, "孝和孝殇帝纪", "本纪/孝和孝殇帝纪#p36", "text-niutrans-3f5fc1596a5fc1dd6dd5", "result", "primary", "窦宪遂登燕然山，刻石勒功而还。"),
   ev(HS, "孝和孝殇帝纪", "本纪/孝和孝殇帝纪#p68", "text-niutrans-d3bad7c7fa329276c959", "impact", "primary", "诏曰： 北狄破灭，名王仍降，西域诸国，纳质内附。"),
  ],
 },
 "qin_han/event-danggu-1.yml": {
  "background_zh_cn": "「时，河内张成善说风角，推占当赦，遂教子杀人」——张成案牵出党人之狱。",
  "process_zh_cn": "「于是天子震怒，班下郡国，逮捕党人，布告天下，使同忿疾，遂收执膺等」——李膺等二百余人下狱。",
  "result_zh_cn": "明年，尚书霍谞、城门校尉窦武并表为请，帝意稍解，「乃皆赦归田里，禁锢终身」——第一次党锢。",
  "impact_zh_cn": "「党锢久积，人情多怨」——士大夫与宦官的对立自此不可解，党锢成为汉末政治崩坏与黄巾之乱的远因。",
  "people": [
   {"person_name_raw": "李膺", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "司隶校尉：党人领袖，下狱", "review_note": "major01-F：后汉书·党锢列传「遂收执膺等」", "person_id": None},
   {"person_name_raw": "窦武", "role": "supporter", "link_status": "needs_linking",
    "role_zh_cn": "城门校尉：表请解党人之狱", "review_note": "major01-F：后汉书·党锢列传「城门校尉窦武并表为请」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "洛阳", "role": "capital", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "党人之狱所在（汉廷）", "review_note": "major01-F：后汉书·党锢列传（逮捕党人）"},
  ],
  "evidence": [
   ev(HS, "党锢列传", "传/党锢列传#p28", "text-niutrans-851f16c697fd26939ac5", "background", "primary", "时，河内张成善说风角，推占当赦，遂教子杀人。"),
   ev(HS, "党锢列传", "传/党锢列传#p32", "text-niutrans-79c3e95f5702744c7352", "process", "primary", "于是天子震怒，班下郡国，逮捕党人……遂收执膺等。"),
   ev(HS, "党锢列传", "传/党锢列传#p35", "text-niutrans-bb63f8c67b986c2f1cf8", "result", "primary", "乃皆赦归田里，禁锢终身。"),
   ev(HS, "党锢列传", "传/党锢列传#p60", "text-niutrans-beb970a229906b163827", "impact", "primary", "中平元年，黄巾贼起，中常侍吕强言于帝曰： 党锢久积，人情多怨。"),
  ],
 },
 "qin_han/event-danggu-2.yml": {
  "background_zh_cn": "「张俭乡人朱并，承望中常侍侯览意旨，上书告俭与同乡二十四人别相署号，共为部党，图危社稷」——第二次党锢之导火索。",
  "process_zh_cn": "大长秋曹节讽有司奏捕前党：「故司空虞放、太仆杜密、长乐少府李膺……等百余人，皆死狱中」。",
  "result_zh_cn": "锢及五族：「而今党人锢及五族，既乖典训之文，有谬经常之法」——党锢之酷至此极。",
  "impact_zh_cn": "光和二年上禄长和海之言终获采纳，「党锢自从祖以下，皆得解释」——党锢虽解而汉室元气已伤，士人离心。",
  "people": [
   {"person_name_raw": "曹节", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "中常侍：讽有司奏捕前党", "review_note": "major01-F：后汉书·党锢列传「大长秋曹节因此讽有司奏捕前党」", "person_id": None},
   {"person_name_raw": "侯览", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "中常侍：纵乡人告发张俭", "review_note": "major01-F：后汉书·党锢列传「承望中常侍侯览意旨」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "洛阳", "role": "capital", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "第二次党锢发端与行刑所在", "review_note": "major01-F：后汉书·党锢列传（皆死狱中）"},
  ],
  "evidence": [
   ev(HS, "党锢列传", "传/党锢列传#p47", "text-niutrans-858df02fe1de9d0a8796", "background", "primary", "张俭乡人朱，承望中常侍侯览意旨，上书告俭与同乡二十四人别相署号，共为部党，图危社稷。"),
   ev(HS, "党锢列传", "传/党锢列传#p50", "text-niutrans-8cdb207c67ab9228c934", "process", "primary", "大长秋曹节因此讽有司奏捕前党……皆死狱中。"),
   ev(HS, "党锢列传", "传/党锢列传#p58", "text-niutrans-4e526b66748c9b4a8d64", "result", "primary", "而今党人锢及五族，既乖典训之文，有谬经常之法。"),
   ev(HS, "党锢列传", "传/党锢列传#p59", "text-niutrans-5d2468e23c10f1e395bd", "impact", "primary", "帝览而悟之，党锢自从祖以下，皆得解释。"),
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
