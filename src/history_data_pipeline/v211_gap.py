# -*- coding: utf-8 -*-
"""V2.1.1 · Critical Person Knowledge Gap Recovery — 共享决策数据
（Frozen Scope 34 + 再解析裁决 + 24 位补充 Person 规格）。

纪律：只用 Knowledge Store(Layer2) 真实 ID 或本项目 curated-person-*；禁伪 CBDB ID；
禁临时 Person；不把 AI 当 data source；补充 Person 必须有来源与 provenance；
现代/民国/抗日/日本人物一律中性表述，不做价值判断。
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .v021_persons import PERSON_SPECS as _PERSON_SPECS

REVIEWED_BY = "china-history-backbone-v2.1.1-curator"
CREATED_BY = "agent"
SUPP_SOURCE_ID = "source-curated-person-knowledge-gap"


def parse_frozen_scope(root: Path) -> list[tuple[str, str]]:
    """权威来源：reports/PERSON_KNOWLEDGE_GAPS.md（V2.1 冻结的 34 条 not_found）。

    直接从报告表格解析，避免手抄引入笔误；解析失败即抛出（不许放宽）。"""
    report = root / "reports" / "PERSON_KNOWLEDGE_GAPS.md"
    rows: list[tuple[str, str]] = []
    with report.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line.startswith("| event-"):
                continue
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) < 4:
                continue
            eid, name = cells[0], cells[1]
            if eid.startswith("event-") and name:
                rows.append((eid, name))
    if len(rows) != 34:
        raise RuntimeError(f"REPORTS/PERSON_KNOWLEDGE_GAPS.md 应含 34 条，实际 {len(rows)} → 范围冻结失败")
    return rows


ROOT = Path(__file__).resolve().parents[2]
FROZEN_SCOPE: list[tuple[str, str]] = parse_frozen_scope(ROOT)

# ---------------------------------------------------------------------------
# 再解析裁决
# ---------------------------------------------------------------------------
# resolved_existing：已探库命中 Knowledge Store 既有 ID（V2.1 漏检）。
RESOLVED_EXISTING: dict[tuple[str, str], dict[str, Any]] = {
    ("event-qin-tongyi", "李斯"): {
        "person_id": "ctext-person-751995", "canonical": "李斯", "resolution": "exact",
        "note": "ctext Layer：people.canonical='李斯' 实测命中；V2.1 suffix 过滤误判 not_found。",
    },
    ("event-yangjian-dai-beizhou", "周静帝"): {
        "person_id": "ctext-person-293600", "canonical": "北周靜帝", "resolution": "exact",
        "note": "周静帝=北周静帝=宇文阐；ctext-person-293600 实测命中。",
    },
    ("event-houliang-dai-tang", "朱温"): {
        "person_id": "cbdb-person-377600", "canonical": "朱晃", "resolution": "exact",
        "note": "person_aliases：朱温→cbdb-person-377600（canonical 朱晃 852-912 后梁）；V2.1 未查 alias 表漏检。",
    },
    ("event-huangchao-qiyi", "朱温"): {
        "person_id": "cbdb-person-377600", "canonical": "朱晃", "resolution": "exact",
        "note": "同 houliang-dai-tang：alias 朱温→cbdb-person-377600。",
    },
}

# ambiguous：同名多项、无法唯一确认 → 保留 gap，不补新 Person
AMBIGUOUS_GAPS: dict[tuple[str, str], str] = {
    ("event-xin-mie", "刘玄"):
        "KB 存在多条 劉玄(CBDB)，均无『更始帝(-23~-25)』时代证据，无法唯一确认 → ambiguous，不补。",
    ("event-xinzhongguo-chengli", "朱德"):
        "KB 存在多条『朱德』先代同名记录（无现代生卒证据），无法证明与朱德元帅同一人或不同人 → 保留 gap，不建第二条 canonical。",
}

# supplemental：genuine_missing → curated-person-*
_NAME_TO_PERSON: dict[str, str] = {
    s["name_raw"]: pid for pid, s in _PERSON_SPECS.items()
}

SUPPLEMENT_IDS: dict[tuple[str, str], str] = {}


def resolve_verdict(eid: str, name: str) -> dict[str, Any]:
    key = (eid, name)
    if key in RESOLVED_EXISTING:
        return {"verdict": "resolved_existing", **RESOLVED_EXISTING[key]}
    if key in AMBIGUOUS_GAPS:
        return {"verdict": "ambiguous", "reason": AMBIGUOUS_GAPS[key]}
    pid = _NAME_TO_PERSON.get(name)
    if pid:
        return {
            "verdict": "supplemental", "person_id": pid,
            "canonical": _PERSON_SPECS[pid]["canonical_name_zh_cn"],
        }
    raise ValueError(f"scope 无裁决: {key}（不在 resolved/ambiguous/supplement 任何一类）")


# 构建 SUPPLEMENT_IDS（所有非 resolved/ambiguous 的 34 条都必须有对应补充 Person）
for _eid, _name in FROZEN_SCOPE:
    v = resolve_verdict(_eid, _name)
    if v["verdict"] == "supplemental":
        SUPPLEMENT_IDS[(_eid, _name)] = v["person_id"]

__all__ = [
    "ROOT", "FROZEN_SCOPE", "RESOLVED_EXISTING", "AMBIGUOUS_GAPS",
    "SUPPLEMENT_IDS", "resolve_verdict", "PERSON_SPECS",
    "REVIEWED_BY", "CREATED_BY", "SUPP_SOURCE_ID",
]

PERSON_SPECS = _PERSON_SPECS