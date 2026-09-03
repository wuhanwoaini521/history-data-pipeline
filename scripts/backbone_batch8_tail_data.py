# -*- coding: utf-8 -*-
"""China History Backbone V1 — Batch 8（中华民国→近现代）Data（part 2）：军阀/五四 + 国民革命 + 中共早期。"""

from __future__ import annotations

from backbone_batch8_data import MODERN, WP, _ev, _rel  # noqa: F401

# ---------------------------------------------------------------------------
# Phase 2 — 军阀混战与五四（1917—1926）
# ---------------------------------------------------------------------------
PHASE_WARLORDS_MAY4TH = [
    _ev("event-fuyuan-zhi-zheng", "府院之争（总统府与国务院冲突）", "political",
        1917, 1917, "year", "period-republic", "major",
        "1916—1917 年，总统黎元洪与国务总理段祺瑞围绕对德宣战等问题冲突，"
        "段祺瑞召督军团入京胁迫国会，黎元洪免段职，府院之争激化，"
        "成为张勋复辟与护法运动的起点。",
        f"档案史料：北洋政府公报、国会议事录；现代研究：{MODERN['warlord']}",
        WP["minguo"],
        ["regime-republic"],
        relations=[
            _rel("event-yuanshikai-qushi", "follows", 0.9, "袁世凯死后总统与总理权力冲突。"),
            _rel("event-zhangxun-fubi", "leads_to", 0.9, "黎元洪召张勋调停，张勋趁机复辟。"),
        ]),
    _ev("event-zhangxun-fubi", "张勋复辟（清室复辟）", "political",
        1917, 1917, "year", "period-republic", "major",
        "1917 年 7 月，长江巡阅使张勋率辫子军入京，拥立清废帝溥仪复辟，"
        "改国号宣统；段祺瑞借机讨伐（马厂誓师），复辟仅十二天即告失败。",
        f"档案史料：张勋复辟电文与《政府公报》；现代研究：{MODERN['warlord']}",
        WP["minguo"],
        ["regime-republic"],
        relations=[
            _rel("event-fuyuan-zhi-zheng", "follows", 0.9, "府院之争中黎元洪召张勋调停。"),
            _rel("event-hufa-yundong", "leads_to", 0.7, "复辟失败后段祺瑞拒绝恢复约法，护法运动起。"),
        ]),
    _ev("event-hufa-yundong", "护法运动（孙中山南下护法）", "war",
        1917, 1918, "range", "period-republic", "major",
        "1917 年孙中山南下广州发起护法运动，反对段祺瑞废弃《临时约法》与国会，"
        "联合西南军阀建立军政府；因军阀内讧与军政府改组，"
        "1918 年孙中山辞职，护法运动第一次失败。",
        f"档案史料：广州军政府文件；现代研究：{MODERN['warlord']}",
        WP["minguo"],
        ["regime-republic"],
        relations=[
            _rel("event-zhangxun-fubi", "follows", 0.8, "复辟与约法危机后的护法。"),
            _rel("event-zhiwan-zhanzheng", "precedes", 0.6, "护法运动后军阀间战争频仍。"),
        ]),
    _ev("event-bali-hehui", "巴黎和会与中国外交失败", "diplomatic",
        1919, 1919, "year", "period-republic", "major",
        "1919 年 1—6 月巴黎和会召开，中国政府要求收回德国在山东权益，"
        "英、法、美等却决定将德国在山东的权利转让日本；"
        "4 月底消息传回国内，直接触发五四运动。",
        f"档案史料：中国代表团交涉文件（《巴黎和会中国外交资料》）；现代研究：{MODERN['warlord']}",
        WP["minguo"],
        ["regime-republic"],
        relations=[
            _rel("event-hufa-yundong", "follows", 0.6, "和会外交失败引发国内抗议。"),
            _rel("event-wusi-yundong", "leads_to", 0.95, "外交失败成为五四运动导火索。"),
        ]),
    _ev("event-wusi-yundong", "五四运动", "political",
        1919, 1919, "year", "period-republic", "critical",
        "1919 年 5 月 4 日，北京学生因巴黎和会山东问题举行游行示威，"
        "抗议北洋政府外交失败（\"外争主权、内除国贼\"口号），"
        "运动随后扩展到全国工商各界（三罢），北洋政府被迫拒签对德和约并罢免曹汝霖等；"
        "五四运动成为新文化运动与民族觉醒的标志性事件（史学通说）。",
        f"档案史料：北京政府档案、各地报刊报道；现代研究：{MODERN['warlord']}",
        WP["minguo"],
        ["regime-republic"],
        relations=[
            _rel("event-bali-hehui", "follows", 0.95, "巴黎和会外交失败引发。"),
        ],
        review_note="五四运动在新文化运动、学生运动与国际思潮（俄国十月革命影响）中的定位，"
                    "学界有不同侧重；本事件按事实进程记录，不写入特定理论定性表述。"),
    _ev("event-zhiwan-zhanzheng", "直皖战争", "war",
        1920, 1920, "year", "period-republic", "major",
        "1920 年 7 月，直系（曹锟、吴佩孚）与皖系（段祺瑞）为争夺北京政权开战，"
        "直系获胜，皖系势力瓦解，北京政府由直系与奉系（张作霖）共同控制。",
        f"档案史料：北洋政府电令与战报；现代研究：{MODERN['warlord']}",
        WP["minguo"],
        ["regime-republic"],
        relations=[
            _rel("event-hufa-yundong", "follows", 0.6, "护法运动期间军阀混战加剧。"),
            _rel("event-diyici-zhifeng-zhanzheng", "leads_to", 0.9, "直皖战后直奉矛盾上升。"),
        ]),
    _ev("event-diyici-zhifeng-zhanzheng", "第一次直奉战争", "war",
        1922, 1922, "year", "period-republic", "major",
        "1922 年 4—5 月，直系与奉系为争北京政权开战，奉系败退关外，"
        "直系统一北京政权（吴佩孚掌权，\"法统重光\"、恢复约法表面文章），"
        "曹锟 1923 年贿选总统。",
        f"档案史料：直奉战争电文与档案；现代研究：{MODERN['warlord']}",
        WP["minguo"],
        ["regime-republic"],
        relations=[
            _rel("event-zhiwan-zhanzheng", "follows", 0.9, "直皖战争后的军阀再度开战。"),
            _rel("event-dierci-zhifeng-zhanzheng", "leads_to", 0.9, "1924 年直奉再度开战。"),
        ]),
    _ev("event-dierci-zhifeng-zhanzheng", "第二次直奉战争与北京政变", "war",
        1924, 1924, "year", "period-republic", "major",
        "1924 年 9—11 月，直奉第二次开战，直系将领冯玉祥在北京发动政变"
        "（倒戈囚曹锟、驱逐溥仪出宫），直系失败，奉系张作霖入关，"
        "北京政权格局再变，孙中山应邀北上，1925 年初病逝。",
        f"档案史料：北京政变通电、军阀电文；现代研究：{MODERN['warlord']}",
        WP["minguo"],
        ["regime-republic"],
        relations=[
            _rel("event-diyici-zhifeng-zhanzheng", "follows", 0.9, "直奉再度开战。"),
        ]),
]


