"""Major Batch 01 · Cluster D：汉武帝时代（9 事件）。"""
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
        "review_note": f"major01-D：{work}源引文：「{quote}」；claim_field={field}；anchor=段落精确锚。{note}"}

SJ = "史记"; HS = "汉书"
BLOCKS = {
 "qin_han/event-hanwudi-jiwei.yml": {
  "background_zh_cn": "景帝崩，太子彻即位；建元元年冬十月即诏丞相、御史、列侯等「举贤良方正直言极谏之士」——新政自求贤始。",
  "process_zh_cn": "甲子，太子即皇帝位，尊皇太后窦氏曰太皇太后、皇后曰皇太后。",
  "result_zh_cn": "建元元年诏举贤良方正直言极谏之士——武帝初政即开求言之路。",
  "impact_zh_cn": "「及今上即位，赵绾、王臧之属明儒学，而上亦乡之，于是招方正贤良文学之士」——儒术之士由此进入汉廷，一个新时代开启。",
  "people": [
   {"person_name_raw": "汉武帝", "role": "monarch", "link_status": "needs_linking",
    "role_zh_cn": "太子刘彻：即皇帝位", "review_note": "major01-D：汉书·武帝纪「甲子，太子即皇帝位」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "长安", "role": "capital", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "武帝即位与初政所在", "review_note": "major01-D：汉书·武帝纪（建元元年诏）"},
  ],
  "evidence": [
   ev(HS, "武帝纪", "纪/武帝纪#p6", "text-niutrans-90b9bc33119be6d6e475", "background", "primary", "建元元年冬十月，诏丞相、御史、列侯……举贤良方正直言极谏之士。"),
   ev(HS, "武帝纪", "纪/武帝纪#p4", "text-niutrans-594510be964b40c886d9", "process", "primary", "甲子，太子即皇帝位，尊皇太后窦氏曰太皇太后，皇后曰皇太后。"),
   ev(SJ, "儒林列传", "七十列传/儒林列传#p27", "text-niutrans-b1be8ba5074e23731557", "impact", "primary", "及今上即位，赵绾、王臧之属明儒学，而上亦乡之，於是招方正贤良文学之士。"),
  ],
 },
 "qin_han/event-dongzhongshu-cedui.yml": {
  "background_zh_cn": "武帝即位，举贤良文学之士前后百数，而仲舒以贤良对策焉——天人三策对答于廷。",
  "process_zh_cn": "对策考问：「陛下有明德嘉道……故举贤良方正之士，论议考问，将欲兴仁谊之林德，明帝王之法制，建太平之道也」。",
  "result_zh_cn": "对策归于一统之义：「《春秋》大一统者，天地之常经，古今之通谊也」——尊儒更化之论自此立。",
  "impact_zh_cn": "「天人之征，古今之道也」——董仲舒援天道以论政，儒学由是上升为汉家治国之学。",
  "people": [
   {"person_name_raw": "董仲舒", "role": "official", "link_status": "needs_linking",
    "role_zh_cn": "贤良对策者：大一统与天人论", "review_note": "major01-D：汉书·董仲舒传「仲舒以贤良对策焉」", "person_id": None},
   {"person_name_raw": "汉武帝", "role": "monarch", "link_status": "needs_linking",
    "role_zh_cn": "策问之君：举贤良、垂问天人", "review_note": "major01-D：汉书·董仲舒传「故朕垂问乎天人之应」", "person_id": None},
  ],
  "places": [],
  "evidence": [
   ev(HS, "董仲舒传", "传/董仲舒传#p6", "text-niutrans-a6fc98d684dbc7ac1f8b", "background", "primary", "武帝即位，举贤良文学之士前后百数，而仲舒以贤良对策焉。"),
   ev(HS, "董仲舒传", "传/董仲舒传#p232", "text-niutrans-79f05f7321194df103c3", "process", "primary", "故举贤良方正之士，论议考问，将欲兴仁谊之林德，明帝王之法制，建太平之道也。"),
   ev(HS, "董仲舒传", "传/董仲舒传#p259", "text-niutrans-38112ef1fd37b21e7d0c", "result", "primary", "《春秋》大一统者，天地之常经，古今之通谊也。"),
   ev(HS, "董仲舒传", "传/董仲舒传#p191", "text-niutrans-47e68f4aeaf1c09667a4", "impact", "primary", "繇此言之，天人之征，古今之道也。"),
  ],
 },
 "qin_han/event-wujing-boshi.yml": {
  "background_zh_cn": "「及今上即位，赵绾、王臧之属明儒学，而上亦乡之，于是招方正贤良文学之士」——尊儒之政次第推行。",
  "process_zh_cn": "置《五经》博士——以五经立学官。",
  "result_zh_cn": "为博士官置弟子员：「郡国县道邑有好文学，敬长上……二千石谨察可者，当与计偕，诣太常，得受业如弟子」。",
  "impact_zh_cn": "「一岁皆辄试，能通一艺以上，补文学掌故缺」——通经入仕之途开启，儒术与利禄结合，五经之学遂为国家教育正轨。",
  "people": [],
  "places": [
   {"place_name_raw": "长安", "role": "capital", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "太常与博士官所在，受业弟子诣之", "review_note": "major01-D：史记·儒林列传「诣太常，得受业如弟子」"},
  ],
  "evidence": [
   ev(SJ, "儒林列传", "七十列传/儒林列传#p27", "text-niutrans-b1be8ba5074e23731557", "background", "primary", "及今上即位，赵绾、王臧之属明儒学，而上亦乡之。"),
   ev(HS, "武帝纪", "纪/武帝纪#p34", "text-niutrans-7c989dc26d0e5a0244c1", "process", "primary", "置《五经》博士。"),
   ev(SJ, "儒林列传", "七十列传/儒林列传#p47", "text-niutrans-b3753f537d881be45a0b", "result", "primary", "二千石謹察可者，当与计偕，诣太常，得受业如弟子。"),
   ev(SJ, "儒林列传", "七十列传/儒林列传#p48", "text-niutrans-d6295328ae2de33fdf39", "impact", "primary", "一岁皆辄试，能通一艺以上，补文学掌故缺。"),
  ],
 },
 "qin_han/event-mayi-zhi-mou.yml": {
  "background_zh_cn": "汉使马邑下人聂翁壹奸兰出物与匈奴交，「详为卖马邑城以诱单于」——马邑之谋始。",
  "process_zh_cn": "汉伏兵三十余万马邑旁，御史大夫韩安国为护军，护四将军以伏单于；单于信之、贪马邑财物，乃以十万骑入武州塞。",
  "result_zh_cn": "单于入汉塞未至马邑百余里，见畜布野而无人牧者、怪之，乃攻亭；「汉兵约单于入马邑而纵，单于不至，以故汉兵无所得」——谋泄无功。",
  "impact_zh_cn": "「自马邑军后五年之秋，汉使四将军各万骑击胡关市下」——马邑之谋虽无功，汉匈和亲之局终结，汉对匈奴转入全面战争。",
  "people": [
   {"person_name_raw": "聂翁壹", "role": "supporter", "link_status": "needs_linking",
    "role_zh_cn": "马邑人：诈卖马邑城诱单于", "review_note": "major01-D：史记·匈奴列传「汉使马邑下人聂翁壹奸兰出物与匈奴交」", "person_id": None},
   {"person_name_raw": "韩安国", "role": "official", "link_status": "needs_linking",
    "role_zh_cn": "御史大夫：护军伏单于", "review_note": "major01-D：史记·匈奴列传「御史大夫韩安国为护军」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "马邑", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "设伏诱敌之地", "review_note": "major01-D：史记·匈奴列传「汉伏兵三十馀万马邑旁」"},
  ],
  "evidence": [
   ev(SJ, "匈奴列传", "七十列传/匈奴列传#p244", "text-niutrans-da0fa8b5ac0ebfa8f86f", "background", "primary", "汉使马邑下人聂翁壹奸兰出物与匈奴交，详为卖马邑城以诱单于。"),
   ev(SJ, "匈奴列传", "七十列传/匈奴列传#p246", "text-niutrans-034a0705e43566b5eea4", "process", "primary", "汉伏兵三十馀万马邑旁，御史大夫韩安国为护军。"),
   ev(SJ, "匈奴列传", "七十列传/匈奴列传#p247", "text-niutrans-1cf362ae7334f11aed28", "result", "primary", "单于既入汉塞，未至马邑百馀里，见畜布野而无人牧者，怪之，乃攻亭。"),
   ev(SJ, "匈奴列传", "七十列传/匈奴列传#p253", "text-niutrans-1efa0c0c8cae477a2622", "result", "supporting", "汉兵约单于入马邑而纵，单于不至，以故汉兵无所得。"),
   ev(SJ, "匈奴列传", "七十列传/匈奴列传#p258", "text-niutrans-cbead7ca537f1774766d", "impact", "primary", "自马邑军后五年之秋，汉使四将军各万骑击胡关市下。"),
  ],
 },
 "qin_han/event-weiqing-ji-longcheng.yml": {
  "background_zh_cn": "元光五年，青为车骑将军击匈奴、出上谷；公孙贺出云中、公孙敖出代郡、李广出雁门——军各万骑，四路并出。",
  "process_zh_cn": "青至茏城，斩首虏数百——汉军直捣匈奴祭天圣地。",
  "result_zh_cn": "其秋，青复为车骑将军出雁门，三万骑击匈奴，斩首虏数千人——连战有功。",
  "impact_zh_cn": "四将军出塞为汉对匈奴首次大规模主动出击；卫青以龙城首功崭露头角，汉军新一代将领由此登上战局。",
  "people": [
   {"person_name_raw": "卫青", "role": "supporter", "link_status": "needs_linking",
    "role_zh_cn": "车骑将军：首战龙城", "review_note": "major01-D：史记·卫将军骠骑列传「青至茏城，斩首虏数百」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "茏城", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "匈奴祭天处，卫青首战所向", "review_note": "major01-D：史记·卫将军骠骑列传「青至茏城」"},
   {"place_name_raw": "上谷", "role": "frontier", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "卫青出塞之地", "review_note": "major01-D：史记·卫将军骠骑列传「击匈奴，出上谷」"},
  ],
  "evidence": [
   ev(SJ, "卫将军骠骑列传", "七十列传/卫将军骠骑列传#p24", "text-niutrans-2df90b1b63672322cebd", "background", "primary", "元光五年，青为车骑将军，击匈奴，出上谷……军各万骑。"),
   ev(SJ, "卫将军骠骑列传", "七十列传/卫将军骠骑列传#p25", "text-niutrans-138a493436ee48f18240", "process", "primary", "青至茏城，斩首虏数百。"),
   ev(SJ, "卫将军骠骑列传", "七十列传/卫将军骠骑列传#p29", "text-niutrans-c706e5c1b4d94b660522", "result", "primary", "其秋，青为车骑将军，出雁门，三万骑击匈奴，斩首虏数千人。"),
   ev(SJ, "卫将军骠骑列传", "七十列传/卫将军骠骑列传#p24", "text-niutrans-2df90b1b63672322cebd", "impact", "primary", "军各万骑。", "四路出击之格局，卫青自此为汉军主将"),
  ],
 },
 "qin_han/event-henan-zhizhan.yml": {
  "background_zh_cn": "其三年五月，匈奴右贤王入居河南地，侵盗上郡葆塞蛮夷、杀略人民——河套之患再起。",
  "process_zh_cn": "车骑将军卫青度西河至高阙，获首虏二千三百级，「遂西定河南地，按榆溪旧塞，绝梓领，梁北河……全甲兵而还，益封青三千户」。",
  "result_zh_cn": "使苏建筑朔方城——河套既复，筑朔方以为北边重镇。",
  "impact_zh_cn": "「匈奴右贤王怨汉夺之河南地而筑朔方，数为寇，盗边」——河南之战开汉匈河套拉锯，朔方郡成为此后汉军北出的基地。",
  "people": [
   {"person_name_raw": "卫青", "role": "supporter", "link_status": "needs_linking",
    "role_zh_cn": "车骑将军：西定河南地", "review_note": "major01-D：史记·卫将军骠骑列传「遂西定河南地」", "person_id": None},
   {"person_name_raw": "苏建", "role": "supporter", "link_status": "needs_linking",
    "role_zh_cn": "校尉→平陵侯：建筑朔方城", "review_note": "major01-D：史记·卫将军骠骑列传「使建筑朔方城」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "河南地", "role": "region", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "河套地区：卫青所复", "review_note": "major01-D：史记·卫将军骠骑列传「遂西定河南地」"},
   {"place_name_raw": "朔方", "role": "city", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "筑城置郡，北边重镇", "review_note": "major01-D：史记·卫将军骠骑列传「使建筑朔方城」"},
  ],
  "evidence": [
   ev(SJ, "匈奴列传", "七十列传/匈奴列传#p143", "text-niutrans-6f29b7ed588ce7a8e437", "background", "primary", "其三年五月，匈奴右贤王入居河南地，侵盗上郡葆塞蛮夷。"),
   ev(SJ, "卫将军骠骑列传", "七十列传/卫将军骠骑列传#p38", "text-niutrans-7941dd34fd8468eae6a4", "process", "primary", "遂西定河南地，按榆谿旧塞……全甲兵而还，益封青三千户。"),
   ev(SJ, "卫将军骠骑列传", "七十列传/卫将军骠骑列传#p34", "text-niutrans-b367a327fad06293488f", "result", "primary", "使建筑朔方城。"),
   ev(SJ, "匈奴列传", "七十列传/匈奴列传#p280", "text-niutrans-f8ddbfdc6687fb1073a0", "impact", "primary", "匈奴右贤王怨汉夺之河南地而筑朔方，数为寇，盗边。"),
  ],
 },
 "qin_han/event-hexi-zhizhan.yml": {
  "background_zh_cn": "其明年春，汉使骠骑将军霍去病将万骑出陇西，过焉支山千余里击匈奴，得胡首虏万八千余级，破得休屠王祭天金人。",
  "process_zh_cn": "其夏，骠骑将军复与合骑侯数万骑出陇西、北地二千里，击匈奴——纵深奔袭。",
  "result_zh_cn": "浑邪王杀休屠王，并将其众降汉——河西匈奴主力归降。",
  "impact_zh_cn": "河西既下，匈奴右臂既断，汉通西域之走廊开辟；「金城、河西并南山至盐泽空无匈奴」之局自此成。",
  "people": [
   {"person_name_raw": "霍去病", "role": "supporter", "link_status": "needs_linking",
    "role_zh_cn": "骠骑将军：两出陇西、破休屠王", "review_note": "major01-D：史记·匈奴列传「骠骑将军去病将万骑出陇西」", "person_id": None},
   {"person_name_raw": "浑邪王", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "匈奴王：杀休屠王、将其众降汉", "review_note": "major01-D：史记·匈奴列传「浑邪王杀休屠王，并将其众降汉」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "陇西", "role": "frontier", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "霍去病出塞之地", "review_note": "major01-D：史记·匈奴列传「出陇西」"},
   {"place_name_raw": "焉支山", "role": "battlesite", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "霍去病过山千里击匈奴处", "review_note": "major01-D：史记·匈奴列传「过焉支山千馀里」"},
  ],
  "evidence": [
   ev(SJ, "匈奴列传", "七十列传/匈奴列传#p293", "text-niutrans-2b69f13ad22e409e76ff", "background", "primary", "其明年春，汉使骠骑将军去病将万骑出陇西，过焉支山千馀里，击匈奴，得胡首虏万八千馀级，破得休屠王祭天金人。"),
   ev(SJ, "匈奴列传", "七十列传/匈奴列传#p294", "text-niutrans-77ab4a4c6102062ce235", "process", "primary", "其夏，骠骑将军复与合骑侯数万骑出陇西、北地二千里，击匈奴。"),
   ev(SJ, "匈奴列传", "七十列传/匈奴列传#p303", "text-niutrans-4e5f72954224d970050c", "result", "primary", "浑邪王杀休屠王，并将其众降汉。"),
   ev(SJ, "匈奴列传", "七十列传/匈奴列传#p303", "text-niutrans-4e5f72954224d970050c", "impact", "primary", "并将其众降汉。", "河西走廊入汉，通西域之路自此开"),
  ],
 },
 "qin_han/event-zhangqian-chuxi-1.yml": {
  "background_zh_cn": "「始月氏居敦煌、祁连间，及为匈奴所败，乃远去」——月氏与匈奴世仇，汉欲联之。",
  "process_zh_cn": "「道必更匈奴中，乃募能使者」；骞以郎应募，使月氏，与堂邑氏胡奴甘父俱出陇西，经匈奴被执，留十余岁而后得脱。",
  "result_zh_cn": "大宛以为然，遣骞，为发导绎，抵康居，康居传致大月氏——张骞身所至者大宛、大月氏、大夏、康居，具为天子言之。",
  "impact_zh_cn": "「然张骞凿空，其后使往者皆称博望侯，以为质于外国，外国由此信之」——凿空西域，丝绸之路由此开启。",
  "people": [
   {"person_name_raw": "张骞", "role": "envoy", "link_status": "needs_linking",
    "role_zh_cn": "郎官→博望侯：首使月氏、凿空西域", "review_note": "major01-D：史记·大宛列传「骞以郎应募，使月氏」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "月氏", "role": "region", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "出使目的地（大月氏）", "review_note": "major01-D：史记·大宛列传「及为匈奴所败，乃远去」"},
   {"place_name_raw": "陇西", "role": "frontier", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "出使之起点", "review_note": "major01-D：史记·大宛列传「俱出陇西」"},
   {"place_name_raw": "大宛", "role": "region", "link_status": "needs_linking", "sequence": 3,
    "description_zh_cn": "中途所至之国，遣骞至康居", "review_note": "major01-D：史记·大宛列传「大宛以为然，遣骞」"},
  ],
  "evidence": [
   ev(SJ, "大宛列传", "七十列传/大宛列传#p52", "text-niutrans-f786e649b2ba8cea9a9d", "background", "primary", "始月氏居敦煌、祁连间，及为匈奴所败，乃远去，过宛，西击大夏而臣之。"),
   ev(SJ, "大宛列传", "七十列传/大宛列传#p5", "text-niutrans-2f2c621bdf6c78bc36d4", "process", "supporting", "道必更匈奴中，乃募能使者。"),
   ev(SJ, "大宛列传", "七十列传/大宛列传#p6", "text-niutrans-bfe1c2ae7caa0c8b6015", "process", "primary", "骞以郎应募，使月氏，与堂邑氏胡奴甘父俱出陇西。"),
   ev(SJ, "大宛列传", "七十列传/大宛列传#p25", "text-niutrans-62a69f21f7f7a15b448b", "result", "primary", "骞身所至者大宛、大月氏、大夏、康居，而传闻其旁大国五六，具为天子言之。"),
   ev(SJ, "大宛列传", "七十列传/大宛列传#p15", "text-niutrans-33bd5884e42ed9c25b42", "result", "supporting", "大宛以为然，遣骞，为发导绎，抵康居，康居传致大月氏。"),
   ev(SJ, "大宛列传", "七十列传/大宛列传#p133", "text-niutrans-aa71e55a5553f0b881a2", "impact", "primary", "然张骞凿空，其后使往者皆称博望侯，以为质於外国，外国由此信之。"),
  ],
 },
 "qin_han/event-tui-en-ling.yml": {
  "background_zh_cn": "主父偃以上书得幸，拜为郎中；其「尊立卫皇后，及发燕王定国阴事，盖偃有功焉」——渐为武帝倚重。",
  "process_zh_cn": "偃说上曰：「原陛下令诸侯得推恩分子弟，以地侯之」——以推恩之策析藩。",
  "result_zh_cn": "春正月，诏曰：「梁王、城阳王亲慈同生，愿以邑分弟，其许之，诸侯王请与子弟邑者，朕将亲览，使有列位焉」——推恩之诏颁行天下。",
  "impact_zh_cn": "推恩之策使诸侯王地自分而愈小、藩国自析——汉廷不削一城而藩国之患渐消，中央集权于制度内完成。",
  "people": [
   {"person_name_raw": "主父偃", "role": "official", "link_status": "needs_linking",
    "role_zh_cn": "郎中：推恩令之献策者", "review_note": "major01-D：史记·平津侯主父列传「原陛下令诸侯得推恩分子弟」", "person_id": None},
   {"person_name_raw": "汉武帝", "role": "monarch", "link_status": "needs_linking",
    "role_zh_cn": "纳推恩策、颁诏天下", "review_note": "major01-D：汉书·武帝纪「诸侯王请与子弟邑者，朕将亲览」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "长安", "role": "capital", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "推恩之议与诏书所出", "review_note": "major01-D：汉书·武帝纪（推恩诏）"},
  ],
  "evidence": [
   ev(SJ, "平津侯主父列传", "七十列传/平津侯主父列传#p183", "text-niutrans-38702cb5427fb7ccbc43", "background", "primary", "於是上乃拜主父偃、徐乐、严安为郎中。"),
   ev(SJ, "平津侯主父列传", "七十列传/平津侯主父列传#p189", "text-niutrans-5920094361f8e814ae55", "process", "primary", "原陛下令诸侯得推恩分子弟，以地侯之。"),
   ev(HS, "武帝纪", "纪/武帝纪#p121", "text-niutrans-d039e210f09e7d3653f1", "result", "primary", "春正月，诏曰： 梁王、城阳王亲慈同生，愿以邑分弟，其许之……使有列位焉。"),
   ev(SJ, "平津侯主父列传", "七十列传/平津侯主父列传#p189", "text-niutrans-5920094361f8e814ae55", "impact", "primary", "以地侯之。", "推恩析藩：藩国自小而中央集权"),
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
