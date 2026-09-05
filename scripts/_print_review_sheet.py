# -*- coding: utf-8 -*-
"""Print compact review sheet: id | rel | desc for the 62 backward relations."""
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

rows = json.load(open("scripts/_backward_62.json", encoding="utf-8"))
for i, r in enumerate(rows, 1):
    d = r.get("relation_desc") or "-"
    s = r["src"].replace("event-", "")
    t = r["tgt"].replace("event-", "")
    gap = r["tgt_start"] - r["src_end"]
    print(f"{i:02d} {r['rel']:8s} gap={gap:+4d} | {r['src_name']}({r['src_start']}) -> {r['tgt_name']}({r['tgt_start']}..{r['tgt_end']})")
    print(f"   ids: {s} -> {t}")
    print(f"   desc: {d}")
