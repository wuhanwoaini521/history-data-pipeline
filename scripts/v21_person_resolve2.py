# -*- coding: utf-8 -*-
"""V2.1 Critical Event Person Linking — 解析器 v2。

v2 改进：
1) MANUAL_QUERY：称谓/尊号 → 个人名（手工消歧映射，match_method=manual_identification + alias_exact）；
2) 亲属噪声过滤（某氏(××妻/母/女/皇后/妃/妾/公主/夫人…) 与 后缀异名，如 谢安富/李斯佺）；
3) 生涯硬冲突（birth>event_end / death<event_start → excluded/rejected）；
4) 政权 hint（dynasty_ids 与事件时代匹配）排序；
5) PREFERRED_ID：CBDB 重复 id 时的人工首选（探库确定）。

输出：data/candidates/event_person/<event_id>.yml + reports/_v21_resolution_v2.txt
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

import opencc  # noqa: E402

CONV = opencc.OpenCC("s2t")


def to_trad(s: str) -> str:
    return CONV.convert(s)


_FAMILY_RE = re.compile(r"^[一-龥]{1,3}氏(?:\()|(?:妻|母|女|父|兄|弟|皇后|妃|妾|公主|夫人|繼母|母)[)）]")


def norm_canon(s: str) -> str:
    s = re.sub(r"[（(][^)）]*[)）]", "", s)
    return s.replace(" ", "").strip()


# 手工消歧映射：候选粗名 → 查询名（称谓规范化，§21/§22）
MANUAL_QUERY: dict[str, str] = {
    "汉景帝": "刘启", "汉武帝": "刘彻", "汉献帝": "刘协", "晋惠帝": "司马衷",
    "晋武帝": "司马炎", "晋怀帝": "司马炽", "晋愍帝": "司马邺", "晋元帝": "司马睿",
    "周武王": "周武王", "周平王": "周平王", "周威烈王": "周威烈王",
    "吴王刘濞": "刘濞", "梁武帝": "萧衍", "陈后主": "陈叔宝", "北周武帝": "宇文邕",
    "周静帝": "宇文阐", "唐高祖": "李渊", "唐太宗": "李世民", "唐睿宗": "李旦",
    "唐中宗": "李显", "唐僖宗": "李儇", "唐哀帝": "李柷", "武则天": "武曌",
    "成吉思汗": "铁木真", "明成祖": "朱棣", "建文帝": "朱允炆", "平王": "周平王",
    "周武王": "周武王", "崇祯帝": "朱由检", "康熙帝": "爱新觉罗玄烨", "道光帝": "爱新觉罗旻宁",
    "光绪帝": "爱新觉罗载湉", "明英宗": "朱祁镇", "努尔哈赤": "爱新觉罗努尔哈赤",
    "多尔衮": "爱新觉罗多尔衮", "楚汉争霸": None,
}

# 人工首选 ID（CBDB 多 id 时的确定性选择；探库确定）
PREFERRED_ID: dict[str, str] = {
    "汉献帝": "cbdb-person-30267", "晋惠帝": "cbdb-person-30898", "晋武帝": "cbdb-person-21207",
    "晋怀帝": "cbdb-person-30899", "晋元帝": "cbdb-person-30902", "汉武帝": "cbdb-person-16626",
    "唐高祖": "cbdb-person-13059", "唐太宗": "cbdb-person-13060", "唐睿宗": "cbdb-person-19243",
    "唐中宗": "cbdb-person-19242", "唐僖宗": "cbdb-person-189295", "唐哀帝": "cbdb-person-339634",
    "武则天": "cbdb-person-93663", "北周武帝": "cbdb-person-31773", "陈后主": "cbdb-person-21303",
    "明成祖": "cbdb-person-30151", "康熙帝": "cbdb-person-65884", "道光帝": "cbdb-person-64991",
    "光绪帝": "cbdb-person-54297", "崇祯帝": "cbdb-person-30165",
    "成吉思汗": "cbdb-person-29239", "忽必烈": "cbdb-person-29244", "明英宗": "cbdb-person-30154",
    "努尔哈赤": "cbdb-person-66013", "多尔衮": "cbdb-person-65991",
    "袁世凯": "cbdb-person-63546", "蔡元培": "cbdb-person-90980", "溥仪": "cbdb-person-439438",
    "丁汝昌": "cbdb-person-58649", "黎元洪": "cbdb-person-91349", "蒋翊武": "cbdb-person-89699",
    "李鸿章": "cbdb-person-58961", "林则徐": "cbdb-person-54819", "李自成": "cbdb-person-65627",
    "张献忠": "cbdb-person-65903", "吴三桂": "cbdb-person-58844", "耿精忠": "cbdb-person-65757",
    "李元昊": "cbdb-person-339687", "完颜阿骨打": "cbdb-person-339707",
}

# 事件 → 政权 hint（CBDB dynasty name 子串）
DYN_HINTS: dict[str, list[str]] = {
    "event-shangtang-miexia": ["夏"], "event-wuwang-fazhou": ["商", "周"],
    "event-pingwang-dongqian": ["周"], "event-sanjia-fenjin": ["周", "晉"],
    "event-changping-zhizhan": ["秦"], "event-qin-mie-liuguo": ["秦"],
    "event-qin-tongyi": ["秦"], "event-qiguo-zhi-luan": ["漢", "西漢"],
    "event-mobei-zhizhan": ["漢", "西漢"], "event-wangmang-chengdi": ["新"],
    "event-xin-mie": ["新"], "event-guangwu-chengdi": ["漢", "東漢"],
    "event-caopi-dai-han": ["三國", "魏", "漢"], "event-jin-mie-wu": ["晉", "吳"],
    "event-bawang-zhi-luan": ["晉", "西晉"], "event-yongjia-zhi-luan": ["晉", "前趙"],
    "event-xijin-mie-wang": ["晉", "前趙"], "event-dongjin-jianguo": ["晉", "東晉"],
    "event-feishui-zhizhan": ["晉", "東晉", "前秦"], "event-beiwei-tongyi-beifang": ["北魏", "北涼"],
    "event-beiwei-fenlie": ["北魏", "東魏", "西魏"], "event-houjing-zhi-luan": ["南梁"],
    "event-beizhou-mie-beiqi": ["北周", "北齊"], "event-yangjian-dai-beizhou": ["北周", "隋"],
    "event-sui-mie-chen": ["隋", "陳", "南北朝"], "event-tang-jianguo": ["唐"],
    "event-xuanwumen-zhibian": ["唐"], "event-tang-mie-dong-tujue": ["唐"],
    "event-wu-zhou-jianguo": ["唐", "周"], "event-shenlong-zhengbian": ["唐"],
    "event-huangchao-qiyi": ["唐"], "event-houliang-dai-tang": ["唐", "後梁"],
    "event-guo-wei-dai-han": ["後周", "後漢"], "event-chenqiao-bingbian": ["宋", "後周"],
    "event-western-xia-jianguo": ["西夏"], "event-jin-jianguo": ["金"],
    "event-jingkang-zhi-bian": ["宋", "金"], "event-zhao-gou-nansong-jianguo": ["宋", "南宋"],
    "event-mongol-jianguo": ["蒙古"], "event-yuan-jianguo": ["元"],
    "event-yanya-haizhan": ["宋", "南宋", "元"], "event-poyanghu-zhizhan": ["元"],
    "event-zhuyuanzhang-chendi": ["元", "明"], "event-hu-weiyong-an": ["明"],
    "event-jingnan-zhizhan": ["明"], "event-qian-du-beijing": ["明"],
    "event-tumu-bao-zhibian": ["明", "蒙古"], "event-saerhu-zhizhan": ["明", "蒙古"],
    "event-lizicheng-gong-beijing": ["明"], "event-qingjun-ru-guan": ["清", "明"],
    "event-sanfan-zhi-luan": ["清"], "event-diyici-yapian-zhanzheng": ["清"],
    "event-jiawu-zhanzheng": ["清"], "event-wuchang-qiyi": ["民國"],
    "event-qingdi-tuiwei": ["清", "民國"], "event-wusi-yundong": ["民國"],
    "event-jiuyiba-shibian": ["民國"], "event-xian-shibian": ["民國"],
    "event-qiqishi-bian": ["民國"], "event-nanjing-datusha": ["民國"],
    "event-riben-touxiang": ["民國"], "event-xinzhongguo-chengli": ["民國"],
}


def load_dynasty_map(con) -> dict[str, str]:
    try:
        return {str(r[1]): str(r[0]) for r in con.execute("SELECT id,name_zh_cn FROM dynasties").fetchall()}
    except Exception:
        return {}


def main() -> None:
    backbone = load_backbone(ROOT)
    crit = {e["id"]: e for e in backbone.events if e["importance"] == "critical"}

    # 候选表复用 v21_person_resolve 的 CANDIDATES
    sys.path.insert(0, str(ROOT / "scripts"))
    import importlib.util
    spec = importlib.util.spec_from_file_location("cand", ROOT / "scripts" / "v21_person_resolve.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # noqa
    CANDIDATES = mod.CANDIDATES

    import duckdb
    con = duckdb.connect(str(KNOWLEDGE), read_only=True)
    dyn_names = load_dynasty_map(con)

    def resolve(name: str, role, role_zh, imp, side, eid: str):
        s_start = crit[eid]["start_year"] or 0
        s_end = crit[eid]["end_year"] or s_start
        query = to_trad(MANUAL_QUERY.get(name, name))
        base = norm_canon(query)
        rows = con.execute("""
            SELECT id, canonical_name_zh_cn, birth_year, death_year, dynasty_ids FROM people
            WHERE canonical_name_zh_cn LIKE '%' || ? || '%'
               OR search_name LIKE '%' || ? || '%'
            ORDER BY canonical_name_zh_cn
        """, (base, base)).fetchall()
        hits = []
        for pid, canon, birth, death, dyns in rows:
            canon_s = canon or ""
            cn = norm_canon(canon_s)
            is_family = bool(re.search(r"氏[\u4e00-\u9fff]{0,2}(?:妻|母|女|皇后|妃|妾|公主|夫人)", canon_s)) \
                or bool(re.match(r"^[\u4e00-\u9fff]{1,3}氏", canon_s))
            if is_family:
                continue
            if cn != base and base not in canon_s.replace(" ", ""):
                continue  # 后缀异名（谢安富/李斯佺）
            exact_base = canon_s.startswith(base)
            conflict = None
            if birth and s_end and birth > s_end + 1:
                conflict = f"birth {birth} > event_end {s_end}"
            if death and s_start and death < s_start - 1:
                conflict = f"death {death} < event_start {s_start}"
            score = 0
            score += 80 if canon_s.startswith(base) else 30
            if birth and death:
                if birth <= s_end and (death >= s_start or death >= s_end):
                    score += 50
                elif not conflict:
                    score += 20
            hint = DYN_HINTS.get(eid, [])
            dh = [d for d in (dyns or "").strip("[]").replace("'", "").split(",") if d]
            if hint:
                if any(any(h in dyn_names.get(d, "") or d in dyn_names.get(h, "") for h in hint) for d in dh):
                    score += 40
            hits.append({"id": pid, "canonical": canon_s, "birth": birth, "death": death,
                         "dynasty_ids": dyns, "exact_base": exact_base, "conflict": conflict, "score": score})
        # 首选
        pref = PREFERRED_ID.get(name)
        if pref:
            for h in hits:
                if h["id"] == pref:
                    h["score"] += 500
        hits_sorted = sorted(hits, key=lambda h: (-h["score"], h["id"]))
        # 分类
        if not hits_sorted:
            return {"resolution": "rejected" if False else "not_found", "hits": [], "selected": None,
                    "base": query, "conflict_detail": None}
        top = hits_sorted[0]
        if top["conflict"] and top["score"] <= 0:
            return {"resolution": "rejected", "hits": hits_sorted, "selected": None, "base": query,
                    "conflict_detail": top["conflict"]}
        if top["conflict"] and top["score"] < 100 and not PREFERRED_ID.get(name):
            return {"resolution": "rejected", "hits": hits_sorted[:3], "selected": None, "base": query,
                    "conflict_detail": top["conflict"]}
        viable = [h for h in hits_sorted if not h["conflict"] or PREFERRED_ID.get(name)]
        if not viable:
            return {"resolution": "rejected", "hits": hits_sorted[:3], "selected": None, "base": query,
                    "conflict_detail": ";".join(h["conflict"] for h in hits_sorted if h["conflict"])}
        best = max(viable, key=lambda h: h["score"])
        deuce = [h for h in viable if h["score"] >= best["score"] - 1]
        if len({h["id"] for h in deuce}) > 1 and not PREFERRED_ID.get(name):
            return {"resolution": "ambiguous", "hits": deuce, "selected": None, "base": query,
                    "conflict_detail": None}
        selected = PREFERRED_ID.get(name, best["id"])
        resolution = "exact" if best["score"] >= 150 else "high_confidence"
        return {"resolution": resolution, "hits": hits_sorted[:4], "selected": selected,
                "base": query, "conflict_detail": top["conflict"] if top["conflict"] else None}

    out = {}
    stats = {"exact": 0, "high_confidence": 0, "ambiguous": 0, "not_found": 0, "rejected": 0}
    lines = []
    for eid in sorted(CANDIDATES):
        ev = crit[eid]
        s0 = ev["start_year"] or 0
        s1 = ev["end_year"] or s0
        results = []
        for (name, role, role_zh, imp, side) in CANDIDATES[eid]:
            r = resolve(name, role, role_zh, imp, side, eid)
            r.update({"event_id": eid, "name_raw": name, "event_years": f"{s0}-{s1}",
                      "role": role, "role_zh_cn": role_zh, "importance": imp, "side": side})
            stats[r["resolution"]] += 1
            results.append(r)
            sel = r["selected"] or "-"
            top_hits = " | ".join(f"{h['id']}:{h['canonical'][:14]}({h['score']})" for h in r["hits"][:2])
            lines.append(f"[{r['resolution']:>13}] {eid} {name:<7} -> {sel:<20} {top_hits}")
        out[eid] = results

    (ROOT / "reports" / "_v21_resolution_v2.txt").write_text("\n".join(lines), encoding="utf-8")
    (ROOT / "reports" / "_v21_resolution_v2.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print("stats:", stats)
    print("total candidates:", sum(len(v) for v in out.values()))


if __name__ == "__main__":
    main()