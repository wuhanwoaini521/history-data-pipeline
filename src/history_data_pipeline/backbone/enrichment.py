"""Autonomous enrichment + QA runner (bootstrap).

Implements the run documented in docs/QUALITY_GATES.md:

    Validate -> Score -> Accept/Quarantine -> Sample Audit -> Report

It *extends* the existing repository gates:

* ``backbone/validate.py`` — deterministic structural / FK / schema gate
  (reused verbatim; its error list feeds the hard-failure signal).
* ``backbone/quality.py`` — new 100-point scoring engine.
* ``reports/current-run/*`` — new per-run output (summary.md, quarantine.jsonl,
  audit-report.md, metrics.json).

Invariants (AGENTS.md §7 §19):

* never writes into ``data/curated/history_backbone/`` (curation stays human);
* never fabricates a datapoint: temporal checks only fire when the window is
  *known*; unknown -> skipped, never invented;
* candidate records never enter canonical data directly — they are either
  quarantined or placed in the audit queue for the human gate.
"""

from __future__ import annotations

import json
import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Iterator

from .quality import (
    VERDICT_AUTO_ACCEPT,
    VERDICT_QUARANTINE_HARD,
    VERDICT_QUARANTINE_LOW,
    VERDICT_QUARANTINE_MEDIUM,
    score_event,
)

# ---------------------------------------------------------------------------
# Report output structure (docs/QUALITY_GATES.md §6)
# ---------------------------------------------------------------------------

DEFAULT_REPORT_DIR = "reports/current-run"

REPORT_FILES = ("summary.md", "quarantine.jsonl", "audit-report.md", "metrics.json")

VERDICTS = (
    VERDICT_AUTO_ACCEPT,
    VERDICT_QUARANTINE_MEDIUM,
    VERDICT_QUARANTINE_LOW,
    VERDICT_QUARANTINE_HARD,
)

# +-1 年容差，与 tests/test_v21_person_linking.py 的历史规则一致
TOLERANCE_YEARS = 1


def parse_year(value: Any) -> int | None:
    """Deterministic year coercion; None when not a number (no guessing)."""
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        try:
            return int(value)
        except (TypeError, ValueError):
            return None
    try:
        return int(str(value).strip().rstrip("s"))
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------------------
# Knowledge inventory (temporal-gate inputs)
# ---------------------------------------------------------------------------


@dataclass
class TemporalInventory:
    """Known person lifespans and place validity windows (unknown stays None)."""

    persons: dict[str, tuple[int | None, int | None]] = field(default_factory=dict)
    places: dict[str, tuple[int | None, int | None]] = field(default_factory=dict)

    @classmethod
    def from_curated_and_db(
        cls,
        root: Path | str,
        knowledge_db: Path | str | None = None,
    ) -> TemporalInventory:
        root = Path(root)
        inv = cls()

        # curated persons (v2.1.1 knowledge-gap files)
        persons_dir = root / "data" / "curated" / "persons"
        if persons_dir.is_dir():
            import yaml

            for file in sorted(persons_dir.glob("*.yml")):
                try:
                    data = yaml.safe_load(file.read_text(encoding="utf-8"))
                except Exception:
                    data = None
                if isinstance(data, dict) and data.get("id"):
                    inv.persons[data["id"]] = (
                        parse_year(data.get("birth_year")),
                        parse_year(data.get("death_year")),
                    )

        # knowledge database (people / places tables) when available
        database = (
            Path(knowledge_db) if knowledge_db else root / "dist" / "history.duckdb"
        )
        if not database.exists():
            return inv
        try:
            import duckdb
        except ImportError:
            return inv
        try:
            with duckdb.connect(str(database), read_only=True) as con:
                for pid, b, d in con.execute(
                    "SELECT id, birth_year, death_year FROM people"
                ).fetchall():
                    known = inv.persons.get(pid)
                    if known and (known[0] is not None or known[1] is not None):
                        b = known[0] if known[0] is not None else parse_year(b)
                        d = known[1] if known[1] is not None else parse_year(d)
                    else:
                        b, d = parse_year(b), parse_year(d)
                    inv.persons[pid] = (b, d)
                for pid, vf, vt in con.execute(
                    "SELECT id, valid_from, valid_to FROM places"
                ).fetchall():
                    inv.places[pid] = (parse_year(vf), parse_year(vt))
        except Exception:
            pass
        return inv


