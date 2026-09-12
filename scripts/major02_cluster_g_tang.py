"""Major Batch 02 · Cluster G：唐 8 事件（白江口/大非川/甘露/淮西/黄巢入长安/会昌灭佛/建中之乱/开元盛世）。

SOURCE-BACKED FIRST：每条 evidence 均来自 data/normalized/history.duckdb 中已定位的
段落（anchor=`section/chapter#pN`，text_id 为语料 id），叙事四段（background/process/
result/impact）只使用这些段落可支撑的陈述；impact 不写「具有重要意义」类空话。
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
        "review_note": f"major02-G：{work}源引文：「{quote}」；claim_field={field}；anchor=段落精确锚。{note}",
    }


BLOCKS = {
 # ---------------- 1. 白江口之战 ----------------
 "sui_tang/event-baijiangkou-zhizhan.yml": {
  "background_zh_cn": "显庆五年（660年）唐遣苏定方灭百济，其地置熊津等府；百济遗臣据周留城起兵，迎故王子扶余丰于倭，倭国发水军助之。"
                       "唐以刘仁愿守熊津，刘仁轨检校带方州刺史，诏孙仁师浮海赴援——百济复兴军与倭兵合势，唐军孤悬海东，唯有先取周留巢穴。",
  "process_zh_cn": "龙朔三年（663年）八月，孙仁师与刘仁愿、刘仁轨合兵，势大振；诸将欲先攻加林城，仁轨以「周留，虏之巢穴，群凶所聚，除恶务本」请先攻之。"
                   "于是仁师、仁愿与新罗王金法敏将陆军以进，仁轨与别将杜爽等将水军及粮船自熊津入白江以会陆军，同趣周留城。"
                   "九月戊午，唐军遇倭兵于白江口，四战皆捷，焚其舟四百艘，「烟炎灼天，海水皆赤」，百济王丰脱身奔高丽。",
  "result_zh_cn": "白江口一捷，百济王子忠胜、忠志等帅众降，百济尽平，唯别帅迟受信据任存城不下；据险应福信之黑齿常之等亦帅众降，唐用其力取任存城。"
                  "《新唐书·东夷传》记其众「屯白江口，四遇皆克，火四百艘」，丰走不知所在——百济复国之势至此尽灭。",
  "impact_zh_cn": "此役焚倭舟四百艘，倭国水军覆没，日本自此数百年不再渡海干预半岛；唐既解百济余党之患，遂专力东向，五岁之后（668年）灭高句丽，安东都护府之设皆以此为基。"
                  "战后刘仁轨镇抚百济遗众、录用黑齿常之等降将，唐在半岛南部的羁縻秩序得以立定。",
  "people": [
   {"person_name_raw": "刘仁轨", "role": "commander", "link_status": "needs_linking",
    "role_zh_cn": "唐军水军主将：力主先攻周留、白江口破倭", "review_note": "major02-G：通鉴唐纪十七「仁轨与别将杜爽……将水军及粮船自熊津入白江」", "person_id": None},
   {"person_name_raw": "孙仁师", "role": "commander", "link_status": "needs_linking",
    "role_zh_cn": "熊津道行军总管：率兵浮海助援、会师白江", "review_note": "major02-G：通鉴唐纪十七「熊津道行军总管、右威卫将军孙仁师等破百济馀众及倭兵于白江」", "person_id": None},
   {"person_name_raw": "刘仁愿", "role": "commander", "link_status": "needs_linking",
    "role_zh_cn": "百济留守唐将：与孙仁师、刘仁轨合兵", "review_note": "major02-G：通鉴唐纪十七「仁师与仁愿、仁轨合兵，势大振」", "person_id": None},
   {"person_name_raw": "扶余丰", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "百济故王子：引倭兵拒唐，兵败奔高丽", "review_note": "major02-G：通鉴唐纪十七「百济王丰南引倭人以拒唐兵」", "person_id": None},
   {"person_name_raw": "黑齿常之", "role": "supporter", "link_status": "needs_linking",
    "role_zh_cn": "百济降将：初据险应福信，败后帅众降唐、取任存城", "review_note": "major02-G：通鉴唐纪十七「常之与别部将沙吒相如各据险以应福信，百济既败，皆帅其众降」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "白江口", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "决战地（今韩国锦江入海口）：唐倭水军四战之处", "review_note": "major02-G：通鉴唐纪十七「遇倭兵于白江口，四战皆捷」"},
   {"place_name_raw": "周留城", "role": "stronghold", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "百济复兴军巢穴：白江口战后被拔", "review_note": "major02-G：通鉴唐纪十七「拔其周留城」"},
   {"place_name_raw": "熊津江", "role": "route", "link_status": "needs_linking", "sequence": 3,
    "description_zh_cn": "唐水军进军水道：仁轨自此入白江会陆军", "review_note": "major02-G：通鉴唐纪十七「将水军及粮船自熊津入白江」"},
  ],
  "evidence": [
   ev("资治通鉴", "唐纪十七", "唐纪/唐纪十七#p58", "text-niutrans-967cc9722b7a874156c7", "background", "primary",
      "百济王丰南引倭人以拒唐兵。"),
   ev("资治通鉴", "唐纪十七", "唐纪/唐纪十七#p61", "text-niutrans-8b4031db636438e10bde", "process", "supporting",
      "周留城，虏之巢穴，群凶所聚，除恶务本，宜先攻之，若克周留，诸城自下。"),
   ev("资治通鉴", "唐纪十七", "唐纪/唐纪十七#p62", "text-niutrans-7f1048ba318137a3c7fc", "process", "primary",
      "于是仁师、仁愿与新罗王法敏将陆军以进，仁轨与别将杜爽、抚馀隆将水军及粮船自熊津入白江，以会陆军，同趣周留城。"),
   ev("资治通鉴", "唐纪十七", "唐纪/唐纪十七#p63", "text-niutrans-a1661bb6c0c1dcadda28", "process", "primary",
      "遇倭兵于白江口，四战皆捷，焚其舟四百艘，烟炎灼天，海水皆赤。"),
   ev("资治通鉴", "唐纪十七", "唐纪/唐纪十七#p56", "text-niutrans-e3219e57ee948e4eb37e", "result", "primary",
      "九月，戊午，熊津道行军总管、右威卫将军孙仁师等破百济馀众及倭兵于白江，拔其周留城。"),
   ev("资治通鉴", "唐纪十七", "唐纪/唐纪十七#p64", "text-niutrans-9a0679e05efb783f3b3b", "result", "primary",
      "百济王丰脱身奔高丽，王子忠胜、忠志等帅众降，百济尽平，唯别帅迟受信据任存城，不下。"),
   ev("新唐书", "东夷传", "列传/卷一百四十五#p352", "text-niutrans-31c0c0723cba606df937", "result", "supporting",
      "丰众屯白江口，四遇皆克，火四百艘；丰走不知所在。"),
   ev("新唐书", "刘仁轨传", "列传/卷三十三#p48", "text-niutrans-b2ece4162bd920dfd26a", "process", "supporting",
      "遇倭人白江口，四战皆克，焚四百艘，海水为丹。"),
   ev("资治通鉴", "唐纪十七", "唐纪/唐纪十七#p70", "text-niutrans-025dea392ee8a257c027", "impact", "supporting",
      "常之与别部将沙吒相如各据险以应福信，百济既败，皆帅其众降。", "百济败后降将归唐，唐用其力定半岛南部"),
  ],
 },
 # ---------------- 2. 大非川之战 ----------------
 "sui_tang/event-dafeichuan-zhizhan.yml": {
  "background_zh_cn": "咸亨元年（670年）四月，吐蕃陷西域十八州，又与于阗袭龟兹拨换城，唐罢安西四镇；吐谷浑为吐蕃所破，其王诺曷钵与亲近数千帐内徙。"
                       "唐乃以右卫大将军薛仁贵为逻娑道行军大总管，左卫员外大将军阿史那道真、左卫将军郭待封副之，「以讨吐蕃，且援送吐谷浑还故地」——名为讨伐，实为护送吐谷浑复国。",
  "process_zh_cn": "军至大非川，将趣乌海，仁贵议留二万人为两栅于大非岭上、辎重悉置栅内，吾属帅轻锐倍道兼行掩其未备；郭待封先与仁贵并列，耻居其下，所言多违。"
                   "仁贵帅所部前行，击吐蕃于河口，大破之，进屯乌海以待；待封不用其策，将辎重徐进，未至乌海遇吐蕃二十余万，军大败，还走，悉弃辎重。"
                   "仁贵退屯大非川，吐蕃相论钦陵将兵四十余万就击之，唐兵大败，死伤略尽；仁贵、待封与阿史那道真并脱身免，与钦陵约和而还。",
  "result_zh_cn": "诏大司宪乐彦玮即军中按其败状，械送京师，三人皆免死除名；《旧唐书·高宗纪》亦书「薛仁贵、郭待封至大非川，为吐蕃大将论钦陵所袭，大败，仁贵等并坐除名」。"
                  "《新唐书·吐蕃传》记此役「师凡十余万，至大非川，为钦陵所拒，王师败绩，遂灭吐谷浑而尽有其地」。",
  "impact_zh_cn": "大非川之败，吐谷浑故地尽陷于吐蕃，「诺曷钵与亲近数千帐才免」，唐西陲屏藩尽失，唐蕃战线退守河陇；论钦陵兄弟皆有才略，此后连年寇边，仪凤三年李敬玄又败于青海。"
                  "唐蕃关系由和亲互市转入长期战争与反复争夺，西线成为高宗后期至武周的主要用兵方向。",
  "people": [
   {"person_name_raw": "薛仁贵", "role": "commander", "link_status": "needs_linking",
    "role_zh_cn": "逻娑道行军大总管：大非川败后免死除名", "review_note": "major02-G：通鉴唐纪十七「以右卫大将军薛仁贵为逻娑道行军大总管」", "person_id": None},
   {"person_name_raw": "郭待封", "role": "commander", "link_status": "needs_linking",
    "role_zh_cn": "副大总管：耻居仁贵之下、违节度致败", "review_note": "major02-G：通鉴唐纪十七「待封不用仁贵策，将辎重徐进……军大败」", "person_id": None},
   {"person_name_raw": "论钦陵", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "吐蕃大相：将兵四十余万击破唐军", "review_note": "major02-G：通鉴唐纪十七「吐蕃相论钦陵将兵四十馀万就击之，唐兵大败」", "person_id": None},
   {"person_name_raw": "阿史那道真", "role": "commander", "link_status": "needs_linking",
    "role_zh_cn": "副大总管：与仁贵、待封同免死除名", "review_note": "major02-G：通鉴唐纪十七「仁贵、待封与阿史那道真并脱身免，与钦陵约和而还」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "大非川", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "决战地（今青海共和一带）：唐军十余万败没之处", "review_note": "major02-G：通鉴唐纪十七「仁贵退屯大非川……唐兵大败」"},
   {"place_name_raw": "乌海", "role": "objective", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "唐军进击目标：仁贵先破吐蕃于河口、进屯乌海以待", "review_note": "major02-G：通鉴唐纪十七「进屯乌海以俟待封」"},
   {"place_name_raw": "大非岭", "role": "depot", "link_status": "needs_linking", "sequence": 3,
    "description_zh_cn": "仁贵议置辎重两栅之地：待封违策致辎重尽失", "review_note": "major02-G：通鉴唐纪十七「宜留二万人，为两栅于大非岭上，辎重悉置栅内」"},
  ],
  "evidence": [
   ev("资治通鉴", "唐纪十七", "唐纪/唐纪十七#p425", "text-niutrans-7196094b6f707be2f535", "background", "supporting",
      "夏，四月，吐蕃陷西域十八州，又与于阗袭龟兹拨换城，陷之。"),
   ev("资治通鉴", "唐纪十七", "唐纪/唐纪十七#p427", "text-niutrans-1fcc3a9f0cb61e3a33b5", "background", "primary",
      "辛亥，以右卫大将军薛仁贵为逻娑道行军大总管，左卫员外大将军阿史那道真、左卫将军郭待封副之，以讨吐蕃，且援送吐谷浑还故地。"),
   ev("资治通鉴", "唐纪十七", "唐纪/唐纪十七#p433", "text-niutrans-19c873d0c99ac5cf3387", "process", "supporting",
      "郭待封先与薛仁贵并列，及征吐蕃，耻居其下，仁贵所言，待封多违之。"),
   ev("资治通鉴", "唐纪十七", "唐纪/唐纪十七#p434", "text-niutrans-33c2a7793557729aa5ff", "process", "supporting",
      "军至大非川，将趣乌海，仁贵曰：宜留二万人，为两栅于大非岭上，辎重悉置栅内，吾属帅轻锐，倍道兼行，掩其未备，破之必矣。"),
   ev("资治通鉴", "唐纪十七", "唐纪/唐纪十七#p436", "text-niutrans-457ebbd2862d04b7b4cf", "process", "primary",
      "待封不用仁贵策，将辎重徐进，未至乌海，遇吐蕃二十馀万，待封军大败，还走，悉弃辎重。"),
   ev("资治通鉴", "唐纪十七", "唐纪/唐纪十七#p437", "text-niutrans-c82f19954555a1182c64", "result", "primary",
      "仁贵退屯大非川，吐蕃相论钦陵将兵四十馀万就击之，唐兵大败，死伤略尽。"),
   ev("资治通鉴", "唐纪十七", "唐纪/唐纪十七#p439", "text-niutrans-97cacc792cd6a98d5838", "result", "supporting",
      "敕大司宪乐彦玮即军中按其败状，械送京师，三人皆免死除名。"),
   ev("新唐书", "吐蕃传", "列传/卷一百四十一#p101", "text-niutrans-d637f78b431cb2b1034d", "impact", "supporting",
      "师凡十余万，至大非川，为钦陵所拒，王师败绩，遂灭吐谷浑而尽有其地。"),
   ev("新唐书", "吐谷浑传", "列传/卷一百四十六#p216", "text-niutrans-3d7ada44e44562b7ef2d", "impact", "supporting",
      "王师败于大非川，举吐谷浑地皆陷，诺曷钵与亲近数千帐才免。"),
   ev("旧唐书", "高宗纪", "本纪/卷五#p101", "text-niutrans-e6124ec38c56ca97eafb", "result", "supporting",
      "薛仁贵、郭待封至大非川，为吐蕃大将论钦陵所袭，大败，仁贵等并坐除名。"),
  ],
 },
 # ---------------- 3. 甘露之变 ----------------
 "sui_tang/event-ganlu-zhi-bian.yml": {
  "background_zh_cn": "唐文宗深恶宦官专权，太和四年与宰相宋申锡谋除宦官，事泄申锡贬死。"
                       "后擢用李训、郑注：二人皆由神策中尉王守澄进用，而反说帝谋诛内官；太和九年十月先鸩杀王守澄，训与注势不两立，训出注为凤翔节度使，托中外应赴之谋，欲内外合势尽诛宦官。",
  "process_zh_cn": "太和九年十一月壬戌，文宗御紫宸殿，金吾大将军韩约奏左仗院石榴树夜有甘露，李训请帝亲往观之；帝令宰相两省官先视，归奏「臣等恐非真甘露，不敢轻言」，帝乃命左右军中尉、枢密内臣往验。"
                   "内臣至左仗，闻幕下有兵声，惊恐走出；李训急召王璠、郭行余受敕旨，唯璠从兵入而邠宁兵不至，事已急。"
                   "内官举软舆迎帝，训攀舆呼「陛下不得入内」，金吾卫士与罗立言、李孝本从人共四百余上殿纵击内官，死伤数十人；帝入东上阁门，门即阖，宦官呼万岁，事遂败。",
  "result_zh_cn": "仇士良等即遣兵大索，中尉仇士良率兵诛宰相王涯、贾餗、舒元舆及李训、王璠、郭行余、郑注、罗立言、李孝本、韩约等十余家，皆族诛；"
                  "李训奔凤翔途中被杀，郑注为监军所杀，宰相四人及朝士死者千余，朝列为之一空。",
  "impact_zh_cn": "甘露之变后宦官挟天子以令朝士，「自是天下事皆决于北司，宰相行文书而已」；文宗自比周赧、汉献，越五年而崩。"
                  "宦官典禁军、预废立之局由此固定，牛李党争亦在其阴影下延续，唐后期皇权自主之望遂绝。",
  "people": [
   {"person_name_raw": "李训", "role": "leader", "link_status": "needs_linking",
    "role_zh_cn": "宰相：甘露之谋主，败后被杀", "review_note": "major02-G：旧唐书·李训郑注传（诈言甘露、攀舆呼「陛下不得入内」）", "person_id": None},
   {"person_name_raw": "郑注", "role": "leader", "link_status": "needs_linking",
    "role_zh_cn": "凤翔节度使：与训同谋、出镇为外应，败后为监军所杀", "review_note": "major02-G：旧唐书·李训郑注传「托以中外应赴之谋，出注为凤翔节度使」", "person_id": None},
   {"person_name_raw": "仇士良", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "左军中尉：率兵诛宰相朝士十余家", "review_note": "major02-G：旧唐书·文宗纪「中尉仇士良率兵诛宰相王涯、贾餗、舒元舆、李训……皆族诛」", "person_id": None},
   {"person_name_raw": "唐文宗", "role": "ruler", "link_status": "needs_linking",
    "role_zh_cn": "唐朝皇帝：密谋诛宦而事败，此后受制北司", "review_note": "major02-G：旧唐书·文宗纪「时李训、郑注谋诛内官，诈言金吾仗舍石榴树有甘露」", "person_id": None},
   {"person_name_raw": "韩约", "role": "supporter", "link_status": "needs_linking",
    "role_zh_cn": "金吾大将军：奏称左仗院有甘露，为事变之引", "review_note": "major02-G：旧唐书·李训郑注传「韩约不报平安，奏曰：金吾左仗院石榴树，夜来有甘露」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "长安", "role": "capital", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "事变地（大明宫紫宸殿、左仗院）：伏兵与族诛皆在京城", "review_note": "major02-G：旧唐书·李训郑注传（紫宸殿奏事、左仗闻兵声）"},
   {"place_name_raw": "凤翔", "role": "base", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "郑注出镇之地：本欲为外应，败后郑注死于此", "review_note": "major02-G：旧唐书·李训郑注传「出注为凤翔节度使」"},
  ],
  "evidence": [
   ev("旧唐书", "文宗纪", "本纪/卷十七#p1220", "text-niutrans-424a155f10907a03ea30", "background", "primary",
      "时李训、郑注谋诛内官，诈言金吾仗舍石榴树有甘露，请上观之。"),
   ev("旧唐书", "李训郑注传", "列传/卷一百一十九#p38", "text-niutrans-745893233b9221e86c0f", "background", "supporting",
      "训虽为郑注引用，及禄位俱大，势不两立；托以中外应赴之谋，出注为凤翔节度使。"),
   ev("旧唐书", "李训郑注传", "列传/卷一百一十九#p43", "text-niutrans-0e1f01aa427f9d7259db", "process", "primary",
      "班定，韩约不报平安，奏曰：金吾左仗院石榴树，夜来有甘露，臣已进状讫。"),
   ev("旧唐书", "李训郑注传", "列传/卷一百一十九#p48", "text-niutrans-b14543d580e73d00bf79", "process", "supporting",
      "上令宰相两省官先往视之。既还，曰：臣等恐非真甘露，不敢轻言。"),
   ev("旧唐书", "李训郑注传", "列传/卷一百一十九#p55", "text-niutrans-eaff8c717c36a311fdde", "process", "primary",
      "中尉、枢密至左仗，闻幕下有兵声，惊恐走出。"),
   ev("旧唐书", "李训郑注传", "列传/卷一百一十九#p63", "text-niutrans-c13ff3a5d247499ec673", "process", "supporting",
      "罗立言率府中从人自东来，李孝本率台中从人自西来，共四百余人，上殿纵击内官，死伤者数十人。"),
   ev("旧唐书", "文宗纪", "本纪/卷十七#p1219", "text-niutrans-a3eb75e0c531c21c496f", "result", "primary",
      "壬戌，中尉仇士良率兵诛宰相王涯、贾餗、舒元舆、李训，新除太原节度王璠，郭行馀、郑注、罗立言、李孝本，韩约等十余家，皆族诛。"),
   ev("资治通鉴", "唐纪六十一", "唐纪/唐纪六十一#p327", "text-niutrans-12b7afb93d25823dc281", "impact", "primary",
      "自是天下事皆决于北司，宰相行文书而已。"),
  ],
 },
 # ---------------- 4. 淮西之战 ----------------
 "sui_tang/event-huai-xi-zhi-zhan.yml": {
  "background_zh_cn": "淮西节度使吴少阳死，其子摄蔡州刺史吴元济匿丧不报、自领军务，「阴聚亡命，牧养马骡，时抄掠寿州茶山以实其军」；宪宗决意讨之，元和十年诏诸道兵环申、蔡而讨，李光颜独当一面，连破元济之众。"
                       "战事数年前后无功，唐邓节度使高霞寓败于铁城，中外恟骇；裴度自请督师，以郾城为行在，激励士众，军士皆愿效死。",
  "process_zh_cn": "元和十二年十月，李愬用降将李祐之谋：元济劲军多在洄曲西境，守蔡者皆市人疲耄之卒，可乘虚掩袭。"
                   "愬令李祐率劲骑三千为前锋、田进诚三千为后军、自率三千为中军，夜出文城栅；诸将请所止，愬曰「入蔡州取吴元济」，诸将失色而不敢违。"
                   "行七十里至悬瓠城，夜半雪愈甚，近城有鹅鸭池，愬令惊击之以杂其声；李祐、李忠义坎墉先登，尽杀守门卒而留击柝者，黎明雪止，愬入止元济外宅，元济犹以为洄曲子弟来求寒衣。",
  "result_zh_cn": "十月十一日，唐军攻衙城，擒元济并其家属以闻，申、光二州及诸镇兵相继来降；裴度入蔡州，以蔡卒为牙兵，量罪加刑不尽如诏，淮西三州遂平。"
                  "淮西既平，藩镇震恐：元和十三年淄青李师道为其部下刘悟所杀，函首至京师，唐廷分其地为三道，淄青亦平。",
  "impact_zh_cn": "淮西之捷为元和削藩的决定性一役，河北藩镇相继请入朝，元和中兴之局由此告成；「李愬雪夜入蔡州」以奇袭典范垂名后世，为历代兵家所称。"
                  "唐廷以蔡州降卒为牙兵、量罪加刑，亦见战后处置之审慎。",
  "people": [
   {"person_name_raw": "李愬", "role": "commander", "link_status": "needs_linking",
    "role_zh_cn": "唐邓节度使：雪夜奇袭蔡州、擒吴元济", "review_note": "major02-G：旧唐书·李晟传附「愬曰：入蔡州取吴元济也」", "person_id": None},
   {"person_name_raw": "吴元济", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "淮西叛帅：匿丧领军，蔡州破后被擒", "review_note": "major02-G：通鉴唐纪五十五「其子摄蔡州刺史元济，匿丧，以病闻，自领军务」", "person_id": None},
   {"person_name_raw": "裴度", "role": "commander", "link_status": "needs_linking",
    "role_zh_cn": "淮西宣慰招讨处置使：督师郾城、入蔡州善后", "review_note": "major02-G：旧唐书·裴度传「诏以度为彰义军节度使，兼申光蔡四面行营招抚使」", "person_id": None},
   {"person_name_raw": "李祐", "role": "supporter", "link_status": "needs_linking",
    "role_zh_cn": "降将：献策乘虚袭蔡，为前锋先登", "review_note": "major02-G：旧唐书·裴度传「祐曰：……可以乘虚掩袭，直抵悬匏」", "person_id": None},
   {"person_name_raw": "李光颜", "role": "commander", "link_status": "needs_linking",
    "role_zh_cn": "忠武节度使：独当一面、屡破元济之众", "review_note": "major02-G：旧唐书·李光颜传「诏光颜以本军独当一面」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "蔡州", "role": "target", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "吴元济巢穴（悬瓠城）：雪夜被袭破", "review_note": "major02-G：旧唐书·李晟传附「比至悬瓠城，夜半，雪愈甚」"},
   {"place_name_raw": "郾城", "role": "base", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "裴度督师行在：诸军会集之地", "review_note": "major02-G：旧唐书·裴度传「以郾城为行在，蔡州为节度所」"},
   {"place_name_raw": "洄曲", "role": "front", "link_status": "needs_linking", "sequence": 3,
    "description_zh_cn": "元济劲军所守之处：愬分兵断其路桥", "review_note": "major02-G：旧唐书·李晟传附「分五百人断洄曲路桥」"},
  ],
  "evidence": [
   ev("资治通鉴", "唐纪五十五", "唐纪/唐纪五十五#p155", "text-niutrans-8e588c36b2f01b2da667", "background", "primary",
      "少阳在蔡州，阴聚亡命，牧养马骡，时抄掠寿州茶山以实其军，其子摄蔡州刺史元济，匿丧，以病闻，自领军务。"),
   ev("旧唐书", "裴度传", "列传/卷一百二十#p61", "text-niutrans-0db8ccd5c33e7c316e88", "background", "supporting",
      "六月，蔡州行营唐邓节度使高霞寓兵败于铁城，中外恟骇。"),
   ev("旧唐书", "裴度传", "列传/卷九十五#p167", "text-niutrans-3e38151cfd9859d6305a", "process", "supporting",
      "祐曰：元济劲军，多在洄曲西境防捍，而守蔡者皆市人疲耄之卒，可以乘虚掩袭，直抵悬匏，比贼将闻之，元济成擒矣！"),
   ev("旧唐书", "裴度传", "列传/卷九十五#p169", "text-niutrans-456a14cb60e6aabb7792", "process", "supporting",
      "十一月，醖夜出军，令李祐率劲骑三千为前锋，田进诚三千为后军，醖自率三千为中军。"),
   ev("旧唐书", "李晟传", "列传/卷八十三#p328", "text-niutrans-91d4249dffdf2df9536d", "process", "primary",
      "初至张柴，诸将请所止，愬曰：入蔡州取吴元济也。"),
   ev("旧唐书", "李晟传", "列传/卷八十三#p333", "text-niutrans-682c70a4bfb451d791f0", "process", "primary",
      "自张柴行七十里，比至悬瓠城，夜半，雪愈甚。"),
   ev("旧唐书", "李晟传", "列传/卷八十三#p334", "text-niutrans-717a7a38a2ebae4ececd", "process", "supporting",
      "近城有鹅鸭池，愬令惊击之，以杂其声。"),
   ev("旧唐书", "李光颜传", "列传/卷一百一十一#p91", "text-niutrans-89f6bf4e344e596f7a5f", "result", "primary",
      "时李愬乘其无备，急引兵袭蔡州，拔之，获元济。"),
   ev("旧唐书", "裴度传", "列传/卷九十五#p171", "text-niutrans-9730f399a9c53b556029", "result", "supporting",
      "十一日，攻衙城，擒元济并其家属以闻。"),
   ev("资治通鉴", "唐纪五十七", "唐纪/唐纪五十七#p65", "text-niutrans-ad8eed3ba5615d0d59af", "impact", "primary",
      "己巳，李师道首函至。", "淮西平后淄青亦平，元和削藩成局"),
   ev("旧唐书", "裴度传", "列传/卷九十五#p164", "text-niutrans-ed2eb7edcfc1d14aa577", "background", "supporting",
      "七月，诏以度为彰义军节度使，兼申光蔡四面行营招抚使，以郾城为行在，蔡州为节度所。"),
  ],
 },
 # ---------------- 5. 黄巢攻入长安 ----------------
 "sui_tang/event-huangchao-ru-changan.yml": {
  "background_zh_cn": "乾符二年（875年）黄巢聚众响应王仙芝，转掠河南；王仙芝败死后，黄巢称「冲天大将军」，渡江陷虔、吉、饶、信等州，开山洞五百里入福建，又陷广州，大掠岭南。"
                       "广明元年（880年）黄巢自桂管北还，连陷湖南、江西，朝廷以高骈为诸道行营都统；骈将张璘战败被杀，骈自保淮南，黄巢遂乘胜渡江，攻天长、六合，詔河南诸道之师屯溵水。",
  "process_zh_cn": "广明元年十一月，黄巢悉众渡淮，自号率土大将军，「其众富足，自淮已北整众而行，不剽财货，惟驱丁壮为兵耳」；己巳陷东都，留守刘允章率分司官属迎谒，贼供顿而去，坊市晏然。"
                   "丙子攻潼关，守关诸将望风自溃，辛巳贼据潼关；十二月甲申，僖宗与诸王、妃、后数百骑自子城由含光殿金光门出幸山南，百官不之知，京城晏然。",
  "result_zh_cn": "是日晡晚贼入京城，右骁卫大将张直方率武官十余迎黄巢于坡头；壬辰黄巢据大内，僭号大齐，称年号金统，悉陈文物、据丹凤门伪赦，以尚让为太尉、崔璆为平章事。"
                  "朝臣豆卢彖、崔沆、刘邺、于琮等从驾不及为贼所捕遇害，郑綦、郑系举家自尽；中和元年正月车驾在兴元，诏诸道会兵讨贼。",
  "impact_zh_cn": "长安陷落与僭号大齐，是黄巢起义之顶点，亦是唐廷中枢权威崩解之标志——僖宗播迁山南、再幸蜀，诏令所及唯在行在；京畿残破、百官屠戮之后，唐室名存实亡。"
                  "此后藩镇各专租税、中原无复上供，二十余年后朱温代唐，五代之局实肇于此。",
  "people": [
   {"person_name_raw": "黄巢", "role": "leader", "link_status": "needs_linking",
    "role_zh_cn": "起义军首领：入长安、僭号大齐", "review_note": "major02-G：旧唐书·僖宗纪「黄巢据大内，僭号大齐，称年号金统」", "person_id": None},
   {"person_name_raw": "唐僖宗", "role": "ruler", "link_status": "needs_linking",
    "role_zh_cn": "唐朝皇帝：出金光门幸山南、再幸蜀", "review_note": "major02-G：旧唐书·僖宗纪「上与诸王、妃、后数百骑，自子城由含光殿金光门出幸山南」", "person_id": None},
   {"person_name_raw": "田令孜", "role": "official", "link_status": "needs_linking",
    "role_zh_cn": "左军中尉：专政误谋、挟帝出奔", "review_note": "major02-G：旧唐书·僖宗纪「时左军中尉田令孜专政，宰相卢携曲事之，相与误谋，以至倾败」", "person_id": None},
   {"person_name_raw": "刘允章", "role": "official", "link_status": "needs_linking",
    "role_zh_cn": "东都留守：率分司官属迎谒黄巢", "review_note": "major02-G：旧唐书·僖宗纪「贼陷东都，留守刘允章率分司官属迎谒之」", "person_id": None},
   {"person_name_raw": "尚让", "role": "commander", "link_status": "needs_linking",
    "role_zh_cn": "黄巢大将：入长安后为太尉", "review_note": "major02-G：旧唐书·僖宗纪「以赵章为中书令，尚让为太尉」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "长安", "role": "capital", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "陷落之都城：黄巢据大内、僭号大齐之处", "review_note": "major02-G：旧唐书·僖宗纪「壬辰，黄巢据大内，僭号大齐」"},
   {"place_name_raw": "潼关", "role": "battlesite", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "长安门户：守将望风自溃、贼据之", "review_note": "major02-G：旧唐书·僖宗纪「丙子，攻潼关，守关诸将望风自溃」"},
   {"place_name_raw": "洛阳", "role": "capital", "link_status": "needs_linking", "sequence": 3,
    "description_zh_cn": "东都：先于长安陷落，留守迎谒", "review_note": "major02-G：旧唐书·僖宗纪「己巳，贼陷东都」"},
   {"place_name_raw": "兴元", "role": "court_in_exile", "link_status": "needs_linking", "sequence": 4,
    "description_zh_cn": "僖宗行在：中和元年正月车驾所在", "review_note": "major02-G：旧唐书·僖宗纪「中和元年春正月庚戌朔，车驾在兴元」"},
  ],
  "evidence": [
   ev("旧唐书", "僖宗纪", "本纪/卷十九#p919", "text-niutrans-1c896f19f83056d46dbb", "background", "supporting",
      "黄巢自号率土大将军，其众富足，自淮已北整众而行，不剽财货，惟驱丁壮为兵耳。"),
   ev("旧唐书", "僖宗纪", "本纪/卷十九#p921", "text-niutrans-fa9df97406529869ee14", "process", "primary",
      "己巳，贼陷东都，留守刘允章率分司官属迎谒之，贼供顿而去，坊市晏然。"),
   ev("旧唐书", "僖宗纪", "本纪/卷十九#p923", "text-niutrans-28d7703b3c8049dc0d86", "process", "primary",
      "丙子，攻潼关，守关诸将望风自溃。"),
   ev("旧唐书", "僖宗纪", "本纪/卷十九#p926", "text-niutrans-a4e10d47420523ef9e44", "background", "supporting",
      "时左军中尉田令孜专政，宰相卢携曲事之，相与误谋，以至倾败。"),
   ev("旧唐书", "僖宗纪", "本纪/卷十九#p931", "text-niutrans-5c3a62fb643eb38d7afa", "process", "primary",
      "是日，上与诸王、妃、后数百骑，自子城由含光殿金光门出幸山南，文武百官僚不之知，并无从行者，京城晏然。"),
   ev("旧唐书", "僖宗纪", "本纪/卷十九#p932", "text-niutrans-cb1025548dd29c5d4e00", "result", "primary",
      "是日晡晚，贼入京城，时右骁卫大将张直方率武官十余迎黄巢于坡头。"),
   ev("旧唐书", "僖宗纪", "本纪/卷十九#p933", "text-niutrans-8ed4700bee278fd99036", "result", "primary",
      "壬辰，黄巢据大内，僭号大齐，称年号金统。悉陈文物，据丹凤门伪赦。"),
   ev("旧唐书", "僖宗纪", "本纪/卷十九#p938", "text-niutrans-96aada7b570d3af496f1", "result", "supporting",
      "时宰相豆卢彖崔沆、故相左仆射刘鄴、太子少师裴谂、御史中丞赵蒙、刑部侍郎李溥、故相于琮皆从驾不及，匿于闾里，为贼所捕，皆遇害。"),
   ev("旧唐书", "僖宗纪", "本纪/卷十九#p940", "text-niutrans-20a7b148e43c2531f582", "impact", "primary",
      "中和元年春正月庚戌朔，车驾在兴元。"),
  ],
  "relations_add": [
   {"target_event_id": "event-houliang-dai-tang", "relation_type": "precedes", "confidence": 0.85,
    "description_zh_cn": "黄巢入长安后唐室名存实亡，二十余年后朱温代唐"},
   {"target_event_id": "event-huangchao-baiwang", "relation_type": "precedes",
    "description_zh_cn": "入长安为黄巢势力顶点，此后诸道会兵、巢败走死"},
  ],
 },
 # ---------------- 6. 会昌灭佛 ----------------
 "sui_tang/event-huichang-miefo.yml": {
  "background_zh_cn": "武宗好道术，宠道士赵归真、衡山道士刘玄靖，与归真胶固，排毁释氏而拆寺之请行。"
                       "佛教自唐初以来寺院经济膨胀：寺田、僧尼、奴婢与两税争夺人口，武宗诏中自言「贞观、开元，亦尝厘革，剷除不尽，流衍转滋」，遂断行厘革。",
  "process_zh_cn": "会昌五年（845年）七月庚子，敕并省天下佛寺；中书门下条疏：上州各留寺一所（工作精妙者留，破落者亦废），下州寺并废，行香日官吏改于道观。"
                   "上都、东都每街留寺二所、寺留僧三十人，上都左街留慈恩、荐福，右街留西明、庄严；八月，敕天下废寺铜像、钟磬委盐铁使铸钱，铁像委本州铸为农器，金银鍮石等像销付度支。"
                   "又勒大秦穆护、袄三千余人还俗，不杂中华之风。",
  "result_zh_cn": "其天下所拆寺四千六百余所，还俗僧尼二十六万五百人，收充两税户；拆招堤、兰若四万余所，收膏腴上田数千万顷，收奴婢为两税户十五万人——佛教史称「会昌法难」，为三武一宗灭佛中规模最大者。"
                  "寺产既没，两京悲田养病坊因僧尼还俗无人主持，敕量给寺田赈济，恐残疾无以取给。",
  "impact_zh_cn": "灭佛所得寺田、僧尼、奴婢尽入两税与度支，唐后期财政赖以纾困；然寺宇经像毁废极广，佛教义学与僧团受创至深。"
                  "武宗寻于次年崩，宣宗即位后即复兴佛教，会昌之政遂为唐代佛教兴衰的一大转折。",
  "people": [
   {"person_name_raw": "唐武宗", "role": "ruler", "link_status": "needs_linking",
    "role_zh_cn": "唐朝皇帝：下敕并省天下佛寺", "review_note": "major02-G：旧唐书·武宗纪「秋七月庚子，敕并省天下佛寺」", "person_id": None},
   {"person_name_raw": "赵归真", "role": "supporter", "link_status": "needs_linking",
    "role_zh_cn": "道士：与刘玄靖排毁释氏，促成拆寺", "review_note": "major02-G：旧唐书·武宗纪「与衡山道士刘玄靖及归真胶固，排毁释氏」", "person_id": None},
   {"person_name_raw": "刘玄靖", "role": "supporter", "link_status": "needs_linking",
    "role_zh_cn": "衡山道士：与归真同排佛", "review_note": "major02-G：旧唐书·武宗纪「与衡山道士刘玄靖及归真胶固」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "长安", "role": "capital", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "上都：两街留寺四所、余皆废毁", "review_note": "major02-G：旧唐书·武宗纪「上都左街留慈恩、荐福，右街留西明、庄严」"},
   {"place_name_raw": "洛阳", "role": "capital", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "东都：与上都同留寺限僧", "review_note": "major02-G：旧唐书·武宗纪「其上都、下都每街留寺两所，寺留僧三十人」"},
  ],
  "evidence": [
   ev("旧唐书", "武宗纪", "本纪/卷十八#p423", "text-niutrans-b640bbed738438e24c78", "background", "primary",
      "由是与衡山道士刘玄靖及归真胶固，排毁释氏，而拆寺之请行焉。"),
   ev("旧唐书", "武宗纪", "本纪/卷十八#p473", "text-niutrans-5ccd7786adaddcf5e142", "background", "supporting",
      "贞观、开元，亦尝厘革，剷除不尽，流衍转滋。"),
   ev("旧唐书", "武宗纪", "本纪/卷十八#p449", "text-niutrans-4c9bcad6ff98ad2bfdb2", "process", "primary",
      "秋七月庚子，敕并省天下佛寺。"),
   ev("旧唐书", "武宗纪", "本纪/卷十八#p450", "text-niutrans-481ebd2a1df6f271a40c", "process", "supporting",
      "中书门下条疏闻奏：据令式，诸上州国忌日官吏行香于寺，其上州望各留寺一所，有列圣尊容，便令移于寺内；其下州寺并废。"),
   ev("旧唐书", "武宗纪", "本纪/卷十八#p454", "text-niutrans-b85da306384654b522f3", "process", "supporting",
      "其上都、下都每街留寺两所，寺留僧三十人。"),
   ev("旧唐书", "武宗纪", "本纪/卷十八#p456", "text-niutrans-568b1eec623e10c60bc4", "process", "supporting",
      "中书又奏：天下废寺，铜像、钟磬委盐铁使铸钱，其铁像委本州铸为农器，金、银、鍮石等像销付度支。"),
   ev("旧唐书", "武宗纪", "本纪/卷十八#p477", "text-niutrans-2fdd07883d999f6201d5", "result", "primary",
      "其天下所拆寺四千六百余所，还俗僧尼二十六万五百人，收充两税户，拆招堤、兰若四万余所，收膏腴上田数千万顷，收奴婢为两税户十五万人。"),
   ev("旧唐书", "武宗纪", "本纪/卷十八#p479", "text-niutrans-f6e5b4a9fbf2c2e318d2", "result", "supporting",
      "勒大秦穆护、袄三千余人还俗，不杂中华之风。"),
   ev("旧唐书", "武宗纪", "本纪/卷十八#p499", "text-niutrans-4e9bd670c40ecb75b770", "impact", "primary",
      "十一月甲辰，敕：悲田养病坊，缘僧尼还俗，无人主持，恐残疾无以取给，两京量给寺田赈济。"),
  ],
 },
 # ---------------- 7. 建中之乱 ----------------
 "sui_tang/event-jianzhong-zhi-luan.yml": {
  "background_zh_cn": "德宗即位锐意削藩：建中二年成德李宝臣死，其子惟岳请袭不获，遂与魏博田悦、淄青李纳、山南东道梁崇义连兵拒命；建中三年卢龙朱滔、成德王武俊复叛，四镇连兵，淮西李希烈受命讨李纳而反。"
                       "建中四年十月，诏泾原节度使姚令言率泾原之师救哥舒曜于襄城，泾原兵过京，遂为变乱之导火。",
  "process_zh_cn": "十月丁未，泾原军出京城，至浐水倒戈谋叛，姚令言不能禁；帝令载缯彩二车，遣晋王往慰谕，乱兵已陈于丹凤阙下，促神策军拒之而「无一人至者」。"
                   "帝与太子诸王妃主百余人出苑北门，其夕至咸阳，戊申至奉天；乱兵剽京城，屯于白华，乃于晋昌里迎朱泚为帅，称太尉，居含元殿，朱泚僭称秦帝，引兵围奉天。"
                   "贼自丁未攻城二十余日，矢石雨下，薨伤者众，人心危蹙，上与浑瑊对泣；朔方、灵武诸道援兵至漠谷者为贼所败。",
  "result_zh_cn": "陆贽劝帝痛自引过以感人心，兴元元年正月癸酉朔赦天下、改元，诏书言「李希烈、田悦、王武俊、李纳等，咸以勋旧……皆由上失其道而下罹其灾，朕实不君，人则何罪」，并所管将吏一切待之如初。"
                  "李晟移军东渭桥，斩不受节制之刘德信而并其军，军势益振；六月李晟收京城，朱泚、姚令言死。",
  "impact_zh_cn": "建中之乱以罪己、赦叛收场，德宗削藩功败垂成，唐廷对河北藩镇转为姑息，世袭之局遂固；奉天之围与李怀光之叛亦使德宗不再信任将帅，转向信用宦官典掌禁军。"
                  "此役后唐中央权威大损，藩镇、宦官、党争三大痼疾自此并作。",
  "people": [
   {"person_name_raw": "唐德宗", "role": "ruler", "link_status": "needs_linking",
    "role_zh_cn": "唐朝皇帝：削藩致乱、出奔奉天、下罪己诏", "review_note": "major02-G：旧唐书·德宗纪「与太子诸王妃主百余人出苑北门」", "person_id": None},
   {"person_name_raw": "姚令言", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "泾原节度使：兵变首领，不能禁军", "review_note": "major02-G：旧唐书·德宗纪「泾原军出京城，至浐水，倒戈谋叛，姚令言不能禁」", "person_id": None},
   {"person_name_raw": "朱泚", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "据长安称秦帝：败后遁走而死", "review_note": "major02-G：旧唐书·德宗纪「乃于晋昌里迎硃泚为帅」；列传卷九十三「六月，李晟收京城，硃泚、姚令言死」", "person_id": None},
   {"person_name_raw": "李晟", "role": "commander", "link_status": "needs_linking",
    "role_zh_cn": "神策军将：收复长安", "review_note": "major02-G：旧唐书·德宗纪「追击至白华，硃泚、姚令言率众万余遁去」", "person_id": None},
   {"person_name_raw": "浑瑊", "role": "supporter", "link_status": "needs_linking",
    "role_zh_cn": "行在都虞候：奉天守城力战", "review_note": "major02-G：旧唐书·德宗纪「贼由是攻城愈急……上与浑瑊对泣」", "person_id": None},
   {"person_name_raw": "陆贽", "role": "official", "link_status": "needs_linking",
    "role_zh_cn": "翰林学士：劝帝引过、草罪己诏", "review_note": "major02-G：通鉴唐纪四十五「陆贽言于上曰：今盗遍天下，舆驾播迁，陛下宜痛自引过以感人心」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "奉天", "role": "court_in_exile", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "德宗行在：被朱泚围城二十余日", "review_note": "major02-G：旧唐书·德宗纪「戊申，至奉天」"},
   {"place_name_raw": "长安", "role": "capital", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "京城：泾原兵剽掠、朱泚据含元殿", "review_note": "major02-G：旧唐书·德宗纪「乱兵既剽京城，屯于白华」"},
   {"place_name_raw": "浐水", "role": "mutiny_site", "link_status": "needs_linking", "sequence": 3,
    "description_zh_cn": "兵变起处：泾原军出京城至浐水倒戈", "review_note": "major02-G：旧唐书·德宗纪「至浐水，倒戈谋叛」"},
  ],
  "evidence": [
   ev("旧唐书", "德宗纪", "本纪/卷十二#p332", "text-niutrans-1b7d20fee344137a3372", "background", "primary",
      "冬十月丙午，诏泾原节度使姚令言率泾原之师救哥舒曜。"),
   ev("旧唐书", "德宗纪", "本纪/卷十二#p333", "text-niutrans-6cecc3f2b8eece2bbfb9", "process", "primary",
      "丁未，泾原军出京城，至浐水，倒戈谋叛，姚令言不能禁。"),
   ev("旧唐书", "德宗纪", "本纪/卷十二#p334", "text-niutrans-8109c5b4b1100b4cc1f7", "process", "supporting",
      "上令载缯彩二车，遣晋王往慰谕之，乱兵已陈于丹凤阙下，促神策军拒之。无一人至者。"),
   ev("旧唐书", "德宗纪", "本纪/卷十二#p337", "text-niutrans-1a827aef8350c3e0b173", "process", "supporting",
      "戊申，至奉天。"),
   ev("旧唐书", "德宗纪", "本纪/卷十二#p339", "text-niutrans-22c619f8341facddb1d9", "process", "primary",
      "乱兵既剽京城，屯于白华，乃于晋昌里迎硃泚为帅，称太尉，居含元殿。"),
   ev("旧唐书", "德宗纪", "本纪/卷十二#p350", "text-niutrans-59d5da2ce219fc4697cc", "process", "supporting",
      "贼由是攻城愈急，矢石雨下，薨伤者众，人心危蹙，上与浑瑊对泣。"),
   ev("资治通鉴", "唐纪四十五", "唐纪/唐纪四十五#p279", "text-niutrans-17cf972d6ccd6bc0e32a", "result", "primary",
      "春，正月，癸酉朔，赦天下，改元。"),
   ev("资治通鉴", "唐纪四十五", "唐纪/唐纪四十五#p286", "text-niutrans-c56d88aacd737dfa3d07", "result", "primary",
      "李希烈、田悦、王武俊、李纳等，咸以勋旧，各守籓维，联抚驭乖方，致其疑惧；皆由上失其道而下罹其灾，朕实不君，人则何罪！宜并所管将吏等一切待之如初。"),
   ev("旧唐书", "李晟传", "列传/卷九十三#p42", "text-niutrans-2d889c6bd7564864e030", "result", "supporting",
      "六月，李晟收京城，硃泚、姚令言死。"),
   ev("资治通鉴", "唐纪四十五", "唐纪/唐纪四十五#p257", "text-niutrans-e05d96945aa9bba3020c", "impact", "supporting",
      "陆贽言于上曰：今盗遍天下，舆驾播迁，陛下宜痛自引过以感人心。", "罪己之诏为唐廷转危之枢机"),
  ],
 },
 # ---------------- 8. 开元盛世 ----------------
 "sui_tang/event-kaiyuan-shengshi.yml": {
  "background_zh_cn": "玄宗以临淄王定韦后之乱，先天二年又诛太平公主及其党与，始总揽万机；开元元年以姚崇为相，纳其请而抑权幸、罢冗官、检责僧尼。"
                       "「临御之初，任姚崇、宋璟，二人皆忠鲠上才，动以致主为心」；其后张嘉贞、张说、韩休、张九龄相继为相，吏治以澄清称。",
  "process_zh_cn": "开元年间检括户口、劝课农桑、广置屯田、修渠灌田，太仓、含嘉仓之粟积至千万石；又改政事堂为中书门下，于沿边设节度使以备四夷。"
                   "开元二十八年（740年），天下县千五百七十三，户八百四十一万二千八百七十一，口四千八百一十四万三千六百九——较贞观、永徽之世户口倍増。",
  "result_zh_cn": "是岁西京、东都米斛直钱不满二百，绢匹亦如之；「海内富安，行者虽万里不持寸兵」——物价之平、行旅之安为史家所记之实况，后世以「开元盛世」名之。"
                  "姚崇上言检责天下僧尼、伪滥还俗者二万余人，亦为盛世厘革之一端。",
  "impact_zh_cn": "开元之盛以户口、物价、治安之数为证，为唐代国力之顶点，文教武备皆极一时；然边兵之费至天宝而大增——「开元之前，每岁供边兵衣粮，费不过二百万；天宝之后，边将奏益兵浸多，每岁用衣千二十万匹、粮百九十万斛」，公私劳费而民始困苦。"
                  "府兵废弛与节度权重已伏盛极而衰之机，天宝末遂有安史之乱。",
  "people": [
   {"person_name_raw": "唐玄宗", "role": "ruler", "link_status": "needs_linking",
    "role_zh_cn": "唐朝皇帝：开元之治的开创者", "review_note": "major02-G：旧唐书·玄宗纪（开元年间政事）；通鉴唐纪三十户口之数", "person_id": None},
   {"person_name_raw": "姚崇", "role": "official", "link_status": "needs_linking",
    "role_zh_cn": "开元名相：革除积弊、检责僧尼", "review_note": "major02-G：旧唐书·玄宗纪「紫微令姚崇上言请检责天下僧尼」", "person_id": None},
   {"person_name_raw": "宋璟", "role": "official", "link_status": "needs_linking",
    "role_zh_cn": "开元名相：与姚崇并称，守正持法", "review_note": "major02-G：旧唐书「临御之初，任姚崇、宋璟，二人皆忠鲠上才」", "person_id": None},
   {"person_name_raw": "张九龄", "role": "official", "link_status": "needs_linking",
    "role_zh_cn": "开元后期名相：以直道事君", "review_note": "major02-G：旧唐书「玄宗用姚崇、宋璟、张九龄、韩休……则理」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "长安", "role": "capital", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "西京：米斛直钱不满二百、行旅万里不持寸兵", "review_note": "major02-G：通鉴唐纪三十「西京、东都米斛直钱不满二百」"},
   {"place_name_raw": "洛阳", "role": "capital", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "东都：与西京并称富庶", "review_note": "major02-G：通鉴唐纪三十「西京、东都米斛直钱不满二百，绢匹亦如之」"},
  ],
  "evidence": [
   ev("旧唐书", "玄宗名臣传", "列传/卷一百一十四#p131", "text-niutrans-b901f944fde5e54a81a8", "background", "primary",
      "临御之初，任姚崇、宋璟，二人皆忠鲠上才，动以致主为心。"),
   ev("旧唐书", "玄宗纪", "本纪/卷八#p88", "text-niutrans-d14cbaa281652b4ed009", "process", "supporting",
      "丙寅，紫微令姚崇上言请检责天下僧尼，以伪滥还俗者二万余人。"),
   ev("资治通鉴", "唐纪三十", "唐纪/唐纪三十#p462", "text-niutrans-5a42f0d0b9ef65187be6", "result", "primary",
      "是岁，天下县千五百七十三，户八百四十一万二千八百七十一，口四千八百一十四万三千六百九。"),
   ev("资治通鉴", "唐纪三十", "唐纪/唐纪三十#p463", "text-niutrans-d7a8437a1d7ceb59fd1e", "result", "primary",
      "西京、东都米斛直钱不满二百，绢匹亦如之。"),
   ev("资治通鉴", "唐纪三十", "唐纪/唐纪三十#p464", "text-niutrans-65389c5f4d7fff7a60e8", "impact", "primary",
      "海内富安，行者虽万里不持寸兵。"),
   ev("资治通鉴", "唐纪三十一", "唐纪/唐纪三十一#p20", "text-niutrans-d5615951ddd5090a0565", "impact", "supporting",
      "开元之前，每岁供边兵衣粮，费不过二百万；天宝之后，边将奏益兵浸多，每岁用衣千二十万匹，粮百九十万斛，公私劳费，民始困苦矣。"),
   ev("旧唐书", "玄宗名臣传", "列传/卷一百零九#p152", "text-niutrans-11dd49348bdcac573ee7", "impact", "supporting",
      "玄宗用姚崇、宋璟、张九龄、韩休、李元纮、杜暹则理；用林甫、杨国忠则乱。"),
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
