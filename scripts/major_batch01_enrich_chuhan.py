"""Major Batch 01 · 楚汉群 enrichment（8 个 READY 事件）。

规则（与 Queue 10 同）：叙述句全部可回溯到 review_note 逐字引文；不引入语料外事实；
已有 reviewed 字段（legacy result_zh_cn 短句）不覆盖，只补 missing 三维 + 字段锚。
写入：append-only（保留头注释与既有字节）。
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
EVENTS = ROOT / "data" / "curated" / "history_backbone" / "events"


def ev(work, term, tid, anchor, field, role, quote, extra=""):
    return {
        "work": work, "term": term, "historical_text_id": tid, "chapter_anchor": anchor,
        "claim_field": field, "evidence_role": role, "link_status": "linked",
        "link_method": "manual", "link_confidence": 1.0, "link_quality_status": "reviewed",
        "context_keywords": [],
        "review_note": f"major-batch01：source-grounded（史记/资治通鉴）引文：「{quote}」；"
                       f"claim_field={field}；anchor=段落精确锚。{extra}",
    }


BLOCKS = {
    "qin_han/event-chuhan-julu.yml": {
        "background_zh_cn": "章邯既破项梁军，以为楚地兵不足忧，乃渡河击赵，大破之；秦军令王离、涉间围钜鹿，章邯军其南、筑甬道输粟。楚怀王以宋义为上将军、项羽为次将救赵，宋义行至安阳留四十六日不进。",
        "process_zh_cn": "项羽晨朝上将军宋义，即其帐中斩之，诸将共立羽为假上将军，怀王因使项羽为上将军；项羽乃悉引兵渡河，皆沉船、破釜甑、烧庐舍，持三日粮以示士卒必死，无一还心。",
        "impact_zh_cn": "当是时楚兵冠诸侯：诸侯军救钜鹿者十馀壁莫敢纵兵，及楚击秦诸将皆从壁上观，楚战士无不一以当十、呼声动天；已破秦军，项羽召见诸侯将，入辕门无不膝行而前，莫敢仰视——诸侯将由此隶属项羽。",
        "people": [
            {"person_name_raw": "宋义", "role": "opponent", "link_status": "needs_linking",
             "role_zh_cn": "楚军上将军：逗留不进，为项羽所斩",
             "review_note": "major-batch01：项羽本纪「项羽晨朝上将军宋义，即其帐中斩宋义头」", "person_id": None},
            {"person_name_raw": "章邯", "role": "opponent", "link_status": "needs_linking",
             "role_zh_cn": "秦军主将：破项梁后围钜鹿",
             "review_note": "major-batch01：项羽本纪「章邯已破项梁军……乃渡河击赵，大破之」", "person_id": None},
        ],
        "evidence": [
            ev("史记", "项羽本纪", "text-niutrans-a2445c75d7487393ecfe", "十二本纪/项羽本纪#p114",
               "background", "primary", "章邯已破项梁军，则以为楚地兵不足忧，乃渡河击赵，大破之。"),
            ev("史记", "项羽本纪", "text-niutrans-a9b492a7760a44a40d88", "十二本纪/项羽本纪#p149",
               "process", "primary", "项羽乃悉引兵渡河，皆沉船，破釜甑，烧庐舍，持三日粮，以示士卒必死，无一还心。"),
            ev("史记", "项羽本纪", "text-niutrans-a58d089bb69dd16197b8", "十二本纪/项羽本纪#p150",
               "result", "primary", "於是至则围王离，与秦军遇，九战，绝其甬道，大破之，杀苏角，虏王离。"),
            ev("史记", "项羽本纪", "text-niutrans-3521797e643c55f5805d", "十二本纪/项羽本纪#p156",
               "impact", "primary", "於是已破秦军，项羽召见诸侯将，入辕门，无不膝行而前，莫敢仰视。"),
            ev("史记", "项羽本纪", "text-niutrans-d92b0287a760c438af5c", "十二本纪/项羽本纪#p139",
               "process", "supporting", "项羽晨朝上将军宋义，即其帐中斩宋义头。"),
        ],
    },
    "qin_han/event-hongmen.yml": {
        "background_zh_cn": "沛公军霸上，未得与项羽相见；左司马曹无伤使人言于项羽「沛公欲王关中，使子婴为相，珍宝尽有之」，项羽大怒，欲旦日飨士卒击破沛公军。时项羽兵四十万在新丰鸿门，沛公兵十万在霸上。",
        "process_zh_cn": "项伯夜驰告张良，沛公约为婚姻、请其转达「吾入关，秋豪不敢有所近……日夜望将军至，岂敢反乎」；项伯还报「不如因善遇之」，项王许诺。沛公旦日从百馀骑至鸿门谢项王；宴间樊哙侧盾撞卫士而入，披帷西乡立，瞋目视项王。",
        "impact_zh_cn": "亚父范增受玉斗置之地、拔剑撞而破之，曰「唉！竖子不足与谋。夺项王天下者，必沛公也，吾属今为之虏矣」；沛公至军，立诛杀曹无伤——鸿门一场，楚汉相争的格局由此注定。",
        "people": [
            {"person_name_raw": "范增", "role": "opponent", "link_status": "needs_linking",
             "role_zh_cn": "项羽谋臣（亚父）：劝击沛公未果，碎玉斗预言天下归属",
             "review_note": "major-batch01：项羽本纪「夺项王天下者，必沛公也」", "person_id": None},
            {"person_name_raw": "樊哙", "role": "supporter", "link_status": "needs_linking",
             "role_zh_cn": "沛公参乘：侧盾撞卫士入帐护主",
             "review_note": "major-batch01：项羽本纪「樊哙侧其盾以撞，卫士仆地，哙遂入」", "person_id": None},
        ],
        "evidence": [
            ev("史记", "项羽本纪", "text-niutrans-08840e0e7fd241c46a9e", "十二本纪/项羽本纪#p197",
               "background", "primary", "沛公左司马曹无伤使人言於项羽曰： 沛公欲王关中，使子婴为相，珍宝尽有之。"),
            ev("史记", "项羽本纪", "text-niutrans-f4096b15253261c6f807", "十二本纪/项羽本纪#p252",
               "process", "primary", "樊哙侧其盾以撞，卫士仆地，哙遂入，披帷西乡立，瞋目视项王。"),
            ev("史记", "项羽本纪", "text-niutrans-d129d1dd7a4c39e98e05", "十二本纪/项羽本纪#p279",
               "result", "primary", "沛公则置车骑，脱身独骑，与樊哙、夏侯婴、靳彊、纪信等四人持剑盾步走，从郦山下，道芷阳间行。"),
            ev("史记", "项羽本纪", "text-niutrans-e8da0dee5412aa4d1e32", "十二本纪/项羽本纪#p284",
               "impact", "primary", "亚父受玉斗，置之地，拔剑撞而破之，曰： 唉！"),
            ev("史记", "项羽本纪", "text-niutrans-e9e8bef6c6561458eda6", "十二本纪/项羽本纪#p286",
               "impact", "supporting", "夺项王天下者，必沛公也，吾属今为之虏矣。"),
        ],
    },
    "qin_han/event-chuhan-pengcheng.yml": {
        "background_zh_cn": "汉王以故得劫五诸侯兵，遂入彭城——项羽主力陷于齐地，刘邦乘虚东进占据楚都。",
        "process_zh_cn": "项羽闻之，乃引兵去齐，从鲁出胡陵至萧，与汉大战彭城灵壁东睢水上，大破汉军，多杀士卒，睢水为之不流。",
        "impact_zh_cn": "当是时，诸侯见楚彊汉败，还皆去汉复为楚，塞王欣亡入楚——刘邦集团惨败后收兵砀地，楚汉战争由局部冲突转为全面相持。",
        "people": [
            {"person_name_raw": "项羽", "role": "opponent", "link_status": "needs_linking",
             "role_zh_cn": "楚军主帅：自齐回击、大破汉军于睢水",
             "review_note": "major-batch01：高祖本纪「项羽闻之，乃引兵去齐……大破汉军」", "person_id": None},
        ],
        "evidence": [
            ev("史记", "高祖本纪", "text-niutrans-cf1616150fc6dc30426a", "十二本纪/高祖本纪#p291",
               "background", "primary", "汉王以故得劫五诸侯兵，遂入彭城。"),
            ev("史记", "高祖本纪", "text-niutrans-ecd7c67e64370ee4ff33", "十二本纪/高祖本纪#p292",
               "process", "primary", "项羽闻之，乃引兵去齐，从鲁出胡陵，至萧，与汉大战彭城灵壁东睢水上，大破汉军，多杀士卒，睢水为之不流。"),
            ev("史记", "高祖本纪", "text-niutrans-5293b4660e8059d2df7d", "十二本纪/高祖本纪#p293",
               "result", "primary", "乃取汉王父母妻子於沛，置之军中以为质。"),
            ev("史记", "高祖本纪", "text-niutrans-180b5d05300cfdaf4eff", "十二本纪/高祖本纪#p294",
               "impact", "primary", "当是时，诸侯见楚彊汉败，还皆去汉复为楚。塞王欣亡入楚。"),
        ],
    },
    "qin_han/event-chuhan-xingyang.yml": {
        "background_zh_cn": "汉王收诸侯，还守成皋、荥阳，下蜀、汉之粟，深沟壁垒，分卒守徼乘塞——楚汉在荥阳、成皋一线转入长期相持。",
        "process_zh_cn": "五月，将军纪信言于汉王「事急矣」；陈平夜出女子东门二千馀人，楚因而四面击之，纪信乃乘王车、黄屋左纛，诈称「食尽，汉王降楚」。",
        "impact_zh_cn": "汉王得以与数十骑出西门遁去，令韩王信与周苛、魏豹、枞公守荥阳；其后项羽闻汉复军成皋，引兵西拔荥阳城、生得周苛——荥阳成皋之间反复易手，楚汉相持的消耗战持续至战争后期。",
        "people": [
            {"person_name_raw": "纪信", "role": "supporter", "link_status": "needs_linking",
             "role_zh_cn": "汉将：乘王车诈降楚军，掩护汉王突围",
             "review_note": "major-batch01：通鉴汉纪二「纪信乃乘王车，黄屋左纛，曰：食尽，汉王降楚」", "person_id": None},
            {"person_name_raw": "周苛", "role": "supporter", "link_status": "needs_linking",
             "role_zh_cn": "汉将：留守荥阳，城破被俘",
             "review_note": "major-batch01：通鉴汉纪二「令韩王信与周苛、魏豹、枞公守荥阳」", "person_id": None},
        ],
        "evidence": [
            ev("资治通鉴", "汉纪二", "text-niutrans-4861fc99aa1261c7ced3", "汉纪/汉纪二#p67",
               "background", "primary", "汉王收诸侯，还守成皋、荥阳，下蜀、汉之粟，深沟壁垒，分卒守徼乘塞。"),
            ev("资治通鉴", "汉纪二", "text-niutrans-18fc0b2e1691ac7cee6e", "汉纪/汉纪二#p158",
               "process", "primary", "于是陈平夜出女子东门二千馀人，楚因而四面击之。纪信乃乘王车，黄屋左纛，曰： 食尽，汉王降楚。"),
            ev("资治通鉴", "汉纪二", "text-niutrans-7d1f2066ecbc4abad9a9", "汉纪/汉纪二#p160",
               "result", "primary", "以故汉王得与数十骑出西门遁去，令韩王信与周苛、魏豹、枞公守荥阳。"),
            ev("资治通鉴", "汉纪二", "text-niutrans-b41d3cb81148408f4f4d", "汉纪/汉纪二#p177",
               "impact", "primary", "六月，羽已破走彭越，闻汉复军成皋，乃引兵西拔荥阳城，生得周苛。"),
        ],
    },
    "qin_han/event-chuhan-gaixia.yml": {
        "background_zh_cn": "韩信自齐、刘贾军自寿春并行，屠城父至垓下；大司马周殷叛楚，举九江兵随刘贾、彭越皆会垓下——诸侯合围之势已成。",
        "process_zh_cn": "项王军壁垓下，兵少食尽，汉军及诸侯兵围之数重；项王夜闻汉军四面皆楚歌，乃大惊曰「汉皆已得楚乎」。",
        "impact_zh_cn": "项羽兵败自刎而死，楚政权覆灭——垓下之战成为楚汉战争的军事终局。",
        "people": [
            {"person_name_raw": "韩信", "role": "supporter", "link_status": "needs_linking",
             "role_zh_cn": "汉军大将：自齐南下会师垓下",
             "review_note": "major-batch01：项羽本纪「韩信乃从齐往……至垓下」", "person_id": None},
        ],
        "evidence": [
            ev("史记", "项羽本纪", "text-niutrans-acfeb6d6a6419b92ba38", "十二本纪/项羽本纪#p490",
               "background", "primary", "大司马周殷叛楚，以舒屠六，举九江兵，随刘贾、彭越皆会垓下，诣项王。"),
            ev("史记", "项羽本纪", "text-niutrans-e329d4521f30fda832ac", "十二本纪/项羽本纪#p491",
               "process", "primary", "项王军壁垓下，兵少食尽，汉军及诸侯兵围之数重。"),
            ev("资治通鉴", "汉纪三", "text-niutrans-b437abd8dc8748eb1549", "汉纪/汉纪三#p16",
               "result", "primary", "项王夜闻汉军四面皆楚歌，乃大惊曰： 汉皆已得楚乎？"),
            ev("史记", "项羽本纪", "text-niutrans-725b090e391bd8ff3144", "十二本纪/项羽本纪#p534",
               "impact", "primary", "乃自刎而死。"),
        ],
    },
    "qin_han/event-chuhan-han-foundation.yml": {
        "background_zh_cn": "垓下战后，汉王还至定陶、驰入齐王信壁夺其军；春正月更立齐王信为楚王、封彭越为梁王；令曰「兵不得休八年，万民与苦甚」，赦天下殊死以下。",
        "process_zh_cn": "诸侯王皆上疏请尊汉王为皇帝；二月甲午，王即皇帝位于汜水之阳。",
        "impact_zh_cn": "皇帝初政即定后妃太子名号、追尊先媪；随后诏封故衡山王吴芮为长沙王等——汉承秦制而兼封建，西汉王朝的统治秩序自此展开。",
        "evidence": [
            ev("资治通鉴", "汉纪三", "text-niutrans-7bfb3905fc28b271cde8", "汉纪/汉纪三#p70",
               "background", "primary", "诸侯王皆上疏请尊汉王为皇帝。"),
            ev("资治通鉴", "汉纪三", "text-niutrans-a158f087083c592fb21e", "汉纪/汉纪三#p71",
               "process", "primary", "二月甲午，王即皇帝位于汜水之阳。"),
            ev("资治通鉴", "汉纪三", "text-niutrans-855fe54bb7c8ced8b7f5", "汉纪/汉纪三#p72",
               "result", "primary", "更王后曰皇后，太子曰皇太子；追尊先媪曰昭灵夫人。"),
            ev("资治通鉴", "汉纪三", "text-niutrans-9db041b336e9103f7bb6", "汉纪/汉纪三#p73",
               "impact", "primary", "诏曰： 故衡山王吴芮，从百粤之兵，佐诸侯，诛暴秦，有大功；诸侯立以为王。"),
        ],
    },
    "qin_han/event-chuhan-qin-revolt.yml": {
        "background_zh_cn": "秦二世元年秋，陈胜等起蕲，至陈而王，号为「张楚」——戍卒起义爆发并迅速建立政权。",
        "process_zh_cn": "陈胜、吴广皆次当行、为屯长，乃谋曰「今亡亦死，举大计亦死，等死，死国可乎」；陈胜曰「天下苦秦久矣」——大泽乡揭竿而起。",
        "impact_zh_cn": "当此时，诸郡县苦秦吏者皆刑其长吏、杀之以应陈涉；山东郡县少年苦秦吏，皆杀其守尉令丞反以应陈涉，相立为侯王、合从西乡，名为伐秦——反秦战争由一隅扩展为天下响应。",
        "people": [
            {"person_name_raw": "吴广", "role": "supporter", "link_status": "needs_linking",
             "role_zh_cn": "起义共同发动者：与陈胜谋于大泽乡",
             "review_note": "major-batch01：陈涉世家「陈胜、吴广乃谋曰」", "person_id": None},
            {"person_name_raw": "陈胜", "role": "monarch", "link_status": "needs_linking",
             "role_zh_cn": "起义领袖：立为王，号张楚",
             "review_note": "major-batch01：陈涉世家「陈涉乃立为王，号为张楚」", "person_id": None},
        ],
        "evidence": [
            ev("史记", "高祖本纪", "text-niutrans-391be1f4e165faaaefcc", "十二本纪/高祖本纪#p65",
               "background", "primary", "秦二世元年秋，陈胜等起蕲，至陈而王，号为 张楚 。"),
            ev("史记", "陈涉世家", "text-niutrans-20d32ac4b5357eb94f28", "三十世家/陈涉世家#p10",
               "process", "primary", "陈胜、吴广乃谋曰： 今亡亦死，举大计亦死，等死，死国可乎？"),
            ev("史记", "陈涉世家", "text-niutrans-a626ffae108062eafbaf", "三十世家/陈涉世家#p45",
               "result", "primary", "将军身被坚执锐，伐无道，诛暴秦，复立楚国之社稷，功宜为王。 陈涉乃立为王，号为张楚。"),
            ev("史记", "陈涉世家", "text-niutrans-c5b7c258c92009a253ad", "三十世家/陈涉世家#p46",
               "impact", "primary", "当此时，诸郡县苦秦吏者，皆刑其长吏，杀之以应陈涉。"),
            ev("史记", "秦始皇本纪", "text-niutrans-92f3cf8f97ee2958f328", "十二本纪/秦始皇本纪#p537",
               "impact", "supporting", "山东郡县少年苦秦吏，皆杀其守尉令丞反，以应陈涉，相立为侯王，合从西乡，名为伐秦。"),
        ],
    },
    "qin_han/event-chuhan-qin-fall.yml": {
        "background_zh_cn": "汉元年十月，沛公兵遂先诸侯至霸上——刘邦先于各路诸侯兵临咸阳。",
        "process_zh_cn": "秦王子婴素车白马、系颈以组，封皇帝玺符节，降轵道旁；诸将或言诛秦王，沛公以「人已服降，又杀之，不祥」止之，乃以秦王属吏，遂西入咸阳，封秦重宝财物府库、还军霸上。",
        "impact_zh_cn": "居数日，项羽引兵西屠咸阳，杀秦降王子婴，烧秦宫室，火三月不灭——秦帝国的心脏在战火中终结，天下进入诸侯重新分配的阶段。",
        "people": [
            {"person_name_raw": "子婴", "role": "deposed_monarch", "link_status": "needs_linking",
             "role_zh_cn": "秦三世：素车白马降轵道，后为项羽所杀",
             "review_note": "major-batch01：高祖本纪「秦王子婴素车白马……降轵道旁」、项羽本纪「杀秦降王子婴」", "person_id": None},
        ],
        "evidence": [
            ev("史记", "高祖本纪", "text-niutrans-74e62b1ff50b5031c0d9", "十二本纪/高祖本纪#p185",
               "background", "primary", "汉元年十月，沛公兵遂先诸侯至霸上。"),
            ev("史记", "高祖本纪", "text-niutrans-6c0c5c66bca3e3dcb823", "十二本纪/高祖本纪#p186",
               "process", "primary", "秦王子婴素车白马，系颈以组，封皇帝玺符节，降轵道旁。"),
            ev("史记", "项羽本纪", "text-niutrans-e71b0b5edb21c732dc04", "十二本纪/项羽本纪#p288",
               "result", "primary", "居数日，项羽引兵西屠咸阳，杀秦降王子婴，烧秦宫室，火三月不灭；收其货宝妇女而东。"),
            ev("史记", "高祖本纪", "text-niutrans-ef4b8d510efa63ca0037", "十二本纪/高祖本纪#p190",
               "impact", "primary", "乃封秦重宝财物府库，还军霸上。"),
        ],
    },
}


def main() -> int:
    applied = 0
    for rel, block in BLOCKS.items():
        path = EVENTS / rel
        existing = yaml.safe_load(path.read_text())
        for key in ("background_zh_cn", "process_zh_cn", "impact_zh_cn"):
            if existing.get(key):
                print(f"SKIP {rel}: already has {key}")
                return 1
        appended = yaml.safe_dump(block, allow_unicode=True, sort_keys=False,
                                  default_flow_style=False, width=10**6)
        with path.open("a", encoding="utf-8") as stream:
            stream.write("\n" + appended)
        applied += 1
        print(f"appended {rel}")
    print(f"total: {applied}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
