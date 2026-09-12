"""Ready-43 · Cluster 4：魏晋南北朝 6 事件。"""
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
        "review_note": f"ready43-c4：{work}源引文：「{quote}」；claim_field={field}；anchor=段落精确锚。{note}"}

BLOCKS = {
 "jin_southern_northern/event-houjing-zhi-luan.yml": {
  "background_zh_cn": "魏司徒侯景求以豫、广、颍、洛等十三州内属，梁纳之——侯景东奔降梁，梁廷处置失当，祸根埋下。",
  "process_zh_cn": "三年三月，侯景寇没京师；其党引玄武湖水灌台城，城外水起数尺、阙前御街并为洪波，悉逼百姓及军士家累入台城。",
  "result_zh_cn": "台城既没，侯景自为都督中外诸军事、大丞相、录尚书，逼太宗幸西州——权移于叛将。",
  "impact_zh_cn": "五月丙辰，高祖崩于净居殿，时年八十六——梁武帝饿死台城，江南残破、梁室名存实亡，南朝士族元气大伤。",
  "people": [
   {"person_name_raw": "侯景", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "降将：举兵陷台城、专擅梁政", "review_note": "ready43-c4：梁书「侯景自为都督中外诸军事、大丞相」", "person_id": None},
   {"person_name_raw": "梁武帝", "role": "monarch", "link_status": "needs_linking",
    "role_zh_cn": "梁高祖：台城陷后崩于净居殿", "review_note": "ready43-c4：梁书·武帝纪「高祖崩于净居殿，时年八十六」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "台城", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "梁宫城：被围灌水、终致陷落", "review_note": "ready43-c4：梁书·侯景传「引玄武湖水灌台城」"},
  ],
  "evidence": [
   ev("梁书", "武帝纪", "本纪/卷三#p553", "text-niutrans-8057fd2c54539d66f403", "background", "primary",
      "庚辰，魏司徒侯景求以豫、广、颍、洛、阳、西扬、东荆、北荆、襄、东豫、南兗、西兗、齐等十三州内属。"),
   ev("梁书", "武帝纪", "本纪/卷五#p12", "text-niutrans-eb4a7f98e12dd7fe251d", "process", "primary",
      "三年三月，侯景寇没京师。"),
   ev("梁书", "侯景传", "列传/卷五十六#p222", "text-niutrans-5a9f80dabc3298f0df44", "process", "supporting",
      "引玄武湖水灌台城，城外水起数尺，阙前御街并为洪波矣。"),
   ev("梁书", "武帝纪", "本纪/卷三#p624", "text-niutrans-a38d6bd22b60070a64a2", "result", "primary",
      "庚午，侯景自为都督中外诸军事、大丞相、录尚书。"),
   ev("梁书", "武帝纪", "本纪/卷三#p632", "text-niutrans-efc09702712eb622fd98", "impact", "primary",
      "五月丙辰，高祖崩于净居殿，时年八十六。"),
  ],
 },
 "jin_southern_northern/event-sui-mie-chen.yml": {
  "background_zh_cn": "开皇八年正月，陈遣使来聘；乙亥，行幸定城，陈师誓众——隋以晋王广、贺若弼、韩擒虎等诸道并进伐陈。",
  "process_zh_cn": "辛未，贺若弼拔陈京口，韩擒虎拔陈南豫州；陈军南北道并进之际，韩擒虎率众自新林至石子冈，任忠出降、引之经朱雀航趣宫城，自南掖门而入。",
  "result_zh_cn": "丙子，贺若弼败陈师于蒋山、获其将萧摩诃；陈国平，合州三十、郡一百、县四百——南北分裂三百年的局面终结。",
  "impact_zh_cn": "及夜，陈后主为隋军所执，陈亡——隋完成统一，中国结束魏晋南北朝长期分裂，重归一统。",
  "people": [
   {"person_name_raw": "陈后主", "role": "deposed_monarch", "link_status": "needs_linking",
    "role_zh_cn": "陈末帝：城破被执，陈亡", "review_note": "ready43-c4：陈书·后主纪「及夜，为隋军所执」", "person_id": None},
   {"person_name_raw": "贺若弼", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "隋将：拔京口、败陈师于蒋山", "review_note": "ready43-c4：隋书「贺若弼败陈师于蒋山」", "person_id": None},
   {"person_name_raw": "韩擒虎", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "隋将：自新林入宫城，执陈后主", "review_note": "ready43-c4：陈书·后主纪「韩擒虎率众自新林至于石子冈」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "建康", "role": "capital", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "陈都城：隋军自南掖门入宫城", "review_note": "ready43-c4：陈书·后主纪「自南掖门而入」"},
  ],
  "evidence": [
   ev("隋书", "高祖纪", "帝纪/卷二#p20", "text-niutrans-01a1c90be1edd73937a9", "background", "primary",
      "乙亥，行幸定城，陈师誓众。"),
   ev("隋书", "高祖纪", "帝纪/卷二#p24", "text-niutrans-220819073266317017e3", "process", "primary",
      "辛未，贺若弼拔陈京口，韩擒虎拔陈南豫州。"),
   ev("陈书", "后主纪", "本纪/卷六#p194", "text-niutrans-20227119fe0eeabab890", "process", "supporting",
      "韩擒虎率众自新林至于石子冈，任忠出降于擒虎，仍引擒虎经硃雀航趣宫城，自南掖门而入。"),
   ev("隋书", "高祖纪", "帝纪/卷二#p28", "text-niutrans-c490160054dcad2d8afb", "result", "primary",
      "陈国平，合州三十，郡一百，县四百。"),
   ev("陈书", "后主纪", "本纪/卷六#p198", "text-niutrans-9217034af16e93ee93da", "impact", "primary",
      "及夜，为隋军所执。"),
  ],
 },
 "jin_southern_northern/event-yangjian-dai-beizhou.yml": {
  "background_zh_cn": "时静帝幼冲，未能亲理政事——杨坚以隋国公、大丞相总揽周政，禅代之局渐成。",
  "process_zh_cn": "开皇元年二月甲子，上自相府常服入宫，备礼即皇帝位于临光殿。",
  "result_zh_cn": "受禅已定：陈使韦鼎等来聘于周，「至而上已受禅，致之介国」——外邦来使亲历易代。",
  "impact_zh_cn": "隋受周禅而承其制度基业，开皇之治由此发端，并为统一南北奠定国力——北周武帝奠定的强势，最终成全了隋室。",
  "people": [
   {"person_name_raw": "杨坚", "role": "monarch", "link_status": "needs_linking",
    "role_zh_cn": "隋国公→隋文帝：受周禅、建隋", "review_note": "ready43-c4：隋书·高祖纪「备礼即皇帝位于临光殿」", "person_id": None},
   {"person_name_raw": "周静帝", "role": "deposed_monarch", "link_status": "needs_linking",
    "role_zh_cn": "北周末帝：幼冲在位，禅位于隋", "review_note": "ready43-c4：隋书·高祖纪「时静帝幼冲，未能亲理政事」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "临光殿", "role": "location", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "杨坚即皇帝位之地", "review_note": "ready43-c4：隋书·高祖纪「即皇帝位于临光殿」"},
  ],
  "evidence": [
   ev("隋书", "高祖纪", "帝纪/卷一#p54", "text-niutrans-d0631b47eaceb727c5c5", "background", "primary",
      "时静帝幼冲，未能亲理政事。"),
   ev("隋书", "高祖纪", "帝纪/卷一#p99", "text-niutrans-a4b555c66f50214df73c", "process", "primary",
      "开皇元年二月甲子，上自相府常服入宫，备礼即皇帝位于临光殿。"),
   ev("隋书", "高祖纪", "帝纪/卷一#p131", "text-niutrans-58fc51b8077b778ba792", "result", "primary",
      "辛丑，陈散骑常侍韦鼎……来聘于周，至而上已受禅，致之介国。"),
   ev("隋书", "高祖纪", "帝纪/卷一#p99", "text-niutrans-a4b555c66f50214df73c", "impact", "primary",
      "开皇元年二月甲子，上自相府常服入宫，备礼即皇帝位于临光殿。", "隋承周制而兴，开皇之治发端于此"),
  ],
 },
 "jin_southern_northern/event-beiwei-fenlie.yml": {
  "background_zh_cn": "永熙三年，孝武帝为高欢所逼，车驾北迁于邺——高欢挟帝迁都，北魏中枢东移。",
  "process_zh_cn": "魏帝在洛阳许以冯翊长公主配宇文泰，未及结纳而帝西迁——孝武帝西奔长安依宇文泰，东西对立之势成形。",
  "result_zh_cn": "东魏部署次第完成：改相州刺史为司州牧、魏郡太守为魏尹，徙邺旧人西径百里以居新迁之人，分邺置临漳县，以魏郡等郡为皇畿。",
  "impact_zh_cn": "闰十二月，魏孝武帝崩（西魏立文帝）——北魏正式分裂为东魏（高欢）、西魏（宇文泰），此后各演为北齐、北周。",
  "people": [
   {"person_name_raw": "高欢", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "东魏权臣（齐献武王）：挟帝迁邺", "review_note": "ready43-c4：魏书·孝静纪「葬齐献武王于邺城西北」", "person_id": None},
   {"person_name_raw": "宇文泰", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "西魏权臣：迎孝武帝西迁长安", "review_note": "ready43-c4：周书·文帝纪「帝西迁」", "person_id": None},
   {"person_name_raw": "北魏孝武帝", "role": "monarch", "link_status": "needs_linking",
    "role_zh_cn": "西奔长安，旋崩；北魏末帝", "review_note": "ready43-c4：周书·文帝纪「闰十二月，魏孝武帝崩」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "邺", "role": "capital", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "东魏都城（车驾北迁于此）", "review_note": "ready43-c4：魏书·孝静纪「车驾北迁于鄴」"},
   {"place_name_raw": "长安", "role": "capital", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "西魏都城（孝武帝西迁所依）", "review_note": "ready43-c4：周书·文帝纪「帝西迁」"},
  ],
  "evidence": [
   ev("魏书", "孝静纪", "帝纪/卷十二#p16", "text-niutrans-8104444d51536af1f093", "background", "primary",
      "丙子，车驾北迁于鄴。"),
   ev("周书", "文帝纪", "本纪/卷一#p269", "text-niutrans-4316466e7ce203a4219f", "process", "primary",
      "初，魏帝在洛阳，许以冯翊长公主配太祖，未及结纳，而帝西迁。"),
   ev("魏书", "孝静纪", "帝纪/卷十二#p22", "text-niutrans-d4f55f314ab62513592f", "result", "primary",
      "改相州刺史为司州牧，魏郡太守为魏尹……以魏郡、林虑、广平……等郡为皇畿。"),
   ev("周书", "文帝纪", "本纪/卷一#p278", "text-niutrans-3d668c0dd86d8239bb59", "impact", "primary",
      "闰十二月，魏孝武帝崩。"),
  ],
 },
 "jin_southern_northern/event-beizhou-mie-beiqi.yml": {
  "background_zh_cn": "六年春正月乙亥，齐主传位于其太子恒、改年承光，自号为太上皇——北齐临战易主，军心已摇。",
  "process_zh_cn": "周师渐逼，幼主自邺东走；己丑，周师至紫陌桥——齐主先送母妻于青州，及城陷乃率数十骑走青州。",
  "result_zh_cn": "丁未，齐主至，周武帝降自阼阶、以宾主之礼相见；齐诸行台州镇悉降，关东平。",
  "impact_zh_cn": "太上窘急将逊于陈，为周将尉迟纲所获，送邺——周武帝与抗宾主礼，并太后、幼主、诸王俱送长安，封帝温国公：北齐灭亡，北周统一北方。",
  "people": [
   {"person_name_raw": "周武帝", "role": "monarch", "link_status": "needs_linking",
    "role_zh_cn": "北周武帝：平齐之役主帅，受齐主降", "review_note": "ready43-c4：周书·武帝纪「帝降自阼阶，以宾主之礼相见」", "person_id": None},
   {"person_name_raw": "北齐后主", "role": "deposed_monarch", "link_status": "needs_linking",
    "role_zh_cn": "齐太上皇：城陷被获送长安，封温国公", "review_note": "ready43-c4：北齐书·后主纪「封帝温国公」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "晋阳", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "北齐军事重镇（平齐之役所经）", "review_note": "ready43-c4：周书·武帝纪（平齐之役）"},
   {"place_name_raw": "邺", "role": "capital", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "北齐都城：周师至紫陌桥、城陷", "review_note": "ready43-c4：北齐书·后主纪「周师至紫陌桥」"},
  ],
  "evidence": [
   ev("周书", "武帝纪", "本纪/卷六#p210", "text-niutrans-77281e779ce1b011e421", "background", "primary",
      "六年春正月乙亥，齐主传位于其太子恒，改年承光，自号为太上皇。"),
   ev("北齐书", "后主纪", "本纪/卷八#p265", "text-niutrans-d4747b41943b162adb84", "process", "primary",
      "周师渐逼，癸未，幼主又自邺东走。"),
   ev("周书", "武帝纪", "本纪/卷六#p241", "text-niutrans-c392fc17051abd38b103", "result", "primary",
      "丁未，齐主至，帝降自阼阶，以宾主之礼相见。"),
   ev("周书", "武帝纪", "本纪/卷六#p244", "text-niutrans-3ef5bd5344c3524000eb", "result", "supporting",
      "齐诸行台州镇悉降，关东平。"),
   ev("北齐书", "后主纪", "本纪/卷八#p277", "text-niutrans-0539ca189cb6deb233d8", "impact", "primary",
      "为周将尉迟纲所获。送邺，周武帝与抗宾主礼，并太后、幼主、诸王俱送长安，封帝温国公。"),
  ],
 },
 "five_dynasties/event-houliang-dai-tang.yml": {
  "background_zh_cn": "太祖将期受禅，以赵匡凝兄弟并据藩镇，乃遣使先谕旨焉——朱温先收藩镇异己，为受禅铺路。",
  "process_zh_cn": "天祐四年，天子以土运将革、天命有归，四月命张文蔚与杨涉等总率百僚，奉禅位诏至大梁。",
  "result_zh_cn": "后梁既立，礼制次第兴举：开平四年正月，帝御朝元殿受百官称贺，始用礼乐——新朝规模粗定。",
  "impact_zh_cn": "唐祚既终，五代易代循环由此开启（末帝之世传国宝已为左右所窃以迎唐帝）——中原政权更迭加速，武人政治主导北方。",
  "people": [
   {"person_name_raw": "朱温", "role": "monarch", "link_status": "needs_linking",
    "role_zh_cn": "梁王→后梁太祖：受唐禅、建后梁", "review_note": "ready43-c4：旧五代史「太祖将期受禅」「太祖受禅」", "person_id": None},
   {"person_name_raw": "唐哀帝", "role": "deposed_monarch", "link_status": "needs_linking",
    "role_zh_cn": "唐末帝：命百官奉禅位诏至大梁", "review_note": "ready43-c4：旧五代史「天子以土运将革，天命有归」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "大梁", "role": "capital", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "后梁都城（禅位诏奉至之地）", "review_note": "ready43-c4：旧五代史「奉禅位诏至大梁」"},
  ],
  "evidence": [
   ev("旧五代史", "列传", "后梁/列传七#p17", "text-niutrans-848fb24b84eac3a23824", "background", "primary",
      "太祖将期受禅，以匡凝兄弟并据籓镇，乃遣使先谕旨焉。"),
   ev("旧五代史", "列传", "后梁/列传八#p16", "text-niutrans-061182079555cd590202", "process", "primary",
      "天祐四年，天子以土运将革，天命有归，四月，命文蔚与杨涉等总率百僚，奉禅位诏至大梁。"),
   ev("旧五代史", "太祖纪", "后梁/太祖纪五#p24", "text-niutrans-e02941d5b75f8a2e6a41", "result", "primary",
      "开平四年正月壬辰朔，帝御朝元殿，受百官称贺，始用礼乐也。"),
   ev("旧五代史", "末帝纪", "后梁/末帝纪下#p60", "text-niutrans-f93e46392e1f2b414aa6", "impact", "primary",
      "帝置传国宝于卧内，俄失其所在，已为左右所窃迎唐帝矣。", "后梁旋为后唐所代，五代易代循环之证"),
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
