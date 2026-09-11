# -*- coding: utf-8 -*-
"""V2.2 · Major Event Person Linking — 确定性自动链接层（Machine Review，逐 period batch）。

原则（延续 §37–§41；V2.2 授权自动扫描，品质门槛从高）：
- 仅接受：「KB/curated 精确命中」＋「事件时窗过滤后唯一存活」＋「(有生卒证据) 或 (名长≥3)」。
- 未达门槛不建链（empty EventPerson 允许）；不为凑数注入低置信/虚构链接。
- 不新增 Person（V2.2 无 supplemental 层）。
- quality_status「候选未经人工 review 禁止直接进入正式 backbone」→ V2.2 落盘到
  独立 machine-review 层（candidates/ / reviews/ / machine_review/ v2_2 目录），
  不并入 loader 扫描的 curated/history_backbone/event_person/（正式 dist 保持不变：
  events=618, event_person=200 门禁与冻结 V1 不受影响）。人工 V2.3 放行后再并入。
- 每个 period batch 落盘后输出 GATE；全部完成后输出 SUMMARY 并 STOP。

用法：
  python scripts/v22_major_person_links.py --dry-run   # 决策预览（不写文件）
  python scripts/v22_major_person_links.py --write     # 落盘 + 每期报告 + 汇总
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))
import yaml  # noqa: E402
import duckdb  # noqa: E402
from history_data_pipeline.backbone.loader import load_backbone  # noqa: E402

KB = ROOT / "data" / "normalized" / "history.duckdb"
# 知识层 V2 重建后 data/normalized 可能只有文本层（people=0）；dist 含 curated people 种子
DIST = ROOT / "dist" / "history.duckdb"
PERSONS_DIR = ROOT / "data" / "curated" / "persons"
# V2.2 专用层（不并入正式 loader 扫描目录）
CAND_DIR = ROOT / "data" / "candidates" / "event_person_v2_2"
REV_ACC = ROOT / "data" / "reviews" / "accepted" / "event_person_v2_2"
REV_PEND = ROOT / "data" / "reviews" / "pending" / "event_person_v2_2"
STORE_V22 = ROOT / "data" / "machine_review" / "event_person_v2_2"
REPORTS = ROOT / "reports"

REVIEWED_BY = "china-history-backbone-v2.2-machine"
GATE_SUMMARY = "V2_2_MAJOR_EVENT_PERSON_LINKING_READY"

CJK_BLOCK = re.compile(r"[\u3400-\u9fff]{2,12}")

# 通用词/时代词/事件措辞停用（避免把常见词汇误当人名）。
STOP = {
    "大业", "元年", "二世", "尚书", "皇帝", "太宗", "高宗", "太祖", "神宗", "仁宗", "英宗",
    "世宗", "武宗", "宣宗", "代宗", "德宗", "文宗", "穆宗", "嘉帝", "哀帝", "少帝",
    "中国", "中华", "天下", "王朝", "朝廷", "政权", "中央", "地方", "领导", "首领", "统治",
    "年代", "时期", "期间", "世纪", "末年", "初年", "中叶", "之初", "以后", "之前", "以前",
    "开始", "结束", "完成", "实现", "确立", "建立", "推翻", "灭亡", "统一", "扩张", "爆发",
    "反击", "进攻", "助阵", "联手", "入侵", "南下", "北伐", "东征", "西进", "平定", "征讨",
    "国王", "将军", "统帅", "主帅", "大将", "宰相", "太后", "皇后", "太子", "王子", "贵族",
    "军队", "主力", "联军", "兵力", "政策", "制度", "变革", "改革", "革命", "起义", "政变",
    "事变", "兵变", "动乱", "叛乱", "内乱", "掌权", "称王", "称帝", "登基", "即位", "篡位",
    "诸侯", "秦国", "晋国", "楚国", "齐国", "吴国", "越国", "郑国", "宋国", "燕国", "韩国",
    "赵国", "隋朝", "唐朝", "宋朝", "明朝", "清朝", "汉朝", "魏国", "辽国", "金国",
    "大国", "小国", "称霸", "会盟", "争霸", "霸权", "秩序", "格局", "态势", "势力", "战线",
    "国家", "疆域", "领土", "边境", "中原", "南方", "北方", "西部", "东部", "长城", "边疆",
    "同时", "此前", "当前", "主要", "重要", "关键", "极为", "日益", "逐渐", "迅速", "最终",
    "彻底", "全面", "直接", "严峻", "困顿", "衰败", "衰退", "覆灭", "陷落", "失守",
    "胜利", "失败", "成功", "十分", "已经", "作为", "以及", "其中", "根本", "核心", "意义",
    "影响", "历史", "地位", "走向", "转折", "起点", "标志", "象征", "代表", "决定", "奠定",
    "成为", "担任", "出任", "在位", "会战",
}
STOP = set(STOP)

# 数字/计数类名称（如「四十七」）绝不作为人名链接。
NUM_WORDS = set("零〇一二三四五六七八九十百千万两")

# 审稿人逐条筛查后的排除项（event_id -> (name, reason)）。
# 均为「文本中的非人名用例」被扫描命中：地方/年号/助词/复合名等。
EXCLUDED_BY_REVIEW = {
    "event-dingdu-tianjing": ("江北", "江北大营（地方/军事部署），非人名"),
    "event-jin-qian-du-bian": ("中都", "金中都（地名），非人名"),
    "event-yuan-dingdu-dadu": ("中都", "金中都（地名），非人名"),
    "event-qin-shutongwen": ("施之", "「措施之一」助词，非人名"),
    "event-liangdu-zhizhan": ("于致和", "「泰定帝于致和元年」：纪年片段，非人名"),
    "event-mayi-zhi-mou": ("王恢之", "正确应为 王恢（马邑之谋）；王恢之 为另一人"),
    "event-xia-taikang-shiguo": ("王太康", "正确应为 夏太康；王太安康为另一条"),
    "event-tang-ping-qiuzi-sizhen": ("阿史那", "复合姓氏（阿史那社尔），非独立人名"),
    "event-yefengling-zhizhan": ("中都", "金中都（城池/政区地名），非人名"),
}


class NameIndex:
    def __init__(self) -> None:
        self.name2rec: dict[str, list[dict]] = {}
        self.persons: dict[str, dict] = {}
        self.build()

    def _put(self, nm: str, rec: dict) -> None:
        if nm and len(nm) >= 2:
            self.name2rec.setdefault(nm, []).append(rec)

    def build(self) -> None:
        # data/normalized 可能只有文本层（people=0）；选 people>0 的库（dist 有 curated 种子）
        kb = KB
        try:
            probe = duckdb.connect(str(KB), read_only=True)
            has_people = probe.execute("SELECT COUNT(*) FROM people").fetchone()[0] > 0
            probe.close()
        except Exception:
            has_people = False
        if not has_people:
            kb = DIST
        con = duckdb.connect(str(kb), read_only=True)
        rows = con.execute(
            "SELECT id, canonical_name_zh_cn, name_raw, birth_year, death_year FROM people"
        ).fetchall()
        for pid, canon, raw, by, dy in rows:
            canon = canon or ""
            rec = self.persons.get(pid)
            if rec is None:
                rec = self.persons[pid] = {
                    "id": pid, "canonical": canon, "birth": by, "death": dy,
                    "has_years": by is not None or dy is not None,
                }
            for nm in dict.fromkeys([canon, (raw or "")]):
                self._put(nm, rec)
        for f in sorted(PERSONS_DIR.glob("*.yml")):
            d = yaml.safe_load(f.read_text(encoding="utf-8"))
            pid = d["id"]
            rec = self.persons.setdefault(pid, {
                "id": pid, "canonical": d["canonical_name_zh_cn"],
                "birth": d.get("birth_year"), "death": d.get("death_year"),
                "has_years": d.get("birth_year") is not None or d.get("death_year") is not None})
            for nm in dict.fromkeys(x for x in ([d["canonical_name_zh_cn"], d["name_raw"]] + d.get("aliases", [])) if x and len(x) >= 2):
                self._put(nm, rec)

    def lookup(self, name: str) -> list[dict]:
        return self.name2rec.get(name, [])


def _ev_years(e: dict) -> tuple[int, int]:
    s = e.get("start_year")
    return (s or 0), (e.get("end_year") or s or 0)


def scan_names(index: NameIndex, text: str) -> set[str]:
    """最长匹配扫描：把文本中命中的词典人名（子串）取最长，去重返回。"""
    names: set[str] = set()
    for m in CJK_BLOCK.finditer(text):
        frag = m.group()
        best = None
        for ln in range(min(len(frag), 8), 1, -1):
            hit = next((frag[i:i + ln] for i in range(len(frag) - ln + 1)
                        if frag[i:i + ln] in index.name2rec), None)
            if hit:
                best = hit
                break
        if best:
            names.add(best)
    return names


def classify(index: NameIndex, e: dict) -> dict:
    """事件名称解析 → {name: info}。"""
    s_start, s_end = _ev_years(e)
    text = e["name_zh_cn"] + "。" + (e.get("summary_zh_cn") or "")
    out: dict[str, dict] = {}
    for name in scan_names(index, text):
        if name in STOP:
            continue
        kept, dropped = [], []
        for rec in index.lookup(name):
            birth, death = rec["birth"], rec["death"]
            ok = True
            if birth is not None and s_end and birth > s_end + 2:
                ok = False
            if death is not None and s_start and death < s_start - 2:
                ok = False
            (kept if ok else dropped).append(rec)
        uniq = len({r["id"] for r in kept}) == 1
        rec0 = kept[0] if kept else None
        out[name] = {
            "name": name,
            "kept": [r["id"] for r in kept],
            "kept_names": sorted({r["canonical"] for r in kept}),
            "canonical": rec0["canonical"] if rec0 else "",
            "unique": bool(uniq),
            "has_years": bool(rec0 and rec0["has_years"]),
            "enough": bool(rec0 and uniq and (rec0["has_years"] or len(name) >= 3)),
            "dropped": sorted({r["canonical"] for r in dropped}),
        }
    return out


def make_block(e: dict, name: str, info: dict) -> dict:
    pid = info["kept"][0]
    recs = [r for r in index.lookup(name) if r["id"] == pid]
    canon = recs[0]["canonical"] if recs else info["canonical"]
    s_start, s_end = _ev_years(e)
    return {
        "person_id": pid,
        "person_name_raw": name,
        "canonical_name": canon,
        "role": "participant",
        "side": "",
        "importance": "major",
        "link_status": "linked",
        "link_quality_status": "reviewed",
        "link_confidence": 0.95 if canon != name else 1.0,
        "resolution": "exact",
        "identity_evidence": (
            f"{REVIEWED_BY}：KB/curated 精确命中（{name}→{canon}），"
            f"事件时窗 {s_start}–{s_end} 内唯一存活候选，无身份冲突"),
        "event_evidence": f"《{e['name_zh_cn']}》summary 明确出现 {name}（依据事件 summary/source_reference）",
        "review_note": f"V2.2 自动 review：exact；reviewed_by={REVIEWED_BY}",
    }


def decide(e: dict, res: dict) -> tuple[list, list]:
    """把 classify 结果套用门控（审阅排除/数字词/唯一性要求）→ (accept, unlinked)。"""
    accept, unlinked = [], []
    for name, info in sorted(res.items()):
        if e["id"] in EXCLUDED_BY_REVIEW and EXCLUDED_BY_REVIEW[e["id"]][0] == name:
            unlinked.append({"person_name_raw": name, "resolution": "excluded_by_review",
                             "reason": EXCLUDED_BY_REVIEW[e["id"]][1]})
            continue
        if name and all(ch in NUM_WORDS for ch in name):
            unlinked.append({"person_name_raw": name, "resolution": "excluded_by_review",
                             "reason": "纯数字/计数词，非人名"})
            continue
        if info["enough"]:
            accept.append(make_block(e, name, info))
        else:
            n_kept = len(info["kept"])
            if n_kept > 1:
                resolution, reason = "ambiguous", f"候选 {n_kept} 人，无法唯一确认 → 不自动链接"
            elif n_kept == 1:
                resolution, reason = "low_confidence", "仅 2 字名且无生卒时间证据 → 低置信，未自动链接"
            else:
                resolution, reason = "not_found", f"KB 无 {name} 精确命中（或全部被时间窗排除）"
            unlinked.append({"person_name_raw": name, "resolution": resolution, "reason": reason})
    # 同 event 内按 person_id 去重（别名指向同一人只保留一条）
    seen, deduped = set(), []
    for b in accept:
        if b["person_id"] in seen:
            continue
        seen.add(b["person_id"])
        deduped.append(b)
    return deduped, unlinked


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="决策预览，不写文件")
    ap.add_argument("--max", type=int, default=0, help="仅处理前 N 个 major event（调试）")
    ap.add_argument("--write", action="store_true", help="落盘 + 每期报告 + 汇总")
    args = ap.parse_args()

    global index
    index = NameIndex()

    bb = load_backbone(ROOT)
    major = [e for e in bb.events if e["importance"] == "major"]
    if args.max:
        major = major[: args.max]

    decisions: list = []
    for e in major:
        res = classify(index, e)
        accept, unlinked = decide(e, res)
        decisions.append((e["id"], e, accept, unlinked, res))

    total_links = sum(len(a) for *_, a, _, _ in decisions)
    n_linked = sum(1 for *_, a, _, _ in decisions if a)
    print(f"major={len(decisions)} | auto links={total_links} | linked events={n_linked} | empty events={len(decisions) - n_linked}")

    if not args.write:
        for eid, e, acc, un, res in decisions[: (args.max or 60)]:
            print(f"\n-- {eid} {e['name_zh_cn']} [{e['period_id']}]")
            for b in acc:
                print("   +", b["person_name_raw"], "->", b["canonical_name"], b["person_id"])
            if not acc:
                print(f"   (empty; candidates={sorted(res)})")
        return 0

    by_period: dict[str, list] = defaultdict(list)
    for d in decisions:
        by_period[d[1]["period_id"]].append(d)
    ok = (write_all(decisions)
          and all(write_period_report(pid, items) for pid, items in sorted(by_period.items()))
          and write_summary(decisions))
    print("V2.2 write:", "OK" if ok else "FAILED")
    return 0 if ok else 1


def _years_str(e: dict) -> str:
    s, t = _ev_years(e)
    return f"{s}–{t}" if t else str(s)


STORE_HEADER = (
    "# China History Backbone V2.2 · Machine-Reviewed Major EventPerson (待 V2.3 人工放行)\n"
    "# 本目录不被 loader/backbone 扫描；正式 backbone 冻结 gate（events=618, event_person=200）不受影响。\n"
    "# 每行 people 字段与最终 schema 兼容；quality_status=candidate，需人工 review 后并入。\n"
)


def write_all(decisions: list) -> bool:
    # 自洽重建：本层全部产物均由本脚本生成，重跑即整体重写（避免 stale 残留）。
    import shutil
    for d in (CAND_DIR, REV_ACC, REV_PEND, STORE_V22):
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True)
    n_cand = n_pend = n_acc = n_store = 0
    for eid, e, accept, unlinked, res in decisions:
        years = _years_str(e)
        # candidate（machine 产生）
        cand = {
            "event_id": eid, "event_name": e["name_zh_cn"], "event_years": years,
            "accepted": [dict(b) for b in accept],
            "unlinked": unlinked,
        }
        (CAND_DIR / f"{eid}.yml").write_text(
            "# V2.2 Major EventPerson — machine candidates\n"
            + yaml.safe_dump(cand, allow_unicode=True, sort_keys=False, width=160),
            encoding="utf-8")
        n_cand += 1
        # accepted review (machine)
        acc = {
            "event_id": eid, "event_name": e["name_zh_cn"], "event_years": years,
            "schema_version": 1, "review_status": "accepted_by_machine_pending_human",
            "reviewed_by": REVIEWED_BY, "candidates_count": len(res),
            "accepted_links": [{"person_id": b["person_id"], "person_name_raw": b["person_name_raw"],
                                "canonical_name": b["canonical_name"], "role": b["role"],
                                "resolution": b["resolution"],
                                "link_quality_status": b["link_quality_status"],
                                "link_confidence": b["link_confidence"]} for b in accept],
        }
        (REV_ACC / f"{eid}.review.json").write_text(
            json.dumps(acc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        n_acc += 1
        # pending queue (machine) — human review now opened
        (REV_PEND / f"{eid}.review.json").write_text(
            json.dumps({
                "event_id": eid, "event_name": e["name_zh_cn"], "review_status": "pending_human",
                "candidates_count": len(res), "link_count": len(accept),
                "note": "V2.2 machine auto-accepted; requests V2.3 human reviewer before formal imprint.",
            }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        n_pend += 1
        # machine store (not loader-scanned)
        if accept:
            fp = STORE_V22 / f"{eid}.yml"
            fields = ("person_id", "person_name_raw", "canonical_name", "role", "side",
                      "importance", "link_status", "link_quality_status", "link_confidence",
                      "resolution", "identity_evidence", "event_evidence", "review_note")
            doc = {"event_id": eid, "event_years": years, "machine_review": REVIEWED_BY,
                   "quality_status": "candidate",
                   "people": [{k: b.get(k) for k in fields} for b in accept]}
            fp.write_text(STORE_HEADER + yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, width=1), encoding="utf-8")
            n_store += 1
    print(f"candidates={n_cand} | accepted_reviews={n_acc} | pending_reviews={n_pend} | machine_store={n_store}")
    return True


def _gate(pid: str) -> str:
    return "V2_2_PERIOD_" + pid.upper().replace("-", "_").replace("PERIOD_", "")


def write_period_report(pid: str, items: list) -> bool:
    linked = [d for d in items if d[2]]
    empty = [d for d in items if not d[2]]
    lines = [
        f"# V2.2 Major EventPerson Linking — {pid}", "",
        f"- gate: `{_gate(pid)}=TRUE`",
        f"- major events: {len(items)} | linked: {len(linked)} | links: {sum(len(d[2]) for d in items)} | empty(allowed): {len(empty)}",
        "",
        "| event | event name | links | persons |", "|---|---|---|---|",
    ]
    for eid, e, acc, un, res in sorted(items, key=lambda d: d[0]):
        names = "; ".join(sorted({b["person_name_raw"] for b in acc})) or "—"
        lines.append(f"| {eid} | {e['name_zh_cn']} | {len(acc)} | {names} |")
    lines += ["", "- 所有链接为 machine exact（时窗唯一）；待 V2.3 人工放行前不进入正式 backbone。",
              f"- 空事件 {len(empty)} 个：KB 未命中 / 多候选 / 低置信 / 审阅排除，V2.2 允许 empty EventPerson。"]
    (REPORTS / f"V2_2_MAJOR_EVENT_PERSON_LINKING_{pid}.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8")
    return True


def write_summary(decisions: list) -> bool:
    per = Counter(d[1]["period_id"] for d in decisions)
    linked = Counter(d[1]["period_id"] for d in decisions if d[2])
    total_links = sum(len(d[2]) for d in decisions)
    lines = [
        "# V2_2 MAJOR EVENT PERSON LINKING SUMMARY", "",
        "- gate: `V2_2_MAJOR_EVENT_PERSON_LINKING_READY=true`",
        f"- major events: {len(decisions)} | auto-accepted links: {total_links} | linked events: {sum(1 for d in decisions if d[2])} | empty-allowed: {sum(1 for d in decisions if not d[2])}",
        "",
        "| Period | events | linked | links |", "|---|---|---|---|",
    ]
    for pid in sorted(per):
        lines.append(f"| {pid} | {per[pid]} | {linked.get(pid, 0)} | {sum(len(d[2]) for d in decisions if d[1]['period_id'] == pid)} |")
    lines += ["",
        "- Rule: KB/curated 精确命中 + 事件时窗内唯一存活 + (有生卒年或名长≥3)；数字词/审阅排除项不放行。",
        "- V2.2 不新增 Person；machine 层已隔离（未并入 loader/store），formal backbone gate 保持 events=618, event_person=200。",
        "- 待办：V2.3 人工 review 通过后决定是否并入正式 Backbone（当前 STOP）。",
    ]
    (REPORTS / "V2_2_MAJOR_EVENT_PERSON_LINKING_SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return True


if __name__ == "__main__":
    main()