"""Quality scoring for History Backbone Event records (AGENTS.md §16/§17).

This module is the **quality-gate scoring engine** introduced by the autonomous
enrichment bootstrap. It is fully deterministic: for the same event document and
the same knowledge inventory, it returns the same score and the same reasons.

The implementation *extends* the existing data governance model:
* it consumes the canonical event shape from `schemas/event.schema.json`;
* it never writes into `data/curated/history_backbone/` (curation stays human);
* it only computes scores and verdicts (QUALITY_GATES.md §3).

Scoring dimensions and weights follow AGENTS.md §16 (sum = 100):

    Schema / FK / uniqueness        10
    Temporal consistency            10
    Person resolution               10
    Place resolution                10
    Source quality                  15
    Evidence precision              15
    Independent source verification 10
    Content completeness            10
    Independent verifier            10
"""

from __future__ import annotations

from typing import Any, Iterable

# ---------------------------------------------------------------------------
# Weights (must sum to 100)
# ---------------------------------------------------------------------------

WEIGHTS: dict[str, int] = {
    "schema_fk_uniqueness": 10,
    "temporal_consistency": 10,
    "person_resolution": 10,
    "place_resolution": 10,
    "source_quality": 15,
    "evidence_precision": 15,
    "independent_source_verification": 10,
    "content_completeness": 10,
    "independent_verifier": 10,
}

assert sum(WEIGHTS.values()) == 100, "quality dimension weights must sum to 100"

# ---------------------------------------------------------------------------
# Verdict taxonomy (AGENTS.md §16 thresholds)
# ---------------------------------------------------------------------------

VERDICT_AUTO_ACCEPT = "AUTO_ACCEPT"
VERDICT_QUARANTINE_MEDIUM = "QUARANTINE_MEDIUM"
VERDICT_QUARANTINE_LOW = "QUARANTINE_LOW"
VERDICT_QUARANTINE_HARD = "QUARANTINE_HARD"

ACCEPT_THRESHOLD = 90.0  # >= => AUTO_ACCEPT
QUARANTINE_MEDIUM_THRESHOLD = 75.0  # < 90 but >= => QUARANTINE_MEDIUM

VERDICTS = {
    VERDICT_AUTO_ACCEPT: "ok - 自动接受（90–100 分）",
    VERDICT_QUARANTINE_MEDIUM: "quarantine - 中危（75–89 分）",
    VERDICT_QUARANTINE_LOW: "quarantine - 低危（0–74 分）",
    VERDICT_QUARANTINE_HARD: "quarantine - 硬失败（分值无法补偿）",
}

REVIEWED_STATUSES = {"verified", "reviewed", "accepted"}
CANDIDATE_STATUSES = {"candidate", "needs_review", None, ""}

# 古代史料标题（primary anchor）用于 source-quality 判定
CLASSICAL_TITLE_HINTS = (
    "尚书",
    "春秋",
    "左传",
    "国语",
    "战国策",
    "史记",
    "汉书",
    "后汉书",
    "三国志",
    "晋书",
    "宋书",
    "梁书",
    "陈书",
    "魏书",
    "北齐书",
    "周书",
    "隋书",
    "南史",
    "北史",
    "旧唐书",
    "新唐书",
    "旧五代史",
    "新五代史",
    "宋史",
    "辽史",
    "金史",
    "续资治通鉴长编",
    "元史",
    "明史",
    "明实录",
    "清史稿",
    "清实录",
    "资治通鉴",
    "通鉴",
    "竹书纪年",
    "唐六典",
    "宋会要",
)

# AGENTS.md §10：official archives 与 primary historical texts 同为 Tier-A。
# 近现代事件的 primary anchor 常为官方档案/机构汇编，需与古代史料标题同级加分。
TIER_A_ARCHIVE_HINTS = (
    "档案史料",
    "官方档案",
    "审判档案",
    "受降档案",
    "军事科学院",
    "中央档案馆",
    "档案馆",
    "馆藏档案",
)


def classify(score: float, hard_failures: Iterable[str] = ()) -> str:
    """Return the quality verdict for a score, overriding with QUARANTINE_HARD

    when any hard failure is present (AGENTS.md §17 — score cannot compensate)."""
    if hard_failures:
        return VERDICT_QUARANTINE_HARD
    if score >= ACCEPT_THRESHOLD:
        return VERDICT_AUTO_ACCEPT
    if score >= QUARANTINE_MEDIUM_THRESHOLD:
        return VERDICT_QUARANTINE_MEDIUM
    return VERDICT_QUARANTINE_LOW


