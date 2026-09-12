"""Major Batch 01 · Cluster C：楚汉与西汉前期（9 事件）。"""
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
        "review_note": f"major01-C：{work}源引文：「{quote}」；claim_field={field}；anchor=段落精确锚。{note}"}

SJ = "史记"; TJ = "资治通鉴"
BLOCKS = {
 "qin_han/event-chuhan-war.yml": {
  "background_zh_cn": "正月，项羽自立为西楚霸王，王梁、楚地九郡，都彭城；又负约更立沛公为汉王，王巴、蜀、汉中，都南郑——分封失当，楚汉对立之局遂成。",
  "process_zh_cn": "楚汉久相持未决，丁壮苦军旅、老弱罢转饷——成皋、荥阳一线数年拉锯。",
  "result_zh_cn": "韩信、彭越诸军会垓下，孔将军、费将军纵，楚兵不利，淮阴侯复乘之，大败垓下——项羽败亡、战争终结。",
  "impact_zh_cn": "二月甲午，汉王即皇帝位于汜水之阳——楚汉战争以刘邦建立汉朝告终，四百年汉室基业由此始。",
  "relations": [
   {"target_event_id": "event-hongmen", "relation_type": "follows", "confidence": 0.9,
    "description_zh_cn": "鸿门之后项羽分封、刘邦就国，楚汉相争全面开启。"},
   {"target_event_id": "event-chuhan-han-foundation", "relation_type": "precedes", "confidence": 0.9,
    "description_zh_cn": "战争以垓下决战收束，紧接汉朝建立。"},
  ],
  "people": [
   {"person_name_raw": "刘邦", "role": "monarch", "link_status": "needs_linking",
    "role_zh_cn": "汉王：战争胜利者、汉朝开国", "review_note": "major01-C：史记·高祖本纪「更立沛公为汉王」", "person_id": None},
   {"person_name_raw": "项羽", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "西楚霸王：战争败亡者", "review_note": "major01-C：史记·高祖本纪「项羽自立为西楚霸王」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "彭城", "role": "capital", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "西楚都城", "review_note": "major01-C：史记·高祖本纪「都彭城」"},
   {"place_name_raw": "南郑", "role": "capital", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "汉王初都", "review_note": "major01-C：史记·高祖本纪「都南郑」"},
   {"place_name_raw": "垓下", "role": "battlesite", "link_status": "needs_linking", "sequence": 3,
    "description_zh_cn": "决战之地", "review_note": "major01-C：史记·高祖本纪「大败垓下」"},
  ],
  "evidence": [
   ev(SJ, "高祖本纪", "十二本纪/高祖本纪#p229", "text-niutrans-1b8859a448eb1b8fb376", "background", "primary", "正月，项羽自立为西楚霸王，王梁、楚地九郡，都彭城。"),
   ev(SJ, "高祖本纪", "十二本纪/高祖本纪#p230", "text-niutrans-1fe93f3e3b2285c333f8", "background", "supporting", "负约，更立沛公为汉王，王巴、蜀、汉中，都南郑。"),
   ev(SJ, "高祖本纪", "十二本纪/高祖本纪#p367", "text-niutrans-383a4cfb1b9ee96dcd2b", "process", "primary", "楚汉久相持未决，丁壮苦军旅，老弱罢转饟。"),
   ev(SJ, "高祖本纪", "十二本纪/高祖本纪#p405", "text-niutrans-8737c6c9a14e680f8430", "result", "primary", "孔将军、费将军纵，楚兵不利，淮阴侯复乘之，大败垓下。"),
   ev(TJ, "汉纪三", "汉纪/汉纪三#p71", "text-niutrans-a158f087083c592fb21e", "impact", "primary", "二月甲午，王即皇帝位于汜水之阳。"),
  ],
 },
 "qin_han/event-han-dingdu-changan.yml": {
  "background_zh_cn": "高祖欲长都雒阳，齐人刘敬说，乃留侯劝上入都关中，高祖是日驾，入都关中。",
  "process_zh_cn": "长乐宫成，丞相已下徙治长安——宫室官署次第就绪。",
  "result_zh_cn": "高祖自布军至长安——都城长安的统治秩序既定。",
  "impact_zh_cn": "「关中阻山河四塞，地肥饶，可都以霸」——定都关中据形胜之地，长安自此为西汉二百年国都，亦为中国千年古都之首。",
  "people": [
   {"person_name_raw": "刘邦", "role": "monarch", "link_status": "needs_linking",
    "role_zh_cn": "汉高祖：决策入都关中", "review_note": "major01-C：史记·高祖本纪「高祖是日驾，入都关中」", "person_id": None},
   {"person_name_raw": "娄敬", "role": "official", "link_status": "needs_linking",
    "role_zh_cn": "齐人（刘敬）：首劝说都关中", "review_note": "major01-C：史记·高祖本纪「齐人刘敬说」", "person_id": None},
   {"person_name_raw": "张良", "role": "official", "link_status": "needs_linking",
    "role_zh_cn": "留侯：劝上入都关中", "review_note": "major01-C：史记·高祖本纪「乃留侯劝上入都关中」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "长安", "role": "capital", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "西汉国都", "review_note": "major01-C：史记·高祖本纪「徙治长安」"},
  ],
  "evidence": [
   ev(SJ, "高祖本纪", "十二本纪/高祖本纪#p441", "text-niutrans-14ffbf5db98df1ed2428", "background", "primary", "高祖欲长都雒阳，齐人刘敬说，乃留侯劝上入都关中，高祖是日驾，入都关中。"),
   ev(SJ, "高祖本纪", "十二本纪/高祖本纪#p483", "text-niutrans-957f2f9b3e40e71c161a", "process", "primary", "长乐宫成，丞相已下徙治长安。"),
   ev(SJ, "高祖本纪", "十二本纪/高祖本纪#p544", "text-niutrans-cfb457fe726b5f2c03e7", "result", "primary", "十一月，高祖自布军至长安。"),
   ev(SJ, "项羽本纪", "十二本纪/项羽本纪#p289", "text-niutrans-1e9b41e2b6d12fd3cb30", "impact", "primary", "关中阻山河四塞，地肥饶，可都以霸。"),
  ],
 },
 "qin_han/event-baima-zhi-meng.yml": {
  "background_zh_cn": "高帝封功臣，「封爵之誓曰：使河如带，泰山若厉，国以永宁，爰及苗裔」——盟誓以为信。",
  "process_zh_cn": "高帝刑白马盟曰「非刘氏而王者，天下共击之」——以白马之盟立同姓王继统之制。",
  "result_zh_cn": "盟约行于朝廷：王陵以之面折吕后欲王诸吕之议，盟誓成为汉廷政治共识。",
  "impact_zh_cn": "「非刘氏不王」成为汉家宪制性约束——吕氏虽一时用事，终以诸吕覆灭而刘氏复安，汉祚得延。",
  "people": [
   {"person_name_raw": "刘邦", "role": "monarch", "link_status": "needs_linking",
    "role_zh_cn": "汉高祖：刑白马立盟", "review_note": "major01-C：史记·吕太后本纪「高帝刑白马盟曰 非刘氏而王，天下共击之」", "person_id": None},
   {"person_name_raw": "王陵", "role": "official", "link_status": "needs_linking",
    "role_zh_cn": "右丞相：以盟约折吕后", "review_note": "major01-C：史记·吕太后本纪「王陵曰：高帝刑白马盟」", "person_id": None},
  ],
  "places": [],
  "evidence": [
   ev(SJ, "高祖功臣侯者年表", "十表/高祖功臣侯者年表#p2", "text-niutrans-4e7d17530398f7f2b523", "background", "primary", "封爵之誓曰： 使河如带，泰山若厉，国以永宁，爰及苗裔。"),
   ev(SJ, "吕太后本纪", "十二本纪/吕太后本纪#p63", "text-niutrans-d01c650b0b25bef0880b", "process", "primary", "王陵曰： 高帝刑白马盟曰 非刘氏而王，天下共击之 。"),
   ev(SJ, "吕太后本纪", "十二本纪/吕太后本纪#p63", "text-niutrans-d01c650b0b25bef0880b", "result", "primary", "非刘氏而王，天下共击之。"),
   ev(SJ, "吕太后本纪", "十二本纪/吕太后本纪#p222", "text-niutrans-f259ac49be96f07186a5", "impact", "primary", "遂遣人分部悉捕诸吕男女，无少长皆斩之。", "诸吕覆灭，刘氏复安，盟约终践"),
  ],
 },
 "qin_han/event-baideng-zhiwei.yml": {
  "background_zh_cn": "冒顿以兵至，大破灭东胡王，虏其民人畜产——匈奴极盛于漠北。",
  "process_zh_cn": "高帝先至平城，步兵未尽到，冒顿纵精兵四十万骑围高帝于白登，七日，汉兵中外不得相救饷。",
  "result_zh_cn": "高帝乃使使间厚遗阏氏，阏氏谓冒顿「两主不相困」；士皆持满傅矢外乡，从解角直出——汉军得脱。",
  "impact_zh_cn": "诸将论之曰「以高帝贤武，然尚困于平城」——白登之围使汉廷转为和亲守边，汉匈关系基调自此定下。",
  "people": [
   {"person_name_raw": "刘邦", "role": "monarch", "link_status": "needs_linking",
    "role_zh_cn": "汉高祖：被围白登七日", "review_note": "major01-C：史记·匈奴列传「围高帝於白登，七日」", "person_id": None},
   {"person_name_raw": "冒顿单于", "role": "opponent", "link_status": "needs_linking",
    "role_zh_cn": "匈奴单于：纵精兵四十万骑围帝", "review_note": "major01-C：史记·匈奴列传「冒顿纵精兵四十万骑围高帝於白登」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "白登", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "汉高帝被围之地（平城白登山）", "review_note": "major01-C：史记·匈奴列传「围高帝於白登」"},
   {"place_name_raw": "平城", "role": "city", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "高帝先至之地", "review_note": "major01-C：史记·匈奴列传「高帝先至平城」"},
  ],
  "evidence": [
   ev(SJ, "匈奴列传", "七十列传/匈奴列传#p90", "text-niutrans-5b773bdf213fb63c3886", "background", "primary", "及冒顿以兵至，击，大破灭东胡王，而虏其民人及畜产。"),
   ev(SJ, "匈奴列传", "七十列传/匈奴列传#p125", "text-niutrans-314fdedbd7225b0d629e", "process", "primary", "冒顿纵精兵四十万骑围高帝於白登，七日，汉兵中外不得相救饷。"),
   ev(SJ, "匈奴列传", "七十列传/匈奴列传#p127", "text-niutrans-1b8c4921c3eb425fff87", "result", "primary", "高帝乃使使间厚遗阏氏，阏氏乃谓冒顿曰： 两主不相困。"),
   ev(SJ, "匈奴列传", "七十列传/匈奴列传#p140", "text-niutrans-aadef7725a7312c52c1b", "impact", "primary", "诸将曰： 以高帝贤武，然尚困於平城。"),
  ],
 },
 "qin_han/event-hanhan-heqin.yml": {
  "background_zh_cn": "白登解围后，「汉亦引兵而罢，使刘敬结和亲之约」。",
  "process_zh_cn": "高帝乃使刘敬奉宗室女公主为单于阏氏，岁奉匈奴絮缯酒米食物各有数，约为昆弟以和亲。",
  "result_zh_cn": "和亲成为定制：「故约，汉常遣翁主，给缯絮食物有品，以和亲，而匈奴亦不扰边」。",
  "impact_zh_cn": "和亲之限亦显：军臣单于立四岁，匈奴复绝和亲、大入上郡云中——守边与和亲并行，为文景至武帝前汉匈关系基本形态。",
  "people": [
   {"person_name_raw": "刘敬", "role": "official", "link_status": "needs_linking",
    "role_zh_cn": "奉宗室女公主为单于阏氏、结和亲", "review_note": "major01-C：史记·匈奴列传「使刘敬奉宗室女公主为单于阏氏」", "person_id": None},
  ],
  "places": [],
  "evidence": [
   ev(SJ, "匈奴列传", "七十列传/匈奴列传#p131", "text-niutrans-ab143175928f007f9dde", "background", "primary", "汉亦引兵而罢，使刘敬结和亲之约。"),
   ev(SJ, "匈奴列传", "七十列传/匈奴列传#p136", "text-niutrans-be56dfc2d100cd2b42d0", "process", "primary", "高帝乃使刘敬奉宗室女公主为单于阏氏，岁奉匈奴絮缯酒米食物各有数，约为昆弟以和亲。"),
   ev(SJ, "匈奴列传", "七十列传/匈奴列传#p356", "text-niutrans-03711a3c97fd1d34513a", "result", "primary", "故约，汉常遣翁主，给缯絮食物有品，以和亲，而匈奴亦不扰边。"),
   ev(SJ, "匈奴列传", "七十列传/匈奴列传#p232", "text-niutrans-6dbb22f3904d37c6d2c3", "impact", "primary", "军臣单于立四岁，匈奴复绝和亲，大入上郡、云中各三万骑。"),
  ],
 },
 "qin_han/event-luhou-linchao.yml": {
  "background_zh_cn": "吕太后者，高祖微时妃也，生孝惠帝——惠帝仁弱，吕后以母后之尊渐预朝政。",
  "process_zh_cn": "孝惠崩，高后用事：听诸吕、擅废帝更立，又比杀三赵王，灭梁、赵、燕以王诸吕，分齐为四。",
  "result_zh_cn": "帝废位，太后幽杀之——少帝之立废皆出吕后之意，临朝称制之权至极。",
  "impact_zh_cn": "诸吕皆居中用事：「请拜吕台、吕产、吕禄为将，将兵居南北军」——吕氏外戚短暂取代刘氏掌军政，为汉初外戚政治之始。",
  "people": [
   {"person_name_raw": "吕后", "role": "monarch", "link_status": "needs_linking",
    "role_zh_cn": "皇太后：临朝称制、王诸吕", "review_note": "major01-C：史记·吕太后本纪「孝惠崩，高后用事」", "person_id": None},
   {"person_name_raw": "吕产", "role": "official", "link_status": "needs_linking",
    "role_zh_cn": "吕氏：将兵居南军", "review_note": "major01-C：史记·吕太后本纪「拜吕台、吕产、吕禄为将，将兵居南北军」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "长安", "role": "capital", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "临朝称制、诸吕用事之地", "review_note": "major01-C：史记·吕太后本纪（高后用事）"},
  ],
  "evidence": [
   ev(SJ, "吕太后本纪", "十二本纪/吕太后本纪#p1", "text-niutrans-7f4cdd9b173d7f46bec1", "background", "primary", "吕太后者，高祖微时妃也，生孝惠帝、女鲁元太后。"),
   ev(SJ, "吕太后本纪", "十二本纪/吕太后本纪#p171", "text-niutrans-802d0233c0a90633df39", "process", "primary", "孝惠崩，高后用事，春秋高，听诸吕，擅废帝更立……以王诸吕。"),
   ev(SJ, "吕太后本纪", "十二本纪/吕太后本纪#p102", "text-niutrans-8749aa353ed74b9380fa", "result", "primary", "帝废位，太后幽杀之。"),
   ev(SJ, "吕太后本纪", "十二本纪/吕太后本纪#p55", "text-niutrans-cf78d5b8847ba6085246", "impact", "primary", "请拜吕台、吕产、吕禄为将，将兵居南北军……居中用事。"),
  ],
 },
 "qin_han/event-zhulv.yml": {
  "background_zh_cn": "赵王禄、梁王产各将兵居南北军，皆吕氏之人——吕氏据军权，刘氏宗室人人自危。",
  "process_zh_cn": "太尉周勃驰入北军、报太尉；吕产欲入未央宫为乱而殿门弗得入，裴回往来——军权既夺，事遂定。",
  "result_zh_cn": "遂遣人分部悉捕诸吕男女，无少长皆斩之——诸吕覆灭。",
  "impact_zh_cn": "丞相陈平、太尉周勃等使人迎代王——诛诸吕之后迎立代王刘恒，是为汉文帝，汉家皇统转入新脉。",
  "people": [
   {"person_name_raw": "周勃", "role": "supporter", "link_status": "needs_linking",
    "role_zh_cn": "太尉：入北军、诛诸吕", "review_note": "major01-C：史记·吕太后本纪「驰入北军，报太尉」", "person_id": None},
   {"person_name_raw": "陈平", "role": "supporter", "link_status": "needs_linking",
    "role_zh_cn": "丞相：与周勃谋夺吕氏军", "review_note": "major01-C：史记·孝文本纪「丞相陈平与太尉周勃谋夺吕产等军」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "未央宫", "role": "location", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "吕产欲为乱而不得入之宫", "review_note": "major01-C：史记·吕太后本纪「乃入未央宫，欲为乱，殿门弗得入」"},
   {"place_name_raw": "北军", "role": "location", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "吕禄所掌之军，周勃夺之", "review_note": "major01-C：史记·吕太后本纪「驰入北军」"},
  ],
  "evidence": [
   ev(SJ, "吕太后本纪", "十二本纪/吕太后本纪#p182", "text-niutrans-4177ccb93b1bf68fe5f6", "background", "primary", "赵王禄、梁王产各将兵居南北军，皆吕氏之人。"),
   ev(SJ, "吕太后本纪", "十二本纪/吕太后本纪#p220", "text-niutrans-81d0ffdd59e98995a269", "process", "primary", "还，驰入北军，报太尉。"),
   ev(SJ, "吕太后本纪", "十二本纪/吕太后本纪#p222", "text-niutrans-f259ac49be96f07186a5", "result", "primary", "遂遣人分部悉捕诸吕男女，无少长皆斩之。"),
   ev(SJ, "孝文本纪", "十二本纪/孝文本纪#p6", "text-niutrans-1aa10ad627f5a2d0114c", "impact", "primary", "丞相陈平、太尉周勃等使人迎代王。"),
  ],
 },
 "qin_han/event-hanwendi-jiwei.yml": {
  "background_zh_cn": "丞相陈平、太尉周勃等使人迎代王——诛诸吕后，代王刘恒为宗室之长、众望所归。",
  "process_zh_cn": "代王报太后计之，犹与未定；群臣请「原大王即天子位」，代王西乡让者三、南乡让者再——再三推让而后受。",
  "result_zh_cn": "遂即天子位——刘恒即位，是为汉文帝。",
  "impact_zh_cn": "文帝即位之初即下「农，天下之本，其开籍田，朕亲率耕」之诏——恭俭亲耕，开文景之治。",
  "people": [
   {"person_name_raw": "汉文帝", "role": "monarch", "link_status": "needs_linking",
    "role_zh_cn": "代王刘恒：即位为汉文帝", "review_note": "major01-C：史记·孝文本纪「遂即天子位」", "person_id": None},
   {"person_name_raw": "周勃", "role": "supporter", "link_status": "needs_linking",
    "role_zh_cn": "太尉：迎立代王", "review_note": "major01-C：史记·孝文本纪「使人迎代王」", "person_id": None},
  ],
  "places": [
   {"place_name_raw": "代", "role": "region", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "代王封国，即位前之藩", "review_note": "major01-C：史记·孝文本纪（代王迎立）"},
  ],
  "evidence": [
   ev(SJ, "孝文本纪", "十二本纪/孝文本纪#p6", "text-niutrans-1aa10ad627f5a2d0114c", "background", "primary", "丞相陈平、太尉周勃等使人迎代王。"),
   ev(SJ, "孝文本纪", "十二本纪/孝文本纪#p20", "text-niutrans-372bf81cb40e23305978", "process", "primary", "代王报太后计之，犹与未定。"),
   ev(SJ, "孝文本纪", "十二本纪/孝文本纪#p48", "text-niutrans-6de69e937b78ae6216ff", "process", "supporting", "代王西乡让者三，南乡让者再。"),
   ev(SJ, "孝文本纪", "十二本纪/孝文本纪#p54", "text-niutrans-52f1d2e1108df82f543c", "result", "primary", "遂即天子位。"),
   ev(SJ, "孝文本纪", "十二本纪/孝文本纪#p140", "text-niutrans-b31ed65c53963e68a1d1", "impact", "primary", "农，天下之本，其开籍田，朕亲率耕，以给宗庙粢盛。"),
  ],
 },
 "qin_han/event-wenjing-zhizhi.yml": {
  "background_zh_cn": "孝惠、高后时天下初定，「量吏禄，度官用，以赋于民」——与民休息之政自汉初延续。",
  "process_zh_cn": "文帝亲耕籍田：「农，天下之本，其开籍田，朕亲率耕」；又论「农，天下之本，务莫大焉」——重农劝耕为文景施政之纲。",
  "result_zh_cn": "轻徭薄赋、务农先籍——「务农先籍，布德偃兵」，民生渐裕。",
  "impact_zh_cn": "「汉兴七十余年之间，国家无事，非遇水旱之灾，民则人给家足，都鄙廪庾皆满，而府库余货财」——文景之治的积累为汉武帝的作为与汉匈战争奠定国力。",
  "people": [
   {"person_name_raw": "汉文帝", "role": "monarch", "link_status": "needs_linking",
    "role_zh_cn": "重农亲耕、与民休息", "review_note": "major01-C：史记·孝文本纪「朕亲率耕」", "person_id": None},
   {"person_name_raw": "汉景帝", "role": "monarch", "link_status": "needs_linking",
    "role_zh_cn": "继文帝之政（文景并称）", "review_note": "major01-C：史记·平准书「汉兴七十余年之间，国家无事」", "person_id": None},
  ],
  "places": [],
  "evidence": [
   ev(SJ, "平准书", "八书/平准书#p5", "text-niutrans-8f33c0ab7063f55133ac", "background", "primary", "孝惠、高后时，为天下初定，复弛商贾之律……量吏禄，度官用，以赋于民。"),
   ev(SJ, "孝文本纪", "十二本纪/孝文本纪#p140", "text-niutrans-b31ed65c53963e68a1d1", "process", "primary", "农，天下之本，其开籍田，朕亲率耕。"),
   ev(SJ, "孝文本纪", "十二本纪/孝文本纪#p201", "text-niutrans-603f2e91c782907c28dc", "result", "primary", "农，天下之本，务莫大焉。"),
   ev(SJ, "平准书", "八书/平准书#p16", "text-niutrans-88b7ed1ffd6e61a487be", "impact", "primary", "汉兴七十余年之间，国家无事，非遇水旱之灾，民则人给家足，都鄙廪庾皆满，而府库余货财。"),
   ev(SJ, "孝文本纪", "十二本纪/孝文本纪#p306", "text-niutrans-c3da0b9d8656e0369920", "impact", "supporting", "务农先籍，布德偃兵。"),
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
