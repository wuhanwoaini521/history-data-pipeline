"""Major Batch 01 · Cluster A：战国变法与争霸（9 事件）。"""
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
        "review_note": f"major01-A：{work}源引文：「{quote}」；claim_field={field}；anchor=段落精确锚。{note}"}

SJ = "史记"
BLOCKS = {
 "chunqiu_zhanguo/event-shangyang-bianfa.yml": {
  "background_zh_cn": "孝公既用卫鞅，鞅欲变法而恐天下议己；鞅以「圣人不易民而教，知者不变法而治」驳甘龙、杜挚之议——变法之议既定于朝堂。",
  "process_zh_cn": "以卫鞅为左庶长，卒定变法之令：令民为什伍，而相牧司连坐——什伍连坐、奖励耕战之法次第推行。",
  "result_zh_cn": "行之十年，秦民大说，道不拾遗、山无盗贼、家给人足——秦国由是富强。",
  "impact_zh_cn": "孝公十二年作为咸阳、筑冀阙而徙都之，秦法行于新都；然变法者终罹祸：「秦惠王车裂商君以徇」——其人虽死，秦法不复更张，为秦并天下奠定制度根基。",
  "people": [
   {"person_name_raw": "商鞅", "role": "official", "link_status": "needs_linking",
    "role_zh_cn": "左庶长：变法主持者，后车裂", "review_note": "major01-A：史记·商君列传「以卫鞅为左庶长，卒定变法之令」「车裂商君以徇」", "person_id": None},
   {"person_name_raw": "秦孝公", "role": "monarch", "link_status": "needs_linking",
    "role_zh_cn": "任用卫鞅变法之君", "review_note": "major01-A：史记·商君列传「孝公既用卫鞅」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "咸阳", "role": "capital", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "孝公十二年新都，变法推行之地", "review_note": "major01-A：史记·秦本纪「作为咸阳，筑冀阙，秦徙都之」"},
  ],
  "evidence": [
   ev(SJ, "商君列传", "七十列传/商君列传#p35", "text-niutrans-358f5695ff3415858e8f", "background", "primary", "孝公既用卫鞅，鞅欲变法，恐天下议己。"),
   ev(SJ, "商君列传", "七十列传/商君列传#p43", "text-niutrans-cbe689717e09adc9e289", "background", "supporting", "圣人不易民而教，知者不变法而治。"),
   ev(SJ, "商君列传", "七十列传/商君列传#p55", "text-niutrans-6a6e061415a6e0ad4a95", "process", "primary", "以卫鞅为左庶长，卒定变法之令。"),
   ev(SJ, "商君列传", "七十列传/商君列传#p56", "text-niutrans-71551dff2d701d4714fb", "process", "supporting", "令民为什伍，而相牧司连坐。"),
   ev(SJ, "商君列传", "七十列传/商君列传#p76", "text-niutrans-619bac542dcc8d9961a3", "result", "primary", "行之十年，秦民大说，道不拾遗，山无盗贼，家给人足。"),
   ev(SJ, "商君列传", "七十列传/商君列传#p168", "text-niutrans-58e29835bb397301c4d8", "impact", "primary", "秦惠王车裂商君以徇。"),
   ev(SJ, "秦本纪", "十二本纪/秦本纪#p422", "text-niutrans-9e8b8164281e542f63ad", "impact", "supporting", "十二年，作为咸阳，筑冀阙，秦徙都之。"),
  ],
 },
 "chunqiu_zhanguo/event-likui-bianfa.yml": {
  "background_zh_cn": "当魏文侯时，李克务尽地力——魏国率先以「尽地力之教」富国。",
  "process_zh_cn": "魏有李悝，「尽地力之教」：教民勤于农事、地尽其利，以农富国。",
  "result_zh_cn": "魏用李克、尽地力，为强君——魏国由是富强，为战国初期首强。",
  "impact_zh_cn": "李悝尽地力之教开列国变法之先声（其后商鞅变法即承此路径），魏之富强为战国变法时代揭幕。",
  "people": [
   {"person_name_raw": "李悝", "role": "official", "link_status": "needs_linking",
    "role_zh_cn": "魏文侯之相：尽地力之教", "review_note": "major01-A：史记·孟子荀卿列传「魏有李悝，尽地力之教」", "person_id": None},
   {"person_name_raw": "魏文侯", "role": "monarch", "link_status": "needs_linking",
    "role_zh_cn": "魏国之君：用李克致强", "review_note": "major01-A：史记·货殖列传「当魏文侯时，李克务尽地力」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "安邑", "role": "capital", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "魏国都城，变法图强之枢", "review_note": "major01-A：史记·魏世家「徙治安邑」"},
  ],
  "evidence": [
   ev(SJ, "货殖列传", "七十列传/货殖列传#p61", "text-niutrans-82c88c9f98e1caefe41d", "background", "primary", "当魏文侯时，李克务尽地力，而白圭乐观时变。"),
   ev(SJ, "孟子荀卿列传", "七十列传/孟子荀卿列传#p80", "text-niutrans-5d3dfcfea5565b4f9361", "process", "primary", "魏有李悝，尽地力之教。"),
   ev(SJ, "平准书", "八书/平准书#p246", "text-niutrans-5e51c6034c07fb9484e4", "result", "primary", "魏用李克，尽地力，为强君。"),
   ev(SJ, "魏世家", "三十世家/魏世家#p31", "text-niutrans-7c205970e1b6b527b39c", "impact", "primary", "徙治安邑。"),
  ],
 },
 "chunqiu_zhanguo/event-wuqi-bianfa.yml": {
  "background_zh_cn": "吴起相楚：楚悼王用吴起，明法审令、捐不急之官、废公族疏远者，以抚养战斗之士。",
  "process_zh_cn": "变法行之，楚国扩张：「于是南平百越；北并陈蔡，却三晋；西伐秦」。",
  "result_zh_cn": "及悼王死，宗室大臣作乱而攻吴起，吴起走之王尸而伏之；击起之徒因射刺吴起，并中悼王——变法中辍。",
  "impact_zh_cn": "吴起变法虽以殉难告终，其「明法审令、废公族」路径为战国楚制改革所本，楚国一度兵威南暨百越、北抗三晋。",
  "people": [
   {"person_name_raw": "吴起", "role": "official", "link_status": "needs_linking",
    "role_zh_cn": "楚悼王之相：变法者，殉难于悼王丧次", "review_note": "major01-A：史记·孙子吴起列传「明法审令……及悼王死，宗室大臣作乱而攻吴起」", "person_id": None},
   {"person_name_raw": "楚悼王", "role": "monarch", "link_status": "needs_linking",
    "role_zh_cn": "楚国君：用吴起变法", "review_note": "major01-A：史记·孙子吴起列传（悼王死、宗室攻吴起）", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "郢", "role": "capital", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "楚都，吴起变法与殉难所在", "review_note": "major01-A：史记·楚世家「昭王之出郢也」（楚都郢）"},
  ],
  "evidence": [
   ev(SJ, "孙子吴起列传", "七十列传/孙子吴起列传#p130", "text-niutrans-8fff9056221c7795d8a4", "process", "primary", "明法审令，捐不急之官，废公族疏远者，以抚养战斗之士。"),
   ev(SJ, "孙子吴起列传", "七十列传/孙子吴起列传#p132", "text-niutrans-e94e404f4bd1972e49e8", "result", "primary", "於是南平百越；北并陈蔡，卻三晋；西伐秦。"),
   ev(SJ, "孙子吴起列传", "七十列传/孙子吴起列传#p135", "text-niutrans-0db3ac4906370cd157b0", "impact", "primary", "及悼王死，宗室大臣作乱而攻吴起，吴起走之王尸而伏之。"),
   ev(SJ, "孙子吴起列传", "七十列传/孙子吴起列传#p136", "text-niutrans-3f1594eb55528cf45356", "impact", "supporting", "击起之徒因射刺吴起，并中悼王。"),
  ],
 },
 "chunqiu_zhanguo/event-guiling-zhizhan.yml": {
  "background_zh_cn": "魏围赵邯郸，赵请救于齐——齐使田忌、孙膑救赵。",
  "process_zh_cn": "田忌从孙膑「批亢捣虚」之计，直趋大梁；魏果去邯郸，与齐战于桂陵。",
  "result_zh_cn": "齐大破梁军于桂陵（十月，邯郸拔，齐因起兵击魏，大败之桂陵）。",
  "impact_zh_cn": "「围魏救赵」之策由是成为兵家范式，魏国东线受挫、齐国声势大振。",
  "people": [
   {"person_name_raw": "孙膑", "role": "supporter", "link_status": "needs_linking",
    "role_zh_cn": "齐军军师：围魏救赵之计", "review_note": "major01-A：史记·孙子吴起列传「田忌从之，魏果去邯郸，与齐战於桂陵」", "person_id": None},
   {"person_name_raw": "田忌", "role": "supporter", "link_status": "needs_linking",
    "role_zh_cn": "齐将：帅师救赵", "review_note": "major01-A：史记·魏世家「齐使田忌、孙膑救赵」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "桂陵", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "齐魏决战之地", "review_note": "major01-A：史记·孙子吴起列传「大破梁军」于桂陵"},
   {"place_name_raw": "邯郸", "role": "city", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "赵都：被魏围攻、齐救之", "review_note": "major01-A：史记·赵世家「魏惠王拔我邯郸」"},
  ],
  "evidence": [
   ev(SJ, "魏世家", "三十世家/魏世家#p144", "text-niutrans-dc54aae141d5746b4f88", "background", "primary", "赵请救于齐，齐使田忌、孙膑救赵，败魏桂陵。"),
   ev(SJ, "孙子吴起列传", "七十列传/孙子吴起列传#p51", "text-niutrans-f80ba70cfcfe8de2d2d3", "process", "primary", "田忌从之，魏果去邯郸，与齐战於桂陵，大破梁军。"),
   ev(SJ, "田敬仲完世家", "三十世家/田敬仲完世家#p222", "text-niutrans-449d57614c0af2be263d", "result", "primary", "十月，邯郸拔，齐因起兵击魏，大败之桂陵。"),
   ev(SJ, "赵世家", "三十世家/赵世家#p356", "text-niutrans-318c81a24af7deb3af54", "impact", "primary", "二十二年，魏惠王拔我邯郸，齐亦败魏于桂陵。"),
  ],
 },
 "chunqiu_zhanguo/event-maling-zhizhan.yml": {
  "background_zh_cn": "魏将庞涓闻齐师至，去韩而归；齐军已过而西——孙膑以减灶诱敌。",
  "process_zh_cn": "庞涓行三日而大喜，曰「我固知齐军怯」；果夜至斫木下，见白书，乃钻火烛之——读其书未毕，齐军万弩俱发，魏军大乱相失。",
  "result_zh_cn": "庞涓自知智穷兵败，乃自刭；齐因乘胜尽破其军，虏魏太子申以归。",
  "impact_zh_cn": "马陵一战魏国精锐尽丧、主将自杀、太子被虏——魏国霸权自此崩落，齐国称雄东方。",
  "people": [
   {"person_name_raw": "孙膑", "role": "supporter", "link_status": "needs_linking",
    "role_zh_cn": "齐军军师：减灶诱敌、马陵设伏", "review_note": "major01-A：史记·孙子吴起列传「齐军万弩俱发」", "person_id": None},
   {"person_name_raw": "庞涓", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "魏将：马陵兵败自刭", "review_note": "major01-A：史记·孙子吴起列传「庞涓自知智穷兵败，乃自刭」", "person_id": None},
   {"person_name_raw": "魏太子申", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "魏军主帅：被齐军俘获", "review_note": "major01-A：史记·孙子吴起列传「虏魏太子申以归」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "马陵", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "齐魏决战之地（万弩俱发处）", "review_note": "major01-A：史记·孙子吴起列传「庞涓果夜至斫木下」"},
  ],
  "evidence": [
   ev(SJ, "孙子吴起列传", "七十列传/孙子吴起列传#p54", "text-niutrans-6217111a7c339305669e", "background", "primary", "魏将庞涓闻之，去韩而归，齐军既已过而西矣。"),
   ev(SJ, "孙子吴起列传", "七十列传/孙子吴起列传#p58", "text-niutrans-cb943958e23c3850ca4b", "process", "supporting", "庞涓行三日，大喜，曰： 我固知齐军怯。"),
   ev(SJ, "孙子吴起列传", "七十列传/孙子吴起列传#p63", "text-niutrans-f28121300f4addf177c2", "process", "primary", "读其书未毕，齐军万弩俱发，魏军大乱相失。"),
   ev(SJ, "孙子吴起列传", "七十列传/孙子吴起列传#p64", "text-niutrans-20b5db6a3259d7b2c73d", "result", "primary", "庞涓自知智穷兵败，乃自刭。"),
   ev(SJ, "孙子吴起列传", "七十列传/孙子吴起列传#p65", "text-niutrans-abadf8355537547b5695", "impact", "primary", "齐因乘胜尽破其军，虏魏太子申以归。"),
  ],
 },
 "chunqiu_zhanguo/event-tianshi-dai-qi.yml": {
  "background_zh_cn": "田常以大斗出贷、小斗收之收揽民心，「行之五年，齐国之政皆归田常」。",
  "process_zh_cn": "田常尽诛鲍、晏、监止及公族之强者，割齐自安平以东至琅邪自为封邑；至田和，与魏文侯会浊泽求为诸侯。",
  "result_zh_cn": "魏文侯乃使使言周天子及诸侯，请立齐相田和为诸侯，周天子许之——田氏列于诸侯。",
  "impact_zh_cn": "齐侯太公和立，田齐纪元开始——「田氏代齐」与三家分晋并称，标志战国封建秩序全面取代春秋旧制。",
  "people": [
   {"person_name_raw": "田常", "role": "official", "link_status": "needs_linking",
    "role_zh_cn": "齐相：尽诛公族、齐政归田氏", "review_note": "major01-A：史记·田敬仲完世家「齐国之政皆归田常」", "person_id": None},
   {"person_name_raw": "田和", "role": "monarch", "link_status": "needs_linking",
    "role_zh_cn": "齐太公：求为诸侯、田齐始封", "review_note": "major01-A：史记·田敬仲完世家「请立齐相田和为诸侯。周天子许之」", "person_id": None},
   {"person_name_raw": "魏文侯", "role": "supporter", "link_status": "needs_linking",
    "role_zh_cn": "为田和请命于周天子", "review_note": "major01-A：史记·田敬仲完世家「魏文侯乃使使言周天子及诸侯」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "浊泽", "role": "assembly_site", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "田和与魏文侯会盟求诸侯之地", "review_note": "major01-A：史记·田敬仲完世家「太公与魏文侯会浊泽，求为诸侯」"},
  ],
  "evidence": [
   ev(SJ, "田敬仲完世家", "三十世家/田敬仲完世家#p108", "text-niutrans-fe0f50a0b6fa6cbd6937", "background", "primary", "行之五年，齐国之政皆归田常。"),
   ev(SJ, "田敬仲完世家", "三十世家/田敬仲完世家#p109", "text-niutrans-a022648f93e9cf4e948d", "process", "primary", "田常于是尽诛鲍、晏、监止及公族之强者，而割齐自安平以东至琅邪，自为封邑。"),
   ev(SJ, "田敬仲完世家", "三十世家/田敬仲完世家#p133", "text-niutrans-097b1265f0626e32bd22", "result", "primary", "魏文侯乃使使言周天子及诸侯，请立齐相田和为诸侯。周天子许之。"),
   ev(SJ, "田敬仲完世家", "三十世家/田敬仲完世家#p135", "text-niutrans-e2b8722167ca505aa7c9", "impact", "primary", "齐侯太公和立二年，和卒，子桓公午立。"),
  ],
 },
 "chunqiu_zhanguo/event-wuguo-fa-qi.yml": {
  "background_zh_cn": "燕昭王悉起兵，以乐毅为上将军，赵惠文王以相国印授乐毅——五国之师共伐齐。",
  "process_zh_cn": "乐毅对曰「齐，霸国之馀业也，地大人众，未易独攻也」，故合五国之兵长驱平齐。",
  "result_zh_cn": "乐毅留徇齐五岁，下齐七十余城，皆为郡县以属燕，唯独莒、即墨未服——齐国几亡。",
  "impact_zh_cn": "乐毅与燕新王有隙，欲连兵留齐之事为人所谮，功败垂成——莒、即墨二城遂成田单复齐之基。",
  "people": [
   {"person_name_raw": "乐毅", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "燕上将军：下齐七十余城", "review_note": "major01-A：史记·乐毅列传「下齐七十馀城」", "person_id": None},
   {"person_name_raw": "燕昭王", "role": "monarch", "link_status": "needs_linking",
    "role_zh_cn": "燕君：悉起兵伐齐", "review_note": "major01-A：史记·乐毅列传「燕昭王悉起兵，使乐毅为上将军」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "临淄", "role": "capital", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "齐都（燕军长驱平齐所向）", "review_note": "major01-A：史记·田单列传「燕师长驱平齐」"},
   {"place_name_raw": "即墨", "role": "battlesite", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "仅存二城之一（田单所守）", "review_note": "major01-A：史记·乐毅列传「唯独莒、即墨未服」"},
   {"place_name_raw": "莒", "role": "battlesite", "link_status": "needs_linking", "sequence": 3,
    "description_zh_cn": "仅存二城之一", "review_note": "major01-A：史记·乐毅列传「唯独莒、即墨未服」"},
  ],
  "evidence": [
   ev(SJ, "乐毅列传", "七十列传/乐毅列传#p20", "text-niutrans-6853abd4273a1aa114ee", "background", "primary", "燕昭王悉起兵，使乐毅为上将军，赵惠文王以相国印授乐毅。"),
   ev(SJ, "乐毅列传", "七十列传/乐毅列传#p16", "text-niutrans-fa8dbc5eb5daec11ffc8", "process", "primary", "乐毅对曰： 齐，霸国之馀业也，地大人众，未易独攻也。"),
   ev(SJ, "乐毅列传", "七十列传/乐毅列传#p28", "text-niutrans-94ab0978d4ead0e14419", "result", "primary", "乐毅留徇齐五岁，下齐七十馀城，皆为郡县以属燕，唯独莒、即墨未服。"),
   ev(SJ, "乐毅列传", "七十列传/乐毅列传#p31", "text-niutrans-72f01d7d09a73f1534a1", "impact", "primary", "闻乐毅与燕新王有隙，欲连兵且留齐，南面而王齐。"),
  ],
 },
 "chunqiu_zhanguo/event-tiandan-fu-qi.yml": {
  "background_zh_cn": "燕师长驱平齐，田单走安平，令宗人尽断车轴末而傅铁笼——唯田单宗人以铁笼故得脱，东保即墨。",
  "process_zh_cn": "城中相与推田单；田单乃凿城数十穴、夜纵火牛，壮士五千人随其后。",
  "result_zh_cn": "牛尾热怒而奔燕军，燕军夜大惊；牛尾炬火光明炫燿，所触尽死伤，五千人因衔枚击之、城中鼓譟从之——燕军大败，齐七十余城皆复。",
  "impact_zh_cn": "襄王封田单，号曰安平君——田单以火牛一战复齐国，战国后期齐得以复立于东方。",
  "people": [
   {"person_name_raw": "田单", "role": "supporter", "link_status": "needs_linking",
    "role_zh_cn": "齐将：火牛阵复齐，封安平君", "review_note": "major01-A：史记·田单列传「夜纵牛，壮士五千人随其后」「襄王封田单，号曰安平君」", "person_id": None},
   {"person_name_raw": "齐襄王", "role": "monarch", "link_status": "needs_linking",
    "role_zh_cn": "齐君：复国后封田单", "review_note": "major01-A：史记·田单列传「襄王封田单」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "即墨", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "田单坚守、火牛出击之地", "review_note": "major01-A：史记·田单列传「东保即墨」"},
   {"place_name_raw": "安平", "role": "city", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "田单初走之地（铁笼得全）", "review_note": "major01-A：史记·田单列传「田单走安平」"},
  ],
  "evidence": [
   ev(SJ, "田单列传", "七十列传/田单列传#p5", "text-niutrans-ec11cd07a4680468f5aa", "background", "primary", "唯田单宗人以铁笼故得脱，东保即墨。"),
   ev(SJ, "田单列传", "七十列传/田单列传#p10", "text-niutrans-85bd39241522ed69d575", "process", "supporting", "城中相与推田单。"),
   ev(SJ, "田单列传", "七十列传/田单列传#p41", "text-niutrans-99603de76c9c6cb8f19f", "process", "primary", "凿城数十穴，夜纵牛，壮士五千人随其后。"),
   ev(SJ, "田单列传", "七十列传/田单列传#p43", "text-niutrans-3f04946eae69d70eb9ef", "result", "primary", "牛尾炬火光明炫燿，燕军视之皆龙文，所触尽死伤。"),
   ev(SJ, "田单列传", "七十列传/田单列传#p49", "text-niutrans-4f33ced7fccb880a4974", "impact", "primary", "襄王封田单，号曰安平君。"),
  ],
 },
 "chunqiu_zhanguo/event-yique-zhizhan.yml": {
  "background_zh_cn": "韩魏联军攻秦（佐韩攻秦），战于伊阙——秦东出之要冲。",
  "process_zh_cn": "其明年，白起为左更，攻韩、魏于伊阙，斩首二十四万，又虏其将公孙喜，拔五城。",
  "result_zh_cn": "秦使白起伐韩于伊阙，大胜，斩首二十四万——韩魏主力尽丧于伊阙之下。",
  "impact_zh_cn": "魏世家载「秦将白起败我军伊阙二十四万」——韩魏自此衰弱，秦国东出中原之势不可复遏。",
  "people": [
   {"person_name_raw": "白起", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "秦左更：伊阙大破韩魏", "review_note": "major01-A：史记·白起王翦列传「攻韩、魏於伊阙，斩首二十四万」", "person_id": None},
   {"person_name_raw": "公孙喜", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "魏将：伊阙被虏", "review_note": "major01-A：史记·白起王翦列传「虏其将公孙喜」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "伊阙", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "白起斩首二十四万之地", "review_note": "major01-A：史记·白起王翦列传「攻韩、魏於伊阙」"},
  ],
  "evidence": [
   ev(SJ, "魏世家", "三十世家/魏世家#p251", "text-niutrans-6b71a96db14d0a307b98", "background", "primary", "三年，佐韩攻秦。"),
   ev(SJ, "白起王翦列传", "七十列传/白起王翦列传#p5", "text-niutrans-fc1da6e503593e940e7f", "process", "primary", "白起为左更，攻韩、魏於伊阙，斩首二十四万，又虏其将公孙喜，拔五城。"),
   ev(SJ, "楚世家", "三十世家/楚世家#p600", "text-niutrans-6e8d62a0f0e649aa4dfe", "result", "primary", "秦使白起伐韩于伊阙，大胜，斩首二十四万。"),
   ev(SJ, "魏世家", "三十世家/魏世家#p251", "text-niutrans-6b71a96db14d0a307b98", "impact", "primary", "秦将白起败我军伊阙二十四万。"),
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