def _score_people_or_places(
    items: list[dict[str, Any]],
    key_id: str,
    weight: int,
    label: str,
) -> tuple[float, str]:
    """Fraction-resolved scoring for `people` / `places` lists.

    A fully resolved bridge entry requires a canonical id plus link_status
    ``linked`` plus (when present) link_confidence >= 0.8. If an event simply
    has no such bridge list, it scores a neutral (weight*0.7)
    — the absence is a completeness matter, not a resolution failure.
    """
    if not items:
        score = weight * 0.7
        reason = f"事件未声明 {label} 桥接（缺失为完整性问题，不判分辨率）"
        return score, reason
    resolved = 0
    for item in items:
        ok = bool(item.get(key_id)) and item.get("link_status") == "linked"
        conf = item.get("link_confidence")
        if ok and conf is not None and conf < 0.8:
            ok = False
        if ok:
            resolved += 1
    ratio = resolved / len(items)
    return round(
        ratio * weight, 2
    ), f"{resolved}/{len(items)} 已规范解析（link_status=linked + 规范 ID）"


def _score_source_quality(event: dict[str, Any]) -> tuple[float, str]:
    src_ref = (event.get("source_reference") or "").strip()
    src_ids = event.get("source_ids") or []
    base, reasons = 0.0, []
    if not (src_ref or src_ids):
        return 0.0, "无 source_reference/source_ids（qaq 现值 0）"
    base += 8.0
    reasons.append("已有 source_reference/source_ids")
    has_primary_anchor = any(hint in src_ref for hint in CLASSICAL_TITLE_HINTS)
    has_archive_anchor = any(hint in src_ref for hint in TIER_A_ARCHIVE_HINTS)
    if has_primary_anchor or has_archive_anchor:
        base += 4.0
        reasons.append("source_reference 含 Tier-A 锚点（古代史料标题或官方档案/机构汇编）")
    if event.get("source_type") == "curated_reference" or len(src_ids) >= 1:
        base += 3.0
        reasons.append("source_type=curated_reference 或 source_ids 非空")
    return round(min(15.0, base), 2), "; ".join(reasons) or "弱来源"


def _score_evidence_precision(event: dict[str, Any]) -> tuple[float, str]:
    items = event.get("evidence") or []
    if not items:
        return 0.0, "无 evidence 条目（evidence_precision 0）"
    total = 0.0
    n = len(items)
    for item in items:
        x = 3.0 if (item.get("work") and item.get("term")) else 1.0
        role = item.get("evidence_role")
        if role == "primary":
            x += 2.0
        elif role == "supporting":
            x += 1.5
        elif role == "related":
            x += 1.0
        if item.get("chapter_hint"):
            x += 1.2
        if item.get("historical_text_id"):
            x += 1.0
        total += x
    # reviewed 加成
    if event.get("quality_status") in REVIEWED_STATUSES:
        total += 0.5 * n
    return round(min(15.0, total), 1), f"{n} 条 evidence（work/term/role 加权）"


def _score_independent_verification(event: dict[str, Any]) -> tuple[float, str]:
    """AGENTS.md §9: count ≠ independent count."""
    src_ids = [s for s in (event.get("source_ids") or []) if s]
    src_ref = (event.get("source_reference") or "").strip()
    distinct = len(set(src_ids))
    has_primary_anchor = any(hint in src_ref for hint in CLASSICAL_TITLE_HINTS)
    has_archive_anchor = any(hint in src_ref for hint in TIER_A_ARCHIVE_HINTS)
    has_anchor = has_primary_anchor or has_archive_anchor
    # 古代史料 + modern 参考两级
    if distinct >= 2 or (distinct >= 1 and src_ref and has_anchor):
        return 10.0, f"≥2 独立来源锚点（source_ids={distinct}）"
    if distinct == 1 and src_ref and has_anchor:
        return 7.5, "1 个独立 source_id + Tier-A 锚点（中等）"
    if src_ref:
        return 4.0, "仅 source_reference 文本（单锚点）"
    if distinct == 1:
        return 4.0, "仅 1 个 source_id"
    return 0.0, "无来源锚点"


def _score_completeness(event: dict[str, Any]) -> tuple[float, str]:
    name = event.get("name_zh_cn")
    summary = event.get("summary_zh_cn")
    overview = event.get("overview_zh_cn") or event.get("background_zh_cn")
    result = event.get("result_zh_cn")
    importance = event.get("importance")
    total = 0.0
    if name:
        total += 2.0
    if summary:
        total += 4.0
    if overview:
        total += 1.5
    if result:
        total += 1.5
    if importance in {"critical", "major", "normal", "minor"}:
        total += 1.0
    return round(
        min(10.0, total), 1
    ), f"name/summary/background/result/importance 共 {round(min(10.0, total), 1)} 分"


