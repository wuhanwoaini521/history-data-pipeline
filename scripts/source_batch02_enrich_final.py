"""Source Batch 02 · 收官富化（12 事件：晋书群 + 旧唐书 + 后汉书 + 旧五代史 + 魏书 + 明史）。

全部锚点来自本轮新入库语料（wikisource/20260912b 及既有 NiuTrans 晋书/魏书/后汉书/旧五代史/明史）。
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


BLOCKS: dict[str, dict] = {
    # ---- 晋书群 ----
    "jin_southern_northern/event-bawang-zhi-luan.yml": {
        "background_zh_cn": "惠帝之世，齐王冏、河间王颙、成都王颖并拥强兵、各据一方；赵王伦党羽秀知诸王必有异图，乃选亲党为三王参佐郡守——宗室相图之势已成。",
        "process_zh_cn": "及三王起兵讨赵王伦檄至，伦、秀始大惧，遣孙辅、张泓等率兵分出延寿、堮阪、成皋诸关以距义师。",
        "result_zh_cn": "长沙王乂与齐王冏相攻：乂奉天子与冏战，连战三日，冏败被斩，并诛其党羽——八王相斫，洛阳屡经兵火。",
        "impact_zh_cn": "终局系于东海王越：越以张方劫迁车驾、天下怨愤，唱义与山东诸侯克期奉迎，先遣使说河间王颙送帝还都——八王之乱以越秉政、惠帝返洛收束，西晋元气已尽。",
        "people": [
            {"person_name_raw": "司马乂", "role": "opponent", "link_status": "needs_linking",
             "role_zh_cn": "长沙王：奉天子与齐王冏相攻，冏败",
             "review_note": "source-batch02：晋书·八王列传「乂奉天子与冏相攻」「冏败，斩之」", "person_id": None},
            {"person_name_raw": "司马越", "role": "opponent", "link_status": "needs_linking",
             "role_zh_cn": "东海王：唱义奉迎、终秉朝政",
             "review_note": "source-batch02：晋书·八王列传「东海王越虑事不济」「越以张方劫迁车驾…唱义与山东诸侯克期奉迎」", "person_id": None},
        ],
        "places": [
            {"place_name_raw": "洛阳", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "八王相攻的中心（奉天子相攻、火烧冏府）",
             "review_note": "source-batch02：晋书·八王列传「奉天子与冏相攻，起火烧冏府」"},
        ],
        "evidence": [
            ev("晋书", "八王列传", "列传/八王列传#p33", "text-wikisource-f21d763277cdfff4294d", "background", "primary",
               "时齊王冏、河間王顒、成都王穎並擁強兵，各據一方。秀知冏等必有異圖。"),
            ev("晋书", "八王列传", "列传/八王列传#p35", "text-wikisource-875b2bf311c66db9e8dc", "process", "primary",
               "及三王起兵討倫檄至，倫、秀始大懼，遣其中堅孫輔为上軍將軍。"),
            ev("晋书", "八王列传", "列传/八王列传#p54", "text-wikisource-5c114b63d3d9540313b8", "result", "primary",
               "奉天子与冏相攻，起火燒冏府，連战三日，冏敗，斬之。"),
            ev("晋书", "八王列传", "列传/八王列传#p74", "text-wikisource-bec16a7220b1a0a70ab5", "impact", "primary",
               "初，越以張方劫遷車駕，天下怨憤，唱義与山东諸侯克期奉迎。"),
        ],
    },
    "jin_southern_northern/event-dongjin-jianguo.yml": {
        "background_zh_cn": "永嘉初，司马睿用王导之计始镇建邺，以顾荣为军司马、贺循为参佐，王敦、王导、周顗、刁协并为腹心股肱，宾礼名贤、存问风俗，江东归心。",
        "process_zh_cn": "愍帝诏使摄万机、时据旧都；三月，帝素服出次举哀三日，群臣以死固请上尊号，乃请依魏晋故事为晋王，许之，辛卯即王位。",
        "result_zh_cn": "六月，刘琨、段匹磾、慕容廆等一百八十人上书劝进——江东政权获得北方流亡势力与诸州牧守的承认。",
        "impact_zh_cn": "王位既立即建东晋体制：立世子绍为晋王太子，以王导都督中外诸军事、王敦为大将军——「王与马共天下」的江左门阀政治格局自此确立。",
        "people": [
            {"person_name_raw": "司马睿", "role": "monarch", "link_status": "needs_linking",
             "role_zh_cn": "晋元帝：镇建邺、即晋王位，东晋开国",
             "review_note": "source-batch02：晋书·元帝纪「用王導計，始鎮建鄴」「辛卯，卽王位」", "person_id": None},
            {"person_name_raw": "王导", "role": "supporter", "link_status": "needs_linking",
             "role_zh_cn": "谋主：劝睿镇建邺、都督中外诸军事",
             "review_note": "source-batch02：晋书·元帝纪「王導都督中外諸軍事」", "person_id": None},
        ],
        "places": [
            {"place_name_raw": "建邺", "role": "capital", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "司马睿镇守之地（后改建康，东晋都城）",
             "review_note": "source-batch02：晋书·元帝纪「始鎮建鄴」"},
        ],
        "evidence": [
            ev("晋书", "元帝纪", "帝纪/元帝纪#p4", "text-wikisource-0b643f82143521fa7eaa", "background", "primary",
               "永嘉初，用王導計，始鎮建鄴……賓禮名賢，存問風俗，江东歸心焉。"),
            ev("晋书", "元帝纪", "帝纪/元帝纪#p6", "text-wikisource-1ec806030740bb1d78d2", "process", "primary",
               "請依魏晉故事爲晉王，許之。辛卯，卽王位。"),
            ev("晋书", "元帝纪", "帝纪/元帝纪#p8", "text-wikisource-269c17bc2cf7e871056a", "result", "primary",
               "等一百八十人上书勸進。"),
            ev("晋书", "元帝纪", "帝纪/元帝纪#p7", "text-wikisource-52d2ae49ae61a6b52c32", "impact", "primary",
               "立世子紹爲晉王太子……王導都督中外諸軍事。"),
        ],
    },
    "jin_southern_northern/event-feishui-zhizhan.yml": {
        "background_zh_cn": "苻坚自率兵次项城，众号百万；凉州之师始达咸阳，蜀汉顺流、幽并系至；先遣苻融、慕容暐等至颍口，梁成等屯洛涧。诏以谢玄为前锋、都督徐兖青三州等诸军事。",
        "process_zh_cn": "硃序诡谓谢石「及其众军未集，宜在速战」，谢琰劝从序言、遣使请战；谢玄、谢琰勒卒数万，阵以待之。",
        "result_zh_cn": "乙亥，诸将及苻坚战于肥水，大破之，俘斩数万计，获坚舆辇及云母车——淝水一战，前秦大军崩溃。",
        "impact_zh_cn": "史论谓「其后，坚再南伐，遂有淝水之败，身戮国亡」——前秦由盛转亡，北方重新分裂，东晋得以延续江左。",
        "people": [
            {"person_name_raw": "谢玄", "role": "supporter", "link_status": "needs_linking",
             "role_zh_cn": "晋军前锋都督：淝水破苻坚",
             "review_note": "source-batch02：晋书·谢玄传「詔以玄为前鋒」", "person_id": None},
            {"person_name_raw": "苻坚", "role": "opponent", "link_status": "needs_linking",
             "role_zh_cn": "前秦天王：率百万之众南伐，淝水大败",
             "review_note": "source-batch02：晋书·苻坚载记「及苻堅自率兵次於项城，眾号百萬」", "person_id": None},
        ],
        "places": [
            {"place_name_raw": "肥水", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "决战之地（淝水）",
             "review_note": "source-batch02：晋书「諸將及苻堅战于肥水，大破之」"},
        ],
        "evidence": [
            ev("晋书", "谢玄传", "列传/谢玄传#p32", "text-wikisource-da3dd5860fbd4f1e1615", "background", "primary",
               "及苻堅自率兵次於项城，眾号百萬……詔以玄为前鋒。"),
            ev("晋书", "苻坚载记", "载记/苻坚载记下#p18", "text-wikisource-348444e7ba4426c3c1f4", "process", "primary",
               "謝玄、謝琰勒卒數萬，陣以待之。"),
            ev("晋书", "第九章", "第九章#p247", "text-niutrans-b3aa61be84234786c5c3", "result", "primary",
               "乙亥，诸将及苻坚战于肥水，大破之，俘斩数万计，获坚舆辇及云母车。"),
            ev("晋书", "第十九章", "第十九章#p420", "text-niutrans-b87486a36d592661116c", "impact", "primary",
               "其后，坚再南伐，遂有淝水之败，身戮国亡。"),
        ],
    },
    "jin_southern_northern/event-jin-mie-wu.yml": {
        "background_zh_cn": "武帝谋伐吴，诏王濬修舟舰：作大船连舫，方百二十步、受二千余人，以木为城、起楼橹，舟楫之盛自古未有；濬造船于蜀，木柿蔽江而下。",
        "process_zh_cn": "十一月，晋大举伐吴：遣琅邪王伷出涂中，王浑出江西，王戎出武昌，平南将军胡奋等出夏口，王濬、唐彬下巴蜀——六路并进。",
        "result_zh_cn": "王濬破石头，降孙皓，威名益振；吴平，三国分裂之局终结。",
        "impact_zh_cn": "帝临轩大会，引孙皓升殿，群臣咸称万岁；孙皓归降后受封归命侯——西晋完成统一，然承平未久而乱端已伏。",
        "people": [
            {"person_name_raw": "王濬", "role": "supporter", "link_status": "needs_linking",
             "role_zh_cn": "益州刺史：造楼船、破石头降孙皓",
             "review_note": "source-batch02：晋书·王濬传「王濬破石頭，降孫皓」", "person_id": None},
            {"person_name_raw": "孙皓", "role": "opponent", "link_status": "needs_linking",
             "role_zh_cn": "吴末帝：穷迫归降，赐号归命侯",
             "review_note": "source-batch02：三国志·三嗣主传「孙皓穷迫归降……其赐号为归命侯」", "person_id": None},
        ],
        "places": [
            {"place_name_raw": "石头", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "建业江防要塞，王濬破之",
             "review_note": "source-batch02：晋书·王濬传「王濬破石頭，降孫皓」"},
        ],
        "evidence": [
            ev("晋书", "王濬传", "列传/王濬传#p20", "text-wikisource-b59cfeb28da6c8c32b41", "background", "primary",
               "武帝謀伐吳，詔濬修舟艦。濬乃作大船連舫，方百二十步，受二千餘人。"),
            ev("晋书", "武帝纪", "帝纪/武帝纪#p153", "text-wikisource-de22c2daa7dbb1bb301b", "process", "primary",
               "十一月，大舉伐吳，遣鎮軍將軍、琅邪王伷出涂中。"),
            ev("晋书", "王濬传", "列传/王濬传#p5", "text-wikisource-1fc1bf754f21fb922f65", "result", "primary",
               "既而王濬破石頭，降孫皓，威名益振。"),
            ev("晋书", "武帝纪", "帝纪/武帝纪#p160", "text-wikisource-a8e4f655c75ac20cd49d", "impact", "primary",
               "帝臨軒大会，引皓升殿，群臣咸稱萬歲。"),
            ev("三国志", "三嗣主传", "吴书/三嗣主传#p354", "text-niutrans-8ee996e48d36905af934", "impact", "supporting",
               "孙皓穷迫归降，前诏待之以不死……其赐号为归命侯。"),
        ],
    },
    "jin_southern_northern/event-xijin-mie-wang.yml": {
        "background_zh_cn": "建兴四年四月，刘曜寇上郡，太守籍韦率众奔南郑；凉州刺史张寔遣步骑五千来赴京都——长安政权仅赖凉州与关中残军支撑。",
        "process_zh_cn": "秋七月，刘曜攻北地，麴允帅步骑三万救之，王师不战而溃；曜进至泾阳，渭北诸城悉溃，建威将军鲁充等皆死之。",
        "result_zh_cn": "八月，刘曜逼京师，内外断绝；麴允与公卿守长安小城以自固——长安已成孤城。",
        "impact_zh_cn": "十一月，帝乘羊车、肉袒衔壁、舆榇出降；刘曜焚榇受壁——西晋灭亡，北方进入十六国时期。",
        "people": [
            {"person_name_raw": "刘曜", "role": "opponent", "link_status": "needs_linking",
             "role_zh_cn": "汉赵将领：攻北地、逼长安，受愍帝出降",
             "review_note": "source-batch02：晋书·愍帝纪「刘曜逼京師，內外斷絕」", "person_id": None},
            {"person_name_raw": "麴允", "role": "supporter", "link_status": "needs_linking",
             "role_zh_cn": "晋将：守长安小城，兵败",
             "review_note": "source-batch02：晋书·愍帝纪「麴允与公卿守長安小城以自固」", "person_id": None},
        ],
        "places": [
            {"place_name_raw": "长安", "role": "capital", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "西晋末代都城：被围、愍帝出降",
             "review_note": "source-batch02：晋书·愍帝纪「刘曜逼京師」「守長安小城」"},
            {"place_name_raw": "北地", "role": "battlesite", "link_status": "needs_linking", "sequence": 2,
             "description_zh_cn": "刘曜攻取之地（王师不战而溃）",
             "review_note": "source-batch02：晋书·愍帝纪「刘曜攻北地」"},
        ],
        "evidence": [
            ev("晋书", "愍帝纪", "帝纪/愍帝纪#p98", "text-wikisource-e0bedf82648d54a615f4", "background", "primary",
               "夏四月丁丑，刘曜寇上郡，太守籍韋率其衆奔于南鄭。"),
            ev("晋书", "愍帝纪", "帝纪/愍帝纪#p101", "text-wikisource-12c7d07e70173ada95b9", "process", "primary",
               "秋七月，刘曜攻北地……曜進至涇陽，渭北諸城悉潰。"),
            ev("晋书", "愍帝纪", "帝纪/愍帝纪#p102", "text-wikisource-0c95405959e570458b53", "result", "primary",
               "八月，刘曜逼京師，內外斷絕……麴允与公卿守長安小城以自固。"),
            ev("晋书", "愍帝纪", "帝纪/愍帝纪#p104", "text-wikisource-98248714ee0d27435bc9", "impact", "primary",
               "帝乘羊車，肉袒銜壁，輿櫬出降……曜焚櫬受壁。"),
        ],
    },
    "jin_southern_northern/event-yongjia-zhi-luan.yml": {
        "background_zh_cn": "怀帝永嘉元年三月，洛阳东北步广里地陷——史官载其异兆，天下已摇。",
        "process_zh_cn": "刘曜乘乱西进：攻北地、进至泾阳，渭北诸城悉溃；建威将军鲁充、散骑常侍梁纬等皆死之——永嘉乱后关中防线瓦解。",
        "result_zh_cn": "刘曜逼京师，内外断绝；公卿守长安小城自固——洛阳既陷（311），长安复成孤城（316），两京相继倾覆。",
        "impact_zh_cn": "史论晋室之亡：「怀帝承乱得位，羁于强臣，愍帝奔播之后，徒厕其虚名，天下之政既去」——衣冠南渡，北方沦入十六国。",
        "people": [
            {"person_name_raw": "晋怀帝", "role": "monarch", "link_status": "needs_linking",
             "role_zh_cn": "永嘉之乱时的皇帝：承乱得位、羁于强臣",
             "review_note": "source-batch02：晋书「怀帝承乱得位，羁于强臣」", "person_id": None},
        ],
        "places": [
            {"place_name_raw": "洛阳", "role": "capital", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "永嘉元年地陷异兆之地；永嘉五年陷落",
             "review_note": "source-batch02：晋书第十九章「怀帝永嘉元年三月，洛阳东北步广里地陷」"},
        ],
        "evidence": [
            ev("晋书", "第十九章", "第十九章#p711", "text-niutrans-dd270692dbfa0ac96bb9", "background", "primary",
               "怀帝永嘉元年三月，洛阳东北步广里地陷。"),
            ev("晋书", "愍帝纪", "帝纪/愍帝纪#p101", "text-wikisource-12c7d07e70173ada95b9", "process", "primary",
               "曜進至涇陽，渭北諸城悉潰。"),
            ev("晋书", "愍帝纪", "帝纪/愍帝纪#p102", "text-wikisource-0c95405959e570458b53", "result", "primary",
               "八月，刘曜逼京師，內外斷絕。"),
            ev("晋书", "第五章", "第五章#p415", "text-niutrans-80eed9095b9e09fb8efa", "impact", "primary",
               "怀帝承乱得位，羁于强臣，愍帝奔播之后，徒厕其虚名，天下之政既去。", "史论（本事件为 311–316 过程 aggregate）"),
        ],
    },
    # ---- 旧唐书/后汉书/旧五代史/魏书/明史 ----
    "sui_tang/event-huangchao-qiyi.yml": {
        "background_zh_cn": "黄巢之众渡江寇淮南；时昭义、武宁、义武等军兵马数万赴淮南，高骈欲收功于己，奏贼已殄、遣还诸道之师。",
        "process_zh_cn": "十一月，贼陷东都，留守刘允章率分司官属迎谒；再陷虢州，攻潼关，守关诸将望风自溃。",
        "result_zh_cn": "黄巢长驱江表、径入关中——广明元年十二月入长安，僖宗西幸。",
        "impact_zh_cn": "其亡也以沙陀与诸道之师：四年二月李克用率山西诸军济河赴援陈州，四月官军败贼于太康，俘斩万计——黄巢起义终至覆灭，而唐廷已赖藩镇之力，名存实亡。",
        "people": [
            {"person_name_raw": "黄巢", "role": "opponent", "link_status": "needs_linking",
             "role_zh_cn": "起义领袖：陷东都、入关中",
             "review_note": "source-batch02：旧唐书·黄巢传「徑入关中」；僖宗纪「賊陷东都」", "person_id": None},
            {"person_name_raw": "李克用", "role": "supporter", "link_status": "needs_linking",
             "role_zh_cn": "沙陀首领：率山西诸军赴援、败贼", "review_note": "source-batch02：旧唐书·黄巢传「李克用率山西諸軍，由蒲、陝濟河」", "person_id": None},
        ],
        "places": [
            {"place_name_raw": "潼关", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "黄巢军攻取之关隘（守将望风自溃）",
             "review_note": "source-batch02：旧唐书·僖宗纪「攻潼关，守关諸將望風自潰」"},
            {"place_name_raw": "东都", "role": "capital", "link_status": "needs_linking", "sequence": 2,
             "description_zh_cn": "洛阳：黄巢陷之",
             "review_note": "source-batch02：旧唐书·僖宗纪「賊陷东都」"},
        ],
        "evidence": [
            ev("旧唐书", "僖宗纪", "本纪/僖宗纪#p65", "text-wikisource-f693adff13f2100dcdbd", "background", "primary",
               "八月，黃巢之眾渡江寇淮南。……駢欲收功於己，乃奏賊已將殄。"),
            ev("旧唐书", "僖宗纪", "本纪/僖宗纪#p67", "text-wikisource-1d473e4764c6d2e3f9fa", "process", "primary",
               "己巳，賊陷东都……丙子，攻潼关，守关諸將望風自潰。"),
            ev("旧唐书", "黄巢传", "列传/黄巢传#p42", "text-wikisource-3c92003bf43ceff24b74", "result", "primary",
               "一旦長驅江表，徑入关中。"),
            ev("旧唐书", "黄巢传", "列传/黄巢传#p34", "text-wikisource-fe6609fdd25d3062c4cb", "impact", "primary",
               "四月，官軍敗賊于太康，俘斬萬計，拔其四壁。"),
        ],
    },
    "sui_tang/event-tang-mie-dong-tujue.yml": {
        "background_zh_cn": "颉利初嗣立，承父兄之资，兵马强盛，有凭陵中国之志；高祖以中原初定，每优容之，赐与不可胜计，颉利求请无厌。",
        "process_zh_cn": "贞观元年，阴山已北薛延陀、回纥、拔也古等部皆相率背叛；其国大雪，平地数尺，羊马皆死，人大饥——东突厥内部瓦解。",
        "result_zh_cn": "及其国乱，诸部多归中国，唯思摩随逐颉利，竟与同擒——颉利可汗被擒，东突厥汗国灭亡。",
        "impact_zh_cn": "颉利既死，太宗闻而异之，赠中郎将，仍葬于颉利墓侧，树碑以纪之——天可汗体制与突厥降众安置自此展开。",
        "people": [
            {"person_name_raw": "颉利可汗", "role": "opponent", "link_status": "needs_linking",
             "role_zh_cn": "东突厥可汗：国乱被擒，东突厥亡",
             "review_note": "source-batch02：旧唐书·突厥传「竟与同擒」", "person_id": None},
            {"person_name_raw": "阿史那思摩", "role": "supporter", "link_status": "needs_linking",
             "role_zh_cn": "颉利族人：随逐颉利同擒，后统颉利旧部",
             "review_note": "source-batch02：旧唐书·突厥传「唯思摩隨逐頡利，竟与同擒」", "person_id": None},
        ],
        "places": [
            {"place_name_raw": "阴山", "role": "region", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "阴山已北诸部叛离之地",
             "review_note": "source-batch02：旧唐书·突厥传「陰山已北薛延陀、回紇、拔也古等部皆相率背叛」"},
        ],
        "evidence": [
            ev("旧唐书", "突厥传", "列传/突厥传#p8", "text-wikisource-db44f3d693fb239f8413", "background", "primary",
               "頡利初嗣立，承父兄之資，兵馬強盛。有憑陵中国之志。"),
            ev("旧唐书", "突厥传", "列传/突厥传#p14", "text-wikisource-4172fc89573d077d6577", "process", "primary",
               "貞觀元年，陰山已北薛延陀、回紇、拔也古等部皆相率背叛……其国大雪，平地數尺，羊馬皆死，人大饑。"),
            ev("旧唐书", "突厥传", "列传/突厥传#p26", "text-wikisource-96804b06b0d62abea878", "result", "primary",
               "及其国亂，諸部多歸中国，唯思摩隨逐頡利，竟与同擒。"),
            ev("旧唐书", "突厥传", "列传/突厥传#p19", "text-wikisource-a17dc331f1b4a364b68d", "impact", "primary",
               "太宗聞而異之，贈中郎將，仍葬於頡利墓側，樹碑以紀之。"),
        ],
    },
    "jin_southern_northern/event-beiwei-tongyi-beifang.yml": {
        "background_zh_cn": "北凉主牧犍统任，自称河西王，遣使请朝命——十六国末期的河西政权在北魏威压下求存。",
        "process_zh_cn": "太武帝亲征北凉：车驾至姑臧，牧犍兄子祖逾城来降，魏乃分军围之。",
        "result_zh_cn": "北凉既平，牧犍仍与故臣民交通谋反，诏司徒崔浩就公主第赐牧犍死——北凉灭亡。",
        "impact_zh_cn": "既克凉州，世祖大会于姑臧——北凉为十六国最后一国，其亡标志北魏完成北方统一，南北朝对峙格局定型。",
        "people": [
            {"person_name_raw": "沮渠牧犍", "role": "opponent", "link_status": "needs_linking",
             "role_zh_cn": "北凉主：降魏后赐死，北凉亡",
             "review_note": "source-batch02：魏书「牧犍猶與故臣民交通謀反……賜牧犍死」", "person_id": None},
            {"person_name_raw": "拓跋焘", "role": "monarch", "link_status": "needs_linking",
             "role_zh_cn": "北魏太武帝：亲征姑臧、克凉州",
             "review_note": "source-batch02：魏书·帝纪「車駕至姑臧」", "person_id": None},
        ],
        "places": [
            {"place_name_raw": "姑臧", "role": "capital", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "北凉都城：被围、城克",
             "review_note": "source-batch02：魏书「車駕至姑臧……乃分軍圍之」「世祖大会于姑臧」"},
        ],
        "evidence": [
            ev("魏书", "列传", "列传/卷八十七#p1", "text-niutrans-041ec118393563a1b5fc", "background", "primary",
               "第三子牧犍統任，自稱河西王，遣使請朝命。"),
            ev("魏书", "帝纪", "帝纪/卷四#p461", "text-niutrans-3b347a4a4bb441170322", "process", "primary",
               "丙申，車駕至姑臧，牧犍兄子祖逾城来降，乃分軍圍之。"),
            ev("魏书", "列传", "列传/卷八十七#p62", "text-niutrans-ab28f12ec6d51e81c0ec", "result", "primary",
               "是年，人又告牧犍猶與故臣民交通謀反，詔司徒崔浩就公主第賜牧犍死。"),
            ev("魏书", "列传", "列传/卷三十二#p8", "text-niutrans-dd1439b496d868e53b47", "impact", "primary",
               "既克涼州，世祖大会于姑臧。"),
        ],
    },
    "three_kingdoms/event-caopi-dai-han.yml": {
        "background_zh_cn": "建安二十五年春正月庚子，魏王曹操薨——汉廷最后的权臣故去，禅代之局交与其子。",
        "process_zh_cn": "冬十月乙卯，皇帝逊位，魏王丕称天子——汉魏禅代完成。",
        "result_zh_cn": "逊位之后十四年，山阳公（献帝）薨，年五十四，谥孝献皇帝——亡国之君得终天年、以礼改谥。",
        "impact_zh_cn": "八月壬申，以汉天子礼仪葬于禅陵，置园邑令丞——汉室以宾礼终，曹魏以「禅让」范式开魏晋南北朝易代模式。",
        "people": [
            {"person_name_raw": "曹丕", "role": "monarch", "link_status": "needs_linking",
             "role_zh_cn": "魏王：受禅称天子（魏文帝）",
             "review_note": "source-batch02：后汉书·孝献帝纪「魏王丕稱天子」", "person_id": None},
            {"person_name_raw": "汉献帝", "role": "deposed_monarch", "link_status": "needs_linking",
             "role_zh_cn": "逊位之君：废为山阳公，谥孝献皇帝",
             "review_note": "source-batch02：后汉书·孝献帝纪「自遜位至薨，十有四年」", "person_id": None},
        ],
        "places": [
            {"place_name_raw": "禅陵", "role": "location", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "献帝以汉天子礼仪所葬之地",
             "review_note": "source-batch02：后汉书·孝献帝纪「以汉天子禮儀葬于禪陵」"},
        ],
        "evidence": [
            ev("后汉书", "孝献帝纪", "本纪/孝献帝纪#p264", "text-niutrans-99ef023433c8ab465a64", "background", "primary",
               "二十五年春正月庚子，魏王曹操薨。"),
            ev("后汉书", "孝献帝纪", "本纪/孝献帝纪#p267", "text-niutrans-4ab573bae8e0325e68fe", "process", "primary",
               "冬十月乙卯，皇帝遜位，魏王丕稱天子。"),
            ev("后汉书", "孝献帝纪", "本纪/孝献帝纪#p271", "text-niutrans-d72d8aa8c42bba3c8d63", "result", "primary",
               "自遜位至薨，十有四年，年五十四，謚孝獻皇帝。"),
            ev("后汉书", "孝献帝纪", "本纪/孝献帝纪#p272", "text-niutrans-07065a7be10c241d3a7e", "impact", "primary",
               "八月壬申，以汉天子禮儀葬于禪陵，置園邑令丞。"),
        ],
    },
    "five_dynasties/event-guo-wei-dai-han.yml": {
        "background_zh_cn": "隐帝遇弑后，郭威得密诏，即召王峻、郭崇、曹英及诸军将校至牙署视诏，兼告杨、史诸公冤枉之状——起兵之名由此而立。",
        "process_zh_cn": "汉太后令曰：枢密使、侍中郭威「剪除祸乱，宏济艰难，功业格天，人望冠世」，宜总万机、可监国。",
        "result_zh_cn": "监国教曰「寡人出自军戎，本无德望，因缘际会，叨窃宠灵」——郭威受监国之任，中外庶事并取监国处分。",
        "impact_zh_cn": "自请立嗣君、入请太后临朝，至受监国、总万机——后周代汉之程序于此完成，五代易代「军士拥立—监国—受禅」的模式再度上演。",
        "people": [
            {"person_name_raw": "郭威", "role": "monarch", "link_status": "needs_linking",
             "role_zh_cn": "枢密使、侍中：受监国，后周太祖",
             "review_note": "source-batch02：旧五代史·周太祖纪「可監國」", "person_id": None},
        ],
        "places": [],
        "evidence": [
            ev("旧五代史", "隐帝纪下", "后汉/隐帝纪下#p40", "text-niutrans-c555b947d961d06dec75", "background", "primary",
               "郭威得之，即召王峻、郭崇、曹英及諸軍將校，至牙署視詔。"),
            ev("旧五代史", "周太祖纪", "后周/太祖纪一#p132", "text-niutrans-3e56b8104fd5b4cca533", "process", "primary",
               "二十七日，汉太后令曰： 樞密使、侍中郭威……宜總萬機，以允群議，可監國。"),
            ev("旧五代史", "周太祖纪", "后周/太祖纪一#p133", "text-niutrans-1a2cd0882143bb3b3936", "result", "primary",
               "中外庶事，並取監國處分。"),
            ev("旧五代史", "周太祖纪", "后周/太祖纪一#p134", "text-niutrans-269a05bceaa575b1aa53", "impact", "primary",
               "監國教曰： 寡人出自軍戎，本无德望，因緣際会，叨竊寵靈。"),
        ],
    },
    "ming/event-qian-du-beijing.yml": {
        "background_zh_cn": "永乐元年，以北平为北京，置北京行部尚书二人、侍郎四人，其属置六曹清吏司；后又分置六部——行在体制初立。",
        "process_zh_cn": "永乐四年闰月，诏以明年五月建北京宫殿，分遣大臣采木于四川、湖广、江西、浙江、山西——营建工程启动。",
        "result_zh_cn": "永乐十八年十一月戊辰，以迁都北京诏天下——北京正式成为都城。",
        "impact_zh_cn": "丁亥，诏自明年改京师为南京、北京为京师——两京并立之制由此定型，明廷政治重心北移，影响此后五百年版图格局。",
        "people": [
            {"person_name_raw": "明成祖", "role": "monarch", "link_status": "needs_linking",
             "role_zh_cn": "永乐帝：决策迁都北京",
             "review_note": "source-batch02：明史·成祖本纪「以迁都北京詔天下」", "person_id": None},
        ],
        "places": [
            {"place_name_raw": "北京", "role": "capital", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "永乐迁都后的京师（原北平）",
             "review_note": "source-batch02：明史「以北平为北京」「以迁都北京詔天下」"},
            {"place_name_raw": "南京", "role": "capital", "link_status": "needs_linking", "sequence": 2,
             "description_zh_cn": "原京师，迁都后改称南京",
             "review_note": "source-batch02：明史·成祖本纪「改京师为南京」"},
        ],
        "evidence": [
            ev("明史", "地理志", "志/卷四十八#p169", "text-niutrans-03e94309ded1feb48be6", "background", "primary",
               "永乐元年，以北平为北京，置北京行部尚书二人，侍郎四人。"),
            ev("明史", "成祖本纪", "本纪/卷六#p122", "text-niutrans-d5e1064e292149c6fbca", "process", "primary",
               "閏月壬戌，詔以明年五月建北京宮殿，分遣大臣采木于四川、湖廣、江西、浙江、山西。"),
            ev("明史", "成祖本纪", "本纪/卷七#p147", "text-niutrans-96e2906f4a1b27a367e3", "result", "primary",
               "十一月戊辰，以遷都北京詔天下。"),
            ev("明史", "成祖本纪", "本纪/卷七#p145", "text-niutrans-d107859c108985a5012b", "impact", "primary",
               "丁亥，詔自明年改京師为南京，北京为京師。"),
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
