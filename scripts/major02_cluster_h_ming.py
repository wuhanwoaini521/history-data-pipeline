"""Major Batch 02 · Cluster H：明 8 事件。

SOURCE-BACKED FIRST：evidence 全部锚定 data/normalized/history.duckdb 中已定位的明史
（本纪/列传/志）与清史稿段落；后金建立一役语料以「大清兵」纪事，锚点如实标注。
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
        "review_note": f"major02-H：{work}源引文：「{quote}」；claim_field={field}；anchor=段落精确锚。{note}",
    }


BLOCKS = {
 # ---------------- 1. 北京保卫战 ----------------
 "ming/event-beijing-baoweizhan.yml": {
  "background_zh_cn": "正统十四年（1449年）七月，瓦剌也先寇大同，参将吴浩战死，英宗下诏亲征；太监王振挟帝北行，尚书邝埜与于谦极谏而不听。"
                       "八月，军次土木，瓦剌兵追至，师大溃，帝蒙尘而王振为乱兵所杀；败报至京，百官恸哭，京师大震，众莫知所为。",
  "process_zh_cn": "郕王监国，命群臣议战守；侍讲徐珵言星象有变当南迁，于谦厉声曰「言南迁者，可斩也」，力主固守京师。"
                   "谦请檄取两京、河南备操军，山东及南京沿海备倭军，江北及北京诸府运粮军亟赴京师，以次经画部署，人心稍安；又遣都督孙镗、卫颖、张軏等分兵守九门要地，列营郭外。"
                   "十月，也先挟上皇破紫荆关直入，京师戒严；于谦亟分遣诸将，率师二十二万列阵九门外，自与石亨率副总兵范广、武兴陈德胜门外当也先。",
  "result_zh_cn": "也先薄都城，都督高礼、毛福寿败之于彰义门，于谦、石亨等连败也先众于城下；相持五日，「也先邀请既不应，战又不利，知终弗可得志，又闻勤王师且至，恐断其归路，遂拥上皇由良乡西去」。"
                  "景泰元年，杨善至瓦剌，也先许上皇归；「卒奉上皇以归，谦力也」。",
  "impact_zh_cn": "京师解严而明室转危为安，于谦以社稷安危为己任、排众议而立郕王，景帝一朝战守之政皆本于此役；"
                  "上皇虽还，南宫幽居，遂启八年后夺门之变之衅。此役亦为明廷南北两京备倭、备操军制的一次实战检验。",
  "people": [
   {"person_name_raw": "于谦", "role": "commander", "link_status": "needs_linking",
    "role_zh_cn": "兵部尚书：主固守、部署九门、躬督德胜门外", "review_note": "major02-H：明史·于谦传「谦自与石亨率副总兵范广、武兴陈德胜门外，当也先」", "person_id": None},
   {"person_name_raw": "石亨", "role": "commander", "link_status": "needs_linking",
    "role_zh_cn": "武清侯：与于谦同总理军务、连败也先", "review_note": "major02-H：明史·景帝纪「于谦、石亨等连败也先众于城下」", "person_id": None},
   {"person_name_raw": "也先", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "瓦剌太师：挟上皇入寇、薄都城", "review_note": "major02-H：明史·景帝纪「戊午，也先薄都城」", "person_id": None},
   {"person_name_raw": "王振", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "司礼太监：挟帝亲征致土木之败，为乱兵所杀", "review_note": "major02-H：明史·于谦传「王振挟帝亲征」；宦官传「帝蒙尘，振乃为乱兵所杀」", "person_id": None},
   {"person_name_raw": "郕王", "role": "ruler", "link_status": "needs_linking",
    "role_zh_cn": "监国→景帝：战守之政所奉", "review_note": "major02-H：明史·于谦传「郕王监国，命群臣议战守」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "京师", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "决战地：九门外列阵二十二万、德胜门血战", "review_note": "major02-H：明史·于谦传「率师二十二万，列阵九门外」"},
   {"place_name_raw": "土木", "role": "battlesite", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "前役覆军处：英宗蒙尘之地", "review_note": "major02-H：明史·英宗前纪「辛酉，次土木，被围」"},
   {"place_name_raw": "紫荆关", "role": "front", "link_status": "needs_linking", "sequence": 3,
    "description_zh_cn": "也先入塞之关隘：陷后京师戒严", "review_note": "major02-H：明史·景帝纪「也先陷紫荆关，孙祥死之，京师戒严」"},
  ],
  "evidence": [
   ev("明史", "英宗前纪", "本纪/卷十#p274", "text-niutrans-22bc07d53023ec3bd799", "background", "primary",
      "秋七月己丑，瓦剌也先寇大同，参将吴浩战死，下诏亲征。"),
   ev("明史", "于谦传", "列传/卷五十八#p45", "text-niutrans-049a17922f26d9b93981", "background", "supporting",
      "谦与尚书邝埜极谏，不听。"),
   ev("明史", "英宗前纪", "本纪/卷十#p290", "text-niutrans-51c128b7b387dfaf7658", "background", "primary",
      "辛酉，次土木，被围。"),
   ev("明史", "于谦传", "列传/卷五十八#p47", "text-niutrans-985211e7456ae544a5a7", "background", "primary",
      "及驾陷土木，京师大震，众莫知所为。"),
   ev("明史", "于谦传", "列传/卷五十八#p50", "text-niutrans-5b6401cef831f1bc05ff", "process", "primary",
      "谦厉声曰：言南迁者，可斩也。"),
   ev("明史", "于谦传", "列传/卷五十八#p54", "text-niutrans-5b5fabfc48ec3e6dcf3b", "process", "primary",
      "谦请王檄取两京、河南备操军，山东及南京沿海备倭军，江北及北京诸府运粮军，亟赴京师。以次经画部署，人心稍安。"),
   ev("明史", "于谦传", "列传/卷五十八#p84", "text-niutrans-e12e4e307995ee82ea8d", "process", "primary",
      "亟分遣诸将，率师二十二万，列阵九门外：都督陶瑾安定门，广宁伯刘安东直门……而谦自与石亨率副总兵范广、武兴陈德胜门外，当也先。"),
   ev("明史", "景帝纪", "本纪/卷十一#p35", "text-niutrans-964cdc5f6fe750673406", "process", "supporting",
      "丙辰，也先陷紫荆关，孙祥死之，京师戒严。"),
   ev("明史", "景帝纪", "本纪/卷十一#p40", "text-niutrans-72d7f1b89bb2179951ce", "result", "primary",
      "于谦、石亨等连败也先众于城下。"),
   ev("明史", "于谦传", "列传/卷五十八#p104", "text-niutrans-008120b38fc0741fc8a2", "result", "primary",
      "相持五日，也先邀请既不应，战又不利，知终弗可得志，又闻勤王师且至，恐断其归路，遂拥上皇由良乡西去。"),
   ev("明史", "景帝纪", "本纪/卷十一#p100", "text-niutrans-b6090ba2b17e5751ac7d", "impact", "supporting",
      "己巳，杨善至瓦剌，也先许上皇归。"),
   ev("明史", "于谦传", "列传/卷五十八#p135", "text-niutrans-0776e919fb19e36cca08", "impact", "primary",
      "先后遣李实、杨善往。卒奉上皇以归，谦力也。"),
  ],
 },
 # ---------------- 2. 崇祯帝即位 ----------------
 "ming/event-chongzhen-jiwei.yml": {
  "background_zh_cn": "天启七年（1627年）八月熹宗崩，无嗣，遗诏以弟信王嗣位。时魏忠贤以司礼监秉笔提督东厂，与崔呈秀等结阉党，"
                       "兴汪文言狱，逮杨涟、左光斗、魏大中、周朝瑞、顾大章等，削赵南星等籍，朝士善类一空。",
  "process_zh_cn": "崇祯帝即位之初，先安置魏忠贤于凤阳，未几忠贤缢死于道；乃戮忠贤及其党崔呈秀尸，削其党冯铨、魏广微籍。"
                   "崇祯二年，定逆案，自崔呈秀以下凡六等，阉党之局遂倾；又赠恤冤陷诸臣，被逮诸君子次第昭雪。",
  "result_zh_cn": "魏忠贤既诛，其党六等定罪，生者戍夺、死者戮尸，阉党不复能祸朝政；汪文言狱所陷诸臣得赠恤，东林善类稍得伸眉。"
                  "然门户之见已深，定逆案之后朝论益分，攻东林者转以「逆案」为口实相攻。",
  "impact_zh_cn": "崇祯初政以诛阉、定案为始，一时号清明；然党争并未止息，十七年间阁臣屡易、边事日坏，"
                  "终至李自成入京师、帝崩于万岁山，王承恩从死——明代之亡虽非阉祸直接所致，而朝局内耗实为长因之一。",
  "people": [
   {"person_name_raw": "崇祯帝", "role": "ruler", "link_status": "needs_linking",
    "role_zh_cn": "信王→庄烈帝：即位后诛魏忠贤、定逆案", "review_note": "major02-H：明史·庄烈帝纪「安置魏忠贤于凤阳」「定逆案」", "person_id": None},
   {"person_name_raw": "魏忠贤", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "司礼太监：天启间专权，崇祯初安置凤阳、缢死", "review_note": "major02-H：明史·庄烈帝纪「己巳，魏忠贤缢死」", "person_id": None},
   {"person_name_raw": "崔呈秀", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "阉党首魁：逆案以之为首，死后戮尸", "review_note": "major02-H：明史·庄烈帝纪「戮魏忠贤及其党崔呈秀尸」", "person_id": None},
   {"person_name_raw": "杨涟", "role": "supporter", "link_status": "needs_linking",
    "role_zh_cn": "左副都御史：劾魏忠贤者，天启间死于狱", "review_note": "major02-H：明史·熹宗纪「逮杨涟、左光斗、袁化中、魏大中、周朝瑞、顾大章」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "京师", "role": "capital", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "诛阉、定逆案之地", "review_note": "major02-H：明史·庄烈帝纪（即位及定逆案皆在京师）"},
   {"place_name_raw": "凤阳", "role": "place_of_exile", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "魏忠贤安置之地：途中缢死", "review_note": "major02-H：明史·庄烈帝纪「安置魏忠贤于凤阳」"},
  ],
  "evidence": [
   ev("明史", "熹宗纪", "本纪/卷二十二#p167", "text-niutrans-15347ceae6adf542f81d", "background", "primary",
      "丁丑，谳汪文言狱，逮杨涟、左光斗、袁化中、魏大中、周朝瑞、顾大章，削尚书赵南星等籍。"),
   ev("明史", "庄烈帝纪", "本纪/卷二十三#p14", "text-niutrans-f92b75312189340d01cd", "process", "primary",
      "十一月甲子，安置魏忠贤于凤阳。"),
   ev("明史", "庄烈帝纪", "本纪/卷二十三#p16", "text-niutrans-eef1e375737d252123e3", "process", "primary",
      "己巳，魏忠贤缢死。"),
   ev("明史", "庄烈帝纪", "本纪/卷二十三#p23", "text-niutrans-e0640bcaf3317823c13d", "result", "primary",
      "丙戌，戮魏忠贤及其党崔呈秀尸。"),
   ev("明史", "庄烈帝纪", "本纪/卷二十三#p37", "text-niutrans-0817d40239811bb4731f", "result", "supporting",
      "六月，削魏忠贤党冯铨、魏广微籍。"),
   ev("明史", "庄烈帝纪", "本纪/卷二十三#p53", "text-niutrans-46ec82dd7ff90ef015dc", "result", "primary",
      "丁丑，定逆案，自崔呈秀以下凡六等。"),
   ev("明史", "庄烈帝纪", "本纪/卷二十三#p29", "text-niutrans-dfb62c4e8fc0b978664f", "impact", "supporting",
      "乙酉，赠恤冤陷诸臣。"),
   ev("明史", "庄烈帝纪", "本纪/卷二十四#p286", "text-niutrans-98a396d48fa8cc7de2b9", "impact", "supporting",
      "帝崩于万岁山，王承恩从死。", "长时段结局：崇祯十七年京师陷、帝殉国"),
  ],
 },
 # ---------------- 3. 建文帝削藩 ----------------
 "ming/event-jianwen-xuefan.yml": {
  "background_zh_cn": "洪武三十一年太祖崩，皇太孙即位，命齐泰与黄子澄同参国政，寻进尚书；时诸王以叔父之尊拥兵边塞，周、齐、湘、代、岷诸王多不法，"
                       "朝廷议削藩以固皇权，遂有次第废徙之举。",
  "process_zh_cn": "建文元年（1399年）八月，周王橚有罪，废为庶人，徙云南；夏四月，湘王柏自焚死，齐王榑、代王桂并废为庶人，"
                   "同时遣燕王世子高炽及其弟高煦、高燧还北平以安燕藩。既而诏让燕王棣，逮其王府官僚，削夺之意渐明；"
                   "秋七月癸酉，燕王棣举兵反，杀布政使张昺、都司谢贵，以「诛齐泰、黄子澄」为名，号其众曰靖难之师。",
  "result_zh_cn": "朝廷初贬齐泰、黄子澄于外以缓燕师，旋复召二人；南北转战四年，建文四年六月乙丑燕兵犯金川门，左都督徐增寿谋内应伏诛，"
                  "宫中火起，帝不知所终——削藩之政以藩王入继告终。",
  "impact_zh_cn": "建文削藩失败，燕王以「靖难」入承大统，是为成祖；有明一代藩禁自此大严，宗室不典兵、不预政，"
                  "而永乐以后内阁与宦官之制亦由此开其端，明初政治格局为之一变。",
  "people": [
   {"person_name_raw": "建文帝", "role": "ruler", "link_status": "needs_linking",
    "role_zh_cn": "皇太孙→恭闵帝：主持削藩，兵败不知所终", "review_note": "major02-H：明史·恭闵帝纪「宫中火起，帝不知所终」", "person_id": None},
   {"person_name_raw": "齐泰", "role": "official", "link_status": "needs_linking",
    "role_zh_cn": "兵部尚书：削藩谋主之一", "review_note": "major02-H：明史·齐泰传「及即位，命与黄子澄同参国政」", "person_id": None},
   {"person_name_raw": "黄子澄", "role": "official", "link_status": "needs_linking",
    "role_zh_cn": "太常卿：与齐泰同主削藩", "review_note": "major02-H：明史·齐泰传「兵起，以诛齐泰、黄子澄为名」", "person_id": None},
   {"person_name_raw": "燕王朱棣", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "燕王→成祖：举兵靖难、入承大统", "review_note": "major02-H：明史·恭闵帝纪「燕王棣举兵反，杀布政使张昺、都司谢贵」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "北平", "role": "base", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "燕藩治所：靖难之师所自起", "review_note": "major02-H：明史·恭闵帝纪「遣燕王世子高炽及其弟高煦、高燧还北平」"},
   {"place_name_raw": "云南", "role": "place_of_exile", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "周王废徙之地", "review_note": "major02-H：明史·恭闵帝纪「周王橚有罪，废为庶人，徙云南」"},
   {"place_name_raw": "金川门", "role": "battlesite", "link_status": "needs_linking", "sequence": 3,
    "description_zh_cn": "京师城门：燕兵入城处", "review_note": "major02-H：明史·恭闵帝纪「乙丑，燕兵犯金川门」"},
  ],
  "evidence": [
   ev("明史", "齐泰传", "列传/卷二十九#p10", "text-niutrans-11e306b1ca1e6cddf894", "background", "primary",
      "及即位，命与黄子澄同参国政。寻进尚书。"),
   ev("明史", "恭闵帝纪", "本纪/卷四#p26", "text-niutrans-ef7a9e6a0f73bf16b1af", "process", "primary",
      "八月，周王橚有罪，废为庶人，徙云南。"),
   ev("明史", "恭闵帝纪", "本纪/卷四#p52", "text-niutrans-51fb0425357d461ef42c", "process", "primary",
      "夏四月，湘王柏自焚死。"),
   ev("明史", "恭闵帝纪", "本纪/卷四#p53", "text-niutrans-aa8bcf31593e9366549c", "process", "supporting",
      "齐王榑、代王桂有罪，废为庶人。遣燕王世子高炽及其弟高煦、高燧还北平。"),
   ev("明史", "恭闵帝纪", "本纪/卷四#p56", "text-niutrans-4914c60ceb525eb9386f", "process", "supporting",
      "诏让燕王棣，逮王府官僚。"),
   ev("明史", "恭闵帝纪", "本纪/卷四#p58", "text-niutrans-833691c5fbe586ea9276", "result", "primary",
      "秋七月癸酉，燕王棣举兵反，杀布政使张昺、都司谢贵。"),
   ev("明史", "齐泰传", "列传/卷三十三#p30", "text-niutrans-691e560534ee0a7e5b6c", "result", "supporting",
      "兵起，以诛齐泰、黄子澄为名，号其众曰靖难之师。"),
   ev("明史", "恭闵帝纪", "本纪/卷四#p182", "text-niutrans-8cc727214d621ac443cc", "result", "primary",
      "乙丑，燕兵犯金川门，左都督徐增寿谋内应，伏诛。"),
   ev("明史", "恭闵帝纪", "本纪/卷四#p184", "text-niutrans-29163e20ec73b614b6a5", "impact", "primary",
      "宫中火起，帝不知所终。"),
  ],
  "relations_add": [
   {"target_event_id": "event-jingnan-qibing", "relation_type": "causes",
    "description_zh_cn": "削藩激起燕王举兵，是为靖难之役之起"},
  ],
 },
 # ---------------- 4. 东林党争 ----------------
 "ming/event-donglin-dangzheng.yml": {
  "background_zh_cn": "万历间顾宪成罢官归无锡，与弟允成倡修东林书院——宋杨时讲道处——常州知府欧阳东凤与无锡知县林宰为之营构；"
                       "宪成偕同志讲学其中，往往讽议朝政、裁量人物，士大夫闻风而附，由是东林名大著而忌者亦多。",
  "process_zh_cn": "自万历争国本、辛亥京察、李三才之讼，至梃击、红丸、移宫三案，凡救李三才者、争京察者、发科场弊者、抗论张差梃击者、忤魏忠贤者，"
                   "皆被指目为东林，抨击无虚日；御史徐兆魁、乔应甲等力排东林，与齐、楚、浙诸党声势相倚，大臣多畏避之。"
                   "天启间魏忠贤用事，谳汪文言狱，逮杨涟、左光斗、魏大中、周朝瑞、顾大章等，削赵南星等籍，党祸遂烈。",
  "result_zh_cn": "崇祯初定逆案，阉党既黜，然门户之见已深：继任阁臣张至发、薛国观皆不喜东林，所司不敢复奏；"
                  "南明诸朝复以东林、复社与马阮之党相攻，党争与国祚相终始。",
  "impact_zh_cn": "东林由书院讲学而成政治标目，党争自万历延至南明，凡京察、三案、逆案皆以门户为断，人才进退系于党派；"
                  "明代士大夫政治之激化与内阁票拟、言路风宪之败坏于此可见，识者以为明亡之由之一。",
  "people": [
   {"person_name_raw": "顾宪成", "role": "leader", "link_status": "needs_linking",
    "role_zh_cn": "东林领袖：倡修东林书院、讲学议政", "review_note": "major02-H：明史·顾宪成传「宪成与弟允成倡修之」", "person_id": None},
   {"person_name_raw": "杨涟", "role": "supporter", "link_status": "needs_linking",
    "role_zh_cn": "东林名臣：劾魏忠贤，天启间死狱", "review_note": "major02-H：明史·熹宗纪「逮杨涟、左光斗、袁化中、魏大中、周朝瑞、顾大章」", "person_id": None},
   {"person_name_raw": "左光斗", "role": "supporter", "link_status": "needs_linking",
    "role_zh_cn": "东林名臣：与杨涟同被逮死", "review_note": "major02-H：明史·熹宗纪（同上）", "person_id": None},
   {"person_name_raw": "魏忠贤", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "司礼太监：兴党狱、杀东林诸臣", "review_note": "major02-H：明史·顾宪成传「忤魏忠贤者，率指目为东林」", "person_id": None},
   {"person_name_raw": "李三才", "role": "supporter", "link_status": "needs_linking",
    "role_zh_cn": "漕运总督：被劾引发东林党名之起", "review_note": "major02-H：明史「南北言官群击李三才、王元翰，连及里居顾宪成，谓之东林党」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "东林书院", "role": "origin", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "无锡书院：东林之名所自出", "review_note": "major02-H：明史·顾宪成传「邑故有东林书院……宪成与弟允成倡修之」"},
   {"place_name_raw": "无锡", "role": "location", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "顾宪成里居与讲学之地", "review_note": "major02-H：明史·顾宪成传（无锡知县林宰为之营构）"},
   {"place_name_raw": "京师", "role": "capital", "link_status": "needs_linking", "sequence": 3,
    "description_zh_cn": "京察、三案、诏狱所在", "review_note": "major02-H：明史「争辛亥京察者……争移宫、红丸者」"},
  ],
  "evidence": [
   ev("明史", "顾宪成传", "列传/卷一百一十九#p72", "text-niutrans-dd77d03b00fb706d69d6", "background", "primary",
      "邑故有东林书院，宋杨时讲道处也，宪成与弟允成倡修之，常州知府欧阳东凤与无锡知县林宰为之营构。"),
   ev("明史", "顾宪成传", "列传/卷一百一十九#p78", "text-niutrans-55e8be427460301a97e1", "background", "supporting",
      "由是东林名大著，而忌者亦多。"),
   ev("明史", "顾宪成传", "列传/卷一百一十九#p83", "text-niutrans-22dbfbcdbd22058d7394", "process", "supporting",
      "谓浒墅有小河，东林专其税为书院费……会时必谈时政，郡邑行事偶相左，必令改图。"),
   ev("明史", "孙丕扬传", "列传/卷一百一十二#p300", "text-niutrans-552da99b3a075c9742a5", "process", "primary",
      "先是，南北言官群击李三才、王元翰，连及里居顾宪成，谓之东林党。"),
   ev("明史", "孙丕扬传", "列传/卷一百一十二#p302", "text-niutrans-76dacb99ad936a808095", "process", "primary",
      "御史徐兆魁、乔应甲、刘国缙、郑继芳、刘光复、房壮丽，给事中王绍徽，朱一桂、姚宗文、徐绍吉、周永春辈，则力排东林，与宾尹、天飐声势相倚，大臣多畏避之。"),
   ev("明史", "顾宪成传", "列传/卷一百一十九#p89", "text-niutrans-690f95a261933fecf56f", "process", "supporting",
      "凡救三才者，争辛亥京察者，卫国本者，发韩敬科场弊者，请行勘熊廷弼者，抗论张差梃击者，最后争移宫、红丸者，忤魏忠贤者，率指目为东林，抨击无虚日。"),
   ev("明史", "熹宗纪", "本纪/卷二十二#p167", "text-niutrans-15347ceae6adf542f81d", "result", "primary",
      "丁丑，谳汪文言狱，逮杨涟、左光斗、袁化中、魏大中、周朝瑞、顾大章，削尚书赵南星等籍。"),
   ev("明史", "列传", "列传/卷一百七十六#p259", "text-niutrans-dedde78591c660ce1cc9", "impact", "primary",
      "当是时，体仁已前罢，继者张至发、薛国观皆不喜东林，故所司不敢复奏。"),
  ],
 },
 # ---------------- 5. 夺门之变 ----------------
 "ming/event-duomen-zhibian.yml": {
  "background_zh_cn": "景泰元年杨善使瓦剌，也先许上皇归，「先后遣李实、杨善往，卒奉上皇以归，谦力也」；上皇既归，幽居南宫。"
                       "景泰八年正月，景帝病笃，储位未定，武清侯石亨、都督张輗张軏、左都御史杨善、副都御史徐有贞与太监曹吉祥等遂谋拥上皇复辟。",
  "process_zh_cn": "天顺元年（1457年）正月壬午昧爽，石亨、张輗、张軏、杨善、徐有贞、曹吉祥以兵迎帝于南宫，御奉天门，朝百官——是为夺门之变。"
                   "越数日，论夺门迎复功，封石亨忠国公、张軏太平侯、张輗文安伯、杨善兴济伯，曹吉祥嗣子钦都督同知；旋复论功，官舍旗军晋级者凡三千余人。"
                   "都御史萧维桢附会徐有贞，枉杀王文、于谦等，朝局为之一变。",
  "result_zh_cn": "夺门诸臣以功邀宠，曹吉祥有宠颛政，石亨益横；天顺三年后石亨以罪罢，未几有罪下狱死，曹吉祥亦以谋反诛；"
                  "英宗晚年从李贤之言，始悟「夺门」非是，诏诸夺门冒功者许自首改正，是非乃渐明。",
  "impact_zh_cn": "夺门之变以「迎复」之名矫杀社稷之臣，于谦、王文之死为明代第一大冤狱；"
                  "此后天顺一朝宦官曹吉祥、武将石亨相继用事，英宗复辟之局反成内耗之源，明代君臣互信再受重创。",
  "people": [
   {"person_name_raw": "石亨", "role": "leader", "link_status": "needs_linking",
    "role_zh_cn": "武清侯：夺门首谋，封忠国公，后下狱死", "review_note": "major02-H：明史·英宗后纪「石亨有罪下狱，寻死」", "person_id": None},
   {"person_name_raw": "徐有贞", "role": "leader", "link_status": "needs_linking",
    "role_zh_cn": "副都御史：夺门谋主，构陷于谦", "review_note": "major02-H：明史·英宗后纪「副都御史徐有贞」；志「附会徐有贞，枉杀王文、于谦等」", "person_id": None},
   {"person_name_raw": "曹吉祥", "role": "supporter", "link_status": "needs_linking",
    "role_zh_cn": "太监：以夺门功有宠颛政", "review_note": "major02-H：明史·宦官传「振门下曹吉祥复以夺门功，有宠颛政」", "person_id": None},
   {"person_name_raw": "明英宗", "role": "ruler", "link_status": "needs_linking",
    "role_zh_cn": "上皇→英宗：南宫迎复复位", "review_note": "major02-H：明史·英宗后纪「以兵迎帝于南宫，御奉天门，朝百官」", "person_id": None},
   {"person_name_raw": "于谦", "role": "victim", "link_status": "needs_linking",
    "role_zh_cn": "兵部尚书：社稷之臣，为夺门诸臣所枉杀", "review_note": "major02-H：明史·刑法志「都御史萧维桢附会徐有贞，枉杀王文、于谦等」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "南宫", "role": "site", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "上皇幽居之地：夺门迎复处", "review_note": "major02-H：明史·英宗后纪「迎帝于南宫」"},
   {"place_name_raw": "奉天门", "role": "site", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "复位后朝百官之所", "review_note": "major02-H：明史·英宗后纪「御奉天门，朝百官」"},
  ],
  "evidence": [
   ev("明史", "景帝纪", "本纪/卷十一#p100", "text-niutrans-b6090ba2b17e5751ac7d", "background", "supporting",
      "己巳，杨善至瓦剌，也先许上皇归。"),
   ev("明史", "于谦传", "列传/卷五十八#p135", "text-niutrans-0776e919fb19e36cca08", "background", "primary",
      "先后遣李实、杨善往。卒奉上皇以归，谦力也。"),
   ev("明史", "英宗后纪", "本纪/卷十二#p2", "text-niutrans-829b4747cd75ea41562b", "process", "primary",
      "天顺元年春正月壬午，昧爽，武清侯石亨，都督张輗、张軏，左都御史杨善，副都御史徐有贞，太监曹吉祥以兵迎帝于南宫，御奉天门，朝百官。"),
   ev("明史", "英宗后纪", "本纪/卷十二#p8", "text-niutrans-f16d68c892d35b54b758", "result", "primary",
      "论夺门迎复功，封石亨忠国公，张軏太平侯，张輗文安伯，杨善兴济伯，曹吉祥嗣子钦都督同知。"),
   ev("明史", "刑法志", "志/卷七十#p411", "text-niutrans-e1410b155957864b005f", "result", "primary",
      "都御史萧维桢附会徐有贞，枉杀王文、于谦等。"),
   ev("明史", "宦官传", "列传/卷一百九十二#p134", "text-niutrans-c7374dad5ac5e91d9708", "result", "supporting",
      "而振门下曹吉祥复以夺门功，有宠颛政。"),
   ev("明史", "英宗后纪", "本纪/卷十二#p91", "text-niutrans-78b12414554e26131cb3", "impact", "supporting",
      "庚午，石亨以罪罢。"),
   ev("明史", "英宗后纪", "本纪/卷十二#p97", "text-niutrans-575c5a96ffbd6f7a3372", "impact", "primary",
      "癸卯，石亨有罪下狱，寻死。"),
   ev("明史", "宦官传", "列传/卷一百九十二#p154", "text-niutrans-1acb884078f0a6bec660", "impact", "supporting",
      "及李贤力言夺门非是，始大悟，疏吉祥。"),
  ],
 },
 # ---------------- 6. 后金建立 ----------------
 "ming/event-houjin-jianguo.yml": {
  "background_zh_cn": "建州三卫自永乐以来为明羁縻，天顺间边将即奏「建州三卫都督私与朝鲜结，恐为中国患」；建州长童仓尝避居朝鲜界而复还建州。"
                       "万历间建州都督王杲以索降人不得，入掠抚顺，守将贾汝翼诘责之——建州与明之边衅渐起，努尔哈赤部遂乘之而兴。",
  "process_zh_cn": "万历四十四年（1616年）努尔哈赤于赫图阿拉称汗建元，语料以「大清兵」纪其事：万历四十六年四月甲辰，大清兵克抚顺城，千总王命印死之；"
                   "闰月，杨镐为兵部左侍郎兼右佥都御史，经略辽东；四十七年三月，杜松遇大清兵于吉林崖，战死。"
                   "兴京之号后世犹存——清史稿记「诏以沈阳为天眷盛京，赫图阿拉城为天眷兴京」。",
  "result_zh_cn": "抚顺既克，明廷以杨镐经略辽东，四路出师而萨尔浒大败，杜松战死；六月大清兵克开原，马林败没，"
                  "乃以大理寺丞熊廷弼为兵部右侍郎兼右佥都御史经略辽东——辽东战守自此为明代第一重务。",
  "impact_zh_cn": "后金既立，辽东攻守之势逆转：萨尔浒一战明军主力尽丧，开原、铁岭相继陷落，明由进攻转为守御；"
                  "二十余年间遂有清兵入关、明清易代之事。明末加派辽饷亦自此始，民困而流寇起，内外交病。",
  "people": [
   {"person_name_raw": "努尔哈赤", "role": "leader", "link_status": "needs_linking",
    "role_zh_cn": "建州左卫首领：称汗建后金（语料以「大清」纪之）", "review_note": "major02-H：语料未见称汗直接记载；以建州源流（明史·外国）与抚顺、萨尔浒诸役为锚", "person_id": None},
   {"person_name_raw": "杨镐", "role": "commander", "link_status": "needs_linking",
    "role_zh_cn": "兵部侍郎：经略辽东、四路出师", "review_note": "major02-H：明史·神宗纪「杨镐为兵部左侍郎兼右佥都御史，经略辽东」", "person_id": None},
   {"person_name_raw": "杜松", "role": "commander", "link_status": "needs_linking",
    "role_zh_cn": "总兵官：萨尔浒之役战死", "review_note": "major02-H：明史·神宗纪「杜松遇大清兵于吉林崖，战死」", "person_id": None},
   {"person_name_raw": "熊廷弼", "role": "commander", "link_status": "needs_linking",
    "role_zh_cn": "经略辽东：开原陷后受命守辽", "review_note": "major02-H：明史·神宗纪「大理寺丞熊廷弼为兵部右侍郎兼右佥都御史，经略辽东」", "person_id": None},
   {"person_name_raw": "王杲", "role": "historical", "link_status": "needs_linking",
    "role_zh_cn": "建州都督：入掠抚顺，建州与明边衅之始", "review_note": "major02-H：明史「建州都督王杲以索降人不得，入掠抚顺」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "赫图阿拉", "role": "capital", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "后金兴京：称汗建元之地（清史稿作天眷兴京）", "review_note": "major02-H：清史稿·太宗本纪一「赫圖阿喇城为天眷興京」"},
   {"place_name_raw": "抚顺", "role": "battlesite", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "后金克明之城：1618年陷落", "review_note": "major02-H：明史·神宗纪「大清兵克抚顺城」"},
   {"place_name_raw": "萨尔浒", "role": "battlesite", "link_status": "needs_linking", "sequence": 3,
    "description_zh_cn": "决战地：明四路之师败没", "review_note": "major02-H：明史·神宗纪「杜松遇大清兵于吉林崖，战死」"},
   {"place_name_raw": "开原", "role": "battlesite", "link_status": "needs_linking", "sequence": 4,
    "description_zh_cn": "辽东重镇：1619年陷落", "review_note": "major02-H：明史·神宗纪「大清兵克开原，马林败没」"},
  ],
  "evidence": [
   ev("明史", "外国传", "列传/卷二百零八#p189", "text-niutrans-d8779b8bc8a3623384ea", "background", "supporting",
      "天顺三年，边将奏，有建州三卫都督私与朝鲜结，恐为中国患。"),
   ev("明史", "列传", "列传/卷一百一十#p253", "text-niutrans-86e822ecc30adf384738", "background", "primary",
      "秋，建州都督王杲以索降人不得，入掠抚顺，守将贾汝翼诘责之。"),
   ev("明史", "神宗纪", "本纪/卷二十一#p279", "text-niutrans-262f1b2faec3b61675d1", "process", "primary",
      "夏四月甲辰，大清兵克抚顺城，千总王命印死之。"),
   ev("明史", "神宗纪", "本纪/卷二十一#p281", "text-niutrans-9fdc960957ffbff9aa4a", "process", "supporting",
      "闰月庚申，杨镐为兵部左侍郎兼右佥都御史，经略辽东。"),
   ev("明史", "神宗纪", "本纪/卷二十一#p295", "text-niutrans-9415b08cc2033d7dd98b", "result", "primary",
      "三月甲早，杜松遇大清兵于吉林崖，战死。"),
   ev("明史", "神宗纪", "本纪/卷二十一#p300", "text-niutrans-c2e16e42017a6184e1fc", "result", "supporting",
      "六月丁卯，大清兵克开原，马林败没。"),
   ev("明史", "神宗纪", "本纪/卷二十一#p301", "text-niutrans-1794875726f0dbe3f8b0", "impact", "primary",
      "癸酉，大理寺丞熊廷弼为兵部右侍郎兼右佥都御史，经略辽东。"),
   ev("清史稿", "太宗本纪一", "本纪/太宗本纪一#p89", "text-wikisource-b4a482a3d796e4a11e74", "impact", "supporting",
      "詔以瀋陽为「天眷盛京」，赫圖阿喇城为「天眷興京」。", "兴京之名出于赫图阿拉，后金发祥之证"),
  ],
  "relations_add": [
   {"target_event_id": "event-saerhu-zhizhan", "relation_type": "precedes",
    "description_zh_cn": "后金既立，萨尔浒之战为明清易代关键一役"},
  ],
 },
 # ---------------- 7. 东南沿海倭患 ----------------
 "ming/event-dongnan-wokou.yml": {
  "background_zh_cn": "嘉靖间倭患大起：海贼汪直纠倭寇濒海诸郡，自嘉靖三十一年二月倭犯温州始，通、泰、青、徐以至嘉兴、苏州皆被其害；"
                       "三十三年官军围倭于南沙五阅月不克，倭溃围出转掠苏、松，东南财赋之地为之骚然。",
  "process_zh_cn": "明廷先以南京兵部尚书张经总督军务讨倭，继用巡抚侍郎胡宗宪总督军务；胡宗宪用徐海、王直降将之策，"
                   "三十四年李遂、胡宗宪破倭于刘家庄。後复征俞大猷、戚继光、刘显诸将合击，破之——"
                   "戚继光练义乌兵、创鸳鸯阵，与俞大猷复兴化城，共破海倭，倭势始衰。",
  "result_zh_cn": "东南倭寇次第荡平：胡宗宪破倭于刘家庄，戚继光、俞大猷破倭于福建、兴化，"
                  "福建巡抚游震得以浙江温、处与福宁接壤、倭所出没，请进戚继光为副总兵守之，海防之制由此重整。",
  "impact_zh_cn": "倭患既平，戚继光等列海防善后事、修城练兵，明代东南海防为一变；"
                  "然倭乱起于海禁与互市之失，隆庆以后部分开海、银钱流通，东南海上之势力遂另开新局。",
  "people": [
   {"person_name_raw": "胡宗宪", "role": "commander", "link_status": "needs_linking",
    "role_zh_cn": "浙直总督：总督军务讨倭、破倭刘家庄", "review_note": "major02-H：明史·世宗纪「巡抚侍郎胡宗宪总督军务，讨倭」", "person_id": None},
   {"person_name_raw": "戚继光", "role": "commander", "link_status": "needs_linking",
    "role_zh_cn": "参将→副总兵：练新军、破海倭、列海防善后事", "review_note": "major02-H：明史「宜进戚继光为副总兵，守之」", "person_id": None},
   {"person_name_raw": "俞大猷", "role": "commander", "link_status": "needs_linking",
    "role_zh_cn": "福建总兵官：与戚继光复兴化城、共破海倭", "review_note": "major02-H：明史「大猷寻擢福建总兵官，与戚继光复兴化城，共破海倭」", "person_id": None},
   {"person_name_raw": "张经", "role": "commander", "link_status": "needs_linking",
    "role_zh_cn": "南京兵部尚书：总督军务讨倭", "review_note": "major02-H：明史·世宗纪「南京兵部尚书张经总督军务，讨倭」", "person_id": None},
   {"person_name_raw": "汪直", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "海贼：纠倭寇濒海诸郡", "review_note": "major02-H：明史·世宗纪「海贼汪直纠倭寇濒海诸郡」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "浙江", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "倭患最烈之区：温州、嘉兴、南沙皆在焉", "review_note": "major02-H：明史·世宗纪「倭犯温州」「倭犯嘉兴」"},
   {"place_name_raw": "苏松", "role": "battlesite", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "倭溃围后转掠之地（苏州、松江）", "review_note": "major02-H：明史·世宗纪「倭溃围出，转掠苏、松」"},
   {"place_name_raw": "福建", "role": "front", "link_status": "needs_linking", "sequence": 3,
    "description_zh_cn": "倭所出没之处：戚继光以副总兵守之", "review_note": "major02-H：明史「浙江温、处与福宁接壤，倭所出没，宜进戚继光为副总兵，守之」"},
   {"place_name_raw": "兴化", "role": "battlesite", "link_status": "needs_linking", "sequence": 4,
    "description_zh_cn": "戚继光、俞大猷收复之城", "review_note": "major02-H：明史「与戚继光复兴化城，共破海倭」"},
  ],
  "evidence": [
   ev("明史", "世宗纪", "本纪/卷十八#p141", "text-niutrans-03f68b76d7c17e8ffa96", "background", "primary",
      "闰三月，海贼汪直纠倭寇濒海诸郡，至六月始去。"),
   ev("明史", "世宗纪", "本纪/卷十八#p156", "text-niutrans-99630fa8de96ad131eff", "process", "primary",
      "戊辰，官军围倭于南沙，五阅月不克，倭溃围出，转掠苏、松。"),
   ev("明史", "世宗纪", "本纪/卷十八#p160", "text-niutrans-3216dbcc538f3a045a61", "process", "supporting",
      "乙亥，倭犯嘉兴，都司周应桢等战死。"),
   ev("明史", "世宗纪", "本纪/卷十八#p163", "text-niutrans-e3dbf71dc6531d584562", "process", "supporting",
      "丁巳，南京兵部尚书张经总督军务，讨倭。"),
   ev("明史", "世宗纪", "本纪/卷十八#p197", "text-niutrans-8d71df7b061b031aaa48", "result", "primary",
      "巡抚侍郎胡宗宪总督军务，讨倭。"),
   ev("明史", "世宗纪", "本纪/卷十八#p250", "text-niutrans-70231470a9b1df573eb1", "result", "primary",
      "秋八月己未，李遂、胡宗宪破倭于刘家庄。"),
   ev("明史", "外国传", "列传/卷二百一十#p356", "text-niutrans-204f6e8bfe79ffce7824", "result", "supporting",
      "至是，远近震动，亟征俞大猷、戚继光、刘显诸将合击，破之。"),
   ev("明史", "职官志", "志/卷六十七#p235", "text-niutrans-e0896ad927a0a3d1217f", "impact", "primary",
      "福建巡抚都御史游震得言：浙江温、处与福宁接壤，倭所出没，宜进戚继光为副总兵，守之。"),
   ev("明史", "列传", "列传/卷一百一十五#p64", "text-niutrans-a75600e3ebe0a6dcf32f", "impact", "supporting",
      "与总兵官戚继光合兵破倭，因列海防善后事。"),
  ],
 },
 # ---------------- 8. 大礼议 ----------------
 "ming/event-daliyi.yml": {
  "background_zh_cn": "正德十六年武宗崩，无嗣，慈寿皇太后与大学士杨廷和定策，遣官以遗诏迎兴献王世子于兴邸；世子父兴献王祐杬，国安陆，正德十四年薨。"
                       "帝即位未几，命礼臣集议兴献王封号，礼官援宋程颐议濮王礼，议考孝宗、称兴献王皇叔父，帝不允；杨廷和等抗疏力争，皆不听。",
  "process_zh_cn": "进士张璁上疏言「继统不继嗣，请尊崇所生，立兴献王庙于京师」，帝得疏大喜曰「此论出，吾父子获全矣」；璁又著《大礼或问》上之，帝遂连驳礼官疏。"
                   "十月，追尊父兴献王为兴献帝、祖母邵氏为皇太后、母妃为兴献后；既而命称孝宗皇考、兴献帝后为本生父母；"
                   "杨廷和以议礼不合致仕，帝复追尊兴献帝为本生皇考恭穆献皇帝，大赦天下。",
  "result_zh_cn": "大礼议以帝意得伸告终：兴献帝后尊号既上，杨廷和等持礼之臣或罢或贬；张璁、桂萼、方献夫等以议礼骤贵，夏言继之，"
                  "成为嘉靖前期内阁之新局——议礼一事遂为嘉靖朝人事更迭之枢机。",
  "impact_zh_cn": "大礼议表面争「继统」「继嗣」之礼，实为嘉靖帝确立皇权自主、重组外廷之契机：持礼旧臣去而议礼新贵进，"
                  "内阁与言路之势为之一变；此后世宗以制礼作乐自任，明代礼制与政治之关系愈密。",
  "people": [
   {"person_name_raw": "明世宗", "role": "ruler", "link_status": "needs_linking",
    "role_zh_cn": "兴献王世子→世宗：以议礼定尊号、伸皇权", "review_note": "major02-H：明史·世宗纪「追尊父兴献王为兴献帝」", "person_id": None},
   {"person_name_raw": "张璁", "role": "leader", "link_status": "needs_linking",
    "role_zh_cn": "进士→议礼新贵：首倡继统不继嗣", "review_note": "major02-H：明史·张璁传「帝方扼廷议，得璁疏大喜」", "person_id": None},
   {"person_name_raw": "杨廷和", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "大学士：持礼力争、议不合致仕", "review_note": "major02-H：明史·世宗纪「杨廷和等抗疏力争，皆不听」；「二月丙午，杨廷和致仕」", "person_id": None},
   {"person_name_raw": "兴献王", "role": "historical", "link_status": "needs_linking",
    "role_zh_cn": "世宗生父：卒后追尊兴献帝、恭穆献皇帝", "review_note": "major02-H：明史·世宗纪「父兴献王祐杬，国安陆，正德十四年薨」", "person_id": None},
   {"person_name_raw": "毛澄", "role": "official", "link_status": "needs_linking",
    "role_zh_cn": "礼部尚书：受遗诏迎王、主礼臣之议", "review_note": "major02-H：明史·世宗纪「礼部尚书毛澄，以遗诏迎王于兴邸」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "安陆", "role": "origin", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "兴献王藩国：世宗所自出", "review_note": "major02-H：明史·世宗纪「父兴献王祐杬，国安陆」"},
   {"place_name_raw": "京师", "role": "capital", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "议礼之地：礼臣集议、兴献王庙立于京师", "review_note": "major02-H：明史·世宗纪「命礼臣集议兴献王封号」"},
  ],
  "evidence": [
   ev("明史", "世宗纪", "本纪/卷十七#p3", "text-niutrans-b11ebdd20c00962a350a", "background", "supporting",
      "父兴献王祐杬，国安陆，正德十四年薨。"),
   ev("明史", "世宗纪", "本纪/卷十七#p6", "text-niutrans-dc74473e73b38c3a710b", "background", "primary",
      "丙寅，武宗崩，无嗣，慈寿皇太后与大学士杨廷和定策，遣太监谷大用、韦彬、张锦，大学士梁储，定国公徐光祚，驸马都尉崔元，礼部尚书毛澄，以遗诏迎王于兴邸。"),
   ev("明史", "世宗纪", "本纪/卷十七#p18", "text-niutrans-4dc86c98b3098acda0b2", "process", "primary",
      "戊申，命礼臣集议兴献王封号。"),
   ev("明史", "世宗纪", "本纪/卷十七#p29", "text-niutrans-9be960c197ae8c0a7275", "process", "primary",
      "秋七月壬子，进士张璁言，继统不继嗣，请尊崇所生，立兴献王庙于京师。"),
   ev("明史", "世宗纪", "本纪/卷十七#p30", "text-niutrans-a28b66ada193183bb090", "process", "supporting",
      "初，礼臣议考孝宗，改称兴献王皇叔父，援宋程颐议濮王礼以进，不允。"),
   ev("明史", "世宗纪", "本纪/卷十七#p32", "text-niutrans-93e54744160c49a49fd5", "process", "supporting",
      "杨廷和等抗疏力争，皆不听。"),
   ev("明史", "张璁传", "列传/卷八十四#p26", "text-niutrans-ef4a6a27c01bf0a2829f", "process", "supporting",
      "帝方扼廷议，得璁疏大喜，曰：此论出，吾父子获全矣。"),
   ev("明史", "世宗纪", "本纪/卷十七#p39", "text-niutrans-53d02d39cdf2433e9ac2", "result", "primary",
      "冬十月己卯朔，追尊父兴献王为兴献帝，祖母宪宗贵妃邵氏为皇太后，母妃为兴献后。"),
   ev("明史", "世宗纪", "本纪/卷十七#p81", "text-niutrans-de10629a411828e79fae", "result", "supporting",
      "二月丙午，杨廷和致仕。"),
   ev("明史", "世宗纪", "本纪/卷十七#p87", "text-niutrans-9c9719d77a7f4273ef16", "impact", "primary",
      "癸丑，追尊兴献帝为本生皇考恭穆献皇帝，大赦。"),
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
        rel_add = block.pop("relations_add", None)
        body = dict(block)
        if rel_add:
            base = data.get("relations") or []
            have = {(r.get("target_event_id"), r.get("relation_type")) for r in base}
            for r in rel_add:
                if (r.get("target_event_id"), r.get("relation_type")) not in have:
                    base.append(r)
            body = {"relations": base, **body}
            data.pop("relations", None)
        with path.open("a", encoding="utf-8") as s:
            s.write("\n" + yaml.safe_dump(body, allow_unicode=True, sort_keys=False,
                                          default_flow_style=False, width=10**6))
        applied += 1
        print(f"appended {rel}")
    print(f"total: {applied}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
