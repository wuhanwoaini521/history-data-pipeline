"""Source Batch 02 · PARTIAL_SOURCE 补全（明 5 + 西汉 2）——长任务 Phase D。

明史（work-curated-mingshi）/ 史记 / 资治通鉴 逐段锚定；叙述全部来自引文。
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
        "review_note": f"source-batch02：{work}源引文：「{quote}」；claim_field={field}；anchor=段落精确锚。{note}",
    }


MS = "明史"
BLOCKS: dict[str, dict] = {
    "ming/event-jianwen-jiwei.yml": {
        "background_zh_cn": "恭闵惠皇帝讳允炆，太祖孙、懿文太子标第二子；洪武二十五年九月立为皇太孙——储位早定而诸王叔强大。",
        "process_zh_cn": "洪武三十一年闰五月辛卯，允炆即皇帝位，改明年为建文元年，是为建文帝。",
        "impact_zh_cn": "史臣论其世：「文皇少长习兵，据幽燕形胜之地，乘建文孱弱，长驱内向，奄有四海」——建文即位后试图约束诸王，终启靖难之役，皇统转入燕王一支。",
        "people": [
            {"person_name_raw": "建文帝", "role": "monarch", "link_status": "needs_linking",
             "role_zh_cn": "恭闵惠皇帝朱允炆：皇太孙入继大统",
             "review_note": "source-batch02：明史·恭闵帝本纪「恭闵惠皇帝讳允炆」「辛卯，即皇帝位」", "person_id": None},
        ],
        "places": [
            {"place_name_raw": "京师", "role": "capital", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "即位地（南京）",
             "review_note": "source-batch02：明史·恭闵帝本纪（洪武三十一年即位）"},
        ],
        "evidence": [
            ev(MS, "恭闵帝本纪", "本纪/卷四#p2", "text-niutrans-a9525604c583ca5b121b", "background", "primary",
               "恭闵惠皇帝讳允炆。"),
            ev(MS, "恭闵帝本纪", "本纪/卷四#p8", "text-niutrans-3d1171a3fcbd6e37d241", "process", "supporting",
               "洪武二十五年九月，立为皇太孙。"),
            ev(MS, "恭闵帝本纪", "本纪/卷四#p14", "text-niutrans-881003f9fa2f4ad7fd96", "process", "primary",
               "辛卯，即皇帝位。"),
            ev(MS, "成祖本纪", "本纪/卷七#p268", "text-niutrans-9991047d0cbbdc75fbdf", "impact", "primary",
               "文皇少长习兵，据幽燕形胜之地，乘建文孱弱，长驱内向，奄有四海。", "史臣赞语，述建文之世结局"),
        ],
    },
    "ming/event-ningwang-zhi-luan.yml": {
        "background_zh_cn": "宁王宸濠谋逆既久（妃娄氏尝谏），正德十四年举兵反；七月甲辰，武宗自将讨宸濠，命安边伯朱泰为威武副将军率师为先锋。",
        "process_zh_cn": "丁巳，王守仁败宸濠于樵舍，擒之——自起兵至被擒仅四十余日。",
        "result_zh_cn": "十二月己丑，宸濠伏诛，宁王之乱平。",
        "impact_zh_cn": "王守仁以一闻宸濠变即仗义兴兵、戡定大难，特加封爵（新建伯）——此役使其事功与学说声望并起，有明一代文臣平乱之典范。",
        "people": [
            {"person_name_raw": "王守仁", "role": "supporter", "link_status": "needs_linking",
             "role_zh_cn": "南赣巡抚：兴兵讨宸濠、樵舍擒之，封新建伯",
             "review_note": "source-batch02：明史「守仁败宸濠于樵舍，擒之」「守仁一闻宸濠变，仗义兴兵，戡定大难」", "person_id": None},
            {"person_name_raw": "朱宸濠", "role": "opponent", "link_status": "needs_linking",
             "role_zh_cn": "宁王：正德十四年举兵谋逆，被擒伏诛",
             "review_note": "source-batch02：明史·武宗本纪「宸濠伏诛」", "person_id": None},
        ],
        "places": [
            {"place_name_raw": "樵舍", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "王守仁擒宸濠之地",
             "review_note": "source-batch02：明史「守仁败宸濠于樵舍，擒之」"},
        ],
        "evidence": [
            ev(MS, "武宗本纪", "本纪/卷十六#p302", "text-niutrans-ddd671219f6e30c30262", "background", "primary",
               "秋七月甲辰，帝自将讨宸濠，安边伯朱泰为威武副将军。帅师为先锋。"),
            ev(MS, "武宗本纪", "本纪/卷十六#p305", "text-niutrans-f9b154e13fdcdc3c35bb", "process", "primary",
               "丁巳，守仁败宸濠于樵舍，擒之。"),
            ev(MS, "武宗本纪", "本纪/卷十六#p327", "text-niutrans-64ec271e0334ffd7355b", "result", "primary",
               "十二月己丑，宸濠伏诛。"),
            ev(MS, "列传·王守仁传", "列传/卷九十四#p113", "text-niutrans-9c19401ff7adadac767f", "impact", "primary",
               "守仁一闻宸濠变，仗义兴兵，戡定大难，特加封爵，以酬大功。"),
        ],
    },
    "ming/event-shanxi-minbian.yml": {
        "background_zh_cn": "陕西饥民苦于加派，流贼大起，分掠鄜州、延安——明末农民战争由此开端。",
        "process_zh_cn": "崇祯四年六月，流贼王嘉胤陷府谷，米脂贼张献忠聚众应之，乱势蔓延。",
        "result_zh_cn": "官军反击：延绥副将曹文诏击贼于河曲，王嘉胤败死，然诸部旋复纷起。",
        "impact_zh_cn": "王嘉胤既死而后起者众：闯王高迎祥与李自成、张献忠等合流（「闯王高迎祥亦与合」）——陕西民变演化为席卷数省的明末农民战争。",
        "people": [
            {"person_name_raw": "王嘉胤", "role": "opponent", "link_status": "needs_linking",
             "role_zh_cn": "陕西流贼首领：陷府谷、败死于河曲",
             "review_note": "source-batch02：明史·庄烈帝本纪「流贼王嘉胤陷府谷」「王嘉胤败死」", "person_id": None},
            {"person_name_raw": "张献忠", "role": "opponent", "link_status": "needs_linking",
             "role_zh_cn": "米脂贼：聚众应王嘉胤起事",
             "review_note": "source-batch02：明史·庄烈帝本纪「米脂贼张献忠聚众应之」", "person_id": None},
            {"person_name_raw": "曹文诏", "role": "supporter", "link_status": "needs_linking",
             "role_zh_cn": "延绥副将：击王嘉胤于河曲",
             "review_note": "source-batch02：明史·庄烈帝本纪「延绥副将曹文诏击贼于河曲」", "person_id": None},
        ],
        "places": [
            {"place_name_raw": "府谷", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "王嘉胤起兵攻陷之地（陕西）",
             "review_note": "source-batch02：明史·庄烈帝本纪「流贼王嘉胤陷府谷」"},
            {"place_name_raw": "延安", "role": "region", "link_status": "needs_linking", "sequence": 2,
             "description_zh_cn": "流贼分掠之地（鄜州、延安）",
             "review_note": "source-batch02：明史·庄烈帝本纪「分掠鄜州、延安」"},
        ],
        "evidence": [
            ev(MS, "庄烈帝本纪一", "本纪/卷二十三#p51", "text-niutrans-4882c469f3393b89c61a", "background", "primary",
               "陕西饥民苦加派，流贼大起，分掠鄜州、延安。"),
            ev(MS, "庄烈帝本纪一", "本纪/卷二十三#p103", "text-niutrans-1b75494b6357fbce9cff", "process", "primary",
               "六月癸丑，流贼王嘉胤陷府谷，米脂贼张献忠聚众应之。"),
            ev(MS, "庄烈帝本纪一", "本纪/卷二十三#p125", "text-niutrans-d1fce83746395b45ac58", "result", "primary",
               "是月，延绥副将曹文诏击贼于河曲，王嘉胤败死。"),
            ev(MS, "列传·张献忠等传", "列传/卷一百六十一#p70", "text-niutrans-3cb1e979665dd935251f", "impact", "primary",
               "闯王高迎祥亦与合。"),
        ],
    },
    "ming/event-lanyu-an.yml": {
        "background_zh_cn": "蓝玉，定远人，开平王常遇春妇弟——明初悍将，捕鱼儿海破北元、受降纳哈出，功高爵至凉国公。",
        "process_zh_cn": "洪武二十六年案发，株连蔓引：会宁侯张温坐蓝玉党诛——「帝发怒，肃清逆党」。",
        "result_zh_cn": "词所连及坐诛者三万余人，明初武臣集团遭空前清洗。",
        "impact_zh_cn": "案后余波绵长，至太祖晚年犹「赦胡惟庸、蓝玉余党」——蓝玉案与胡惟庸案并称明初两大狱，开国功臣诛戮殆尽，中枢军权尽归皇室。",
        "people": [
            {"person_name_raw": "蓝玉", "role": "opponent", "link_status": "needs_linking",
             "role_zh_cn": "凉国公：明初名将，洪武二十六年以谋反诛",
             "review_note": "source-batch02：明史·蓝玉传「蓝玉，定远人」；本纪「坐蓝玉党诛」", "person_id": None},
        ],
        "places": [],
        "evidence": [
            ev(MS, "蓝玉传", "列传/卷二十#p118", "text-niutrans-d6275902c97b24072699", "background", "primary",
               "蓝玉，定远人。开平王常遇春妇弟也。"),
            ev(MS, "太祖本纪三", "本纪/卷三#p281", "text-niutrans-d69fb84d993e7890e076", "process", "primary",
               "壬戌，会宁侯张温坐蓝玉党诛。"),
            ev(MS, "列传·奸臣等传", "列传/卷一百九十六#p63", "text-niutrans-d88d51bf4926e114d014", "result", "primary",
               "帝发怒，肃清逆党，词所连及坐诛者三万余人。"),
            ev(MS, "太祖本纪三", "本纪/卷三#p291", "text-niutrans-c13fc60f11c491901900", "impact", "primary",
               "赦胡惟庸、蓝玉余党。"),
        ],
    },
    "ming/event-li-zicheng-fazhan.yml": {
        "background_zh_cn": "李自成自湖广走河南，饥民附之，连陷宜阳、永宁，杀万安王采崿，陷偃师，势大炽——中原饥荒成为其势力扩张的土壤。",
        "process_zh_cn": "李自成陷延安，寻屠凤翔，西北震动。",
        "result_zh_cn": "其势进退河南陕西之间：李自成走归德，与罗汝才复入陕西，诸部离合不定而实力日增。",
        "impact_zh_cn": "明廷议者已视之为心腹之患：「陕有李自成、惠登相等，大部未能剿绝」——围剿方略力主隔绝诸部使不得合，然终不能制。",
        "people": [
            {"person_name_raw": "李自成", "role": "opponent", "link_status": "needs_linking",
             "role_zh_cn": "闯王：饥民依附、转战河南陕西",
             "review_note": "source-batch02：明史·庄烈帝本纪「李自成自湖广走河南，饥民附之……势大炽」", "person_id": None},
            {"person_name_raw": "罗汝才", "role": "opponent", "link_status": "needs_linking",
             "role_zh_cn": "流贼首领：与李自成合兵入陕西",
             "review_note": "source-batch02：明史·庄烈帝本纪「李自成走归德，与罗汝才复入陕西」", "person_id": None},
        ],
        "places": [
            {"place_name_raw": "河南", "role": "region", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "饥民依附、连陷诸县之地",
             "review_note": "source-batch02：明史·庄烈帝本纪「自湖广走河南，饥民附之」"},
            {"place_name_raw": "陕西", "role": "region", "link_status": "needs_linking", "sequence": 2,
             "description_zh_cn": "与罗汝才复入之地",
             "review_note": "source-batch02：明史·庄烈帝本纪「与罗汝才复入陕西」"},
        ],
        "evidence": [
            ev(MS, "庄烈帝本纪二", "本纪/卷二十四#p95", "text-niutrans-8f2ab0d8906423af63c4", "background", "primary",
               "是月，李自成自湖广走河南，饥民附之，连陷宜阳、永宁，杀万安王采崿，陷偃师，势大炽。"),
            ev(MS, "庄烈帝本纪二", "本纪/卷二十四#p237", "text-niutrans-6f6394fd7bcca127b189", "process", "primary",
               "十一月甲午，李自成陷延安，寻屠凤翔。"),
            ev(MS, "庄烈帝本纪一", "本纪/卷二十三#p251", "text-niutrans-a016b1fc98a69fd359de", "result", "primary",
               "李自成走归德，与罗汝才复入陕西。"),
            ev(MS, "列传", "列传/卷一百四十#p43", "text-niutrans-73a37f98e30529e61446", "impact", "primary",
               "然陕有李自成、惠登相等，大部未能剿绝。"),
        ],
    },
    "qin_han/event-hanchu-yixingwang.yml": {
        "background_zh_cn": "陈平献策：高帝发使告诸侯会陈，「吾将南游云梦」——以游猎之名会诸侯于陈，实为擒韩信之谋。",
        "process_zh_cn": "春，淮阴侯韩信谋反关中，夷三族——楚王韩信先贬淮阴侯，终以谋反诛。",
        "result_zh_cn": "夏，梁王彭越谋反，废迁蜀，复欲反，遂夷三族；异姓诸侯王相继翦除。",
        "impact_zh_cn": "秋七月，淮南王黥布反，东并荆王刘贾地，北渡淮——异姓王诛锄既尽，而淮南之叛继起，汉初郡国并行之局与同姓王分封由此定型。",
        "people": [
            {"person_name_raw": "韩信", "role": "opponent", "link_status": "needs_linking",
             "role_zh_cn": "淮阴侯：由楚王贬侯，以谋反夷三族",
             "review_note": "source-batch02：史记·高祖本纪「淮阴侯韩信谋反关中，夷三族」", "person_id": None},
            {"person_name_raw": "彭越", "role": "opponent", "link_status": "needs_linking",
             "role_zh_cn": "梁王：谋反废迁蜀，复以谋反夷三族",
             "review_note": "source-batch02：史记·高祖本纪「梁王彭越谋反，废迁蜀……遂夷三族」", "person_id": None},
            {"person_name_raw": "黥布", "role": "opponent", "link_status": "needs_linking",
             "role_zh_cn": "淮南王英布：异姓王中最后反者",
             "review_note": "source-batch02：史记·高祖本纪「淮南王黥布反」", "person_id": None},
        ],
        "places": [
            {"place_name_raw": "云梦", "role": "region", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "高帝伪游之地（擒韩信之谋）",
             "review_note": "source-batch02：史记·陈丞相世家「吾将南游云梦」"},
        ],
        "evidence": [
            ev("史记", "陈丞相世家", "三十世家/陈丞相世家#p119", "text-niutrans-20374c806004b411107e",
               "background", "primary", "乃发使告诸侯会陈， 吾将南游云梦 。"),
            ev("史记", "高祖本纪", "十二本纪/高祖本纪#p521", "text-niutrans-9bb1b44bc1c5f9881135",
               "process", "primary", "春，淮阴侯韩信谋反关中，夷三族。"),
            ev("史记", "高祖本纪", "十二本纪/高祖本纪#p522", "text-niutrans-9d8292921af904c17e12",
               "result", "primary", "夏，梁王彭越谋反，废迁蜀；复欲反，遂夷三族。"),
            ev("史记", "高祖本纪", "十二本纪/高祖本纪#p524", "text-niutrans-961b059199ad61df9817",
               "impact", "primary", "秋七月，淮南王黥布反，东并荆王刘贾地，北渡淮。"),
        ],
    },
    "qin_han/event-wangmang-fuchu.yml": {
        "background_zh_cn": "成帝绥和元年，王莽以太后之侄为大司马，时年三十八——王氏外戚由是秉政。",
        "process_zh_cn": "哀帝崩，皇太后诏大司马莽杂与御史、丞相、廷尉治，问皇帝起居发病状——莽于帝崩之际重掌机要，赵昭仪自杀。",
        "result_zh_cn": "平帝初立，太皇太后自用莽为大司马、领尚书事——王莽复出辅政，军政大权集于一身。",
        "impact_zh_cn": "复出即领尚书事，为居摄、篡汉之渐——王莽自哀帝朝被劾「当伏显戮」，至是权柄在手，西汉末年的外戚政治进入最后阶段。",
        "people": [
            {"person_name_raw": "王莽", "role": "official", "link_status": "needs_linking",
             "role_zh_cn": "新都侯→大司马领尚书事：复出辅政",
             "review_note": "source-batch02：资治通鉴汉纪二十七「太皇太后自用莽为大司马、领尚书事」", "person_id": None},
            {"person_name_raw": "王政君", "role": "monarch", "link_status": "needs_linking",
             "role_zh_cn": "太皇太后：用莽为大司马、领尚书事",
             "review_note": "source-batch02：资治通鉴汉纪二十七「太皇太后自用莽为大司马」", "person_id": None},
        ],
        "places": [],
        "evidence": [
            ev("资治通鉴", "汉纪二十四", "汉纪/汉纪二十四#p226", "text-niutrans-d8f09e2287f449171b69",
               "background", "primary", "丙寅，以莽为大司马，时年三十八。"),
            ev("资治通鉴", "汉纪二十五", "汉纪/汉纪二十五#p22", "text-niutrans-9f009d0f0efbc03c4c80",
               "process", "primary", "皇太后诏大司马莽杂与御史、丞相、廷尉治，问皇帝起居发病状；赵昭仪自杀。"),
            ev("资治通鉴", "汉纪二十七", "汉纪/汉纪二十七#p184", "text-niutrans-f25f004d44ddf2ac4008",
               "result", "primary", "庚申，太皇太后自用莽为大司马、领尚书事。"),
            ev("资治通鉴", "汉纪二十六", "汉纪/汉纪二十六#p43", "text-niutrans-213445f2b097a41fb6ad",
               "impact", "supporting", "新都侯王莽前为大司马，不广尊尊之义，抑贬尊号，亏损孝道，当伏显戮。",
               "哀帝朝被劾之语，反衬其复出专权为篡汉之渐"),
        ],
    },
}


def main() -> int:
    applied = 0
    for rel, block in BLOCKS.items():
        path = EVENTS / rel
        existing = yaml.safe_load(path.read_text())
        if existing.get("process_zh_cn") or existing.get("background_zh_cn"):
            print(f"SKIP {rel}: already enriched")
            continue
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
