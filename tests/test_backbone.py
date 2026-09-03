"""Backbone 校验测试：taxonomy / event / story / 引用完整性 / Schema。

所有测试都从 Curated Backbone（data/curated/history_backbone/）读取，
不依赖网络与 legacy 数据库。
"""

from __future__ import annotations

from pathlib import Path

import pytest

from history_data_pipeline.backbone.loader import load_backbone
from history_data_pipeline.backbone.reference import CANONICAL_PERSON_NAMES, resolve_references, _seed_place_ids
from history_data_pipeline.backbone.schema import load_schemas, validate_document
from history_data_pipeline.backbone.validate import (
    DATE_PRECISIONS,
    EVIDENCE_ROLES,
    RELATION_TYPES,
    validate_backbone,
)

ROOT = Path(__file__).parents[1]


@pytest.fixture(scope="module")
def backbone():
    return load_backbone(ROOT)


@pytest.fixture(scope="module")
def schemas():
    return load_schemas(ROOT)


def test_backbone_loads(backbone):
    assert len(backbone.periods) >= 30
    assert len(backbone.regimes) >= 30
    # Batch 1（82）+ Batch 2（70）+ Batch 3（LATE_HAN 15 + TK 13 + WJ 12 + EJ16K 22）
    assert len(backbone.events) == 240
    assert len(backbone.stories) == 3
    # 三个 Story 标题
    assert {story["title_zh_cn"] for story in backbone.stories} == {"楚汉争霸", "三国格局形成", "安史之乱"}


def test_validate_backbone_clean(backbone):
    assert validate_backbone(backbone, ROOT) == []


def test_raw_immutable():
    """Layer 1 规则：data/raw 永不可变、不入 Git；构建产物不得出现在 raw。

    本地可能已下载官方快照（cbdb/ctext/wikipedia/wikisource/classical-modern 等，gitignored）；
    无论是否下载，raw 都不得出现任何 Pipeline 构建产物（构建产物归 dist/ 与 data/reports 等）。
    """
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    assert "data/raw/" in gitignore
    raw = ROOT / "data" / "raw"
    assert raw.exists()
    entries = {path.name for path in raw.iterdir() if path.name != ".gitkeep"}
    forbidden = {"dist", "normalized", "exports", "reports", "logs", "staging", "curated", "candidates"}
    assert not (entries & forbidden), f"raw 中出现构建产物: {entries & forbidden}"
    # 官方数据集快照以外的内容不应在 raw（构建产物禁止写入 raw）
    assert not any(path.is_file() for path in raw.iterdir() if path.name != ".gitkeep"), "raw 根目录不应有散落文件"


def test_legacy_curated_preserved():
    """旧 Semantic Layer 数据不删除，标记 legacy。"""
    legacy = ROOT / "data" / "curated" / "stories.yml"
    assert legacy.exists()
    assert "历史" in legacy.read_text(encoding="utf-8")
    semantic_module = (ROOT / "src" / "history_data_pipeline" / "semantic_layer.py").read_text(encoding="utf-8")
    assert "LEGACY" in semantic_module.split("\n")[1].upper() or "legacy" in semantic_module.lower()


def test_period_schema(backbone, schemas):
    for period in backbone.periods:
        errors = validate_document(schemas, "period", period)
        assert errors == [], f"{period['id']}: {errors}"
    # 必须覆盖提示中的全部浏览 Period
    required = {"上古", "夏", "商", "西周", "春秋", "战国", "秦", "西汉", "新", "东汉", "东汉末", "三国",
                "西晋", "东晋", "十六国", "南北朝", "隋", "唐", "五代十国", "北宋", "辽", "西夏", "金",
                "南宋", "元", "明", "清", "晚清", "中华民国", "近现代"}
    names = {period["name_zh_cn"] for period in backbone.periods}
    assert required <= names, f"缺少 Period: {required - names}"


def test_regime_schema(backbone, schemas):
    for regime in backbone.regimes:
        errors = validate_document(schemas, "regime", regime)
        assert errors == [], f"{regime['id']}: {errors}"
    names = {regime["name_zh_cn"] for regime in backbone.regimes}
    assert {"曹魏", "蜀汉", "东吴"} <= names


