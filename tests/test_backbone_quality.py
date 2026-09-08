"""Quality scoring engine tests (AGENTS.md §16/§17).

Covers: weight invariants, verdict thresholds, per-dimension computation,
hard-failure override, and exact determinism.
"""

from __future__ import annotations

import pytest

from history_data_pipeline.backbone import quality as q


def _rich_event(**overrides):
    """A canonical event designed to AUTO_ACCEPT under the rubric."""
    event = {
        "id": "event-test-rich",
        "name_zh_cn": "测试之役",
        "start_year": -700,
        "end_year": -690,
        "date_precision": "range",
        "summary_zh_cn": "简述",
        "overview_zh_cn": "背景",
        "result_zh_cn": "结果",
        "importance": "critical",
        "source_reference": "《左传》僖公",
        "source_ids": ["src-a", "src-b"],
        "source_type": "curated_reference",
        "quality_status": "verified",
        "people": [
            {"person_id": "p1", "link_status": "linked", "link_confidence": 0.9}
        ],
        "places": [
            {"place_id": "pl1", "link_status": "linked", "link_confidence": 0.95}
        ],
        "evidence": [
            {
                "work": "左传",
                "term": "僖公十五年",
                "evidence_role": "primary",
                "historical_text_id": "T1",
            },
            {
                "work": "史记",
                "term": "晋世家",
                "evidence_role": "supporting",
                "historical_text_id": "T2",
            },
        ],
    }
    event.update(overrides)
    return event


def test_weights_sum_to_100():
    assert sum(q.WEIGHTS.values()) == 100
    assert set(q.WEIGHTS) == {
        "schema_fk_uniqueness",
        "temporal_consistency",
        "person_resolution",
        "place_resolution",
        "source_quality",
        "evidence_precision",
        "independent_source_verification",
        "content_completeness",
        "independent_verifier",
    }


def test_classify_thresholds():
    assert q.classify(90.0) == q.VERDICT_AUTO_ACCEPT
    assert q.classify(99.0) == q.VERDICT_AUTO_ACCEPT
    assert q.classify(89.0) == q.VERDICT_QUARANTINE_MEDIUM
    assert q.classify(75.0) == q.VERDICT_QUARANTINE_MEDIUM
    assert q.classify(74.9) == q.VERDICT_QUARANTINE_LOW
    assert q.classify(0.0) == q.VERDICT_QUARANTINE_LOW


def test_classify_hard_overrides_score():
    assert (
        q.classify(99.0, hard_failures=["impossible_chronology"])
        == q.VERDICT_QUARANTINE_HARD
    )


def test_rich_event_auto_accepts():
    result = q.score_event(_rich_event())
    assert result["verdict"] == q.VERDICT_AUTO_ACCEPT
    assert result["score"] >= 90.0
    assert result["hard_failures"] == []
    dims = result["dims"]
    assert all(dims[k]["weight"] == q.WEIGHTS[k] for k in q.WEIGHTS)
    assert sum(dims[k]["weight"] for k in q.WEIGHTS) == 100


def test_results_are_deterministic():
    a = q.score_event(_rich_event())
    b = q.score_event(_rich_event())
    assert a == b


def test_impossible_chronology_is_a_hard_failure():
    result = q.score_event(_rich_event(start_year=700, end_year=400))
    assert result["verdict"] == q.VERDICT_QUARANTINE_HARD
    assert any("impossible_chronology" in h for h in result["hard_failures"])
    # 分值无法补偿：分数即使很高也被硬失败覆盖
    assert result["dims"]["temporal_consistency"]["score"] == 0.0


def test_temporal_conflict_list_forces_hard_failure():
    result = q.score_event(
        _rich_event(),
        temporal_conflicts=[("event-test-rich", "人物 某 出生晚于事件结束")],
    )
    assert result["verdict"] == q.VERDICT_QUARANTINE_HARD
    assert result["dims"]["temporal_consistency"]["score"] == 0.0


def test_unresolved_people_penalize_person_dimension_only():
    event = _rich_event(people=[{"person_id": "p1"}])  # no link_status -> unresolved
    result = q.score_event(event)
    assert result["dims"]["person_resolution"]["score"] == 0.0
    # 其余维度不受人员链接影响
    assert result["dims"]["schema_fk_uniqueness"]["score"] == 10.0
    assert result["dims"]["source_quality"]["score"] == 15.0


def test_no_people_is_neutral_not_zero():
    event = _rich_event(people=[], places=[])
    result = q.score_event(event)
    # 缺人/地点是完整性问题，不做分辨率惩罚（weight*0.7）
    assert result["dims"]["person_resolution"]["score"] == pytest.approx(7.0)
    assert result["dims"]["place_resolution"]["score"] == pytest.approx(7.0)


def test_missing_evidence_and_sources_start_low():
    event = {
        "id": "event-empty",
        "name_zh_cn": "无名",
        "start_year": -500,
        "end_year": -500,
    }
    result = q.score_event(event)
    assert result["score"] < 40.0  # 无来源/无证据/无内容：远低于可接受线
    assert result["verdict"] == q.VERDICT_QUARANTINE_LOW
    assert result["dims"]["source_quality"]["score"] == 0.0
    assert result["dims"]["evidence_precision"]["score"] == 0.0


def test_score_within_documented_bounds():
    # 所有分数必须落在 0..100 之间且无 NaN
    import math

    for event in (_rich_event(), {"id": "x", "start_year": 1}):
        result = q.score_event(event)
        score = result["score"]
        assert isinstance(score, (int, float))
        assert not math.isnan(score)
        assert 0.0 <= score <= 100.0


def test_reasons_always_present_for_every_dimension():
    result = q.score_event(_rich_event())
    reasons = result["reasons"]
    assert len(reasons) == len(q.WEIGHTS)
    # 每个维度都被记录 reason
    for name in q.WEIGHTS:
        assert any(reason.startswith(name) for reason in reasons)
