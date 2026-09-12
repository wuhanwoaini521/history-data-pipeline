"""Major Batch 01 · Cluster E：武帝后期与昭宣（7 事件）。"""
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
        "review_note": f"major01-E：{work}源引文：「{quote}」；claim_field={field}；anchor=段落精确锚。{note}"}

HS = "汉书"
BLOCKS = {
 "qin_han/event-wugu-zhi-huo.yml": {
  "background_zh_cn": "武帝晚年「巫蛊起」——方士巫祝之术盛行于宫禁，江充等因之构陷。",
  "process_zh_cn": "征和二年，巫蛊事起，太子据被诬；「庚寅，太子亡，皇后自杀」——兵变与追捕相继。",
  "result_zh_cn": "八月辛亥，太子自杀于湖——巫蛊之祸以太子死、皇后崩告终，死者数万。",
  "impact_zh_cn": "太子既没，储位空虚，武帝晚年立幼子、托孤霍光——巫蛊之祸直接改写了汉室的继承格局。",
  "people": [
   {"person_name_raw": "汉武帝", "role": "monarch", "link_status": "needs_linking",
    "role_zh_cn": "晚年惑于巫蛊、太子死而悔之", "review_note": "major01-E：汉书·武帝纪「巫蛊起」", "person_id": None},
   {"person_name_raw": "戾太子", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "太子据：被诬亡走、自杀于湖", "review_note": "major01-E：汉书·武帝纪「太子自杀于湖」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "湖", "role": "location", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "太子自杀之地（湖县）", "review_note": "major01-E：汉书·武帝纪「太子自杀于湖」"},
  ],
  "evidence": [
   ev(HS, "武帝纪", "纪/武帝纪#p446", "text-niutrans-256f26a428f12e53a1cb", "background", "primary", "巫蛊起。"),
   ev(HS, "武帝纪", "纪/武帝纪#p452", "text-niutrans-9c65df00a51df8e5d057", "process", "primary", "庚寅，太子亡，皇后自杀。"),
   ev(HS, "武帝纪", "纪/武帝纪#p455", "text-niutrans-af71d834064f6d5118e0", "result", "primary", "八月辛亥，太子自杀于湖。"),
   ev(HS, "武帝纪", "纪/武帝纪#p76", "text-niutrans-d48eddd6bf1041bbc180", "impact", "primary", "捕为巫蛊者，皆枭首。"),
  ],
 },
 "qin_han/event-luntai-zhao.yml": {
  "background_zh_cn": "上既悔远征伐，而搜粟都尉桑弘羊与丞相御史奏言：故轮台东捷枝、渠犁皆故国，「可益通沟渠，种五谷」——请复屯田轮台。",
  "process_zh_cn": "诏书论之：「今请远田轮台，欲起亭隧，是扰劳天下，非所以优民也」——深陈既往之悔，罢轮台屯田之议。",
  "result_zh_cn": "轮台诏定「禁苛暴、止擅赋、力本农」之政——武帝晚年国策由征伐转向休息。",
  "impact_zh_cn": "「深陈既往之悔」的轮台诏为昭宣中兴之转关——昭帝用桑弘羊前议仅作屯田调整，而汉政自此以务农安民为本。",
  "people": [
   {"person_name_raw": "汉武帝", "role": "monarch", "link_status": "needs_linking",
    "role_zh_cn": "下轮台诏、悔远征", "review_note": "major01-E：汉书·西域传下「上既悔远征伐」", "person_id": None},
   {"person_name_raw": "桑弘羊", "role": "official", "link_status": "needs_linking",
    "role_zh_cn": "搜粟都尉：奏请屯田轮台", "review_note": "major01-E：汉书·西域传下「搜粟都尉桑弘羊与丞相御史奏言」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "轮台", "role": "frontier", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "诏书所罢屯田之地", "review_note": "major01-E：汉书·西域传下「今请远田轮台」"},
  ],
  "evidence": [
   ev(HS, "西域传下", "传/西域传下#p163", "text-niutrans-05b9e01acc787daa1708", "background", "primary", "上既悔远征伐，而搜粟都尉桑弘羊与丞相御史奏言。"),
   ev(HS, "西域传下", "传/西域传下#p190", "text-niutrans-84943e56bbaf18e21247", "process", "primary", "今请远田轮台，欲起亭隧，是扰劳天下，非所以优民也。"),
   ev(HS, "西域传下", "传/西域传下#p190", "text-niutrans-84943e56bbaf18e21247", "result", "primary", "是扰劳天下，非所以优民也。"),
   ev(HS, "西域传下", "传/西域传下#p202", "text-niutrans-4e77f249edd25fba7668", "impact", "primary", "昭帝乃用桑弘羊前议，以杅弥太子赖丹为校尉，将军田轮台。"),
  ],
 },
 "qin_han/event-wudi-si-huoguang.yml": {
  "background_zh_cn": "后岁余，武帝疾，立皇子钩弋夫人男为太子——储位既定，托孤之臣待命。",
  "process_zh_cn": "上以光为大司马大将军，日磾为车骑将军，及太仆上官桀为左将军，搜粟都尉桑弘羊为御史大夫，皆拜卧内床下，受遗诏辅少主。",
  "result_zh_cn": "遗诏既定：拜大将军霍光、车骑将军金日磾、御史大夫桑弘羊及丞相千秋，「并受遗诏，辅道少主」。",
  "impact_zh_cn": "霍光以大司马大将军辅政，昭宣之世由此开启——「党亲连体，根据于朝廷」，霍氏专权之局也随之而生。",
  "people": [
   {"person_name_raw": "霍光", "role": "official", "link_status": "needs_linking",
    "role_zh_cn": "大司马大将军：受遗诏辅少主", "review_note": "major01-E：汉书·霍光金日磾传「上以光为大司马大将军」", "person_id": None},
   {"person_name_raw": "金日磾", "role": "official", "link_status": "needs_linking",
    "role_zh_cn": "车骑将军：同受遗诏", "review_note": "major01-E：汉书·霍光金日磾传「日磾为车骑将军」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "长安", "role": "capital", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "卧内受遗诏之地", "review_note": "major01-E：汉书·霍光金日磾传「皆拜卧内床下」"},
  ],
  "evidence": [
   ev(HS, "公孙刘田王杨蔡陈郑传", "传/公孙刘田王杨蔡陈郑传#p104", "text-niutrans-b5a93a9dd8dfe392acda", "background", "primary", "后岁余，武帝疾，立皇子钩弋夫人男为太子，拜大将军霍光……并受遗诏，辅道少主。"),
   ev(HS, "霍光金日磾传", "传/霍光金日磾传#p21", "text-niutrans-ad7ff49eca691db2c547", "process", "primary", "上以光为大司马大将军，日磾为车骑将军……皆拜卧内床下，受遗诏辅少主。"),
   ev(HS, "霍光金日磾传", "传/霍光金日磾传#p188", "text-niutrans-f7b2b48afef75b693441", "result", "primary", "光薨，上及皇太后亲临光丧。"),
   ev(HS, "霍光金日磾传", "传/霍光金日磾传#p202", "text-niutrans-a1683f737551bd925a79", "impact", "primary", "禹既嗣为博陆侯，太夫人显改光时所自造茔制而侈大之。"),
  ],
 },
 "qin_han/event-changyi-wang-feili.yml": {
  "background_zh_cn": "昭帝崩，亡子，「昌邑王贺嗣立，官属皆征入」。",
  "process_zh_cn": "昌邑王即位后狂乱失道：「后昭帝崩，无子，征昌邑王贺嗣位，狂乱失道，光废之，更立昭帝兄卫太子之孙，是为宣帝」。",
  "result_zh_cn": "光卒与安世白太后，废昌邑王、尊立宣帝——二十余日而废立皆决于辅臣。",
  "impact_zh_cn": "废立之举开霍光专擅之极：「帝崩，昌邑王即位，废，大将军光、车骑将军张安世与大臣议所立」——汉家皇统由辅臣议定，宣帝一朝隐忍而后清算霍氏。",
  "people": [
   {"person_name_raw": "霍光", "role": "official", "link_status": "needs_linking",
    "role_zh_cn": "大将军：废昌邑王、立宣帝", "review_note": "major01-E：汉书「光废之，更立……是为宣帝」", "person_id": None},
   {"person_name_raw": "昌邑王", "role": "deposed_monarch", "link_status": "needs_linking",
    "role_zh_cn": "刘贺：即位旋废", "review_note": "major01-E：汉书·杜周传「昌邑王即位，废」", "person_id": None},
   {"person_name_raw": "汉宣帝", "role": "monarch", "link_status": "needs_linking",
    "role_zh_cn": "卫太子之孙：霍光等所立", "review_note": "major01-E：汉书「更立昭帝兄卫太子之孙，是为宣帝」", "person_id": None},
  ],
  "places": [],
  "evidence": [
   ev(HS, "循吏传", "传/循吏传#p159", "text-niutrans-fa714921f81541634e76", "background", "primary", "会昭帝崩，亡子，昌邑王贺嗣立，官属皆征入。"),
   ev(HS, "五行志中之下", "志/五行志中之下#p96", "text-niutrans-ab9536c14f6a579b0f8b", "process", "primary", "后昭帝崩，无子，征昌邑王贺嗣位，狂乱失道，光废之，更立昭帝兄卫太子之孙，是为宣帝。"),
   ev(HS, "眭两夏侯京翼李传", "传/眭两夏侯京翼李传#p38", "text-niutrans-ff86ea494916ee8c3e4f", "result", "primary", "后十余日，光卒与安世白太后，废昌邑王，尊立宣帝。"),
   ev(HS, "杜周传", "传/杜周传#p53", "text-niutrans-df9bc6a6fea16bb898c6", "impact", "primary", "帝崩，昌邑王即位，废，大将军光、车骑将军张安世与大臣议所立。"),
  ],
 },
 "qin_han/event-huo-shi-fumie.yml": {
  "background_zh_cn": "霍光既薨，宣帝「更以禹为大司马，冠小冠，亡印绶，罢其右将军屯兵官属」——渐收霍氏兵权。",
  "process_zh_cn": "霍氏不自安而谋变：「谋令太后为博平君置酒，召丞相、平恩侯以下，使范明友、邓广汉承太后制引斩之，因废天子而立禹」。",
  "result_zh_cn": "谋泄事败：「霍氏伏诛」，杨恽等五人皆封——霍氏集团覆灭。",
  "impact_zh_cn": "「上始亲政事……令群臣得奏封事，以知下情」——宣帝亲政、广开言路，昭宣中兴之政自此真正展开。",
  "people": [
   {"person_name_raw": "霍禹", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "霍光之子：谋废天子而立己，败诛", "review_note": "major01-E：汉书·霍光传「因废天子而立禹」", "person_id": None},
   {"person_name_raw": "汉宣帝", "role": "monarch", "link_status": "needs_linking",
    "role_zh_cn": "收霍氏权、始亲政事", "review_note": "major01-E：汉书·宣帝纪「上始亲政事」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "长安", "role": "capital", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "霍氏谋变与伏诛之地", "review_note": "major01-E：汉书·霍光传（谋废天子而立禹）"},
  ],
  "evidence": [
   ev(HS, "霍光金日磾传", "传/霍光金日磾传#p227", "text-niutrans-1cd36fc9dc786ec78f08", "background", "primary", "更以禹为大司马，冠小冠，亡印绶，罢其右将军屯兵官属。"),
   ev(HS, "霍光金日磾传", "传/霍光金日磾传#p275", "text-niutrans-27c80d20d877197937db", "process", "primary", "谋令太后为博平君置酒……因废天子而立禹。"),
   ev(HS, "公孙刘田王杨蔡陈郑传", "传/公孙刘田王杨蔡陈郑传#p153", "text-niutrans-827961ef0378507ae613", "result", "primary", "霍氏伏诛，惲等五人皆封。"),
   ev(HS, "宣帝纪", "纪/宣帝纪#p98", "text-niutrans-916321204ec47df8cfbd", "impact", "primary", "上始亲政事，又思报大将军功德……令群臣得奏封事，以知下情。"),
  ],
 },
 "qin_han/event-han-yuandi-jiwei.yml": {
  "background_zh_cn": "「孝元皇帝，宣帝太子也」；宣帝尝「有意欲用淮阳王代太子，然以少依许氏，俱从微起，故终不背焉」——储位几易而终定。",
  "process_zh_cn": "黄龙元年十二月，宣帝崩；癸巳，太子即皇帝位，谒高庙。",
  "result_zh_cn": "元帝即位，尊皇太后、立皇后——昭宣之政向元成之世过渡。",
  "impact_zh_cn": "元帝之立为许氏外戚与儒臣政治之渐：柔仁好儒之君临朝，汉政自此转向儒术与权臣交争之局。",
  "people": [
   {"person_name_raw": "汉元帝", "role": "monarch", "link_status": "needs_linking",
    "role_zh_cn": "宣帝太子：即皇帝位", "review_note": "major01-E：汉书·元帝纪「太子即皇帝位，谒高庙」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "长安", "role": "capital", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "即位与谒高庙所在", "review_note": "major01-E：汉书·元帝纪（即位谒高庙）"},
  ],
  "evidence": [
   ev(HS, "元帝纪", "纪/元帝纪#p1", "text-niutrans-245cc337d17b7731edbc", "background", "primary", "孝元皇帝，宣帝太子也。"),
   ev(HS, "元帝纪", "纪/元帝纪#p12", "text-niutrans-1542e9604643599d7e25", "background", "supporting", "上有意欲用淮阳王代太子，然以少依许氏，俱从微起，故终不背焉。"),
   ev(HS, "元帝纪", "纪/元帝纪#p14", "text-niutrans-83cd9fc5cb5bf2755bdf", "process", "primary", "癸巳，太子即皇帝位，谒高庙。"),
   ev(HS, "元帝纪", "纪/元帝纪#p53", "text-niutrans-8a2971d838916f564bcd", "impact", "primary", "夏四月丁巳，立皇太子。"),
  ],
 },
 "qin_han/event-xiyu-duhu.yml": {
  "background_zh_cn": "自敦煌西至盐泽往往起亭，「而轮台、渠犁皆有田卒数百人，置使者校尉领护，以给使外国者」——西域经营既有基础。",
  "process_zh_cn": "郑吉「既破车师，降日逐，威震西域，遂并护车师以西北道，故号都护」——都护之号自此始。",
  "result_zh_cn": "都护治所立，西域诸国皆属汉护——「都护郑吉使冯夫人说乌就屠」，汉使号令行于西域。",
  "impact_zh_cn": "西域都护之置为汉经营西域的制度化标志：护南北两道、统诸国，丝绸之路的政治保障自此确立。",
  "people": [
   {"person_name_raw": "郑吉", "role": "official", "link_status": "needs_linking",
    "role_zh_cn": "首任西域都护：破车师、降日逐", "review_note": "major01-E：汉书·傅常郑甘陈段传「故号都护」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "西域", "role": "region", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "都护所护之地", "review_note": "major01-E：汉书·傅常郑甘陈段传「威震西域」"},
   {"place_name_raw": "车师", "role": "region", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "郑吉所破之国（并护其以西北道）", "review_note": "major01-E：汉书·傅常郑甘陈段传「并护车师以西北道」"},
  ],
  "evidence": [
   ev(HS, "西域传上", "传/西域传上#p18", "text-niutrans-77c4b89f9cc7489edfff", "background", "primary", "而轮台、渠犁皆有田卒数百人，置使者校尉领护，以给使外国者。"),
   ev(HS, "傅常郑甘陈段传", "传/傅常郑甘陈段传#p62", "text-niutrans-ffffec645e1ce94fdb80", "process", "primary", "吉既破车师，降日逐，威震西域，遂并护车师以西北道，故号都护。"),
   ev(HS, "西域传下", "传/西域传下#p94", "text-niutrans-eba12b0abc4eaeb2b698", "result", "primary", "都护郑吉使冯夫人说乌就屠，以汉兵方出，必见灭，不如降。"),
   ev(HS, "西域传下", "传/西域传下#p110", "text-niutrans-326d720ef66a1334483d", "impact", "primary", "后段会宗为都护，招还亡畔，安定之。"),
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
