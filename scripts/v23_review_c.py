# -*- coding: utf-8 -*-
"""V2.3 agent-assisted formal review dataset (PART C: event-song-mie-jingnan .. end)."""

from __future__ import annotations

REVIEW_C: dict[str, dict[str, tuple]] = {
    # 宋并荆南/湖南 — 周行逢为武平(湖南)政权领主
    "event-song-mie-jingnan": {
        "cbdb-person-41649": ("A", "ruler", "武平(湖南)",
            "周行逢为武平节度、湖南一方政主，宋并荆南湖域事件之当事领主。"),
    },
    "event-songjiaoren-yuci": {
        "cbdb-person-79898": ("A", "victim", "中华民国",
            "宋教仁（国民党代理理事长）沪上遇刺身亡，为事件遇害当事人，也是「二次革命」的导火索。"),
    },
    # 大索貌阅
    "event-sui-dasuo-miaoyue": {
        "ctext-person-803544": ("A", "ruler", "隋",
            "隋文帝推行「大索貌阅」核查户口，为直接拍板的皇帝。"),
    },
    # 废太子勇
    "event-sui-fei-tai-zi-yong": {
        "ctext-person-803544": ("A", "ruler", "隋",
            "隋文帝决策废太子杨勇、改立杨广，为废立最高决策者。"),
    },
    "event-sui-keju-chuangjian": {
        "ctext-person-803544": ("A", "ruler", "隋",
            "隋文帝开科取士、开创科举制度，为定制君主。"),
    },
    "event-sui-mie-xiliang": {
        "ctext-person-803544": ("A", "ruler", "隋",
            "隋文帝下诏灭西梁、收其地，为灭梁之主。"),
    },
    "event-sui-sansheng-liubu": {
        "ctext-person-803544": ("A", "ruler", "隋",
            "隋文帝确立三省六部制、厘定官制，为制度创立之君。"),
    },
    "event-sunquan-chengdi": {
        "cbdb-person-20609": ("A", "initiator", "吴",
            "孙权武昌称帝（229），为建吴称帝之正主。"),
    },
    "event-suzong-jiwei": {
        "ctext-person-62031": ("A", "initiator", "唐",
            "李亨于灵武即位为唐肃宗（756），为安史之乱中建平叛中枢的直接主角。"),
    },
    "event-taiping-tianguo": {
        "cbdb-person-65447": ("A", "ruler", "太平天国",
            "洪秀全定都天京（1853）称天王，为太平天国最高统治者。"),
    },
    # 唐隆政变
    "event-tang-long-zhengbian": {
        "ctext-person-840838": ("A", "initiator", "唐",
            "太平公主深度参与唐隆政变（联合李隆基剪除韦氏党），为政变的发起核心之一。"),
    },
    "event-tang-tongyi-quanguo": {
        "cbdb-person-134932": ("A", "ruler", "郑(洛阳)",
            "唐统一之战中王世充为据洛阳之割据首领，是被唐军反复攻伐、最终迫降的重要对象。"),
    },
    "event-three-chibi": {
        "cbdb-person-30257": ("A", "commander", "曹操(魏)",
            "曹操率军南下发动赤壁之战，为魏方最高军事指挥（战败北还）。"),
    },
    "event-three-guandu": {
        "cbdb-person-30257": ("A", "commander", "曹操(魏)",
            "曹操在官渡以少胜多击溃袁绍，为官渡之战的主帅与赢家。"),
    },
    "event-three-north-consolidation": {
        "cbdb-person-30257": ("A", "initiator", "曹操(魏)",
            "曹操扫平北方群雄、实现北方统一，为「北定中原」的缔造者。"),
    },
    "event-three-sun-liu-alliance": {
        "cbdb-person-20609": ("A", "political_leader", "吴",
            "孙权与刘备结盟、共御曹操，为孙刘联盟（赤壁联合）的领袖与决策者。"),
    },
    "event-tianbao-li-linfu": {
        "cbdb-person-32534": ("A", "official", "唐",
            "李林甫独任宰相近十九年、专权天宝朝政，为天宝权相事件的核心人物。"),
    },
    "event-tianbao-yangguozhong": {
        "cbdb-person-379873": ("A", "participant", "范阳(边)",
            "安禄山为边将、与杨国忠不和，是天宝末年杨国忠主政下朝局震荡的直接相关人。"),
        "cbdb-person-32534": ("R", "相邻事件",
            "李林甫之死仅是杨国忠继任的前事背景，其专权详情归入事件 event-tianbao-li-linfu，本事件无独立参与事实。"),
        "cbdb-person-31221": ("A", "official", "唐",
            "杨国忠继任宰相专决朝政，为本次事件核心当事人。"),
    },
    # 天京事变
    "event-tianjing-shibian": {
        "cbdb-person-65447": ("A", "initiator", "太平天国",
            "洪秀全卷入并主导清除杨秀清等（一手促进太原变局），为天京事变核心当事者。"),
    },
    # 天京陷落
    "event-tianjing-xianluo": {
        "cbdb-person-65447": ("A", "victim", "太平天国",
            "洪秀全拒迁城、病崩城中，为天京陷落（1864）的主要当事人与亡当事人。"),
    },
    # 田氏代齐
    "event-tianshi-dai-qi": {
        "ctext-person-134993": ("I",
            "事件以田和求周封为诸侯；周安王仅为被迫册封的名义授权方，无实际参与行为可述，视为 insufficient_event_evidence。"),
    },
    # 剃发令
    "event-tifa-yifu": {
        "cbdb-person-339770": ("A", "official", "清",
            "多尔衮以摄政王下令全国剃发易服，为该政策的强制主导者。"),
    },
    "event-tongmenghui-chengli": {
        "curated-person-sun-yat-sen": ("A", "initiator", "同盟会",
            "孙中山发起创建中国同盟会，为成立大会的首席发起人与总理。"),
    },
    # 吐蕃入长安（郭子仪率 联回纥 退吐蕃）
    "event-tubo-ru-changan": {
        "cbdb-person-94373": ("A", "commander", "唐",
            "郭子仪单骑退吐蕃、光复长安，为唐主宰直接御狄的主帅。"),
    },
    # 瓦岗军崛起
    "event-wagang-jun-jueqi": {
        "cbdb-person-134932": ("A", "ruler", "郑(洛阳)",
            "王世充乘瓦岗内乱坐大洛阳（郑），为隋末割据一方之主要受立者。"),
    },
    "event-wanganshi-bianfa": {
        "cbdb-person-1762": ("A", "initiator", "北宋",
            "王安石主持熙宁变法、行新政，为本事件核心主持人。"),
    },
    "event-wangfeng-waigi": {
        "cbdb-person-135028": ("A", "ruler", "西汉",
            "王政君身为太后给兄弟王凤以政枢地位，为王氏外戚掌权的授受核心。"),
        "cbdb-person-339519": ("R", "背景引用",
            "「王莽亦由此家族登上政治舞台」仅为日后发迹之起笔（前33年王莽尚未任职），非本事件直接参与者。"),
    },
    "event-wangmang-fuchu": {
        "cbdb-person-135028": ("A", "ruler", "西汉(王氏)",
            "太后王政君与王莽共立平帝、再授大司马，为复出掌权之太后主体。"),
        "cbdb-person-339519": ("A", "initiator", "西汉(王氏)",
            "王莽复任大司马、录尚书事复执朝政，为复出掌权的当事者。"),
    },
    "event-wangmang-jushe": {
        "cbdb-person-339519": ("A", "ruler", "新莽",
            "王莽居摄、称假皇帝未僭号，为居摄主事者。"),
    },
    "event-wangxianzhi-qiyi": {
        "ctext-person-590256": ("A", "initiator", "农民军",
            "王仙芝（与黄巢）起于长垣，为晚唐大起义的先发首领。"),
    },
    "event-wangxiaobo-li-shun-qiyi": {
        "ctext-person-768940": ("A", "initiator", "农民军",
            "王小波以「均贫富」号召起事，为直接发动者。"),
    },
    "event-weihaiwei-zhizhan": {
        "cbdb-person-58649": ("A", "commander", "清",
            "丁汝昌督率北洋舰队守威海，城陷自裁殉国，为守卫战之提督。"),
    },
    "event-wentianxiang-kangyuan": {
        "cbdb-person-19123": ("A", "commander", "南宋",
            "文天祥举兵拥宋抗元、兵败被俘慷慨殉国，为抗元忠臣主帅。"),
    },
    # 吴国崛起
    "event-wu-guo-jueqi": {
        "ctext-person-6646198": ("A", "official", "吴",
            "伍子胥与孙武共辅阖闾整军经政，为吴崛起南强之直接功臣。"),
    },
    # 汉昭帝之宦官之……
    "event-wudi-si-huoguang": {
        "ctext-person-216197": ("A", "official", "西汉",
            "上官桀为武帝崩后顾命辅臣之一，参与当日朝政，为「霍光辅政群」平常之主角。"),
        "ctext-person-152034": ("A", "official", "西汉",
            "金日磾亦为武帝顾命大臣之一（车骑将军），直接参与后武帝辅政。"),
    },
    # 五国伐齐
    "event-wuguo-fa-qi": {
        "ctext-person-657661": ("A", "commander", "燕",
            "燕昭王与各国联盟伐齐，为五国联军主轴与主帅（乐毅代率亦在区内）。"),
    },
    # 吴起变法
    "event-wuqi-bianfa": {
        "ctext-person-746424": ("A", "ruler", "楚",
            "楚悼王任用吴起推行变法于楚，为变法决策之君。"),
    },
    # 戊戌变法
    "event-wuxu-bianfa": {
        "curated-person-cixi-taihou": ("A", "ruler", "清",
            "慈禧太后发动戊戌政变、废止变法并幽禁光绪，为事件主导决策的太后。"),
    },
    "event-xian-di-dong-gui": {
        "cbdb-person-30257": ("A", "ruler", "汉",
            "曹操于献帝东归之末将其迎至许昌，为控制汉廷之收局实际主导者。"),
    },
    # 先天政变
    "event-xiantian-zhengbian": {
        "ctext-person-840838": ("A", "participant", "唐",
            "先天政变中太平公主为失败方（被赐死），为政变对立双方的核心当事人。"),
    },
    # 肴之战
    "event-xiao-zhizhan": {
        "ctext-person-629332": ("A", "ruler", "秦",
            "秦穆公谋郑之役（崤之战前奏），决定伐郑、兵败崤山之君。"),
    },
    # 北魏孝文帝改革
    "event-xiaowendi-gaige": {
        "ctext-person-762138": ("A", "initiator", "北魏",
            "北魏孝文帝（拓跋宏）亲主迁都洛阳、行汉化改革，为全盘主导者。"),
    },
    "event-xin-gaizhi": {
        "cbdb-person-339519": ("A", "ruler", "新莽",
            "王莽托古改制、行王田五均六筦等新法，为改制正主。"),
    },
    "event-xinjiang-jiansheng": {
        "cbdb-person-54964": ("A", "official", "清",
            "左宗棠奏请新疆建省并主持善后，为该建制主要推动者与执行者。"),
    },
    "event-xuanwang-zhongxing": {
        "ctext-person-257248": ("A", "ruler", "周",
            "周宣王（召公之子）复振王室，为西周中兴之主。"),
    },
    "event-xuanzong-jiwei": {
        "ctext-person-840838": ("A", "official", "唐",
            "太平公主以睿宗之妹阻敕入卷，参与玄宗承继朝局，其势力随后被铲除，为相关贵戚当事方。"),
    },
    "event-xuda-beifa": {
        "cbdb-person-66291": ("A", "commander", "明",
            "常遇春为北伐副大将军、随徐达克元大都，为北伐直接主将。"),
    },
    "event-xuge-zhizhan": {
        "ctext-person-65549": ("A", "victim", "周",
            "周桓王御驾征郑中箭负伤，为缁葛之战受害的周天子。"),
    },
    "event-yan-yun-shiliuzhou": {
        "cbdb-person-339657": ("A", "ruler", "后晋",
            "石敬瑭割燕云十六州与契丹，为割地倚辽之决策者。"),
    },
    "event-yangguang-jiwei": {
        "ctext-person-803544": ("A", "ruler", "隋",
            "隋文帝于本事件中病逝（604，有被弑传说）成而为历状，直接触发杨广即位（炀帝系主角，受知识库所限未另录）。"),
    },
    "event-yangjian-zhuanquan": {
        "ctext-person-522578": ("A", "ruler", "北周",
            "北周宣帝之死为杨坚辅政之直接前提，为「宣帝崩逝、王死伤」事件背景核心人物。"),
    },
    "event-yanling-zhizhan": {
        "ctext-person-443095": ("A", "ruler", "楚",
            "楚共王在位时晋楚鄢陵之战（575），楚方全军溃败之君决策所系。"),
    },
    "event-yongle-beizheng": {
        "ctext-person-654665": ("A", "participant", "蒙古(鞑靼)",
            "本雅失里为永乐北伐之讨伐目标（鞑靼可汗，败后西走），为直接受征对象。"),
    },
    # 永贞革新
    "event-yongzhen-gexin": {
        "cbdb-person-3605": ("A", "official", "唐",
            "柳宗元参与永贞革新（王叔文集团）主理文事，为革新重要成员。"),
        "cbdb-person-189642": ("A", "official", "唐",
            "王伾为永贞革新核心二人组「二王」之一，主持内务。"),
        "cbdb-person-33597": ("A", "initiator", "唐",
            "王叔文为永贞革新实际主持（翰林学士），发起并推进新改革，革新失败后被贬杀。"),
    },
    "event-youwang-zhi-luan": {
        "ctext-person-382372": ("A", "victim", "西周",
            "周幽王废申后等致镐京之乱，被申侯等共同兵临，为暴乱是最的直接受害者与祸主。"),
    },
    "event-yuanshi-wajie": {
        "cbdb-person-30257": ("A", "commander", "魏（操）",
            "曹操挟天子、分化瓦解袁绍集团，为期中原逐鹿的关键玩家。"),
    },
    "event-yuanshu-chengdi": {
        "cbdb-person-30257": ("A", "commander", "魏(曹操)",
            "曹操讨灭僭号称帝的袁术，为指挥之帅。"),
    },
    "event-zhang-xianzhong-fazhan": {
        "cbdb-person-65627": ("R", "背景引用",
            "summary将李自成与张献忠并列为两支平行势力（剖川、陕各转战），李自成未参与张献忠部势力发展。"),
    },
    "event-zhangshichen-ju-gaoyou": {
        "cbdb-person-30148": ("R", "背景引用",
            "summary「与朱元璋、陈友谅并列为元末三大势力」仅作并列背景，朱元璋未直接参与张士诚据高邮、称诚王之事。"),
    },
    "event-zhangxun-fubi": {
        "cbdb-person-63908": ("A", "political_leader", "中华民国",
            "段祺瑞率部讨伐张勋、驱其复辟兵破，为事件收束的主要军政决策人。"),
    },
    "event-zhaowang-nanzheng": {
        "ctext-person-74633": ("A", "ruler", "周",
            "周昭王南征荆楚、卒于江上，为南征事件之君主当事人。"),
    },
    "event-zheng-zhuanggong-xiaoba": {
        "ctext-person-668302": ("A", "participant", "郑",
            "共叔段据京城不臣、作乱的直接对立当事人，为郑庄公初期内政（郑庄小霸前夜）的核心人物。"),
    },
    "event-zhengde-zhengzhi": {
        "ctext-person-947007": ("A", "ruler", "明",
            "明武宗（正德）在位亲政，内廷格局与军政皆系其主，为时代事件之核心君主。"),
    },
    "event-zhenguan-zhizhi": {
        "cbdb-person-30864": ("A", "official", "唐",
            "杜如晦为贞观机制核心宰辅之一（与防玄龄共理机务），为贞观治世的重要行政者。"),
        "cbdb-person-15610": ("A", "official", "唐",
            "魏徵以直言极谏辅佐唐太宗，为贞观之治的代表名臣（《贞观政要》）。"),
    },
    "event-zhiwan-zhanzheng": {
        "cbdb-person-63908": ("A", "commander", "中华民国",
            "直拳战争（直皖大战）中段祺瑞为皖系一方的统帅。"),
    },
    "event-zhizhi-xinzheng": {
        "cbdb-person-100386": ("A", "ruler", "元",
            "元英宗在任推行新政（行新政、岁务院各行中书省更制规），因被弑而新政中断，为新政决断之元主。"),
    },
    "event-zhonghua-suweiai": {
        "curated-person-mao-zedong": ("A", "political_leader", "中国共产党",
            "毛泽东在瑞金主持中华苏维埃共和国成立并任主席，为建政主持者。"),
    },
    "event-zhougong-dongzheng": {
        "ctext-person-263104": ("A", "commander", "周",
            "周公旦东征平定武庚三监之乱，为东征主帅（《尚书》）。"),
    },
    "event-zhougong-shezheng": {
        "ctext-person-263104": ("A", "ruler", "周",
            "周公摄政当国、制作礼乐，为摄政朝主。"),
    },
    "event-zhuge-liang-beifa": {
        "cbdb-person-25403": ("A", "commander", "蜀汉",
            "诸葛亮率蜀军六出祁山北伐，为北伐主导与主帅。"),
    },
    "event-zhuge-liang-nanzheng": {
        "cbdb-person-25403": ("A", "commander", "蜀汉",
            "诸葛亮指挥南征南中（七擒孟获），为南征主帅。"),
    },
    "event-zhuge-liang-shoubei": {
        "cbdb-person-25403": ("A", "commander", "蜀汉",
            "诸葛亮主理北伐后防、屯田边防，为蜀汉前线军事核心。"),
    },
    "event-zhuge-liang-zhishi": {
        "cbdb-person-25403": ("A", "official", "蜀汉",
            "诸葛亮于五丈原病逝，为蜀汉丞相核心（丞相之终局与意志落点）。"),
    },
    "event-zhuyuanzhang-mie-zhang": {
        "cbdb-person-66291": ("A", "commander", "明",
            "徐达/常遇春讨灭吴、攻擒张士诚，为歼灭战主帅之一（徐亦即）。"),
        "cbdb-person-30148": ("A", "initiator", "明",
            "朱元璋决策攻灭张士诚等江南势力，为南方统一之最高决策者。"),
    },
    "event-zhuyuanzhang-qu-jqing": {
        "cbdb-person-30148": ("A", "initiator", "明",
            "朱元璋并诸侯、讨元定江南以北，为南定之主的最高决策者。"),
    },
    "event-zhuyuanzhang-toujun": {
        "cbdb-person-30148": ("A", "participant", "淮西义军",
            "朱元璋慧亲投郭子兴红巾军（濠州），辚从军之始的核心参与者。"),
    },
    "event-zunyi-huiyi": {
        "curated-person-mao-zedong": ("A", "political_leader", "中国共产党",
            "遵义会议重新确立毛泽东的领导地位，为其在长征转折中的决策核心。"),
    },
    "event-zuozongtang-xizheng": {
        "cbdb-person-54964": ("A", "commander", "清",
            "左宗棠率湘军西征、平定阿古柏收复新疆，为西征主帅。"),
    },
}