# ---------------------------------------------------------------------------
# Phase 3 — 国民革命与北伐（1924—1928）
# ---------------------------------------------------------------------------
PHASE_NATIONAL_REV = [
    _ev("event-guomindang-gaizu", "国民党改组与第一次全国代表大会", "political",
        1924, 1924, "year", "period-republic", "major",
        "1924 年 1 月，中国国民党第一次全国代表大会在广州召开，"
        "确定联俄、容共、扶助农工的三大政策，接纳共产党员以个人身份加入国民党，"
        "国共第一次合作正式形成，为北伐奠定组织基础。",
        f"档案史料：国民党一大宣言与决议；现代研究：{MODERN['cpc']}",
        WP["minguo"],
        ["regime-republic"],
        relations=[
            _rel("event-wusi-yundong", "follows", 0.8, "五四运动推动新民主义力量发展。"),
            _rel("event-huangpu-junxiao", "leads_to", 0.9, "改组后创办黄埔军校。"),
        ],
        review_note="\"三大政策\"为后世概括表述（若干政策在大会文件中共有具体决议）；"
                    "本事件记录改组与国共合作形成的事实。"),
    _ev("event-huangpu-junxiao", "黄埔军校建立", "foundation",
        1924, 1924, "year", "period-republic", "major",
        "1924 年 5 月，中国国民党陆军军官学校（黄埔军校）在广州黄埔成立，"
        "蒋介石任校长，周恩来等任政治工作职务；"
        "军校培养出国民革命军大批军事骨干。",
        f"档案史料：黄埔军校《校史稿》与章程；现代研究：{MODERN['cpc']}",
        WP["minguo"],
        ["regime-republic"],
        relations=[
            _rel("event-guomindang-gaizu", "follows", 0.9, "改组后建立的军事教育机构。"),
            _rel("event-guomin-gemingjun-beifa", "leads_to", 0.9, "国民革命军以黄埔系为骨干。"),
        ]),
    _ev("event-guomin-gemingjun-beifa", "国民革命军北伐", "war",
        1926, 1928, "range", "period-republic", "major",
        "1926 年 7 月，国民革命军从广东誓师北伐，"
        "先后击溃吴佩孚（湖北）、孙传芳（东南）、张作霖（北方），"
        "1928 年 6 月进入北京，北伐名义完成，北洋军阀政权覆灭。",
        f"档案史料：北伐军档案与战报；现代研究：{MODERN['minguo']}",
        WP["minguo"],
        ["regime-republic"],
        relations=[
            _rel("event-huangpu-junxiao", "follows", 0.9, "黄埔军校培养的军队为主力。"),
            _rel("event-nanjing-guominzhengfu", "leads_to", 0.9, "北伐期间在南京建立国民政府。"),
            _rel("event-dongbei-yizhi", "leads_to", 0.9, "1928 年张作霖死后东北易帜，名义统一。"),
        ]),
    _ev("event-nanjing-guominzhengfu", "南京国民政府建立", "foundation",
        1927, 1927, "year", "period-republic", "major",
        "1927 年 4 月 18 日，国民政府在南京成立（宁汉分裂后逐步整合），"
        "1928 年北伐完成后南京成为全国性中央政府所在地（抗战时期曾迁重庆）。",
        f"档案史料：国民政府组织系统档案；现代研究：{MODERN['minguo']}",
        WP["minguo"],
        ["regime-republic"],
        relations=[
            _rel("event-guomin-gemingjun-beifa", "follows", 0.9, "北伐推进中建都。"),
        ]),
    _ev("event-guogong-fenlie-1927", "国共合作破裂（1927 年清党与分共）", "political",
        1927, 1927, "year", "period-republic", "major",
        "1927 年 4 月至 7 月，国共合作破裂：蒋介石集团在上海等地实施\"清党\""
        "（4 月 12 日后武力清除共产党员），7 月 15 日武汉国民政府宣布\"分共\"，"
        "共产党员与国民党左派关系终结，第一次国内战争（十年内战）开始。",
        f"档案史料：1927 年清党档案、国民党组织史料；现代研究：{MODERN['cpc']}",
        WP["minguo"],
        ["regime-republic"],
        relations=[
            _rel("event-guomin-gemingjun-beifa", "follows", 0.9, "北伐期间统一战线破裂。"),
        ],
        review_note="\"清党\"\"分共\"为历史文献与史学通用术语；事件准确时间点（412/715）按"
                    "《中国共产党历史》与《中华民国史》通行记载。"),
    _ev("event-dongbei-yizhi", "东北易帜", "political",
        1928, 1928, "year", "period-republic", "major",
        "1928 年 12 月 29 日，张学良通电宣布东北归附南京国民政府，改悬青天白日旗，"
        "史称东北易帜；国民政府实现形式上的全国统一（新疆、西藏等地仍为割据或名义统辖）。",
        f"档案史料：东北易帜通电与国民政府档案；现代研究：{MODERN['minguo']}",
        WP["minguo"],
        ["regime-republic"],
        relations=[
            _rel("event-guomin-gemingjun-beifa", "follows", 0.9, "北伐完成后东北归附。"),
        ]),
]


