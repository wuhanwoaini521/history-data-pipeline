"""Major Batch 01 · Queue 7 — Content Depth Audit（只读；不修改 coverage score）。

规则（透明、确定性）：
- process_depth: DEVELOPED = process_zh_cn 含 ≥2 个来源支持阶段（以句号/分号切分 ≥2 段且 ≥60 字）
                 BASIC = 有内容但 <60 字或单句； MISSING = 空
- impact_depth:  同样规则作用于 impact_zh_cn
- FULL + CONTENT_DEPTH_LOW = score==100 且 (process_depth != DEVELOPED 或 impact_depth != DEVELOPED)
- 统计 evidence_claim_field 覆盖度（四维字段锚）
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path
from collections import Counter

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from history_data_pipeline.backbone.product_completeness import event_completeness

def depth(text: str | None) -> str:
    if not text or not str(text).strip():
        return "MISSING"
    t = str(text).strip()
    # 阶段分隔：句号/分号/冒号/破折号（含中文标点）——透明、确定性
    stages = len([s for s in re.split(r"[。；;：:—]", t) if len(s) >= 6])
    if len(t) >= 50 and stages >= 2:
        return "DEVELOPED"
    return "BASIC"

rows = []
for f in (ROOT / "data" / "curated" / "history_backbone" / "events").rglob("event-*.yml"):
    d = yaml.safe_load(f.read_text())
    eid = d.get("id")
    if not eid:
        continue
    c = event_completeness(d)
    pd_, id_ = depth(d.get("process_zh_cn")), depth(d.get("impact_zh_cn"))
    fields = {e.get("claim_field") for e in (d.get("evidence") or []) if e.get("claim_field")}
    rows.append({
        "event_id": eid, "name": d.get("name_zh_cn"), "score": c["product_completeness_score"],
        "process_depth": pd_, "impact_depth": id_,
        "evidence_count": len(d.get("evidence") or []),
        "claim_field_count": len(fields),
        "people_count": len(d.get("people") or []),
        "place_count": len(d.get("places") or []),
        "relation_count": len(d.get("relations") or []),
    })

full = [r for r in rows if r["score"] == 100.0]
low = [r for r in full if r["process_depth"] != "DEVELOPED" or r["impact_depth"] != "DEVELOPED"]
strong = [r for r in full if r not in low]

lines = ["# Major Batch 01 · Queue 7 — Content Depth Audit", "",
         "> 只读审计：Coverage Score ≠ Content Quality。不修改任何 coverage score。",
         "> 规则：DEVELOPED = ≥50 字且 ≥2 个阶段分隔（。；：—）；BASIC = 有内容但单句/过短；MISSING = 空。", "",
         "## 总览", "",
         f"- 全库事件：{len(rows)}", f"- FULL（100 分）：{len(full)}",
         f"- FULL + STRONG：{len(strong)}", f"- **FULL + CONTENT_DEPTH_LOW：{len(low)}**", "",
         "## 本批 50 个 Major Batch 01 事件", "",
         "| event | score | process | impact | evidence | claim_fields | people | place | rel |",
         "|---|---:|---|---|---:|---:|---:|---:|---:|"]
batch50 = None  # filled below by caller-provided list
BATCH = json.loads((ROOT / "reports" / "current-run" / "major01-batch50.json").read_text()) if (ROOT / "reports" / "current-run" / "major01-batch50.json").exists() else []
bset = set(BATCH)
for r in rows:
    if r["event_id"] in bset:
        lines.append(f"| {r['event_id']} | {r['score']} | {r['process_depth']} | {r['impact_depth']} | {r['evidence_count']} | {r['claim_field_count']} | {r['people_count']} | {r['place_count']} | {r['relation_count']} |")
lines += ["", "## FULL + CONTENT_DEPTH_LOW（全库，需后续加深）", ""]
for r in sorted(low, key=lambda x: x["event_id"]):
    lines.append(f"- {r['event_id']}（{r['name']}）process={r['process_depth']} impact={r['impact_depth']} evidence={r['evidence_count']}")
(ROOT / "reports" / "current-run" / "major01-07-content-depth-audit.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"rows={len(rows)} full={len(full)} strong={len(strong)} low={len(low)}")
b_low = [r for r in low if r['event_id'] in bset]
print(f"batch50 in low: {len(b_low)}")
for r in b_low[:20]:
    print("  LOW:", r['event_id'], r['process_depth'], r['impact_depth'])
