"""Ready-43 · Cluster 2：唐 4 事件（玄武门之变/唐建国/武周建国/神龙政变）。"""
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
        "review_note": f"ready43-c2：{work}源引文：「{quote}」；claim_field={field}；anchor=段落精确锚。{note}"}

BLOCKS = {
 "sui_tang/event-xuanwumen-zhibian.yml": {
  "background_zh_cn": "九年，皇太子建成、齐王元吉谋害太宗；建成尝私使募壮士送长安——秦王功高望重，与东宫、齐府的矛盾不可调和。",
  "process_zh_cn": "六月四日，长孙无忌与尉迟敬德、侯君集、张公谨等九人入玄武门讨建成、元吉，平之；当日世民射建成、杀之。",
  "result_zh_cn": "八月癸亥，高祖传位于皇太子，太宗即位于东宫显德殿——政权交接完成。",
  "impact_zh_cn": "贞观元年春正月乙酉改元——玄武门之变以李世民继位收场，中国进入「贞观之治」。",
  "people": [
   {"person_name_raw": "李世民", "role": "monarch", "link_status": "needs_linking",
    "role_zh_cn": "秦王→唐太宗：玄武门之变主谋、继位", "review_note": "ready43-c2：旧唐书·太宗纪「太宗即位于东宫显德殿」", "person_id": None},
   {"person_name_raw": "李建成", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "皇太子：玄武门之变中被杀", "review_note": "ready43-c2：通鉴唐纪七「世民射建成，杀之」", "person_id": None},
   {"person_name_raw": "李元吉", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "齐王：与建成同谋，变中被讨平", "review_note": "ready43-c2：旧唐书·长孙无忌传「入玄武门讨建成、元吉，平之」", "person_id": None},
   {"person_name_raw": "尉迟敬德", "role": "supporter", "link_status": "needs_linking",
    "role_zh_cn": "秦府骁将：随入玄武门", "review_note": "ready43-c2：旧唐书「无忌与尉迟敬德……等九人」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "玄武门", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "事变发生地（长安宫城北门）", "review_note": "ready43-c2：旧唐书·长孙无忌传「入玄武门讨建成、元吉」"},
  ],
  "evidence": [
   ev("旧唐书", "太宗纪", "本纪/卷二#p207", "text-niutrans-b5ad5ecf1a8f336d93c1", "background", "primary",
      "九年，皇太子建成、齐王元吉谋害太宗。"),
   ev("资治通鉴", "唐纪七", "唐纪/唐纪七#p13", "text-niutrans-616c9fc983daeb14e7c7", "background", "supporting",
      "建成与之亲厚，私使募壮士送长安。"),
   ev("旧唐书", "长孙无忌传", "列传/卷十五#p125", "text-niutrans-e25ed27e04e2e3d211e4", "process", "primary",
      "六月四日，无忌与尉迟敬德……等九人，入玄武门讨建成、元吉，平之。"),
   ev("资治通鉴", "唐纪七", "唐纪/唐纪七#p335", "text-niutrans-6a1bda7b86bfbc6e3b2c", "process", "supporting",
      "世民从而呼之，元吉张弓射世民，再三不彀，世民射建成，杀之。"),
   ev("旧唐书", "太宗纪", "本纪/卷二#p220", "text-niutrans-06b1baeb390891783f48", "result", "primary",
      "八月癸亥，高祖传位于皇太子，太宗即位于东宫显德殿。"),
   ev("旧唐书", "太宗纪", "本纪/卷二#p252", "text-niutrans-7f62948a1cf63f7fb692", "impact", "primary",
      "贞观元年春正月乙酉，改元。"),
  ],
 },
 "sui_tang/event-tang-jianguo.yml": {
  "background_zh_cn": "春正月丁未朔，隋恭帝诏唐王剑履上殿、赞拜不名；戊辰，诏以十郡益唐国，以唐王为相国、总百揆，唐国置丞相以下官，又加九锡——禅代之礼次第完备。",
  "process_zh_cn": "戊午，隋恭帝禅位于唐，逊居代邸。",
  "result_zh_cn": "甲子，唐王即皇帝位于太极殿，遣刑部尚书萧造告天于南郊，大赦，改元——唐兴而隋统终结。",
  "impact_zh_cn": "大赦改元、告天南郊，唐承隋制而立——隋唐易代以「禅让」形式完成，唐室自此开启三百年基业。",
  "people": [
   {"person_name_raw": "李渊", "role": "monarch", "link_status": "needs_linking",
    "role_zh_cn": "唐高祖：受禅即位、唐朝开国", "review_note": "ready43-c2：通鉴唐纪一「唐王即皇帝位于太极殿」", "person_id": None},
   {"person_name_raw": "隋恭帝", "role": "deposed_monarch", "link_status": "needs_linking",
    "role_zh_cn": "隋末代皇帝：禅位逊居代邸", "review_note": "ready43-c2：通鉴唐纪一「隋恭帝禅位于唐，逊居代邸」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "太极殿", "role": "location", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "唐王即位之地（长安宫城正殿）", "review_note": "ready43-c2：通鉴唐纪一「唐王即皇帝位于太极殿」"},
  ],
  "evidence": [
   ev("资治通鉴", "唐纪一", "唐纪/唐纪一#p4", "text-niutrans-d9b0524ca2e68d55fd8b", "background", "primary",
      "春，正月，丁未朔，隋恭帝诏唐王剑履上殿，赞拜不名。"),
   ev("资治通鉴", "唐纪一", "唐纪/唐纪一#p148", "text-niutrans-fe87494963d478f2e794", "background", "supporting",
      "戊辰，隋恭帝诏以十郡益唐国，仍以唐王为相国，总百揆……又加九锡。"),
   ev("资治通鉴", "唐纪一", "唐纪/唐纪一#p240", "text-niutrans-d996903b432b80669377", "process", "primary",
      "戊午，隋恭帝禅位于唐，逊居代邸。"),
   ev("资治通鉴", "唐纪一", "唐纪/唐纪一#p241", "text-niutrans-179f6b1a52857dfa3227", "result", "primary",
      "甲子，唐王即皇帝位于太极殿，遣刑部尚书萧造告天于南郊，大赦，改元。"),
   ev("资治通鉴", "唐纪一", "唐纪/唐纪一#p244", "text-niutrans-1f70b5ba029068ec4420", "impact", "primary",
      "隋炀帝凶问至东都，戊辰，留守官奉越王即皇帝位，大赦，改元皇泰。", "隋室残余立越王，天下归唐之势已成"),
  ],
 },
 "sui_tang/event-wu-zhou-jianguo.yml": {
  "background_zh_cn": "九月丙子，侍御史傅游艺帅关中百姓九百余人诣阙上表，请改国号曰周、赐皇帝姓武氏；太后命有司议崇先庙室数，减唐太庙为五室——易姓之议起于符命与朝议。",
  "process_zh_cn": "乙酉，上尊号曰圣神皇帝，以皇帝为皇嗣、赐姓武氏，以皇太子为皇孙。",
  "result_zh_cn": "改元为天授，大赦天下，赐酺七日——武周代唐立国。",
  "impact_zh_cn": "十二月己酉，神皇拜洛水、受「天授圣图」——以符命受图确立新朝天命，武周（则天皇帝）之治自此展开。",
  "people": [
   {"person_name_raw": "武则天", "role": "monarch", "link_status": "needs_linking",
    "role_zh_cn": "则天皇后：受尊号圣神皇帝、改国号周", "review_note": "ready43-c2：旧唐书·则天皇后纪「改元为天授」；通鉴唐纪二十「上尊号曰圣神皇帝」", "person_id": None},
   {"person_name_raw": "傅游艺", "role": "supporter", "link_status": "needs_linking",
    "role_zh_cn": "侍御史：率关中百姓上表请改国号", "review_note": "ready43-c2：通鉴唐纪二十「傅游艺帅关中百姓九百馀人诣阙上表」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "洛水", "role": "location", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "神皇拜洛受图之地", "review_note": "ready43-c2：旧唐书·则天皇后纪「神皇拜洛水，受天授圣图」"},
  ],
  "evidence": [
   ev("资治通鉴", "唐纪二十", "唐纪/唐纪二十#p299", "text-niutrans-98ffe1ad8ff26ad82599", "background", "primary",
      "九月，丙子，侍御史汲人傅游艺帅关中百姓九百馀人诣阙上表，请改国号曰周，赐皇帝姓武氏。"),
   ev("资治通鉴", "唐纪二十", "唐纪/唐纪二十#p45", "text-niutrans-0f9557b617b280d6f0fb", "background", "supporting",
      "太后命有司议崇先庙室数……又减唐太庙为五室。"),
   ev("资治通鉴", "唐纪二十", "唐纪/唐纪二十#p304", "text-niutrans-98e4e6b8b55dab016506", "process", "primary",
      "乙酉，上尊号曰圣神皇帝，以皇帝为皇嗣，赐姓武氏。"),
   ev("旧唐书", "则天皇后纪", "本纪/卷六#p107", "text-niutrans-14e2f5c018e8668359c8", "result", "primary",
      "改元为天授，大赦天下，赐酺七日。"),
   ev("旧唐书", "则天皇后纪", "本纪/卷六#p83", "text-niutrans-bb072e511c105439223c", "impact", "primary",
      "十二月己酉，神皇拜洛水，受 天授圣图 ，是日还宫。"),
  ],
 },
 "sui_tang/event-shenlong-zhengbian.yml": {
  "background_zh_cn": "则天晚年宠臣张易之及其弟昌宗置控鹤府官员，寻改奉宸府，班在御史大夫下——二张用事，朝局不安。",
  "process_zh_cn": "癸亥，麟台监张易之与弟司仆卿昌宗反，皇太子率左右羽林军桓彦范、敬晖等，以羽林兵入禁中诛之。",
  "result_zh_cn": "丙午，中宗即位——李唐复辟。",
  "impact_zh_cn": "冬十一月壬寅，则天将大渐，遗制祔庙、归陵，令去帝号、称则天大圣皇后——武周政权终结，李唐皇统恢复，武氏以皇后身份祔葬乾陵。",
  "people": [
   {"person_name_raw": "张易之", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "则天宠臣：神龙政变中被诛", "review_note": "ready43-c2：旧唐书·则天皇后纪「张易之与弟司仆卿昌宗反……诛之」", "person_id": None},
   {"person_name_raw": "唐中宗", "role": "monarch", "link_status": "needs_linking",
    "role_zh_cn": "皇太子：政变后即位复位", "review_note": "ready43-c2：通鉴唐纪二十三「丙午，中宗即位」", "person_id": None},
   {"person_name_raw": "桓彦范", "role": "supporter", "link_status": "needs_linking",
    "role_zh_cn": "羽林军将领：率兵入禁中诛二张", "review_note": "ready43-c2：旧唐书「皇太子率左右羽林军桓彦范、敬晖等」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "洛阳", "role": "capital", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "政变发生地（神都禁中/上阳宫）", "review_note": "ready43-c2：旧唐书·则天皇后纪（禁中诛二张、崩于上阳宫）"},
  ],
  "evidence": [
   ev("旧唐书", "则天皇后纪", "本纪/卷六#p214", "text-niutrans-792b15823cf418d7c398", "background", "primary",
      "初为宠臣张易之及其弟昌宗置控鹤府官员，寻改为奉宸府，班在御史大夫下。"),
   ev("旧唐书", "则天皇后纪", "本纪/卷六#p278", "text-niutrans-68fd7e2383299f0bbf53", "process", "primary",
      "癸亥，麟台监张易之与弟司仆卿昌宗反，皇太子率左右羽林军桓彦范、敬晖等，以羽林兵入禁中诛之。"),
   ev("资治通鉴", "唐纪二十三", "唐纪/唐纪二十三#p444", "text-niutrans-8aedc010f30b9223f043", "result", "primary",
      "丙午，中宗即位。"),
   ev("旧唐书", "则天皇后纪", "本纪/卷六#p282", "text-niutrans-59b198ebbf9637e9d53b", "impact", "primary",
      "则天将大渐，遗制祔庙、归陵，令去帝号，称则天大圣皇后。"),
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
