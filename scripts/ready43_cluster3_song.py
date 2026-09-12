"""Ready-43 · Cluster 3：宋辽金 5 事件（陈桥兵变/金建国/靖康之变/南宋建国/崖山海战）。"""
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
        "review_note": f"ready43-c3：{work}源引文：「{quote}」；claim_field={field}；anchor=段落精确锚。{note}"}

BLOCKS = {
 "song_liao_xia_jin/event-chenqiao-bingbian.yml": {
  "background_zh_cn": "大军次陈桥驿，军中知星者苗训引门吏视「日下复有一日，黑光摩荡者久之」——兵变前夜的天象造势。",
  "process_zh_cn": "诸校露刃列于庭，曰「诸军无主，愿策太尉为天子」；未及对，有以黄衣加太祖身，众皆罗拜、呼万岁，即掖太祖乘马。",
  "result_zh_cn": "翰林承旨陶谷出周恭帝禅位制书于袖中，宣徽使引太祖就庭北面拜受，乃掖太祖升崇元殿、服衮冕，即皇帝位。",
  "impact_zh_cn": "建隆元年春正月乙巳，大赦、改元，「定有天下之号曰宋」——兵不血刃而周宋易代，五代武人拥立之局以宋朝建立收束。",
  "people": [
   {"person_name_raw": "赵匡胤", "role": "monarch", "link_status": "needs_linking",
    "role_zh_cn": "殿前都点检→宋太祖：陈桥兵变、受禅建宋", "review_note": "ready43-c3：宋史·太祖纪「即皇帝位」「定有天下之号曰宋」", "person_id": None},
   {"person_name_raw": "陶谷", "role": "official", "link_status": "needs_linking",
    "role_zh_cn": "翰林承旨：出周恭帝禅位制书", "review_note": "ready43-c3：宋史·太祖纪「陶谷出周恭帝禅位制书于袖中」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "陈桥驿", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "兵变发生地（开封东北）", "review_note": "ready43-c3：宋史·太祖纪「次陈桥驿」"},
  ],
  "evidence": [
   ev("宋史", "太祖纪", "本纪/卷一#p58", "text-niutrans-d77239ac01d51edaffc5", "background", "primary",
      "次陈桥驿，军中知星者苗训引门吏楚昭辅视日下复有一日，黑光摩荡者久之。"),
   ev("宋史", "太祖纪", "本纪/卷一#p61", "text-niutrans-d9073d6ee9be627e6b3f", "process", "primary",
      "诸校露刃列于庭，曰： 诸军无主，愿策太尉为天子。"),
   ev("宋史", "太祖纪", "本纪/卷一#p62", "text-niutrans-1fabbb9e7e3a41c89ac7", "process", "supporting",
      "有以黄衣加太祖身，众皆罗拜，呼万岁。"),
   ev("宋史", "太祖纪", "本纪/卷一#p72", "text-niutrans-c56e75915a91f4f418f9", "result", "primary",
      "陶谷出周恭帝禅位制书于袖中……即皇帝位。"),
   ev("宋史", "太祖纪", "本纪/卷一#p74", "text-niutrans-79c4b77f6204a923d1fd", "impact", "primary",
      "建隆元年春正月乙巳，大赦，改元，定有天下之号曰宋。"),
  ],
 },
 "song_liao_xia_jin/event-jin-jianguo.yml": {
  "background_zh_cn": "太祖讳阿骨打，世祖第二子——完颜部首领承女真诸部之势崛起于按出虎水。",
  "process_zh_cn": "收国元年正月壬申朔，群臣奉上尊号；于是国号大金，改元收国。",
  "result_zh_cn": "金室既建，以猛安谋克之制整军经武，十年之间灭辽伐宋——「大金」国号行于天下。",
  "impact_zh_cn": "国号大金、改元收国——女真由部落联盟转为王朝国家，东北亚政治格局重组，辽宋先后受其冲击（宋人国书自此称「侄宋皇帝」奉「大金皇帝」）。",
  "people": [
   {"person_name_raw": "完颜阿骨打", "role": "monarch", "link_status": "needs_linking",
    "role_zh_cn": "金太祖：建号大金、改元收国", "review_note": "ready43-c3：金史·太祖纪「国号大金，改元收国」", "person_id": None},
  ],
  "places": [],
  "evidence": [
   ev("金史", "太祖纪", "本纪/卷二#p1", "text-niutrans-8670d5f04d6cf57c6412", "background", "primary",
      "太祖应乾兴运昭德定功仁明庄孝大圣武元皇帝，讳旻，本讳阿骨打，世祖第二子也。"),
   ev("金史", "太祖纪", "本纪/卷二#p182", "text-niutrans-7d1184a902337ce518c4", "process", "primary",
      "收国元年正月壬申朔，群臣奉上尊号。"),
   ev("金史", "太祖纪", "本纪/卷二#p187", "text-niutrans-84605f292739f3f1b4d7", "result", "primary",
      "于是国号大金，改元收国。"),
   ev("金史", "熙宗纪", "本纪/卷三#p171", "text-niutrans-6b53814740c4b7cc0654", "impact", "primary",
      "辛巳，宋上誓书、地图，称侄大宋皇帝、伯大金皇帝。", "金以国号临宋之证"),
  ],
 },
 "song_liao_xia_jin/event-jingkang-zhi-bian.yml": {
  "background_zh_cn": "乙未，金人入青城、攻朝阳门；括借金银、籍倡优家财以充犒军——汴京在围城与索金中耗尽。",
  "process_zh_cn": "秦元领保甲斩关遁，京城陷；金人以括金未足，杀户部尚书梅执礼、侍郎陈知质等。",
  "result_zh_cn": "丁卯，金人要上皇如青城；次年三月，帝在青城——徽钦二帝相继被胁入金营。",
  "impact_zh_cn": "二帝北狩、京城倾覆——北宋灭亡；五月庚寅朔，康王赵构登坛受命、即位于应天府，宋室南渡（改元建炎）。",
  "people": [
   {"person_name_raw": "宋钦宗", "role": "deposed_monarch", "link_status": "needs_linking",
    "role_zh_cn": "北宋末帝：在青城被胁北狩", "review_note": "ready43-c3：宋史·钦宗纪「帝在青城」", "person_id": None},
   {"person_name_raw": "宋徽宗", "role": "deposed_monarch", "link_status": "needs_linking",
    "role_zh_cn": "上皇：被金人要如青城", "review_note": "ready43-c3：宋史·钦宗纪「金人要上皇如青城」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "青城", "role": "location", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "汴京南郊斋宫，二帝被胁入金营处", "review_note": "ready43-c3：宋史·钦宗纪「金人要上皇如青城」"},
   {"place_name_raw": "汴京", "role": "capital", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "北宋都城：城陷、括金", "review_note": "ready43-c3：宋史·钦宗纪「京城陷」「括借金银」"},
  ],
  "evidence": [
   ev("宋史", "钦宗纪", "本纪/卷二十三#p346", "text-niutrans-9fbb8a153d1a1213db36", "background", "primary",
      "乙未，金人入青城，攻朝阳门。"),
   ev("宋史", "钦宗纪", "本纪/卷二十三#p379", "text-niutrans-38eb9032b6d3b0f3c2be", "process", "primary",
      "秦元领保甲斩关遁，京城陷。"),
   ev("宋史", "钦宗纪", "本纪/卷二十三#p425", "text-niutrans-9db07d5b6b66d6e5887b", "process", "supporting",
      "乙酉，金人以括金未足，杀户部尚书梅执礼。"),
   ev("宋史", "钦宗纪", "本纪/卷二十三#p420", "text-niutrans-8f6000535dacafef95ce", "result", "primary",
      "丁卯，金人要上皇如青城。"),
   ev("宋史", "钦宗纪", "本纪/卷二十三#p426", "text-niutrans-8c18b356a0f1f10a9292", "impact", "primary",
      "三月辛卯朔，帝在青城。"),
  ],
 },
 "song_liao_xia_jin/event-zhao-gou-nansong-jianguo.yml": {
  "background_zh_cn": "癸未，康王至应天府；济州父老诣军门请帝即位——靖康之后，宗室与军民推戴康王。",
  "process_zh_cn": "五月庚寅朔，帝登坛受命，礼毕恸哭，遥谢二帝，即位于府治。",
  "result_zh_cn": "改元建炎——南宋政权于应天府建立。",
  "impact_zh_cn": "建炎改元、以应天府为南京，宋室南渡而国祚延续——南宋一百五十年自此始，中原士民随之南迁（衣冠南渡再演）。",
  "people": [
   {"person_name_raw": "赵构", "role": "monarch", "link_status": "needs_linking",
    "role_zh_cn": "康王→宋高宗：应天府即位、南宋开国", "review_note": "ready43-c3：宋史·高宗纪「即位于府治」「改元建炎」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "应天府", "role": "capital", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "南宋开国即位之地（南京）", "review_note": "ready43-c3：宋史·高宗纪「至应天府」「即位于府治」"},
  ],
  "evidence": [
   ev("宋史", "高宗纪", "本纪/卷二十四#p94", "text-niutrans-ffc425e350961a7166af", "background", "primary",
      "癸未，至应天府。"),
   ev("宋史", "高宗纪", "本纪/卷二十四#p78", "text-niutrans-4836afc04bbac2f0d6fb", "background", "supporting",
      "戊辰，济州父老诣军门……请帝即位于济。"),
   ev("宋史", "高宗纪", "本纪/卷二十四#p99", "text-niutrans-2d256364aa1c250fff8e", "process", "primary",
      "五月庚寅朔，帝登坛受命，礼毕恸哭，遥谢二帝，即位于府治。"),
   ev("宋史", "高宗纪", "本纪/卷二十四#p100", "text-niutrans-0eafd0f70c92845fa99c", "result", "primary",
      "改元建炎。"),
   ev("宋史", "钦宗纪", "本纪/卷二十三#p426", "text-niutrans-8c18b356a0f1f10a9292", "impact", "supporting",
      "帝在青城。", "二帝未归而康王继统，南渡之局已成"),
  ],
 },
 "song_liao_xia_jin/event-yanya-haizhan.yml": {
  "background_zh_cn": "庚午，众又立卫王昺为主，以陆秀夫为左丞相；五月改元祥兴，帝昺徙居崖山——宋室最后据点定于海岛。",
  "process_zh_cn": "十六年正月壬戌，张弘范兵至崖山；张世杰来拒战，败之，世杰遁去。",
  "result_zh_cn": "广王昺偕其官属俱赴海死，元军获其金宝以献——南宋行朝覆灭。",
  "impact_zh_cn": "崖山既没，陆秀夫负帝蹈海、张世杰舟覆而亡——南宋彻底灭亡，元朝完成全国统一，中国首次全境为北方民族王朝所统。",
  "people": [
   {"person_name_raw": "陆秀夫", "role": "supporter", "link_status": "needs_linking",
    "role_zh_cn": "左丞相：崖山殉国", "review_note": "ready43-c3：宋史「以陆秀夫为左丞相」；元史「广王昺偕其官属俱赴海死」", "person_id": None},
   {"person_name_raw": "张世杰", "role": "supporter", "link_status": "needs_linking",
    "role_zh_cn": "宋军统帅：崖山拒战败走", "review_note": "ready43-c3：元史·世祖纪「张世杰来拒战，败之，世杰遁去」", "person_id": None},
   {"person_name_raw": "张弘范", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "元军统帅：兵至崖山破宋", "review_note": "ready43-c3：宋史「张弘范兵至崖山」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "崖山", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "宋末决战之地（广东新会海岛）", "review_note": "ready43-c3：宋史「昺徙居崖山」；元史「追宋二王至崖山寨」"},
  ],
  "evidence": [
   ev("宋史", "瀛国公纪", "本纪/卷四十七#p605", "text-niutrans-6afbca7bd0bfb5fb26da", "background", "primary",
      "庚午，众又立卫王昺为主，以陆秀夫为左丞相。"),
   ev("宋史", "瀛国公纪", "本纪/卷四十七#p607", "text-niutrans-53e8323e03810448effb", "background", "supporting",
      "五月癸未朔，改元祥兴。"),
   ev("宋史", "瀛国公纪", "本纪/卷四十七#p625", "text-niutrans-82c7b57f1e731c88fc7e", "process", "primary",
      "十六年正月壬戌，张弘范兵至崖山。"),
   ev("元史", "世祖纪", "本纪/卷十#p264", "text-niutrans-f1c299077a3a6fe09e21", "result", "primary",
      "张弘范将兵追宋二王至崖山寨，张世杰来拒战，败之，世杰遁去，广王昺偕其官属俱赴海死。"),
   ev("宋史", "瀛国公纪", "本纪/卷四十七#p612", "text-niutrans-ece427e67b5cba9de965", "impact", "supporting",
      "己未，昺徙居崖山，升广州为翔龙府。"),
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
