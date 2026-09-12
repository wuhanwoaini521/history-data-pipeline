"""Overnight Queue 08 · 14 Critical Events 纵向富化（Batch 01，source-backed）。

原则（AGENTS.md §7/§17 + overnight 指令）：
- 叙述字段（background/process/result/impact）全部从本轮已读入的语料原文提取整理，
  每条以 evidence 行回链到具体段落（chapter_anchor#p行号 + historical_text_id），
  review_note 记录逐字引文 —— 无逐字引文支撑的字段保持 NEEDS_SOURCE 不填。
- 只处理语料覆盖的 6 个事件；8 个 20 世纪/西夏事件语料缺失，今晚不补，保持缺口。
- evidence 行 claim_field 标注所支持字段；link_method=manual（agent 已逐句核对引文）。
- 幂等：review_note 带 marker（overnight-08）的行不重复添加。

anchors 键为 (语料相对路径, 行号)；行号 = paragraph_index（与 text_id 生成一致）。
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / "data" / "normalized" / "history.duckdb"
MARKER = "overnight-08"


def text_id(rel_path: str, line_number: int) -> str:
    return "text-niutrans-" + hashlib.sha1(f"{rel_path}:{line_number}".encode("utf-8")).hexdigest()[:20]


B = "repository/双语数据"

# 逐事件富化数据（叙述文字由语料原文提取整理；引文逐字来自 source.txt 对应行）
ENRICHMENTS: list[dict] = [
    {
        "event_id": "event-mongol-jianguo",
        "fields": {
            "background_zh_cn": "铁木真起于蒙古高原部落兼并之中，先后与泰赤乌、汪罕（克烈）、乃蛮等部长期征战：先会汪罕于萨里河，与泰赤乌部大战于斡难河上而败之；后移军斡难河源谋攻汪罕，诸部次第降附，统一之势已成。",
            "process_zh_cn": "乙丑年（1205）先征西夏，拔力吉里寨，经落思城而还。元年丙寅（1206），铁木真大会诸王群臣，建九斿白旗，即皇帝位于斡难河之源，诸王群臣共上尊号曰成吉思皇帝。即位后旋发兵复征乃蛮：于兀鲁塔山擒卜欲鲁罕，乃蛮太阳罕之子屈出律与脱脱奔也儿的石河。",
            "result_zh_cn": "大蒙古国（Yeke Mongghol Ulus）正式建成，铁木真受尊号「成吉思皇帝」。至也儿的石河讨灭蔑里乞部，脱脱中流矢死，屈出律奔契丹（西辽）；四年己巳（1209）春，畏吾儿国来归，草原诸部归于一统。",
            "impact_zh_cn": "即位当年「帝始议伐金」——以金人杀害宗亲咸补海罕为由定议致讨，并连年用兵西夏（乙丑、丁卯两征，克斡罗孩城），遣使乞力吉思、通使诸部。蒙古自草原统一战争转向对外扩张，金与西夏成为最初目标。",
        },
        "people": [
            {"person_name_raw": "屈出律", "role": "opponent", "link_status": "needs_linking",
             "role_zh_cn": "乃蛮太阳罕之子，兵败奔契丹",
             "review_note": f"{MARKER}：元史·太祖纪 行245「至也儿的石河，讨蔑里乞部，灭之，脱脱中流矢死，屈出律奔契丹。」"},
        ],
        "places": [
            {"place_name_raw": "斡难河源", "role": "location", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "1206 年铁木真即皇帝位、建九斿白旗之地",
             "review_note": f"{MARKER}：元史·太祖纪 行230「即皇帝位于斡难河之源」"},
            {"place_name_raw": "也儿的石河", "role": "battlesite", "link_status": "needs_linking", "sequence": 2,
             "description_zh_cn": "乃蛮残余与蔑里乞败亡之地",
             "review_note": f"{MARKER}：元史·太祖纪 行245「至也儿的石河，讨蔑里乞部，灭之…屈出律奔契丹」"},
        ],
        "evidence": [
            {"rel": f"{B}/元史/本纪/卷一/source.txt", "line": 230, "work": "元史", "term": "太祖纪",
             "chapter_anchor": "本纪/卷一#p230", "claim_field": "process", "evidence_role": "primary",
             "quote": "元年丙寅，帝大会诸王群臣，建九斿白旗，即皇帝位于斡难河之源，诸王群臣共上尊号曰成吉思皇帝。"},
            {"rel": f"{B}/元史/本纪/卷一/source.txt", "line": 236, "work": "元史", "term": "太祖纪",
             "chapter_anchor": "本纪/卷一#p236", "claim_field": "impact", "evidence_role": "supporting",
             "quote": "帝始议伐金。初，金杀帝宗亲咸补海罕，帝欲复仇。"},
            {"rel": f"{B}/元史/本纪/卷一/source.txt", "line": 245, "work": "元史", "term": "太祖纪",
             "chapter_anchor": "本纪/卷一#p245", "claim_field": "result", "evidence_role": "supporting",
             "quote": "至也儿的石河，讨蔑里乞部，灭之，脱脱中流矢死，屈出律奔契丹。"},
            {"rel": f"{B}/元史/本纪/卷一/source.txt", "line": 115, "work": "元史", "term": "太祖纪",
             "chapter_anchor": "本纪/卷一#p115", "claim_field": "background", "evidence_role": "supporting",
             "quote": "时泰赤乌犹强，帝会汪罕于萨里河，与泰赤乌部长沆忽等大战斡难河上，败走之，斩获无算。"},
        ],
    },
    {
        "event_id": "event-yuan-jianguo",
        "fields": {
            "background_zh_cn": "中统元年（1260），忽必烈即皇帝位（元史·世祖纪：辛卯，帝即皇帝位），冬驻燕京近郊，设燕京路宣慰司抚治之，以开平府为草创期政治中心（诸路市马、运米皆输开平府）。",
            "process_zh_cn": "至元八年（1271）十一月，禁行金《泰和律》；刘秉忠、王磐、徒单公履等建言正元正朝会圣节诏赦百官宣敕之仪，诏从之；同月乙亥，诏告天下：建国号曰大元。",
            "result_zh_cn": "国号正式定为「大元」——诏书明言「可建国号曰大元，盖取《易经》乾元之义」，一改秦汉以「初起之地名」、隋唐以「所封之爵邑」命名的旧例；同期颁行新朝仪、废金律。",
            "impact_zh_cn": "诏书自陈立号之义：「诞膺景命，奄四海以宅尊；必有美名，绍百王而纪统」，以绍续百王之正统自命；「事从因革，道协天人」。国号的义理化命名与禁金律、定朝仪同批推行，标志蒙元政权从草原大汗体制向中原王朝体制的制度转向。",
        },
        "people": [
            {"person_name_raw": "刘秉忠", "role": "minister", "link_status": "needs_linking",
             "role_zh_cn": "建言朝仪、参预立制",
             "review_note": f"{MARKER}：元史·世祖纪 卷七 行274「乙亥，刘秉忠及王磐、徒单公履等言：元正、朝会、圣节、诏赦及百官宣敕，具公服迎拜行礼。从之。」"},
        ],
        "places": [
            {"place_name_raw": "开平府", "role": "capital", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "世祖即位前后草创期政治中心（诸路市马、运米输开平府）",
             "review_note": f"{MARKER}：元史·世祖纪 卷四 行82「征诸路兵三万驻燕京近地，命诸路市马万匹送开平府。」"},
            {"place_name_raw": "燕京", "role": "location", "link_status": "needs_linking", "sequence": 2,
             "description_zh_cn": "世祖即位之冬驻跸近郊，置燕京路宣慰使",
             "review_note": f"{MARKER}：元史·世祖纪 卷四 行17「是冬，驻燕京近郊」、行21「以祃祃、赵璧、董文炳为燕京路宣慰使」"},
        ],
        "evidence": [
            {"rel": f"{B}/元史/本纪/卷七/source.txt", "line": 288, "work": "元史", "term": "世祖纪",
             "chapter_anchor": "本纪/卷七#p288", "claim_field": "result", "evidence_role": "primary",
             "quote": "可建国号曰大元，盖取《易经》 乾元 之义。"},
            {"rel": f"{B}/元史/本纪/卷七/source.txt", "line": 277, "work": "元史", "term": "世祖纪",
             "chapter_anchor": "本纪/卷七#p277", "claim_field": "impact", "evidence_role": "supporting",
             "quote": "诞膺景命，奄四海以宅尊；必有美名，绍百王而纪统。"},
            {"rel": f"{B}/元史/本纪/卷七/source.txt", "line": 275, "work": "元史", "term": "世祖纪",
             "chapter_anchor": "本纪/卷七#p275", "claim_field": "process", "evidence_role": "supporting",
             "quote": "禁行金《泰和律》。"},
            {"rel": f"{B}/元史/本纪/卷四/source.txt", "line": 21, "work": "元史", "term": "世祖纪",
             "chapter_anchor": "本纪/卷四#p21", "claim_field": "background", "evidence_role": "supporting",
             "quote": "辛卯，帝即皇帝位，以祃祃、赵璧、董文炳为燕京路宣慰使。"},
        ],
    },
    {
        "event_id": "event-pingwang-dongqian",
        "fields": {
            "background_zh_cn": "幽王宠褒姒，废申后与太子宜臼；又任虢石父为卿用事，国人皆怨；烽火数举而失信于诸侯。申侯积怒，周王室内部与外戚、西戎的矛盾总爆发。",
            "process_zh_cn": "申侯联合缯与西夷犬戎攻幽王；幽王举烽火徵兵，诸侯兵莫至。犬戎遂杀幽王于骊山下，虏褒姒，尽取周赂而去。",
            "result_zh_cn": "诸侯即申侯之约，共立故幽王太子宜臼，是为平王，以奉周祀；平王即位后东迁于雒邑，以避戎寇。西周亡而东周始。",
            "impact_zh_cn": "史迁总括平王之世：「周室衰微，诸侯彊并弱，齐、楚、秦、晋始大，政由方伯」——王室权威跌落、政令移于方伯，列国争霸的春秋格局自此开启。",
        },
        "people": [
            {"person_name_raw": "周平王", "role": "monarch", "link_status": "needs_linking",
             "role_zh_cn": "故幽王太子宜臼，诸侯共立，东迁雒邑",
             "review_note": f"{MARKER}：史记·周本纪 行364「共立故幽王太子宜臼，是为平王，以奉周祀」、行365「平王立，东迁于雒邑」"},
            {"person_name_raw": "申侯", "role": "instigator", "link_status": "needs_linking",
             "role_zh_cn": "联合缯、犬戎攻幽王，拥立平王",
             "review_note": f"{MARKER}：史记·周本纪 行361「申侯怒，与缯、西夷犬戎攻幽王」、行364「诸侯乃即申侯而共立…宜臼」"},
            {"person_name_raw": "周幽王", "role": "deposed_monarch", "link_status": "needs_linking",
             "role_zh_cn": "废申后太子、烽火失信，死于骊山",
             "review_note": f"{MARKER}：史记·周本纪 行363「遂杀幽王骊山下，虏襃姒，尽取周赂而去」"},
        ],
        "places": [
            {"place_name_raw": "雒邑", "role": "destination", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "平王东迁之都邑（成周）",
             "review_note": f"{MARKER}：史记·周本纪 行365「平王立，东迁于雒邑，辟戎寇」"},
            {"place_name_raw": "骊山", "role": "battlesite", "link_status": "needs_linking", "sequence": 2,
             "description_zh_cn": "幽王被杀之地",
             "review_note": f"{MARKER}：史记·周本纪 行363「遂杀幽王骊山下」"},
        ],
        "evidence": [
            {"rel": f"{B}/史记/十二本纪/周本纪/source.txt", "line": 365, "work": "史记", "term": "周本纪",
             "chapter_anchor": "十二本纪/周本纪#p365", "claim_field": "result", "evidence_role": "primary",
             "quote": "於是诸侯乃即申侯而共立故幽王太子宜臼，是为平王，以奉周祀。平王立，东迁于雒邑，辟戎寇。"},
            {"rel": f"{B}/史记/十二本纪/周本纪/source.txt", "line": 361, "work": "史记", "term": "周本纪",
             "chapter_anchor": "十二本纪/周本纪#p361", "claim_field": "process", "evidence_role": "primary",
             "quote": "申侯怒，与缯、西夷犬戎攻幽王。"},
            {"rel": f"{B}/史记/十二本纪/周本纪/source.txt", "line": 366, "work": "史记", "term": "周本纪",
             "chapter_anchor": "十二本纪/周本纪#p366", "claim_field": "impact", "evidence_role": "supporting",
             "quote": "平王之时，周室衰微，诸侯彊并弱，齐、楚、秦、晋始大，政由方伯。"},
            {"rel": f"{B}/史记/十二本纪/周本纪/source.txt", "line": 358, "work": "史记", "term": "周本纪",
             "chapter_anchor": "十二本纪/周本纪#p358", "claim_field": "background", "evidence_role": "supporting",
             "quote": "幽王以虢石父为卿，用事，国人皆怨。"},
        ],
    },
    {
        "event_id": "event-chuzhuang-wang-ba",
        "fields": {
            "background_zh_cn": "庄王即位三年不出号令、日夜为乐，伍举以「三年不蜚不鸣」之鸟讽谏，庄王答「三年不蜚，蜚将冲天；三年不鸣，鸣将惊人」，随即亲政振作，楚势日张。",
            "process_zh_cn": "八年（前606）伐陆浑戎，遂至洛，观兵于周郊，遣人问鼎之大小轻重，王孙满对以「在德不在鼎」，庄王乃归。十七年（前597）春围郑，三月克之，郑伯肉袒牵羊逆降，庄王引兵退三十里许其求平；夏六月，晋出兵救郑，楚与晋战于河上，大败晋师，遂至衡雍而归。",
            "result_zh_cn": "邲之战（河上之役）大败晋师，楚庄王代晋主盟中原；二十年（前594）围宋五月，宋城中食尽、易子而食，华元出告以情，庄王罢兵而去——郑、宋诸国皆服从于楚。",
            "impact_zh_cn": "庄王以「以义伐之而贪其县，亦何以复令于天下」复国陈后，立信义于诸侯，霸主政治以德义为号召。楚霸虽成，晋楚相争未绝：庄王卒后至共王十六年（前575），晋楚战于鄢陵，晋败楚、射中共王目，两国争霸长期拉锯。",
        },
        "people": [
            {"person_name_raw": "楚庄王", "role": "monarch", "link_status": "needs_linking",
             "role_zh_cn": "问鼎中原、邲之战败晋、主盟中原",
             "review_note": f"{MARKER}：史记·楚世家 行139「楚王问鼎小大轻重」、行172「大败晋师河上」"},
            {"person_name_raw": "王孙满", "role": "envoy", "link_status": "needs_linking",
             "role_zh_cn": "周定王使，劳楚王并以「在德不在鼎」答问鼎",
             "review_note": f"{MARKER}：史记·楚世家 行138-139「周定王使王孙满劳楚王。楚王问鼎小大轻重，对曰：在德不在鼎。」"},
        ],
        "places": [
            {"place_name_raw": "洛", "role": "location", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "庄王伐陆浑戎后观兵周郊、问鼎之地",
             "review_note": f"{MARKER}：史记·楚世家 行138「伐陆浑戎，遂至洛，观兵于周郊」"},
            {"place_name_raw": "郑", "role": "battlesite", "link_status": "needs_linking", "sequence": 2,
             "description_zh_cn": "庄王十七年围郑三月克之",
             "review_note": f"{MARKER}：史记·楚世家 行162「十七年春，楚庄王围郑，三月克之」"},
        ],
        "evidence": [
            {"rel": f"{B}/史记/三十世家/楚世家/source.txt", "line": 172, "work": "史记", "term": "楚世家",
             "chapter_anchor": "三十世家/楚世家#p172", "claim_field": "result", "evidence_role": "primary",
             "quote": "夏六月，晋救郑，与楚战，大败晋师河上，遂至衡雍而归。"},
            {"rel": f"{B}/史记/三十世家/楚世家/source.txt", "line": 139, "work": "史记", "term": "楚世家",
             "chapter_anchor": "三十世家/楚世家#p139", "claim_field": "process", "evidence_role": "primary",
             "quote": "楚王问鼎小大轻重，对曰： 在德不在鼎。"},
            {"rel": f"{B}/史记/三十世家/楚世家/source.txt", "line": 160, "work": "史记", "term": "楚世家",
             "chapter_anchor": "三十世家/楚世家#p160", "claim_field": "impact", "evidence_role": "supporting",
             "quote": "且王以陈之乱而率诸侯伐之，以义伐之而贪其县，亦何以复令于天下！"},
            {"rel": f"{B}/史记/三十世家/楚世家/source.txt", "line": 128, "work": "史记", "term": "楚世家",
             "chapter_anchor": "三十世家/楚世家#p128", "claim_field": "background", "evidence_role": "supporting",
             "quote": "庄王曰： 三年不蜚，蜚将冲天；三年不鸣，鸣将惊人。"},
        ],
    },
    {
        "event_id": "event-jinwen-gong-ba",
        "fields": {
            "background_zh_cn": "楚围宋急，晋文公救宋而攻楚之与国：二十有八年（前632）春，晋侯侵曹、伐卫，假道于卫不获；楚人出兵救卫，晋楚两军相向。",
            "process_zh_cn": "三月丙午，晋侯入曹，执曹伯，畀宋人；夏四月己巳，晋侯、齐师、宋师、秦师及楚人战于城濮，楚师败绩。楚杀其大夫得臣，卫侯出奔楚。",
            "result_zh_cn": "五月癸丑，公会晋侯、齐侯、宋公、蔡侯、郑伯、卫子、莒子盟于践土，陈侯如会；晋文公率诸侯朝于王所——践土之盟确立晋国盟主之位，晋文公霸业告成。",
            "impact_zh_cn": "是年冬，公会晋侯、齐侯、宋公、蔡侯、郑伯、陈子、莒子、邾子、秦人于温——城濮胜后晋国以会盟号召诸侯的霸政体制持续运转，晋国自此长期为中原盟主。",
        },
        "people": [
            {"person_name_raw": "晋文公", "role": "monarch", "link_status": "needs_linking",
             "role_zh_cn": "盟主：城濮败楚、践土主盟",
             "review_note": f"{MARKER}：左传·僖公二十八年 行6「晋侯…及楚人战于城濮，楚师败绩」、行9「盟于践土」"},
            {"person_name_raw": "得臣", "role": "opponent", "link_status": "needs_linking",
             "role_zh_cn": "楚大夫（子玉），城濮败后为楚所杀",
             "review_note": f"{MARKER}：左传·僖公二十八年 行7「楚杀其大夫得臣」"},
        ],
        "places": [
            {"place_name_raw": "城濮", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "晋楚决战之地",
             "review_note": f"{MARKER}：左传·僖公二十八年 行6「战于城濮，楚师败绩」"},
            {"place_name_raw": "践土", "role": "assembly_site", "link_status": "needs_linking", "sequence": 2,
             "description_zh_cn": "晋文公会盟诸侯之地（作王宫于践土）",
             "review_note": f"{MARKER}：左传·僖公二十八年 行9「盟于践土」、行109「作王宫于践土」"},
        ],
        "evidence": [
            {"rel": f"{B}/左传/僖公/僖公二十八年/source.txt", "line": 9, "work": "左传", "term": "僖公二十八年",
             "chapter_anchor": "僖公/僖公二十八年#p9", "claim_field": "result", "evidence_role": "primary",
             "quote": "五月癸丑，公会晋侯、齐侯、宋公、蔡侯、郑伯、卫子、莒子，盟于践土。"},
            {"rel": f"{B}/左传/僖公/僖公二十八年/source.txt", "line": 6, "work": "左传", "term": "僖公二十八年",
             "chapter_anchor": "僖公/僖公二十八年#p6", "claim_field": "process", "evidence_role": "primary",
             "quote": "夏四月己巳，晋侯、齐师、宋师、秦师及楚人战于城濮，楚师败绩。"},
            {"rel": f"{B}/左传/僖公/僖公二十八年/source.txt", "line": 16, "work": "左传", "term": "僖公二十八年",
             "chapter_anchor": "僖公/僖公二十八年#p16", "claim_field": "impact", "evidence_role": "supporting",
             "quote": "冬，公会晋侯、齐侯、宋公、蔡侯、郑伯、陈子、莒子、邾子、秦人于温。"},
            {"rel": f"{B}/左传/僖公/僖公二十八年/source.txt", "line": 1, "work": "左传", "term": "僖公二十八年",
             "chapter_anchor": "僖公/僖公二十八年#p1", "claim_field": "background", "evidence_role": "supporting",
             "quote": "二十有八年春，晋侯侵曹。晋侯伐卫。"},
        ],
    },
    {
        "event_id": "event-hezong-lianheng",
        "fields": {
            "background_zh_cn": "秦强而诸侯弱：苏秦按天下地图案之，「诸侯之地五倍於秦，料度诸侯之卒十倍於秦」，主张「六国为一，并力西乡而攻秦，秦必破矣」；否则从亲则诸侯割地事楚、衡合则楚割地事秦，两策对峙为战国外交基本格局。",
            "process_zh_cn": "苏秦先后说燕、赵等国，赵肃侯封为武安君；说楚王以「秦，虎狼之国，不可亲也」动之，楚王自陈「谨奉社稷以从」。於是六国从合而并力，苏秦为从约长，并相六国，乃投从约书于秦。",
            "result_zh_cn": "合纵既成，「秦兵不敢闚函谷关十五年」——秦国东出被合纵封锁十五年。",
            "impact_zh_cn": "其后秦使犀首欺齐、魏，与共伐赵，欲败从约——合纵自此始遭离间；而「从亲/衡合」两策自此成为战国中后期列国外交与纵横家活动的主轴。",
        },
        "people": [
            {"person_name_raw": "苏秦", "role": "diplomat", "link_status": "needs_linking",
             "role_zh_cn": "合纵发起者：从约长，并相六国",
             "review_note": f"{MARKER}：史记·苏秦列传 行171-172「於是六国从合而并力焉。苏秦为从约长，并相六国。」"},
            {"person_name_raw": "赵肃侯", "role": "supporter", "link_status": "needs_linking",
             "role_zh_cn": "封苏秦为武安君，合纵之约自赵出",
             "review_note": f"{MARKER}：史记·苏秦列传 行184「苏秦既约六国从亲，归赵，赵肃侯封为武安君」"},
        ],
        "places": [
            {"place_name_raw": "函谷关", "role": "frontier", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "合纵封锁下秦兵十五年不敢东出之关",
             "review_note": f"{MARKER}：史记·苏秦列传 行185「秦兵不敢闚函谷关十五年」"},
        ],
        "evidence": [
            {"rel": f"{B}/史记/七十列传/苏秦列传/source.txt", "line": 171, "work": "史记", "term": "苏秦列传",
             "chapter_anchor": "七十列传/苏秦列传#p171", "claim_field": "process", "evidence_role": "primary",
             "quote": "於是六国从合而并力焉。苏秦为从约长，并相六国。"},
            {"rel": f"{B}/史记/七十列传/苏秦列传/source.txt", "line": 185, "work": "史记", "term": "苏秦列传",
             "chapter_anchor": "七十列传/苏秦列传#p185", "claim_field": "result", "evidence_role": "primary",
             "quote": "秦兵不敢闚函谷关十五年。"},
            {"rel": f"{B}/史记/七十列传/苏秦列传/source.txt", "line": 186, "work": "史记", "term": "苏秦列传",
             "chapter_anchor": "七十列传/苏秦列传#p186", "claim_field": "impact", "evidence_role": "supporting",
             "quote": "其後秦使犀首欺齐、魏，与共伐赵，欲败从约。"},
            {"rel": f"{B}/史记/七十列传/苏秦列传/source.txt", "line": 69, "work": "史记", "term": "苏秦列传",
             "chapter_anchor": "七十列传/苏秦列传#p69", "claim_field": "background", "evidence_role": "supporting",
             "quote": "臣窃以天下之地图案之，诸侯之地五倍於秦，料度诸侯之卒十倍於秦，六国为一，并力西乡而攻秦，秦必破矣。"},
        ],
    },
]


def load_event(events_dir: Path, event_id: str):
    from history_data_pipeline.backbone.evidence_link import _load_event_yaml
    hits = list(events_dir.rglob(f"{event_id}.yml"))
    if not hits:
        raise FileNotFoundError(event_id)
    doc, blocks = _load_event_yaml(hits[0])
    return hits[0], doc, blocks


def verify_anchor(connection, rel: str, line: int) -> str:
    tid = text_id(rel, line)
    row = connection.execute(
        "SELECT paragraph_index, original_simplified FROM historical_texts WHERE id = ?", [tid]
    ).fetchone()
    if row is None:
        raise RuntimeError(f"锚点 id 不存在于知识库: {tid} ({rel}:{line})")
    return tid


def main() -> int:
    import duckdb

    from history_data_pipeline.backbone.product_completeness import event_completeness

    events_dir = ROOT / "data" / "curated" / "history_backbone" / "events"
    connection = duckdb.connect(str(KB), read_only=True)
    written = 0
    print("== 14 Critical 纵向富化（Batch 01，source-backed）==")
    for spec in ENRICHMENTS:
        path, doc, (head_block, tail_block) = load_event(events_dir, spec["event_id"])
        before = event_completeness(doc)
        for field, value in spec["fields"].items():
            if not (doc.get(field) or "").strip():
                doc[field] = value
        for person in spec.get("people", []):
            # 幂等 + schema 修补：event_person schema 要求 person_id 键存在（可空）
            existing_people = doc.get("people") or []
            match = next((p for p in existing_people
                          if p.get("person_name_raw") == person["person_name_raw"]
                          and MARKER in (p.get("review_note") or "")), None)
            if match is None:
                entry = dict(person)
                entry.setdefault("person_id", None)
                existing_people.append(entry)
                doc["people"] = existing_people
            else:
                match.setdefault("person_id", None)
        for place in spec.get("places", []):
            existing_places = doc.get("places") or []
            match = next((pl for pl in existing_places
                          if pl.get("place_name_raw") == place["place_name_raw"]
                          and MARKER in (pl.get("review_note") or "")), None)
            if match is None:
                existing_places.append(place)
                doc["places"] = existing_places
        for ev in spec["evidence"]:
            tid = verify_anchor(connection, ev["rel"], ev["line"])
            note = (f"{MARKER}：source-grounded 提取（{ev['rel']}:{ev['line']}）引文：「{ev['quote']}」"
                    f"；claim_field={ev['claim_field']}；anchor=段落精确锚")
            existing = [
                (e.get("chapter_anchor"), e.get("claim_field"), e.get("review_note") or "")
                for e in (doc.get("evidence") or [])
            ]
            if any(a == ev["chapter_anchor"] and c == ev["claim_field"] for a, c, _ in existing):
                continue
            doc.setdefault("evidence", []).append({
                "work": ev["work"], "term": ev["term"],
                "historical_text_id": tid,
                "chapter_anchor": ev["chapter_anchor"],
                "claim_field": ev["claim_field"],
                "evidence_role": ev["evidence_role"],
                "link_status": "linked",
                "link_method": "manual",
                "link_confidence": 1.0,
                "link_quality_status": "reviewed",
                "context_keywords": [],
                "review_note": note,
            })
        after = event_completeness(doc)
        yaml_text = head_block + yaml.safe_dump(doc, allow_unicode=True, sort_keys=False) + tail_block
        path.write_text(yaml_text, encoding="utf-8")
        written += 1
        print(f"{spec['event_id']}: {before['product_completeness_score']} -> {after['product_completeness_score']}"
              f"  missing(before)={before['missing']} missing(after)={after['missing']}")
    connection.close()
    print(f"written: {written} events")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