def _strip(document: dict):
    return {k: v for k, v in document.items() if not k.startswith("_")}


def test_event_schema(backbone, schemas):
    for event in backbone.events:
        errors = validate_document(schemas, "event", _strip(event))
        assert errors == [], f"{event['id']}: {errors}"


def test_story_schema(backbone, schemas):
    for story in backbone.stories:
        errors = validate_document(schemas, "story", _strip(story))
        assert errors == [], f"{story['id']}: {errors}"


def test_event_dates(backbone):
    for event in backbone.events:
        assert event["date_precision"] in DATE_PRECISIONS, event["id"]
        start, end = event["start_year"], event["end_year"]
        if start is not None and end is not None:
            assert start <= end, f"{event['id']}: start={start} > end={end}"
    # 夏商周等早期 Period 不得伪装精确年代
    for period in backbone.periods:
        if period["name_zh_cn"] in {"夏", "商", "西周"}:
            assert period["date_precision"] in {"approximate", "range"}, period["id"]


def test_story_event_sequence(backbone):
    for story in backbone.stories:
        sequences = [item["sequence"] for item in story["events"]]
        assert len(sequences) == len(set(sequences)), story["id"]
        assert sequences == sorted(sequences), story["id"]
        assert all(isinstance(value, int) and value >= 1 for value in sequences), story["id"]


def test_event_person_reference(backbone):
    """Person 引用规则：linked 必须在 curated canonical identity 中；needs_linking 保留 name_raw。"""
    for event in backbone.events:
        for person in event.get("people", []):
            assert person.get("person_name_raw"), f"{event['id']}: person 缺 name_raw"
            link_status = person.get("link_status")
            assert link_status in {"linked", "needs_linking", "pending_knowledge", "rejected"}, f"{event['id']}: {link_status}"
            if link_status == "linked":
                assert person.get("person_id"), f"{event['id']}: linked 但无 person_id"
                assert person["person_id"] in CANONICAL_PERSON_NAMES, f"{event['id']}: 未知 linked person {person['person_id']}"
            else:
                assert person.get("person_id") is None, f"{event['id']}: {link_status} 不应带 person_id {person['person_id']}"


def test_event_place_reference(backbone):
    seed_places = _seed_place_ids(backbone)
    for event in backbone.events:
        for place in event.get("places", []):
            assert place.get("place_name_raw"), f"{event['id']}: place 缺 name_raw"
            link_status = place.get("link_status")
            assert link_status in {"linked", "needs_linking", "pending_knowledge", "rejected"}
            if link_status == "linked":
                assert place.get("place_id"), f"{event['id']}: linked 但无 place_id"
                assert place["place_id"] in seed_places, f"{event['id']}: 未知 linked place {place['place_id']}"
            else:
                assert place.get("place_id") is None, f"{event['id']}: {link_status} 不应带 place_id"


def test_event_evidence_reference(backbone):
    """Evidence 规则（V1 采用 Event First, Evidence Later，见 China History Backbone V1 §11/§13）：
    事件允许暂不携带 evidence（不要求第一阶段就具备 HistoricalText ID）；
    凡携带 evidence 的必须满足 work/term/role/link_status 规则。"""
    for event in backbone.events:
        for evidence in event.get("evidence", []):
            assert evidence.get("work") and evidence.get("term"), f"{event['id']}: evidence 缺 work/term"
            assert evidence.get("evidence_role") in EVIDENCE_ROLES, f"{event['id']}: role={evidence.get('evidence_role')}"
            assert evidence.get("link_status") in {"linked", "needs_linking", "pending_knowledge", "rejected"}
            if evidence.get("link_status") == "linked":
                assert evidence.get("historical_text_id"), f"{event['id']}: linked evidence 缺 historical_text_id"


def test_event_relation_reference(backbone):
    event_ids = backbone.event_ids
    for event in backbone.events:
        for relation in event.get("relations", []):
            assert relation.get("relation_type") in RELATION_TYPES, f"{event['id']}: {relation.get('relation_type')}"
            target = relation.get("target_event_id")
            assert target in event_ids, f"{event['id']}: 关系目标不存在 {target}"
            assert target != event["id"], f"{event['id']}: 自引用"
            confidence = relation.get("confidence")
            if confidence is not None:
                assert 0.0 <= confidence <= 1.0


