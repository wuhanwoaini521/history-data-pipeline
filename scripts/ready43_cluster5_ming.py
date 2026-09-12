"""Ready-43 · Cluster 5：明 8 事件（朱元璋称帝/胡惟庸案/靖难之战/鄱阳湖/土木堡/萨尔浒/李自成攻北京/清军入关）。"""
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
        "review_note": f"ready43-c5：{work}源引文：「{quote}」；claim_field={field}；anchor=段落精确锚。{note}"}

MS = "明史"
BLOCKS = {
 "ming/event-zhuyuanzhang-chendi.yml": {
  "background_zh_cn": "陈友谅既亡，太祖曰「友谅亡，天下不难定也」——南方群雄次第削平，帝业之势已成。",
  "process_zh_cn": "洪武元年春正月乙亥，祀天地于南郊，即皇帝位。",
  "result_zh_cn": "追尊四代考妣为帝后、立妃马氏为皇后、世子标为皇太子——国本与宗庙制度初定。",
  "impact_zh_cn": "以李善长、徐达为左、右丞相，诸功臣进爵有差——明初中枢架构与功臣体制自此建立。",
  "people": [
   {"person_name_raw": "朱元璋", "role": "monarch", "link_status": "needs_linking",
    "role_zh_cn": "吴王→明太祖：即皇帝位、建号大明", "review_note": "ready43-c5：明史·太祖纪「祀天地于南郊，即皇帝位」", "person_id": None},
   {"person_name_raw": "李善长", "role": "official", "link_status": "needs_linking",
    "role_zh_cn": "左丞相：开国文臣之首", "review_note": "ready43-c5：明史·太祖纪「以李善长、徐达为左、右丞相」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "应天", "role": "capital", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "明初都城（南京），即位与祀天之所", "review_note": "ready43-c5：明史·太祖纪「祀天地于南郊，即皇帝位」"},
  ],
  "evidence": [
   ev(MS, "太祖纪", "本纪/卷一#p237", "text-niutrans-2336f825af62077cf90b", "background", "primary", "友谅亡，天下不难定也。"),
   ev(MS, "太祖纪", "本纪/卷二#p1", "text-niutrans-e145591d06aa37b748aa", "process", "primary", "洪武元年春正月乙亥，祀天地于南郊，即皇帝位。"),
   ev(MS, "太祖纪", "本纪/卷二#p3", "text-niutrans-c79a3018b50bfa5d2734", "result", "primary", "立妃马氏为皇后，世子标为皇太子。"),
   ev(MS, "太祖纪", "本纪/卷二#p4", "text-niutrans-d2ec9477fd0458e5054d", "impact", "primary", "以李善长、徐达为左、右丞相，诸功臣进爵有差。"),
  ],
 },
 "ming/event-hu-weiyong-an.yml": {
  "background_zh_cn": "胡惟庸为丞相，欲结好于徐达，达薄其人、不答，惟时时为帝言「惟庸不任相」——相权膨胀而帝相矛盾日深。",
  "process_zh_cn": "十三年春正月戊戌，左丞相胡惟庸谋反，及其党御史大夫陈宁、中丞涂节等伏诛。",
  "result_zh_cn": "案后株连不已：吉安侯陆仲亨等坐胡惟庸党下狱，靖宁侯叶升亦坐党诛——「胡惟庸、蓝玉两狱，株连死者且四万」。",
  "impact_zh_cn": "皇权借案整肃相权，株连绵延至太祖晚年犹「赦胡惟庸、蓝玉余党」——胡惟庸案成为明初中央官制剧变（废丞相）的枢机。",
  "people": [
   {"person_name_raw": "胡惟庸", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "左丞相：以谋反诛", "review_note": "ready43-c5：明史·太祖纪「左丞相胡惟庸谋反……伏诛」", "person_id": None},
   {"person_name_raw": "徐达", "role": "official", "link_status": "needs_linking",
    "role_zh_cn": "大将军：尝言惟庸不任相", "review_note": "ready43-c5：明史「徐达…时时为帝言惟庸不任相」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "京师", "role": "capital", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "案发与株连所在（南京）", "review_note": "ready43-c5：明史·太祖纪（洪武十三年正月）"},
  ],
  "evidence": [
   ev(MS, "列传", "列传/卷十三#p164", "text-niutrans-1222e1a1f5000cd568bc", "background", "primary",
      "胡惟庸为丞相，欲结好于达，达薄其人，不答……时时为帝言惟庸不任相。"),
   ev(MS, "太祖纪", "本纪/卷二#p434", "text-niutrans-cae23cbda66f3fd68845", "process", "primary",
      "十三年春正月戊戌，左丞相胡惟庸谋反，及其党御史大夫陈宁、中丞涂节等伏诛。"),
   ev(MS, "太祖纪", "本纪/卷三#p194", "text-niutrans-79697cb30b177f4e1a37", "result", "primary",
      "夏四月，吉安侯陆仲亨等坐胡惟庸党下狱。"),
   ev(MS, "刑法志", "志/卷七十#p309", "text-niutrans-15b29df74c0e67c1243b", "result", "supporting",
      "而胡惟庸、蓝玉两狱，株连死者且四万。"),
   ev(MS, "太祖纪", "本纪/卷三#p291", "text-niutrans-c13fc60f11c491901900", "impact", "primary",
      "赦胡惟庸、蓝玉余党。"),
  ],
 },
 "ming/event-jingnan-zhizhan.yml": {
  "background_zh_cn": "建文立，惮燕王强而未发，乃先废周王橚，欲以牵引燕；太祖遗诏诸王临国中、毋得至京师——削藩逼燕，兵衅已成。",
  "process_zh_cn": "燕王上书天子指齐泰、黄子澄为奸臣，援《祖训》「朝无正臣，内有奸恶，则亲王训兵待命」，遂举兵，自署官属、称其师曰「靖难」；拔居庸关、破怀来、取密云、克遵化、降永平，二旬众至数万。",
  "result_zh_cn": "乙丑，燕师至金川门，谷王橞、李景隆等开门纳王，都城遂陷。",
  "impact_zh_cn": "王升辇、诣奉天殿即皇帝位——靖难之役以燕王继统收场，永乐之世自此开启。",
  "people": [
   {"person_name_raw": "朱棣", "role": "monarch", "link_status": "needs_linking",
    "role_zh_cn": "燕王→明成祖：靖难起兵、入京即位", "review_note": "ready43-c5：明史·成祖纪「遂举兵……称其师曰靖难」「诣奉天殿即皇帝位」", "person_id": None},
   {"person_name_raw": "李景隆", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "建文军统帅：金川门开门纳燕师", "review_note": "ready43-c5：明史·成祖纪「谷王橞、李景隆等开门纳王」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "金川门", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "京师城门：燕师由此入都", "review_note": "ready43-c5：明史·成祖纪「至金川门……都城遂陷」"},
   {"place_name_raw": "北平", "role": "city", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "燕王起兵之地", "review_note": "ready43-c5：明史·成祖纪「洪武三年，封燕王」"},
  ],
  "evidence": [
   ev(MS, "成祖纪", "本纪/卷五#p13", "text-niutrans-38871e46435c81c3a122", "background", "primary",
      "惮燕王强，未发，乃先废周王橚，欲以牵引燕。"),
   ev(MS, "成祖纪", "本纪/卷五#p22", "text-niutrans-01592f9c9c77629ac767", "process", "primary",
      "遂举兵。自署官属，称其师曰 靖难 ……二旬众至数万。"),
   ev(MS, "成祖纪", "本纪/卷五#p156", "text-niutrans-b20cd847f660836c2ef1", "result", "primary",
      "乙丑，至金川门，谷王橞、李景隆等开门纳王，都城遂陷。"),
   ev(MS, "成祖纪", "本纪/卷五#p162", "text-niutrans-e554a7f91a4a93b26d5e", "impact", "primary",
      "王升辇，诣奉天殿即皇帝位。"),
  ],
 },
 "yuan/event-poyanghu-zhizhan.yml": {
  "background_zh_cn": "友谅兵号六十万，联巨舟为阵，楼橹高十余丈、绵亘数十里，旌旗戈盾望之如山——陈汉倾国而来。",
  "process_zh_cn": "会日晡，大风起东北，乃命敢死士操七舟、实火药芦苇中，纵火焚友谅舟。",
  "result_zh_cn": "友谅兵大乱，诸将鼓噪乘之，斩首二千余级，焚溺死者无算，友谅气夺。",
  "impact_zh_cn": "太祖论之曰「友谅亡，天下不难定也」——鄱阳湖一战定江南归属，帝业由此奠基。",
  "people": [
   {"person_name_raw": "陈友谅", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "汉王：倾国来战，兵败气夺", "review_note": "ready43-c5：明史·太祖纪「友谅兵号六十万，联巨舟为阵」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "鄱阳湖", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "决战水域（纵火焚舟之地）", "review_note": "ready43-c5：明史·太祖纪（湖口—鄱阳湖之战）"},
  ],
  "evidence": [
   ev(MS, "太祖纪", "本纪/卷一#p214", "text-niutrans-be1fec54086f8c6fa05c", "background", "primary",
      "友谅兵号六十万，联巨舟为阵，楼橹高十余丈，绵亘数十里，旌旗戈盾，望之如山。"),
   ev(MS, "太祖纪", "本纪/卷一#p220", "text-niutrans-91d75158e3a213be6825", "process", "primary",
      "会日晡，大风起东北，乃命敢死士操七舟，实火药芦苇中，纵火焚友谅舟。"),
   ev(MS, "太祖纪", "本纪/卷一#p222", "text-niutrans-1eac0c73a8048ac76a1e", "result", "primary",
      "友谅兵大乱，诸将鼓噪乘之，斩首二千余级，焚溺死者无算，友谅气夺。"),
   ev(MS, "太祖纪", "本纪/卷一#p237", "text-niutrans-2336f825af62077cf90b", "impact", "primary",
      "友谅亡，天下不难定也。"),
  ],
 },
 "ming/event-tumu-bao-zhibian.yml": {
  "background_zh_cn": "甲戌，敕边将备瓦剌也先；秋七月己丑，也先寇大同、参将吴浩战死，英宗下诏亲征。",
  "process_zh_cn": "辛酉，次土木，被围。",
  "result_zh_cn": "张辅、陈瀛、邝野、曹鼐等从征文武皆死，帝北狩——明军精锐尽丧于土木堡。",
  "impact_zh_cn": "皇太后命郕王监国；九月癸未，郕王即位、遥尊帝为太上皇帝，以明年为景泰元年——土木之变使明廷中枢更替、国防转入守势。",
  "people": [
   {"person_name_raw": "明英宗", "role": "monarch", "link_status": "needs_linking",
    "role_zh_cn": "亲征被围，北狩；后复辟", "review_note": "ready43-c5：明史·英宗前纪「次土木，被围」「帝北狩」", "person_id": None},
   {"person_name_raw": "也先", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "瓦剌太师：寇大同、围土木", "review_note": "ready43-c5：明史·英宗前纪「瓦剌也先寇大同」", "person_id": None},
   {"person_name_raw": "明代宗", "role": "monarch", "link_status": "needs_linking",
    "role_zh_cn": "郕王祁钰：监国、即位，改元景泰", "review_note": "ready43-c5：明史「郕王即位，遥尊帝为太上皇帝」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "土木", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "明军被围之地（土木堡）", "review_note": "ready43-c5：明史·英宗前纪「次土木，被围」"},
  ],
  "evidence": [
   ev(MS, "英宗前纪", "本纪/卷十#p274", "text-niutrans-22bc07d53023ec3bd799", "background", "primary",
      "秋七月己丑，瓦剌也先寇大同，参将吴浩战死，下诏亲征。"),
   ev(MS, "英宗前纪", "本纪/卷十#p290", "text-niutrans-51c128b7b387dfaf7658", "process", "primary",
      "辛酉，次土木，被围。"),
   ev(MS, "英宗前纪", "本纪/卷十#p292", "text-niutrans-bcdb1f4ab52536fb6ffc", "result", "primary",
      "英国公张辅……等，皆死，帝北狩。"),
   ev(MS, "英宗前纪", "本纪/卷十#p299", "text-niutrans-426ee9e3b0c3ac1f40da", "impact", "primary",
      "九月癸未，郕王即位，遥尊帝为太上皇帝。"),
   ev(MS, "景帝纪", "本纪/卷十一#p19", "text-niutrans-3b7f52b955bfae8ebed4", "impact", "supporting",
      "九月癸未，王即皇帝位，遥尊皇帝为太上皇帝，以明年为景泰元年。"),
  ],
 },
 "ming/event-saerhu-zhizhan.yml": {
  "background_zh_cn": "夏四月甲辰，大清兵克抚顺城，千总王命印死之——辽东衅起，明廷议大举进剿。",
  "process_zh_cn": "四十七年春二月乙丑，经略杨镐誓师于辽阳，总兵官李如柏、杜松、刘綎、马林分道出塞。",
  "result_zh_cn": "杜松、马林先败，刘綎深入三百里犹不知；遇大清兵于阿布达里冈，殊死战而军溃，綎战死、士卒脱者无几，朝鲜军亦溃。",
  "impact_zh_cn": "萨尔浒一战明军四路丧师、精锐尽没——辽东攻守之势逆转，明清兴亡之局自此奠定。",
  "people": [
   {"person_name_raw": "杨镐", "role": "official", "link_status": "needs_linking",
    "role_zh_cn": "辽东经略：四路出师主帅", "review_note": "ready43-c5：明史·神宗纪「经略杨镐誓师于辽阳」", "person_id": None},
   {"person_name_raw": "刘綎", "role": "supporter", "link_status": "needs_linking",
    "role_zh_cn": "总兵官：阿布达里冈战死", "review_note": "ready43-c5：明史·刘綎传「綎战死」", "person_id": None},
   {"person_name_raw": "杜松", "role": "supporter", "link_status": "needs_linking",
    "role_zh_cn": "总兵官：先败，军覆", "review_note": "ready43-c5：明史·刘綎传「杜松军覆犹不知」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "萨尔浒", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "决战之地（明军四路出师所向）", "review_note": "ready43-c5：明史·神宗纪「分道出塞」；刘綎传「遇大清兵」"},
   {"place_name_raw": "辽阳", "role": "city", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "明军誓师之地", "review_note": "ready43-c5：明史·神宗纪「誓师于辽阳」"},
  ],
  "evidence": [
   ev(MS, "神宗纪", "本纪/卷二十一#p279", "text-niutrans-262f1b2faec3b61675d1", "background", "primary",
      "夏四月甲辰，大清兵克抚顺城，千总王命印死之。"),
   ev(MS, "神宗纪", "本纪/卷二十一#p294", "text-niutrans-0eb853d0dfae3b33e177", "process", "primary",
      "四十七年春二月乙丑，经略杨镐誓师于辽阳，总兵官李如柏、杜松、刘綎、马林分道出塞。"),
   ev(MS, "刘綎传", "列传/卷一百三十五#p140", "text-niutrans-8e95332d60fcd51b8994", "process", "supporting",
      "綎已深入三百里，杜松军覆犹不知。"),
   ev(MS, "刘綎传", "列传/卷一百三十五#p144", "text-niutrans-937557c06f1b0adaf6df", "result", "primary",
      "未及陈，复为大清兵所乘，大溃，綎战死。"),
   ev(MS, "刘綎传", "列传/卷一百三十五#p146", "text-niutrans-09032a6daff4e4c2fcbb", "result", "supporting",
      "士卒脱者无几。"),
   ev(MS, "刘綎传", "列传/卷一百三十五#p149", "text-niutrans-4121be55c02021e6758b", "impact", "primary",
      "应乾发火器，反击己营，大乱。", "明鲜联军尽溃之状"),
  ],
 },
 "ming/event-lizicheng-gong-beijing.yml": {
  "background_zh_cn": "辛丑，京师戒严；辛卯，李自成陷陕州——流贼自秦入豫、渐逼畿甸。",
  "process_zh_cn": "丁未，昧爽，内城陷。",
  "result_zh_cn": "帝崩于万岁山，王承恩从死——崇祯殉国，明朝作为全国政权的统治终结。",
  "impact_zh_cn": "是年夏四月，大清兵破贼于山海关，五月入京师，以帝体改葬、令臣民为服丧三日，谥曰庄烈愍皇帝，陵曰思陵——李自成败亡而清朝入主，易代之局完成。",
  "people": [
   {"person_name_raw": "李自成", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "闯王：破京师、覆明", "review_note": "ready43-c5：明史·庄烈帝纪「李自成陷陕州」「内城陷」", "person_id": None},
   {"person_name_raw": "崇祯帝", "role": "monarch", "link_status": "needs_linking",
    "role_zh_cn": "明思宗：京师陷后崩于万岁山", "review_note": "ready43-c5：明史·庄烈帝纪「帝崩于万岁山，王承恩从死」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "北京", "role": "capital", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "明京师：内城陷、帝殉国", "review_note": "ready43-c5：明史·庄烈帝纪「京师戒严」「内城陷」"},
   {"place_name_raw": "万岁山", "role": "location", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "帝殉国处（煤山）", "review_note": "ready43-c5：明史·庄烈帝纪「帝崩于万岁山」"},
  ],
  "evidence": [
   ev(MS, "庄烈帝纪", "本纪/卷二十三#p229", "text-niutrans-787fc0027bcb98f837f6", "background", "primary",
      "辛丑，京师戒严。"),
   ev(MS, "庄烈帝纪", "本纪/卷二十三#p276", "text-niutrans-f56b96cc9d490b29662b", "background", "supporting",
      "辛卯，李自成陷陕州。"),
   ev(MS, "庄烈帝纪", "本纪/卷二十四#p285", "text-niutrans-0bc162436a79e9c96582", "process", "primary",
      "丁未，昧爽，内城陷。"),
   ev(MS, "庄烈帝纪", "本纪/卷二十四#p286", "text-niutrans-98a396d48fa8cc7de2b9", "result", "primary",
      "帝崩于万岁山，王承恩从死。"),
   ev(MS, "庄烈帝纪", "本纪/卷二十四#p293", "text-niutrans-c468d084612c8b693c95", "impact", "primary",
      "是年夏四月，我大清兵破贼于山海关，五月，入京师，以帝体改葬，令臣民为服丧三日，谥曰庄烈愍皇帝，陵曰思陵。"),
  ],
 },
 "qing/event-qingjun-ru-guan.yml": {
  "background_zh_cn": "癸巳，明廷封总兵官吴三桂、左良玉、唐通、黄得功俱为伯——危急之秋倚重边将，山海关之得失系于三桂。",
  "process_zh_cn": "是年夏四月，我大清兵破贼于山海关。",
  "result_zh_cn": "五月，大清兵入京师。",
  "impact_zh_cn": "入京师后以帝体改葬、令臣民为服丧三日，谥曰庄烈愍皇帝、陵曰思陵——清朝以「为明复仇」的名义入主中原，中国历史进入清朝时期。",
  "people": [
   {"person_name_raw": "吴三桂", "role": "official", "link_status": "needs_linking",
    "role_zh_cn": "明总兵：封伯，后引清兵入关", "review_note": "ready43-c5：明史·庄烈帝纪「封总兵官吴三桂……俱为伯」", "person_id": None},
   {"person_name_raw": "多尔衮", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "清摄政王：统兵入关", "review_note": "ready43-c5：明史·庄烈帝纪「我大清兵破贼于山海关」（清方主帅为多尔衮，见清史稿）", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "山海关", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "破贼入关之地", "review_note": "ready43-c5：明史·庄烈帝纪「我大清兵破贼于山海关」"},
  ],
  "evidence": [
   ev(MS, "庄烈帝纪", "本纪/卷二十四#p275", "text-niutrans-f104a688ea08d1dd9c70", "background", "primary",
      "癸巳，封总兵官吴三桂、左良玉、唐通、黄得功俱为伯。"),
   ev(MS, "庄烈帝纪", "本纪/卷二十四#p183", "text-niutrans-5274274044ec475d4645", "background", "supporting",
      "庚辰，大清兵克蓟州。"),
   ev(MS, "庄烈帝纪", "本纪/卷二十四#p293", "text-niutrans-c468d084612c8b693c95", "process", "primary",
      "是年夏四月，我大清兵破贼于山海关。"),
   ev(MS, "庄烈帝纪", "本纪/卷二十四#p293", "text-niutrans-c468d084612c8b693c95", "result", "primary",
      "五月，入京师。"),
   ev(MS, "庄烈帝纪", "本纪/卷二十四#p293", "text-niutrans-c468d084612c8b693c95", "impact", "primary",
      "以帝体改葬，令臣民为服丧三日，谥曰庄烈愍皇帝，陵曰思陵。"),
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
