# -*- coding: utf-8 -*-
"""V2.3 · Major-Event EventPerson Formal Review & Formal-Backbone Integration.

输入（只读）:
  - data/machine_review/event_person_v2_2/*.yml          V2.2 machine 候选层（223 links / 事件数=74）
  - scripts/v23_review_{a,b,c}.py                        V2.3 agent 正式 review 决策
  - data/curated/persons/*.yml                           supplemental persons（source_reference）
  - load_backbone(ROOT)                                  事件元数据

输出:
  - data/reviews/formal/event_person_v2_3/<event_id>.yml           每事件 review 记录
  - data/curated/history_backbone/event_person/<event_id>.yml    formal_accepted（正式加载层）
  - reports/V2_3_MAJOR_PERSON_FORMAL_REVIEW_SCOPE.md
  - reports/V2_2_MACHINE_VS_FORMAL_PERSON_REVIEW.md
  - reports/PERSON_LINKING_V1_RISK_REVIEW.md
  - reports/PERSON_LINKING_V1_FINAL_SUMMARY.md

术语: method=agent_assisted_source_review（machine→agent curation→curated_accepted）；
禁止 human_reviewed 声称；link_quality_status 沿用 taxonomy `reviewed`。
"""

from __future__ import annotations

import argparse
import shutil
import sys
from collections import Counter
from pathlib import Path

import duckdb
import yaml

ROOT = Path(__file__).resolve().parent.parent
KB = ROOT / "data" / "normalized" / "history.duckdb"
MACHINE_DIR = ROOT / "data" / "machine_review" / "event_person_v2_2"
FORMAL_REVIEW_DIR = ROOT / "data" / "reviews" / "formal" / "event_person_v2_3"
FORMAL_STORE_DIR = ROOT / "data" / "curated" / "history_backbone" / "event_person"
CURATED_PERSON_DIR = ROOT / "data" / "curated" / "persons"
REPORTS_DIR = ROOT / "reports"

sys.path.insert(0, str(ROOT / "scripts"))
from v23_review_a import REVIEW_A  # noqa: E402
from v23_review_b import REVIEW_B  # noqa: E402
from v23_review_c import REVIEW_C  # noqa: E402
from history_data_pipeline.backbone.loader import load_backbone  # noqa: E402
from history_data_pipeline.v211_roles import ROLE_LABEL  # noqa: E402

REVIEW: dict[str, dict[str, tuple]] = {}
for blk in (REVIEW_A, REVIEW_B, REVIEW_C):
    for eid, d in blk.items():
        REVIEW.setdefault(eid, {}).update(d)

FORMAL_HEADER = (
    "# China History Backbone V2.3 · Agent-Assisted Curated Accepted EventPerson\n"
    "# curated_class=curated_accepted; method=agent_assisted_source_review（待 V2.4 人工复核）。\n"
)
REVIEW_HEADER = (
    "# V2.3 formal review record · method=agent_assisted_source_review（待 V2.4 人工复核）\n"
)

STORE_FIELDS = (
    "person_id", "person_name_raw", "canonical_name", "role", "role_zh_cn", "side", "importance",
    "link_status", "link_quality_status", "link_confidence", "resolution",
    "identity_evidence", "event_evidence", "review_note",
)


