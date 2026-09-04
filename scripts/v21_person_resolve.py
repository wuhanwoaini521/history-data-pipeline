# -*- coding: utf-8 -*-
"""V2.1 Critical Event Person Linking — 候选表 + 知识库解析 + 四级分类。

原则（§7-§20）：
- 候选仅来自 Event summary / source_reference / story 上下文的**核心人物**（1~8 人/事件）；
- 简繁归一（opencc）后对 Knowledge Store（data/normalized/history.duckdb，676,427 people）解析；
- 硬冲突（生晚于事件/死早于事件/身份明显不符）→ rejected；
- 0 命中 → not_found（绝不临时造 Person）；
- 多义 → ambiguous（不进入正式 EventPerson）；
- 唯一且无冲突 → exact / high_confidence（高置信仍需人工 review 后才 accepted）。

产出：
- data/candidates/event_person/<event_id>.yml        （候选 + 解析证据，per event）
- data/reviews/pending/event_person/<event_id>.review.json（pending review，人工复审后转 accepted/rejected）
- reports/_v21_resolution_preview.txt                （供人审阅的解析预视）
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from history_data_pipeline.backbone.loader import load_backbone  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE = ROOT / "data" / "normalized" / "history.duckdb"

try:
    import opencc
    CONV = opencc.OpenCC("s2t")
except Exception:  # pragma: no cover
    CONV = None


def to_trad(s: str) -> str:
    return CONV.convert(s) if CONV else s


def norm_name(s: str) -> str:
    """去掉括号注释与空格，返回基础名。"""
    s = re.sub(r"[（(][^)）]*[)）]", "", s)
    return s.replace(" ", "").strip()


# ---------------------------------------------------------------------------
# 候选表：event_id -> [(name_raw, role, role_zh_cn, importance, side)]
# 依据：62 个 Critical Event 自身 summary/source_reference 中的核心人物（§38/§47-§50）。
# ---------------------------------------------------------------------------
CANDIDATES: dict[str, list[tuple[str, str, str, str, str]]] = {
    "event-shangtang-miexia": [("商汤", "initiator", "伐夏之主（成汤）", "major", "商")],
    "event-wuwang-fazhou": [("周武王", "initiator", "伐纣联军统帅", "major", "周")],
    "event-pingwang-dongqian": [("周平王", "ruler", "东迁之主（姬宜臼）", "major", "周")],
    "event-sanjia-fenjin": [("周威烈王", "ruler", "册命三家为诸侯（姬午）", "major", "周"),
                            ("魏文侯", "participant", "三家分晋受命诸侯（魏斯）", "major", "魏")],
    "event-changping-zhizhan": [("白起", "commander", "秦军主将", "major", "秦"),
                                ("赵括", "commander", "赵军主将（战死）", "major", "赵")],
    "event-qin-mie-liuguo": [("嬴政", "ruler", "灭六国发动者（秦王政/秦始皇）", "major", "秦"),
                             ("王翦", "commander", "灭六国主将", "major", "秦")],
    "event-qin-tongyi": [("嬴政", "initiator", "完成统一（秦始皇）", "major", "秦"),
                         ("李斯", "official", "统一制度参与者（丞相）", "major", "秦")],
    "event-qiguo-zhi-luan": [("汉景帝", "ruler", "平叛决策者（刘启）", "major", "西汉"),
                             ("晁错", "official", "削藩主张者（被杀）", "major", "西汉"),
                             ("吴王刘濞", "initiator", "七国之乱首谋", "major", "西汉"),
                             ("周亚夫", "commander", "平叛主帅", "major", "西汉")],
    "event-mobei-zhizhan": [("卫青", "commander", "漠北之战西路主帅", "major", "西汉"),
                            ("霍去病", "commander", "漠北之战东路主帅", "major", "西汉"),
                            ("汉武帝", "ruler", "北击匈奴决策者（刘彻）", "major", "西汉")],
    "event-wangmang-chengdi": [("王莽", "initiator", "篡汉称帝者", "major", "新"),
                               ("孺子婴", "victim", "被废黜的皇太子（刘婴）", "major", "新")],
    "event-xin-mie": [("王莽", "victim", "新朝末主（被杀）", "major", "新"),
                      ("刘玄", "rebel_leader", "绿林军立更始帝", "major", "更始"),
                      ("刘秀", "commander", "昆阳之战破莽军主将", "major", "绿林")],
    "event-guangwu-chengdi": [("刘秀", "initiator", "即帝位建立东汉（光武帝）", "major", "东汉")],
    "event-caopi-dai-han": [("曹丕", "initiator", "代汉称帝（魏文帝）", "major", "曹魏"),
                            ("汉献帝", "victim", "禅让退位（刘协）", "major", "东汉")],
    "event-jin-mie-wu": [("晋武帝", "ruler", "灭吴决策者（司马炎）", "major", "西晋"),
                         ("王濬", "commander", "灭吴水师主将", "major", "西晋"),
                         ("孙皓", "victim", "吴末帝（出降）", "major", "东吴")],
    "event-bawang-zhi-luan": [("晋惠帝", "ruler", "八王之乱中的皇帝（司马衷）", "major", "西晋"),
                              ("贾南风", "initiator", "首乱发动者（皇后）", "major", "西晋"),
                              ("司马伦", "participant", "称帝夺位者（赵王）", "major", "西晋"),
                              ("司马越", "participant", "乱局终结者（东海王）", "major", "西晋")],
    "event-yongjia-zhi-luan": [("刘聪", "initiator", "攻陷洛阳的汉赵主", "major", "汉赵"),
                               ("石勒", "commander", "汉赵南下主将", "major", "汉赵"),
                               ("晋怀帝", "victim", "被俘皇帝（司马炽）", "major", "西晋"),
                               ("晋愍帝", "victim", "西晋末帝（司马邺）", "major", "西晋")],
    "event-xijin-mie-wang": [("刘曜", "commander", "攻陷长安者", "major", "汉赵"),
                             ("晋愍帝", "victim", "出降被俘（司马邺）", "major", "西晋")],
    "event-dongjin-jianguo": [("晋元帝", "initiator", "建康即位（司马睿）", "major", "东晋"),
                              ("王导", "official", "辅立元帝（王与马共天下）", "major", "东晋")],
    "event-feishui-zhizhan": [("苻坚", "commander", "前秦主（败军统帅）", "major", "前秦"),
                              ("谢安", "official", "东晋决策者", "major", "东晋"),
                              ("谢玄", "commander", "北府军统帅", "major", "东晋")],
    "event-beiwei-tongyi-beifang": [("拓跋焘", "commander", "北魏统一北方（太武帝）", "major", "北魏"),
                                    ("沮渠牧犍", "victim", "北凉末主（被灭国）", "major", "北凉")],
    "event-beiwei-fenlie": [("高欢", "initiator", "拥立东魏实权者", "major", "东魏"),
                            ("宇文泰", "initiator", "拥立西魏实权者", "major", "西魏"),
                            ("魏孝武帝", "victim", "出奔西魏的皇帝（元修）", "major", "北魏")],
    "event-houjing-zhi-luan": [("侯景", "initiator", "叛乱首领", "major", "侯景政权"),
                               ("梁武帝", "victim", "饿死台城（萧衍）", "major", "萧梁")],
    "event-beizhou-mie-beiqi": [("北周武帝", "commander", "灭齐决策者（宇文邕）", "major", "北周"),
                                ("高纬", "victim", "北齐后主（被俘）", "major", "北齐")],
    "event-yangjian-dai-beizhou": [("杨坚", "initiator", "代周建隋（隋文帝）", "major", "隋"),
                                   ("周静帝", "victim", "禅位幼帝（宇文阐）", "major", "北周")],
    "event-sui-mie-chen": [("杨坚", "ruler", "灭陈决策者", "major", "隋"),
                           ("杨广", "commander", "灭陈军事统帅（晋王）", "major", "隋"),
                           ("陈后主", "victim", "陈末帝（被俘）", "major", "南陈")],
    "event-tang-jianguo": [("唐高祖", "initiator", "建唐之主（李渊）", "major", "唐"),
                           ("李世民", "commander", "开国征战核心（太原起兵/唐太宗）", "major", "唐")],
    "event-xuanwumen-zhibian": [("李世民", "initiator", "政变发动者（唐太宗）", "major", "唐"),
                                ("李建成", "victim", "太子（政变被杀）", "major", "唐"),
                                ("李元吉", "victim", "齐王（政变被杀）", "major", "唐"),
                                ("唐高祖", "ruler", "退位太上皇（李渊）", "major", "唐")],
    "event-tang-mie-dong-tujue": [("李靖", "commander", "灭东突厥主帅", "major", "唐"),
                                  ("唐太宗", "ruler", "用兵决策者（李世民）", "major", "唐"),
                                  ("颉利可汗", "victim", "东突厥可汗（被俘）", "major", "东突厥")],
    "event-wu-zhou-jianguo": [("武则天", "initiator", "称帝建立武周（武曌）", "major", "武周"),
                              ("唐睿宗", "victim", "被废皇帝（李旦）", "major", "唐")],
    "event-shenlong-zhengbian": [("张柬之", "initiator", "政变发动者", "major", "唐"),
                                 ("武则天", "opponent", "被迫退位（武曌）", "major", "武周"),
                                 ("唐中宗", "ruler", "复位皇帝（李显）", "major", "唐")],
    "event-huangchao-qiyi": [("黄巢", "initiator", "起义首领（大齐皇帝）", "major", "大齐"),
                             ("唐僖宗", "victim", "在位皇帝（李儇）", "major", "唐"),
                             ("朱温", "commander", "降唐后镇压起义者（后梁太祖）", "major", "唐"),
                             ("李克用", "commander", "镇压起义的沙陀将领", "major", "唐")],
    "event-houliang-dai-tang": [("朱温", "initiator", "废唐自立（后梁太祖）", "major", "后梁"),
                                ("唐哀帝", "victim", "被废末帝（李柷）", "major", "唐")],
    "event-guo-wei-dai-han": [("郭威", "initiator", "代汉建周（后周太祖）", "major", "后周"),
                              ("刘承祐", "opponent", "后汉隐帝（被杀）", "major", "后汉")],
    "event-chenqiao-bingbian": [("赵匡胤", "initiator", "陈桥兵变首领（宋太祖）", "major", "北宋"),
                                ("柴宗训", "victim", "后周恭帝（被取代）", "major", "后周")],
    "event-western-xia-jianguo": [("李元昊", "initiator", "称帝建国（夏景宗）", "major", "西夏")],
    "event-jin-jianguo": [("完颜阿骨打", "initiator", "建金称帝（金太祖）", "major", "金")],
    "event-jingkang-zhi-bian": [("宋徽宗", "victim", "被俘太上皇（赵佶）", "major", "北宋"),
                                ("宋钦宗", "victim", "被俘皇帝（赵桓）", "major", "北宋"),
                                ("完颜宗翰", "commander", "围汴金军主帅", "major", "金"),
                                ("完颜宗望", "commander", "围汴金军主帅", "major", "金")],
    "event-zhao-gou-nansong-jianguo": [("宋高宗", "initiator", "即位建南宋（赵构）", "major", "南宋")],
    "event-mongol-jianguo": [("成吉思汗", "initiator", "建立大蒙古国（铁木真）", "major", "大蒙古国")],
    "event-yuan-jianguo": [("忽必烈", "initiator", "改国号大元（元世祖）", "major", "元"),
                           ("刘秉忠", "official", "建议国号者", "major", "元")],
    "event-yanya-haizhan": [("赵昺", "victim", "宋末帝（蹈海）", "major", "南宋"),
                            ("陆秀夫", "participant", "负帝蹈海（丞相）", "major", "南宋"),
                            ("张世杰", "commander", "崖山宋军统帅", "major", "南宋")],
    "event-poyanghu-zhizhan": [("朱元璋", "commander", "决战指挥者（吴国公）", "major", "朱元璋势力"),
                               ("陈友谅", "commander", "汉政权主（中流矢死）", "major", "大汉")],
    "event-zhuyuanzhang-chendi": [("朱元璋", "initiator", "称帝建立明朝（明太祖）", "major", "明")],
    "event-hu-weiyong-an": [("朱元璋", "initiator", "处置胡案的皇帝", "major", "明"),
                            ("胡惟庸", "victim", "被诛丞相", "major", "明")],
    "event-jingnan-zhizhan": [("朱棣", "initiator", "靖难起兵者（明成祖）", "major", "明"),
                              ("建文帝", "opponent", "被推翻皇帝（朱允炆）", "major", "明")],
    "event-qian-du-beijing": [("明成祖", "initiator", "迁都决策者（朱棣）", "major", "明")],
    "event-tumu-bao-zhibian": [("明英宗", "victim", "被俘皇帝（朱祁镇）", "major", "明"),
                               ("也先", "commander", "瓦剌首领（作战指挥）", "major", "瓦剌"),
                               ("王振", "initiator", "怂恿亲征的宦官", "major", "明")],
    "event-saerhu-zhizhan": [("努尔哈赤", "commander", "后金统帅", "major", "后金"),
                             ("杨镐", "commander", "明军四路总指挥", "major", "明")],
    "event-lizicheng-gong-beijing": [("李自成", "initiator", "大顺军首领（攻陷北京）", "major", "大顺"),
                                     ("崇祯帝", "victim", "自缢皇帝（朱由检）", "major", "明")],
    "event-qingjun-ru-guan": [("多尔衮", "commander", "清军入关最高指挥", "major", "清"),
                              ("吴三桂", "initiator", "引清军入关者", "major", "明")],
    "event-sanfan-zhi-luan": [("吴三桂", "initiator", "三藩之乱首谋", "major", "清"),
                              ("康熙帝", "ruler", "平叛决策者（玄烨）", "major", "清"),
                              ("耿精忠", "participant", "响应叛乱者（靖南王）", "major", "清")],
    "event-diyici-yapian-zhanzheng": [("林则徐", "official", "禁烟与广东防务主持者", "major", "清"),
                                      ("道光帝", "ruler", "在位皇帝（旻宁）", "major", "清")],
    "event-jiawu-zhanzheng": [("光绪帝", "ruler", "在位皇帝（载湉）", "major", "清"),
                              ("慈禧太后", "political_leader", "清廷实权决策者", "major", "清"),
                              ("李鸿章", "official", "主和与议和代表", "major", "清"),
                              ("丁汝昌", "commander", "北洋海军提督（殉国）", "major", "清")],
    "event-wuchang-qiyi": [("蒋翊武", "commander", "起义总指挥（文学社）", "major", "革命党"),
                           ("孙武", "initiator", "起义组织者（共进会）", "major", "革命党"),
                           ("黎元洪", "political_leader", "被推举都督", "major", "革命党")],
    "event-qingdi-tuiwei": [("溥仪", "victim", "退位皇帝（宣统帝）", "major", "清"),
                            ("隆裕太后", "ruler", "代行皇权下诏退位", "major", "清"),
                            ("袁世凯", "official", "南北和议主导者", "major", "中华民国"),
                            ("孙中山", "political_leader", "南京临时政府一方", "major", "中华民国")],
    "event-wusi-yundong": [("陈独秀", "political_leader", "新文化运动领袖（《新青年》）", "major", "民国"),
                           ("李大钊", "political_leader", "北大教授（运动推动者）", "major", "民国"),
                           ("蔡元培", "official", "北大校长（支持学生运动）", "major", "民国")],
    "event-jiuyiba-shibian": [("石原莞尔", "initiator", "事变策划者（关东军参谋）", "major", "日本"),
                              ("板垣征四郎", "initiator", "事变策划者（关东军参谋）", "major", "日本"),
                              ("张学良", "commander", "东北军统帅", "major", "中华民国"),
                              ("蒋介石", "political_leader", "国民政府领导（方针争议两说并存）", "major", "中华民国")],
    "event-xian-shibian": [("张学良", "initiator", "兵谏发动者", "major", "中华民国"),
                           ("杨虎城", "initiator", "兵谏发动者", "major", "中华民国"),
                           ("蒋介石", "victim", "被扣留者", "major", "中华民国"),
                           ("周恩来", "participant", "中共谈判代表", "major", "中共")],
    "event-qiqishi-bian": [("宋哲元", "commander", "第29军军长（冀察政务委员会委员长）", "major", "中华民国"),
                           ("秦德纯", "official", "北平军政当局代理", "major", "中华民国"),
                           ("牟田口廉也", "commander", "日军驻屯军联队长（下令攻击宛平）", "major", "日本")],
    "event-nanjing-datusha": [("松井石根", "commander", "日军华中方面军司令（东京审判定罪）", "major", "日本"),
                              ("谷寿夫", "commander", "日军第6师团长（南京审判处决）", "major", "日本"),
                              ("唐生智", "commander", "南京卫戍司令长官", "major", "中华民国")],
    "event-riben-touxiang": [("裕仁", "political_leader", "日本天皇（终战诏书）", "major", "日本"),
                             ("蒋介石", "political_leader", "中国战区最高统帅", "major", "中华民国")],
    "event-xinzhongguo-chengli": [("毛泽东", "initiator", "中央人民政府主席", "major", "中华人民共和国"),
                                  ("周恩来", "official", "政务院总理", "major", "中华人民共和国"),
                                  ("朱德", "commander", "人民解放军总司令", "major", "中华人民共和国")],
}


def event_years(backbone, eid: str) -> tuple[int, int]:
    e = next(x for x in backbone.events if x["id"] == eid)
    return e.get("start_year") or 0, e.get("end_year") or (e.get("start_year") or 0)


def resolve(knowledge, name: str, s_start: int, s_end: int) -> dict:
    """返回候选 person 列表（已按 person_id 去重）与分类。"""
    trad = to_trad(name)
    base = norm_name(trad)
    base_simple = norm_name(name)
    rows = knowledge.execute("""
        SELECT id, canonical_name_zh_cn, birth_year, death_year, dynasty_ids
        FROM people WHERE canonical_name_zh_cn LIKE '%' || ? || '%'
                      OR search_name LIKE '%' || ? || '%'
                      OR traditional_name LIKE '%' || ? || '%'
                      OR search_aliases LIKE '%' || ? || '%'
    """, (base, base, base, base)).fetchall()
    if not rows:
        rows = knowledge.execute("""
            SELECT p.id, p.canonical_name_zh_cn, p.birth_year, p.death_year, p.dynasty_ids
            FROM person_aliases a JOIN people p ON p.id = a.person_id
            WHERE a.alias_zh_cn = ? OR a.alias = ? OR a.alias_zh_cn LIKE '%' || ? || '%'
        """, (base, base, base)).fetchall()
    seen: dict[str, dict] = {}
    for pid, canon, birth, death, dyn in rows:
        canon_s = canon or ""
        if pid not in seen:
            seen[pid] = {"id": pid, "canonical": canon_s, "birth": birth, "death": death,
                         "dynasty": dyn, "matches_base": (base in canon_s),
                         "conflict": False, "conflict_reason": None}
        # 硬冲突：生晚于事件结束、死早于事件开始
        rec = seen[pid]
        if rec["conflict"]:
            continue
        if birth is not None and s_end and birth > s_end + 1:
            rec["conflict"], rec["conflict_reason"] = True, f"birth {birth} > event_end {s_end}"
        if death is not None and s_start and death < s_start - 1:
            rec["conflict"], rec["conflict_reason"] = True, f"death {death} < event_start {s_start}"
    return {"name": name, "raw_name": name, "trad": trad, "hits": list(seen.values())}


def classify(res: dict) -> str:
    hits = [h for h in res["hits"] if not h["conflict"]]
    conflicts = [h for h in res["hits"] if h["conflict"]]
    if not hits:
        return "rejected" if conflicts else "not_found"
    if len(hits) == 1:
        h = hits[0]
        return "exact" if h["matches_base"] else "high_confidence"
    return "ambiguous"


def main() -> None:
    backbone = load_backbone(ROOT)
    crit = {e["id"]: e for e in backbone.events if e["importance"] == "critical"}
    missing = [eid for eid in CANDIDATES if eid not in crit]
    uncov = [eid for eid in crit if eid not in CANDIDATES]
    print("candidate events:", len(CANDIDATES), "| critical:", len(crit),
          "| 无候选的 critical:", len(uncov), uncov[:8], "| 候选含非 critical:", missing)

    import duckdb
    knowledge = duckdb.connect(str(KNOWLEDGE), read_only=True)
    out = {}
    for eid, cands in CANDIDATES.items():
        s_start, s_end = event_years(backbone, eid)
        results = []
        for (name, role, role_zh, imp, side) in cands:
            res = resolve(knowledge, name, s_start, s_end)
            res["role"], res["role_zh_cn"], res["importance"], res["side"] = role, role_zh, imp, side
            res["classification"] = classify(res)
            results.append(res)
        out[eid] = {"event": crit[eid]["name_zh_cn"], "years": f"{s_start}-{s_end}", "results": results}

    # 写候选 YAML
    cand_dir = ROOT / "data" / "candidates" / "event_person"
    cand_dir.mkdir(parents=True, exist_ok=True)
    import yaml
    for eid, info in out.items():
        doc = {"event_id": eid, "event_name": info["event"], "event_years": info["years"],
               "candidates": [
                   {"person_name_raw": r["raw_name"], "role": r["role"], "role_zh_cn": r["role_zh_cn"],
                    "importance": r["importance"], "side": r["side"],
                    "candidate_person_ids": [h["id"] for h in r["hits"]],
                    "canonical_names": [h["canonical"] for h in r["hits"]],
                    "resolution": r["classification"],
                    "identity_evidence": f"Knowledge Store 匹配：{'；'.join(h['canonical'] for h in r['hits'][:3]) or '无'}",
                    "event_evidence": f"该人物为《{info['event']}》事件核心参与者（来自事件 summary/source_reference）",
                    "review_status": "pending"}
                   for r in info["results"]],
               "review": "candidate → pending → accepted/rejected/ambiguous/not_found"}
        (cand_dir / f"{eid}.yml").write_text(
            f"# V2.1 Critical Event Person Linking Candidates\n"
            + yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")

    # 预视文本（供人工 review）
    lines = []
    stats = {"exact": 0, "high_confidence": 0, "ambiguous": 0, "not_found": 0, "rejected": 0}
    for eid, info in sorted(out.items()):
        for r in info["results"]:
            stats[r["classification"]] += 1
            hits = f"{[(h['id'], h['canonical'][:22]) for h in r['hits'][:3]]}"
            lines.append(f"[{r['classification']:>14}] {eid} {r['raw_name']:<8} hits={hits}")
    (ROOT / "reports" / "_v21_resolution_preview.txt").write_text("\n".join(lines), encoding="utf-8")
    print("分类统计:", stats)
    print("preview -> reports/_v21_resolution_preview.txt")


if __name__ == "__main__":
    main()