def test_source_traceability(backbone):
    for story in backbone.stories:
        assert story.get("source_type") == "curated_reference"
        assert story.get("source_reference")
    for event in backbone.events:
        assert event.get("source_type") == "curated_reference"
        assert event.get("source_reference")
    # 每条 evidence 的审核记录（review_note）应可追溯
    for event in backbone.events:
        for evidence in event.get("evidence", []):
            assert evidence.get("review_note"), f"{event['id']}: evidence 缺 review_note"


def test_evidence_not_auto_generated_from_text():
    """Knowledge Store 不允许自动生成 Event：检查 Backbone 里所有 Event 都是人工 curated 文件。"""
    for path in (ROOT / "data" / "curated" / "history_backbone" / "events").rglob("*.yml"):
        text = path.read_text(encoding="utf-8")
        assert "source_type: curated_reference" in text, path
        assert "自动生成" not in text, path


@pytest.fixture(scope="module")
def resolution(backbone):
    return resolve_references(backbone, knowledge_db=None)


def test_resolution_linked_places(resolution):
    assert resolution.places["linked"] == 3
    assert resolution.places["needs_linking"] == 23


def test_resolution_no_broken(resolution):
    assert resolution.broken == []
    assert resolution.persons["linked"] == 58
    assert resolution.evidences["pending_knowledge"] == 26


def test_unique_person_ids(resolution):
    ids = list(resolution.seed_persons.keys())
    assert len(ids) == len(set(ids))
    assert "cbdb-person-30257" in ids  # 曹操
    assert "curated-person-fan-zeng" in ids  # 范增

def test_pre_qin_events_baseline(backbone):
    """China History Backbone V1 · Batch 1：先秦 Event 主干完整性基线。"""
    pre_qin = [e for e in backbone.events if e["period_id"] in {"period-xia", "period-shang", "period-western-zhou"}]
    chunqiu = [e for e in backbone.events if e["period_id"] == "period-spring-autumn"]
    zhanguo = [e for e in backbone.events if e["period_id"] == "period-warring-states"]
    assert len(pre_qin) >= 15, f"夏商周事件过少: {len(pre_qin)}"
    assert len(chunqiu) >= 20, f"春秋事件过少: {len(chunqiu)}"
    assert len(zhanguo) >= 25, f"战国事件过少: {len(zhanguo)}"
    batch1 = pre_qin + chunqiu + zhanguo
    # V1 主干只维护 critical + major
    assert all(e["importance"] in {"critical", "major"} for e in batch1)
    assert all(e.get("source_reference") for e in batch1)
    # 早期纪年不伪装精确：前 1000 年以前的节点必须是 approximate/range
    for e in pre_qin:
        if e["start_year"] is not None and e["start_year"] < -1000:
            assert e["date_precision"] in {"approximate", "range"}, f"{e['id']} 早期纪年不应伪装精确"
    # 秦灭六国 aggregate + 至少 6 个 part_of 子事件（韩/赵/燕/魏/楚/齐）
    liuguo = next(e for e in batch1 if e["id"] == "event-qin-mie-liuguo")
    children = {e["id"] for e in batch1 for r in e.get("relations", [])
                if r["relation_type"] == "part_of" and r["target_event_id"] == "event-qin-mie-liuguo"}
    assert liuguo["importance"] == "critical"
    assert len(children) >= 6, f"秦灭六国子事件不足: {children}"


def test_timeline_filter_sorted(backbone):
    """backbone timeline：默认只含 critical+major，并按 start_year 升序。"""
    from history_data_pipeline.backbone.timeline import filter_timeline, timeline_record

    records = [timeline_record(e) for e in filter_timeline(backbone)]
    assert records
    assert all(r["importance"] in {"critical", "major"} for r in records)
    years = [r["start_year"] for r in records]
    assert years == sorted(years)
    # 先秦最早节点 = 夏朝建立（前2070）
    assert records[0]["id"] == "event-xia-jianguo"
    # period 过滤：战国只含 period-warring-states
    zhanguo = [r for r in (timeline_record(e) for e in filter_timeline(backbone, period_filter="warring"))]
    assert zhanguo and all(r["period_id"] == "period-warring-states" for r in zhanguo)
    # critical 过滤
    critical = [r for r in (timeline_record(e) for e in filter_timeline(backbone, importance={"critical"}))]
    assert all(r["importance"] == "critical" for r in critical)
    assert len(critical) >= 7