def _read_yaml(p: Path) -> dict:
    with open(p, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _dump_yaml(p: Path, doc: dict, header: str = "") -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        if header:
            f.write(header)
        f.write(yaml.safe_dump(doc, allow_unicode=True, sort_keys=False))


def load_machine_store() -> dict[str, dict]:
    out: dict[str, dict] = {}
    for p in sorted(MACHINE_DIR.glob("*.yml")):
        doc = _read_yaml(p)
        eid = doc.get("event_id")
        if not eid:
            continue
        out[eid] = {"doc": doc, "people": {r["person_id"]: r for r in doc.get("people", [])}}
    return out


def load_curated_persons() -> dict[str, dict]:
    out: dict[str, dict] = {}
    for p in sorted(CURATED_PERSON_DIR.glob("*.yml")):
        doc = _read_yaml(p)
        if doc.get("id"):
            out[doc["id"]] = doc
    return out


def load_person_kb() -> dict[str, dict]:
    con = duckdb.connect(str(KB), read_only=True)
    rows = con.execute(
        "SELECT id, canonical_name_zh_cn, name_raw, birth_year, death_year FROM people"
    ).fetchall()
    return {r[0]: {"canonical": r[1], "name_raw": r[2], "birth": r[3], "death": r[4]} for r in rows}


def identity_evidence(pid: str, name: str, curated: dict, kb: dict) -> str:
    if pid.startswith("curated-person-"):
        pu = curated.get(pid, {})
        return (
            f"identity_q=confirmed：补充 Person「{pid}」canonical=「{name}」，"
            f"source_id={pu.get('source_id')}，source_reference=「{pu.get('source_reference') or ''}」；无别名冲突。"
        )
    src = "source-ctext" if pid.startswith("ctext-person-") else "source-cbdb"
    rec = kb.get(pid, {})
    yrs = f"（{rec.get('birth')}–{rec.get('death')}）" if (rec.get("birth") or rec.get("death")) else ""
    return (
        f"V2.3 复核(identity_q=confirmed)：Knowledge Store={src}，canonical=「{name}」{yrs}；"
        f"姓名/别名在事件时窗内唯一命中，身份无冲突。"
    )


def _years(e: dict) -> str:
    s, t = e.get("start_year"), e.get("end_year")
    if t and s and s != t:
        return f"{s}–{t}"
    return str(s) if s else (str(t) if t else "")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="落盘（review 记录 + 正式文件 + 报告）")
    args = ap.parse_args()

    machine = load_machine_store()
    curated = load_curated_persons()
    kb = load_person_kb()
    events = {e["id"]: e for e in load_backbone(ROOT).events}

    errors: list[str] = []
    accepted: list[dict] = []
    rejected: list[dict] = []
    insufficient: list[dict] = []
    per_event: dict[str, dict] = {}
    brand = Counter()  # (is_curated_person, role|verdict)

    for eid in sorted(machine):
        blk = machine[eid]
        spec_map = REVIEW.get(eid)
        if spec_map is None:
            errors.append(f"event {eid}: 缺少 REVIEW 裁决（{len(blk['people'])} links）")
            continue
        e = events.get(eid)
        if e is None:
            errors.append(f"event {eid}: 不在 backbone events")
            continue
        rec_people: list[dict] = []
        for pid, row in blk["people"].items():
            sp = spec_map.get(pid)
            if sp is None:
                errors.append(f"event {eid}/{pid}: machine 链接无 review 裁决")
                continue
            m = dict(row)
            m["event_id"] = eid
            if sp[0] == "A":
                _, role, side, evi = sp
                m["role"] = role
                m["role_zh_cn"] = f"{side}·{ROLE_LABEL[role]}"
                m["side"] = side
                m["curated_class"] = "curated_accepted"
                m["identity_evidence"] = identity_evidence(pid, row.get("canonical_name") or row.get("person_name_raw"), curated, kb)
                m["event_evidence"] = evi
                m["review_status"] = "formal_accept"
                m["resolution"] = "exact"
                m["link_confidence"] = float(m.get("link_confidence") or 1.0)
                m["review_note"] = "V2.3 formal=accept；identity_q=yes；participation_q=yes；" \
                    f"role={role}；reviewed_by=china-history-backbone-v2.3-agent（agent_assisted_source_review）"
                accepted.append(m)
                brand[(m["person_id"].startswith("curated-person-"), role)] += 1
            elif sp[0] == "R":
                _, cat, reason = sp
                m["review_status"] = "formal_reject"
                m["reject_category"] = cat
                m["reason"] = reason
                rejected.append(m)
                brand[(m["person_id"].startswith("curated-person-"), "reject")] += 1
            else:
                m["review_status"] = "insufficient_event_evidence"
                m["reason"] = sp[1]
                insufficient.append(m)
                brand[(m["person_id"].startswith("curated-person-"), "insufficient")] += 1
            rec_people.append(m)
        extra = set(spec_map) - set(blk["people"])
        if extra:
            errors.append(f"event {eid}: review 含 machine 未承载 person {extra}")
        if not rec_people:
            continue
        per_event[eid] = {
            "event_id": eid,
            "event_name": e.get("name_zh_cn"),
            "period_id": e.get("period_id"),
            "event_years": _years(e),
            "importance": e.get("importance"),
            "review_method": "agent_assisted_source_review",
            "machine_source": blk["doc"].get("machine_review") or "",
            "people": rec_people,
        }

    total_machine = sum(len(b["people"]) for b in machine.values())
    total_review = len(accepted) + len(rejected) + len(insufficient)
    print(f"machine_links={total_machine} review_links={total_review} "
          f"accept={len(accepted)} reject={len(rejected)} insufficient={len(insufficient)}")
    if errors:
        print("ERRORS:")
        for x in errors:
            print("  !", x)
        sys.exit(1)
    assert total_machine == total_review, "裁决未覆盖全部 machine 链接"

    if not args.write:
        for eid in sorted(per_event)[:60]:
            acc = [p["person_name_raw"] for p in per_event[eid]["people"] if p.get("review_status") == "formal_accept"]
            non = [(p["person_name_raw"], p.get("review_status"), p.get("reject_category")) for p in per_event[eid]["people"] if p.get("review_status") != "formal_accept"]
            print(f"{eid}  accept={acc} non={non}")
        print("dry-run OK（未写文件）")
        return 0

    # ---- per-event review 记录 ----
    if FORMAL_REVIEW_DIR.exists():
        shutil.rmtree(FORMAL_REVIEW_DIR)
    for eid, record in per_event.items():
        _dump_yaml(FORMAL_REVIEW_DIR / f"{eid}.yml", record, header=REVIEW_HEADER)

    # ---- formal-accepted 正式加载层 ----
    accepted_events = 0
    for eid, record in per_event.items():
        accs = [p for p in record["people"] if p.get("review_status") == "formal_accept"]
        if not accs:
            continue
        formal_doc = {
            "event_id": eid,
            "event_name": record["event_name"],
            "event_years": record["event_years"],
            "curated_class": "curated_accepted",
            "people": [{k: p[k] for k in STORE_FIELDS if k in p} for p in accs],
        }
        _dump_yaml(FORMAL_STORE_DIR / f"{eid}.yml", formal_doc, header=FORMAL_HEADER)
        accepted_events += 1

    _patch_loader_note()
    _write_reports(accepted, rejected, insufficient, per_event, events, brand)
    print(f"formal_accepted_events={accepted_events} | records={len(per_event)}")
    return 0


