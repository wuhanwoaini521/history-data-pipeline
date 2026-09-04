# -*- coding: utf-8 -*-
"""V2.1.1 · Critical Person Knowledge Gap Recovery — Finalize。

把 34 条 not_found 的再解析结果『追加式』落盘（不触碰 V2.1 已 accepted 的 110 条链接）：
  - resolved_existing（4） → 追加既有 KB 链接（person_id 已在 knowledge store）
  - supplemental（28）     → 追加 curated-person-* 链接（24 位唯一 Person）
  - ambiguous（2 条：刘玄、朱德）→ 只更新 review/unlinked 注明，不创建人物
产出：
  - data/curated/history_backbone/event_person/<eid>.yml  （新链接 32 条，7 个新 store 文件 + 13 个追加）
  - data/candidates/event_person/<eid>.yml               （append：accepted 新增 inner list）
  - data/reviews/{pending,accepted}/event_person/<eid>.review.json
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from pathlib import Path
import sys
_SRC = Path(__file__).resolve().parents[1]
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))


def _pkg(mod: str):
    import importlib
    m = importlib.import_module(f"src.history_data_pipeline.{mod}")
    return m


G = _pkg("v211_gap")
R = _pkg("v211_roles")

ROOT = G.ROOT
STORE_DIR = ROOT / "data" / "curated" / "history_backbone" / "event_person"
CAND_DIR = ROOT / "data" / "candidates" / "event_person"
PEND_DIR = ROOT / "data" / "reviews" / "pending" / "event_person"
ACC_DIR = ROOT / "data" / "reviews" / "accepted" / "event_person"
STORE_HEADER = "# China History Backbone V2.1.1 · Accepted EventPerson (append layer; V1 events/ frozen)\n"


def _block(eid: str, idx: int, name: str) -> dict[str, Any]:
    role, side = R.ROLE_ROWS[idx]
    role_zh = R.role_zh_for(idx)
    v = G.resolve_verdict(eid, name)
    kind = v["verdict"]
    if kind == "resolved_existing":
        pid, canon, res = v["person_id"], v["canonical"], v["resolution"]
        confidence = 1.0
        evi = f"V2.1.1 再核实 hit 既有 KB（person_id={pid}）：{v.get('note','')}"
    else:  # supplemental
        pid = v["person_id"]
        canon = G.PERSON_SPECS[pid]["canonical_name_zh_cn"]
        res = "exact"
        confidence = 0.9
        evi = f"V2.1.1 补充 Person（{pid}），curated layer，来源={G.SUPP_SOURCE_ID}"
    return {
        "person_id": pid,
        "person_name_raw": name,
        "canonical_name": canon,
        "role": role,
        "role_zh_cn": role_zh,
        "side": side,
        "importance": "major",
        "link_status": "linked",
        "link_quality_status": "reviewed",
        "link_confidence": confidence,
        "resolution": res,
        "identity_evidence": evi,
        "event_evidence": f"{name}（{role_zh}）为该事件核心参与者（依据事件 summary/source_reference 及标准史实）",
        "review_note": f"V2.1.1 review：{res}（{kind}）；reviewed_by={G.REVIEWED_BY}",
    }


def _build_new() -> dict[str, list[dict[str, Any]]]:
    out: dict[str, list[dict[str, Any]]] = {}
    order = {}
    for k, v_ in G.SUPPLEMENT_IDS.items():
        order[k[0]] = True
    for k, v_ in G.RESOLVED_EXISTING.items():
        order[k[0]] = True
    for i, (eid, name) in enumerate(G.FROZEN_SCOPE):
        v = G.resolve_verdict(eid, name)
        if v["verdict"] == "ambiguous":
            continue
        out.setdefault(eid, []).append(_block(eid, i, name))
    return out


def _main() -> None:
    for d in (STORE_DIR, CAND_DIR, PEND_DIR, ACC_DIR):
        d.mkdir(parents=True, exist_ok=True)

    new = _build_new()
    n_links = 0
    new_files = 0
    scope_ids = sorted({e for e, _ in G.FROZEN_SCOPE})
    for eid in scope_ids:
        blocks = new.get(eid, [])
        n_links += len(blocks)
        fp = STORE_DIR / f"{eid}.yml"
        if blocks:
            if not fp.exists():
                new_files += 1
            if not fp.exists():
                doc = {"event_id": eid, "people": blocks}
            else:
                doc = yaml.safe_load(fp.read_text(encoding="utf-8")) or {"event_id": eid}
                people = list(doc.get("people", []))
                seen = {p["person_id"] for p in people}
                for b in blocks:
                    if b["person_id"] not in seen:
                        people.append(b)
                        seen.add(b["person_id"])
                doc["people"] = people
            fp.write_text(STORE_HEADER + yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, width=120),
                          encoding="utf-8")

        # ---- candidate: 保留 v2.1 内容，幂等合并（按 person_id 去重，重跑不重复）----
        cand_fp = CAND_DIR / f"{eid}.yml"
        cand = yaml.safe_load(cand_fp.read_text(encoding="utf-8")) if cand_fp.exists() else {
            "event_id": eid, "accepted": [], "unlinked": []}
        cand.setdefault("accepted", [])
        cand.setdefault("unlinked", [])
        grouped: dict[str, dict] = {}
        null_groups: list[dict] = []
        for block in cand["accepted"]:
            for g in block:
                pid = g.get("person_id")
                if pid:
                    grouped.setdefault(pid, g)
                else:
                    null_groups.append(g)
        for b in blocks:
            grouped.setdefault(b["person_id"], b)
        new_accepted = [[g] for g in grouped.values()] + [[g] for g in null_groups]
        cand["accepted"] = new_accepted
        # unlinked：先前 not_found 的，若本次已判 resolved/supplemental 则改为“已转链”，ambiguous 保留
        out_u = []
        for u in cand["unlinked"]:
            raw = u.get("person_name_raw")
            key = (eid, raw)
            # 用 FROZEN_SCOPE 精确判断
            if key in list(G.FROZEN_SCOPE):
                vv = G.resolve_verdict(*key)
                if vv["verdict"] == "ambiguous":
                    u = dict(u, resolution="ambiguous",
                             reason="V2.1.1 : 同名多项，无法唯一确认，保留 gap（不建 Person）")
                    out_u.append(u)
                    continue
                out_u.append({
                    "person_name_raw": raw, "resolution": "linked_in_v211",
                    "reason": f"V2.1.1 已转链：person_id={vv.get('person_id')}",
                })
                continue
            out_u.append(u)
        cand["unlinked"] = out_u
        cand_fp.write_text(yaml.safe_dump(cand, allow_unicode=True, sort_keys=False, width=120),
                           encoding="utf-8")

        # ---- 签名 review（append-only）----
        add = [{
            "person_id": b["person_id"], "person_name_raw": b["person_name_raw"],
            "role": b["role"], "resolution": b["resolution"],
        } for b in blocks]
        # accepted
        acc_fp = ACC_DIR / f"{eid}.review.json"
        if acc_fp.exists():
            acc = json.loads(acc_fp.read_text(encoding="utf-8"))
            acc["accepted_links"] = list(acc.get("accepted_links", []))
        else:
            acc = {"schema_version": 1, "event_id": eid, "review_status": "accepted",
                   "reviewed_by": G.REVIEWED_BY, "accepted_links": []}
        # 去重（person_id+raw）
        have = {(x.get("person_id"), x.get("person_name_raw")) for x in acc["accepted_links"]}
        for a in add:
            if (a["person_id"], a["person_name_raw"]) not in have:
                acc["accepted_links"].append(a)
                have.add((a["person_id"], a["person_name_raw"]))
        # 更新 null unlinked：ambiguous 两条 -> 显式 null 记录
        for (aeid, aname) in [k for k in G.AMBIGUOUS_GAPS if k[0] == eid]:
            hit = next((x for x in acc["accepted_links"]
                        if x.get("person_name_raw") == aname and x.get("person_id") is None), None)
            if hit is None:
                acc["accepted_links"].append({
                    "person_id": None, "person_name_raw": aname, "role": None,
                    "resolution": "ambiguous",
                    "reason": "V2.1.1 确认同名冲突/无法唯一 → 不建 Person，保留 gap",
                })
            else:
                hit["resolution"] = "ambiguous"
                hit["reason"] = "V2.1.1 确认同名冲突/无法唯一 → 不建 Person，保留 gap"
        acc_fp.write_text(json.dumps(acc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        # pending
        pend = {"event_id": eid, "review_status": "accepted",
                "candidates_count": len(blocks),
                "review": "V2.1.1 re-resolution final（append to V2.1 store）"}
        (PEND_DIR / f"{eid}.review.json").write_text(
            json.dumps(pend, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    store_total = sum(
        len(yaml.safe_load(f.read_text(encoding="utf-8")).get("people", []))
        for f in STORE_DIR.glob("*.yml")
    )
    print(f"V2.1.1 changed links: {n_links} | new store files: {new_files}")
    print(f"store files: {len(list(STORE_DIR.glob('*.yml')))} | store persons total: {store_total}")


if __name__ == "__main__":
    _main()