def test_backbone_qa_report_functions(backbone):
    """qa --report：duplicate 候选不应再标记已用 part_of 结构解释的 秦灭X 系列。"""
    from history_data_pipeline.backbone.qa_report import duplicate_check, gap_detection

    duplicates = duplicate_check(backbone)
    qin_mie_children = {"event-qin-mie-han", "event-qin-mie-zhao", "event-qin-mie-yan",
                        "event-qin-mie-wei", "event-qin-mie-chu", "event-qin-mie-qi"}
    for item in duplicates:
        pair = {item["event_a"]["id"], item["event_b"]["id"]}
        assert not pair <= qin_mie_children, f"秦灭X 子事件不应被标记为重复候选: {pair}"
    gaps = gap_detection(backbone)
    # 夏代传统纪年节点稀疏，存在真实空白（属于预期，不自动补点）
    assert any(g["period_id"] == "period-xia" for g in gaps)


# ---------------------------------------------------------------------------
# China History Backbone V1 · Batch 2（秦→西汉→新→东汉）
# ---------------------------------------------------------------------------
QIN_HAN_PERIODS = {"period-qin", "period-western-han", "period-xin", "period-eastern-han"}
CHU_HAN_EVENTS = {
    "event-chuhan-qin-revolt", "event-chuhan-julu", "event-chuhan-qin-fall",
    "event-hongmen", "event-chuhan-pengcheng", "event-chuhan-xingyang",
    "event-chuhan-gaixia", "event-chuhan-han-foundation", "event-chuhan-later",
}


def _qin_han_events(backbone):
    return [e for e in backbone.events if e["period_id"] in QIN_HAN_PERIODS]


def test_qin_han_backbone_baseline(backbone):
    """Batch 2：秦/西汉/新/东汉均形成 Backbone（数量下限 + 关键节点在场）。"""
    by_period = {pid: [e for e in _qin_han_events(backbone) if e["period_id"] == pid] for pid in QIN_HAN_PERIODS}
    assert len(by_period["period-qin"]) >= 8, f"秦事件过少: {len(by_period['period-qin'])}"
    assert len(by_period["period-western-han"]) >= 25, f"西汉事件过少: {len(by_period['period-western-han'])}"
    assert len(by_period["period-xin"]) >= 5, f"新事件过少: {len(by_period['period-xin'])}"
    assert len(by_period["period-eastern-han"]) >= 10, f"东汉事件过少: {len(by_period['period-eastern-han'])}"
    names = {e["name_zh_cn"] for e in _qin_han_events(backbone)}
    for key in ("秦推行郡县制", "陈胜吴广起义", "七国之乱", "漠北之战", "巫蛊之祸", "轮台诏",
                "王莽称帝、新朝建立", "昆阳之战", "刘秀称帝、东汉建立", "第一次党锢之祸", "第二次党锢之祸"):
        assert key in names, f"缺少关键节点: {key}"
    # Batch2 只维护 critical/major（既有迁移 9 Event 保留其原分级，如 event-chuhan-later=normal）
    batch2_new = [e for e in _qin_han_events(backbone) if e["id"] not in CHU_HAN_EVENTS]
    assert all(e["importance"] in {"critical", "major"} for e in batch2_new)


def test_qin_han_event_ids_unique(backbone):
    ids = [e["id"] for e in backbone.events]
    assert len(ids) == len(set(ids))
    qh_ids = [e["id"] for e in _qin_han_events(backbone)]
    assert len(qh_ids) == len(set(qh_ids))


def test_qin_han_period_refs(backbone):
    period_ids = {p["id"] for p in backbone.periods}
    for event in _qin_han_events(backbone):
        assert event["period_id"] in period_ids, event["id"]
    # 定向过滤可用（§45 CLI 语义）
    from history_data_pipeline.backbone.timeline import filter_timeline
    for needle in ("qin", "western-han", "xin", "eastern-han"):
        rows = filter_timeline(backbone, period_filter=needle)
        assert rows, f"--period {needle} 无结果"


