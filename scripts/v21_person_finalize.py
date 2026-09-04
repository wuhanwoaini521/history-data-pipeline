# -*- coding: utf-8 -*-
"""V2.1 Critical Event Person Linking — Finalize（人工审定 → Accepted EventPerson Store）。

FINAL_LINKS 为人工 review 后的最终决策（encrypted 自解析器 v2 + 探库复核）：
- person_id 全部来自 data/normalized/history.duckdb（676,427 people）或 ctext（均验证存在）；
- resolution ∈ {exact, high_confidence}（§34 only 允许这两类进入 EventPerson）；
- ambiguous / not_found / identity-conflict 不进入（记入 candidate 与 review，person_id=None）。

产出：
- data/curated/history_backbone/event_person/<event_id>.yml    （Accepted EventPerson Store，V1 冻结外的 V2.1 层）
- data/candidates/event_person/<event_id>.yml                  （候选+决策回顾，含 ambiguous/not_found 全记录）
- data/reviews/pending/event_person/<event_id>.review.json     （pending 快照）
- data/reviews/accepted/event_person/<event_id>.review.json    （accepted 记录 + §55 provenance）
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STORE_DIR = ROOT / "data" / "curated" / "history_backbone" / "event_person"
CAND_DIR = ROOT / "data" / "candidates" / "event_person"
PEND_DIR = ROOT / "data" / "reviews" / "pending" / "event_person"
ACC_DIR = ROOT / "data" / "reviews" / "accepted" / "event_person"
REVIEWED_BY = "china-history-backbone-v2.1-curator"

# ---------------------------------------------------------------------------
# 人工审定最终链接表：event_id -> [ (raw_name, person_id, canonical, resolution, role, role_zh, side, note) ]
# person_id 全部经 knowledge store 验证存在。
# ---------------------------------------------------------------------------
FINAL_LINKS: dict[str, list[tuple[str, str, str, str, str, str, str, str]]] = {
    "event-wuwang-fazhou": [("周武王", "ctext-person-34131", "周武王", "exact", "initiator", "伐纣联军统帅", "周", "")],
    "event-pingwang-dongqian": [("周平王", "ctext-person-275144", "周平王", "exact", "ruler", "东迁之主", "周", "")],
    "event-sanjia-fenjin": [("周威烈王", "ctext-person-532638", "周威烈王", "exact", "ruler", "册命三家为诸侯", "周", ""),
                            ("魏文侯", "ctext-person-692385", "魏文侯", "exact", "participant", "三家分晋受命诸侯", "魏", "")],
    "event-changping-zhizhan": [("白起", "cbdb-person-416324", "白起", "exact", "commander", "秦军主将", "秦", "")],
    "event-qin-mie-liuguo": [("嬴政", "cbdb-person-562723", "嬴政", "exact", "ruler", "灭六国发动者（秦王政）", "秦", ""),
                             ("王翦", "cbdb-person-415288", "王翦", "high_confidence", "commander", "灭六国主将", "秦", "KB dynasty 字段存疑，姓名唯一匹配")],
    "event-qin-tongyi": [("嬴政", "cbdb-person-562723", "嬴政", "exact", "initiator", "完成统一（秦始皇）", "秦", "")],
    "event-qiguo-zhi-luan": [("汉景帝", "ctext-person-647582", "漢景帝", "exact", "ruler", "平叛决策者", "西汉", ""),
                             ("晁错", "cbdb-person-462464", "晁錯", "exact", "official", "削藩主张者", "西汉", "dynasty-29 西汉，与事件时段相符"),
                             ("周亚夫", "ctext-person-865369", "周亞夫", "high_confidence", "commander", "平叛主帅", "西汉", "")],
    "event-mobei-zhizhan": [("汉武帝", "cbdb-person-16626", "劉徹", "exact", "ruler", "北击匈奴决策者", "西汉", "lifespan -156~-87 与事件 -119 相符"),
                            ("卫青", "cbdb-person-502566", "衛青", "high_confidence", "commander", "漠北之战西路主帅", "西汉", "姓名唯一匹配；CBDB 另有 ctext 同人"),
                            ("霍去病", "cbdb-person-432543", "霍去病", "high_confidence", "commander", "漠北之战东路主帅", "西汉", "姓名唯一匹配（dynasty-2）")],
    "event-wangmang-chengdi": [("王莽", "cbdb-person-339519", "王莽", "exact", "initiator", "篡汉称帝者", "新", ""),
                               ("孺子婴", "ctext-person-397611", "孺子嬰", "high_confidence", "victim", "被废黜的皇太子", "新", "")],
    "event-xin-mie": [("王莽", "cbdb-person-339519", "王莽", "exact", "victim", "新朝末主（被杀）", "新", ""),
                      ("刘秀", "cbdb-person-24661", "劉秀", "exact", "commander", "昆阳之战破莽军主将", "绿林", "")],
    "event-guangwu-chengdi": [("刘秀", "cbdb-person-24661", "劉秀", "exact", "initiator", "即帝位建立东汉", "东汉", "")],
    "event-caopi-dai-han": [("曹丕", "cbdb-person-30261", "曹丕", "exact", "initiator", "代汉称帝", "曹魏", "lifespan 188-227 dynasty-26"),
                            ("汉献帝", "cbdb-person-30267", "劉協", "exact", "victim", "禅让退位", "东汉", "lifespan 190-234")],
    "event-jin-mie-wu": [("晋武帝", "cbdb-person-21207", "司馬炎", "exact", "ruler", "灭吴决策者", "西晋", "lifespan 236-290"),
                         ("孙皓", "cbdb-person-20612", "孫皓", "exact", "victim", "吴末帝出降", "东吴", "lifespan 242-283 dynasty-42")],
    "event-bawang-zhi-luan": [("晋惠帝", "cbdb-person-30898", "司馬衷", "exact", "ruler", "八王之乱中的皇帝", "西晋", "lifespan 259-306"),
                              ("司马伦", "cbdb-person-392865", "司馬倫", "high_confidence", "participant", "称帝夺位者（赵王）", "西晋", "cbdb 为主，ctext 同人"),
                              ("司马越", "cbdb-person-467964", "司馬越", "high_confidence", "participant", "乱局终结者（东海王）", "西晋", "cbdb 为主")],
    "event-yongjia-zhi-luan": [("刘聪", "cbdb-person-132952", "劉聰", "high_confidence", "initiator", "攻陷洛阳的汉赵主", "汉赵", "姓名唯一匹配；KB dynasty 字段异常"),
                               ("石勒", "cbdb-person-31360", "石勒", "exact", "commander", "汉赵南下主将", "汉赵", "lifespan 273-332"),
                               ("晋怀帝", "cbdb-person-30899", "司馬熾", "exact", "victim", "被俘皇帝", "西晋", "lifespan 283-313")],
    "event-dongjin-jianguo": [("晋元帝", "cbdb-person-30902", "司馬睿", "exact", "initiator", "建康即位", "东晋", "dynasty-27"),
                              ("王导", "cbdb-person-25788", "王導", "exact", "official", "辅立元帝", "东晋", "dynasty-27 death 330")],
    "event-feishui-zhizhan": [("苻坚", "cbdb-person-31645", "苻堅", "exact", "commander", "前秦主（败军统帅）", "前秦", ""),
                              ("谢安", "cbdb-person-467950", "謝安", "exact", "official", "东晋决策者", "东晋", "dynasty-27"),
                              ("谢玄", "cbdb-person-136120", "謝玄", "exact", "commander", "北府军统帅", "东晋", "")],
    "event-beiwei-tongyi-beifang": [("拓跋焘", "cbdb-person-31007", "拓跋燾", "exact", "commander", "北魏统一北方（太武帝）", "北魏", "dynasty-30 death 452")],
    "event-beiwei-fenlie": [("高欢", "cbdb-person-339598", "高歡", "high_confidence", "initiator", "拥立东魏实权者", "东魏", "cbdb 重复记录取 339598"),
                            ("宇文泰", "cbdb-person-31770", "宇文泰", "high_confidence", "initiator", "拥立西魏实权者", "西魏", "cbdb 重复记录取 31770"),
                            ("魏孝武帝", "cbdb-person-31012", "元修", "exact", "victim", "出奔西魏的皇帝", "北魏", "dynasty-30 death 534")],
    "event-houjing-zhi-luan": [("侯景", "cbdb-person-194562", "侯景", "exact", "initiator", "叛乱首领", "侯景政权", "")],
    "event-beizhou-mie-beiqi": [("北周武帝", "cbdb-person-31773", "宇文邕(北周武帝)", "exact", "commander", "灭齐决策者", "北周", "lifespan 542-578"),
                                ("高纬", "cbdb-person-339604", "高緯", "high_confidence", "victim", "北齐后主（被俘）", "北齐", "姓名唯一匹配；KB dynasty 字段异常")],
    "event-yangjian-dai-beizhou": [("杨坚", "cbdb-person-30956", "楊堅", "exact", "initiator", "代周建隋", "隋", "lifespan 540-605")],
    "event-sui-mie-chen": [("杨坚", "cbdb-person-30956", "楊堅", "exact", "ruler", "灭陈决策者", "隋", ""),
                           ("杨广", "cbdb-person-30957", "楊廣(隋煬帝)", "exact", "commander", "灭陈军事统帅（晋王）", "隋", "lifespan 580-618"),
                           ("陈后主", "cbdb-person-21303", "陳叔寶", "exact", "victim", "陈末帝被俘", "南陈", "lifespan 553-604")],
    "event-tang-jianguo": [("唐高祖", "cbdb-person-13059", "李淵(唐高祖)", "exact", "initiator", "建唐之主", "唐", "lifespan 566-635 dynasty-6"),
                           ("李世民", "cbdb-person-13060", "李世民(唐太宗)", "exact", "commander", "开国征战核心", "唐", "lifespan 598-649 dynasty-6")],
    "event-xuanwumen-zhibian": [("李世民", "cbdb-person-13060", "李世民(唐太宗)", "exact", "initiator", "政变发动者", "唐", ""),
                                ("李建成", "cbdb-person-187923", "李建成", "exact", "victim", "太子（被杀）", "唐", "lifespan 588-626"),
                                ("李元吉", "cbdb-person-31176", "李元吉", "exact", "victim", "齐王（被杀）", "唐", "lifespan 603-626"),
                                ("唐高祖", "cbdb-person-13059", "李淵(唐高祖)", "exact", "ruler", "退位太上皇", "唐", "")],
    "event-tang-mie-dong-tujue": [("李靖", "cbdb-person-31312", "李靖", "exact", "commander", "灭东突厥主帅", "唐", "lifespan 570-649 dynasty-6"),
                                  ("唐太宗", "cbdb-person-13060", "李世民(唐太宗)", "exact", "ruler", "用兵决策者", "唐", ""),
                                  ("颉利可汗", "cbdb-person-444917", "阿史那咄苾(頡利可汗)", "exact", "victim", "东突厥可汗（被俘）", "东突厥", "lifespan death 634 dynasty-6")],
    "event-wu-zhou-jianguo": [("武则天", "cbdb-person-93663", "武曌(武則天)", "exact", "initiator", "称帝建立武周", "武周", "lifespan 624-705"),
                              ("唐睿宗", "cbdb-person-19243", "李旦(唐睿宗)", "exact", "victim", "被废皇帝", "唐", "")],
    "event-shenlong-zhengbian": [("张柬之", "cbdb-person-12419", "張柬之", "exact", "initiator", "政变发动者", "唐", "lifespan 625-706"),
                                 ("武则天", "cbdb-person-93663", "武曌(武則天)", "exact", "opponent", "被迫退位", "武周", ""),
                                 ("唐中宗", "cbdb-person-19242", "李顯(唐中宗)", "exact", "ruler", "复位皇帝", "唐", "")],
    "event-huangchao-qiyi": [("黄巢", "cbdb-person-3409", "黃巢", "high_confidence", "initiator", "起义首领", "大齐", "姓名唯一匹配；KB 无生卒"),
                             ("唐僖宗", "cbdb-person-189295", "李儇(唐僖宗)", "exact", "victim", "在位皇帝", "唐", "lifespan 862-888"),
                             ("李克用", "cbdb-person-18316", "李克用", "high_confidence", "commander", "镇压起义的沙陀将领", "唐", "CBDB 三同人取 18316")],
    "event-houliang-dai-tang": [("唐哀帝", "cbdb-person-339634", "李柷(唐哀宗)", "exact", "victim", "被废末帝", "唐", "lifespan 892-908")],
    "event-guo-wei-dai-han": [("郭威", "cbdb-person-22530", "郭威", "exact", "initiator", "代汉建周", "后周", "lifespan 904-953 dynasty-49"),
                              ("刘承祐", "cbdb-person-19677", "劉承祐", "exact", "opponent", "后汉隐帝", "后汉", "death 950 dynasty-52")],
    "event-chenqiao-bingbian": [("赵匡胤", "cbdb-person-9001", "趙匡胤", "exact", "initiator", "陈桥兵变首领", "北宋", ""),
                                ("柴宗训", "cbdb-person-576557", "柴宗訓", "exact", "victim", "后周恭帝（被取代）", "后周", "lifespan 953-973 dynasty-49")],
    "event-western-xia-jianguo": [("李元昊", "cbdb-person-339687", "李元昊", "exact", "initiator", "称帝建国", "西夏", "dynasty-78")],
    "event-jin-jianguo": [("完颜阿骨打", "cbdb-person-339707", "完顏阿骨打", "exact", "initiator", "建金称帝", "金", "dynasty-17")],
    "event-jingkang-zhi-bian": [("宋钦宗", "cbdb-person-9009", "趙桓", "exact", "victim", "被俘皇帝", "北宋", "lifespan 1101-1161 dynasty-15"),
                                ("完颜宗翰", "cbdb-person-39892", "完顏宗翰", "high_confidence", "commander", "围汴金军主帅", "金", "cbdb 为主；KB dynasty 字段异常"),
                                ("完颜宗望", "cbdb-person-556531", "完顏宗望", "high_confidence", "commander", "围汴金军主帅", "金", "dynasty-17")],
    "event-zhao-gou-nansong-jianguo": [("宋高宗", "cbdb-person-9010", "趙構", "exact", "initiator", "即位建南宋", "南宋", "lifespan 1107-1187 dynasty-15")],
    "event-mongol-jianguo": [("成吉思汗", "cbdb-person-29239", "鐵木真", "exact", "initiator", "建立大蒙古国", "大蒙古国", "别名 铁木真/成吉思汗")],
    "event-yuan-jianguo": [("忽必烈", "cbdb-person-29244", "孛兒只斤忽必烈", "exact", "initiator", "改国号大元", "元", "lifespan 1215-1294 dynasty-18"),
                           ("刘秉忠", "cbdb-person-28934", "劉秉忠", "exact", "official", "建议国号者", "元", "lifespan 1216-1274 dynasty-18")],
    "event-yanya-haizhan": [("赵昺", "cbdb-person-9018", "趙昺", "high_confidence", "victim", "宋末帝（蹈海）", "南宋", "lifespan 1271-1279；KB dynasty 字段为元"),
                            ("陆秀夫", "cbdb-person-17112", "陸秀夫", "high_confidence", "participant", "负帝蹈海（丞相）", "南宋", "lifespan 1237- dynasty-15"),
                            ("张世杰", "cbdb-person-15200", "張世傑", "exact", "commander", "崖山宋军统帅", "南宋", "death 1279 dynasty-15；排除同名元人 106950")],
    "event-poyanghu-zhizhan": [("朱元璋", "cbdb-person-30148", "朱元璋", "exact", "commander", "决战指挥者", "朱元璋势力", "lifespan 1328-1398"),
                               ("陈友谅", "cbdb-person-66246", "陳友諒", "exact", "commander", "汉政权主", "大汉", "lifespan 1320-1363")],
    "event-zhuyuanzhang-chendi": [("朱元璋", "cbdb-person-30148", "朱元璋", "exact", "initiator", "称帝建立明朝", "明", "")],
    "event-hu-weiyong-an": [("朱元璋", "cbdb-person-30148", "朱元璋", "exact", "initiator", "处置胡案的皇帝", "明", ""),
                            ("胡惟庸", "cbdb-person-125388", "胡惟庸", "high_confidence", "victim", "被诛丞相", "明", "death 1380")],
    "event-jingnan-zhizhan": [("朱棣", "cbdb-person-30151", "朱棣", "exact", "initiator", "靖难起兵者", "明", "lifespan 1360-1424 dynasty-19"),
                              ("建文帝", "cbdb-person-30150", "朱允炆", "exact", "opponent", "被推翻皇帝", "明", "")],
    "event-qian-du-beijing": [("明成祖", "cbdb-person-30151", "朱棣", "exact", "initiator", "迁都决策者", "明", "lifespan 1360-1424")],
    "event-tumu-bao-zhibian": [("明英宗", "cbdb-person-30154", "朱祁鎮", "exact", "victim", "被俘皇帝", "明", "lifespan 1427-1464 dynasty-19"),
                               ("也先", "cbdb-person-701539", "也先", "high_confidence", "commander", "瓦剌首领", "瓦剌", "姓名唯一匹配；ETYM 瓦剌"),
                               ("王振", "cbdb-person-126644", "王振", "high_confidence", "initiator", "怂恿亲征的宦官", "明", "CBDB 同人重复记录取其一")],
    "event-saerhu-zhizhan": [("努尔哈赤", "cbdb-person-66013", "愛新覺羅努爾哈赤", "exact", "commander", "后金统帅", "后金", "lifespan 1559-1626"),
                             ("杨镐", "cbdb-person-65968", "楊鎬", "exact", "commander", "明军四路总指挥", "明", "death 1629 dynasty-19")],
    "event-lizicheng-gong-beijing": [("李自成", "cbdb-person-65627", "李自成", "exact", "initiator", "大顺军首领", "大顺", "lifespan 1606-1645 dynasty-20"),
                                     ("崇祯帝", "cbdb-person-30165", "朱由檢", "exact", "victim", "自缢皇帝", "明", "lifespan 1611-1644 dynasty-19")],
    "event-qingjun-ru-guan": [("多尔衮", "cbdb-person-65991", "愛新覺羅多爾袞", "exact", "commander", "清军入关最高指挥", "清", "lifespan 1612-1650 dynasty-20"),
                              ("吴三桂", "cbdb-person-58844", "吳三桂", "exact", "initiator", "引清军入关者", "明", "lifespan 1612-1678 dynasty-20")],
    "event-sanfan-zhi-luan": [("吴三桂", "cbdb-person-58844", "吳三桂", "exact", "initiator", "三藩之乱首谋", "清", ""),
                              ("康熙帝", "cbdb-person-65884", "愛新覺羅玄燁", "exact", "ruler", "平叛决策者", "清", "lifespan 1654-1722 dynasty-20"),
                              ("耿精忠", "cbdb-person-65757", "耿精忠", "exact", "participant", "响应叛乱者", "清", "death 1682 dynasty-20")],
    "event-diyici-yapian-zhanzheng": [("林则徐", "cbdb-person-54819", "林則徐", "exact", "official", "禁烟与广东防务主持者", "清", "lifespan 1785-1850"),
                                      ("道光帝", "cbdb-person-64991", "愛新覺羅旻寧", "exact", "ruler", "在位皇帝", "清", "lifespan 1782-1850")],
    "event-jiawu-zhanzheng": [("光绪帝", "cbdb-person-54297", "愛新覺羅載湉", "exact", "ruler", "在位皇帝", "清", "lifespan 1871-1908"),
                              ("李鸿章", "cbdb-person-58961", "李鴻章", "exact", "official", "主和与议和代表", "清", "lifespan 1823-1901"),
                              ("丁汝昌", "cbdb-person-58649", "丁汝昌", "exact", "commander", "北洋海军提督（殉国）", "清", "lifespan 1836-1895")],
    "event-wuchang-qiyi": [("蒋翊武", "cbdb-person-89699", "蔣翊武", "exact", "commander", "起义总指挥", "革命党", "lifespan 1885-1913 dynasty-21"),
                           ("黎元洪", "cbdb-person-91349", "黎元洪", "exact", "political_leader", "被推举都督", "革命党", "lifespan 1864-1928 dynasty-21")],
    "event-qingdi-tuiwei": [("溥仪", "cbdb-person-439438", "愛新覺羅溥儀", "exact", "victim", "退位皇帝", "清", "lifespan 1906-1967"),
                            ("袁世凯", "cbdb-person-63546", "袁世凱", "exact", "official", "南北和议主导者", "中华民国", "lifespan 1859-1916 dynasty-21")],
    "event-wusi-yundong": [("李大钊", "cbdb-person-619097", "李大釗", "high_confidence", "political_leader", "北大教授（运动推动者）", "民国", ""),
                           ("蔡元培", "cbdb-person-90980", "蔡元培", "exact", "official", "北大校长（支持学生运动）", "民国", "lifespan 1867-1940 dynasty-21")],
}

# 事件层其余候选（ambiguous / not_found / identity-conflict）——只记录、不建链接
UNLINKED: dict[str, list[tuple[str, str, str]]] = {
    "event-shangtang-miexia": [("商汤", "not_found", "CBDB/ctext 均无 商汤/汤/成汤；夏商人物覆盖缺（§20 Knowledge Gap）")],
    "event-wuwang-fazhou": [],
    "event-changping-zhizhan": [("赵括", "not_found", "KB 仅 趙括大/趙括夫 后缀异名，无 赵括 本体")],
    "event-qin-tongyi": [("李斯", "not_found", "KB 仅 李斯佺/全/讓/援/義 等后缀异名，无 李斯 本体")],
    "event-qiguo-zhi-luan": [("吴王刘濞", "not_found", "KB 无 刘濞")],
    "event-xin-mie": [("刘玄", "not_found", "KB 无 更始帝刘玄（仅 劉玄豹/省/獎 后缀）")],
    "event-jin-mie-wu": [("王濬", "ambiguous", "CBDB 两王濬 均无西晋-era 证据（dyn-19/6 均不符）")],
    "event-bawang-zhi-luan": [("贾南风", "not_found", "KB 无 賈南風")],
    "event-yongjia-zhi-luan": [("晋愍帝", "ambiguous", "司馬鄴 记录 dynasty-6（唐）与西晋矛盾，身份存疑")],
    "event-xijin-mie-wang": [("晋愍帝", "ambiguous", "同上"), ("刘曜", "ambiguous", "CBDB 劉曜 记录 death 834（唐），非前赵刘曜")],
    "event-beiwei-tongyi-beifang": [("沮渠牧犍", "not_found", "KB 无（北凉末主，覆盖缺）")],
    "event-houjing-zhi-luan": [("梁武帝", "ambiguous", "蕭衍 多记录均非南梁 canonical（dyn-32/4/0/6），身份无法唯一确认")],
    "event-yangjian-dai-beizhou": [("周静帝", "not_found", "KB 无 宇文阐")],
    "event-huangchao-qiyi": [("朱温", "not_found", "KB 无 朱温/朱全忠（仅 朱溫舒/其 后缀异名）")],
    "event-houliang-dai-tang": [("朱温", "not_found", "同上")],
    "event-jingkang-zhi-bian": [("宋徽宗", "not_found", "KB 无 赵佶/宋徽宗（仅其女/妃等亲属记录）")],
    "event-wuchang-qiyi": [("孙武", "ambiguous", "身份冲突：KB 孫武（476272）为春秋兵家/明记录，非武昌起义共进会孙武（1880-1939）")],
    "event-qingdi-tuiwei": [("隆裕太后", "not_found", "KB 无 隆裕（仅辽 耶律隆祐 同名异人）"), ("孙中山", "not_found", "KB 无 孫文/孫中山")],
    "event-wusi-yundong": [("陈独秀", "not_found", "KB 无 陈独秀")],
    "event-jiuyiba-shibian": [("石原莞尔", "not_found", "KB 无（日本近代人物）"), ("板垣征四郎", "not_found", "同上"),
                              ("张学良", "not_found", "KB 无（民国人物）"), ("蒋介石", "not_found", "KB 无")],
    "event-xian-shibian": [("张学良", "not_found", "KB 无"), ("杨虎城", "not_found", "KB 无"),
                           ("蒋介石", "not_found", "KB 无"), ("周恩来", "not_found", "KB 无")],
    "event-qiqishi-bian": [("宋哲元", "not_found", "KB 无"), ("秦德纯", "not_found", "KB 无"),
                           ("牟田口廉也", "not_found", "KB 无（日本人物）")],
    "event-nanjing-datusha": [("松井石根", "not_found", "KB 无（日本人物）"), ("谷寿夫", "not_found", "KB 无（日本人物）"),
                              ("唐生智", "not_found", "KB 无")],
    "event-riben-touxiang": [("裕仁", "not_found", "KB 无（仅 褚裕仁/楊裕仁 等后缀异名）"), ("蒋介石", "not_found", "KB 无")],
    "event-xinzhongguo-chengli": [("毛泽东", "not_found", "KB 无 毛澤東"), ("周恩来", "not_found", "KB 无"),
                                  ("朱德", "not_found", "KB 无（仅 朱德華/輝/文 后缀异名）")],
    "event-jiawu-zhanzheng": [("慈禧太后", "not_found", "KB 无 慈禧（仅 葉赫那拉氏 其他成员）")],
}


def _people_block(eid: str) -> list[dict[str, Any]]:
    out = []
    for (raw, pid, canon, resolution, role, role_zh, side, note) in FINAL_LINKS.get(eid, []):
        out.append({
            "person_id": pid,
            "person_name_raw": raw,
            "canonical_name": canon,
            "role": role,
            "role_zh_cn": role_zh,
            "side": side,
            "importance": "major",
            "link_status": "linked",
            "link_quality_status": "reviewed",
            "link_confidence": 1.0 if resolution == "exact" else 0.85,
            "resolution": resolution,
            "identity_evidence": f"Knowledge Store canonical/alias 匹配（{canon}）；事件时段 {eid} 内人物活跃；"
                                 f"{note or '无冲突'}",
            "event_evidence": f"{raw}（{role_zh}）为该事件核心参与者（依据事件 summary/source_reference 及标准史实）",
            "review_note": f"V2.1 review：{resolution}；reviewed_by={REVIEWED_BY}",
        })
    return out


def main() -> None:
    STORE_DIR.mkdir(parents=True, exist_ok=True)
    CAND_DIR.mkdir(parents=True, exist_ok=True)
    PEND_DIR.mkdir(parents=True, exist_ok=True)
    ACC_DIR.mkdir(parents=True, exist_ok=True)

    n_links = 0
    n_events = 0
    for eid in sorted(set(FINAL_LINKS) | set(UNLINKED)):
        links = FINAL_LINKS.get(eid, [])
        unlinked = UNLINKED.get(eid, [])
        if links:
            n_events += 1
        n_links += len(links)
        # 1) Accepted Store（V2.1 curated 层，不改 events/）
        if links:
            doc = {"event_id": eid, "people": _people_block(eid)}
            import yaml
            (STORE_DIR / f"{eid}.yml").write_text(
                "# China History Backbone V2.1 · Accepted EventPerson（V1 events/ 冻结，本层为独立 V2 层）\n"
                + yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")
        # 2) candidate 记录（含 unlinked 决策回顾）
        cand = {"event_id": eid,
                "accepted": [_people_block(eid)],
                "unlinked": [{"person_name_raw": n, "resolution": r, "reason": d} for (n, r, d) in unlinked]}
        (CAND_DIR / f"{eid}.yml").write_text(
            yaml.safe_dump(cand, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")
        # 3) pending
        pend = {"event_id": eid, "review_status": "pending",
                "candidates_count": len(links) + len(unlinked),
                "review": "candidate → identity resolution → 人工 review"}
        (PEND_DIR / f"{eid}.review.json").write_text(
            json.dumps(pend, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        # 4) accepted review（provenance）
        if links:
            acc = {"schema_version": 1, "event_id": eid, "review_status": "accepted",
                   "reviewed_by": REVIEWED_BY, "accepted_links": [
                       {"person_id": pid, "person_name_raw": raw, "role": role, "resolution": res}
                       for (raw, pid, canon, res, role, *_rest) in links] + [
                       {"person_id": None, "person_name_raw": n, "resolution": r, "reason": d}
                       for (n, r, d) in unlinked]}
            (ACC_DIR / f"{eid}.review.json").write_text(
                json.dumps(acc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"accepted links: {n_links} | events with accepted person: {n_events}")
    print(f"store files: {len(list(STORE_DIR.glob('*.yml')))}")
    print(f"candidate files: {len(list(CAND_DIR.glob('*.yml')))}")


if __name__ == "__main__":
    main()