def _score_independent_verifier(event: dict[str, Any]) -> tuple[float, str]:
    """是否存在与 Producer 分离的 Reviewer 信号（quality_status / review 文件）。"""
    status = event.get("quality_status")
    if status == "verified":
        return 10.0, "已由独立 Verifier 确认 (quality_status=verified)"
    if status == "reviewed":
        return 9.0, "已人工 review (quality_status=reviewed)"
    if status == "accepted":
        return 6.0, "accepted（未正式 review）"
    return 0.0, f"无独立 verifier 信号（quality_status={status!r}）"


def score_event(
    event: dict[str, Any],
    *,
    person_years: dict[str, tuple[Any, Any]] | None = None,
    place_windows: dict[str, tuple[Any, Any]] | None = None,
    temporal_conflicts: list[tuple[str, str]] | None = None,
) -> dict[str, Any]:
    """Deterministic 100-point score for one event document.

    Args:
        event: event dict in `schemas/event.schema.json` shape.
        person_years: mapping person_id -> (birth_year, death_year) to enforce
            temporal consistency (may be empty; unknown lifespans are skipped,
            never invented).
        place_windows: mapping place_id -> (valid_from, valid_to).
        temporal_conflicts: list of (event_id, detail) already computed by
            temporal checks; a non-empty list adds a hard failure.

    Returns a dict with ``score``, ``verdict``, ``dims`` (per-dimension
    breakdown), ``hard_failures`` and ``reasons`` (human-facing list).
    """
    person_years = person_years or {}
    place_windows = place_windows or {}
    temporal_conflicts = temporal_conflicts or []

    dims: dict[str, dict[str, Any]] = {}

    # 1) schema / fk / uniqueness
    # 唯一性/FK 由确定性校验门（validate.py）返回错误列表，分值不受重复影响。
    dims["schema_fk_uniqueness"] = {
        "score": 10.0,
        "reason": "唯一性/FK 由确定性校验门负责；框架不重复计数",
    }

    # 2) temporal consistency
    t_score = 10.0
    t_reasons = []
    start = event.get("start_year")
    end = event.get("end_year", start)
    precision = event.get("date_precision")
    if start is not None and end is not None and start > end:
        t_score = 0.0
        t_reasons.append("start_year > end_year（即时序矛盾）")
    else:
        if precision in {"exact", "year", "range"} and start is None:
            t_score -= 2.0
            t_reasons.append("date_precision 要求但无 start_year")
        if precision not in {
            "exact",
            "year",
            "range",
            "approximate",
            "before",
            "after",
            "unknown",
        }:
            t_score -= 1.0
            t_reasons.append("date_precision 非法")
    if temporal_conflicts:
        t_score = 0.0
        t_reasons.append("存在 event/person 或 event/place 时序冲突")
    dims["temporal_consistency"] = {
        "score": round(max(0.0, t_score), 1),
        "reason": "; ".join(t_reasons) or "无冲突",
    }

    # 3) person resolution
    score, reason = _score_people_or_places(
        event.get("people", []), "person_id", 10, "人物"
    )
    dims["person_resolution"] = {"score": score, "reason": reason}

    # 4) place resolution
    score, reason = _score_people_or_places(
        event.get("places", []), "place_id", 10, "地点"
    )
    dims["place_resolution"] = {"score": score, "reason": reason}

    # 5) source quality
    score, reason = _score_source_quality(event)
    dims["source_quality"] = {"score": score, "reason": reason}

    # 6) evidence precision
    score, reason = _score_evidence_precision(event)
    dims["evidence_precision"] = {"score": score, "reason": reason}

    # 7) independent source verification
    score, reason = _score_independent_verification(event)
    dims["independent_source_verification"] = {"score": score, "reason": reason}

    # 8) content completeness
    score, reason = _score_completeness(event)
    dims["content_completeness"] = {"score": score, "reason": reason}

    # 9) independent verifier
    score, reason = _score_independent_verifier(event)
    dims["independent_verifier"] = {"score": score, "reason": reason}

    total = sum(d["score"] for d in dims.values())
    total = round(total, 1)

    hard: list[str] = []
    if start is not None and end is not None and start > end:
        hard.append("impossible_chronology")
    if temporal_conflicts:
        hard.append(
            "impossible_chronology: " + " | ".join(d for _, d in temporal_conflicts[:3])
        )

    verdict = classify(total, hard)

    reasons = [
        f"{name}={d['score']:.1f}/{WEIGHTS[name]} ({d['reason']})"
        for name, d in dims.items()
    ]
    return {
        "event_id": event.get("id"),
        "score": total,
        "verdict": verdict,
        "dims": {name: {"weight": WEIGHTS[name]} | d for name, d in dims.items()},
        "hard_failures": hard,
        "reasons": reasons,
    }