def test_qin_han_timeline_order(backbone):
    from history_data_pipeline.backbone.timeline import filter_timeline, timeline_record
    rows = [timeline_record(e) for e in filter_timeline(backbone)]
    years = [r["start_year"] for r in rows if r["period_id"] in QIN_HAN_PERIODS]
    assert years == sorted(years)
    # 秦汉段首个 = 秦推行郡县制（前221，早于既有 秦统一 的口径差分由排序保证）
    qh = [r for r in rows if r["period_id"] in QIN_HAN_PERIODS]
    assert qh[0]["start_year"] >= -221


def test_existing_chu_han_events_reused(backbone):
    """楚汉 Story 9 个既有审核 Event 全部复用，无重复建档。"""
    by_id = {e["id"]: e for e in backbone.events}
    for event_id in CHU_HAN_EVENTS:
        assert event_id in by_id, f"缺失既有 Event: {event_id}"
        assert by_id[event_id]["quality_status"] == "reviewed"
    # 楚汉战争 aggregate 引用既有子事件（part_of，不重复建档）
    war = by_id["event-chuhan-war"]
    assert war["importance"] in {"critical", "major"}
    children = {e["id"] for e in backbone.events for r in e.get("relations", [])
                if r["relation_type"] == "part_of" and r["target_event_id"] == "event-chuhan-war"}
    assert {"event-hongmen", "event-chuhan-pengcheng", "event-chuhan-xingyang", "event-chuhan-gaixia"} <= children


def test_huangjin_event_reused(backbone):
    """黄巾起义复用既有 event-three-yellow-turbans，不新建第二个。"""
    matching = [e for e in backbone.events if "黄巾" in e["name_zh_cn"]]
    assert len(matching) == 1, f"黄巾事件应为 1 个，实际 {len(matching)}: {[e['id'] for e in matching]}"
    huangjin = matching[0]
    assert huangjin["id"] == "event-three-yellow-turbans"
    assert huangjin["start_year"] == 184
    # 党锢之祸 → 黄巾 有 precedes 衔接
    assert any(r["target_event_id"] == "event-three-yellow-turbans" and r["relation_type"] == "precedes"
               for e in backbone.events for r in e.get("relations", []))


def test_qin_unification_no_duplicate(backbone):
    """秦统一：不得出现 event-qin-tongyi 之外的重复建档（§40 语义近邻检查）。"""
    ids = [e["id"] for e in backbone.events]
    # 秦统一系列仍只存在于 chunqiu_zhanguo（Batch1 已建：秦灭六国 + 秦统一六国）
    unify = [e for e in backbone.events if e["id"] in {"event-qin-tongyi", "event-qin-mie-liuguo"}]
    assert len(unify) == 2, f"统一节点应为 秦灭六国+秦统一 两个: {[e['id'] for e in unify]}"
    assert "event-qin-tongyi" in ids
    # qin_han 目录内不得出现 秦统一/秦灭六国 的重复建档
    qh_files = {e["id"] for e in backbone.events if "qin_han" in e.get("_file", "")}
    assert not (qh_files & {"event-qin-tongyi", "event-qin-mie-liuguo"})
    # 党锢第一/第二次为规范分列（§26），不视作重复
    assert {"event-danggu-1", "event-danggu-2"} <= qh_files


def test_qin_han_source_coverage(backbone):
    """Batch2 Event 100% 携带 source_reference；新建 Event 同时携带 source_ids（两层来源链）。

    既有迁移 Event（楚汉 Story 9 个，仅带 source_reference）随其审核状态保留，
    不要求补 source_ids（沿用 §36：source 指 Event 来源依据而非 HistoricalText Evidence）。
    """
    for event in _qin_han_events(backbone):
        assert event.get("source_type") == "curated_reference", event["id"]
        assert event.get("source_reference"), event["id"]
        assert "AI" not in event["source_reference"] and "ChatGPT" not in event["source_reference"], event["id"]
    batch2_new = [e for e in _qin_han_events(backbone) if e["id"] not in CHU_HAN_EVENTS]
    for event in batch2_new:
        assert event.get("source_ids"), event["id"]
