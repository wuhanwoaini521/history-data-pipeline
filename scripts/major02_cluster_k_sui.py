"""Major Batch 02 · Cluster K：隋 4 事件（开皇之治/大运河开凿/江都兵变/李渊太原起兵）。

SOURCE-BACKED FIRST：evidence 锚定隋书（帝纪/列传）、资治通鉴（隋纪）、旧唐书（高祖纪）。
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
        "review_note": f"major02-K：{work}源引文：「{quote}」；claim_field={field}；anchor=段落精确锚。{note}",
    }


BLOCKS = {
 # ---------------- 1. 开皇之治 ----------------
 "sui_tang/event-kaihuang-zhizhi.yml": {
  "background_zh_cn": "隋有天下之初，李德林每赞平陈之计，高祖以马鞭南指曰「待平陈讫，会以七宝装严公」——混一南北为开皇一朝之宿志。"
                       "开皇初置御史官，朝廷以鲠正者拜治书侍御史，名为称职；高祖躬行节俭、任贤纳谏，政治清明之基由此立。",
  "process_zh_cn": "开皇之政以轻徭薄赋、均平田土为务：诏曰「宁积于人，无藏府库」，河北、河东田租三分减一、兵减半功、调全免；时天下户口岁增，京辅及三河地少人众，乃发使四出均天下之田。"
                   "其后库藏充溢，更辟左藏院以受之；开皇十一年以平陈所得古器多为妖变，悉命毁之——制度与文治并进，俭朴之俗行于上下。",
  "result_zh_cn": "史臣总其治曰：「于是躬节俭，平徭赋，仓廪实，法令行，君子咸乐其生，小人各安其业，强无陵弱，众不暴寡，人物殷阜，朝野欢娱。」"
                  "开皇九年平陈，南北复归一统，天下户数与仓储皆倍于前代，京师、诸州义仓之积至隋末犹为群雄所资。",
  "impact_zh_cn": "开皇之治为唐宋制度所自出：均田、租调、府兵、科举诸制皆定于此际；通鉴记「开皇、仁寿之间，丈夫率衣绢布，不服绫绮，装带不过铜铁骨角，无金玉之饰」，风俗之淳为史家所称。"
                  "然炀帝嗣位，宫室巡游、三征高丽，开皇之积一朝而尽，治乱之对比尤足为后世鉴戒。",
  "people": [
   {"person_name_raw": "隋文帝", "role": "ruler", "link_status": "needs_linking",
    "role_zh_cn": "隋高祖：躬节俭、平徭赋，开皇之治之主", "review_note": "major02-K：隋书·帝纪卷二「于是躬节俭，平徭赋，仓廪实，法令行」", "person_id": None},
   {"person_name_raw": "李德林", "role": "official", "link_status": "needs_linking",
    "role_zh_cn": "隋臣：每赞平陈之计", "review_note": "major02-K：隋书·列传卷七「德林自隋有天下，每赞平陈之计」", "person_id": None},
   {"person_name_raw": "苏威", "role": "official", "link_status": "needs_linking",
    "role_zh_cn": "开皇名臣：与高颎同掌朝政", "review_note": "major02-K：隋书「开皇初，置御史官……名为称职」（人物影）", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "长安", "role": "capital", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "隋都：左藏院、太仓所在", "review_note": "major02-K：通鉴·隋纪二「更辟左藏院以受之」"},
   {"place_name_raw": "陈", "role": "conquered_state", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "开皇九年所平：南北复归一统", "review_note": "major02-K：隋书·帝纪卷二「以平陈所得古器多为妖变」"},
   {"place_name_raw": "河北", "role": "region", "link_status": "needs_linking", "sequence": 3,
    "description_zh_cn": "减租之地：田租三分减一", "review_note": "major02-K：通鉴·隋纪二「河北、河东今年田租三分减一」"},
  ],
  "evidence": [
   ev("隋书", "列传", "列传/卷七#p139", "text-niutrans-05fd03babca1e0a17817", "background", "primary",
      "德林自隋有天下，每赞平陈之计。"),
   ev("隋书", "列传", "列传/卷七#p144", "text-niutrans-87b947c3c59245560b9f", "background", "supporting",
      "后从驾还，在途中，高祖以马鞭南指云：待平陈讫，会以七宝装严公，使自山东无及之者。"),
   ev("隋书", "列传", "列传/卷二十七#p163", "text-niutrans-5645ec2655583010308e", "background", "supporting",
      "开皇初，置御史官，朝廷以毗鲠正，拜治书侍御史，名为称职。"),
   ev("资治通鉴", "隋纪二", "隋纪/隋纪二#p43", "text-niutrans-211cb59a7bb4281aaa43", "process", "primary",
      "于是更辟左藏院以受之。诏曰：宁积于人，无藏府库。河北、河东今年田租三分减一，兵减半功，调全免。时天下户口岁增，京辅及三河地少而人众，衣食不给，帝乃发使四出，均天下之田。"),
   ev("隋书", "帝纪", "帝纪/卷二#p342", "text-niutrans-b3312cd6ea7c6fb67df5", "result", "primary",
      "于是躬节俭，平徭赋，仓廪实，法令行，君子咸乐其生，小人各安其业，强无陵弱，众不暴寡，人物殷阜，朝野欢娱。"),
   ev("隋书", "帝纪", "帝纪/卷二#p67", "text-niutrans-d68c0dc2770d69bad5bb", "result", "supporting",
      "十一年春正月丁酉，以平陈所得古器多为妖变，悉命毁之。"),
   ev("资治通鉴", "隋纪四", "隋纪/隋纪四#p16", "text-niutrans-23478047f93ef72dac48", "impact", "primary",
      "天下化之，开皇、仁寿之间，丈夫率衣绢布，不服绫绮，装带不过铜铁骨角，无金玉之饰。"),
  ],
 },
 # ---------------- 2. 大运河开凿 ----------------
 "sui_tang/event-dayunhe-kaiwa.yml": {
  "background_zh_cn": "隋之漕运自开皇始：开皇初开渠引杜阳水于三畴原，又「开渠，自渭达河，以通运漕」——广通渠之役已见转漕关中之需。"
                       "炀帝即位，以天下承平日久、士马全盛，慨然慕秦皇汉武之事，乃盛治宫室、即事巡游，南北通漕之议遂大举。",
  "process_zh_cn": "大业元年（605年），发河南诸郡男女百余万开通济渠，自西苑引谷、洛水达于河，自板渚引河通于淮；通鉴记「命尚书右丞皇甫议发河南、淮北诸郡民，前后百余万，开通济渠」。"
                   "大业四年春正月，诏发河北诸郡男女百余万开永济渠，引沁水南达于河、北通涿郡，通鉴记「诏发河北诸军五百余万众穿永济渠」。"
                   "自是自江都至涿郡，龙舟可直达：帝自江都御龙舟入通济渠，遂幸于涿郡。",
  "result_zh_cn": "运河既通，帝自江都行幸涿郡，御龙舟，渡河入永济渠；选部、门下、内史、御史四司之官于前船选补，受选者三千余人或徒步随船三千余里，冻馁疲顿，因而致死者什一二——役重民困之弊与漕运之利并见。"
                  "至隋末，永济渠、通济渠犹为诸雄用兵转粮之干道。",
  "impact_zh_cn": "大运河以洛阳为中心，北通涿郡、南达江都、余杭，沟通河、淮、江、海四大水系，为此后唐宋漕运与南北经济交流之第一命脉；"
                  "然役夫数百万、民力凋敝，隋末群盗皆据渠为营（义臣据永济渠为营，化及粮尽渡永济渠），论者以开河与征辽并为隋亡之由。",
  "people": [
   {"person_name_raw": "隋炀帝", "role": "ruler", "link_status": "needs_linking",
    "role_zh_cn": "隋炀帝：诏开通济渠、永济渠，御龙舟幸涿郡", "review_note": "major02-K：隋书·帝纪卷三「发河南诸郡男女百余万，开通济渠」", "person_id": None},
   {"person_name_raw": "皇甫议", "role": "official", "link_status": "needs_linking",
    "role_zh_cn": "尚书右丞：奉命发民开通济渠", "review_note": "major02-K：通鉴·隋纪四「命尚书右丞皇甫议发河南、淮北诸郡民……开通济渠」", "person_id": None},
   {"person_name_raw": "隋文帝", "role": "ruler", "link_status": "needs_linking",
    "role_zh_cn": "隋高祖：开渠自渭达河以通运漕（运河之先声）", "review_note": "major02-K：隋书·帝纪卷一「壬子，开渠，自渭达河，以通运漕」", "person_id": None},
   {"person_name_raw": "杨义臣", "role": "commander", "link_status": "needs_linking",
    "role_zh_cn": "隋将：据永济渠为营讨张金称", "review_note": "major02-K：通鉴·隋纪七「义臣引兵直进抵临清之西，据永济渠为营」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "通济渠", "role": "canal", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "引谷洛达河、引河通淮之渠：大业元年开", "review_note": "major02-K：隋书·帝纪卷三「开通济渠……自板渚引河通于淮」"},
   {"place_name_raw": "永济渠", "role": "canal", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "引沁水南达于河、北通涿郡之渠：大业四年开", "review_note": "major02-K：隋书·帝纪卷三「诏发河北诸郡男女百余万开永济渠」"},
   {"place_name_raw": "江都", "role": "terminus", "link_status": "needs_linking", "sequence": 3,
    "description_zh_cn": "南端重镇：炀帝御龙舟所自", "review_note": "major02-K：隋书·帝纪卷三「上自江都御龙舟入通济渠」"},
   {"place_name_raw": "涿郡", "role": "terminus", "link_status": "needs_linking", "sequence": 4,
    "description_zh_cn": "北端重镇：永济渠所通", "review_note": "major02-K：隋书·帝纪卷三「北通涿郡」"},
  ],
  "evidence": [
   ev("隋书", "帝纪", "帝纪/卷一#p271", "text-niutrans-561165efe73f816e0de3", "background", "primary",
      "壬子，开渠，自渭达河，以通运漕。"),
   ev("隋书", "帝纪", "帝纪/卷一#p173", "text-niutrans-9d3b7c864f23971addde", "background", "supporting",
      "三月戊申，开渠，引杜阳水于三畴原。"),
   ev("隋书", "帝纪", "帝纪/卷三#p70", "text-niutrans-e7482cb54944c17d027f", "process", "primary",
      "辛亥，发河南诸郡男女百余万，开通济渠，自西苑引谷、洛水达于河，自板渚引河通于淮。"),
   ev("资治通鉴", "隋纪四", "隋纪/隋纪四#p186", "text-niutrans-7219aa53bd7bd6c8e718", "process", "primary",
      "辛亥，命尚书右丞皇甫议发河南、淮北诸郡民，前后百馀万，开通济渠。"),
   ev("隋书", "帝纪", "帝纪/卷三#p217", "text-niutrans-e3ce4c16a2d061488f2c", "process", "primary",
      "四年春正月乙巳，诏发河北诸郡男女百余万开永济渠，引沁水，南达于河，北通涿郡。"),
   ev("资治通鉴", "隋纪五", "隋纪/隋纪五#p3", "text-niutrans-ccb2552a12e1f87c5556", "process", "supporting",
      "春，正月，乙巳，诏发河北诸军五百馀万众穿永济渠，引沁水南达于河，北通涿郡。"),
   ev("隋书", "帝纪", "帝纪/卷三#p331", "text-niutrans-ee272dca3030f1b252cd", "result", "primary",
      "乙亥，上自江都御龙舟入通济渠，遂幸于涿郡。"),
   ev("资治通鉴", "隋纪五", "隋纪/隋纪五#p206", "text-niutrans-c5e763a19d657de30fa9", "result", "primary",
      "乙亥，帝自江都行幸涿郡，御龙舟，渡河入永济渠……其受选者三千余人，或徒步随船三千馀里，不得处分，冻馁疲顿，因而致死者什一二。"),
   ev("资治通鉴", "隋纪七", "隋纪/隋纪七#p124", "text-niutrans-7f01038c6f9f379ad735", "impact", "primary",
      "帝遣太仆卿杨义臣讨张金称。金称营于平恩东北，义臣引兵直进抵临清之西，据永济渠为营。", "隋末用兵皆以运河为干道"),
   ev("隋书", "列传", "列传/卷五十#p81", "text-niutrans-b0b476e93cbdb33222fd", "impact", "supporting",
      "化及粮尽，渡永济渠，与密决战于童山，遂入汲郡求军粮。"),
  ],
 },
 # ---------------- 3. 江都兵变 ----------------
 "sui_tang/event-jiangdu-bingbian.yml": {
  "background_zh_cn": "大业十二年，炀帝幸江都宫，以越王侗、光禄大夫段达、太府卿元文都等总留后事；中原群盗蜂起，江都阻绝，从驾骁果思归关中。"
                       "帝括江都人女寡妇以配从兵，又夜见流星坠于江都、日光四散如流血而恶之；宇文化及将乱之夕，宗人虞伋知而告其弟熙——变乱之兆已著。",
  "process_zh_cn": "大业十四年（618年）三月，右屯卫将军宇文化及，武贲郎将司马德戡、元礼，监门直阁裴虔通，将作少监宇文智及等，以骁果作乱，入犯宫闱。"
                   "先是裴蕴共惠绍谋，欲矫诏发郭下兵民、尽取荣公来护儿节度，收在外逆党宇文化及等，仍发羽林殿脚入自西苑，扣门援帝——谋泄而不果，变遂作。",
  "result_zh_cn": "上崩于温室，时年五十；萧后令宫人撤床箦为棺以埋之，化及发后，右御卫将军陈棱奉梓宫于成象殿，葬吴公台下；大唐平江南之后，改葬雷塘。"
                  "化及令裴矩参定仪注，推秦王子浩为帝，以矩为侍内，随化及至河北；俄而宇文化及率众自江都北指黎阳，兵十余万。",
  "impact_zh_cn": "江都之变弑君于行宫，隋室遂亡其政：越王侗于东都称尊号，遣使授李密太尉、魏国公，令先平化及然后入朝辅政——群雄讨逆之局已成；"
                  "化及与密相遇于童山，密知其军少食、利在急战，故不与交锋而遏其归路，化及终败。隋之亡不亡于外寇，而亡于从驾之骁果，论者深叹之。",
  "people": [
   {"person_name_raw": "隋炀帝", "role": "victim", "link_status": "needs_linking",
    "role_zh_cn": "隋炀帝：遇弑于江都温室", "review_note": "major02-K：隋书·帝纪卷四「上崩于温室，时年五十」", "person_id": None},
   {"person_name_raw": "宇文化及", "role": "leader", "link_status": "needs_linking",
    "role_zh_cn": "右屯卫将军：兵变之首，率众北指黎阳", "review_note": "major02-K：隋书·帝纪卷四「右屯卫将军宇文化及……以骁果作乱，入犯宫闱」", "person_id": None},
   {"person_name_raw": "司马德戡", "role": "leader", "link_status": "needs_linking",
    "role_zh_cn": "武贲郎将：兵变同谋", "review_note": "major02-K：隋书·帝纪卷四「武贲郎将司马德戡、元礼」", "person_id": None},
   {"person_name_raw": "裴虔通", "role": "leader", "link_status": "needs_linking",
    "role_zh_cn": "监门直阁：兵变同谋，入犯宫闱", "review_note": "major02-K：隋书·帝纪卷四「监门直阁裴虔通」", "person_id": None},
   {"person_name_raw": "萧后", "role": "supporter", "link_status": "needs_linking",
    "role_zh_cn": "炀帝皇后：撤床箦为棺以埋帝", "review_note": "major02-K：隋书·帝纪卷四「萧后令宫人撤床箦为棺以埋之」", "person_id": None},
   {"person_name_raw": "陈棱", "role": "official", "link_status": "needs_linking",
    "role_zh_cn": "右御卫将军：奉梓宫于成象殿", "review_note": "major02-K：隋书·帝纪卷四「右御卫将军陈棱奉梓宫于成象殿」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "江都", "role": "site", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "兵变地：炀帝行宫所在", "review_note": "major02-K：隋书·帝纪卷四「幸江都宫」"},
   {"place_name_raw": "吴公台", "role": "burial", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "炀帝初葬之地", "review_note": "major02-K：隋书·帝纪卷四「葬吴公台下」"},
   {"place_name_raw": "黎阳", "role": "destination", "link_status": "needs_linking", "sequence": 3,
    "description_zh_cn": "化及率众北指之地", "review_note": "major02-K：隋书·列传卷三十五「率众自江都北指黎阳，兵十余万」"},
   {"place_name_raw": "东都", "role": "capital", "link_status": "needs_linking", "sequence": 4,
    "description_zh_cn": "越王侗称尊号之地", "review_note": "major02-K：隋书·列传卷三十五「会越王侗称尊号」"},
  ],
  "evidence": [
   ev("隋书", "帝纪", "帝纪/卷四#p239", "text-niutrans-16d73e90c2aa8daab2a2", "background", "primary",
      "甲子，幸江都宫，以越王侗、光禄大夫段达、太府卿元文都、检校民部尚书韦津、右武卫将军皇甫无逸、右司郎卢楚等总留后事。"),
   ev("隋书", "帝纪", "帝纪/卷四#p284", "text-niutrans-98ff4be4919db2d57c50", "background", "supporting",
      "九月己丑，帝括江都人女寡妇以配从兵。"),
   ev("隋书", "帝纪", "帝纪/卷四#p278", "text-niutrans-2895ea1fee448490c2b0", "background", "supporting",
      "五月辛酉，夜有流星如彳育攵坠于江都。"),
   ev("隋书", "帝纪", "帝纪/卷四#p298", "text-niutrans-721a021e2709ee19daf9", "process", "primary",
      "二年三月，右屯卫将军宇文化及，武贲郎将司马德戡、元礼，监门直阁裴虔通，将作少监宇文智及……以骁果作乱，入犯宫闱。"),
   ev("隋书", "列传", "列传/卷三十二#p99", "text-niutrans-a777d4e7b829e72fa4df", "process", "supporting",
      "蕴共惠绍谋，欲矫诏发郭下兵民，尽取荣公来护兒节度，收在外逆党宇文化及等。"),
   ev("隋书", "帝纪", "帝纪/卷四#p299", "text-niutrans-83a4c8f2ae53838ff391", "result", "primary",
      "上崩于温室，时年五十。"),
   ev("隋书", "帝纪", "帝纪/卷四#p300", "text-niutrans-3ba4601941263cf620a9", "result", "supporting",
      "萧后令宫人撤床箦为棺以埋之。"),
   ev("隋书", "帝纪", "帝纪/卷四#p301", "text-niutrans-8598afc03c29d79df526", "result", "supporting",
      "化及发后，右御卫将军陈棱奉梓宫于成象殿，葬吴公台下。"),
   ev("隋书", "列传", "列传/卷三十二#p264", "text-niutrans-a2a963bd0a1227aad220", "impact", "primary",
      "令矩参定仪注，推秦王子浩为帝，以矩为侍内，随化及至河北。"),
   ev("隋书", "列传", "列传/卷三十五#p357", "text-niutrans-0a3e12769d5e1a989654", "impact", "supporting",
      "俄而宇文化及杀逆，率众自江都北指黎阳，兵十余万。"),
   ev("隋书", "列传", "列传/卷三十五#p359", "text-niutrans-b7a2ac3ec48776cfa692", "impact", "supporting",
      "会越王侗称尊号，遣使者授密太尉、尚书令、东南道大行台、行军元帅、魏国公，令先平化及，然后入朝辅政。"),
  ],
 },
 # ---------------- 4. 李渊太原起兵 ----------------
 "sui_tang/event-liyuan-qibing.yml": {
  "background_zh_cn": "大业十三年，李渊为太原留守，郡丞王威、武牙郎将高君雅为副；时群贼蜂起、江都阻绝，李世民与晋阳令刘文静首谋，劝举义兵。"
                       "晋阳乡长刘世龙知其谋，以告高祖，高祖阴为之备——起兵之谋内外相济，只待发机。",
  "process_zh_cn": "高祖先发制人：遣开阳府司马刘政会告王威、高君雅谋反，即斩之以徇，遂起义兵；"
                   "从父弟神通起兵鄠县，柴氏妇举兵于司竹，至是并与太宗会，关中豪杰争相应赴。",
  "result_zh_cn": "秋七月壬子，高祖率兵西图关中，以元吉为镇北将军、太原留守；癸丑发自太原，有兵三万。"
                  "京师留守刑部尚书卫文升、右翊卫将军阴世师、京兆郡丞滑仪挟代王侑以拒义师，高祖既破之，以阴世师、滑仪等拒义兵并斩之；癸亥，率百僚备法驾，立代王侑为天子，遥尊炀帝为太上皇，大赦，改元义宁。",
  "impact_zh_cn": "太原起兵以「举义兵」为名，由晋阳一隅而入长安、立代王、改元义宁，隋祚之移遂不可逆；"
                  "次年受禅建唐，凡隋之制度、府兵、仓储皆归唐有——李渊父子以留守之兵借乱而起，实开三百年唐室之基。",
  "people": [
   {"person_name_raw": "李渊", "role": "leader", "link_status": "needs_linking",
    "role_zh_cn": "太原留守→唐高祖：斩王威高君雅、起义兵", "review_note": "major02-K：旧唐书·高祖纪「十三年，为太原留守」；「遂起义兵」", "person_id": None},
   {"person_name_raw": "李世民", "role": "leader", "link_status": "needs_linking",
    "role_zh_cn": "高祖次子：与刘文静首谋劝举义兵", "review_note": "major02-K：旧唐书·高祖纪「太宗与晋阳令刘文静首谋，劝举义兵」", "person_id": None},
   {"person_name_raw": "刘文静", "role": "supporter", "link_status": "needs_linking",
    "role_zh_cn": "晋阳令：首谋起兵", "review_note": "major02-K：旧唐书·高祖纪「太宗与晋阳令刘文静首谋」", "person_id": None},
   {"person_name_raw": "王威", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "太原郡丞：被斩以徇", "review_note": "major02-K：旧唐书·高祖纪「遣开阳府司马刘政会告威等谋反，即斩之以徇」", "person_id": None},
   {"person_name_raw": "高君雅", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "武牙郎将：与王威同被斩", "review_note": "major02-K：旧唐书·高祖纪「郡丞王威、武牙郎将高君雅为副」", "person_id": None},
   {"person_name_raw": "李元吉", "role": "supporter", "link_status": "needs_linking",
    "role_zh_cn": "高祖四子：留守太原", "review_note": "major02-K：旧唐书·高祖纪「以元吉为镇北将军、太原留守」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "太原", "role": "origin", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "起兵之地（晋阳）：高祖留守所", "review_note": "major02-K：旧唐书·高祖纪「癸丑，发自太原，有兵三万」"},
   {"place_name_raw": "关中", "role": "objective", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "西图之目标：入长安之门户", "review_note": "major02-K：旧唐书·高祖纪「高祖率兵西图关中」"},
   {"place_name_raw": "长安", "role": "capital", "link_status": "needs_linking", "sequence": 3,
    "description_zh_cn": "义师所向之都城：立代王、改元义宁", "review_note": "major02-K：旧唐书·高祖纪「立代王侑为天子，遥尊炀帝为太上皇……改元为义宁」"},
   {"place_name_raw": "鄠县", "role": "support_base", "link_status": "needs_linking", "sequence": 4,
    "description_zh_cn": "神通起兵处：与太宗会师", "review_note": "major02-K：旧唐书·高祖纪「神通起兵鄠县」"},
  ],
  "evidence": [
   ev("旧唐书", "高祖纪", "本纪/卷一#p35", "text-niutrans-3c5d7e3f3f615e18de7c", "background", "primary",
      "十三年，为太原留守，郡丞王威、武牙郎将高君雅为副。"),
   ev("旧唐书", "高祖纪", "本纪/卷一#p36", "text-niutrans-8a1153707d04c6f661ee", "background", "primary",
      "群贼蜂起，江都阻绝，太宗与晋阳令刘文静首谋，劝举义兵。"),
   ev("旧唐书", "高祖纪", "本纪/卷一#p40", "text-niutrans-a6abed28381f90bf4559", "background", "supporting",
      "晋阳乡长刘世龙知之，以告高祖，高祖阴为之备。"),
   ev("旧唐书", "高祖纪", "本纪/卷一#p42", "text-niutrans-fa7770577a6044e50bf3", "process", "primary",
      "遣开阳府司马刘政会告威等谋反，即斩之以徇，遂起义兵。"),
   ev("旧唐书", "高祖纪", "本纪/卷一#p72", "text-niutrans-b2d2cbc9b525cc251df9", "process", "supporting",
      "高祖从父弟神通起兵鄠县，柴氏妇举兵于司竹，至是并与太宗会。"),
   ev("旧唐书", "高祖纪", "本纪/卷一#p48", "text-niutrans-22e1ed4e584ad6021191", "result", "primary",
      "秋七月壬子，高祖率兵西图关中，以元吉为镇北将军、太原留守。"),
   ev("旧唐书", "高祖纪", "本纪/卷一#p49", "text-niutrans-ff978510731754a20611", "result", "supporting",
      "癸丑，发自太原，有兵三万。"),
   ev("旧唐书", "高祖纪", "本纪/卷一#p77", "text-niutrans-cc6e76b554c057273ef6", "result", "supporting",
      "京师留守刑部尚书卫文升、右翊卫将军阴世师、京兆郡丞滑仪挟代王侑以拒义师。"),
   ev("旧唐书", "高祖纪", "本纪/卷一#p82", "text-niutrans-dd4a1db4d95e687dbc5d", "impact", "primary",
      "癸亥，率百僚，备法驾，立代王侑为天子，遥尊炀帝为太上皇，大赦，改元为义宁。"),
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
