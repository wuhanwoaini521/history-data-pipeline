"""Major Batch 02 · Cluster J：春秋 4 事件（城濮之战/邲之战/柏举之战/管仲改革）。

SOURCE-BACKED FIRST：evidence 锚定左传（僖/宣/定/哀公）、史记（管晏列传/齐太公世家）、国语（齐语）。
"""
from __future__ import annotations
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
EVENTS = ROOT / "data" / "curated" / "history_backbone" / "events"


def ev(work, term, anchor, tid, field, role, quote, note=""):
    return {
        "work": work, "term": term, "historical_text_id": tid, "chapter_anchor": anchor,
        "claim_field": field, "evidence_role": role, "link_status": "linked",
        "link_method": "manual", "link_confidence": 1.0, "link_quality_status": "reviewed",
        "context_keywords": [],
        "review_note": f"major02-J：{work}源引文：「{quote}」；claim_field={field}；anchor=段落精确锚。{note}",
    }


BLOCKS = {
 # ---------------- 1. 城濮之战 ----------------
 "chunqiu_zhanguo/event-chengpu-zhizhan.yml": {
  "background_zh_cn": "僖公二十八年春，晋侯侵曹、伐卫，以救宋而报楚；楚人救卫，晋侯入曹、执曹伯畀宋人，晋楚之隙遂成。"
                       "先是晋文公出亡过楚，楚成王礼之，文公有「退三舍辟之」之诺——战前子犯、栾枝皆以「战而捷，必得诸侯」为言，晋侯梦与楚子搏，子犯占之曰吉，决战之意乃决。",
  "process_zh_cn": "夏四月戊辰，晋侯、宋公、齐国归父崔夭、秦小子慭次于城濮；子玉使鬥勃请战曰「请与君之士戏」，晋侯使栾枝对之。"
                   "晋师退三舍以报楚惠，楚众欲止而子玉不可；己巳，晋师陈于莘北：胥臣蒙马以虎皮先犯陈、蔡，陈蔡奔而楚右师溃；"
                   "狐毛设二旆而退之，栾枝使舆曳柴而伪遁，楚师驰之，原轸、郤溱以中军公族横击之，狐毛、狐偃以上军夹攻子西，楚左师亦溃。",
  "result_zh_cn": "楚师败绩，唯子玉收其卒而止，故不败；晋师三日馆穀，及癸酉而还。甲午至于衡雍，作王宫于践土；五月丙午晋侯及郑伯盟于衡雍，丁未献楚俘于王——驷介百乘、徒兵千，郑伯傅王，用平礼也。"
                  "己酉，王享醴，命晋侯宥——践土之会，晋文公遂为诸侯之伯。",
  "impact_zh_cn": "城濮一战胜楚而晋霸业成，践土之盟周王策命晋侯为侯伯，「九合诸侯」之局由是开端；"
                  "左氏记城濮之役「晋师三日穀，文公犹有忧色」，可见胜而愈慎；至成公二年晋人犹以「此城濮之赋也」追述其军赋之旧——晋楚争霸之格局自此绵延百余年。",
  "people": [
   {"person_name_raw": "晋文公", "role": "ruler", "link_status": "needs_linking",
    "role_zh_cn": "晋侯：退三舍报楚、一战而成伯", "review_note": "major02-J：左传·僖公二十八年「晋侯、宋公、齐国归父崔夭、秦小子慭次于城濮」", "person_id": None},
   {"person_name_raw": "子玉", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "楚令尹得臣：请战而败，后见杀", "review_note": "major02-J：左传·僖公二十八年「子玉使鬥勃请战」；「楚杀其大夫得臣」", "person_id": None},
   {"person_name_raw": "先轸", "role": "commander", "link_status": "needs_linking",
    "role_zh_cn": "晋中军将原轸：横击楚师", "review_note": "major02-J：左传·僖公二十八年「原轸、郤溱以中军公族横击之」", "person_id": None},
   {"person_name_raw": "狐偃", "role": "commander", "link_status": "needs_linking",
    "role_zh_cn": "晋上军将子犯：主战、占梦", "review_note": "major02-J：左传·僖公二十八年「子犯曰：战也」；「狐毛、狐偃以上军夹攻子西」", "person_id": None},
   {"person_name_raw": "栾枝", "role": "commander", "link_status": "needs_linking",
    "role_zh_cn": "晋将：曳柴伪遁诱楚", "review_note": "major02-J：左传·僖公二十八年「栾枝使舆曳柴而伪遁」", "person_id": None},
   {"person_name_raw": "胥臣", "role": "commander", "link_status": "needs_linking",
    "role_zh_cn": "晋下军佐：蒙马以虎皮先犯陈蔡", "review_note": "major02-J：左传·僖公二十八年「胥臣蒙马以虎皮，先犯陈、蔡」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "城濮", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "决战地（卫地）：晋楚主力会战之处", "review_note": "major02-J：左传·僖公二十八年「战于城濮，楚师败绩」"},
   {"place_name_raw": "践土", "role": "site", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "作王宫、盟诸侯之地：晋文公受策命", "review_note": "major02-J：左传·僖公二十八年「作王宫于践土」"},
   {"place_name_raw": "莘北", "role": "battlesite", "link_status": "needs_linking", "sequence": 3,
    "description_zh_cn": "晋师布阵之处（有莘之虚）", "review_note": "major02-J：左传·僖公二十八年「晋师陈于莘北」"},
  ],
  "evidence": [
   ev("左传", "僖公二十八年", "僖公/僖公二十八年#p1", "text-niutrans-a582e6a3052715d103f7", "background", "supporting",
      "二十有八年春，晋侯侵曹。"),
   ev("左传", "僖公二十八年", "僖公/僖公二十八年#p5", "text-niutrans-bdbedc26fb91a50c1860", "background", "primary",
      "三月丙午，晋侯入曹，执曹伯，畀宋人。"),
   ev("左传", "僖公二十八年", "僖公/僖公二十八年#p75", "text-niutrans-4f89631fe69543b9615a", "background", "supporting",
      "微楚之惠不及此，退三舍辟之，所以报也。"),
   ev("左传", "僖公二十八年", "僖公/僖公二十八年#p79", "text-niutrans-b332924addffbdc287dd", "process", "primary",
      "退三舍，楚众欲止，子玉不可。"),
   ev("左传", "僖公二十八年", "僖公/僖公二十八年#p98", "text-niutrans-a16d9ba9463f02fc0ccc", "process", "primary",
      "己巳，晋师陈于莘北，胥臣以下军之佐当陈、蔡。"),
   ev("左传", "僖公二十八年", "僖公/僖公二十八年#p101", "text-niutrans-93e06851f81287b77817", "process", "primary",
      "胥臣蒙马以虎皮，先犯陈、蔡。"),
   ev("左传", "僖公二十八年", "僖公/僖公二十八年#p104", "text-niutrans-8f8be2a22c8928b50fa4", "process", "primary",
      "栾枝使舆曳柴而伪遁，楚师驰之。原轸、郤溱以中军公族横击之。"),
   ev("左传", "僖公二十八年", "僖公/僖公二十八年#p6", "text-niutrans-02231e225d76da6b6db0", "result", "primary",
      "夏四月己巳，晋侯、齐师、宋师、秦师及楚人战于城濮，楚师败绩。"),
   ev("左传", "僖公二十八年", "僖公/僖公二十八年#p113", "text-niutrans-115b82b53f96799ae4df", "result", "primary",
      "丁未，献楚俘于王，驷介百乘，徒兵千。"),
   ev("左传", "僖公二十八年", "僖公/僖公二十八年#p115", "text-niutrans-d1ba255b5a0022b8ef69", "impact", "primary",
      "己酉，王享醴，命晋侯宥。", "践土受命，晋文公为诸侯伯"),
   ev("左传", "宣公十二年", "宣公/宣公十二年#p206", "text-niutrans-2471f09598ef088f12e1", "impact", "supporting",
      "城濮之役，晋师三日穀，文公犹有忧色。"),
  ],
 },
 # ---------------- 2. 邲之战 ----------------
 "chunqiu_zhanguo/event-bi-zhizhan.yml": {
  "background_zh_cn": "宣公十二年，楚子围郑，晋荀林父帅师救之，诸卿并出：赵括、赵婴齐为中军大夫，巩朔、韩穿为上军大夫，荀首、赵同为下军大夫，军令不一。"
                       "闻晋师既济，楚王欲还，嬖人伍参欲战，令尹孙叔敖弗欲，曰「昔岁入陈，今兹入郑，不无事矣」；其佐先縠刚愎不仁，未肯用命，赵括、赵同亦曰「率师以来，唯敌是求」——晋军将帅异议，战守不决。",
  "process_zh_cn": "楚师既出陈，晋师犹疑不进：彘子（先縠）以为谄，使赵括从而更之，曰「行人失辞」，遂违命而济。"
                   "楚人亦惧王之入晋军也，乃悉师以出。六月乙卯，晋荀林父帅师及楚子战于邲，楚军骤至，晋师不能成列而败。"
                   "及昏，楚师军于邲，晋之余师不能军，宵济，亦终夜有声；丙辰，楚重至于邲，遂次于衡雍。",
  "result_zh_cn": "晋师败绩，晋人讨邲之败，归罪于先縠而杀之，尽灭其族；郑人惧于邲之役而求媚于晋，晋侯复伐郑，为邲故也。"
                  "成公三年春，诸侯伐郑，次于伯牛，讨邲之役也，遂东侵郑——邲之一败，晋之诸侯之盟遂衰，楚庄王遂霸。",
  "impact_zh_cn": "邲之战为晋楚争霸之转折：晋军内部分歧致丧师，先縠以违命灭族，晋卿专权之弊暴露无遗；"
                  "楚庄王既胜于邲而威震中原，饮马黄河之志遂伸，晋楚争霸由此进入楚势全盛之期，至鞌之战、鄢陵之战乃复相攻。",
  "people": [
   {"person_name_raw": "荀林父", "role": "commander", "link_status": "needs_linking",
    "role_zh_cn": "晋中军将：帅师与楚战于邲而败", "review_note": "major02-J：左传·宣公十二年「晋荀林父帅师及楚子战于邲，晋师败绩」", "person_id": None},
   {"person_name_raw": "楚庄王", "role": "ruler", "link_status": "needs_linking",
    "role_zh_cn": "楚子：胜邲而霸", "review_note": "major02-J：左传·宣公十二年「及楚子战于邲」", "person_id": None},
   {"person_name_raw": "孙叔敖", "role": "commander", "link_status": "needs_linking",
    "role_zh_cn": "楚令尹：初不欲战而终胜", "review_note": "major02-J：左传·宣公十二年「令尹孙叔敖弗欲」", "person_id": None},
   {"person_name_raw": "先縠", "role": "commander", "link_status": "needs_linking",
    "role_zh_cn": "晋中军佐彘子：刚愎违命，败后灭族", "review_note": "major02-J：左传·宣公十二年「其佐先縠刚愎不仁，未肯用命」", "person_id": None},
   {"person_name_raw": "伍参", "role": "commander", "link_status": "needs_linking",
    "role_zh_cn": "楚嬖人：力主与晋战", "review_note": "major02-J：左传·宣公十二年「嬖人伍参欲战」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "邲", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "决战地（郑地，近荥阳）：晋楚主力会战", "review_note": "major02-J：左传·宣公十二年「战于邲，晋师败绩」"},
   {"place_name_raw": "衡雍", "role": "site", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "楚重所次之地（践土旧盟处）", "review_note": "major02-J：左传·宣公十二年「丙辰，楚重至于邲，遂次于衡雍」"},
   {"place_name_raw": "郑", "role": "contested_state", "link_status": "needs_linking", "sequence": 3,
    "description_zh_cn": "晋楚所争之郑国：邲后晋复伐郑", "review_note": "major02-J：左传·宣公十四年「夏，晋侯伐郑，为邲故也」"},
  ],
  "evidence": [
   ev("左传", "宣公十二年", "宣公/宣公十二年#p23", "text-niutrans-7f8c5e7b4c40a6a72a14", "background", "supporting",
      "赵括、赵婴齐为中军大夫。巩朔、韩穿为上军大夫。荀首、赵同为下军大夫。"),
   ev("左传", "宣公十二年", "宣公/宣公十二年#p63", "text-niutrans-13b982d475a9d55b7cf1", "background", "primary",
      "闻晋师既济，王欲还，嬖人伍参欲战。令尹孙叔敖弗欲，曰：昔岁入陈，今兹入郑，不无事矣。"),
   ev("左传", "宣公十二年", "宣公/宣公十二年#p69", "text-niutrans-b3b43266450c4232c0d3", "background", "primary",
      "其佐先縠刚愎不仁，未肯用命。"),
   ev("左传", "宣公十二年", "宣公/宣公十二年#p100", "text-niutrans-8d71a33768f2d7a74bd3", "process", "supporting",
      "彘子以为谄，使赵括从而更之，曰：行人失辞。"),
   ev("左传", "宣公十二年", "宣公/宣公十二年#p142", "text-niutrans-407aac51b4acb82c134d", "process", "primary",
      "楚人亦惧王之入晋军也，遂出陈。"),
   ev("左传", "宣公十二年", "宣公/宣公十二年#p3", "text-niutrans-b6e093257714ae5c2d7b", "result", "primary",
      "夏六月乙卯，晋荀林父帅师及楚子战于邲，晋师败绩。"),
   ev("左传", "宣公十二年", "宣公/宣公十二年#p177", "text-niutrans-c0026592078690054ab8", "result", "primary",
      "及昏，楚师军于邲，晋之馀师不能军，宵济，亦终夜有声。"),
   ev("左传", "宣公十二年", "宣公/宣公十二年#p178", "text-niutrans-b5f80f8ee4332cf7ba10", "result", "supporting",
      "丙辰，楚重至于邲，遂次于衡雍。"),
   ev("左传", "宣公十三年", "宣公/宣公十三年#p9", "text-niutrans-efcce5b2f7419ef848af", "impact", "primary",
      "冬，晋人讨邲之败，与清之师，归罪于先縠而杀之，尽灭其族。"),
   ev("左传", "宣公十四年", "宣公/宣公十四年#p10", "text-niutrans-abf964ffebaf32f8169d", "impact", "supporting",
      "夏，晋侯伐郑，为邲故也。"),
   ev("左传", "成公三年", "成公/成公三年#p17", "text-niutrans-359f4947c9d40b1df3b7", "impact", "supporting",
      "三年春，诸侯伐郑，次于伯牛，讨邲之役也，遂东侵郑。"),
  ],
 },
 # ---------------- 3. 柏举之战 ----------------
 "chunqiu_zhanguo/event-boju-zhizhan.yml": {
  "background_zh_cn": "定公四年，蔡侯、吴子与楚人构兵：春，公会刘子、晋侯、宋公、蔡侯等于召陵，侵楚；夏，蔡公孙姓帅师灭沈，楚人围蔡——蔡怨楚而请师于吴。"
                       "吴阖庐久蓄入楚之志，伍员、孙武为之谋；楚令尹子常（囊瓦）贪而失信，其臣莫有死志，楚师自小别至于大别三战皆不利，子常知不可而欲奔。",
  "process_zh_cn": "冬十有一月庚午，二师陈于柏举。阖庐之弟夫槩王晨请于阖庐曰：「楚瓦不仁，其臣莫有死志，先伐之，其卒必奔，而后大师继之，必克。」弗许。"
                   "夫槩王曰：「所谓臣义而行，不待命者，其此之谓也。今日我死，楚可入也。」乃以其属五千先击子常之卒，子常之卒奔，楚师乱，吴师大败之。",
  "result_zh_cn": "子常奔郑，史皇以其乘广死——楚之令尹既走，大军遂溃；吴人五战及郢，败诸雍澨，庚辰，吴入郢，以班处宫。"
                  "定公五年，吴人获薳射于柏举，其子帅奔徒以从子西，败吴师于军祥；秋七月，子期、子蒲灭唐——楚虽失郢而秦师来援，吴师乃退。",
  "impact_zh_cn": "柏举之战为春秋后期吴楚强弱之枢：吴以偏师深入，五战入郢，几亡楚国；楚大夫后追论之曰「阖庐惟能用其民，以败我于柏举」，可见其创痛之深。"
                  "楚迁都于鄀以避吴锋，吴亦因秦楚之反攻而未得全胜，东南两大国之争自此益烈，卒有吴越迭兴之局。",
  "people": [
   {"person_name_raw": "阖庐", "role": "ruler", "link_status": "needs_linking",
    "role_zh_cn": "吴王：用其民以败楚于柏举", "review_note": "major02-J：左传·哀公元年「阖庐惟能用其民，以败我于柏举」", "person_id": None},
   {"person_name_raw": "夫槩王", "role": "commander", "link_status": "needs_linking",
    "role_zh_cn": "阖庐之弟：不待命先击子常之卒", "review_note": "major02-J：左传·定公四年「以其属五千，先击子常之卒」", "person_id": None},
   {"person_name_raw": "子常", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "楚令尹囊瓦：贪而失众，败后奔郑", "review_note": "major02-J：左传·定公四年「子常之卒奔，楚师乱」；「子常奔郑」", "person_id": None},
   {"person_name_raw": "史皇", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "楚大夫：以乘广死战", "review_note": "major02-J：左传·定公四年「史皇以其乘广死」", "person_id": None},
   {"person_name_raw": "蔡侯", "role": "supporter", "link_status": "needs_linking",
    "role_zh_cn": "蔡昭侯：以吴子伐楚，战于柏举", "review_note": "major02-J：左传·定公四年「蔡侯以吴子及楚人战于柏举」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "柏举", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "决战地（楚地）：吴师大败楚师", "review_note": "major02-J：左传·定公四年「二师陈于柏举」"},
   {"place_name_raw": "郢", "role": "capital", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "楚都：吴人五战及郢而入之", "review_note": "major02-J：左传·定公四年「庚辰，吴入郢」"},
   {"place_name_raw": "大别", "role": "front", "link_status": "needs_linking", "sequence": 3,
    "description_zh_cn": "楚师济汉列阵之处（自小别至大别）", "review_note": "major02-J：左传·定公四年「乃济汉而陈，自小别至于大别」"},
   {"place_name_raw": "雍澨", "role": "battlesite", "link_status": "needs_linking", "sequence": 4,
    "description_zh_cn": "吴败楚师之处：五战及郢之一", "review_note": "major02-J：左传·定公四年「败诸雍澨，五战及郢」"},
  ],
  "evidence": [
   ev("左传", "定公四年", "定公/定公四年#p2", "text-niutrans-d1e37d5b154fe5cc7874", "background", "supporting",
      "三月，公会刘子、晋侯、宋公、蔡侯、卫侯、陈子、郑伯、许男、曹伯等于召陵，侵楚。"),
   ev("左传", "定公四年", "定公/定公四年#p11", "text-niutrans-dc1f315e56a968759278", "background", "supporting",
      "楚人围蔡。"),
   ev("左传", "定公四年", "定公/定公四年#p78", "text-niutrans-2dbe840c451bee821451", "background", "primary",
      "乃济汉而陈，自小别至于大别。"),
   ev("左传", "定公四年", "定公/定公四年#p82", "text-niutrans-079e3ecb5a351ea50df4", "process", "primary",
      "十一月庚午，二师陈于柏举。"),
   ev("左传", "定公四年", "定公/定公四年#p83", "text-niutrans-4b77a954e0924df53cbc", "process", "primary",
      "阖庐之弟夫槩王，晨请于阖庐曰：楚瓦不仁，其臣莫有死志，先伐之，其卒必奔。"),
   ev("左传", "定公四年", "定公/定公四年#p88", "text-niutrans-b86c2ba4c6b1d92ef831", "process", "primary",
      "以其属五千，先击子常之卒。子常之卒奔，楚师乱，吴师大败之。"),
   ev("左传", "定公四年", "定公/定公四年#p14", "text-niutrans-7799f5fe5c8a888af1df", "result", "primary",
      "冬十有一月庚午，蔡侯以吴子及楚人战于柏举，楚师败绩。"),
   ev("左传", "定公四年", "定公/定公四年#p89", "text-niutrans-0279f43c547d108dc0af", "result", "supporting",
      "子常奔郑。"),
   ev("左传", "定公四年", "定公/定公四年#p98", "text-niutrans-ef0b1350a5eef1f05d90", "result", "primary",
      "败诸雍澨，五战及郢。"),
   ev("左传", "定公四年", "定公/定公四年#p16", "text-niutrans-ca5e40f94dd4aad6194a", "result", "primary",
      "庚辰，吴入郢。"),
   ev("左传", "定公五年", "定公/定公五年#p21", "text-niutrans-76312401247ac3a2be7a", "impact", "supporting",
      "吴人获薳射于柏举。其子帅奔徒以从子西，败吴师于军祥。秋七月，子期、子蒲灭唐。"),
   ev("左传", "哀公元年", "哀公/哀公元年#p47", "text-niutrans-af6566ea91a38e827505", "impact", "primary",
      "吴师在陈，楚大夫皆惧，曰：阖庐惟能用其民，以败我于柏举。"),
  ],
 },
 # ---------------- 4. 管仲改革 ----------------
 "chunqiu_zhanguo/event-guanzhong-gaige.yml": {
  "background_zh_cn": "管仲夷吾，颍上人，少与鲍叔牙游而鲍叔知其贤；鲍叔事公子小白，管仲事公子纠。及小白立为桓公，公子纠死，管仲囚焉，鲍叔遂进管仲——"
                       "齐太公世家记桓公中钩佯死、先入而立，「召忽、管仲雠也，请得而甘心醢之」，鲁人杀子纠而管仲请囚，桓公卒置射钩之仇而使之为相。",
  "process_zh_cn": "管仲既任政相齐，以区区之齐在海滨，通货积财，富国强兵，与俗同好恶；其称曰「仓廪实而知礼节，衣食足而知荣辱，上服度则六亲固」，下令如流水之原，令顺民心，"
                   "其为政善因祸而为福、转败而为功，贵轻重、慎权衡。国语·齐语载其定民之居：制国以为二十一乡，工商之乡六、士农之乡十五，公与国子、高子各帅五乡；又「作内政而寄军令」，军政合一。",
  "result_zh_cn": "管仲既用，任政于齐，齐桓公以霸，九合诸侯，一匡天下，管仲之谋也；周襄王时桓公使管仲平戎于周，王以上卿之礼享管仲，管仲辞曰「臣贱有司也」，卒受下卿之礼而还——尊王而不僭，霸业以固。"
                  "僖公十七年，管仲卒，五公子皆求立，齐国内乱，霸业中衰。",
  "impact_zh_cn": "管仲之政以富国足民为本、以军政合一为用，齐桓之霸业实赖其纪纲齐国、裨辅先君——晋人论之曰「此大夫管仲之所以纪纲齐国，裨辅先君而成霸者也」；"
                  "其「仓廪实而知礼节」之论与通货积财之术，为后世法家与轻重之学所自出，春秋霸政之规模自此立。",
  "people": [
   {"person_name_raw": "管仲", "role": "official", "link_status": "needs_linking",
    "role_zh_cn": "齐相：通货积财、制乡作内政而寄军令", "review_note": "major02-J：史记·管晏列传「管仲既任政相齐……通货积财，富国强兵」", "person_id": None},
   {"person_name_raw": "齐桓公", "role": "ruler", "link_status": "needs_linking",
    "role_zh_cn": "齐君：置射钩之仇而相管仲，遂霸诸侯", "review_note": "major02-J：左传·僖公二十四年「齐桓公置射鉤而使管仲相」", "person_id": None},
   {"person_name_raw": "鲍叔牙", "role": "supporter", "link_status": "needs_linking",
    "role_zh_cn": "齐大夫：进管仲而以身下之", "review_note": "major02-J：史记·管晏列传「鲍叔遂进管仲」「鲍叔既进管仲，以身下之」", "person_id": None},
   {"person_name_raw": "隰朋", "role": "supporter", "link_status": "needs_linking",
    "role_zh_cn": "齐大夫：与管仲并事桓公", "review_note": "major02-J：史记·周本纪「使隰朋平戎于晋」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "齐", "role": "polity", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "管仲任政之国：区区之齐在海滨而富国强兵", "review_note": "major02-J：史记·管晏列传「以区区之齐在海滨，通货积财」"},
   {"place_name_raw": "颍上", "role": "origin", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "管仲籍贯", "review_note": "major02-J：史记·管晏列传「管仲夷吾者，颍上人也」"},
   {"place_name_raw": "周", "role": "court", "link_status": "needs_linking", "sequence": 3,
    "description_zh_cn": "王室：桓公使管仲平戎于周、王以上卿礼之", "review_note": "major02-J：史记·周本纪「齐桓公使管仲平戎于周……王以上卿礼管仲」"},
  ],
  "evidence": [
   ev("史记", "管晏列传", "七十列传/管晏列传#p1", "text-niutrans-b7deedec4d213a3f51ea", "background", "primary",
      "管仲夷吾者，颍上人也。"),
   ev("史记", "管晏列传", "七十列传/管晏列传#p5", "text-niutrans-256db546e7f6562c980f", "background", "supporting",
      "及小白立为桓公，公子纠死，管仲囚焉。"),
   ev("史记", "管晏列传", "七十列传/管晏列传#p6", "text-niutrans-c5a954ebd5fea0e05dc0", "background", "primary",
      "鲍叔遂进管仲。"),
   ev("史记", "齐太公世家", "三十世家/齐太公世家#p128", "text-niutrans-cf035d6687f66d449f89", "background", "supporting",
      "鲁人患之，遂杀子纠于笙渎。召忽自杀，管仲请囚。"),
   ev("史记", "管晏列传", "七十列传/管晏列传#p17", "text-niutrans-50722830b4b544aaf7f3", "process", "primary",
      "管仲既任政相齐，以区区之齐在海滨，通货积财，富国强兵，与俗同好恶。"),
   ev("史记", "管晏列传", "七十列传/管晏列传#p18", "text-niutrans-64c8d1df6bc802cae6e8", "process", "primary",
      "故其称曰：仓廪实而知礼节，衣食足而知荣辱，上服度则六亲固。四维不张，国乃灭亡。"),
   ev("史记", "管晏列传", "七十列传/管晏列传#p22", "text-niutrans-12bf22c3367d4272e7f0", "process", "supporting",
      "其为政也，善因祸而为福，转败而为功。"),
   ev("国语", "齐语", "齐语/管仲对桓公以霸术#p57", "text-niutrans-e31243390847f7fd119c", "process", "supporting",
      "管子于是制国以为二十一乡：工商之乡六；士农之乡十五。公帅五乡焉，国子帅五乡焉，高子帅五乡焉。"),
   ev("国语", "齐语", "齐语/管仲对桓公以霸术#p69", "text-niutrans-74fe6d7cd5ce97b4f973", "process", "primary",
      "管子对曰：作内政而寄军令焉。桓公曰：善。"),
   ev("史记", "管晏列传", "七十列传/管晏列传#p7", "text-niutrans-4ebb61fb6ee2554f4517", "result", "primary",
      "管仲既用，任政于齐，齐桓公以霸，九合诸侯，一匡天下，管仲之谋也。"),
   ev("史记", "周本纪", "十二本纪/周本纪#p392", "text-niutrans-dc0621426eb7376e2d17", "result", "supporting",
      "齐桓公使管仲平戎于周，使隰朋平戎于晋。"),
   ev("史记", "周本纪", "十二本纪/周本纪#p394", "text-niutrans-ac3352477c973d9eac0e", "impact", "supporting",
      "管仲辞曰：臣贱有司也，有天子之二守国、高在。若节春秋来承王命，何以礼焉。"),
   ev("国语", "晋语", "晋语/齐姜劝重耳勿怀安#p34", "text-niutrans-5afb4f1c755026990009", "impact", "primary",
      "此大夫管仲之所以纪纲齐国，裨辅先君而成霸者也。"),
   ev("左传", "僖公十七年", "僖公/僖公十七年#p22", "text-niutrans-d71bf7e8adc306c69513", "impact", "supporting",
      "管仲卒，五公子皆求立。"),
  ],
 },
}


def main() -> int:
    applied = 0
    for rel, block in BLOCKS.items():
        path = EVENTS / rel
        if not path.exists():
            print(f"MISSING {rel}")
            continue
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if data.get("process_zh_cn"):
            print(f"SKIP {rel}")
            continue
        with path.open("a", encoding="utf-8") as s:
            s.write("\n" + yaml.safe_dump(block, allow_unicode=True, sort_keys=False,
                                          default_flow_style=False, width=10**6))
        applied += 1
        print(f"appended {rel}")
    print(f"total: {applied}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
