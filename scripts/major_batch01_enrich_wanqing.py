"""Source Batch 02 · 晚清/清初 enrichment（10 事件）——major/长任务 Phase C。

清史稿（清史稿/卷N，work-curated-qingshigao）逐段锚定；顺带把 4 条 needs_linking 的
清史稿行重定位（Queue 11 同法：章节+内容双核实 + 逐字引文）。
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
EVENTS = ROOT / "data" / "curated" / "history_backbone" / "events"


def ev(book_anchor, tid, field, role, quote, note=""):
    return {
        "work": "清史稿", "term": book_anchor.split("#")[0].split("/")[-1],
        "historical_text_id": tid, "chapter_anchor": book_anchor,
        "claim_field": field, "evidence_role": role, "link_status": "linked",
        "link_method": "manual", "link_confidence": 1.0, "link_quality_status": "reviewed",
        "context_keywords": [],
        "review_note": f"source-batch02：清史稿源（wikisource/20260912b）引文：「{quote}」；"
                       f"claim_field={field}；anchor=段落精确锚。{note}",
    }


BLOCKS: dict[str, dict] = {
    # ---------------------------------------------------------------- 清初
    "qing/event-huangtaiji-jiwei.yml": {
        "background_zh_cn": "太祖崩，储嗣未定；大贝勒代善与其子岳託、萨哈廉以上才德冠世，与诸贝勒议请嗣位，上辞再三，久之乃许。",
        "process_zh_cn": "丙寅九月庚午朔，皇太极即位于沈阳，诏以明年为天聪元年——后金汗位由诸贝勒公议推举完成交接。",
        "result_zh_cn": "即位之初即行使汗权：以蒙古喀尔喀札鲁特部败盟杀掠、私通于明，命大贝勒代善等率精兵万人讨之，先贻书声其罪。",
        "impact_zh_cn": "察哈尔阿喇克绰忒部贝勒巴尔巴图鲁等率众来归，蒙古诸部渐附——皇太极继位后后金对蒙古的整合与对明攻势自此展开。",
        "people": [
            {"person_name_raw": "代善", "role": "supporter", "link_status": "needs_linking",
             "role_zh_cn": "大贝勒：与诸贝勒议请皇太极嗣位",
             "review_note": "source-batch02：清史稿·太宗本纪一「代善与其子岳託、薩哈廉以上才德冠世，与諸貝勒議請嗣位」", "person_id": None},
        ],
        "places": [
            {"place_name_raw": "沈阳", "role": "capital", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "皇太极即位地（盛京）",
             "review_note": "source-batch02：清史稿·太宗本纪一「丙寅九月庚午朔，即位於瀋陽」"},
        ],
        "evidence": [
            ev("本纪/太宗本纪一#p3", "text-wikisource-db127f638d1e94469a3f", "background", "primary",
               "太祖崩，儲嗣未定。代善与其子岳託、薩哈廉以上才德冠世，与諸貝勒議請嗣位。"),
            ev("本纪/太宗本纪一#p4", "text-wikisource-302ebbe020a25738a793", "process", "primary",
               "丙寅九月庚午朔，即位於瀋陽。"),
            ev("本纪/太宗本纪一#p6", "text-wikisource-290fc87e237abb5b773c", "result", "primary",
               "冬十月己酉，以蒙古喀爾喀札魯特部敗盟殺掠，私通於明，命大貝勒代善等率精兵萬人討之。"),
            ev("本纪/太宗本纪一#p16", "text-wikisource-3f3ce1a5458bf6878d4e", "impact", "primary",
               "察哈爾阿喇克綽忒部貝勒巴爾巴圖魯、諾门達賚、吹爾扎木蘇率眾来歸。"),
        ],
    },
    # ---------------------------------------------------------------- 三藩
    "qing/event-sanfan-zhi-luan.yml": {
        "process_zh_cn": "三桂反问至京师，清廷即日遣前锋统领硕岱驰镇荆州，命顺承郡王勒尔锦为宁南靖寇大将军率师讨三桂，并停撤平南、靖南二藩；三桂兵陷清浪卫、辰州。",
        "impact_zh_cn": "康熙十九年春清军全面反攻：赵良栋克成都、王进宝取汉中，王屏藩自杀，重庆、辰州相继下；次年进围云南会城，世璠诸将先后降，临安、姚安、大理、鹤庆、丽江诸府悉下——三藩之乱走向终结。",
        "places": [
            {"place_name_raw": "云南", "role": "region", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "吴三桂根据地；康熙二十年清军进攻云南会城",
             "review_note": "source-batch02：清史稿·吴三桂传「進攻云南会城，屯歸化寺」"},
            {"place_name_raw": "辰州", "role": "battlesite", "link_status": "needs_linking", "sequence": 2,
             "description_zh_cn": "三桂起兵初期攻陷之地",
             "review_note": "source-batch02：清史稿·吴三桂传「復進陷辰州」"},
        ],
        "evidence": [
            ev("列传/吴三桂传#p16", "text-wikisource-aec76627289976252839", "process", "primary",
               "三桂反問聞。上以荊州咽喉地，即日遣前鋒統領碩岱率禁旅馳赴鎮守。尋命順承郡王勒爾錦为寧南靖寇大將軍，率師討三桂。"),
            ev("列传/吴三桂传#p16", "text-wikisource-aec76627289976252839", "background", "primary",
               "十二月，黨務禮、薩穆哈至京師，三桂反問聞。", "与既有 background 字段互证"),
            ev("列传/吴三桂传#p26", "text-wikisource-32d10f0bff0d940e65a3", "result", "primary",
               "十九年春，將軍趙良棟自略陽破陽平关，克成都。……王屏籓走保寧……屏籓自殺。"),
            ev("列传/吴三桂传#p29", "text-wikisource-953fcee4fa215b89f714", "impact", "primary",
               "二月，進攻云南会城，屯歸化寺，世璠遣將胡国柄等將萬人为像陣拒战。……臨安、姚安、大理、鶴慶、麗江諸府悉下。"),
        ],
    },
    # ---------------------------------------------------------------- 鸦片战争
    "qing/event-diyici-yapian-zhanzheng.yml": {
        "process_zh_cn": "道光二十一年正月，英人寇广东虎门，副将陈连陞父子死之，虎门陷；清廷命奕山为靖逆将军督办广东海防，命讷尔经额驻天津督办海防。",
        "impact_zh_cn": "战争进程中林则徐、邓廷桢被遣戍伊犁，琦善逮问论斩——战后清廷将战败归咎主战与主和官员；道光二十二年七月英船寇江宁省城，耆英等与英方定约钤用御宝，是为江宁条约。",
        "people": [
            {"person_name_raw": "林则徐", "role": "official", "link_status": "needs_linking",
             "role_zh_cn": "钦差大臣/两广总督：禁烟主事者，战后遣戍伊犁",
             "review_note": "source-batch02：清史稿·宣宗本纪三「鄧廷楨、林則徐遣戍伊犁」", "person_id": None},
            {"person_name_raw": "关天培", "role": "opponent", "link_status": "needs_linking",
             "role_zh_cn": "广东水师提督：虎门之战殉国",
             "review_note": "source-batch02：清史稿·宣宗本纪三「琦善以虎门陷，下部嚴議，褫提督关天培頂戴」", "person_id": None},
            {"person_name_raw": "耆英", "role": "envoy", "link_status": "needs_linking",
             "role_zh_cn": "钦差大臣：办理江浙通商事宜、与英定约",
             "review_note": "source-batch02：清史稿·宣宗本纪三「命耆英为欽差大臣，辦理江浙通商事宜」", "person_id": None},
        ],
        "places": [
            {"place_name_raw": "虎门", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "英军进攻之广东海口要塞",
             "review_note": "source-batch02：清史稿·宣宗本纪三「英人寇廣东虎门」"},
            {"place_name_raw": "定海", "role": "battlesite", "link_status": "needs_linking", "sequence": 2,
             "description_zh_cn": "浙江海口，战争中被英军占据",
             "review_note": "source-batch02：清史稿·宣宗本纪三「英人去定海」"},
            {"place_name_raw": "江宁", "role": "city", "link_status": "needs_linking", "sequence": 3,
             "description_zh_cn": "江宁条约签订地（英船寇江宁省城后定约）",
             "review_note": "source-batch02：清史稿·宣宗本纪三「英船寇江寧省城。命伊里布等議款」"},
        ],
        "evidence": [
            ev("本纪/宣宗本纪二#p44", "text-wikisource-d464bb7af5f4236f0076", "background", "primary",
               "命盧坤等驅逐英吉利販鴉片躉船，勿任停泊。"),
            ev("本纪/宣宗本纪三#p1", "text-wikisource-421aba473b1da04d4475", "process", "primary",
               "二十一年春正月己丑，英人寇廣东虎门，副將陳連陛及其子舉鵬死之。……命奕山为靖逆將軍。"),
            ev("本纪/宣宗本纪三#p21", "text-wikisource-eb1f2b1a2c40bbedab46", "result", "primary",
               "秋七月甲寅，英船寇江寧省城。命伊里布等議款。……癸亥，耆英等請与英兵官定約，鈐御寶。"),
            ev("本纪/宣宗本纪三#p6", "text-wikisource-e7f45f82ff9959e2e480", "impact", "primary",
               "五月丙辰，英船入浙洋，命裕謙申嚴各海口兵備。癸亥，鄧廷楨、林則徐遣戍伊犁。"),
        ],
    },
    # ---------------------------------------------------------------- 金田起义
    "qing/event-jintian-qiyi.yml": {
        "background_zh_cn": "粤西岁饥多盗，湖南雷再浩、新宁李沅发复窜入为乱；洪秀全乘之，与杨秀清创立保良攻匪会，练兵筹饷，归附者益众。",
        "process_zh_cn": "是月，广东花县人洪秀全在广西桂平县金田起事——拜上帝会众团营举兵，太平天国运动由此发端。",
        "result_zh_cn": "起义后清廷调兵进剿：钦差大臣李星沅奏「剿贼金田获胜」，然乱势已成、官军未能扑灭。",
        "impact_zh_cn": "金田举兵迅速扩展为席卷长江的战争：石达开攻武昌，众号五十万，资粮军械尽置舟中，分两岸步骑夹行，进向九江、黄州——太平军由一隅起事发展为南北交争之势力。",
        "people": [
            {"person_name_raw": "洪秀全", "role": "monarch", "link_status": "needs_linking",
             "role_zh_cn": "拜上帝会首领：金田起事、建号太平天国",
             "review_note": "source-batch02：清史稿·文宗本纪「廣东花縣人洪秀全在廣西桂平縣金田起事」", "person_id": None},
            {"person_name_raw": "杨秀清", "role": "supporter", "link_status": "needs_linking",
             "role_zh_cn": "与洪秀全创立保良攻匪会、练兵筹饷",
             "review_note": "source-batch02：清史稿·洪秀全传「秀全乘之，与楊秀清創立保良攻匪会」", "person_id": None},
        ],
        "places": [
            {"place_name_raw": "金田", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "起义爆发地（广西桂平县金田村）",
             "review_note": "source-batch02：清史稿·文宗本纪「在廣西桂平縣金田起事」"},
            {"place_name_raw": "桂平", "role": "city", "link_status": "needs_linking", "sequence": 2,
             "description_zh_cn": "洪秀全、杨秀清传教团营之地",
             "review_note": "source-batch02：清史稿·洪秀全传「傳教至廣西，居桂平」"},
        ],
        "evidence": [
            ev("列传/洪秀全传#p2", "text-wikisource-19a5bc69f4cbd0c4056c", "background", "primary",
               "秀全乘之，与楊秀清創立保良攻匪会，練兵籌餉，歸附者益眾。"),
            ev("本纪/文宗本纪#p7", "text-wikisource-9ffe35cb659b50dcb6ca", "process", "primary",
               "是月，廣东花縣人洪秀全在廣西桂平縣金田起事。"),
            ev("本纪/文宗本纪#p16", "text-wikisource-def26983fd886ac81875", "result", "primary",
               "庚午，李星沅奏剿賊金田獲勝。"),
            ev("列传/洪秀全传#p8", "text-wikisource-c6a5226f335215dd1d28", "impact", "primary",
               "时石達開攻武昌……寇棄武昌駕船东下，眾号五十萬，資糧、軍械、子女、財帛盡置舟中，分兩岸步騎夾行。"),
        ],
    },
    # ---------------------------------------------------------------- 天京陷落
    "qing/event-tianjing-xianluo.yml": {
        "background_zh_cn": "金陵危急之际，洪秀全服毒死，群酋用上帝教殓法秘不发丧；其子年十六袭伪位（幼主）。",
        "process_zh_cn": "同治三年六月十六日，曾国荃饬诸军发太平门地雷，塌城垣二十余丈，总兵李臣典等先登，诸将分门合力攻克江宁省城。",
        "result_zh_cn": "城破后搜杀三日，毙寇十余万；清军搜掘洪秀全尸于伪宫，戮而焚之；李秀成及洪仁发、洪仁达被搜获，曾国藩亲讯后駢诛于市。",
        "impact_zh_cn": "幼主出走宁国、辗转被追获，洪仁玕等皆伏诛；史论谓太平天国「立国逾十余年，用兵至十余省……当时竭天下之力，始克平之，而元气遂已伤矣」——清朝虽平大乱而国力大损。",
        "people": [
            {"person_name_raw": "洪秀全", "role": "monarch", "link_status": "needs_linking",
             "role_zh_cn": "太平天国天王：金陵危急时服毒死，尸被掘戮",
             "review_note": "source-batch02：清史稿·洪秀全传「洪秀全以金陵危急，服毒死」「搜掘洪秀全屍於偽宮，戮而焚之」", "person_id": None},
            {"person_name_raw": "曾国荃", "role": "supporter", "link_status": "needs_linking",
             "role_zh_cn": "湘军统帅：督军用地雷破城、克江宁",
             "review_note": "source-batch02：清史稿·洪秀全传「国荃飭諸軍發太平门地雷」", "person_id": None},
            {"person_name_raw": "李秀成", "role": "opponent", "link_status": "needs_linking",
             "role_zh_cn": "太平天国忠王：城破后护幼主出走，被搜获诛杀",
             "review_note": "source-batch02：清史稿·洪秀全传「蕭孚泗搜獲李秀成……駢誅於市」", "person_id": None},
        ],
        "places": [
            {"place_name_raw": "金陵", "role": "capital", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "太平天国都城（江宁省城），同治三年被湘军攻克",
             "review_note": "source-batch02：清史稿·洪秀全传「攻克江寧省城」"},
        ],
        "evidence": [
            ev("列传/洪秀全传#p193", "text-wikisource-011de263adf638a8f64d", "background", "primary",
               "是月，洪秀全以金陵危急，服毒死。……其子年十六，襲偽位。"),
            ev("列传/洪秀全传#p196", "text-wikisource-d35d0ee601dd35dfbed8", "process", "primary",
               "六月十六日，国荃飭諸軍發太平门地雷，塌城垣二十餘丈……攻克江寧省城。"),
            ev("列传/洪秀全传#p196", "text-wikisource-d35d0ee601dd35dfbed8", "result", "primary",
               "搜殺三日，斃寇十餘萬……搜掘洪秀全屍於偽宮，戮而焚之。"),
            ev("列传/洪秀全传#p200", "text-wikisource-297e173b13dc22d1f440", "impact", "primary",
               "立国逾十餘年，用兵至十餘省，南北交爭，隱然敵国。當时竭天下之力，始克平之，而元氣遂已傷矣。"),
        ],
    },
    # ---------------------------------------------------------------- 戊戌变法
    "qing/event-wuxu-bianfa.yml": {
        "background_zh_cn": "光绪二十四年四月，恭亲王奕訢薨，荣禄授文渊阁大学士——变法前夜清廷中枢人事更迭；诏中外臣工当法恭忠亲王，各摅忠悃，共济时艰。",
        "process_zh_cn": "六月癸未朔诏改定科举新章，命康有为督办官报；五月曾诏自下科始乡会岁科各试改策论、陆军改练洋操——百日维新新政次第颁行。",
        "result_zh_cn": "八月丁亥，皇太后复垂帘于便殿训政；诏以康有为结党营私，新政中断（戊戌政变）。",
        "impact_zh_cn": "政变后缉捕不止：十一月再暴康有为、梁启超罪状，悬赏严捕；戊戌党籍至光绪三十年虽获特赦（除康、梁、孙文外），维新派自此流亡海外，清末政局转入保守与革命并行之局。",
        "people": [
            {"person_name_raw": "康有为", "role": "official", "link_status": "needs_linking",
             "role_zh_cn": "维新派领袖：督办官报、政变后遭通缉",
             "review_note": "source-batch02：清史稿·德宗本纪二「詔以康有为結黨營私」「命康有为督辦官報」", "person_id": None},
            {"person_name_raw": "梁启超", "role": "official", "link_status": "needs_linking",
             "role_zh_cn": "维新派：与康有为并列遭悬赏严捕",
             "review_note": "source-batch02：清史稿·德宗本纪二「再暴康有为、梁啟超罪狀，懸賞嚴捕」", "person_id": None},
            {"person_name_raw": "慈禧太后", "role": "monarch", "link_status": "needs_linking",
             "role_zh_cn": "皇太后：复垂帘训政，终结新政",
             "review_note": "source-batch02：清史稿·德宗本纪二「皇太后復垂簾於便殿訓政」", "person_id": None},
        ],
        "places": [
            {"place_name_raw": "京师", "role": "capital", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "百日维新与政变发生地",
             "review_note": "source-batch02：清史稿·德宗本纪二（光绪二十四年变法上谕与训政）"},
        ],
        "evidence": [
            ev("本纪/德宗本纪二#p46", "text-wikisource-b0565504f6faba773f3e", "background", "primary",
               "夏四月壬辰，恭親王奕訢薨……詔中外臣工當法恭忠親王，各攄忠悃，共濟时艱。"),
            ev("本纪/德宗本纪二#p48", "text-wikisource-670931eca6ba9c7189a4", "process", "primary",
               "六月癸未朔，詔改定科舉新章。……命康有为督辦官報。"),
            ev("本纪/德宗本纪二#p51", "text-wikisource-8dd85de04c2217bb2ba8", "result", "primary",
               "丁亥，皇太后復垂簾於便殿訓政。詔以康有为結黨營私。"),
            ev("本纪/德宗本纪二#p67", "text-wikisource-64250440032daa256046", "impact", "primary",
               "壬戌，再暴康有为、梁啟超罪狀，懸賞嚴捕。"),
        ],
    },
    # ---------------------------------------------------------------- 左宗棠西征
    "qing/event-zuozongtang-xizheng.yml": {
        "background_zh_cn": "海防与塞防之争：光绪元年宗棠既平关陇、将出关，论者多言自高宗定新疆岁糜数百万，宜徇英人议许帕夏自立为国称藩、罢西征专力海防，李鸿章言之尤力；宗棠力主规复新疆。",
        "process_zh_cn": "西征之饷糈筹措：宗棠虑各行省协饷不时至，请借外债；诏拨库款五百万、敕自借外国债五百万，并仿古屯田之法画兵农为二、简精壮为兵、散愿弱使屯垦。",
        "result_zh_cn": "出塞凡二十月，新疆南北城尽复——西征以节兵裕饷为本谋而竟全功。",
        "impact_zh_cn": "西征既成，宗棠条上新疆建行省事宜，并请与俄议还伊犁、交叛人二事；其平帕夏使外国对中国军力稍稍传说，新疆建省自此奠定西北版图。",
        "people": [
            {"person_name_raw": "左宗棠", "role": "official", "link_status": "needs_linking",
             "role_zh_cn": "钦差大臣/陕甘总督：西征主帅，收复新疆",
             "review_note": "source-batch02：清史稿·左宗棠传「出塞凡二十月，而新疆南北城盡复」", "person_id": None},
            {"person_name_raw": "李鸿章", "role": "opponent", "link_status": "needs_linking",
             "role_zh_cn": "北洋大臣：主张罢西征、专力海防",
             "review_note": "source-batch02：清史稿·左宗棠传「鴻章言之尤力」", "person_id": None},
        ],
        "places": [
            {"place_name_raw": "新疆", "role": "region", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "西征收复之地；战后奏请建行省",
             "review_note": "source-batch02：清史稿·左宗棠传「新疆南北城盡复」「條上新疆建行省事宜」"},
            {"place_name_raw": "伊犁", "role": "frontier", "link_status": "needs_linking", "sequence": 2,
             "description_zh_cn": "对俄交涉归还之地",
             "review_note": "source-batch02：清史稿·左宗棠传「請与俄議還伊犁」"},
        ],
        "evidence": [
            ev("列传/左宗棠传#p21", "text-wikisource-f30b2a4407d7984406ce", "background", "primary",
               "宜徇英人議，許帕夏自立为国稱籓，罷西征，專力海防。鴻章言之尤力。"),
            ev("列传/左宗棠传#p26", "text-wikisource-c94c1b5caf0fb7bfb622", "process", "primary",
               "始西征，慮各行省協助餉不时至，請一借貸外国。……为撥款五百萬，敕自借外国債五百萬。"),
            ev("列传/左宗棠传#p26", "text-wikisource-c94c1b5caf0fb7bfb622", "result", "primary",
               "出塞凡二十月，而新疆南北城盡复者，饋運饒給之力也。"),
            ev("列传/左宗棠传#p24", "text-wikisource-e71693b5db46e8dd0e6d", "impact", "primary",
               "四年正月，條上新疆建行省事宜，並請与俄議還伊犁、交叛人二事。"),
        ],
    },
    # ---------------------------------------------------------------- 武昌起义
    "qing/event-wuchang-qiyi.yml": {
        "process_zh_cn": "宣统三年八月甲寅，革命党谋乱于武昌事觉，捕三十二人；乙卯，武昌新军变附于革命党，总督瑞澂弃城走，遂陷武昌；丙辰，武昌军民拥陆军第二十一混成协统领官黎元洪称都督，置军政府。",
        "impact_zh_cn": "「嗣是行省各拥兵据地号独立，举为魁者皆称都督」——武昌首义后各省相继独立；清廷起用袁世凯为湖广总督、督办剿抚，并命陆军大臣荫昌督师往讨，然大势已去。",
        "people": [
            {"person_name_raw": "黎元洪", "role": "monarch", "link_status": "needs_linking",
             "role_zh_cn": "湖北新军协统：被拥为都督、置军政府",
             "review_note": "source-batch02：清史稿·宣统皇帝本纪「武昌軍民擁……黎元洪稱都督」", "person_id": None},
            {"person_name_raw": "瑞澂", "role": "official", "link_status": "needs_linking",
             "role_zh_cn": "湖广总督：弃城走，被夺职",
             "review_note": "source-batch02：清史稿·宣统皇帝本纪「總督瑞澂棄城走」", "person_id": None},
            {"person_name_raw": "荫昌", "role": "official", "link_status": "needs_linking",
             "role_zh_cn": "陆军大臣：奉命督师往讨武昌",
             "review_note": "source-batch02：清史稿·宣统皇帝本纪「命陸軍大臣蔭昌督師往討」", "person_id": None},
        ],
        "places": [
            {"place_name_raw": "武昌", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "首义爆发地：新军变、总督弃城",
             "review_note": "source-batch02：清史稿·宣统皇帝本纪「武昌新軍變附於革命黨……遂陷武昌」"},
            {"place_name_raw": "汉阳", "role": "battlesite", "link_status": "needs_linking", "sequence": 2,
             "description_zh_cn": "革命军攻取汉阳、袭兵工厂铁厂",
             "review_note": "source-batch02：清史稿·宣统皇帝本纪「革命軍取汉陽，襲兵工廠、鐵廠」"},
        ],
        "evidence": [
            ev("本纪/宣统皇帝本纪#p38", "text-wikisource-0ea03f6165e788ada18f", "process", "primary",
               "乙卯，武昌新軍變附於革命黨，總督瑞澂棄城走，遂陷武昌。……武昌軍民擁……黎元洪稱都督，置軍政府。"),
            ev("本纪/宣统皇帝本纪#p38", "text-wikisource-0ea03f6165e788ada18f", "background", "primary",
               "甲寅，革命黨謀亂於武昌，事覺，捕三十二人。", "与既有 background 字段互证"),
            ev("本纪/宣统皇帝本纪#p38", "text-wikisource-0ea03f6165e788ada18f", "result", "primary",
               "嗣是行省各擁兵據地号獨立，舉为魁者皆稱都督。", "与既有 result 字段互证"),
            ev("本纪/宣统皇帝本纪#p40", "text-wikisource-bcf2db4dde7b2748ac70", "impact", "primary",
               "戊戌，伍廷芳、張謇、唐文治、溫宗堯勸告攝政王，請贊共和政体。"),
        ],
    },
    # ---------------------------------------------------------------- 清帝退位
    "qing/event-qingdi-tuiwei.yml": {
        "process_zh_cn": "十二月己酉，皇太后懿旨授袁世凯全权与民军商酌条件奏闻；时岑春煊、袁树勋、陆徵祥、段祺瑞等请速定共和团体以免生灵涂炭，故不俟国会召集，决定自让政权。",
        "impact_zh_cn": "退位诏宣示：民军所开优礼条件——宗庙陵寝永远奉祀、先皇陵制如旧妥修——均已一律担承，「皇帝但卸政权，不废尊号」，并议定优待皇室八条、待遇皇族四条、待遇满蒙回藏七条；随后逊位。史论谓「大变既起，遽谢政权，天下为公，永存优待，遂开千古未有之奇」。",
        "people": [
            {"person_name_raw": "袁世凯", "role": "official", "link_status": "needs_linking",
             "role_zh_cn": "内阁总理大臣：受全权与民军商酌退位条件",
             "review_note": "source-batch02：清史稿·宣统皇帝本纪「授袁世凱全權，与民軍商酌條件奏聞」", "person_id": None},
            {"person_name_raw": "隆裕太后", "role": "monarch", "link_status": "needs_linking",
             "role_zh_cn": "皇太后：颁授全权、宣布逊位",
             "review_note": "source-batch02：清史稿·宣统皇帝本纪「皇太后懿旨」", "person_id": None},
            {"person_name_raw": "伍廷芳", "role": "envoy", "link_status": "needs_linking",
             "role_zh_cn": "南方代表：与袁世凯方议和",
             "review_note": "source-batch02：清史稿·宣统皇帝本纪「袁世凱奏与南方代表伍廷[芳]」", "person_id": None},
        ],
        "places": [
            {"place_name_raw": "京师", "role": "capital", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "清廷让政权、颁退位诏之地",
             "review_note": "source-batch02：清史稿·宣统皇帝本纪（宣统三年十二月逊位诏）"},
        ],
        "evidence": [
            ev("本纪/宣统皇帝本纪#p42", "text-wikisource-b8ccd18e57ccefc5bff1", "process", "primary",
               "己酉，皇太后懿旨，授袁世凱全權，与民軍商酌條件奏聞。……故不俟国会召集，決定自讓政權，遂有是命。"),
            ev("本纪/宣统皇帝本纪#p41", "text-wikisource-95515204c9bdd2230a76", "background", "primary",
               "壬申，皇太后命召集臨时国会。", "与既有 background 字段互证"),
            ev("本纪/宣统皇帝本纪#p42", "text-wikisource-b8ccd18e57ccefc5bff1", "result", "primary",
               "特飭內閣与民軍商酌優待皇室各條件，以期和平解決。……並議定優待皇室八條，待遇皇族四條，待遇滿、蒙、回、藏七條。……遂遜位。", "与既有 result 字段互证"),
            ev("本纪/宣统皇帝本纪#p43", "text-wikisource-f942d80357df34f7c3e0", "impact", "primary",
               "大變既起，遽謝政權，天下为公，永存優待，遂開千古未有之奇。"),
        ],
    },
    # ---------------------------------------------------------------- 甲午战争
    "qing/event-jiawu-zhanzheng.yml": {
        "process_zh_cn": "战争既起，清廷命吴大澂督军出关、以四川提督宋庆帮办北洋军务，发内帑三百万备军需；李鸿章以师久无功褫三眼孔雀翎、黄马褂。",
        "impact_zh_cn": "光绪二十一年三月日兵陷澎湖，李鸿章与日本全权伊藤博文、陆奥宗光马关会议，「和约成，定朝鲜为独立自主国，割辽南地、台湾、澎湖各岛，偿军费二万万」——甲午战败及马关条约后，列强租借纷至（是夏九龙半岛、威海卫俱租借于英吉利），瓜分危机日亟。",
        "people": [
            {"person_name_raw": "李鸿章", "role": "envoy", "link_status": "needs_linking",
             "role_zh_cn": "北洋大臣：马关议和全权大臣",
             "review_note": "source-batch02：清史稿·德宗本纪二「李鴻章与日本全權伊籐博文、陸奧宗光馬关会議」", "person_id": None},
            {"person_name_raw": "伊藤博文", "role": "envoy", "link_status": "needs_linking",
             "role_zh_cn": "日本全权：马关会议日方代表",
             "review_note": "source-batch02：清史稿·德宗本纪二「与日本全權伊籐博文……」", "person_id": None},
            {"person_name_raw": "吴大澂", "role": "official", "link_status": "needs_linking",
             "role_zh_cn": "湖南巡抚：督军出关参战",
             "review_note": "source-batch02：清史稿·德宗本纪一「吳大澂督軍出关」", "person_id": None},
        ],
        "places": [
            {"place_name_raw": "澎湖", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
             "description_zh_cn": "马关条约割让岛屿之一；战末被日军攻陷",
             "review_note": "source-batch02：清史稿·德宗本纪二「日兵陷澎湖……割遼南地、台灣、澎湖各島」"},
            {"place_name_raw": "威海卫", "role": "battlesite", "link_status": "needs_linking", "sequence": 2,
             "description_zh_cn": "北洋海军基地；战后租借于英",
             "review_note": "source-batch02：清史稿·德宗本纪二「山东威海衛俱租借於英吉利」"},
            {"place_name_raw": "台湾", "role": "region", "link_status": "needs_linking", "sequence": 3,
             "description_zh_cn": "马关条约割让之地",
             "review_note": "source-batch02：清史稿·德宗本纪二「割遼南地、台灣、澎湖各島」"},
        ],
        "evidence": [
            ev("本纪/德宗本纪一#p271", "text-wikisource-2be07e4500c8e5620bd0", "process", "primary",
               "八月丙午，吳大澂督軍出关……李鴻章以師久無功，褫三眼孔雀翎、黃馬褂。……懿旨發內帑三百萬備軍需。"),
            ev("本纪/德宗本纪二#p3", "text-wikisource-ce5e323dd28ebe397b81", "result", "primary",
               "三月壬申朔……日兵陷澎湖。……李鴻章与日本全權伊籐博文、陸奧宗光馬关会議。和約成，定朝鮮为獨立自主国，割遼南地、台灣、澎湖各島，償軍費二萬[萬兩]。"),
            ev("本纪/德宗本纪二#p49", "text-wikisource-998f346c3886e60c096e", "impact", "primary",
               "是夏，廣东九龍半島、山东威海衛俱租借於英吉利。"),
        ],
    },
}

# needs_linking 行的清史稿重定位（Queue 11 同法）
RECOVERY: dict[str, list[dict]] = {
    "event-sanfan-zhi-luan": [{"work": "清史稿", "term": "吴三桂传", "tid": "text-wikisource-aec76627289976252839",
        "anchor": "列传/吴三桂传#p16", "quote": "三桂反問聞。上以荊州咽喉地，即日遣前鋒統領碩岱率禁旅馳赴鎮守。"}],
    "event-jiawu-zhanzheng": [{"work": "清史稿", "term": "德宗本纪", "tid": "text-wikisource-ce5e323dd28ebe397b81",
        "anchor": "本纪/德宗本纪二#p3", "quote": "李鴻章与日本全權伊籐博文、陸奧宗光馬关会議。和約成……"}],
    "event-wuchang-qiyi": [{"work": "清史稿", "term": "宣统本纪", "tid": "text-wikisource-0ea03f6165e788ada18f",
        "anchor": "本纪/宣统皇帝本纪#p38", "quote": "乙卯，武昌新軍變附於革命黨，總督瑞澂棄城走，遂陷武昌。"}],
    "event-qingdi-tuiwei": [{"work": "清史稿", "term": "宣统本纪", "tid": "text-wikisource-b8ccd18e57ccefc5bff1",
        "anchor": "本纪/宣统皇帝本纪#p42", "quote": "皇太后懿旨，授袁世凱全權，与民軍商酌條件奏聞……遂遜位。"}],
}


def apply_recovery() -> int:
    import sys as _sys
    _sys.path.insert(0, str(ROOT / "src"))
    from history_data_pipeline.backbone.evidence_link import _load_event_yaml
    changed = 0
    for eid, rows in RECOVERY.items():
        for path in EVENTS.rglob(f"{eid}.yml"):
            doc, (head, tail) = _load_event_yaml(path)
            dirty = False
            for e in doc.get("evidence") or []:
                if e.get("link_status") != "needs_linking":
                    continue
                for r in rows:
                    if e.get("work") == r["work"] and r["term"] in (e.get("term") or ""):
                        e["historical_text_id"] = r["tid"]
                        e["chapter_anchor"] = r["anchor"]
                        e["link_method"] = "manual"
                        e["link_status"] = "linked"
                        e["link_confidence"] = 0.9
                        e["link_quality_status"] = "reviewed"
                        e["review_note"] = (f"source-batch02：清史稿入库后重定位（章节+内容双核实）。"
                                            f"引文：「{r['quote']}」；anchor=段落精确锚。")
                        dirty = True
                        changed += 1
                        break
            if dirty:
                path.write_text(head + yaml.safe_dump(doc, allow_unicode=True, sort_keys=False,
                                                       default_flow_style=False, width=10**6) + tail,
                                encoding="utf-8")
    return changed


def main() -> int:
    applied = 0
    for rel, block in BLOCKS.items():
        path = EVENTS / rel
        existing = yaml.safe_load(path.read_text())
        if existing.get("process_zh_cn"):
            print(f"SKIP {rel}: already enriched (idempotent guard)")
            continue
        appended = yaml.safe_dump(block, allow_unicode=True, sort_keys=False,
                                  default_flow_style=False, width=10**6)
        with path.open("a", encoding="utf-8") as stream:
            stream.write("\n" + appended)
        applied += 1
        print(f"appended {rel}")
    recovered = apply_recovery()
    print(f"total appended: {applied} | needs_linking recovered: {recovered}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
