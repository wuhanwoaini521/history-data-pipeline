# -*- coding: utf-8 -*-
"""V2.3 agent-assisted formal review dataset (PART B: event-kunyang .. event-sima-yan)."""

from __future__ import annotations

REVIEW_B: dict[str, dict[str, tuple]] = {
    "event-kunyang-zhizhan": {
        "cbdb-person-339519": ("A", "ruler", "新",
            "王莽为新朝之主，遭围攻的昆阳所派覆灭新军主力，是昆阳破局的直接承担方。"),
    },
    "event-lanyu-an": {
        "cbdb-person-30148": ("A", "ruler", "明",
            "朱元璋以谋逆罪诛蓝玉、连坐功臣，为清洗案的最高决策者。"),
    },
    "event-li-zicheng-fazhan": {
        "cbdb-person-65627": ("A", "commander", "大顺(农民军)",
            "李自成转战陕豫湖广、据襄阳称王，为势力发展的主体统帅。"),
    },
    "event-li-zicheng-jian-dashun": {
        "cbdb-person-65627": ("A", "initiator", "大顺",
            "李自成西安称帝、建国大顺，为建国正主。"),
    },
    "event-likui-bianfa": {
        "ctext-person-692385": ("A", "ruler", "魏",
            "魏文侯任用李悝推行变法（尽地力、平籴、法经），为变法采行之君。"),
    },
    "event-linshi-yuefa": {
        "curated-person-sun-yat-sen": ("A", "ruler", "中华民国",
            "孙中山以临时大总统名义公布约法，为颁布之直接决策者（《孙中山全集》）。"),
    },
    "event-liubang-ru-guan": {
        "cbdb-person-16622": ("A", "commander", "汉",
            "刘邦率军自武关破入关中、兵至霸上，楚亡秦之主力一方主将。"),
    },
    "event-liubang-si": {
        "cbdb-person-16622": ("A", "ruler", "汉",
            "汉高祖崩于长乐宫，为事件自身的当事人。"),
    },
    "event-liubei-beng-zhugeliang": {
        "cbdb-person-25403": ("A", "political_leader", "蜀汉",
            "诸葛亮受遗诏辅政、专决军政，为后刘备时代实际执政者。"),
    },
    "event-longxing-beifa": {
        "ctext-person-46529": ("A", "ruler", "南宋",
            "宋孝宗起用张浚兴师北伐，是隆兴北伐的最高决策者。"),
    },
    "event-luoyang-xianshi": {
        "cbdb-person-31360": ("A", "commander", "汉赵(石勒)",
            "石勒率部攻克洛阳、俘晋怀帝，为洛阳陷落一事的直接统兵主帅。"),
    },
    "event-lv-meng-xi-jingzhou": {
        "cbdb-person-20609": ("A", "initiator", "吴",
            "孙权决策遣吕蒙袭取荆州，为「白衣渡江」的发起人与最高决策者。"),
    },
    "event-lvbu-baiwang": {
        "cbdb-person-30257": ("A", "commander", "魏",
            "曹操围攻下邳、破灭吕布，为讨灭之直接指挥者。"),
    },
    "event-lvlin-qiyi": {
        "cbdb-person-339519": ("A", "ruler", "新莽",
            "绿林军起义反新，王莽为被推翻之新朝皇帝（统治对象双方核心）。"),
    },
    "event-ming-feng-zhuzhuwang": {
        "cbdb-person-30148": ("A", "ruler", "明",
            "朱元璋分封诸子为王，为分藩政策的亲定者。"),
    },
    "event-ming-ping-yunnan": {
        "cbdb-person-66288": ("A", "commander", "明",
            "沐英率明军征讨云南、克昆明并续镇之，为平定战事主将。"),
    },
    "event-mongol-mie-jin": {
        "ctext-person-117475": ("A", "victim", "金",
            "金哀宗守蔡州而城破自缢，为亡国之君与事件当事人。"),
    },
    "event-muwang-xizheng": {
        "ctext-person-533410": ("A", "ruler", "周",
            "周穆王亲征犬戎、西巡，为「穆王西征」当事人（《竹书纪年》）。"),
    },
    "event-nanchang-qiyi": {
        "curated-person-zhou-enlai": ("A", "political_leader", "中国共产党",
            "周恩来为南昌起义核心领导（前委书记），直接决策并指挥起义。"),
    },
    "event-nanjing-linshi-zhengfu": {
        "curated-person-sun-yat-sen": ("A", "political_leader", "中华民国",
            "孙中山就任临时大总统、定都南京，为临时政府之首脑（《孙中山全集》）。"),
    },
    "event-nanpo-zhi-bian": {
        "cbdb-person-100386": ("A", "victim", "元",
            "元英宗在南坡被弑，为事件遇害的当事人（《元史·英宗纪》）。"),
    },
    "event-ningwang-zhi-luan": {
        "cbdb-person-67356": ("A", "initiator", "明",
            "宁王朱宸濠起兵叛乱，为事件发起者。"),
        "cbdb-person-30374": ("A", "commander", "明",
            "王守仁不待朝命募兵讨平宸濠，为平叛主帅。"),
    },
    "event-niu-li-dangzheng": {
        "cbdb-person-15161": ("A", "official", "唐",
            "李德裕为李党为首、久秉政权行政，是党争一方的核心人物。"),
        "cbdb-person-32054": ("A", "official", "唐",
            "牛僧孺为牛党主要代表之一，是党争另一方领军人物。"),
    },
    "event-nuerhachi-tongyi-nvzhen": {
        "cbdb-person-339768": ("A", "initiator", "建州(女真)",
            "努尔哈赤以「十三副遗甲」起兵、统一诸部，为统一事业的发起与统帅。"),
    },
    "event-qian-qin-mie-qian-yan": {
        "cbdb-person-31260": ("A", "victim", "前燕",
            "前燕主慕容暐被前秦所俘、国亡，为亡国当事人。"),
    },
    "event-qian-qin-wajie": {
        "cbdb-person-95217": ("A", "initiator", "后燕",
            "慕容垂自立称燕而复重立国，为前秦瓦解自立诸势力的直接发起者之一。"),
    },
    "event-qian-yan-qiang": {
        "cbdb-person-402973": ("A", "ruler", "前燕",
            "慕容儁续前燕入主中原，为前燕强盛期重要君主。"),
        "cbdb-person-17120": ("A", "initiator", "前燕",
            "慕容皝自称燕王建前燕，为开国奠基之自主者。"),
    },
    "event-qidahen": {
        "cbdb-person-339768": ("A", "initiator", "后金",
            "努尔哈赤以「七大恨」告天而对明宣战，为行为文武之主。"),
    },
    "event-qidan-mie-houjin": {
        "cbdb-person-43077": ("A", "initiator", "辽(契丹)",
            "耶律德光自将灭后晋、代国号大辽，为灭晋之主帅。"),
    },
    "event-qin-mie-dongzhou": {
        "ctext-person-703206": ("A", "victim", "周",
            "周赧王为末代周天子，秦灭东周视为周亡之当事人。"),
        "ctext-person-457718": ("A", "initiator", "秦",
            "秦昭襄王遣兵灭周（前256），为灭周之君。"),
    },
    "event-qin-mie-wei": {
        "ctext-person-187500": ("A", "victim", "魏",
            "魏王假开门出降，为秦灭魏之亡国当事主。"),
    },
    "event-qin-mie-yan": {
        "ctext-person-289019": ("A", "victim", "燕",
            "燕王喜徙居辽东后被秦俘，为燕亡当事人。"),
    },
    "event-qing-nanxia-jiangnan": {
        "cbdb-person-34792": ("A", "commander", "弘光(南明)",
            "史可法督战守扬州、城破殉难，为南明抗清之核心将领。"),
    },
    "event-qing-tongyi-taiwan": {
        "cbdb-person-56824": ("A", "commander", "清",
            "施琅督水师澎湖海战大破郑军并收台，为统一台湾直接主将。"),
    },
    "event-qingli-heyi": {
        "cbdb-person-339687": ("A", "ruler", "西夏",
            "李元昊为西夏国主，与宋议约定盟约并为受册之封伯，为缔约一方之首脑。"),
    },
    "event-qingli-xinzheng": {
        "cbdb-person-1762": ("R", "背景引用",
            "庆历新政系范仲淹主导（1043-44），王安石变法属多年后的熙宁新法，summary以「后之王安石变法」为远引，非本事件参与者。"),
        "cbdb-person-8043": ("A", "official", "北宋",
            "范仲淹参知政事提「十事」推行新政，为庆历新政首脑与主要推手。"),
    },
    "event-qinmu-gong-ba-xirong": {
        "cbdb-person-134960": ("A", "official", "秦",
            "百里奚辅秦穆公理政、与蹇叔共佐，为秦治西戎重臣。"),
        "ctext-person-629332": ("A", "ruler", "秦",
            "秦穆公开地称霸西戎，荆艮称霸西戎之君（《史记·秦本纪》）。"),
    },
    "event-qiushou-qiyi": {
        "curated-person-mao-zedong": ("A", "initiator", "中国共产党",
            "毛泽东在湘赣边境领导秋收起义，为起义的直接发动领导人。"),
    },
    "event-quanrong-mie-xizhou": {
        "ctext-person-382372": ("A", "victim", "西周",
            "周幽王被铂宫破镐京所杀，为西周亡国之君。"),
    },
    "event-ran-wei": {
        "cbdb-person-31362": ("R", "背景引用",
            "summary「石虎死后诸子争立」之背景语，石虎已死、非冉魏建立之直接参与者。"),
    },
    "event-sanchuankou-zhizhan": {
        "cbdb-person-339687": ("A", "commander", "西夏",
            "李元昊攻宋延州、三川口之战败宋军，为其亲军之主帅。"),
    },
    "event-sanfan-xingcheng": {
        "cbdb-person-59135": ("A", "ruler", "广东藩王",
            "尚可喜镇守两广，为三藩局面形成一藩之主。"),
        "cbdb-person-65757": ("A", "ruler", "福建藩王",
            "耿精忠镇闽、承袭勇忠王位，为三藩局面相关方之一。"),
    },
    "event-sanjian-zhiluan": {
        "ctext-person-263104": ("A", "initiator", "周",
            "周公旦摄政平管蔡武庚之乱，为平乱与当政的主角。"),
    },
    "event-shangyang-bianfa": {
        "ctext-person-179465": ("A", "ruler", "秦",
            "秦孝公任用商鞅变法，为变法支持与拍板之君。"),
    },
    "event-shanxi-minbian": {
        "cbdb-person-65627": ("A", "participant", "农民军",
            "李自成为中国农民军，聚众起事，直接参与陕西民变扩大。"),
        "cbdb-person-438099": ("A", "initiator", "农民军",
            "高迎祥为明朝末年农民军早期首领（闯王先导），常事参与本变事。"),
    },
    "event-shi-jingtang-dai-tang": {
        "cbdb-person-339657": ("A", "initiator", "后晋",
            "石敬瑭引契丹兵灭后唐而定国后，为代唐自立之主。"),
        "cbdb-person-43077": ("A", "ruler", "辽(契丹)",
            "耶律德光大封，出兵助其灭唐，为「儿皇帝」所依之强援君主。"),
    },
    "event-shi-le-hou-zhao": {
        "cbdb-person-31360": ("A", "initiator", "后赵",
            "石勒自置赵王建国后赵、都襄国，为独立建国之主。"),
    },
    "event-sima-yan-dai-wei": {
        "ctext-person-138323": ("A", "ruler", "魏",
            "魏元帝被迫禅位于司马炎，为「以晋代魏」的被禅让当事人。"),
    },
}