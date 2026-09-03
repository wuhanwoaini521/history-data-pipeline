# -*- coding: utf-8 -*-
"""China History Backbone V1 — Batch 7（清→晚清→辛亥革命）Data（part 2）：鸦片战争+太平天国 + 洋务+边疆。"""

from __future__ import annotations

from backbone_batch7_data import MODERN, W, _ev, _rel  # noqa: F401

# ---------------------------------------------------------------------------
# Phase 3 — 鸦片战争与太平天国（1839—1864）
# ---------------------------------------------------------------------------
PHASE_OPIUM_TAIPING = [
    _ev("event-linzexu-jinyan", "林则徐广东禁烟与虎门销烟", "political",
        1838, 1839, "range", "period-late-qing", "major",
        "道光十八至十九年（1838—1839 年），道光帝派林则徐为钦差大臣赴广东禁烟；"
        "1839 年 6 月在虎门海滩当众销毁收缴鸦片共约二百三十七万斤，"
        "英方以此为口实武力报复，鸦片战争随即爆发。",
        f"古代史料：《清实录·宣宗实录》；《林则徐集》奏稿；现代参考：{MODERN['opium']}",
        W["qingshigao_lu"],
        ["regime-qing"],
        relations=[
            _rel("event-bailianjiao-qiyi", "follows", 0.6, "林则徐禁烟针对英商对华鸦片输入。"),
            _rel("event-diyici-yapian-zhanzheng", "leads_to", 0.95, "销烟成为战争直接导火索。"),
        ],
        review_note="虎门销烟销毁方式为盐卤石灰浸化；鸦片来源、数量各记载基本一致（约 2 万余箱）。"),
    _ev("event-diyici-yapian-zhanzheng", "第一次鸦片战争", "war",
        1840, 1842, "range", "period-late-qing", "critical",
        "道光二十年至二十二年（1840—1842 年），英国因对华鸦片贸易与通商问题发动战争，"
        "先后攻陷定海、吴淞等地，进逼南京；"
        "清军在广东（林则徐）与东南沿海多处抵抗失利，"
        "1842 年 8 月清廷接受英国条件，战争以《南京条约》签订结束。",
        f"古代史料：《清实录·宣宗实录》；《筹办夷务始末（道光朝）》；现代参考：{MODERN['opium']}",
        W["qingshigao_lu"],
        ["regime-qing"],
        relations=[
            _rel("event-linzexu-jinyan", "follows", 0.95, "禁烟引发英军来犯。"),
            _rel("event-nanjing-tiaoyue", "leads_to", 0.95, "战败后签订南京条约。"),
        ],
        review_note="战争性质为英国以武力打开中国市场（\"通商战争\"说见英国方面档案）；"
                    "本事件记录开战、进程与结局事实，单因论（如\"林则徐激化\"）不采用。"),
    _ev("event-nanjing-tiaoyue", "《南京条约》签订", "treaty",
        1842, 1842, "year", "period-late-qing", "major",
        "道光二十二年（1842 年）七月，清廷与英国签订《南京条约》："
        "割让香港岛、赔款二千一百万银元、开放五口通商、协定关税；"
        "鸦片战争后中国开始进入与西方列强不平等条约关系的阶段（近代半殖民地化的开端，学界表述不一）。",
        f"古代史料：《南京条约》文本；《筹办夷务始末（道光朝）》；现代参考：{MODERN['opium']}",
        W["qingshigao"],
        ["regime-qing"],
        relations=[
            _rel("event-diyici-yapian-zhanzheng", "follows", 0.95, "鸦片战争结束和约。"),
        ],
        review_note="条约文本与谈判过程见《筹办夷务始末》等国朝档案；“不平等条约”“半殖民地半封建”"
                    "等为历史研究常用术语而非事实描述，本事件用条约内容直陈。"),
    _ev("event-taiping-tianguo", "太平天国运动", "rebellion",
        1851, 1864, "range", "period-late-qing", "major",
        "咸丰元年至同治三年（1851—1864 年），洪秀全领导太平天国运动，"
        "建号定都、北伐西征，占据中国南部半壁，与清廷对峙十四年，"
        "同治三年（1864 年）湘军攻陷天京，运动失败。"
        "本事件为 aggregate，子事件（金田起义、定都天京、天京事变、天京陷落）经 part_of 关联。",
        f"古代史料：《清实录·文宗实录》；《太平天国文书汇编》等史料集；现代参考：{MODERN['taiping']}",
        W["qingshigao_lu"],
        ["regime-qing", "regime-taiping"],
        relations=[
            _rel("event-diyici-yapian-zhanzheng", "follows", 0.8, "鸦片战争后社会矛盾激化背景下的起义。"),
            _rel("event-jintian-qiyi", "leads_to", 0.9, "金田起义为开端。"),
        ],
        review_note="太平天国评价（农民起义性质、宗教色彩、破坏与建设）在史学界争论激烈；"
                    "本事件按政权建立、战争进程与覆亡的事实框架记录。"),
    _ev("event-jintian-qiyi", "金田起义（太平天国建立）", "rebellion",
        1851, 1851, "year", "period-late-qing", "major",
        "咸丰元年（1851 年）1 月，洪秀全在广西桂平金田村聚众起义，"
        "建号太平天国，颁行天历，洪秀全称天王；太平天国运动由此开始。",
        f"古代史料：《清实录·文宗实录》；《太平天国文书汇编》；现代参考：{MODERN['taiping']}",
        W["qingshigao_lu"],
        ["regime-taiping"],
        relations=[
            _rel("event-taiping-tianguo", "part_of", 0.95, "太平天国运动开端。"),
            _rel("event-dingdu-tianjing", "leads_to", 0.9, "起义军两年后攻占南京定都。"),
        ]),
    _ev("event-dingdu-tianjing", "太平军攻占南京、定都天京", "war",
        1853, 1853, "year", "period-late-qing", "major",
        "咸丰三年（1853 年）3 月，太平军（春官正丞相杨秀清等统军）攻占江宁（南京），"
        "改名天京定为都城，随即派出北伐军与西征军，太平天国控制区扩展至长江中下游；"
        "清政府设江南、江北大营围困天京。",
        f"古代史料：《清实录·文宗实录》；现代参考：{MODERN['taiping']}",
        W["qingshigao_lu"],
        ["regime-taiping", "regime-qing"],
        relations=[
            _rel("event-taiping-tianguo", "part_of", 0.95, "定都后的政权巩固阶段。"),
            _rel("event-jintian-qiyi", "follows", 0.9, "起义后两年攻占南京。"),
        ]),
    _ev("event-tianjing-shibian", "天京事变", "political",
        1856, 1856, "year", "period-late-qing", "major",
        "咸丰六年（1856 年），太平天国领导集团内讧：韦昌辉奉洪秀全密令杀杨秀清，"
        "旋又被洪秀全处死，石达开出走；"
        "天京事变致太平天国元气大伤，由盛转衰。",
        f"古代史料：《清实录》相关奏报；《李秀成自述》等；现代参考：{MODERN['taiping']}",
        W["qingshigao_lu"],
        ["regime-taiping"],
        relations=[
            _rel("event-taiping-tianguo", "part_of", 0.95, "领导集团内讧。"),
            _rel("event-dingdu-tianjing", "follows", 0.9, "定都三年后的权力斗争。"),
            _rel("event-tianjing-xianluo", "leads_to", 0.8, "事变后清军湘军乘势反攻。"),
        ]),
    _ev("event-tianjing-xianluo", "湘军攻陷天京（太平天国结束）", "war",
        1864, 1864, "year", "period-late-qing", "major",
        "同治三年（1864 年）7 月，曾国藩弟曾国荃率湘军攻陷天京，"
        "天王府被焚，洪秀全已病亡，幼天王等突围后被俘，"
        "太平天国主要政权结束（余部转战至 1868 年捻军覆亡）。",
        f"古代史料：《清实录·穆宗实录》；《曾国藩全集》家书奏稿；现代参考：{MODERN['taiping']}",
        W["qingshigao_lu"],
        ["regime-qing", "regime-taiping"],
        relations=[
            _rel("event-taiping-tianguo", "part_of", 0.95, "运动结束。"),
            _rel("event-tianjing-shibian", "follows", 0.9, "天京事变后清军逐渐得势。"),
        ]),
    _ev("event-dierci-yapian-zhanzheng", "第二次鸦片战争（英法联军之役）", "war",
        1856, 1860, "range", "period-late-qing", "major",
        "咸丰六年至十年（1856—1860 年），英国以\"亚罗号\"事件、法国以广西教案为借口"
        "联合对华开战，攻陷广州、大沽、天津，1860 年攻入北京；"
        "清廷先后签订《天津条约》《北京条约》，战争结束。"
        "本事件为 aggregate，子事件（天津条约、北京条约与联军入京）经 part_of 关联。",
        f"古代史料：《筹办夷务始末（咸丰朝）》；现代参考：{MODERN['opium']}",
        W["qingshigao"],
        ["regime-qing"],
        relations=[
            _rel("event-nanjing-tiaoyue", "follows", 0.9, "第一次鸦片战争后十四年战端再起。"),
        ]),
    _ev("event-tianjin-tiaoyue", "《天津条约》签订", "treaty",
        1858, 1858, "year", "period-late-qing", "major",
        "咸丰八年（1858 年），清廷与英、法、美、俄签订《天津条约》："
        "增开通商口岸、外国公使驻京、内河通航、传教自由等；"
        "1859 年大沽口之战清军重创英法舰队，但战事持续。",
        f"古代史料：《筹办夷务始末（咸丰朝）》；现代参考：{MODERN['opium']}",
        W["qingshigao"],
        ["regime-qing"],
        relations=[
            _rel("event-dierci-yapian-zhanzheng", "part_of", 0.95, "战争第一阶段的条约。"),
        ]),
    _ev("event-beijing-tiaoyue", "《北京条约》与英法联军入京", "treaty",
        1860, 1860, "year", "period-late-qing", "major",
        "咸丰十年（1860 年）9 月，英法联军攻陷通州后进逼北京，咸丰帝北逃热河，"
        "联军于 10 月 18 日焚毁圆明园等园林（属历史事实，中外记载一致）；"
        "清廷被迫签订《北京条约》：增开天津为口岸、割九龙司地方一区、赔款等，第二次鸦片战争结束。",
        f"古代史料：《筹办夷务始末（咸丰朝）》；英法方面记录（《英军华北作战记》等）；现代参考：{MODERN['opium']}",
        W["qingshigao"],
        ["regime-qing"],
        relations=[
            _rel("event-dierci-yapian-zhanzheng", "part_of", 0.95, "战争结束与最终条约。"),
            _rel("event-tianjin-tiaoyue", "follows", 0.9, "天津条约之后城下之盟。"),
        ],
        review_note="圆明园焚毁史实中外档案一致；本事件直述事实，不用情绪化民族主义修辞。"),
]


