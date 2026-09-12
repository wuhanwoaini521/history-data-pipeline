"""Batch 02 · Queue 10 — Critical source-grounded enrichment（append-only YAML 写入）。

对 6 个可解锁 Critical（西夏建国/七七/日本投降/南京大屠杀/新中国成立/五四运动），
把 wikisource Batch 01 语料中的段落锚（text-wikisource-*）落为：
  background/process/result/impact 四维叙述 + people/places(needs_linking) + evidence(manual 段落锚)。
所有叙述句均可回溯到 review_note 中逐字引文；不引入语料外事实。
写入方式：只向 YAML 文件末尾追加，绝不重写既有字节（保留头注释与 relations）。
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
EVENTS = ROOT / "data" / "curated" / "history_backbone" / "events"


def ev(work, term, text_id, anchor, field, role, quote, note_extra=""):
    return {
        "work": work, "term": term, "historical_text_id": text_id, "chapter_anchor": anchor,
        "claim_field": field, "evidence_role": role, "link_status": "linked",
        "link_method": "manual", "link_confidence": 1.0, "link_quality_status": "reviewed",
        "context_keywords": [],
        "review_note": f"batch02-10：source-grounded（wikisource/20260912）引文：「{quote}」；claim_field={field}；anchor=段落精确锚。{note_extra}",
    }


BLOCKS: dict[str, dict] = {
    "song_liao_xia_jin/event-western-xia-jianguo.yml": {
        "background_zh_cn": "元昊袭封夏国王后整军立制：明号令、以兵法勒诸部，自号「嵬名吾祖」，设中书、枢密等文武班官制；宝元元年（1038）先遣使窥探河东道路，与诸豪歃血约先攻鄜延，欲自德靖、塞门砦、赤城路三道并进。",
        "process_zh_cn": "宝元元年十月十一日，元昊郊坛备礼、筑坛受册，即皇帝位，时年三十；国称大夏，年号天授礼法延祚。随后遣使上表宋廷，自陈「臣祖宗本出帝胄」，称「制小蕃文字，改大汉衣冠……吐蕃、塔塔、张掖、交河，莫不从伏」，求「许以西郊之地，册为南面之君」。",
        "result_zh_cn": "宋廷不允，诏削夺元昊官爵、互市，揭榜于边，募能擒斩元昊者即授定难军节度使，并遣使赍嫚书、纳还旌节敕告；宋夏交恶，康定元年战事起，夏人破金明砦、围延州、设伏三川口，宋将刘平、石元孙等被执。",
        "impact_zh_cn": "西夏以大夏国号、年号与官制立国，宋廷削爵绝市，康定元年后金明砦、延州、三川口、镇戎军等役接连爆发——宋夏长期军事对峙自此展开。",
        "people": [
            {"person_name_raw": "李元昊", "role": "monarch", "link_status": "needs_linking",
             "role_zh_cn": "称帝建国者：筑坛受册即皇帝位，国称大夏",
             "review_note": "batch02-10：宋史·夏国传上「遂築壇受冊，即皇帝位，時年三十」", "person_id": None},
            {"person_name_raw": "刘平", "role": "opponent", "link_status": "needs_linking",
             "role_zh_cn": "宋将，三川口之役被夏军所执",
             "review_note": "batch02-10：宋史·夏国传上「圍延州，設伏三川口，執劉平、石元孫、傅偃、劉發、石遜等」", "person_id": None},
        ],
        "places": [
            {"place_name_raw": "鄜延", "role": "region", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "元昊与诸豪歃血谋攻的宋边路分",
             "review_note": "batch02-10：宋史·夏国传上「與諸豪歃血約先攻鄜延」"},
            {"place_name_raw": "延州", "role": "battlesite", "link_status": "needs_linking", "sequence": 2,
             "description_zh_cn": "康定元年夏军围困的宋边州城",
             "review_note": "batch02-10：宋史·夏国传上「破安遠、塞門、永平諸砦，圍延州」"},
            {"place_name_raw": "三川口", "role": "battlesite", "link_status": "needs_linking", "sequence": 3,
             "description_zh_cn": "夏军设伏俘宋将之地",
             "review_note": "batch02-10：宋史·夏国传上「設伏三川口，執劉平、石元孫」"},
            {"place_name_raw": "五台山", "role": "location", "link_status": "needs_linking", "sequence": 4,
             "description_zh_cn": "宝元元年元昊表遣使供佛、借以窥探河东道路",
             "review_note": "batch02-10：宋史·夏国传上「表遣使詣五臺山供佛寶，欲窺河東道路」"},
        ],
        "evidence": [
            ev("宋史", "夏国传上", "text-wikisource-e2ab9a632298b908abd8", "列传/卷四百八十五#p62",
               "background", "primary", "既襲封，明號令，以兵法勒諸部。始衣白窄衫，氈冠紅裏，冠頂後垂紅結綬，自號嵬名吾祖。"),
            ev("宋史", "夏国传上", "text-wikisource-3e7bdfe7ebf23c85d890", "列传/卷四百八十五#p66",
               "process", "primary", "宋寶元元年……遂築壇受冊，即皇帝位，時年三十。"),
            ev("宋史", "夏国传上", "text-wikisource-1baf68638ec0ef28a5da", "列传/卷四百八十五#p68",
               "result", "primary", "遂以十月十一日郊壇備禮，為世祖始文本武興法建禮仁孝皇帝，國稱大夏，年號天授禮法延祚。……許以西郊之地，冊為南面之君。"),
            ev("宋史", "夏国传上", "text-wikisource-923daddd9f5888878759", "列传/卷四百八十五#p69",
               "impact", "primary", "詔削奪官爵、互市，揭榜于邊，募人能擒元昊若斬首獻者，即為定難軍節度使。"),
            ev("宋史", "夏国传上", "text-wikisource-d56a33d10b62b88bbcb9", "列传/卷四百八十五#p70",
               "impact", "supporting", "破安遠、塞門、永平諸砦，圍延州，設伏三川口，執劉平、石元孫、傅偃、劉發、石遜等。"),
        ],
    },
    "modern/event-qiqishi-bian.yml": {
        "background_zh_cn": "中国「外求和平、内求统一」，国民政府外交政策主张对内求自存、对外求共存，近两年对日外交一秉此旨；其时东四省失陷已六年，继有塘沽协定，冲突地点已至北平门口的卢沟桥。",
        "process_zh_cn": "卢沟桥事变发生后，日方舆论与外交直接间接表示显露事变征兆，并传播扩大塘沽协定范围、扩大冀东伪组织、驱逐第二十九军、逼迫宋哲元离开等传闻——「这一次的事件，并不是偶然的」。",
        "result_zh_cn": "国民政府确定始终一贯的方针和立场：「我们希望和平，而不求苟安；准备应战，而决不求战」；「万一真到了无可避免的最后关头，我们当然只有牺牲，只有抗战」。",
        "impact_zh_cn": "「如果战端一开，那就是地无分南北，年无分老幼，无论何人，皆有守土抗战之责任，皆应抱定牺牲一切之决心」——最后关头的抗战宣言昭告中外，成为全国抗战动员的标志性文告。",
        "people": [
            {"person_name_raw": "蒋中正", "role": "monarch", "link_status": "needs_linking",
             "role_zh_cn": "庐山谈话发表者：宣示应战而不求战的方针与最后关头立场",
             "review_note": "batch02-10：對盧溝橋事件之嚴正聲明 页首署「蔣中正」；行文以「政府」立场宣示", "person_id": None},
            {"person_name_raw": "宋哲元", "role": "opponent", "link_status": "needs_linking",
             "role_zh_cn": "第二十九军将领；日方传闻逼迫其离开，为事变征兆之一",
             "review_note": "batch02-10：對盧溝橋事件之嚴正聲明「要驅逐第二十九軍，要逼迫宋哲元離開」", "person_id": None},
        ],
        "places": [
            {"place_name_raw": "卢沟桥", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "事变爆发地：声明称「现在冲突地点已到了北平门口的卢沟桥」",
             "review_note": "batch02-10：對盧溝橋事件之嚴正聲明「現在沖突地點已到了北平門口的盧溝橋」"},
            {"place_name_raw": "北平", "role": "city", "link_status": "needs_linking", "sequence": 2,
             "description_zh_cn": "声明称其为百年故都、北方政治文化中心与军事重镇",
             "review_note": "batch02-10：對盧溝橋事件之嚴正聲明「我們百年故都，北方政治文化的中心與軍事重鎮的北平」"},
            {"place_name_raw": "冀东", "role": "region", "link_status": "needs_linking", "sequence": 3,
             "description_zh_cn": "日方谋扩大伪组织之地（冀东伪组织）",
             "review_note": "batch02-10：對盧溝橋事件之嚴正聲明「要擴大冀東偽組織」"},
        ],
        "evidence": [
            ev("對盧溝橋事件之嚴正聲明", "廬山談話·民國二十六年七月十七日", "text-wikisource-b80b143e5db4453fe552",
               "對盧溝橋事件之嚴正聲明#p3", "background", "primary",
               "中國民族本是酷愛和平，國民政府的外交政策，向來主張對內求自存，對外求共存。"),
            ev("對盧溝橋事件之嚴正聲明", "廬山談話·民國二十六年七月十七日", "text-wikisource-4e48620507c7d3133118",
               "對盧溝橋事件之嚴正聲明#p4", "process", "primary",
               "可想見這一次的事件，並不是偶然的。……現在沖突地點已到了北平門口的盧溝橋。"),
            ev("對盧溝橋事件之嚴正聲明", "廬山談話·民國二十六年七月十七日", "text-wikisource-2dc70a86512dd928c9b9",
               "對盧溝橋事件之嚴正聲明#p5", "result", "primary",
               "萬一真到了無可避免的最後關頭，我們當然只有犧牲，只有抗戰！但我們的態度祗是應戰，而不是求戰。"),
            ev("對盧溝橋事件之嚴正聲明", "廬山談話·民國二十六年七月十七日", "text-wikisource-a62b07668ccd00525245",
               "對盧溝橋事件之嚴正聲明#p12", "impact", "primary",
               "如果戰端一開，那就是地無分南北，年無分老幼，無論何人，皆有守土抗戰之責任，皆應抱定犧牲一切之決心。"),
        ],
    },
    "modern/event-riben-touxiang.yml": {
        "background_zh_cn": "日本天皇、日本政府及大本营之代表接受美、中、英三国政府首领一九四五年七月二十六日在波茨坦所发表、其后经苏联加入之公告条款；中英美苏四国在文件中被称为盟邦。",
        "process_zh_cn": "「余等兹宣布：日本大本营与所有日本军队及所有在日人管制下的军队，无论在任何地点，向盟邦无条件投降」；并命令各地日军立即停止敌对行动、保存船舶航空器及军民财产，令大本营立即对各地部队司令官发布无条件投降命令。",
        "result_zh_cn": "命令所有民政及陆海军官员遵照盟邦统帅的公告命令与指示、各留岗位继续执行非战斗职务；宣布「天皇与日本政府统治国家之权力，应听命于盟邦统帅」，日本政府及其继承者担任忠实执行波茨坦宣言各项条款。",
        "impact_zh_cn": "文书载明「签字于一九四五年九月二日九时四分在日本东京湾」；由日本代表重光葵、梅津美治郎与盟邦统帅麦克阿瑟及美、中、英、苏等各国代表签署——中国代表徐永昌列名，日本帝国大本营及所有军队向盟邦无条件投降。",
        "people": [
            {"person_name_raw": "徐永昌", "role": "envoy", "link_status": "needs_linking",
             "role_zh_cn": "中华民国代表：在投降书上列名签署",
             "review_note": "batch02-10：降伏文書签署栏「徐永昌／中華民國代表」", "person_id": None},
            {"person_name_raw": "重光葵", "role": "envoy", "link_status": "needs_linking",
             "role_zh_cn": "日本代表：奉日本天皇与政府之命签署",
             "review_note": "batch02-10：降伏文書「重光葵／奉日本天皇與日本政府之命及代表天皇與日本政府」", "person_id": None},
            {"person_name_raw": "梅津美治郎", "role": "envoy", "link_status": "needs_linking",
             "role_zh_cn": "日本大本营代表：奉大本营之命签署",
             "review_note": "batch02-10：降伏文書「梅津美治郎／奉日本帝國大本營之命及代表日本帝國大本營」", "person_id": None},
            {"person_name_raw": "麦克阿瑟", "role": "envoy", "link_status": "needs_linking",
             "role_zh_cn": "盟邦统帅：代表对日作战联合国家接受投降",
             "review_note": "batch02-10：降伏文書「道格拉斯·麥克阿瑟／盟邦統帥」", "person_id": None},
        ],
        "places": [
            {"place_name_raw": "东京湾", "role": "location", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "投降书签署地（一九四五年九月二日九时四分）",
             "review_note": "batch02-10：降伏文書「簽字於一九四五年九月二日九時四分在日本東京灣」"},
        ],
        "evidence": [
            ev("降伏文書", "投降书全文", "text-wikisource-2ce5a293173a14e2ae5b", "降伏文書#p1",
               "background", "primary",
               "茲接受美、中、英三國政府首領於一九四五年七月二十六日在波茨坦所發表，其後又經蘇維埃社會主義共和國聯邦所加入之公告所列舉之條款。"),
            ev("降伏文書", "投降书全文", "text-wikisource-095b793c99a08b5fa677", "降伏文書#p2",
               "process", "primary",
               "日本大本營與所有日本軍隊及所有在日人管制下的軍隊，無論在任何地點，向盟邦無條件投降。"),
            ev("降伏文書", "投降书全文", "text-wikisource-31401a96815b1e61e9a1", "降伏文書#p8",
               "result", "primary",
               "天皇與日本政府統治國家之權力，應聽命於盟邦統帥。盟邦統帥可採取其所認為適當之各項步驟，以實施此等投降。"),
            ev("降伏文書", "投降书全文", "text-wikisource-49400a72c7628d9f430b", "降伏文書#p9",
               "impact", "primary",
               "簽字於一九四五年九月二日九時四分在日本東京灣。"),
            ev("降伏文書", "投降书全文", "text-wikisource-5bae458d14531153a579", "降伏文書#p19",
               "impact", "supporting", "徐永昌／中華民國代表。"),
            ev("降伏文書", "投降书全文", "text-wikisource-447bd6a16a22b10a3050", "降伏文書#p7",
               "result", "supporting",
               "余等茲命令日本帝國政府與日本帝國大本營，立即釋放現在日本管制下之所有盟國戰俘，與拘留之僑民。"),
        ],
    },
    "modern/event-nanjing-datusha.yml": {
        "background_zh_cn": "日军以南京为抗战中心，纠集第六师团谷寿夫部队、第十六师团中岛部队、第十八师团牛岛部队、第一一四师团末松部队等，在松井石根指挥下会攻南京；因遭中国军队坚强抵抗，陷城后作有计划之屠杀以报复。",
        "process_zh_cn": "谷寿夫所率第六师团任前锋，一九三七年十二月十二日傍晚攻陷中华门，先头部队用绳梯攀垣而入，即开始屠杀；翌晨复率大军进城，与中岛、牛岛、末松等部分窜京市各区，展开大规模屠杀，继以焚烧抢掠；屠杀最惨厉时期为十二月十二日至二十一日。",
        "result_zh_cn": "判决认定：中华门外花神庙、石观音、小心桥、扫帚巷、正觉寺、方家山、宝塔桥、下关草鞋峡等处被集体杀戮及焚尸灭迹者达十九万人以上；中华门下码头、东岳庙、堆草卷、斩龙桥等处零星残杀、尸骸经慈善团体掩埋者达十五万人以上——被害总数达三十余万人；主文判处谷寿夫死刑。",
        "impact_zh_cn": "判决基于身历其境之证人及主持掩埋尸体者之具结证明认定事实，依海牙陆战规例、战时俘虏待遇公约、战争犯罪审判条例等作出——南京大屠杀经战后司法审判程序认定。",
        "people": [
            {"person_name_raw": "谷寿夫", "role": "opponent", "link_status": "needs_linking",
             "role_zh_cn": "日军第六师团长：纵兵屠杀、判处死刑",
             "review_note": "batch02-10：審字第壹號主文「共同縱兵屠殺俘虜及非戰鬥人員，並強奸、搶劫、破壞財產，處死刑」", "person_id": None},
            {"person_name_raw": "松井石根", "role": "opponent", "link_status": "needs_linking",
             "role_zh_cn": "日军大将：指挥会攻南京诸部队",
             "review_note": "batch02-10：審字第壹號事實段「在松井石根大將指揮之下，合理會攻」", "person_id": None},
            {"person_name_raw": "向井敏明", "role": "opponent", "link_status": "needs_linking",
             "role_zh_cn": "日军少尉：南京会攻期间屠杀竞赛，判处死刑",
             "review_note": "batch02-10：審字第十三號主文「共同連續屠殺俘虜及非戰鬥員，各處死刑」、理由段「以屠殺俘虜及非戰鬥人員為競賽娛樂」", "person_id": None},
            {"person_name_raw": "野田岩", "role": "opponent", "link_status": "needs_linking",
             "role_zh_cn": "日军副官：南京会攻期间屠杀竞赛，判处死刑",
             "review_note": "batch02-10：審字第十三號理由段「野田巖共殺百零五人，向井敏明則以殺百零六人獲勝」", "person_id": None},
        ],
        "places": [
            {"place_name_raw": "南京", "role": "city", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "大屠杀发生地：日军陷城后分窜京市各区屠杀",
             "review_note": "batch02-10：審字第壹號「分竄京市各區，展開大規模屠殺」"},
            {"place_name_raw": "中华门", "role": "battlesite", "link_status": "needs_linking", "sequence": 2,
             "description_zh_cn": "一九三七年十二月十二日傍晚被攻陷之城門，屠杀自此开始",
             "review_note": "batch02-10：審字第壹號「攻陷中華門，先頭部隊用繩梯攀垣而入，即開始屠殺」"},
            {"place_name_raw": "下关草鞋峡", "role": "battlesite", "link_status": "needs_linking", "sequence": 3,
             "description_zh_cn": "集体杀戮及焚尸灭迹处之一（十九万人以上统计所含处所）",
             "review_note": "batch02-10：審字第壹號理由段「下關草鞋峽等處，慘遭集體殺戮及焚屍滅跡者，達十九萬人以上」"},
        ],
        "evidence": [
            ev("國防部審判戰犯軍事法庭判決三十六年度審字第壹號", "谷寿夫案判决书", "text-wikisource-62258a5dee4860b73b55",
               "審字第壹號#p6", "background", "primary",
               "日本軍閥以我首都為抗戰中心，逐糾集其精銳而兇殘之第六師團谷壽夫部隊……乃於陷城後，作有計劃之屠殺。"),
            ev("國防部審判戰犯軍事法庭判決三十六年度審字第壹號", "谷寿夫案判决书", "text-wikisource-aef86c6ae58710010571",
               "審字第壹號#p7", "process", "primary",
               "血戰四晝夜，始於是年十二月十二日傍晚，由中用繩梯攀垣而入。翌晨率大隊進城，留駐一旬。"),
            ev("國防部審判戰犯軍事法庭判決三十六年度審字第壹號", "谷寿夫案判决书", "text-wikisource-aef86c6ae58710010571",
               "審字第壹號#p7", "result", "primary",
               "慘遭集體殺戮及焚屍滅跡者，達十九萬人以上。……被害總數達三十余萬人。"),
            ev("國防部審判戰犯軍事法庭判決三十六年度審字第壹號", "谷寿夫案判决书", "text-wikisource-bd2dc5ba1767dfe9c339",
               "審字第壹號#p8", "impact", "primary",
               "據上論結，應依刑事訴訟法第二百九十一條前段；海牙陸戰規例第四條第二項……判決如主文。"),
            ev("國防部審判戰犯軍事法庭判決三十六年度審字第十三號", "百人斩案判决书", "text-wikisource-a56cc96988311ef2c20d",
               "審字第十三號#p7", "result", "supporting",
               "向井敏明、野田巖、田中軍吉，在作戰期間，共同連續屠殺俘虜及非戰鬥員，各處死刑。"),
        ],
    },
    "modern/event-xinzhongguo-chengli.yml": {
        "background_zh_cn": "公告称：自蒋介石国民党反动派政府背叛祖国、勾结帝国主义、发动反革命战争以来，全国人民处于水深火热之中；人民解放军在全国人民援助下英勇作战，消灭反动军队、推翻国民政府反动统治。",
        "process_zh_cn": "人民解放战争已取得基本胜利、全国大多数人民已获解放；由各民主党派、各人民团体、人民解放军、各地区、各民族、国外华侨及爱国民主分子代表组成的中国人民政治协商会议第一届全体会议集会，制定中央人民政府组织法，选举政府领导人。",
        "result_zh_cn": "组成中央人民政府委员会，宣告中华人民共和国的成立，并决定北京为首都；委员会本日在首都就职，接受共同纲领为施政方针，互选林伯渠为秘书长，任命周恩来为政务院总理兼外交部长、毛泽东为人民革命军事委员会主席、朱德为解放军总司令等。",
        "impact_zh_cn": "决议向各国政府宣布本政府为「代表中华人民共和国全国人民的唯一合法政府」；凡愿遵守平等、互利及互相尊重领土主权等项原则的任何外国政府，本政府均愿与之建立外交关系。",
        "people": [
            {"person_name_raw": "毛泽东", "role": "monarch", "link_status": "needs_linking",
             "role_zh_cn": "中央人民政府主席：公告署名发布者",
             "review_note": "batch02-10：中央人民政府公告「毛澤東爲中央人民政府主席」「中華人民共和國中央人民政府主席 毛澤東」", "person_id": None},
            {"person_name_raw": "周恩来", "role": "official", "link_status": "needs_linking",
             "role_zh_cn": "任命为政务院总理兼外交部长",
             "review_note": "batch02-10：中央人民政府公告「任命周恩來爲中央人民政府政務院總理兼外交部部長」", "person_id": None},
            {"person_name_raw": "朱德", "role": "official", "link_status": "needs_linking",
             "role_zh_cn": "任命为中国人民解放军总司令",
             "review_note": "batch02-10：中央人民政府公告「朱德爲人民解放軍總司令」", "person_id": None},
        ],
        "places": [
            {"place_name_raw": "北京", "role": "capital", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "公告决定为中华人民共和国首都",
             "review_note": "batch02-10：中央人民政府公告「決定北京爲中華人民共和國的首都」"},
        ],
        "evidence": [
            ev("中華人民共和國中央人民政府公告", "中央人民政府公告（1949-10-01）", "text-wikisource-7c93b903d48a44dc28c2",
               "中華人民共和國中央人民政府公告#p2", "background", "primary",
               "自蔣介石國民黨反動派政府背叛祖國，勾結帝國主義，發動反革命戰爭以來，全國人民處於水深火熱的情况之中。"),
            ev("中華人民共和國中央人民政府公告", "中央人民政府公告（1949-10-01）", "text-wikisource-5ef5f26343c14b2f1dc6",
               "中華人民共和國中央人民政府公告#p3", "process", "primary",
               "由全國各民主黨派、各人民團體、人民解放軍、各地區、各民族、國外華僑及其他愛國民主分子的代表們所組成的中國人民政治協商會議第一屆全體會議業已集會。"),
            ev("中華人民共和國中央人民政府公告", "中央人民政府公告（1949-10-01）", "text-wikisource-496b97f4f14864d4d4df",
               "中華人民共和國中央人民政府公告#p7", "result", "primary",
               "組成中央人民政府委員會，宣告中華人民共和國的成立，並決定北京爲中華人民共和國的首都。"),
            ev("中華人民共和國中央人民政府公告", "中央人民政府公告（1949-10-01）", "text-wikisource-d242dc10d927617ca6cd",
               "中華人民共和國中央人民政府公告#p8", "impact", "primary",
               "向各國政府宣佈，本政府爲代表中華人民共和國全國人民的唯一合法政府。凡願遵守平等、互利及互相尊重領土主權等項原則的任何外國政府，本政府均願與之建立外交關係。"),
            ev("中國人民政治協商會議共同綱領", "共同纲领（1949-09-29）", "text-wikisource-edece602696408e68ebf",
               "中國人民政治協商會議共同綱領#p1", "process", "supporting",
               "一九四九年九月二十九日中國人民政治協商會議第一屆全體會議通過。"),
        ],
    },
    "modern/event-wusi-yundong.yml": {
        "background_zh_cn": "宣言称：日本在巴黎和会要求并吞青岛、管理山东一切权利，「他们的外交，大胜利了。我们的外交，大失败了」——山东大势一去就是破坏中国领土，「中国的领土破坏，中国就要亡了」。",
        "process_zh_cn": "「所以我们学界，今天排队到各公使馆去，要求各国出来维持公理」；并号召「务望全国农工商各界，一律起来，设法开国民大会，外争主权，内除国贼」。",
        "result_zh_cn": "宣言向全国同胞立下两个信条：「中国的土地，可以征服，而不可以断送」「中国的人民，可以杀戮，而不可以低头」，末呼「国亡了，同胞起来呀！」。",
        "impact_zh_cn": "据罗家伦注：此宣言为五四当日唯一印刷品，由北大同学受托起草、罗执笔，写好即付印刷所印五万张（印成二万张分散）——「写时所凝结的却是大家的愿望和热情」，是五四当天学界向全国发出的公开呼吁。",
        "people": [
            {"person_name_raw": "罗家伦", "role": "author", "link_status": "needs_linking",
             "role_zh_cn": "《北京学界全体宣言》执笔者（时北京大学学生）",
             "review_note": "batch02-10：五四運動宣言页首署 author=羅家倫；页内罗注自述执笔经过", "person_id": None},
        ],
        "places": [
            {"place_name_raw": "青岛", "role": "city", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "和会交涉标的：日本要求并吞青岛、管理山东权利",
             "review_note": "batch02-10：五四運動宣言「現在日本在國際和會，要求並吞青島」"},
            {"place_name_raw": "北京", "role": "city", "link_status": "needs_linking", "sequence": 2,
             "description_zh_cn": "宣言执笔与印发地（汉花园北京大学新潮社）",
             "review_note": "batch02-10：五四運動宣言罗注「回到漢花園北京大學新潮社」"},
            {"place_name_raw": "山东", "role": "region", "link_status": "needs_linking", "sequence": 3,
             "description_zh_cn": "和会交涉标的：日本要求管理山东一切权利",
             "review_note": "batch02-10：五四運動宣言「管理山東一切權利」"},
        ],
        "evidence": [
            ev("五四運動宣言", "北京学界全体宣言（1919-05-04）", "text-wikisource-edf9e0d1fdd4bf8e571a",
               "五四運動宣言#p1", "background", "primary",
               "現在日本在國際和會，要求並吞青島，管理山東一切權利，就要成功了。……中國的領土破壞，中國就要亡了。"),
            ev("五四運動宣言", "北京学界全体宣言（1919-05-04）", "text-wikisource-edf9e0d1fdd4bf8e571a",
               "五四運動宣言#p1", "process", "primary",
               "所以我們學界，今天排隊到各公使館去，要求各國出來維持公理。務望全國農工商各界，一律起來，設法開國民大會，外爭主權，內除國賊。"),
            ev("五四運動宣言", "北京学界全体宣言（1919-05-04）", "text-wikisource-e59ce1051d6946e6c4a5",
               "五四運動宣言#p2", "result", "primary",
               "（一）中國的土地，可以征服，而不可以斷送。"),
            ev("五四運動宣言", "北京学界全体宣言（1919-05-04）", "text-wikisource-facceaf404161ca675d1",
               "五四運動宣言#p6", "impact", "primary",
               "這是五四那天唯一的印刷品。……寫時所凝結的卻是大家的願望和熱情。"),
            ev("五四運動宣言", "北京学界全体宣言（1919-05-04）", "text-wikisource-6981f991c91c978bc57e",
               "五四運動宣言#p3", "result", "supporting",
               "（二）中國的人民，可以殺戮，而不可以低頭。"),
        ],
    },
}


def main() -> int:
    for rel, block in BLOCKS.items():
        path = EVENTS / rel
        existing = yaml.safe_load(path.read_text())
        for key in ("background_zh_cn", "process_zh_cn", "result_zh_cn", "impact_zh_cn",
                    "people", "places", "evidence"):
            if existing.get(key):
                print(f"SKIP {rel}: already has {key}")
                return 1
        appended = yaml.safe_dump(block, allow_unicode=True, sort_keys=False,
                                  default_flow_style=False, width=10**6)
        with path.open("a", encoding="utf-8") as stream:
            stream.write("\n" + appended)
        print(f"appended {rel}: {list(block)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