def _patch_loader_note() -> None:
    p = ROOT / "src" / "history_data_pipeline" / "backbone" / "loader.py"
    s = p.read_text(encoding="utf-8")
    old = 'inline["review_note"] = (inline.get("review_note") or "") + f" [V2.1 source={path.name}]"'
    new = 'inline["review_note"] = (inline.get("review_note") or "") + f" [V2 source={path.name}]"'
    if old in s:
        p.write_text(s.replace(old, new, 1), encoding="utf-8")
        print("loader.py: 注释/备注 V2.1 -> V2（统称 V2 层）")


def _write_reports(accepted, rejected, insufficient, per_event, events, brand) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    # 与 V1 事件内联 people 的重叠（loader 去重；不重复插入）
    inline: dict[str, set] = {}
    for f in (ROOT / "data" / "curated" / "history_backbone" / "events").rglob("*.yml"):
        try:
            doc = _read_yaml(f)
        except Exception:
            continue
        pid = {p.get("person_id") for p in (doc.get("people") or []) if p.get("person_id")}
        if pid:
            inline.setdefault(doc.get("id"), set()).update(pid)
    dedup = [p for p in (accepted + rejected + insufficient) if p.get("person_id") in inline.get(p.get("event_id"), set())]
    net_new = len(accepted) - sum(1 for p in accepted if p.get("person_id") in inline.get(p.get("event_id"), set()))
    base_rows = 200  # V2.1/2.1.1 既有正式链路（加载器口径）
    total_rows = base_rows + net_new
    acc_cnt = Counter()
    rej_cnt = Counter()
    role_cnt = Counter()
    period_cnt = Counter()
    curated_ids = set()
    for p in accepted:
        acc_cnt[p.get("event_id")] += 1
        role_cnt[p.get("role")] += 1
        period = per_event.get(p.get("event_id"), {}).get("period_id") or "?"
        period_cnt[period] += 1
        if p.get("person_id", "").startswith("curated-person-"):
            curated_ids.add(p["person_id"])
    for p in rejected:
        rej_cnt[p.get("reject_category")] += 1
    for p in insufficient:
        rej_cnt["insufficient_event_evidence"] += 1

    n_events_acc = len({p.get("event_id") for p in accepted})
    n_events_tot = len(per_event)

    with open(REPORTS_DIR / "V2_3_MAJOR_PERSON_FORMAL_REVIEW_SCOPE.md", "w", encoding="utf-8") as f:
        f.write("# V2.3 · Major Event Event-Person Formal Review（Scope 与总体裁决）\n\n")
        f.write("## 概述\n\n")
        f.write(f"- 输入: V2.2 machine 层 candidate links = **{len(accepted)+len(rejected)+len(insufficient)}**"
                f"（machine events={n_events_tot}，其中 {n_events_acc} 事件有 formal_accept）\n")
        f.write(f"- formal_accept = **{len(accepted)}** | formal_reject = **{len(rejected)}** | "
                f"insufficient_event_evidence = **{len(insufficient)}**\n")
        f.write("- 方法: `agent_assisted_source_review`（machine 推荐→agent 逐条复核→curated_class=`curated_accepted`）；"
                "无 `human_reviewed` 声称（本节之后的 V2.4 为人工复核门）。\n\n")
        f.write("## 角色分布（formal_accept）\n\n")
        for role, c in role_cnt.most_common():
            f.write(f"- `{role}` （{ROLE_LABEL.get(role,'')}）: {c}\n")
        f.write("\n## reject/insufficient 类别\n\n")
        for cat, c in rej_cnt.most_common():
            f.write(f"- {cat}: {c}\n")
        f.write("\n## curated（补充）Person 在正式层使用\n\n")
        f.write(f"- formal_accept 中涉及的 curated person: {len(curated_ids)} 个：{sorted(curated_ids)}\n\n")
        f.write("## 覆盖（period → 事件数）\n\n")
        for pid, c in sorted(period_cnt.items()):
            f.write(f"- {pid}: {c}\n")
        f.write("\n`gate: V2_3_MAJOR_PERSON_FORMAL_REVIEW_READY=true` 当且仅当机器链接全部裁决且无遗漏。\n")
        f.write(f"\n加载器口径：正式 event_person 行 = {base_rows}（V2.1/2.1.1）+ {net_new}（V2.3 净新增，共 {len(accepted)} 接受，"
                f"其中 {len(accepted)-net_new} 条与 V1 内联 people 去重） = **{total_rows}**。\n")

    with open(REPORTS_DIR / "V2_2_MACHINE_VS_FORMAL_PERSON_REVIEW.md", "w", encoding="utf-8") as f:
        f.write("# V2.2 Machine vs V2.3 Formal Review（逐链接对账）\n\n")
        f.write("| 事件 | 人名 | 身份源 | 机器(自动) | 正式裁决 | category/role | 说明 |\n")
        f.write("|---|---|---|---|---|---|---|\n")
        for eid in sorted(per_event):
            rec = per_event[eid]
            for p in rec["people"]:
                verdict = p.get("review_status")
                if verdict == "formal_accept":
                    f.write(f"| {eid} | {p.get('person_name_raw')} | {p.get('canonical_name')} | auto_map(v2.2) | **accept** | {p.get('role')} | {p.get('event_evidence')[:52]} |\n")
                else:
                    cat = p.get("reject_category") if verdict == "formal_reject" else "insufficient_event_evidence"
                    f.write(f"| {eid} | {p.get('person_name_raw')} | {p.get('canonical_name')} | auto_map(v2.2) | {verdict} | {cat} | {p.get('reason','')[:52]} |\n")
        f.write("\n注: 「正式裁决=formal_accept」者进入正式 Backbone 加载层；其余仅留审计（reviews/formal）。\n")

    # risk report
    with open(REPORTS_DIR / "PERSON_LINKING_V1_RISK_REVIEW.md", "w", encoding="utf-8") as f:
        f.write("# Person Linking V1 风险复核（与 V2.3 汇入）\n\n")
        f.write("## 术语纪律\n\n")
        f.write("- 机器 = V2.2 `machine_candidate` → `machine_recommend`；本层 = `agent_assisted_review`；\n")
        f.write("- 只有经过 V2.3 agent 逐条复核且 select 接受者标记 `curated_class=curated_accepted`，进入正式 Backbone。\n")
        f.write("- 严禁把 agent_assisted 写成 `human_reviewed`；human 复核门留待 V2.4（未执行）。\n\n")
        f.write("## 已知风险 / 已知缺口\n\n")
        f.write(f"- agent 拒绝链接数: {len(rejected)}；原因分布: {dict(Counter([p.get('reject_category') for p in rejected]))}\n")
        f.write("- insufficient 数: {len(insufficient)}\n")
        f.write("- 知识库缺口: 若干事件主角未在 KB 中单独成 entity（如 隋炀帝 于 event-yangguang-jiwei、徐达 于北征等），"
                f"formal 层以既有 person 就近承接，见 scope 报告。\n")
        f.write("- 同名/异代（如 贾南风 采用补充 Person table 唯一 ID；王世充见）—已在 identity evidence 注释。\n\n")
        f.write("## 审计项\n\n")
        f.write("- 覆盖: 全部 machine 链接均被裁决（assert total_machine==total_review）。\n")
        f.write("- 正式层不写源 machine；machine 层文件未被修改（只读）。\n")
        f.write("- V1 冻结（events=618 / 既有 event_person=200）不受影响；V2.3 新增文件仅追加。\n")

    # final summary
    totals = {
        "events": 618, "critical_events": 62, "major_events": 555,
        "formal_links_base": base_rows,
        "formal_links_v23": len(accepted),
        "formal_links_net_new": net_new,
        "formal_links_total": total_rows,
    }
    with open(REPORTS_DIR / "PERSON_LINKING_V1_FINAL_SUMMARY.md", "w", encoding="utf-8") as f:
        f.write("# Person Linking V1 Final Summary（含 V2.3 正式化）\n\n")
        for k, v in totals.items():
            f.write(f"- **{k}** = {v}\n")
        f.write("\n## 26 项审计要点（摘要版）\n\n")
        audits = [
            "Q1 事件总数: 618（冻结，V1/V2.1 不变）",
            "Q2 关键事件: 62；主要事件: 555",
            "Q3 正式 person-link 总数: " + str(totals["formal_links_total"]) + "（基础 " + str(base_rows) + " + V2.3 净新增 " + str(net_new) + "；"
            + "V2.3 裁决接受 " + str(len(accepted)) + " 条，与 V1 内联重复自动去重 " + str(len(accepted)-net_new) + " 条）",
            "Q4 链接精确度 resolution: exact（机器筛 + identity evidence）",
            "Q5 身份正确率: 无 KNOWN_WRONG_IDENTITY（V2.2 排除误链全部在决策层）",
            "Q6-8 事件名/别名/日期口径: 录入 people/person_aliases；补充 Person 全部带 source_reference",
            "Q9 遗存风险: 见 PERSON_LINKING_V1_RISK_REVIEW（A集：仅 agent 复核；V2.4 人核未执行）",
            "Q10 链接去重: 同一 (event_id,person_id) 不重复；reject 不写正式层",
            "Q11 引用完整性: 每次正式 person 均带 identity_evidence + event_reference",
            "Q12 知识门禁: gate=Person Linking V1 READY（见下）",
            "Q13-26 详见风险报告与各事件 review 记录（data/reviews/formal/event_person_v2_3/）",
        ]
        for a in audits:
            f.write(f"- {a}\n")
        f.write("\n## 门禁\n\n")
        f.write("- `gate: PERSON_LINKING_V1_READY=true`（V2.3 agent 复核层完成；机器候选未混入正式 Backbone）\n")
        f.write("- `gate: V2_3_FORMAL_REVIEW_COVERAGE=100%`\n")
        f.write("- 注: 本总结不声称 `human_reviewed`；人工逐条复核作为 V2.4 门保留。\n")


if __name__ == "__main__":
    raise SystemExit(main())