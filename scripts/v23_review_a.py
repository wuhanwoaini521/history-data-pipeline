# -*- coding: utf-8 -*-
"""V2.3 agent-assisted formal review dataset (PART A: event-agubo .. event-kuiqiu).

Entry: event_id -> { person_id: ("A", role, side, event_evidence) | ("R", category, reason) | ("I", reason) }
Review method = agent_assisted_source_review (curated_accepted; NOT human_verified).
Engine: scripts/v23_major_person_formal_review.py
"""

from __future__ import annotations

REVIEW_A: dict[str, dict[str, tuple]] = {
    "event-agubo-geju": {
        "cbdb-person-54964": ("R", "背景引用",
            "summary 仅以「为左宗棠西征的背景」作铺垫；阿古柏割据期间左宗棠未直接参与，收复新疆另立事件 event-zuozongtang-xizheng。"),
    },
    "event-anlu-changan-recapture": {
        "cbdb-person-94373": ("A", "commander", "唐",
            "郭子仪组织反攻并指挥收复长安，为该役直接军事主导者（《旧唐书·郭子仪传》）。"),
    },
    "event-anlu-shi-siming": {
        "cbdb-person-32814": ("A", "initiator", "燕(叛军)",
            "史思明杀安庆绪后重举叛旗南下，是第二次叛乱阶段的直接发动者与统帅。"),
        "cbdb-person-379873": ("R", "背景引用",
            "安禄山此前（757）已死，本事件为史思明再叛阶段，安禄山仅属背景叙述人物。"),
    },
    "event-anlu-three-frontiers": {
        "cbdb-person-379873": ("A", "ruler", "范阳·河东·平卢",
            "安禄山本人兼领三镇、蓄兵自重，所领兵权即本事件核心事实。"),
    },
    "event-anlu-uprising": {
        "cbdb-person-379873": ("A", "initiator", "范阳",
            "安禄山自范阳起兵叛乱，是安史之乱的直接发动者与首叛统帅。"),
    },
    "event-baguo-lianjun-ru-jing": {
        "curated-person-cixi-taihou": ("A", "ruler", "清",
            "太后为朝政实际掌权者，战和抉择与西巡决策均由太后拍板，是庚子国难之当事君主。"),
    },
    "event-baideng-zhiwei": {
        "cbdb-person-16622": ("A", "ruler", "汉",
            "刘邦亲率汉军讨伐韩王信而被围白登，是事件的当事人与直接指挥方（《史记·匈奴列传》）。"),
    },
    "event-beiwei-jianguo": {
        "cbdb-person-31005": ("A", "initiator", "北魏",
            "拓跋珪重建代国、称帝建魏，为北魏开国主导者（《魏书·序纪》）。"),
    },
    "event-beiwei-mie-hou-yan": {
        "cbdb-person-17122": ("A", "official", "后燕",
            "慕容德为后燕宗室重臣，参合陂惨败后参与存亡决策，为后燕一方直接参与者。"),
        "cbdb-person-31005": ("A", "initiator", "北魏",
            "拓跋珪亲率魏军在参合陂大破后燕并乘势灭燕，为灭燕战争的发动者与总指挥。"),
    },
    "event-beiyang-haijun": {
        "cbdb-person-58649": ("A", "official", "清",
            "丁汝昌任北洋海军提督、统领舰队成军，是该事件的核心主持人（《清史稿》）。"),
    },
    "event-boju-zhizhan": {
        "ctext-person-6646198": ("A", "commander", "吴",
            "伍子胥辅佐阖闾运筹攻楚、与孙武分兵，为破楚入郢的重要策划与指挥者（《左传》定公四年）。"),
    },
    "event-caishi-zhizhan": {
        "cbdb-person-8170": ("A", "commander", "南宋",
            "虞允文以文臣代督军务、督战采石击退金军，是采石大捷的直接指挥者。"),
    },
    "event-cao-mao-zhisha": {
        "cbdb-person-30273": ("A", "victim", "魏",
            "曹髦亲率卫队机攻司马昭而被弑，是事件当事人与被杀目标（《三国志·魏书·三少帝纪》）。"),
    },
    "event-caocao-ying-xian-di": {
        "cbdb-person-30257": ("A", "ruler", "汉",
            "曹操迎汉献帝至许、奉天子以令诸侯，为该策的发起人与实际执行者。"),
    },
    "event-chanyuan-zhi-meng": {
        "ctext-person-983419": ("A", "ruler", "北宋",
            "宋真宗御驾亲征澶渊并抉择签订盟约，为澶渊之盟的直接决策皇帝。"),
    },
    "event-chenbaxian-jianzhen": {
        "ctext-person-427839": ("A", "ruler", "梁",
            "梁敬帝被迫禅位于陈霸先，是被禅让的末帝，名分交接的直接当事人。"),
    },
    "event-chengpu-zhizhan": {
        "ctext-person-928177": ("A", "ruler", "楚",
            "楚成王在位之楚军参与城濮会战战国，为楚方争霸的最高决策者（虽未亲征）。"),
    },
    "event-chenyouliang-dai-han": {
        "cbdb-person-30148": ("A", "ruler", "明",
            "朱元璋为最终击败陈友谅、取汉政权的追溯决策者与指挥者。"),
    },
    "event-chongqing-tanpan": {
        "curated-person-mao-zedong": ("A", "political_leader", "中华人民共和国",
            "毛泽东亲率代表团赴重庆、双方谈判后签订《双十协定》，为中共首席决策与一线代表。"),
    },
    "event-chongxi-zengbi": {
        "cbdb-person-628": ("A", "official", "北宋",
            "富弼两使辽邦完成重熙增币谈判（拒割地），为宋方主谈的直接执行者（《宋史·富弼传》）。"),
    },
    "event-chu-mie-yue": {
        "ctext-person-441859": ("A", "ruler", "楚",
            "楚威王在位时灭越、并吴越故地，为灭越之君（《史记·越王勾践世家》）。"),
    },
    "event-chuhan-han-foundation": {
        "cbdb-person-16622": ("A", "ruler", "汉",
            "刘邦称帝建汉，为汉朝创立的核心决策者与首位皇帝。"),
    },
    "event-chuhan-war": {
        "cbdb-person-16622": ("A", "commander", "汉",
            "刘邦在楚汉战争中为汉方最高决策者与总指挥（《史记·高祖本纪》）。"),
    },
    "event-chuwuwang-chengwang": {
        "ctext-person-514671": ("A", "ruler", "楚",
            "楚武王僭号称王，是楚始称王事件之主角与开王先例的决策者。"),
    },
    "event-daliyi": {
        "ctext-person-414147": ("A", "ruler", "明",
            "明世宗（嘉靖）以藩入继，亲决大礼议之争论与典礼，为事件核心决策者。"),
    },
    "event-dierci-zhifeng-zhanzheng": {
        "curated-person-sun-yat-sen": ("R", "背景引用",
            "事件主体为直奉再战与冯玉祥北京政变；孙中山系被邀请北上及随后的结局线索，未直接参与，参与证据不足。"),
    },
    "event-dongbei-yizhi": {
        "curated-person-zhang-xueliang": ("A", "initiator", "中华民国(东北)",
            "张教授1928年末宣布东北易帜、归顺中央，为易帜事件的拍板者与推动人。"),
    },
    "event-doujiande-shili": {
        "cbdb-person-134932": ("R", "背景引用",
            "summary 中王世充仅为「与窦建德鼎足而三」之对照，未直接参与窦建德据河北之军政。"),
    },
    "event-dujiangyan-xiuzhu": {
        "ctext-person-457718": ("A", "ruler", "秦",
            "秦昭襄王在秦皇地专赵豹下令组织李冰修筑都江堰，为秦国内组织地方建设的最高决策层。"),
    },
    "event-erci-geming": {
        "curated-person-sun-yat-sen": ("A", "initiator", "中华民国",
            "孙文等发动武装讨袁，为二次革命的发起人之一。"),
    },
    "event-fangguozhen-jiang": {
        "cbdb-person-30148": ("A", "ruler", "明",
            "朱元璋逼降方国珍一方，为决策逼降与受降的最高决策者。"),
    },
    "event-fu-jian-wangmeng": {
        "cbdb-person-31644": ("A", "victim", "前秦",
            "苻坚击杀暴虐的苻生而即位，苻生为被除之当事主（前秦天王位段）。"),
    },
    "event-fuyuan-zhi-zheng": {
        "cbdb-person-63908": ("A", "political_leader", "中华民国",
            "段祺瑞为国务院总理一方，召督军团压国会、与总统立遭免职冲突，是府院之争的主角之一。"),
        "cbdb-person-91349": ("A", "ruler", "中华民国",
            "黎元洪（总统）与段博弈并罢免总理，是府院之争另一核心当事人。"),
    },
    "event-fuzhou-chuanzheng": {
        "cbdb-person-54964": ("A", "official", "清",
            "左宗棠奏设并主持福州船政局，为洋务应急举措的主要主持人与决策者。"),
    },
    "event-gaiguohao-qing": {
        "cbdb-person-339769": ("A", "ruler", "清",
            "皇太极称帝、改国号大清并改族称满洲，即本事件正主（《清太宗实录》）。"),
    },
    "event-guan-dong-tao-dong": {
        "cbdb-person-30257": ("A", "official", "汉",
            "曹操为关东联军中亲率其部讨董卓的直接参与方将。"),
    },
    "event-guan-yu-bei-fa": {
        "cbdb-person-20609": ("R", "相邻事件",
            "孙权本人未参与关羽北伐；其发兵袭荆另属事件（吕蒙袭荆州），属相邻事件，不应并列。"),
        "cbdb-person-30257": ("A", "ruler", "曹魏",
            "曹操为关羽北伐之敌方最高决策者，遣于禁解围、拟迁都避锋，直接应对。"),
    },
    "event-guo-zixing-qibing": {
        "cbdb-person-30148": ("A", "participant", "红巾(濠州)",
            "朱元璋已投郭子兴部、参与濠州守，为直接参与者。"),
    },
    "event-guogong-fenlie-1927": {
        "curated-person-chiang-kai-shek": ("A", "initiator", "中华民国",
            "蒋介石发动上海「清党」、决断四一二武力除共，为国共分裂重要主导发起者。"),
    },
    "event-hai-shang-zhi-meng": {
        "curated-person-songhuizong": ("A", "ruler", "北宋",
            "徽宗君臣定策、遣使由海路赴金缔约，为缔结海上之盟的最终决策者（《宋史·徽宗纪》）。"),
    },
    "event-han-dingdu-changan": {
        "cbdb-person-16622": ("A", "ruler", "汉",
            "刘邦从师敬/张良议定都关中、营建长安，为定都之最终决策皇帝。"),
    },
    "event-han-liner-chengdi": {
        "cbdb-person-30148": ("R", "背景引用",
            "summary 「各地红巾（包括朱元璋部）名义上奉其正朔」仅为政治从属关系；朱元璋未直接参与韩林儿称帝，参与证据不足。"),
    },
    "event-hanchu-yixingwang": {
        "cbdb-person-16622": ("A", "ruler", "汉",
            "刘邦翦除变韩彭英等异姓侯王，为整饬之最高决策者。"),
        "cbdb-person-22437": ("A", "victim", "汉",
            "楚王韩信被夺王位废为淮阴侯，是剪除异姓王行动的当事受害者。"),
    },
    "event-handan-zhizhan": {
        "ctext-person-219287": ("A", "official", "楚",
            "楚春申君遣兵援赵以解邯郸之围，为援赵救困的直接执行者。"),
    },
    "event-hanwudi-caizheng": {
        "ctext-person-482249": ("A", "official", "汉",
            "桑弘羊主持均输平准与盐铁官营，是财政集权政策的直接主持臣僚。"),
    },
    "event-he-shuo-sanzhen": {
        "cbdb-person-146183": ("A", "ruler", "魏博镇",
            "田承嗣为首任魏博节度使，是「国中之国」割据格局的直接创立者。"),
    },
    "event-hongmen": {
        "cbdb-person-16622": ("A", "participant", "汉",
            "刘邦赴鸿门宴而复全身而退，是宴会当事人与核心人物。"),
    },
    "event-hou-shu-jianli": {
        "cbdb-person-18317": ("A", "initiator", "后蜀",
            "孟知祥成都称帝建立后蜀，为开国发起之主。"),
    },
    "event-hou-yan-jianli": {
        "cbdb-person-95217": ("A", "initiator", "后燕",
            "慕容垂称燕王、重建燕政权，为后燕开国之主。"),
    },
    "event-hou-zhao-bingqian-zhao": {
        "cbdb-person-31360": ("A", "initiator", "后赵",
            "石勒部署石虎攻灭前赵，本人以天王决军国者之全局。"),
        "cbdb-person-31362": ("A", "commander", "后赵",
            "石虎率军攻灭前赵、斩其主刘曜，是本役主帅。"),
    },
    "event-houjin-jianguo": {
        "cbdb-person-339768": ("A", "initiator", "后金",
            "努尔哈赤于赫图阿拉称汗、建元天命，为后金政权创建者与首汗。"),
    },
    "event-huangchao-ru-changan": {
        "ctext-person-249317": ("A", "ruler", "唐",
            "唐僖宗坐镇长安遭破城、窘迫西奔成都，是陷都之当事人。"),
    },
    "event-huangpu-junxiao": {
        "curated-person-zhou-enlai": ("A", "political_leader", "中华民国",
            "周恩来任黄埔军校政治部主任等职，是建校工作的核心参与者。"),
        "curated-person-chiang-kai-shek": ("A", "commander", "中华民国",
            "蒋介石任黄埔军校校长，主持建校与训练，是学校创办的主事人。"),
    },
    "event-huangtaiji-jiwei": {
        "cbdb-person-339768": ("A", "ruler", "后金",
            "努尔哈赤之卒是继统之直接前提，为事件背景核心人物。"),
        "cbdb-person-339769": ("A", "initiator", "后金",
            "皇太极在继汗位并改元，为本次继位之当事者。"),
    },
    "event-hufa-yundong": {
        "curated-person-sun-yat-sen": ("A", "political_leader", "中华民国",
            "孙中山南下发起护法、组织护法军政府，为事件发动与组织者。"),
        "cbdb-person-63908": ("A", "political_leader", "中华民国",
            "段祺瑞废弃临时约法、拒绝恢复国会，是护法运动直面的对手方核心。"),
    },
    "event-hulao-zhizhan": {
        "cbdb-person-134932": ("A", "ruler", "郑(洛阳)",
            "洛阳王世充被唐军围困，经虎牢决战而出降，是被击溃受降的当事人。"),
    },
    "event-jia-hou-gan-zheng": {
        "curated-person-jia-nanfeng": ("A", "initiator", "西晋",
            "贾南风联手楚王玮剪除杨骏擅政一涯，为政变与其专制干政的发起与当事人。"),
    },
    "event-jiangdu-bingbian": {
        "cbdb-person-173126": ("A", "initiator", "隋",
            "宇文化及帅骁果军弑隋炀帝，为江都兵变的直接发动者与主谋。"),
    },
    "event-jianwen-jiwei": {
        "cbdb-person-30150": ("A", "ruler", "明",
            "朱允炆以皇太孙即位，为建文朝新君，即位的当事人。"),
        "cbdb-person-30148": ("A", "ruler", "明",
            "建文帝即位系因朱元璋之死，崩殂为即位之直接前提与背景。"),
    },
    "event-jianwen-xuefan": {
        "cbdb-person-28093": ("A", "official", "明",
            "方孝孺为建文帝削藩计谋（皇帝谋侍讲），直接参与削藩决策。"),
    },
    "event-jianzhong-zhi-luan": {
        "cbdb-person-194619": ("A", "initiator", "秦帝(朱泚)",
            "朱泚被泾原兵拥立僭号秦帝，是建中之乱中占据长安皇权的主要反唐中心人物。"),
        "cbdb-person-191752": ("A", "participant", "成德镇",
            "王武俊为起兵反削藩的镇将之一（后称冀王），属建中之乱直接参与者。"),
    },
    "event-jin-qian-du-bian": {
        "ctext-person-364088": ("A", "ruler", "金",
            "金宣宗迫于蒙古军压力作出移都开封之决策，为迁都事件的直接拍板君主。"),
    },
    "event-jin-wudi-beng": {
        "curated-person-jia-nanfeng": ("R", "背景引用",
            "summary 仅以贾后为后续「埋下伏笔」之远引，其未直接参与晋武帝崩与惠帝即位，参与证据不足。"),
    },
    "event-jintian-qiyi": {
        "cbdb-person-65447": ("A", "initiator", "太平天国",
            "洪秀全在金田创团起事、自称天王，为金田起义直接发动者。"),
    },
    "event-kuiqiu-zhi-hui": {
        "ctext-person-773298": ("I",
            "周襄王仅遣使赐胙而未亲与会（「襄王亦遣使」），王亲自参与之证据不足。"),
    },
    "event-kaihuang-lv": {
        "ctext-person-803544": ("A", "ruler", "隋",
            "隋文帝命臣更定刑律、颁《开皇律》，是该法律事件的决定者。"),
    },
    "event-kaihuang-zhizhi": {
        "ctext-person-803544": ("A", "ruler", "隋",
            "隋文帝之在位与施策构成开皇之治，为治世之主（史称「开皇之治」概括）。"),
    },
    "event-kaiyuan-zhizheng": {
        "cbdb-person-31275": ("A", "official", "唐",
            "宋璟任相与其他群辅整饬朝政，为开元前期整顿的直接执政宰辅。"),
    },
}