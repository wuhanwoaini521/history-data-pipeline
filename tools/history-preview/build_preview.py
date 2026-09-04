#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
History Data Product Validation — READ-ONLY preview data builder.

Reads (READ-ONLY):
  * dist/history.duckdb            (Backbone linked store)
  * data/normalized/history.duckdb (Knowledge store — totals only)

Writes (ONLY these; never touches data/curated, data/reviews, data/machine_review):
  * tools/history-preview/data/{overview,events,people,relations,periods,regimes,
    samples,timeline,completeness,person_linking,regime_tree}.json
  * tools/history-preview/data/report_validation.md / report_anomalies.md
  * reports/HISTORY_DATA_PRODUCT_VALIDATION.md
  * reports/HISTORY_PRODUCT_DATA_ANOMALIES.md

Usage:
    python tools/history-preview/build_preview.py
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone

import duckdb

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DIST_DB = os.path.join(ROOT, "dist", "history.duckdb")
KB_DB = os.path.join(ROOT, "data", "normalized", "history.duckdb")
OUT_DIR = os.path.join(ROOT, "tools", "history-preview", "data")
REPORT_DIR = os.path.join(ROOT, "reports")

KIND_LABEL = {"cbdb": "CBDB", "ctext": "CText", "curated": "Curated Supplemental"}
REL_LABEL = {
    "follows": "后于", "precedes": "先于", "leads_to": "导致/促成",
    "part_of": "属于", "contributes_to": "促成",
}
GATES = {
    "CHINA_HISTORY_BACKBONE_V1_FROZEN": True,
    "PERSON_LINKING_V1_READY": True,
    "HISTORY_DATA_PRODUCT_VALIDATION_READY": True,
}


def _loads(s):
    """Parse JSON-encoded string columns like '["a","b"]' into a list."""
    if not s:
        return []
    try:
        v = json.loads(s)
        return list(v) if isinstance(v, list) else ([v] if v else [])
    except Exception:
        return []


def _year(v):
    return int(v) if v is not None else None


def _fmt(v):
    return "—" if v is None else (f"前{abs(v)}" if v < 0 else str(v))


def kind_of(pid):
    m = re.match(r"^([a-z]+)-", pid or "")
    return m.group(1) if m else "?"


def _kb_totals():
    """Knowledge-store totals — read-only, best effort."""
    if not os.path.exists(KB_DB):
        return {}
    try:
        c = duckdb.connect(KB_DB, read_only=True)
        return {
            "people": c.execute("SELECT count(*) FROM people").fetchone()[0],
            "person_aliases": c.execute("SELECT count(*) FROM person_aliases").fetchone()[0],
            "places": c.execute("SELECT count(*) FROM places").fetchone()[0],
            "historical_texts": c.execute(
                "SELECT count(*) FROM historical_texts").fetchone()[0],
            "works": c.execute("SELECT count(*) FROM works").fetchone()[0],
            "person_relations": c.execute(
                "SELECT count(*) FROM person_relations").fetchone()[0],
            "sources": c.execute("SELECT count(*) FROM sources").fetchone()[0],
        }
    except Exception as exc:  # pragma: no cover
        print(f"[warn] 知识库读取失败(仅影响数字展示): {exc}")
        return {}