# ---------------------------------------------------------------------------
# Temporal consistency rules (G2) — only fire when the window is known
# ---------------------------------------------------------------------------


def check_event_person_temporal(
    event: dict[str, Any],
    inventory: TemporalInventory,
) -> list[str]:
    """Event vs person lifespan: birth after event end (beyond tolerance) or
    death before event start is a hard conflict (AGENTS.md §8/§13)."""
    errors: list[str] = []
    start = parse_year(event.get("start_year"))
    end = parse_year(event.get("end_year")) or start
    if start is None:
        return errors
    event_id = event.get("id", "?")
    for person in event.get("people", []):
        person_id = person.get("person_id")
        if not person_id or person_id not in inventory.persons:
            continue
        birth, death = inventory.persons[person_id]
        label = person.get("person_name_raw") or person_id
        if birth is not None and end + TOLERANCE_YEARS < birth:
            errors.append(
                f"events/{event_id}: person {label}({person_id}) born {birth} after event end {end}"
            )
        if death is not None and start - TOLERANCE_YEARS > death:
            errors.append(
                f"events/{event_id}: person {label}({person_id}) died {death} before event start {start}"
            )
    return errors


def check_event_place_temporal(
    event: dict[str, Any],
    inventory: TemporalInventory,
) -> list[str]:
    """Event vs place validity window (only when valid_from/valid_to known)."""
    errors: list[str] = []
    start = parse_year(event.get("start_year"))
    end = parse_year(event.get("end_year")) or start
    if start is None:
        return errors
    event_id = event.get("id", "?")
    for place in event.get("places", []):
        place_id = place.get("place_id")
        if not place_id or place_id not in inventory.places:
            continue
        valid_from, valid_to = inventory.places[place_id]
        label = place.get("place_name_raw") or place_id
        if valid_to is not None and start - TOLERANCE_YEARS > valid_to:
            errors.append(
                f"events/{event_id}: place {label}({place_id}) valid to {valid_to} before event start {start}"
            )
        if valid_from is not None and end + TOLERANCE_YEARS < valid_from:
            errors.append(
                f"events/{event_id}: place {label}({place_id}) valid from {valid_from} after event end {end}"
            )
    return errors


def check_curated_person_lifespans(inventory: TemporalInventory) -> list[str]:
    """birth > death is an impossible lifespan -> hard error (invariant)."""
    return [
        f"persons/{pid}: birth {b} > death {d}"
        for pid, (b, d) in inventory.persons.items()
        if b is not None and d is not None and b > d
    ]


def temporal_conflicts_for_event(
    event: dict[str, Any],
    inventory: TemporalInventory,
) -> list[tuple[str, str]]:
    """(event_id, detail) pairs the scoring engine uses to flag impossible_chronology."""
    return [
        (str(event.get("id", "?")), detail)
        for detail in check_event_person_temporal(event, inventory)
        + check_event_place_temporal(event, inventory)
    ]


# ---------------------------------------------------------------------------
# Candidate intake
# ---------------------------------------------------------------------------


def iter_candidate_documents(
    candidate_dir: str | Path,
) -> Iterator[tuple[str, dict[str, Any]]]:
    """Yield (source_path, event_dict) from a candidate directory.

    Supports the container shapes used by the repo's existing candidate files:
    * ``candidates: [...]``   (backbone-candidates-v1)
    * ``events: [...]``
    * a bare event dict at the top level.
    Unparseable files yield an event with ``_error`` so the caller can
    quarantine them.
    """
    path = Path(candidate_dir)
    if not path.is_dir():
        return
    import yaml

    for file in sorted(path.rglob("*.yml")) + sorted(path.rglob("*.yaml")):
        try:
            data = yaml.safe_load(file.read_text(encoding="utf-8"))
        except Exception as exc:
            yield (
                str(file),
                {"id": "", "name_zh_cn": "", "_error": f"yaml parse: {exc}"},
            )
            continue
        if not isinstance(data, dict):
            yield (
                str(file),
                {"id": "", "name_zh_cn": "", "_error": "top-level is not a dict"},
            )
            continue
        for key in ("candidates", "events"):
            items = data.get(key)
            if isinstance(items, list):
                for item in items:
                    if isinstance(item, dict):
                        item.setdefault("_source", str(file))
                        item.setdefault("_list", key)
                        yield str(file), item
                break
        else:
            data.setdefault("_source", str(file))
            yield str(file), data


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------


