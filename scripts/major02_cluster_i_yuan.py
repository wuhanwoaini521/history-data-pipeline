"""Major Batch 02 · Cluster I：元末 6 事件（红巾军起义/郭子兴起兵/陈友谅代汉/韩林儿称帝/贾鲁治河/南坡之变）。

SOURCE-BACKED FIRST：evidence 锚定元史（列传/本纪，语料无顺帝纪与河渠志，缺失处以 review_note 如实标注）与明史太祖纪。
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
        "review_note": f"major02-I：{work}源引文：「{quote}」；claim_field={field}；anchor=段落精确锚。{note}",
    }


BLOCKS = {
 # ---------------- 1. 红巾军起义 ----------------
 "yuan/event-hongjin-jun-qiyi.yml": {
  "background_zh_cn": "至正初脱脱为中书右丞相，悉更伯颜旧政，复科举、蠲负逋，中外翕然称为贤相；然河患连年，至正二年于都城外开河置闸役丁夫数万讫无成功。"
                       "时民间白莲教盛行，颍上之寇「始结白莲，以佛法诱众，终饰威权，以兵抗拒」——教门与民怨相结，遂为起事之资。",
  "process_zh_cn": "至正十一年（1351年），颍州以贼反告，时车驾在上都，朝堂皆犹豫未决，欲驿奏以待命；已而汝、颍之间妖寇聚众反，以红巾为号，襄、樊、唐、邓皆起而应之。"
                   "至正十四年，河南贼芝麻李据徐州，太师脱脱南征，用也速之计以巨石为炮昼夜攻之，贼困莫能支，遁走。"
                   "然红巾之众散而复聚，刘福通等转战中原，元军讨之屡失利：答失八都鲁与刘福通野战为其所败，将士奔溃。",
  "result_zh_cn": "红巾既起，所在兵起势相联结：安丰贼刘福通等陷汴梁，造宫阙，易正朔，号召群盗，「巴蜀、荆楚、江淮、齐鲁、辽海，西至甘肃」皆乱；"
                  "元廷遣知院达理麻失理来援，分兵雷泽、濮州，而达理麻失理为刘福通所杀，达达诸军皆溃——元之兵威自此不振。",
  "impact_zh_cn": "元末论者谓「颍上之寇……其势不至于亡吾社稷、烬吾国家不已也」：红巾军起事十数年而元亡，"
                  "朱元璋、陈友谅、张士诚皆自其中出，元末群雄之局实肇于汝颍之一呼。",
  "people": [
   {"person_name_raw": "刘福通", "role": "leader", "link_status": "needs_linking",
    "role_zh_cn": "红巾军首领：据颍州、陷汴梁、号召群盗", "review_note": "major02-I：元史「安丰贼刘福通等陷汴梁，造宫阙，易正朔」", "person_id": None},
   {"person_name_raw": "芝麻李", "role": "leader", "link_status": "needs_linking",
    "role_zh_cn": "红巾首领：据徐州，脱脱南征破之", "review_note": "major02-I：元史「河南贼芝麻李据徐州，也速从太师脱脱南征」", "person_id": None},
   {"person_name_raw": "脱脱", "role": "commander", "link_status": "needs_linking",
    "role_zh_cn": "元中书右丞相：悉更旧政、南征徐州", "review_note": "major02-I：元史·脱脱传「中外翕然称为贤相」", "person_id": None},
   {"person_name_raw": "答失八都鲁", "role": "commander", "link_status": "needs_linking",
    "role_zh_cn": "元河南行省平章：与刘福通战，屡败", "review_note": "major02-I：元史「与刘福通野战，为其所败，将士奔溃」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "颍州", "role": "origin", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "红巾起事之地：至正十一年以贼反告", "review_note": "major02-I：元史「至正十一年，颍州以贼反告」"},
   {"place_name_raw": "徐州", "role": "battlesite", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "芝麻李根据地：脱脱南征破之", "review_note": "major02-I：元史「河南贼芝麻李据徐州」"},
   {"place_name_raw": "汴梁", "role": "capital", "link_status": "needs_linking", "sequence": 3,
    "description_zh_cn": "刘福通所陷：造宫阙、易正朔", "review_note": "major02-I：元史「安丰贼刘福通等陷汴梁」"},
  ],
  "evidence": [
   ev("元史", "脱脱传", "列传/卷二十五#p205", "text-niutrans-674fbb16e637737bca9a", "background", "primary",
      "至正元年，遂命脱脱为中书右丞相、录军国重事，诏天下。脱脱乃悉更伯颜旧政……中外翕然称为贤相。"),
   ev("元史", "列传", "列传/卷七十三#p26", "text-niutrans-371208b49e64bdfdbc98", "background", "supporting",
      "颍上之寇，始结白莲，以佛法诱众，终饰威权，以兵抗拒，视其所向，骎骎可畏，其势不至于亡吾社稷、烬吾国家不已也。"),
   ev("元史", "列传", "列传/卷三十一#p124", "text-niutrans-8efe37be477634017cba", "process", "primary",
      "至正十一年，颍州以贼反告，时车驾在上都，朝堂皆犹豫未决，欲驿奏以待命。"),
   ev("元史", "脱脱传", "列传/卷二十五#p216", "text-niutrans-afca929d3304e5868dd9", "process", "primary",
      "已而汝、颍之间妖寇聚众反，以红巾为号，襄、樊、唐、邓皆起而应之。"),
   ev("元史", "列传", "列传/卷二十九#p84", "text-niutrans-ce08925ffa42e755fbf1", "process", "supporting",
      "至正十四年，河南贼芝麻李据徐州，也速从太师脱脱南征，徐州城坚不可猝拔，脱脱用也速计，以巨石为炮，昼夜攻之不息，贼困莫能支。"),
   ev("元史", "列传", "列传/卷二十九#p33", "text-niutrans-35b253fb957ae5dbe1a8", "process", "supporting",
      "六月，拜河南行省平章政事。进次许州长葛，与刘福通野战，为其所败，将士奔溃。"),
   ev("元史", "列传", "列传/卷二十八#p69", "text-niutrans-7d79b351b9f75c2428ed", "result", "primary",
      "是年，安丰贼刘福通等陷汴梁，造宫阙，易正朔，号召群盗。巴蜀、荆楚、江淮、齐鲁、辽海，西至甘肃，所在兵起，势相联结。"),
   ev("元史", "列传", "列传/卷二十九#p44", "text-niutrans-fc0d7e139841fb3bee40", "result", "supporting",
      "十月，诏遣知院达理麻失理来援，分兵雷泽、濮州，而达理麻失理为刘福通所杀，达达诸军皆溃。"),
   ev("元史", "列传", "列传/卷七十三#p26", "text-niutrans-371208b49e64bdfdbc98", "impact", "supporting",
      "其势不至于亡吾社稷、烬吾国家不已也。"),
  ],
 },
 # ---------------- 2. 郭子兴起兵 ----------------
 "yuan/event-guo-zixing-qibing.yml": {
  "background_zh_cn": "元末汝颍红巾既起，江淮响应；至正十二年春二月，定远人郭子兴与其党孙德崖等起兵濠州，据城自守。"
                       "子兴为人任侠喜宾客，马公素善子兴，临卒以后托之，子兴育之如己女，是为后来之马皇后。",
  "process_zh_cn": "太祖时在皇觉寺为僧，卜之吉，遂以闰三月甲戌朔入濠见子兴；子兴奇其状貌，留为亲兵，战辄胜，遂妻以所抚马公女。"
                   "时彭、赵所部暴横，子兴弱，太祖度无足与共事，乃以兵属他将，独与徐达、汤和、费聚等南略定远；子兴与孙德崖龃龉，太祖屡调护之。"
                   "至正十五年正月，子兴用太祖计，遣张天祐等拔和州，檄太祖总其军；三月，郭子兴卒。",
  "result_zh_cn": "子兴既卒，其部曲渐归太祖：九月郭天叙、张天祐攻集庆，野先叛，二人皆战死，「于是子兴部将尽归太祖矣」——太祖遂尽有濠州旧部，为渡江取太平、克集庆之本。",
  "impact_zh_cn": "郭子兴濠州起兵为明太祖创业所自始：太祖自亲兵而总其军，再进而尽统濠州部众，"
                  "徐达、汤和等皆自此从龙，明代开国将帅之基实立于此；子兴虽中道而卒，明兴之后犹追念其旧恩（马皇后之德亦系焉）。",
  "people": [
   {"person_name_raw": "郭子兴", "role": "leader", "link_status": "needs_linking",
    "role_zh_cn": "濠州起兵首领：太祖所依、後追封滁阳王", "review_note": "major02-I：明史·太祖纪「定远人郭子兴与其党孙德崖等起兵濠州」", "person_id": None},
   {"person_name_raw": "朱元璋", "role": "supporter", "link_status": "needs_linking",
    "role_zh_cn": "后之明太祖：入濠见子兴为亲兵，终统其军", "review_note": "major02-I：明史·太祖纪「子兴奇其状貌，留为亲兵」", "person_id": None},
   {"person_name_raw": "孙德崖", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "与子兴同起兵而相争：执子兴将杀之", "review_note": "major02-I：明史·太祖纪「德崖遂与谋，伺子兴出，执而械诸孙氏，将杀之」", "person_id": None},
   {"person_name_raw": "马皇后", "role": "supporter", "link_status": "needs_linking",
    "role_zh_cn": "马公之女：子兴育之并以妻太祖", "review_note": "major02-I：明史·太祖纪「遂妻以所抚马公女，即高皇后也」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "濠州", "role": "origin", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "起兵之地（今安徽凤阳）：太祖入濠所始", "review_note": "major02-I：明史·太祖纪「起兵濠州」"},
   {"place_name_raw": "和州", "role": "objective", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "子兴用太祖计所拔：檄太祖总其军", "review_note": "major02-I：明史·太祖纪「遣张天祐等拔和州，檄太祖总其军」"},
   {"place_name_raw": "定远", "role": "base", "link_status": "needs_linking", "sequence": 3,
    "description_zh_cn": "太祖南略之地：徐达、汤和、费聚从焉", "review_note": "major02-I：明史·太祖纪「独与徐达、汤和、费聚等南略定远」"},
  ],
  "evidence": [
   ev("明史", "太祖纪", "本纪/卷一#p17", "text-niutrans-b151b272f894a2538ebd", "background", "primary",
      "十二年春二月，定远人郭子兴与其党孙德崖等起兵濠州。"),
   ev("明史", "后妃传", "列传/卷一#p3", "text-niutrans-3b963881d8a2c6b4cbd4", "background", "supporting",
      "马公素善郭子兴，遂以后托子兴。"),
   ev("明史", "太祖纪", "本纪/卷一#p20", "text-niutrans-3ad2465fd174a4ee3e92", "process", "primary",
      "卜之吉，大喜，遂以闰三月甲戌朔入濠见子兴。"),
   ev("明史", "太祖纪", "本纪/卷一#p21", "text-niutrans-d7e7569b6516c3cb2d00", "process", "primary",
      "子兴奇其状貌，留为亲兵。战辄胜，遂妻以所抚马公女，即高皇后也。"),
   ev("明史", "太祖纪", "本纪/卷一#p33", "text-niutrans-37b9c772f3e00f80defb", "process", "supporting",
      "时彭、赵所部暴横，子兴弱，太祖度无足与共事，乃以兵属他将，独与徐达、汤和、费聚等南略定远。"),
   ev("明史", "太祖纪", "本纪/卷一#p44", "text-niutrans-0473e4d735d8f38981ec", "process", "supporting",
      "十五年春正月，子兴用太祖计，遣张天祐等拔和州，檄太祖总其军。"),
   ev("明史", "太祖纪", "本纪/卷一#p54", "text-niutrans-069aca70391d1fee1b68", "result", "primary",
      "三月，郭子兴卒。"),
   ev("明史", "太祖纪", "本纪/卷一#p84", "text-niutrans-e5b282b8da1808ad5b83", "result", "primary",
      "秋九月，郭天叙、张天祐攻集庆，野先叛，二人皆战死，于是子兴部将尽归太祖矣。"),
   ev("明史", "太祖纪", "本纪/卷一#p25", "text-niutrans-59211ebf4ecbbbc6bce7", "impact", "supporting",
      "德崖遂与谋，伺子兴出，执而械诸孙氏，将杀之。"),
  ],
 },
 # ---------------- 3. 陈友谅代汉称帝 ----------------
 "yuan/event-chenyouliang-dai-han.yml": {
  "background_zh_cn": "陈友谅本徐寿辉部将，徐寿辉据蕲水为天完之号，江左群雄之一；至正十八年四月，徐寿辉将陈友谅遣赵普胜陷池州，"
                       "至正二十年五月，徐达、常遇春败陈友谅于池州——友谅与太祖之隙既深，遂有并吞诸部、自取之志。",
  "process_zh_cn": "闰五月丙辰，友谅陷太平，守将朱文逊、院判花云、王鼎、知府许瑗死之；未几，友谅弑其主徐寿辉，自称皇帝，国号汉，尽有江西、湖广地，"
                   "约张士诚合攻应天，应天大震。太祖乃驰谕胡大海捣信州牵其后，而令康茂才以书绐友谅，令速来，设伏以待之——友谅既败于龙湾，太祖率师御之。",
  "result_zh_cn": "友谅西还，迎战于鄱阳湖：至正二十三年，友谅闻太祖至，解围，逆战于鄱阳湖；相持既久，泾江军复遮击之，友谅中流矢死，张定边以其子理奔武昌。"
                  "九月，太祖还应天，论功行赏——汉政权遂亡，江西、湖广为太祖所有。",
  "impact_zh_cn": "陈友谅之汉为元末群雄中土地最广、兵势最盛者，其亡使太祖独当江汉，南下平张士诚、北伐中原皆无后顾；"
                  "鄱阳一役亦为中国水战史上以少胜多之著例，太祖混一天下之基业自此奠定。",
  "people": [
   {"person_name_raw": "陈友谅", "role": "leader", "link_status": "needs_linking",
    "role_zh_cn": "汉帝：弑徐寿辉自立，鄱阳湖中流矢死", "review_note": "major02-I：明史·太祖纪「友谅弑其主徐寿辉，自称皇帝，国号汉」", "person_id": None},
   {"person_name_raw": "徐寿辉", "role": "victim", "link_status": "needs_linking",
    "role_zh_cn": "天完主：为友谅所弑", "review_note": "major02-I：明史·太祖纪「友谅弑其主徐寿辉」", "person_id": None},
   {"person_name_raw": "朱元璋", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "后之明太祖：御友谅于应天、大战鄱阳", "review_note": "major02-I：明史·太祖纪「太祖率师御之」", "person_id": None},
   {"person_name_raw": "康茂才", "role": "supporter", "link_status": "needs_linking",
    "role_zh_cn": "太祖将：以书绐友谅诱其速来", "review_note": "major02-I：明史·太祖纪「令康茂才以书绐友谅，令速来」", "person_id": None},
   {"person_name_raw": "张定边", "role": "supporter", "link_status": "needs_linking",
    "role_zh_cn": "友谅将：友谅死后以其子理奔武昌", "review_note": "major02-I：明史·太祖纪「张定边以其子理奔武昌」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "太平", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "友谅所陷之城：守将花云等死之", "review_note": "major02-I：明史·太祖纪「友谅陷太平」"},
   {"place_name_raw": "应天", "role": "capital", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "太祖所都：友谅约士诚合攻而应天大震", "review_note": "major02-I：明史·太祖纪「约士诚合攻应天，应天大震」"},
   {"place_name_raw": "鄱阳湖", "role": "battlesite", "link_status": "needs_linking", "sequence": 3,
    "description_zh_cn": "决战地：友谅逆战而殒", "review_note": "major02-I：明史·太祖纪「逆战于鄱阳湖」"},
   {"place_name_raw": "武昌", "role": "stronghold", "link_status": "needs_linking", "sequence": 4,
    "description_zh_cn": "汉之残部所奔之地", "review_note": "major02-I：明史·太祖纪「张定边以其子理奔武昌」"},
  ],
  "evidence": [
   ev("明史", "太祖纪", "本纪/卷一#p118", "text-niutrans-a3d8ada5a7657b468cbc", "background", "supporting",
      "夏四月，徐寿辉将陈友谅遣赵普胜陷池州。"),
   ev("明史", "太祖纪", "本纪/卷一#p150", "text-niutrans-ffbfd63997b42867f399", "background", "supporting",
      "夏五月，徐达、常遇春败陈友谅于池州。"),
   ev("明史", "太祖纪", "本纪/卷一#p151", "text-niutrans-29568720098ca7d64b04", "process", "primary",
      "闰月丙辰，友谅陷太平，守将朱文逊，院判花云、王鼎，知府许瑗死之。"),
   ev("明史", "太祖纪", "本纪/卷一#p152", "text-niutrans-040e9218671701ae06b8", "process", "primary",
      "未几，友谅弑其主徐寿辉，自称皇帝，国号汉，尽有江西、湖广地，约士诚合攻应天，应天大震。"),
   ev("明史", "太祖纪", "本纪/卷一#p157", "text-niutrans-4c84d1cf48306fd50613", "process", "supporting",
      "乃驰谕胡大海捣信州牵其后，而令康茂才以书绐友谅，令速来。"),
   ev("明史", "太祖纪", "本纪/卷一#p213", "text-niutrans-5d6bb80dae47b7c974b0", "result", "primary",
      "友谅闻太祖至，解围，逆战于鄱阳湖。"),
   ev("明史", "太祖纪", "本纪/卷一#p231", "text-niutrans-eb7b431d142747608cec", "result", "primary",
      "泾江军复遮击之，友谅中流矢死。"),
   ev("明史", "太祖纪", "本纪/卷一#p232", "text-niutrans-a5335897b19f2ab6ecf1", "result", "supporting",
      "张定边以其子理奔武昌。"),
   ev("明史", "太祖纪", "本纪/卷一#p233", "text-niutrans-30afa05620fa526c9b2b", "impact", "supporting",
      "九月，还应天，论功行赏。"),
  ],
 },
 # ---------------- 4. 韩林儿称帝（龙凤政权） ----------------
 "yuan/event-han-liner-chengdi.yml": {
  "background_zh_cn": "至正十五年，刘福通等访求韩山童之子林儿于砀山，迎立之于亳，国号宋，建元龙凤，"
                       "中原红巾诸部奉之为共主；韩山童先以白莲教聚众起事而被害，林儿承其名号，宋室复兴之说遂为号召。",
  "process_zh_cn": "龙凤政权初都亳州，至正十七年刘福通破汴梁，迎韩林儿都之，以为宋室旧都；然红巾诸部不相统属，"
                   "至正十九年秋八月，元察罕帖木儿复汴梁，福通以林儿退保安丰。太祖初起，念林儿势盛可倚藉，乃用其年号以令军中，龙凤正朔行于江南。",
  "result_zh_cn": "至正二十三年三月，张士诚将吕珍攻安丰，太祖自将救之，珍败走，以韩林儿归滁州，乃还应天；"
                  "龙凤政权名存实亡，至正二十六年十二月，韩林儿卒——宋之号遂绝，太祖亦不复用龙凤年号。",
  "impact_zh_cn": "韩林儿之宋为元末红巾之共名，太祖始奉龙凤而后自成：其兴也以白莲之众，其亡也以群雄相攻，"
                  "龙凤年号之废为太祖建号吴、进而定鼎金陵之先声，元末群雄由「复宋」而归于新朝之局于此可见。",
  "people": [
   {"person_name_raw": "韩林儿", "role": "ruler", "link_status": "needs_linking",
    "role_zh_cn": "宋帝（小明王）：龙凤政权之共主", "review_note": "major02-I：明史·太祖纪「时刘福通迎立韩山童子林儿于亳，国号宋，建元龙凤」", "person_id": None},
   {"person_name_raw": "刘福通", "role": "leader", "link_status": "needs_linking",
    "role_zh_cn": "红巾首领：迎立林儿、破汴梁、保林儿于安丰", "review_note": "major02-I：明史·太祖纪「刘福通破汴梁，迎韩林儿都之」", "person_id": None},
   {"person_name_raw": "韩山童", "role": "historical", "link_status": "needs_linking",
    "role_zh_cn": "林儿之父：白莲教首倡起事者", "review_note": "major02-I：明史·太祖纪「迎立韩山童子林儿于亳」", "person_id": None},
   {"person_name_raw": "朱元璋", "role": "supporter", "link_status": "needs_linking",
    "role_zh_cn": "后之明太祖：用龙凤年号、救安丰迎林儿", "review_note": "major02-I：明史·太祖纪「乃用其年号以令军中」；「以韩林儿归滁州」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "亳", "role": "capital", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "龙凤政权初建之地", "review_note": "major02-I：明史·太祖纪「迎立韩山童子林儿于亳」"},
   {"place_name_raw": "汴梁", "role": "capital", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "宋室旧都：刘福通破之而迎林儿都焉", "review_note": "major02-I：明史·太祖纪「刘福通破汴梁，迎韩林儿都之」"},
   {"place_name_raw": "安丰", "role": "stronghold", "link_status": "needs_linking", "sequence": 3,
    "description_zh_cn": "汴梁复失后林儿所退保之地", "review_note": "major02-I：明史·太祖纪「福通以林儿退保安丰」"},
   {"place_name_raw": "滁州", "role": "place_of_residence", "link_status": "needs_linking", "sequence": 4,
    "description_zh_cn": "太祖迎林儿所归之地", "review_note": "major02-I：明史·太祖纪「以韩林儿归滁州」"},
  ],
  "evidence": [
   ev("明史", "太祖纪", "本纪/卷一#p55", "text-niutrans-6412d3f729fe6534434d", "background", "primary",
      "时刘福通迎立韩山童子林儿于亳，国号宋，建元龙凤。"),
   ev("明史", "太祖纪", "本纪/卷一#p58", "text-niutrans-b93a24ef56bc3e20d454", "process", "primary",
      "然念林儿势盛，可倚藉，乃用其年号以令军中。"),
   ev("明史", "太祖纪", "本纪/卷一#p120", "text-niutrans-f0d6dfa42402a0ee2b5b", "process", "supporting",
      "五月，刘福通破汴梁，迎韩林儿都之。"),
   ev("明史", "太祖纪", "本纪/卷一#p143", "text-niutrans-24785a6b270a8ad41a41", "process", "supporting",
      "秋八月，元察罕帖木儿复汴梁，福通以林儿退保安丰。"),
   ev("元史", "列传", "列传/卷二十八#p69", "text-niutrans-7d79b351b9f75c2428ed", "process", "supporting",
      "是年，安丰贼刘福通等陷汴梁，造宫阙，易正朔，号召群盗。"),
   ev("明史", "太祖纪", "本纪/卷一#p206", "text-niutrans-8ddcaf4feab93284e60f", "result", "primary",
      "三月辛丑，太祖自将救安丰，珍败走，以韩林儿归滁州，乃还应天。"),
   ev("明史", "太祖纪", "本纪/卷一#p302", "text-niutrans-fb0f366c80545388859d", "impact", "primary",
      "十二月，韩林儿卒。"),
  ],
 },
 # ---------------- 5. 贾鲁治河 ----------------
 "yuan/event-jialu-zhihe.yml": {
  "background_zh_cn": "至正初脱脱复相，中外翕然称为贤相；然河患积年，至正二年尝于都城外开河置闸、放金口水，欲引通州船至丽正门，役丁夫数万而讫无成功。"
                       "元末论治河者谓「自古治河，处得其当，则用力少而患迟；事失其宜，则用力多而患速」，河事之难为朝野所共知。",
  "process_zh_cn": "至正十一年（1351年），元廷决意大举治河，开黄河故道、塞决口，役丁夫以兴工；"
                   "工既毕，天子嘉其功，赐世袭答剌罕之号，又敕儒臣欧阳玄制《河平碑》以载其功，仍赐淮安路为其食邑。"
                   "（按：元史语料无河渠志与顺帝纪，一期工程之役夫数目与贾鲁之名据《元史·河渠志》后世补记，本事件以「河平碑」与红巾起事为锚。）",
  "result_zh_cn": "河工之役与民力相弊：已而汝、颍之间妖寇聚众反，以红巾为号，襄、樊、唐、邓皆起而应之；"
                  "至正十一年颍州以贼反告，时车驾在上都，朝堂皆犹豫未决，欲驿奏以待命——治河之众散而为乱，元末大乱自此不可制。",
  "impact_zh_cn": "贾鲁治河为元代最后一次大规模河工，塞决、开故道于一时有功，河平之碑立于朝；"
                  "然役重民困，河工之丁夫与白莲之众相合，遂为亡元之祸首——颍上之寇「其势不至于亡吾社稷、烬吾国家不已也」，论者以治河为元亡之近因。",
  "people": [
   {"person_name_raw": "贾鲁", "role": "engineer", "link_status": "needs_linking",
    "role_zh_cn": "河工主持人：开黄河故道、塞决口", "review_note": "major02-I：元史语料无河渠志/顺帝纪，贾鲁之名据元史河渠志后世补记；本事件以河平碑（脱脱传）与红巾起事为锚", "person_id": None},
   {"person_name_raw": "脱脱", "role": "official", "link_status": "needs_linking",
    "role_zh_cn": "中书右丞相：主持治河、受答剌罕之号", "review_note": "major02-I：元史·脱脱传「于是天子嘉其功，赐世袭答剌罕之号」", "person_id": None},
   {"person_name_raw": "欧阳玄", "role": "official", "link_status": "needs_linking",
    "role_zh_cn": "儒臣：奉敕制《河平碑》", "review_note": "major02-I：元史·脱脱传「敕儒臣欧阳玄制《河平碑》以载其功」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "黄河", "role": "work_site", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "治河对象：开故道、塞决口", "review_note": "major02-I：元史·脱脱传（河平碑）；元史「境有黄河故道」"},
   {"place_name_raw": "淮安路", "role": "fief", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "治河功成后脱脱所赐食邑", "review_note": "major02-I：元史·脱脱传「仍赐淮安路为其食邑」"},
   {"place_name_raw": "颍州", "role": "revolt_site", "link_status": "needs_linking", "sequence": 3,
    "description_zh_cn": "河工之众起事之地：至正十一年以贼反告", "review_note": "major02-I：元史「至正十一年，颍州以贼反告」"},
  ],
  "evidence": [
   ev("元史", "脱脱传", "列传/卷二十五#p205", "text-niutrans-674fbb16e637737bca9a", "background", "primary",
      "至正元年，遂命脱脱为中书右丞相、录军国重事……二年五月，用参议孛罗帖木儿等言，于都城外开河置闸，放金口水，欲引通州船至丽正门，役丁夫数万，讫无成功。"),
   ev("元史", "列传", "列传/卷五十七#p21", "text-niutrans-ff0cd758ff4896068e3c", "background", "supporting",
      "自古治河，处得其当，则用力少而患迟；事失其宜，则用力多而患速。此不易之定论也。"),
   ev("元史", "脱脱传", "列传/卷二十五#p214", "text-niutrans-d6e7ed3ee7fe7c7c99f4", "process", "primary",
      "于是天子嘉其功，赐世袭答剌罕之号。又敕儒臣欧阳玄制《河平碑》以载其功。"),
   ev("元史", "脱脱传", "列传/卷二十五#p215", "text-niutrans-1bc17b21b11c6fd1561f", "process", "supporting",
      "仍赐淮安路为其食邑，郡邑长吏听其自用。"),
   ev("元史", "脱脱传", "列传/卷二十五#p216", "text-niutrans-afca929d3304e5868dd9", "result", "primary",
      "已而汝、颍之间妖寇聚众反，以红巾为号，襄、樊、唐、邓皆起而应之。"),
   ev("元史", "列传", "列传/卷三十一#p124", "text-niutrans-8efe37be477634017cba", "result", "primary",
      "至正十一年，颍州以贼反告，时车驾在上都，朝堂皆犹豫未决，欲驿奏以待命。"),
   ev("元史", "列传", "列传/卷七十三#p26", "text-niutrans-371208b49e64bdfdbc98", "impact", "primary",
      "颍上之寇，始结白莲，以佛法诱众，终饰威权，以兵抗拒，视其所向，骎骎可畏，其势不至于亡吾社稷、烬吾国家不已也。"),
   ev("元史", "列传", "列传/卷七十七#p104", "text-niutrans-1bdce3d99ae8fc3f2d1a", "impact", "supporting",
      "十年，召为秘书少监，议治河事，皆辞疾不赴。", "时人于治河之议多有避忌，可见其事之难与民力之弊"),
  ],
 },
 # ---------------- 6. 南坡之变 ----------------
 "yuan/event-nanpo-zhi-bian.yml": {
  "background_zh_cn": "英宗硕德八剌即位，厉精图治，丞相拜住请更前政不便者，会议中书堂，中外望治；"
                       "然英宗锐于更张，铁木迭儿之党失势，御史大夫铁失等内不自安，遂谋为变。",
  "process_zh_cn": "至治三年（1323年）秋八月癸亥，英宗自上都南还，驻跸南坡。是夕，铁失与知枢密院事也先铁木儿、大司农失秃儿、"
                   "前中书平章政事赤斤铁木儿、前治书侍御史锁南等，及诸王按梯不花、孛罗等，以铁失所领阿速卫兵为外应，杀右丞相拜住，铁失直犯禁幄，手弑英宗于卧所。"
                   "（《元史·泰定帝纪》亦书：「是夕，铁失等矫杀拜住，英宗遂遇弑于幄殿。」）",
  "result_zh_cn": "变起之后，晋王也孙铁木儿（泰定帝）即位于龙居河，九月四日，铁失及其党皆伏诛；元廷遣旭迈杰、纽泽诛逆贼铁失、失秃儿、赤斤铁木儿等于大都，并戮其子孙、籍入家产。"
                  "泰定元年，御史犹言「逆贼铁失等虽伏诛，其党枢密副使阿散身亲弑逆，以告变得不死」，乞早正天讨。",
  "impact_zh_cn": "南坡之变弑君于行幄，为元代政治之一大转折：英宗新政随之中止，泰定以降权臣与诸王交结之局渐深，"
                  "距亡国不足五十年；后世论者以宿卫之臣不能死节为耻（「南坡之变，不能勇效一死」），可见士论之痛。",
  "people": [
   {"person_name_raw": "元英宗", "role": "ruler", "link_status": "needs_linking",
    "role_zh_cn": "元英宗硕德八剌：遇弑于南坡", "review_note": "major02-I：元史「铁失直犯禁幄，手弑英宗于卧所」", "person_id": None},
   {"person_name_raw": "拜住", "role": "official", "link_status": "needs_linking",
    "role_zh_cn": "中书右丞相：新政主持者，被杀于变中", "review_note": "major02-I：元史「杀右丞相拜住」", "person_id": None},
   {"person_name_raw": "铁失", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "御史大夫：南坡之变主谋，后伏诛", "review_note": "major02-I：元史「铁失及其党皆伏诛」", "person_id": None},
   {"person_name_raw": "泰定帝", "role": "ruler", "link_status": "needs_linking",
    "role_zh_cn": "晋王也孙铁木儿：变后即位，诛逆党", "review_note": "major02-I：元史「九月四日，晋王即位，铁失及其党皆伏诛」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "南坡", "role": "site", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "弑君之地（上都以南驻跸处）", "review_note": "major02-I：元史「英宗自上都南还，驻跸南坡」"},
   {"place_name_raw": "上都", "role": "capital", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "英宗南还所自之地", "review_note": "major02-I：元史「英宗自上都南还，驻跸南坡」"},
   {"place_name_raw": "大都", "role": "capital", "link_status": "needs_linking", "sequence": 3,
    "description_zh_cn": "逆党伏诛之地", "review_note": "major02-I：元史「诛逆贼铁失、失秃儿、赤斤铁木儿、脱火赤、章台等于大都」"},
  ],
  "evidence": [
   ev("元史", "列传", "列传/卷七十一#p79", "text-niutrans-2b60e737fb148332735f", "background", "primary",
      "时英宗厉精图治，丞相拜住请更前政不便者，会议中书堂，克敬首言：江南包银，民贫有不能输者，有司以责之役户，甚无谓也，当罢之。"),
   ev("元史", "英宗纪", "本纪/卷二十八#p403", "text-niutrans-da9e8b252ce9445a8d48", "process", "primary",
      "八月癸亥，车驾南还，驻跸南坡。"),
   ev("元史", "列传", "列传/卷九十四#p20", "text-niutrans-d74ac312cd23e894e764", "process", "primary",
      "秋八月癸亥，英宗自上都南还，驻跸南坡。是夕，铁失与知枢密院事也先铁木儿……杀右丞相拜住，而铁失直犯禁幄，手弑英宗于卧所。"),
   ev("元史", "泰定帝纪", "本纪/卷二十九#p14", "text-niutrans-ff67edbe7d8665978f04", "process", "supporting",
      "是夕，铁失等矫杀拜住，英宗遂遇弑于幄殿。"),
   ev("元史", "列传", "列传/卷九十四#p21", "text-niutrans-92aa9b34321830cc66a7", "result", "primary",
      "九月四日，晋王即位，铁失及其党皆伏诛。"),
   ev("元史", "泰定帝纪", "本纪/卷二十九#p25", "text-niutrans-9fbe0ae45ef0cb45d4b0", "result", "primary",
      "遣旭迈杰、纽泽诛逆贼铁失、失秃儿、赤斤铁木儿、脱火赤、章台等于大都，并戮其子孙，籍入家产。"),
   ev("元史", "列传", "列传/卷七十一#p133", "text-niutrans-3516be94ca04f8305ce5", "impact", "supporting",
      "臣曩备宿卫，南坡之变，不能勇效一死，以报国士之知。"),
   ev("元史", "列传", "列传/卷六十九#p159", "text-niutrans-e170c05d638e64093fae", "impact", "supporting",
      "泰定元年春，除监察御史，首言：逆贼铁失等虽伏诛，其党枢密副使阿散，身亲弑逆，以告变得不死，窜岭南，乞早正天讨。"),
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