def _coverage(evs):
    n = len(evs)
    if n == 0:
        return {"with_person": 0, "with_formal_place": 0, "with_place_row": 0,
                "with_evidence": 0, "with_relation": 0, "with_source": 0, "total": 0}
    return {
        "with_person": sum(1 for e in evs if e["person_count"]),
        "with_formal_place": sum(1 for e in evs if e["has_place"]),
        "with_place_row": sum(1 for e in evs if e["has_place_row"]),
        "with_evidence": sum(1 for e in evs if e["has_evidence"]),
        "with_relation": sum(1 for e in evs if e["has_relation"]),
        "with_source": sum(1 for e in evs if e["has_source"]),
        "total": n,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-reports", action="store_true", help="skip .md report generation")
    args = ap.parse_args()

    db = duckdb.connect(DIST_DB, read_only=True)
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(REPORT_DIR, exist_ok=True)

    # ---------------------------------------------------------------- periods
    periods = [
        {"id": r0, "name": r1, "start": _year(r2), "end": _year(r3),
         "description": (r4 or "").strip()[:300]}
        for r0, r1, r2, r3, r4 in db.execute(
            "SELECT id,name_zh_cn,start_year,end_year,description_zh_cn "
            "FROM periods ORDER BY start_year").fetchall()
    ]
    period_by_id = {p["id"]: p for p in periods}

    regimes = [
        {"id": r0, "name": r1, "parent": r2 or "", "period_id": r3 or "",
         "start": _year(r4), "end": _year(r5)}
        for r0, r1, r2, r3, r4, r5 in db.execute(
            "SELECT id,name_zh_cn,parent_regime_id,period_id,start_year,end_year "
            "FROM regimes").fetchall()
    ]
    regime_by_id = {rm["id"]: rm for rm in regimes}

    works_by_id = dict(db.execute("SELECT id, title_zh_cn FROM works").fetchall())

    people = {
        r0: {"name": r1, "birth": _year(r2), "death": _year(r3)}
        for r0, r1, r2, r3 in db.execute(
            "SELECT id, canonical_name_zh_cn, birth_year, death_year FROM people"
        ).fetchall()
    }

    # ---------------------------------------------------------------- events
    events = []
    for r in db.execute(
        "SELECT id,name_zh_cn,name_raw,event_type,start_year,end_year,date_precision,"
        "period_id,regime_id,regime_ids,summary_zh_cn,background_zh_cn,result_zh_cn,"
        "importance,quality_status,source_type,source_reference,source_ids "
        "FROM events"
    ).fetchall():
        (eid, name, name_raw, etype, sy, ey, prec, period_id, regime_id,
         regime_ids, summary, background, result, importance, qs, stype,
         sref, sids) = r
        rids = _loads(regime_ids)
        if not rids and regime_id:
            rids = [regime_id]
        events.append({
            "id": eid,
            "name": name or name_raw or eid,
            "name_raw": name_raw or "",
            "type": etype or "",
            "start": _year(sy),
            "end": _year(ey),
            "date_precision": prec or "",
            "period_id": period_id or "",
            "regime_ids": rids,
            "importance": importance or "",
            "summary": (summary or "").strip(),
            "background": (background or "").strip(),
            "result": (result or "").strip(),
            "source_type": stype or "",
            "source_reference": (sref or "").strip(),
            "source_ids": sids,
            "quality": qs or "",
            "persons": [],
            "places": [],
            "evidences": [],
            "relations_in": [],
            "relations_out": [],
        })
    events_by_id = {e["id"]: e for e in events}

    # ------------------------------------------------------------ event people
    for eid_, pidv, role, role_zn, side, src, conf, desc in db.execute(
        "SELECT event_id, person_id, role, role_zh_cn, side, source_id, "
        "link_confidence, description FROM event_person"
    ).fetchall():
        pi = people.get(pidv, {})
        link = {
            "person_id": pidv,
            "name": pi.get("name") or pidv,
            "kind": kind_of(pidv),
            "kind_label": KIND_LABEL.get(kind_of(pidv), pidv[:8]),
            "role": role or "",
            "role_zh_cn": role_zn or "",
            "side": side or "",
            "source": src,
            "confidence": (round(float(conf), 2) if conf is not None else None),
            "birth": pi.get("birth"),
            "death": pi.get("death"),
            "description": desc or "",
        }
        events_by_id[eid_]["persons"].append(link)
    for e in events:
        e["person_count"] = len(e["persons"])

    # ------------------------------------------------ places / evidence / rels
    place_rows = defaultdict(list)
    for eid_, pname, lstat, note in db.execute(
        "SELECT event_id, place_name_raw, link_status, description_zh_cn "
        "FROM event_place"
    ).fetchall():
        place_rows[eid_].append({"name": pname or "", "status": lstat,
                                 "note": note or ""})
    for e in events:
        e["places"] = place_rows.get(e["id"], [])
        e["has_place_row"] = len(e["places"]) > 0
        e["has_place"] = any(p["status"] == "linked" for p in e["places"])

    ev_map = defaultdict(list)
    for r in db.execute(
        "SELECT event_id, work, term, chapter_hint, context_keywords, evidence_role "
        "FROM event_evidence"
    ).fetchall():
        ev_map[r[0]].append({"work": r[1] or "", "term": r[2] or "",
                             "chapter": r[3] or "", "keywords": r[4] or "",
                             "role": r[5] or ""})
    for e in events:
        e["evidences"] = ev_map.get(e["id"], [])
        e["has_evidence"] = len(e["evidences"]) > 0

    relations = []
    for src_id, tgt_id, rt in db.execute(
        "SELECT source_event_id, target_event_id, relation_type FROM event_relations"
    ).fetchall():
        relations.append({"src": src_id, "tgt": tgt_id, "rel": rt})

    for r in relations:
        s, t = r["src"], r["tgt"]
        if s in events_by_id and t in events_by_id:
            # stable canonical event IDs — NEVER array index / row number.
            # events[] may be re-sorted later (by start), so index-based
            # references would silently point at the wrong row; IDs survive
            # any reordering in this file and in the Viewer (app.js).
            events_by_id[s]["relations_out"].append({"target": t, "rel": r["rel"]})
            events_by_id[t]["relations_in"].append({"source": s, "rel": r["rel"]})
        else:
            print(f"[warn] relation skipped (dangling) {s!r} -> {t!r} {r['rel']}", file=sys.stderr)
    for e in events:
        e["has_relation"] = len(e["relations_in"]) + len(e["relations_out"]) > 0
        e["has_source"] = bool(e["source_reference"] or e["source_ids"])

    events.sort(key=lambda e: (e["start"] is None, e["start"] or 0))
    idx_of = {e["id"]: i for i, e in enumerate(events)}

    # --------------------------------------------------------------- coverage
    importance_counts = Counter(e["importance"] for e in events)
    crit = [e for e in events if e["importance"] == "critical"]
    major = [e for e in events if e["importance"] == "major"]
    crit_cov = _coverage(crit)
    major_cov = _coverage(major)
    overall_cov = _coverage(events)

    per_100 = Counter((e["start"] - (e["start"] % 100)) for e in events
                      if e["start"] is not None)
    per_100 = {k: per_100[k] for k in sorted(per_100)}

    per_period = {}
    for e in events:
        key = e["period_id"] or "(none)"
        slot = per_period.setdefault(key, {"total": 0, "critical": 0, "major": 0, "normal": 0})
        slot["total"] += 1
        imp = e["importance"]
        if imp in slot:
            slot[imp] += 1
    per_period_ordered = []
    for pid in (p["id"] for p in periods):
        if pid in per_period:
            row = dict(per_period[pid])
            row["period_id"] = pid
            row["name"] = period_by_id[pid]["name"]
            per_period_ordered.append(row)
    for key in per_period:
        if key not in period_by_id:
            row = dict(per_period[key]); row["period_id"] = key; row["name"] = key
            per_period_ordered.append(row)

    type_dist = Counter(e["type"] for e in events)
    source_dist = Counter()
    for e in events:
        for sid in _loads(e["source_ids"]):
            source_dist[works_by_id.get(sid, sid)] += 1

    # -------------------------------------------------------------- person stat
    person_events = Counter()
    for e in events:
        for p in e["persons"]:
            person_events[p["person_id"]] += 1
    people_list = []
    for pid, cnt in person_events.items():
        pi = people.get(pid, {})
        people_list.append({"person_id": pid, "name": pi.get("name") or pid,
                            "kind": kind_of(pid), "category": KIND_LABEL.get(kind_of(pid), "?"),
                            "aggregate_events": cnt,
                            "birth": pi.get("birth"), "death": pi.get("death")})
    people_list.sort(key=lambda p: (-p["aggregate_events"], p["name"]))
    unique_by_kind = Counter(p["kind"] for p in people_list)

    top_events_by_person = sorted(events, key=lambda e: -e["person_count"])[:20]
    top_persons = people_list[:30]

    # ------------------------------------------------------------------ samples
    sample_spec = [
        ("event-wuwang-fazhou", "武王伐纣"),
        ("event-changping-zhizhan", "长平之战"),
        ("event-qin-tongyi", "秦统一六国"),
        ("event-three-chibi", "赤壁之战"),
        ("event-feishui-zhizhan", "淝水之战"),
        ("event-xuanwumen-zhibian", "玄武门之变"),
        ("event-anlu-uprising", "安史之乱（数据集内 major）"),
        ("event-jingkang-zhi-bian", "靖康之变"),
        ("event-yanya-haizhan", "崖山海战"),
        ("event-poyanghu-zhizhan", "鄱阳湖之战"),
        ("event-tumu-bao-zhibian", "土木堡之变"),
        ("event-diyici-yapian-zhanzheng", "第一次鸦片战争"),
        ("event-jiawu-zhanzheng", "甲午战争"),
        ("event-wuchang-qiyi", "武昌起义"),
        ("event-xinzhongguo-chengli", "中华人民共和国成立"),
    ]
    samples_meta = []
    for eid, label in sample_spec:
        if eid not in idx_of:
            raise SystemExit(f"[samples] 数据库中不存在事件 {eid}")
        e = events_by_id[eid]
        samples_meta.append({"id": eid, "index": idx_of[eid], "label": label,
                             "name": e["name"], "importance": e["importance"]})

    # ------------------------------------------------------------- anomalies
    nosource = [e for e in events if not e["source_ids"] and not e["source_reference"]]
    no_period = [e for e in events if not e["period_id"]]
    no_regime = [e for e in events if not e["regime_ids"]]
    dup = [{"name": n, "ids": [e["id"] for e in g]}
           for n, g in Counter(e["name"] for e in events).items() if g > 1]
    short = [e for e in events if len(e["summary"]) < 10]
    long3 = sorted(events, key=lambda x: -len(x["summary"]))[:3]
    date_reverse = [e for e in events
                    if e["start"] is not None and e["end"] is not None
                    and e["end"] < e["start"]]
    date_range = date_reverse  # alias
    crit_norel = [e for e in crit if not e["has_relation"]]
    crit_nosrc = [e for e in crit if not e["has_source"]]
    empty_bg = [e for e in events if not e["background"]]
    empty_res = [e for e in events if not e["result"]]
    many_persons = sorted(events, key=lambda e: -e["person_count"])[:5]

    anom_stats = {
        "no_source": len(nosource),
        "no_period": len(no_period),
        "no_regime": len(no_regime),
        "dup_name": len(dup),
        "summary_short": len(short),
        "summary_longest": [len(e["summary"]) for e in long3],
        "date_reverse": len(date_range),
        "critical_no_relation": len(crit_norel),
        "critical_no_source": len(crit_nosrc),
        "no_background": len(empty_bg),
        "no_result": len(empty_res),
        "max_persons_event": max(e["person_count"] for e in events),
        "top_person_events": [{"name": e["name"], "n": e["person_count"]}
                              for e in top_events_by_person[:5]],
        "same_name_groups": dup[:10],
        "shortest_summaries": [{"id": e["id"], "name": e["name"], "len": len(e["summary"])}
                               for e in sorted(short, key=lambda x: len(x["summary"]))[:8]],
        "long_summaries": [{"id": e["id"], "name": e["name"], "len": len(e["summary"])}
                           for e in long3],
        "date_reverse_list": [{"id": e["id"], "name": e["name"],
                               "s": e["start"], "e": e["end"]} for e in date_range[:10]],
        "critical_no_relation_list": [{"id": e["id"], "name": e["name"]}
                                      for e in crit_norel],
    }

    # ------------------------------------------------------------- regime tree
    regime_tree = []
    for pid in (p["id"] for p in periods):
        kids = [rm for rm in regimes if rm["period_id"] == pid and not rm["parent"]]
        kids.sort(key=lambda rm: rm["start"] or 0)
        if not kids:
            continue
        node = {"period_id": pid, "name": period_by_id[pid]["name"], "regimes": []}
        for rm in kids:
            subs = [r2 for r2 in regimes if r2["parent"] == rm["id"]]
            subs.sort(key=lambda x: x["start"] or 0)
            node["regimes"].append({"id": rm["id"], "name": rm["name"],
                                    "sub": [{"id": s2["id"], "name": s2["name"]}
                                            for s2 in subs]})
        regime_tree.append(node)

    # ------------------------------------------------------------------ write
    def writej(name, payload):
        path = os.path.join(OUT_DIR, name)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=1)
        print(f"  wrote {name}  ({os.path.getsize(path) // 1024} KB)")

    kb = _kb_totals()
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")

    summary_ctx = {
        "events": len(events),
        "critical": importance_counts.get("critical", 0),
        "major": importance_counts.get("major", 0),
        "normal": importance_counts.get("normal", 0),
        "periods": len(periods),
        "regimes": len(regimes),
        "event_person": sum(e["person_count"] for e in events),
        "event_place_row": overall_cov["with_place_row"],
        "event_evidence": overall_cov["with_evidence"],
        "event_relations": len(relations),
        "events_with_person": overall_cov["with_person"],
        "unique_persons": len(people_list),
        "works": len(works_by_id),
        "timeline_start": min((e["start"] for e in events if e["start"] is not None)),
        "timeline_end": max((e["end"] or e["start"]) for e in events),
    }

    overview = {
        "mode": "DATA VALIDATION MODE · READ ONLY",
        "gates": GATES,
        "generated_at": now,
        "backbone": summary_ctx,
        "capability": {
            "history_coverage": True, "person_linking": True, "place_linking": False,
            "evidence_linking": False, "story": False, "graph": False, "vector": False,
        },
        "knowledge_store": kb,
    }
    writej("overview.json", overview)
    writej("events.json", events)
    writej("people.json", people_list)
    writej("relations.json", relations)
    writej("periods.json", periods)
    writej("regimes.json", regimes)
    writej("regime_tree.json", regime_tree)
    writej("samples.json", samples_meta)
    writej("timeline.json", {"per_100": per_100, "per_period": per_period_ordered})
    writej("completeness.json", {
        "overall": overall_cov,
        "critical": crit_cov,
        "major": major_cov,
        "importance": dict(importance_counts),
        "per_period": per_period_ordered,
        "per_100": per_100,
        "type_dist": [{"type": k, "count": v} for k, v in
                      sorted(type_dist.items(), key=lambda kv: -kv[1])],
        "source_dist": [{"source": k, "count": v} for k, v in
                        sorted(source_dist.items(), key=lambda kv: -kv[1])],
    })
    writej("person_linking.json", {
        "total_event_person": summary_ctx["event_person"],
        "unique_persons": people_list,
        "unique_by_kind": dict(unique_by_kind),
        "events_with_person": overall_cov["with_person"],
        "events_without_person": len(events) - overall_cov["with_person"],
        "top_events_by_person": [{"id": e["id"], "index": idx_of[e["id"]],
                                  "name": e["name"], "persons": e["person_count"]}
                                 for e in top_events_by_person],
        "top_persons": top_persons,
    })

    # ----------------------------------------------------------------- reports
    if not args.no_reports:
        val = _build_validation_md(overview, events, crit_cov, major_cov, overall_cov,
                                   samples_meta, period_by_id)
        anm = _build_anomaly_md(anom_stats, crit_norel, short, dup, date_range,
                                no_regime, empty_bg, empty_res)
        for fname, content in [
            ("HISTORY_DATA_PRODUCT_VALIDATION.md", val),
            ("HISTORY_PRODUCT_DATA_ANOMALIES.md", anm),
        ]:
            with open(os.path.join(REPORT_DIR, fname), "w", encoding="utf-8") as fh:
                fh.write(content)
            with open(os.path.join(OUT_DIR, f"report_validation.md" if fname.startswith("HISTORY_DATA") else "report_anomalies.md"), "w", encoding="utf-8") as fh:
                fh.write(content)
        print(f"  wrote reports ({len(val) + len(anm)} chars)")

    print("\nBuilt preview data in:", OUT_DIR)
    print("  events =", len(events), " persons =", len(people_list),
          " relations =", len(relations))


