"""Q18 — Final Dist Validation（只读 + 确定性构建检查）。

检查：dangling evidence/relations、duplicate ID、duplicate place、
      event_text mismatch、invalid claim_field、fuzzy linked。
用法：python scripts/phase_final_dist_check.py [--determinism]
      --determinism 会连续 build 两次并对比各表计数（需要知识库）。
"""
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist" / "history.duckdb"
OUT = ROOT / "reports" / "current-run" / "phase-wrapup-18-dist-check.json"

VALID_FIELDS = {"background", "process", "result", "impact", "people", "places"}
TABLES = ["events", "event_evidence", "event_place", "event_relations", "event_person",
          "historical_texts", "people", "places", "stories", "story_events", "periods", "regimes"]


def counts(con):
    return {t: con.execute(f"select count(*) from {t}").fetchone()[0] for t in TABLES}


def check():
    con = duckdb.connect(str(DIST), read_only=True)
    res = {}
    # dangling evidence
    res["dangling_evidence"] = con.execute("""
        select count(*) from event_evidence ev
        left join events e on e.id = ev.event_id
        where e.id is null
    """).fetchone()[0]
    res["dangling_evidence_text"] = con.execute("""
        select count(*) from event_evidence ev
        where ev.historical_text_id is not null
          and ev.historical_text_id not in (select id from historical_texts)
    """).fetchone()[0]
    # dangling relations
    res["dangling_relations"] = con.execute("""
        select count(*) from event_relations r
        left join events s on s.id = r.source_event_id
        left join events t on t.id = r.target_event_id
        where s.id is null or t.id is null
    """).fetchone()[0]
    # duplicate ids
    res["duplicate_event_ids"] = con.execute("""
        select count(*) from (select id from events group by id having count(*) > 1)
    """).fetchone()[0]
    # duplicate place name within event
    res["duplicate_event_place"] = con.execute("""
        select count(*) from (
          select event_id, place_name_raw from event_place
          group by 1, 2 having count(*) > 1
        )
    """).fetchone()[0]
    # invalid claim_field
    res["invalid_claim_field"] = con.execute("""
        select count(*) from event_evidence
        where claim_field is not null and claim_field not in ('background','process','result','impact','people','places')
    """).fetchone()[0]
    # fuzzy linked
    res["fuzzy_linked"] = con.execute("""
        select count(*) from event_evidence where link_method = 'fuzzy' and link_status = 'linked'
    """).fetchone()[0]
    # event_text mismatch (event_text 指向不存在文本)
    res["event_text_mismatch"] = con.execute("""
        select count(*) from event_text et
        where et.historical_text_id not in (select id from historical_texts)
    """).fetchone()[0]
    # self relations
    res["self_relations"] = con.execute("""
        select count(*) from event_relations where source_event_id = target_event_id
    """).fetchone()[0]
    con.close()
    res["counts"] = counts(duckdb.connect(str(DIST), read_only=True))
    return res


def main() -> int:
    res = check()
    if "--determinism" in sys.argv:
        py = sys.executable
        env = {"PYTHONPATH": "src", "PATH": "/usr/bin:/bin"}
        import os
        e = dict(os.environ)
        e.update(env)
        cmds = [[py, "-m", "history_data_pipeline.cli", "backbone", "--knowledge",
                 "data/normalized/history.duckdb", "build"] for _ in range(2)]
        first = second = None
        for i, c in enumerate(cmds):
            subprocess.run(c, cwd=str(ROOT), env=e, capture_output=True)
            cnt = counts(duckdb.connect(str(DIST), read_only=True))
            if i == 0:
                first = cnt
            else:
                second = cnt
        res["determinism"] = {"build_1": first, "build_2": second,
                              "identical": first == second}
    OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(res, ensure_ascii=False, indent=1))
    bad = [k for k, v in res.items() if isinstance(v, int) and v != 0]
    print("NON-ZERO:", bad if bad else "none")
    return 0


if __name__ == "__main__":
    sys.exit(main())
