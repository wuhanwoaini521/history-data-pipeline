# -*- coding: utf-8 -*-
"""V2.1.1 · personas ：由 v021_persons 规格批量写入 data/curated/persons/*.yml（一次性生成，可重跑幂等）。"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

_SRC = Path(__file__).resolve().parents[1]
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from history_data_pipeline.v021_persons import PERSON_SPECS

ROOT = _SRC
OUT = ROOT / "data" / "curated" / "persons"
SID = "source-curated-person-knowledge-gap"

_EXTRA = {
    "source_type": "curated_reference",
    "source_id": SID,
    "quality_status": "reviewed",
    "created_by": "agent",
    "snapshot_version": "v2.1.1",
}

_MANDATORY = {
    "id", "name_raw", "canonical_name_zh_cn", "traditional_name",
    "birth_year", "death_year", "birth_precision", "death_precision",
    "gender", "period_ids", "aliases", "intro_zh_cn", "source_reference",
}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    n = 0
    for pid, spec in sorted(PERSON_SPECS.items()):
        missing = _MANDATORY - set(spec)
        if missing:
            raise ValueError(f"{pid}: spec 缺字段 {sorted(missing)}")
        doc = {k: spec[k] for k in _MANDATORY}
        doc.update(_EXTRA)
        fp = OUT / f"{pid}.yml"
        text = (
            "# China History Backbone V2.1.1 · curated Person "
            "(critical knowledge-gap recovery; agent-reviewed)\n"
            + yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, width=120)
        )
        fp.write_text(text, encoding="utf-8")
        n += 1
    print(f"written {n} person files -> {OUT}")


if __name__ == "__main__":
    main()