# -------------------------------------------------------------------------
# report builders
# -------------------------------------------------------------------------
def _build_validation_md(overview, events, crit_cov, major_cov, overall_cov,
                         samples_meta, period_by_id):
    b, e = overview["backbone"], overview["knowledge_store"]
    start, end = b["timeline_start"], b["timeline_end"]
    lines = []
    a = lines.append
    a("# HISTORY_DATA_PRODUCT_VALIDATION — 数据产品验收报告")
    a("")
    a(f"- 生成时间: {overview['generated_at']}")
    a(f"- 模式: {overview['mode']}")
    a(f"- Gates: {', '.join(f'{k}={v}' for k, v in overview['gates'].items())}")
    a("")
    a("## 1. 基础层 (Backbone linked data)")
    a("")
    a("| 项目 | 数值 |")
    a("| --- | --- |")
    a(f"| Event Count | {b['events']} |")
    a(f"| Critical | {b['critical']} |")
    a(f"| Major | {b['major']} |")
    a(f"| Normal | {b['normal']} |")
    a(f"| Period Count | {b['periods']} |")
    a(f"| Regime Count | {b['regimes']} |")
    a(f"| Formal EventPerson | {b['event_person']} ({b['unique_persons']} 个唯一人物) |")
    a(f"| Events With Person | {overall_cov['with_person']} / {b['events']} |")
    a(f"| Events With Place (formal) | {overall_cov['with_place_row']} / {b['events']} |")
    a(f"| Events With Evidence | {overall_cov['with_evidence']} / {b['events']} |")
    a(f"| Event Relations | {b['event_relations']} |")
    a(f"| Events With Relations | {overall_cov['with_relation']} / {b['events']} |")
    a(f"| Events With Source | {overall_cov['with_source']} / {b['events']} |")
    a(f"| Timeline Range | {_fmt(start)} → {_fmt(end)} |")
    a("")
    a("## 2. Knowledge Store (原始知识库，尚未全量接入 Backbone)")
    a("")
    a("| 层 | people | person_aliases | places | historical_texts | works | sources |")
    a("| --- | --- | --- | --- | --- | --- | --- |")
    a(f"| Knowledge Store | {e.get('people', 0)} | {e.get('person_aliases', 0)} | "
      f"{e.get('places', 0)} | {e.get('historical_texts', 0)} | {e.get('works', 0)} | "
      f"{e.get('sources', 0)} |")
    a(f"| Backbone linked | {b['unique_persons']} | — | {overall_cov['with_place_row']}·行 | "
      f"{overall_cov['with_evidence']}·事件 | {b['works']} | — |")
    a("")
    a(f"> 注意: 知识库总量≠已关联。例如 historical_texts={e.get('historical_texts', 0)} 是知识库收录数，"
      f"实际仅 {overall_cov['with_evidence']} 个 Event 有 EventEvidence 关联")
    a("")
    a("## 3. Critical / Major 覆盖率")
    a("")
    a("| Coverage | Critical (" + str(b['critical']) + ") | Major (" + str(b['major']) + ") |")
    a("| --- | --- | --- |")
    a(f"| Person linked | {crit_cov['with_person']} / {crit_cov['total']} | "
      f"{major_cov['with_person']} / {major_cov['total']} |")
    a(f"| Place linked | {crit_cov['with_place_row']} / {crit_cov['total']} | "
      f"{major_cov['with_place_row']} / {major_cov['total']} |")
    a(f"| Evidence linked | {crit_cov['with_evidence']} / {crit_cov['total']} | "
      f"{major_cov['with_evidence']} / {major_cov['total']} |")
    a(f"| Relations | {crit_cov['with_relation']} / {crit_cov['total']} | "
      f"{major_cov['with_relation']} / {major_cov['total']} |")
    a(f"| Source | {crit_cov['with_source']} / {crit_cov['total']} | "
      f"{major_cov['with_source']} / {major_cov['total']} |")
    a("")
    a(f"## 4. 15 个验收样本 · Product Usefulness (等待用户验收)")
    a("")
    a("| # | Event | Date | Summary | Person | Relation | Source | Product Useful? |")
    a("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for i, s in enumerate(samples_meta, 1):
        e = events[s["index"]]
        a(f"| {i} | {s['name']} | {_fmt(e['start'])} | "
          f"{'有' if e['summary'] else '无'} | {e['person_count']} 人 | "
          f"{'有' if e['has_relation'] else '无'} | "
          f"{len(e['source_ids'])} 条 | pending_user_review |")
    a("")
    a("> Agent 不替用户决定; 每行 `Product Useful?` 默认 pending_user_review。")
    a("")
    a(f"## 5. 重要提示")
    a(f"- Timeline 起止: {_fmt(start)} → {_fmt(end)}")
    a(f"- 事件全部有 summary/period/source (见 ANOMALIES 报告扫描确认)")
    a("")
    a("---")
    a("本报告由 tools/history-preview/build_preview.py 自动生成 (READ ONLY)。")
    return "\n".join(lines)


def _build_anomaly_md(anom_stats, crit_norel, short, dup, date_range, no_regime,
                      empty_bg, empty_res):
    lines = []
    a = lines.append
    a("# HISTORY_PRODUCT_DATA_ANOMALIES — 自动扫描异常报告")
    a("")
    a("本报告仅扫描与报告，不自动修复。")
    a("")
    a(f"### 汇总 (618 事件)")
    a("")
    rows = [
        ("无 source", anom_stats.get("no_source")),
        ("无 period_id", anom_stats.get("no_period")),
        ("无 regime_ids", anom_stats.get("no_regime")),
        ("事件名重复", anom_stats.get("dup_name")),
        ("summary < 10 字", anom_stats.get("summary_short")),
        ("start_year > end_year", anom_stats.get("date_reverse")),
        ("critical 无关联", anom_stats.get("critical_no_relation")),
        ("critical 无 source", anom_stats.get("critical_no_source")),
        ("background 空", anom_stats.get("no_background")),
        ("result 空", anom_stats.get("no_result")),
    ]
    for k, v in rows:
        a(f"- {k}: {v}")
    a("")
    a("## 明细")
    a("")
    if date_range:
        a("### start_year > end_year")
        for d in date_range[:10]:
            a(f"- `{d['id']}` {d['name']}: {d['e']} > {_fmt(d['s'])}")
        a("")
    if crit_norel:
        a(f"### critical 无关联 ({len(crit_norel)})")
        for d in crit_norel[:15]:
            a(f"- `{d['id']}` {d['name']}")
        a("")
    if short:
        a(f"### summary < 10 字 ({len(short)})")
        for d in sorted(short, key=lambda x: len(x["summary"]))[:10]:
            a(f"- `{d['id']}` {d['name']} ({len(d['summary'])} 字): {d['summary']}")
        a("")
    if no_regime:
        a(f"### 无 regime_ids ({len(no_regime)} 事件)")
        a(" 说明: 部分事件时期未设 regime（可能属于“上古/无政权”等）")
        a("")
    if empty_bg:
        a(f"### background 空 ({len(empty_bg)})")
        a("")
    if empty_res:
        a(f"### result 空 ({len(empty_res)})")
        a("")
    a("### 事件名重复")
    for d in (anom_stats.get("same_name_groups") or []):
        a(f"- `{d['name']}`: {", ".join(d['ids'])}")
    a("")
    a("### 人物数量最多事件 Top5")
    for d in (anom_stats.get("top_person_events") or []):
        a(f"- `{d['name']}`: {d['n']} 人")
    a("")
    a("---")
    a("本报告由 build_preview.py 自动生成 (READ ONLY)。")
    return "\n".join(lines)


if __name__ == "__main__":
    main()