def score_events(
    events: Iterable[dict[str, Any]],
    inventory: TemporalInventory,
) -> list[dict[str, Any]]:
    """Score each event document, injecting the temporal-error signal."""
    person_years = {
        pid: (b, d)
        for pid, (b, d) in inventory.persons.items()
        if b is not None or d is not None
    }
    return [
        score_event(
            event,
            person_years=person_years,
            place_windows=dict(inventory.places),
            temporal_conflicts=temporal_conflicts_for_event(event, inventory),
        )
        for event in events
    ]


# ---------------------------------------------------------------------------
# Report writer helpers
# ---------------------------------------------------------------------------


def _wjsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False, default=str) + "\n")


def _wmarkdown(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _wjson(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(obj, ensure_ascii=False, indent=2, default=str) + "\n",
        encoding="utf-8",
    )


def _histogram(values: list[float]) -> dict[str, int]:
    buckets = {"90-100": 0, "75-89": 0, "0-74": 0}
    for v in values:
        if v >= 90.0:
            buckets["90-100"] += 1
        elif v >= 75.0:
            buckets["75-89"] += 1
        else:
            buckets["0-74"] += 1
    return buckets


def _evidence_head(event: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "work": ev.get("work"),
            "term": ev.get("term"),
            "evidence_role": ev.get("evidence_role"),
            "link_status": ev.get("link_status"),
            "historical_text_id": ev.get("historical_text_id"),
        }
        for ev in event.get("evidence", [])
    ][:5]


def _quarantine_row(
    event: dict[str, Any], scored: dict[str, Any], source: str
) -> dict[str, Any]:
    reasons = scored.get("reasons") or []
    return {
        "id": event.get("id"),
        "name_zh_cn": event.get("name_zh_cn") or event.get("name"),
        "source": source,
        "kind": "event",
        "verdict": scored.get("verdict"),
        "score": scored.get("score"),
        "hard_failures": scored.get("hard_failures") or [],
        "reasons": reasons[:8],
        "evidence_head": _evidence_head(event),
        "source_reference": event.get("source_reference"),
        "source_ids": event.get("source_ids"),
        "importance": event.get("importance"),
        "quality_status": event.get("quality_status"),
        "recommended_action": _recommended_action(scored, source),
    }


def _recommended_action(scored: dict[str, Any], source: str) -> str:
    hard = scored.get("hard_failures") or []
    if source != "candidate":
        return "canonical 记录命中硬失败 → 需人工复核后修正"
    if scored["verdict"] == VERDICT_AUTO_ACCEPT:
        return "已达标；转人工 review 队列后进 canonical"
    if any("impossible_chronology" in h for h in hard):
        return "修复日期/身份时序冲突后重跑"
    return "补充证据/来源、消解 identity 后重新评审"


def _write_summary(
    report_dir: Path,
    metrics: dict[str, Any],
    quarantine_rows: list[dict[str, Any]],
) -> str:
    vc = metrics["verdict_counts"]
    hist = metrics["score"]["histogram"]
    errors = metrics["validation"].get("errors") or []
    md = [
        "# Enrichment / QA Run Summary",
        "",
        f"- report_dir: `{report_dir}`",
        "",
        "## 判定计数",
        "",
        "| verdict | count |",
        "| --- | --- |",
        *[f"| {v} | {vc.get(v, 0)} |" for v in VERDICTS],
        "",
        "## 分数分布",
        *[f"- `{bucket}`: {n}" for bucket, n in hist.items()],
        f"- mean: {metrics['score']['mean']}",
        "",
        f"## 校验错误（{len(errors)}）",
        *[f"- `{err}`" for err in errors[:40]],
        "",
        f"## 隔离：{len(quarantine_rows)} → `quarantine.jsonl`",
        f"## 审计采样：{metrics['counts']['audited']} → `audit-report.md`",
        "",
        "> 由 `history-data backbone qa-run` 生成（确定性 seed，可复现）。",
    ]
    return "\n".join(md)


