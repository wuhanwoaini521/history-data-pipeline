# -*- coding: utf-8 -*-
"""Phase 2: classify the 62 backward EventRelations for agent-assisted semantic review.

Read-only. Input: scripts/_backward_62.json (Phase-1 snapshot).

Categories:
  A  overlap      : src_start <= tgt_start (target begins INSIDE the source lifespan)
                    -> "parallel / same-era" edges, mostly benign
  B  full-reverse : tgt_start < src_start (target starts BEFORE the source itself)
                    -> strong backward pointing, needs semantic judgment

Gap = tgt_start - src_end (always negative here). |gap| is how far the target
begins before the source ends.
"""
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

rows = json.load(open("scripts/_backward_62.json", encoding="utf-8"))
assert len(rows) == 62

for r in rows:
    r["gap"] = r["tgt_start"] - r["src_end"]          # negative
    r["same_range"] = r["src_start"] <= r["tgt_start"]
    r["span_overlap"] = (not r["same_range"]) and (
        r["tgt_start"] >= r["src_start"] or True
    )
    # bucket by |gap|
    g = -r["gap"]
    if g <= 2:
        r["bucket"] = "p1  |gap|<=2 (year precision)"
    elif g <= 10:
        r["bucket"] = "p2  |gap|<=10"
    elif g <= 50:
        r["bucket"] = "p3  |gap|<=50"
    else:
        r["bucket"] = "p4  |gap|>50"

cat_a = [r for r in rows if r["same_range"]]
cat_b = [r for r in rows if not r["same_range"]]
print(f"A overlap (tgt starts inside src lifespan) : {len(cat_a)}")
print(f"B full-reverse (tgt starts before src start): {len(cat_b)}")
print()

def line(r):
    conf = f"{r['confidence']:.2f}" if r["confidence"] is not None else "  --"
    return (
        f"[{r['bucket'][:2]}] gap={r['gap']:+5d} conf={conf} {r['rel']:8s} "
        f"{r['src']}({r['src_start']}..{r['src_end']},{r['src_period']}) -> "
        f"{r['tgt']}({r['tgt_start']}..{r['tgt_end']},{r['tgt_period']})"
    )

print("== A. overlap ==")
for r in cat_a:
    print(line(r))
print()
print("== B. full-reverse ==")
for r in cat_b:
    print(line(r))
print()
print("== bucket distribution ==")
from collections import Counter
for b, n in sorted(Counter(r["bucket"] for r in rows).items()):
    print(f"{b}: {n}")
print()
print("== cross-period subset ==")
for r in rows:
    if r["src_period"] != r["tgt_period"]:
        print(line(r))