# ---------------------------------------------------------------------------
# Phase 4 — 洋务运动与边疆（1861—1888）
# ---------------------------------------------------------------------------
PHASE_WESTERN_SELF = [
    _ev("event-yangwu-yundong", "洋务运动（自强求富）", "reform",
        1861, 1894, "range", "period-late-qing", "major",
        "咸丰十一年至光绪二十年（1861—1894 年），清廷部分官僚主持\"自强\"\"求富\"新政："
        "创立总理衙门、兴办近代军事与民用工业、编练新式海陆军、设学堂派留学生；"
        "甲午战争北洋海军覆没后，洋务运动宣告破产。"
        "本事件为 aggregate，子事件（江南制造总局、福州船政、轮船招商局、北洋海军成军）经 part_of 关联。",
        f"古代史料：洋务档案（《洋务运动》资料丛刊）；《清实录·穆宗/德宗实录》；现代参考：{MODERN['yangwu']}",
        W["qingshigao_lu"],
        ["regime-qing"],
        relations=[
            _rel("event-dierci-yapian-zhanzheng", "follows", 0.9, "第二次鸦片战争失败促发自强运动。"),
        ]),
    _ev("event-jiangnan-zaochu", "江南制造总局设立", "economic",
        1865, 1865, "year", "period-late-qing", "major",
        "同治四年（1865 年），李鸿章在上海设立江南机器制造总局，"
        "生产枪炮弹药并译书育人（附设翻译馆），为洋务运动最大军事工厂。",
        f"古代史料：洋务资料丛刊；现代参考：{MODERN['yangwu']}",
        W["qingshigao"],
        ["regime-qing"],
        relations=[
            _rel("event-yangwu-yundong", "part_of", 0.95, "军事工业代表。"),
        ]),
    _ev("event-fuzhou-chuanzheng", "福州船政局设立（马尾船政）", "economic",
        1866, 1866, "year", "period-late-qing", "major",
        "同治五年（1866 年），左宗棠奏设福州船政局（马尾船政），"
        "制造舰船并办船政学堂培养海军人才，为洋务运动最大的造船基地。",
        f"古代史料：洋务资料丛刊；现代参考：{MODERN['yangwu']}",
        W["qingshigao"],
        ["regime-qing"],
        relations=[
            _rel("event-yangwu-yundong", "part_of", 0.95, "船舶工业代表。"),
        ]),
    _ev("event-lunchuan-zhaoshangju", "轮船招商局创办", "economic",
        1872, 1872, "year", "period-late-qing", "major",
        "同治十一年（1872 年），李鸿章创办轮船招商局，为洋务运动中"
        "\"求富\"阶段最早的官督商办民用企业，兼行航运与贸易。",
        f"古代史料：洋务资料丛刊；现代参考：{MODERN['yangwu']}",
        W["qingshigao"],
        ["regime-qing"],
        relations=[
            _rel("event-yangwu-yundong", "part_of", 0.95, "民用企业代表。"),
        ]),
    _ev("event-beiyang-haijun", "北洋海军成军", "political",
        1888, 1888, "year", "period-late-qing", "major",
        "光绪十四年（1888 年），北洋海军正式成军（提督丁汝昌），"
        "拥有定远、镇远等主力舰，一时为远东劲旅；"
        "甲午战争（1894—1895）中北洋海军覆没，洋务海防遂败。",
        f"古代史料：《清实录·德宗实录》；现代参考：{MODERN['yangwu']}",
        W["qingshigao_lu"],
        ["regime-qing"],
        relations=[
            _rel("event-yangwu-yundong", "part_of", 0.95, "海防近代化。"),
        ]),
    _ev("event-agubo-geju", "阿古柏割据南疆", "political",
        1865, 1877, "range", "period-late-qing", "major",
        "同治四年至光绪三年（1865—1877 年），浩罕军阀阿古柏乘西北回民起义之机入疆，"
        "先后占据喀什、乌鲁木齐等南疆与北疆部分地区，建立政权并受英、俄支持；"
        "为左宗棠西征的背景。",
        f"古代史料：《清史稿》相关；左宗棠奏稿；现代参考：{MODERN['late']}",
        W["qingshigao"],
        ["regime-agubo", "regime-qing"],
        relations=[
            _rel("event-zuozongtang-xizheng", "leads_to", 0.95, "新疆被占促使清廷西征。"),
        ]),
    _ev("event-zuozongtang-xizheng", "左宗棠西征收复新疆", "war",
        1876, 1878, "range", "period-late-qing", "major",
        "光绪二年至四年（1876—1878 年），左宗棠督军西征，"
        "先平北疆（乌鲁木齐）再克南疆（喀什），阿古柏败亡（1877 年），"
        "清军收复新疆大部，中原政权重新控制西域。",
        f"古代史料：《左宗棠全集》奏稿；《清实录·德宗实录》；现代参考：{MODERN['late']}",
        W["qingshigao_lu"],
        ["regime-qing", "regime-agubo"],
        relations=[
            _rel("event-agubo-geju", "follows", 0.95, "针对阿古柏政权的军事行动。"),
            _rel("event-xinjiang-jiansheng", "leads_to", 0.9, "收复后清廷将新疆改设行省。"),
        ]),
    _ev("event-xinjiang-jiansheng", "新疆建省", "political",
        1884, 1884, "year", "period-late-qing", "major",
        "光绪十年（1884 年），清廷采纳左宗棠等建议，新疆改设行省，"
        "以刘锦棠为新疆巡抚；新疆由军府治理转为行省体制，"
        "与清朝其他省份同制。",
        f"古代史料：《清实录·德宗实录》；现代参考：{MODERN['late']}",
        W["qingshigao_lu"],
        ["regime-qing"],
        relations=[
            _rel("event-zuozongtang-xizheng", "follows", 0.95, "收复新疆后的政区改革。"),
        ]),
    _ev("event-zhongfa-zhanzheng", "中法战争（越南与西南）", "war",
        1883, 1885, "range", "period-late-qing", "major",
        "光绪九至十一年（1883—1885 年），法国侵略越南北圻并进犯中国西南，"
        "清军（含黑旗军）在镇南关、谅山等地击退法军，"
        "但清廷仍与法国签订《中法新约》，放弃对越宗主权。"
        "本事件为 aggregate，子事件（马尾海战、镇南关大捷、中法新约）经 part_of 关联。",
        f"古代史料：《清实录·德宗实录》；《中法越南交涉资料》；现代参考：{MODERN['late']}",
        W["qingshigao_lu"],
        ["regime-qing"],
        relations=[
            _rel("event-xinjiang-jiansheng", "follows", 0.6, "西南边疆危机同时期的对外战争。"),
        ]),
    _ev("event-mawei-haizhan", "马尾海战（福建水师覆没）", "war",
        1884, 1884, "year", "period-late-qing", "major",
        "光绪十年（1884 年）8 月，法国舰队突袭马尾港（福州），"
        "福建水师未及开战即遭重创，兵舰损失殆尽；"
        "中法战争东南战场清朝海军首次惨败。",
        f"古代史料：《清实录·德宗实录》；现代参考：{MODERN['late']}",
        W["qingshigao_lu"],
        ["regime-qing"],
        relations=[
            _rel("event-zhongfa-zhanzheng", "part_of", 0.95, "东南海战。"),
        ]),
    _ev("event-zhennanguan-dajie", "镇南关大捷与谅山大捷", "war",
        1885, 1885, "year", "period-late-qing", "major",
        "光绪十一年（1885 年）3 月，冯子材督军在镇南关（今友谊关）击溃法军主力，"
        "继复谅山，法军大败；这是中法战争中清军取得的重大胜利，"
        "由此引发法国政局变动（茹费理内阁倒台）。",
        f"古代史料：《清实录》相关奏报；现代参考：{MODERN['late']}",
        W["qingshigao_lu"],
        ["regime-qing"],
        relations=[
            _rel("event-zhongfa-zhanzheng", "part_of", 0.95, "陆路反攻。"),
            _rel("event-zhongfa-xinyue", "leads_to", 0.9, "大捷后仍在条约层面让步。"),
        ]),
    _ev("event-zhongfa-xinyue", "《中法新约》签订", "treaty",
        1885, 1885, "year", "period-late-qing", "major",
        "光绪十一年（1885 年）6 月，清廷与法国签订《中法新约》（《中法会订越南条约十款》）："
        "清廷承认法国对越南的保护权，撤出北圻，开放中越边境陆路通商；"
        "\"中国不败而败，法国不胜而胜\"的概括流行于当时舆论（史家亦有讨论）。",
        f"古代史料：《中法新约》文本；现代参考：{MODERN['late']}",
        W["qingshigao"],
        ["regime-qing"],
        relations=[
            _rel("event-zhongfa-zhanzheng", "part_of", 0.95, "战争结局条约。"),
        ]),
]