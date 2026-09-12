"""Ready-43 · Cluster 1：先秦秦汉 12 事件富化（补 place/process/impact 等缺失维度）。

规则同前：叙述全部可回溯引文；已有 reviewed 字段保留并补锚；append-only + 重复键后处理。
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
        "review_note": f"ready43-c1：{work}源引文：「{quote}」；claim_field={field}；anchor=段落精确锚。{note}",
    }


BLOCKS: dict[str, dict] = {
    "chunqiu_zhanguo/event-changping-zhizhan.yml": {
        "process_zh_cn": "赵王怒廉颇军多失亡、又坚壁不敢战，闻秦反间之言，使赵括代廉颇将以击秦；秦闻马服子将，阴使武安君白起为上将军。赵括至军悉更约束、易置军吏，出兵击秦师，乘胜追造秦壁，壁坚拒不得入；秦奇兵二万五千人绝赵军之后，又五千骑绝赵壁间，赵军分而为二、粮道绝。",
        "impact_zh_cn": "长平战后赵壮者尽没：「赵壮者尽于长平，其孤未壮」；白起自谓「长平之战，赵卒降者数十万人，我诈而尽阬之，是足以死」——赵自此一蹶不振，秦并天下之势遂成。",
        "places": [
            {"place_name_raw": "长平", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "秦赵决战之地（上党长平）",
             "review_note": "ready43-c1：史记·廉颇蔺相如列传「秦与赵兵相距长平」+ 通鉴周纪五「赵括乘胜追造秦壁」"},
        ],
        "evidence": [
            ev("史记", "廉颇蔺相如列传", "七十列传/廉颇蔺相如列传#p133", "text-niutrans-a4e9ea061e2005ffe430",
               "background", "primary", "七年，秦与赵兵相距长平……赵军固壁不战。"),
            ev("史记", "白起王翦列传", "七十列传/白起王翦列传#p45", "text-niutrans-a046934aa5355f5dec80",
               "process", "primary", "因使赵括代廉颇将以击秦。秦闻马服子将，乃阴使武安君白起为上将军。"),
            ev("资治通鉴", "周纪五", "周纪/周纪五#p226", "text-niutrans-c6ffa4a4559c8e591773",
               "process", "supporting", "奇兵二万五千人绝赵军之后，又五千骑绝赵壁间。赵军分而为二，粮道绝。"),
            ev("史记", "白起王翦列传", "七十列传/白起王翦列传#p103", "text-niutrans-8424002c93a78573eb97",
               "impact", "primary", "长平之战，赵卒降者数十万人，我诈而尽阬之，是足以死。"),
            ev("史记", "廉颇蔺相如列传", "七十列传/廉颇蔺相如列传#p161", "text-niutrans-cb9d13e0b9c3bf9285af",
               "impact", "supporting", "赵壮者尽於长平，其孤未壮。"),
        ],
    },
    "chunqiu_zhanguo/event-qin-mie-liuguo.yml": {
        "process_zh_cn": "秦王政之世次第灭六国：十七年韩王纳地效玺请为藩臣，已而倍约，秦兴兵诛之、虏其王；十九年王翦、羌瘣尽定取赵地东阳，得赵王；其后灭魏、灭楚，二十五年虏燕王；二十六年齐王用后胜计绝秦使，兵吏诛之、虏其王，平齐地。",
        "impact_zh_cn": "六王毕而四海一：秦初并天下，令丞相、御史议帝号，分天下以为三十六郡，郡置守、尉、监——封建诸侯之局终结，郡县帝国自此建立。",
        "places": [
            {"place_name_raw": "邯郸", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "赵都，王翦尽定赵地、得赵王",
             "review_note": "ready43-c1：史记·秦始皇本纪「王翦、羌瘣尽定取赵地东阳，得赵王」"},
        ],
        "evidence": [
            ev("史记", "秦始皇本纪", "十二本纪/秦始皇本纪#p132", "text-niutrans-756aad0533841b929247",
               "process", "primary", "异日韩王纳地效玺，请为籓臣，已而倍约，与赵、魏合从畔秦，故兴兵诛之，虏其王。"),
            ev("史记", "秦始皇本纪", "十二本纪/秦始皇本纪#p104", "text-niutrans-d8677ddbe52e2f16f42c",
               "process", "supporting", "十九年，王翦、羌瘣尽定取赵地东阳，得赵王。"),
            ev("史记", "秦始皇本纪", "十二本纪/秦始皇本纪#p139", "text-niutrans-ff06b0dbc4f3c9eac183",
               "result", "primary", "齐王用后胜计，绝秦使，欲为乱，兵吏诛，虏其王，平齐地。"),
            ev("史记", "秦始皇本纪", "十二本纪/秦始皇本纪#p172", "text-niutrans-fe665881879c068407e2",
               "impact", "primary", "分天下以为三十六郡，郡置守、尉、监。"),
        ],
    },
    "chunqiu_zhanguo/event-qin-tongyi.yml": {
        "process_zh_cn": "秦初并天下，令丞相、御史曰「异日韩王纳地效玺……故兴兵诛之，虏其王」——以武功告成议帝号；分天下以为三十六郡，郡置守、尉、监。",
        "impact_zh_cn": "统一制度次第颁行：一法度衡石丈尺、书同文字、车同轨——「百代都行秦政法」，中国第一次以中央集权帝国形态完成整合。",
        "places": [
            {"place_name_raw": "咸阳", "role": "capital", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "秦都，议帝号、颁统一制度之地",
             "review_note": "ready43-c1：史记·秦始皇本纪（初并天下、分三十六郡）"},
        ],
        "evidence": [
            ev("史记", "秦始皇本纪", "十二本纪/秦始皇本纪#p132", "text-niutrans-756aad0533841b929247",
               "process", "primary", "秦初并天下，令丞相、御史曰……虏其王。"),
            ev("史记", "秦始皇本纪", "十二本纪/秦始皇本纪#p172", "text-niutrans-fe665881879c068407e2",
               "result", "primary", "分天下以为三十六郡，郡置守、尉、监。"),
            ev("史记", "秦始皇本纪", "十二本纪/秦始皇本纪#p176", "text-niutrans-215d0ddac58fddb0aad0",
               "impact", "primary", "一法度衡石丈尺。"),
            ev("史记", "秦始皇本纪", "十二本纪/秦始皇本纪#p178", "text-niutrans-b7610d62e29cf31d5654",
               "impact", "supporting", "书同文字。"),
        ],
    },
    "chunqiu_zhanguo/event-sanjia-fenjin.yml": {
        "process_zh_cn": "先是赵襄子、韩康子、魏桓子共杀知伯、尽并其地，三家分智氏之田（赵襄子漆智伯之头以为饮器）；至周威烈王二十三年，初命晋大夫魏斯、赵籍、韩虔为诸侯——三家由晋臣受命而立国。",
        "impact_zh_cn": "温公论之曰：「君臣之礼既坏矣，则天下以智力相雄长，遂使圣贤之后为诸侯者，社稷无不泯绝」——三家分晋被视为战国之始，礼崩乐坏、兼并大幕由此拉开。",
        "places": [
            {"place_name_raw": "晋阳", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "三家围灌智伯之地（城不浸者三版）",
             "review_note": "ready43-c1：资治通鉴周纪一「三家以国人围而灌之，城不浸者三版」"},
        ],
        "evidence": [
            ev("史记", "晋世家", "三十世家/晋世家#p859", "text-niutrans-5f6e29eacf97f5284c01",
               "background", "primary", "哀公四年，赵襄子、韩康子、魏桓子共杀知伯，尽并其地。"),
            ev("资治通鉴", "周纪一", "周纪/周纪一#p134", "text-niutrans-4a70b5677c80a0004093",
               "process", "primary", "三家分智氏之田。赵襄子漆智伯之头，以为饮器。"),
            ev("资治通鉴", "周纪一", "周纪/周纪一#p3", "text-niutrans-384a8a08a35c8bae3966",
               "result", "primary", "二十三年初命晋大夫魏斯、赵籍、韩虔为诸侯。"),
            ev("资治通鉴", "周纪一", "周纪/周纪一#p52", "text-niutrans-d4309c5ca0c788ed6787",
               "impact", "primary", "君臣之礼既坏矣，则天下以智力相雄长，遂使圣贤之后为诸侯者，社稷无不泯绝。"),
        ],
    },
    "pre_qin/event-shangtang-miexia.yml": {
        "process_zh_cn": "伊尹相汤伐桀，升自陑，遂与桀战于鸣条之野；汤誓众曰「格尔众庶，悉听朕言，非台小子，敢行称乱」「夏氏有罪，予畏上帝，不敢不正」——以天命为号讨夏。",
        "impact_zh_cn": "汤既胜夏，诸侯闻之曰「汤德至矣，及禽兽」——商以德义之名声代夏而立，汤誓成为后世「吊民伐罪」的文告典范。",
        "places": [
            {"place_name_raw": "鸣条", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "汤桀决战之野",
             "review_note": "ready43-c1：尚书·汤誓「遂与桀战于鸣条之野」"},
        ],
        "evidence": [
            ev("尚书", "汤誓", "商书/汤誓#p1", "text-niutrans-c7cea9d9c100baa496c0",
               "background", "primary", "伊尹相汤伐桀，升自陑，遂与桀战于鸣条之野，作《汤誓》。"),
            ev("尚书", "汤誓", "商书/汤誓#p2", "text-niutrans-4640fcfe53639be9354f",
               "process", "primary", "王曰： 格尔众庶，悉听朕言，非台小子，敢行称乱！"),
            ev("尚书", "汤誓", "商书/汤誓#p5", "text-niutrans-a414343d516b2b416034",
               "result", "primary", "夏氏有罪，予畏上帝，不敢不正。"),
            ev("史记", "殷本纪", "十二本纪/殷本纪#p38", "text-niutrans-cf2fabf7e73738b9e0f2",
               "impact", "primary", "诸侯闻之，曰： 汤德至矣，及禽兽。"),
        ],
    },
    "pre_qin/event-wuwang-fazhou.yml": {
        "process_zh_cn": "武王戎车三百两、虎贲三百人，与商战于牧野；甲子昧爽，王朝至于商郊牧野乃誓，称尔戈、比尔干、立尔矛；师尚父与百夫致师，以大卒驰帝纣师。",
        "impact_zh_cn": "纣师皆倒兵以战、以开武王——商军倒戈，商亡周兴；牧誓所载「友邦冢君、庸蜀羌髳微卢彭濮」之联军阵容，成为周初封建秩序的原点。",
        "places": [
            {"place_name_raw": "牧野", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "商郊决战之地",
             "review_note": "ready43-c1：尚书·牧誓「王朝至于商郊牧野，乃誓」"},
        ],
        "evidence": [
            ev("尚书", "牧誓", "周书/牧誓#p1", "text-niutrans-523e45ce0b7dab4635d1",
               "background", "primary", "武王戎车三百两，虎贲三百人，与商战于牧野，作《牧誓》。"),
            ev("尚书", "牧誓", "周书/牧誓#p2", "text-niutrans-8b7cea30d15ca3e3c53d",
               "process", "primary", "时甲子昧爽，王朝至于商郊牧野，乃誓。"),
            ev("史记", "周本纪", "十二本纪/周本纪#p122", "text-niutrans-c93793417aee529c3e06",
               "result", "primary", "武王使师尚父与百夫致师，以大卒驰帝纣师。"),
            ev("史记", "周本纪", "十二本纪/周本纪#p124", "text-niutrans-a9dd2be4622ef56ef585",
               "impact", "primary", "纣师皆倒兵以战，以开武王。"),
        ],
    },
    "qin_han/event-mobei-zhizhan.yml": {
        "process_zh_cn": "大将军卫青将四将军出定襄，将军霍去病出代，各将五万骑；青出塞斩首万余，去病与左贤王战、斩获首虏七万余级。",
        "impact_zh_cn": "封狼居胥山、禅于姑衍、登临翰海——漠北决战重创匈奴主力，「漠南无王庭」，汉匈攻守之势自此逆转。",
        "places": [
            {"place_name_raw": "狼居胥山", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "霍去病封禅之地（漠北）",
             "review_note": "ready43-c1：史记·卫将军骠骑列传「封狼居胥山，禅於姑衍，登临翰海」"},
        ],
        "evidence": [
            ev("汉书", "武帝纪", "纪/武帝纪#p199", "text-niutrans-02b4dc0abd7aac41d20e",
               "process", "primary", "大将军卫青将四将军出定襄，将军去病出代，各将五万骑。"),
            ev("汉书", "武帝纪", "纪/武帝纪#p202", "text-niutrans-ecedd38b5b9bc7c1f285",
               "result", "primary", "去病与左贤王战，斩获首虏七万余级，封狼居胥山乃还。"),
            ev("史记", "卫将军骠骑列传", "七十列传/卫将军骠骑列传#p151", "text-niutrans-6bf3bce4c2a2607c37ac",
               "impact", "primary", "封狼居胥山，禅於姑衍，登临翰海。"),
            ev("汉书", "匈奴传下", "传/匈奴传下#p221", "text-niutrans-c42581b78ad65a31ccc0",
               "impact", "supporting", "追奔逐北，封狼居胥山，禅于姑衍，以临翰海，虏名王贵人以百数。"),
        ],
    },
    "qin_han/event-qiguo-zhi-luan.yml": {
        "process_zh_cn": "及削吴会稽、豫章郡书至，吴王先起兵，诛汉吏二千石以下；其将周丘一夜得三万人，遂将其兵北略城邑。",
        "impact_zh_cn": "景帝斩御史大夫晁错以谢七国而不止兵；诸将破七国、斩首十余万级——乱平，吴王败走、诸侯王坐大之患稍息，汉廷集权得以推进。",
        "places": [
            {"place_name_raw": "下邳", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "吴王败后其将引兵归守之地",
             "review_note": "ready43-c1：汉书·荆燕吴传「闻吴王败走……即引兵归下邳」"},
        ],
        "evidence": [
            ev("汉书", "荆燕吴传", "传/荆燕吴传#p123", "text-niutrans-b7e296e813bbd91555b1",
               "process", "primary", "及削吴会稽、豫章郡书至，则吴王先起兵，诛汉吏二千石以下。"),
            ev("汉书", "荆燕吴传", "传/荆燕吴传#p197", "text-niutrans-668dccaa229d7c7849fb",
               "process", "supporting", "周丘一夜得三万人，使人报吴王，遂将其兵北略城邑。"),
            ev("汉书", "景帝纪", "纪/景帝纪#p50", "text-niutrans-b90e763dd3ec19b015ff",
               "result", "primary", "斩御史大夫晁错以谢七国。"),
            ev("汉书", "景帝纪", "纪/景帝纪#p52", "text-niutrans-45fd7e89044f3b556dcf",
               "impact", "primary", "诸将破七国，斩首十余万级。"),
        ],
    },
    "qin_han/event-wangmang-chengdi.yml": {
        "process_zh_cn": "其令安汉公居摄践祚，如周公故事，以武功县为安汉公采地；莽惶惧不能食，昼夜抱孺子告祷郊庙，放《大诰》作策，谕以摄位当反政孺子之意。",
        "result_anchor_note": "result 保留既有 legacy 文本，补锚",
        "impact_zh_cn": "「疏远欲进者并作符命，莽遂据以即真」；既即真，尤备大臣、抑夺下权——王莽由摄政至真皇帝，西汉以「禅让」形式易姓，开后世权臣代汉之先例。",
        "places": [
            {"place_name_raw": "长安", "role": "capital", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "居摄、即真与改制之地",
             "review_note": "ready43-c1：汉书·王莽传（居摄践祚、即真）"},
        ],
        "evidence": [
            ev("汉书", "王莽传上", "传/王莽传上#p454", "text-niutrans-8512c108bca3743f09f1",
               "process", "primary", "其令安汉公居摄践祚，如周公故事，以武功县为安汉公采地，名曰汉光邑。"),
            ev("汉书", "王莽传上", "传/王莽传上#p540", "text-niutrans-2c1c079822eb520a54f3",
               "process", "supporting", "莽惶惧不能食，昼夜抱孺子告祷郊庙，放《大诰》作策。"),
            ev("资治通鉴", "汉纪二十九", "汉纪/汉纪二十九#p10", "text-niutrans-07ff19c92b23a4926309",
               "result", "primary", "中傅将孺子下殿，北面而称臣。"),
            ev("资治通鉴", "汉纪二十九", "汉纪/汉纪二十九#p191", "text-niutrans-db18ce9a4dc88667d733",
               "impact", "primary", "而疏远欲进者并作符命，莽遂据以即真。"),
            ev("资治通鉴", "汉纪二十九", "汉纪/汉纪二十九#p352", "text-niutrans-88d4c7e38a1b36f48454",
               "impact", "supporting", "莽即真，尤备大臣，抑夺下权。"),
        ],
    },
    "qin_han/event-guangwu-chengdi.yml": {
        "process_zh_cn": "更始遣侍御史持节立光武为萧王；行至鄗，同舍生彊华自关中奉《赤伏符》曰「刘秀发兵捕不道，四夷云集龙斗野，四七之际火为主」——六月己未，即皇帝位。",
        "impact_zh_cn": "冬十月癸丑，车驾入洛阳，幸南宫却非殿，遂定都焉——东汉肇建，汉祚中兴。",
        "people": [
            {"person_name_raw": "刘秀", "role": "monarch", "link_status": "needs_linking",
             "role_zh_cn": "汉光武帝：由萧王即帝位，东汉开国",
             "review_note": "ready43-c1：后汉书·光武帝纪「六月己未，即皇帝位」", "person_id": None},
            {"person_name_raw": "彊华", "role": "supporter", "link_status": "needs_linking",
             "role_zh_cn": "奉《赤伏符》劝进者",
             "review_note": "ready43-c1：后汉书·光武帝纪「同舍生彊华自关中奉《赤伏符》」", "person_id": None},
        ],
        "places": [
            {"place_name_raw": "鄗", "role": "city", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "光武即皇帝位之地",
             "review_note": "ready43-c1：后汉书·光武帝纪「行至鄗……即皇帝位」"},
            {"place_name_raw": "洛阳", "role": "capital", "link_status": "needs_linking", "sequence": 2,
             "description_zh_cn": "东汉定都之地",
             "review_note": "ready43-c1：后汉书·光武帝纪「车驾入洛阳……遂定都焉」"},
        ],
        "evidence": [
            ev("后汉书", "光武帝纪上", "本纪/光武帝纪上#p110", "text-niutrans-68f1ea55cfa357183423",
               "background", "primary", "更始遣侍御史持节立光武为萧王，悉令罢兵诣行在所。"),
            ev("后汉书", "光武帝纪上", "本纪/光武帝纪上#p158", "text-niutrans-337d7f939456ec06867d",
               "process", "primary", "行至鄗……奉《赤伏符》。"),
            ev("后汉书", "光武帝纪上", "本纪/光武帝纪上#p161", "text-niutrans-7dae2d98aac3bd933078",
               "result", "primary", "六月己未，即皇帝位。"),
            ev("后汉书", "光武帝纪上", "本纪/光武帝纪上#p186", "text-niutrans-83272c2e2cfd2e33f697",
               "impact", "primary", "冬十月癸丑，车驾入洛阳，幸南宫却非殿，遂定都焉。"),
        ],
    },
    "qin_han/event-xin-mie.yml": {
        "process_zh_cn": "昆阳之战：世祖悉发郾、定陵兵数千人来救昆阳，莽将寻、邑易之，自将万余人行陈、敕诸营按部毋得动；昆阳中兵出并战，邑走、军乱——新莽主力崩溃。",
        "impact_zh_cn": "莽就车之渐台、欲阻池水；商人杜吴杀莽，校尉公宾就斩莽首；传莽首诣宛，县于市，百姓共提击之、或切食其舌——新莽覆灭，天下复归汉室。",
        "people": [
            {"person_name_raw": "王莽", "role": "opponent", "link_status": "needs_linking",
             "role_zh_cn": "新朝皇帝：昆阳败后于渐台被杀",
             "review_note": "ready43-c1：通鉴汉纪三十一「商人杜吴杀莽」", "person_id": None},
            {"person_name_raw": "王邑", "role": "opponent", "link_status": "needs_linking",
             "role_zh_cn": "莽将：昆阳败走，后守渐台",
             "review_note": "ready43-c1：汉书·王莽传下「昆阳中兵出并战，邑走，军乱」", "person_id": None},
        ],
        "places": [
            {"place_name_raw": "昆阳", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "新汉决战之地",
             "review_note": "ready43-c1：汉书·王莽传下「昆阳中兵出并战，邑走，军乱」"},
            {"place_name_raw": "渐台", "role": "location", "link_status": "needs_linking", "sequence": 2,
             "description_zh_cn": "王莽败亡被杀处（长安未央宫渐台）",
             "review_note": "ready43-c1：汉书·王莽传下「莽就车，之渐台，欲阻池水」"},
        ],
        "evidence": [
            ev("汉书", "王莽传下", "传/王莽传下#p412", "text-niutrans-2b564a2309cdac4da36b",
               "process", "primary", "会世祖悉发郾、定陵兵数千人来救昆阳……与汉兵战，不利。"),
            ev("汉书", "王莽传下", "传/王莽传下#p414", "text-niutrans-ea2b8f151f5c8a5258d6",
               "process", "supporting", "昆阳中兵出并战，邑走，军乱。"),
            ev("资治通鉴", "汉纪三十一", "汉纪/汉纪三十一#p147", "text-niutrans-c3873ee431c31d0ac33a",
               "result", "primary", "商人杜吴杀莽，校尉东海公宾就斩莽首。"),
            ev("资治通鉴", "汉纪三十一", "汉纪/汉纪三十一#p153", "text-niutrans-ab9c76a72314bae36f5c",
               "impact", "primary", "传莽首诣宛，县于市。百姓共提击之，或切食其舌。"),
            ev("汉书", "王莽传下", "传/王莽传下#p523", "text-niutrans-abc67f48b74385304e3d",
               "result", "supporting", "莽就车，之渐台，欲阻池水。"),
        ],
    },
    "qin_han/event-chuhan-later.yml": {
        "background_zh_cn": "垓下战后，汉王还至定陶，驰入齐王信壁夺其军——战争结束即着手收兵权、定秩序。",
        "process_zh_cn": "春正月，更立齐王信为楚王，王淮北、都下邳；封魏相国建城侯彭越为梁王，王魏故地、都定陶——以分封安置功臣、重组东方秩序。",
        "impact_zh_cn": "既而诏封故衡山王吴芮为长沙王等，令曰「兵不得休八年，万民与苦甚，今天下事毕，其赦天下殊死以下」——与民休息、郡国并行，汉初秩序自此定型。",
        "relations": [
            {"target_event_id": "event-chuhan-han-foundation", "relation_type": "follows", "confidence": 0.9,
             "description_zh_cn": "汉政权建立后的整合与秩序重建，紧承称帝之后。"},
            {"target_event_id": "event-hanchu-yixingwang", "relation_type": "related_to", "confidence": 0.8,
             "description_zh_cn": "同为汉初收兵权、定秩序的进程（分封—剪除异姓王的前后章）。"},
        ],
        "evidence": [
            ev("资治通鉴", "汉纪三", "汉纪/汉纪三#p64", "text-niutrans-bf7a2c8c22c8b226bb45",
               "background", "primary", "汉王还，至定陶，驰入齐王信壁，夺其军。"),
            ev("资治通鉴", "汉纪三", "汉纪/汉纪三#p66", "text-niutrans-925eaf5ac4a1d672be96",
               "process", "primary", "春，正月，更立齐王信为楚王，王淮北，都下邳。"),
            ev("资治通鉴", "汉纪三", "汉纪/汉纪三#p73", "text-niutrans-9db041b336e9103f7bb6",
               "result", "primary", "诏曰： 故衡山王吴芮，从百粤之兵，佐诸侯，诛暴秦，有大功。"),
            ev("资治通鉴", "汉纪三", "汉纪/汉纪三#p68", "text-niutrans-d4c5b107aff141f573b1",
               "impact", "primary", "令曰： 兵不得休八年，万民与苦甚。"),
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
        existing = yaml.safe_load(path.read_text())
        if existing.get("process_zh_cn"):
            print(f"SKIP {rel}")
            continue
        block.pop("result_anchor_note", None)
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