def _audit_markdown(audit_rows: list[dict[str, Any]], seed: int | None) -> str:
    md = [
        "# Sampled Independent Audit (G5)",
        "",
        f"- seed = {seed}",
        f"- sample size = {len(audit_rows)}",
        "",
        "| event_id | name_zh_cn | status | checks |",
        "| --- | --- | --- | --- |",
        *[
            f"| {r['event_id']} | {r['name_zh_cn']} | {r['status']} | {', '.join(r['checks'])} |"
            for r in audit_rows
        ],
        "",
        "> This file fixes the audit queue; an independent Verifier/Auditor fills in findings.",
    ]
    return "\n".join(md)


def _sample_audit(
    candidates_accepted: list[dict[str, Any]],
    canonical_accepted: list[dict[str, Any]],
    sample_size: int,
    seed: int | None,
) -> list[dict[str, Any]]:
    """Deterministic independent-audit sample (G5) from accepted records."""
    pool = [e for e in candidates_accepted if e.get("id")]
    pool.extend(canonical_accepted)
    if sample_size <= 0 or not pool:
        return []
    rng = random.Random(seed)
    picked = rng.sample(pool, min(sample_size, len(pool)))
    return [
        {
            "event_id": e.get("id"),
            "name_zh_cn": e.get("name_zh_cn"),
            "status": "needs_independent_audit",
            "checks": [
                "source_quality",
                "identity_resolution",
                "date_accuracy",
                "place_window",
                "evidence_chain",
            ],
        }
        for e in picked
    ]


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------


@dataclass
class EnrichmentReport:
    """Container returned by :func:`build_report`."""

    metrics: dict[str, Any]
    report_dir: Path
    files: dict[str, Path] = field(init=False)

    def __post_init__(self) -> None:
        self.files = {name: self.report_dir / name for name in REPORT_FILES}

    def report_files(self) -> dict[str, str]:
        return {k: str(v) for k, v in self.files.items()}