# ---------------------------------------------------------------------------
# Phase 4 — 中共早期节点（1921—1936）
# ---------------------------------------------------------------------------
PHASE_CPC_EARLY = [
    _ev("event-zggcd-chengli", "中国共产党成立（中共一大）", "foundation",
        1921, 1921, "year", "period-republic", "major",
        "1921 年 7 月，中国共产党第一次全国代表大会在上海（后转移至嘉兴南湖）召开，"
        "宣告中国共产党成立；此为 20 世纪中国政治史的重大组织事件（1920s 各地共产主义小组即已酝酿）。",
        f"档案史料：中共一大文件与回忆；现代研究：中共中央党史研究室《中国共产党历史》第一卷",
        WP["minguo"],
        [],
        relations=[
            _rel("event-wusi-yundong", "follows", 0.8, "五四后马克思主义传播促成建党。"),
            _rel("event-guomindang-gaizu", "precedes", 0.7, "建党后与国民党合作。"),
        ]),
    _ev("event-nanchang-qiyi", "南昌起义", "rebellion",
        1927, 1927, "year", "period-republic", "major",
        "1927 年 8 月 1 日，周恩来、贺龙、叶挺等率部在南昌举行武装起义"
        "（共产党领导的首批武装反抗），起义军随后南下广东受挫；"
        "南昌起义日后来被确定为中国人民解放军的建军纪念日（史实与纪念惯例）。",
        f"档案史料：南昌起义军事档案（中央档案馆藏）；现代研究：《中国共产党历史》第一卷",
        WP["minguo"],
        [],
        relations=[
            _rel("event-guogong-fenlie-1927", "follows", 0.95, "国共破裂后的武装起义。"),
            _rel("event-qiushou-qiyi", "precedes", 0.8, "同年 9 月秋收起义。"),
        ]),
    _ev("event-qiushou-qiyi", "秋收起义", "rebellion",
        1927, 1927, "year", "period-republic", "major",
        "1927 年 9 月，毛泽东在湘赣边界领导秋收起义，起义军受挫后转至井冈山地区，"
        "初步尝试开创农村根据地（\"农村包围城市\"为后来的理论总结）。",
        f"档案史料：秋收起义纪录与毛著相关文献；现代研究：《中国共产党历史》第一卷",
        WP["minguo"],
        [],
        relations=[
            _rel("event-nanchang-qiyi", "follows", 0.9, "南昌起义后同年秋的武装起义。"),
            _rel("event-jinggangshan-jidi", "leads_to", 0.9, "受挫后转上井冈山。"),
        ]),
    _ev("event-jinggangshan-jidi", "井冈山根据地形成", "foundation",
        1927, 1928, "range", "period-republic", "major",
        "1927 年秋至 1928 年，秋收起义余部与南昌起义余部（朱德、陈毅）在井冈山会合，"
        "建立中共领导的第一块农村根据地（井冈山革命根据地），"
        "为土地革命时期根据地建设之先例。",
        f"档案史料：井冈山斗争档案与回忆；现代研究：《中国共产党历史》第一卷",
        WP["minguo"],
        [],
        relations=[
            _rel("event-qiushou-qiyi", "follows", 0.9, "秋收起义部队上井冈山。"),
            _rel("event-zhonghua-suweiai", "leads_to", 0.8, "根据地发展至建立苏维埃政权。"),
        ]),
    _ev("event-zhonghua-suweiai", "中华苏维埃共和国成立（瑞金）", "foundation",
        1931, 1931, "year", "period-republic", "major",
        "1931 年 11 月，中华苏维埃第一次全国代表大会在江西瑞金召开，"
        "宣布成立中华苏维埃共和国临时中央政府，毛泽东任主席；"
        "在国共对峙中建立的中共政权形态（1934 年随长征转移，1937 年因国共合作取消）。",
        f"档案史料：苏维埃第一次代表大会文件；现代研究：《中国共产党历史》第一卷",
        WP["minguo"],
        ["regime-chinese-soviet-republic"],
        relations=[
            _rel("event-jinggangshan-jidi", "follows", 0.9, "根据地发展的高峰。"),
            _rel("event-changzheng", "leads_to", 0.9, "第五次围剿后被迫长征。"),
        ]),
    _ev("event-changzheng", "红军长征（战略转移）", "war",
        1934, 1936, "range", "period-republic", "major",
        "1934 年 10 月至 1936 年 10 月，中央红军等因第五次反\"围剿\"失败进行战略转移，"
        "历尽转战（四渡赤水、强渡大渡河、翻雪山草地等），"
        "1935 年 10 月到达陕北，1936 年 10 月红军三大主力在甘肃会宁会师，长征结束。",
        f"档案史料：红军长征军事文献；现代研究：《中国共产党历史》第一卷",
        WP["minguo"],
        [],
        relations=[
            _rel("event-zhonghua-suweiai", "follows", 0.95, "反围剿失败后战略转移。"),
        ],
        review_note="长征途中的重大战斗与决策（湘江、遵义、四渡赤水）详见专史；"
                    "本事件记录整体转移进程与终点（1936 年会师）。"),
    _ev("event-zunyi-huiyi", "遵义会议", "political",
        1935, 1935, "year", "period-republic", "major",
        "1935 年 1 月，中共中央政治局在贵州遵义召开扩大会议，"
        "调整军事领导（确立毛泽东在军事上的领导地位，通行表述），"
        "是长征中具有转折意义的会议（史学通说）。",
        f"档案史料：遵义会议决议与回忆纪录；现代研究：《中国共产党历史》第一卷",
        WP["minguo"],
        [],
        relations=[
            _rel("event-changzheng", "part_of", 0.9, "长征途中召开的会议。"),
        ]),
]