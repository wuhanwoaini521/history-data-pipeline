# -*- coding: utf-8 -*-
"""Phase 2 verdicts for the 62 backward EventRelations (agent-assisted review).

Verdicts:
  keep                    — 时序/语义均成立，保留
  keep_with_note          — 并行/era 语境下语义可读，precedes/leads_to 措辞不严格，保留并记录
  recommend_reverse       — 方向与其 desc 或日期矛盾，建议反向
  recommend_delete_or_repoint — 无清晰语义，建议删除或改指向

Index refers to the ordering in scripts/_backward_62.json.
"""
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

V = {
    1: ("keep", "同期对外经略（西域经营与北伐并行），era 内边可接受"),
    2: ("keep_with_note", "「同时期北方后赵崛起」南北并立语境；precedes 仅表叙事先后"),
    3: ("keep", "孙恩卢循之乱中刘裕声望鹊起，因果在重叠期内成立"),
    4: ("keep_with_note", "1 年交错，「南唐与中原政权并存」并立语境"),
    5: ("keep_with_note", "aggregate→开端子事件，语义实为「开端/组成」而非 leads_to；可考虑 part_of"),
    6: ("keep", "新疆被占促使清廷西征，因果成立"),
    7: ("keep", "契丹与五代同期兴起（已验证为合法跨 period 并立）"),
    8: ("keep", "正德朝政失序下宁王起兵，era 内边"),
    9: ("keep", "东林与阉党斗争因果在重叠期内成立"),
    10: ("keep", "崇祯即位与陕西民变同期展开"),
    11: ("keep", "收兵权先于大规模统一作战，因果成立"),
    12: ("keep", "宣和二年同时期事件"),
    13: ("keep", "元嘉之治后期转入北伐，era 内边"),
    14: ("keep_with_note", "府兵制创建(543)早于玉壁之战(546)；「守城取胜强化府兵制构建」因果可读、时序措辞不严谨"),
    15: ("keep", "周武帝改革后出兵灭北齐，因果成立"),
    16: ("keep", "反秦战争发展引出巨鹿之战"),
    17: ("keep", "郑成功依托南明海疆继续抗清，重叠期内成立"),
    18: ("keep", "雍正朝财政与西南改流同步推行"),
    19: ("keep", "北伐期间建立南京国民政府"),
    20: ("keep_with_note", "1 年交错，敌后/正面战场并行语境"),
    21: ("keep", "1944 年反攻期间豫湘桂战役，重叠期内成立"),
    22: ("recommend_reverse", "desc「冉魏亡于前燕扩张」已表明因果与前向指认相反；应为 前燕崛起 leads_to 冉魏"),
    23: ("recommend_reverse", "无 desc；前燕崛起(337..352)整体早于苻坚即位(357)；应反向（秦燕先后崛起对峙）"),
    24: ("keep", "前秦瓦解后后燕等政权并立，同年因果成立"),
    25: ("keep_with_note", "「前秦崩溃中拓跋部重建政权」为 amid 语境，precedes 措辞不严谨"),
    26: ("keep", "南渡期间宋金长江沿线交战，重叠期内成立"),
    27: ("recommend_reverse", "desc「宋蒙战争以南宋灭亡告终」；应为 宋蒙战争 leads_to 崖山海战"),
    28: ("keep", "管仲改革成就齐桓公霸业，era 内因果成立"),
    29: ("keep", "城濮之胜确立霸权（culmination 型，霸业 span 含登位前段）"),
    30: ("keep_with_note", "称霸西戎 span(-659..-621) 大部早于崤之战(-627)；实指「东进受阻后转向西戎」之后期成就，事件自身跨度偏大所致"),
    31: ("keep", "开皇后期废太子，era 内边"),
    32: ("recommend_reverse", "desc「陈朝自557年建立，589年亡」；应为 陈霸先建陈 precedes 隋灭陈"),
    33: ("keep", "营建东都与运河工程同期展开"),
    34: ("keep_with_note", "炀帝前期西征与运河工程并举（政策群并行）"),
    35: ("keep", "河北与河南民变并立"),
    36: ("keep", "杜伏威据江淮与隋亡相先后"),
    37: ("keep_with_note", "隋末群雄并行语境"),
    38: ("keep", "统一战争后期发生玄武门之变，era 内边"),
    39: ("keep", "虎牢大捷后完成统一（culmination 型）"),
    40: ("keep", "贞观对外扩张以灭东突厥为标志，era 内边"),
    41: ("keep_with_note", "「太宗末年同时经营西域与东征高句丽」并行语境"),
    42: ("keep_with_note", "「高宗承太宗基业」为承接语境，非严格先后"),
    43: ("keep", "废王立武与灭西突厥同期，重叠期内成立"),
    44: ("recommend_reverse", "desc「白江口之战（663）先行斩断日本援军」；应为 白江口 precedes 唐灭高句丽"),
    45: ("keep_with_note", "「对外战线由东转向西」转段叙事；目标在前 2 年可接受"),
    46: ("recommend_delete_or_repoint", "无 desc；武则天临朝(683..690)无法先于大非川之战(670)，亦无清晰因果；建议删除或改指向武周/吐蕃相关事件"),
    47: ("keep", "姚宋整顿促成开元盛世（culmination 型）"),
    48: ("keep", "开元末李林甫执政、天宝由盛转衰，era 尾边"),
    49: ("recommend_reverse", "desc「吐蕃自大非川之胜后持续东进」；应为 大非川之战 precedes 吐蕃攻入长安"),
    50: ("keep", "两税法面对藩镇分权的财政回应"),
    51: ("keep", "削藩成功造就元和中兴（culmination 型）"),
    52: ("keep_with_note", "desc 意为「中兴之后宦官更张」，但目标事件(神策中尉确立 796..806)早于中兴主段；建议后续改指向更晚的宦官事件"),
    53: ("keep", "党争持续至会昌年间，era 尾边"),
    54: ("keep_with_note", "党争(821 起)早于甘露之变(835)；desc 言「甘露变后继续缠斗」，era 语境"),
    55: ("keep", "王仙芝败后黄巢领其众，因果成立"),
    56: ("keep", "平巢诸镇中朱温坐大，因果成立"),
    57: ("keep_with_note", "1 年交错，吴蜀并立语境"),
    58: ("keep_with_note", "姜维北伐(247 起)早于高平陵(249)，并行语境"),
    59: ("keep_with_note", "李悝变法(-406 起)略早于三家分晋(-403)；desc 已注明「魏国李悝变法为其中最早者」，变法浪潮叙事可读"),
    60: ("keep", "文景后期削藩问题浮出，era 尾边"),
    61: ("keep", "理财扩张与行省体制同期的财政政治"),
    62: ("keep", "西北诸王战争(1277 起)确实先于乃颜之乱(1287)爆发"),
}

rows = json.load(open("scripts/_backward_62.json", encoding="utf-8"))
assert len(rows) == 62 and len(V) == 62

out = []
for i, r in enumerate(rows, 1):
    verdict, note = V[i]
    out.append({
        "idx": i, "src": r["src"], "tgt": r["tgt"],
        "rel": r["rel"], "gap": r["tgt_start"] - r["src_end"],
        "verdict": verdict, "note": note,
    })

from collections import Counter
c = Counter(o["verdict"] for o in out)
print(dict(c))
assert sum(c.values()) == 62

with open("scripts/_backward_62_verdicts.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("saved scripts/_backward_62_verdicts.json")