def build_report(
    root: str | Path,
    *,
    report_dir: str | Path = DEFAULT_REPORT_DIR,
    candidate_dir: str | Path | None = None,
    knowledge_db: str | Path | None = None,
    sample_size: int = 3,
    seed: int | None = 1,
) -> EnrichmentReport:
    """Run the full Enrichment/QA pipeline and write reports.

    Steps (docs/QUALITY_GATES.md §§2-6):

    1. load curated backbone
    2. deterministic validation: existing ``validate_backbone`` + new temporal
       rules (event/person, event/place, curated person lifespan)
    3. 100-point score every curated event and every candidate
    4. quarantine: hard failures of canonical events; any candidate not
       AUTO_ACCEPT (or unparsable) → ``quarantine.jsonl``
    5. sampled audit (deterministic seed) → ``audit-report.md``
    6. write ``summary.md`` + ``metrics.json``

    Never mutates ``data/curated``.
    """
    from .loader import load_backbone
    from .validate import validate_backbone

    root_path = Path(root)
    report_path = Path(report_dir)
    report_path.mkdir(parents=True, exist_ok=True)

    backbone = load_backbone(root_path)
    inventory = TemporalInventory.from_curated_and_db(root_path, knowledge_db)

    # ---- candidates ----
    candidates = (
        [doc for _, doc in iter_candidate_documents(candidate_dir)]
        if candidate_dir
        else []
    )
    if candidate_dir is not None and not Path(candidate_dir).is_dir():
        candidates.append({"_error": f"candidate_dir not found: {candidate_dir}"})

    # ---- 2. deterministic validation ----
    errors: list[str] = list(validate_backbone(backbone, root_path))
    errors.extend(check_curated_person_lifespans(inventory))
    for event in backbone.events:
        errors.extend(check_event_person_temporal(event, inventory))
        errors.extend(check_event_place_temporal(event, inventory))
    for doc in candidates:
        errors.extend(check_event_person_temporal(doc, inventory))
        errors.extend(check_event_place_temporal(doc, inventory))

    # ---- 3. scoring ----
    canonical_scores = score_events(backbone.events, inventory)
    candidate_scores = score_events(candidates, inventory)

    # ---- 4. quarantine / accept ----
    quarantine_rows: list[dict[str, Any]] = []
    canonical_accepted: list[dict[str, Any]] = []
    candidate_accepted: list[dict[str, Any]] = []

    for event, score in zip(backbone.events, canonical_scores):
        if score["verdict"] == VERDICT_AUTO_ACCEPT and not score["hard_failures"]:
            canonical_accepted.append(event)
        elif score["hard_failures"]:
            # canonical 硬失败（确定性完整性）→ 隔离
            quarantine_rows.append(_quarantine_row(event, score, "curated"))
        # 其余 canonical（无硬失败、分数低于阈值）仅计入统计，不隔离

    for doc, score in zip(candidates, candidate_scores):
        if "_error" in doc:
            quarantine_rows.append(
                {
                    "id": str(doc.get("id") or doc.get("_source", "?")),
                    "name_zh_cn": "",
                    "source": "candidate",
                    "kind": "event",
                    "verdict": VERDICT_QUARANTINE_HARD,
                    "score": 0.0,
                    "hard_failures": ["schema_problem"],
                    "reasons": [doc["_error"]],
                    "recommended_action": "修复候选 YAML 后重跑",
                }
            )
            continue
        if score["verdict"] == VERDICT_AUTO_ACCEPT and not score["hard_failures"]:
            candidate_accepted.append(doc)
        else:
            quarantine_rows.append(_quarantine_row(doc, score, "candidate"))

    # ---- 5. sampled audit ----
    # AGENTS.md §18: 抽样对象为「已接受记录」。canonical 事件全部已过 review（accepted），
    # 加 AUTO_ACCEPT 候选；不信造、只确定性定队列，由人/独立 Verifier 填充结论。
    audit_rows = _sample_audit(
        candidate_accepted, list(backbone.events), sample_size, seed
    )

    # ---- 6. verdict counts + scores ----
    verdict_counts: dict[str, int] = {}
    all_scores = canonical_scores + candidate_scores
    for score in all_scores:
        v = score["verdict"]
        verdict_counts[v] = verdict_counts.get(v, 0) + 1
    # _error 候选在隔离行里，补记 Hard
    if any("_error" in d for d in candidates):
        verdict_counts[VERDICT_QUARANTINE_HARD] = verdict_counts.get(
            VERDICT_QUARANTINE_HARD, 0
        ) + sum(1 for d in candidates if "_error" in d)

    values = [s["score"] for s in all_scores if s["score"] is not None]
    metrics: dict[str, Any] = {
        "report": "autonomous-enrichment-run",
        "report_dir": str(report_path),
        "root": str(root_path),
        "seed": seed,
        "counts": {
            "backbone_events": len(backbone.events),
            "candidates": len(candidates),
            "accepted": len(canonical_accepted) + len(candidate_accepted),
            "quarantined": len(quarantine_rows),
            "audited": len(audit_rows),
        },
        "verdict_counts": verdict_counts,
        "score": {
            "mean": round(sum(values) / len(values), 1) if values else None,
            "min": min(values) if values else None,
            "max": max(values) if values else None,
            "histogram": _histogram(values),
        },
        "validation": {"error_count": len(errors), "errors": errors},
        "audit": audit_rows,
    }

    # ---- write artifacts ----
    _wmarkdown(
        report_path / "summary.md",
        _write_summary(report_path, metrics, quarantine_rows),
    )
    _wjsonl(report_path / "quarantine.jsonl", quarantine_rows)
    _wmarkdown(report_path / "audit-report.md", _audit_markdown(audit_rows, seed))
    _wjson(report_path / "metrics.json", metrics)
    return EnrichmentReport(metrics=metrics, report_dir=report_path)


__all__ = [
    "DEFAULT_REPORT_DIR",
    "REPORT_FILES",
    "TemporalInventory",
    "parse_year",
    "check_event_person_temporal",
    "check_event_place_temporal",
    "check_curated_person_lifespans",
    "temporal_conflicts_for_event",
    "iter_candidate_documents",
    "score_events",
    "build_report",
    "EnrichmentReport",
]
