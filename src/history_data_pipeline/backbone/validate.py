"""Backbone Validator：结构 + 引用完整性 + Schema 合规。

Validation Gate：发现 broken reference / duplicate id / invalid date /
accepted evidence missing source 等错误时，`build` 必须失败，不能只给 Warning。
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .loader import Backbone, EVENT_PERIOD_DIRS, PERIOD_DIR_HINTS

# 允许的引用链接状态
LINK_STATUSES = {"linked", "needs_linking", "pending_knowledge", "rejected"}
REVIEWED_STATUSES = {"verified", "reviewed", "accepted"}
# evidence role 枚举
EVIDENCE_ROLES = {"primary", "supporting", "related"}
DATE_PRECISIONS = {"exact", "year", "range", "approximate", "before", "after", "unknown"}
IMPORTANCES = {"critical", "major", "normal", "minor"}
RELATION_TYPES = {"precedes", "follows", "causes", "caused_by", "leads_to", "contributes_to", "part_of", "related_to"}


def _ids_unique(rows: list[dict[str, Any]], kind: str) -> list[str]:
    seen: dict[str, str] = {}
    errors: list[str] = []
    for row in rows:
        identifier = row.get("id")
        if not identifier:
            errors.append(f"{kind}: 缺少 id（file={row.get('_file', '?')}）")
            continue
        if identifier in seen:
            errors.append(f"{kind}: ID 重复 {identifier}（{seen[identifier]} 与 {row.get('_file', '?')}）")
        else:
            seen[identifier] = row.get("_file", "?")
    return errors


def _check_event_dates(event: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    start = event.get("start_year")
    end = event.get("end_year", start)
    precision = event.get("date_precision")
    if precision not in DATE_PRECISIONS:
        errors.append(f"events/{event['id']}: date_precision 非法: {precision!r}")
    if precision in {"exact", "year", "range"} and start is None:
        errors.append(f"events/{event['id']}: date_precision={precision} 但 start_year 为空")
    if start is not None and end is not None and start > end:
        errors.append(f"events/{event['id']}: start_year={start} > end_year={end}")
    return errors


def _check_reference_link(item: dict[str, Any], entity: str, event_id: str) -> list[str]:
    """引用规则：linked 必须给出规范 ID；需要关联/等待知识库允许 ID 为 null 但必须保留 name_raw。"""
    errors: list[str] = []
    link_status = item.get("link_status")
    if link_status and link_status not in LINK_STATUSES:
        errors.append(f"events/{event_id}: {entity} link_status 非法: {link_status!r}")
    if entity == "person":
        identifier = item.get("person_id")
    elif entity == "place":
        identifier = item.get("place_id")
    else:
        identifier = item.get("historical_text_id")
    if link_status == "linked" and not identifier:
        errors.append(f"events/{event_id}: {entity} 声明 link_status=linked 但未提供规范 ID")
    if entity == "person" and not item.get("person_name_raw"):
        errors.append(f"events/{event_id}: person 缺少 person_name_raw")
    if entity == "place" and not item.get("place_name_raw"):
        errors.append(f"events/{event_id}: place 缺少 place_name_raw")
    if entity == "evidence":
        for required in ("work", "term"):
            if not item.get(required):
                errors.append(f"events/{event_id}: evidence 缺少 {required}")
    return errors


def _validate_schema_objects(root: Path, backbone: Backbone) -> list[str]:
    """用 schemas/ 下的 JSON Schema 校验每个实体与桥接条目。"""
    from .schema import validate_document, load_schemas

    errors: list[str] = []
    schemas = load_schemas(root)
    if not schemas:
        return ["schemas/: 未找到 JSON Schema 文件，跳过 Schema 校验"]
    for period in backbone.periods:
        errors.extend(validate_document(schemas, "period", _strip(period)))
    for regime in backbone.regimes:
        errors.extend(validate_document(schemas, "regime", _strip(regime)))
    for event in backbone.events:
        errors.extend(validate_document(schemas, "event", _strip(event)))
        for person in event.get("people", []):
            errors.extend(validate_document(schemas, "event_person", {**person, "event_id": event["id"]}))
        for place in event.get("places", []):
            errors.extend(validate_document(schemas, "event_place", {**place, "event_id": event["id"]}))
        for evidence in event.get("evidence", []):
            errors.extend(validate_document(schemas, "event_evidence", {**evidence, "event_id": event["id"]}))
        for relation in event.get("relations", []):
            errors.extend(validate_document(schemas, "event_relation", {**relation, "source_event_id": event["id"]}))
    for story in backbone.stories:
        errors.extend(validate_document(schemas, "story", _strip(story)))
    return errors


def _strip(document: dict[str, Any]) -> dict[str, Any]:
    """去掉加载器注入的内部字段（_file），避免污染 Schema 校验。"""
    return {key: value for key, value in document.items() if not key.startswith("_")}


def validate_backbone(backbone: Backbone, root: Path | None = None) -> list[str]:
    """完整 Backbone 校验。返回错误列表；空列表表示通过。"""
    errors: list[str] = []

    # 1) ID 唯一
    errors.extend(_ids_unique(backbone.periods, "periods"))
    errors.extend(_ids_unique(backbone.regimes, "regimes"))
    errors.extend(_ids_unique(backbone.events, "events"))
    errors.extend(_ids_unique(backbone.stories, "stories"))

    period_ids = backbone.period_ids
    regime_ids = backbone.regime_ids
    event_ids = backbone.event_ids
    story_ids = backbone.story_ids

    # 2) Period / Regime 存在性
    for regime in backbone.regimes:
        if regime.get("period_id") and regime["period_id"] not in period_ids:
            errors.append(f"regimes/{regime['id']}: period_id 不存在 {regime['period_id']}")
        if regime.get("parent_regime_id") and regime["parent_regime_id"] not in regime_ids:
            errors.append(f"regimes/{regime['id']}: parent_regime_id 不存在 {regime['parent_regime_id']}")

    for event in backbone.events:
        if event.get("period_id") and event["period_id"] not in period_ids:
            errors.append(f"events/{event['id']}: period_id 不存在 {event['period_id']}")
        for regime_id in event.get("regime_ids") or []:
            if regime_id not in regime_ids:
                errors.append(f"events/{event['id']}: regime_id 不存在 {regime_id}")
        # 事件目录归属提示（不强制，仅提示）
        hint = PERIOD_DIR_HINTS.get(event.get("period_id", ""))
        if hint and event.get("_file") and f"/{hint}/" not in event["_file"]:
            pass  # 目录归属是组织约定，不阻断构建

    for story in backbone.stories:
        if story.get("period_id") and story["period_id"] not in period_ids:
            errors.append(f"stories/{story['id']}: period_id 不存在 {story['period_id']}")

    # 3) Event 时间合法
    for event in backbone.events:
        errors.extend(_check_event_dates(event))

    # 4) Story → Event 引用 + sequence 唯一
    for story in backbone.stories:
        sequences: list[int] = []
        for item in story.get("events", []):
            event_id = item.get("event_id")
            if event_id not in event_ids:
                errors.append(f"stories/{story['id']}: events 引用不存在 {event_id}")
            sequences.append(item.get("sequence"))
        duplicates = len(sequences) != len(set(sequences))
        if duplicates:
            errors.append(f"stories/{story['id']}: sequence 重复")
        if sequences != sorted(sequences):
            errors.append(f"stories/{story['id']}: sequence 未按序排列")

    # 5) EventRelation 两端存在 + 关系类型白名单
    for event in backbone.events:
        event_relations = event.get("relations", [])
        for relation in event_relations:
            target = relation.get("target_event_id")
            if target not in event_ids:
                errors.append(f"events/{event['id']}: relation 目标事件不存在 {target}")
            if relation.get("relation_type") not in RELATION_TYPES:
                errors.append(f"events/{event['id']}: relation_type 非法 {relation.get('relation_type')!r}（只允许 {sorted(RELATION_TYPES)}）")
            if relation.get("confidence") is not None and not (0.0 <= relation["confidence"] <= 1.0):
                errors.append(f"events/{event['id']}: relation confidence 越界 {relation.get('confidence')}")
            if target == event["id"]:
                errors.append(f"events/{event['id']}: 自引用关系 target_event_id == 自身")

    # 6) EventPerson / EventPlace / EventEvidence 引用规则
    for event in backbone.events:
        for person in event.get("people", []):
            errors.extend(_check_reference_link(person, "person", event["id"]))
            if person.get("importance") and person["importance"] not in IMPORTANCES:
                errors.append(f"events/{event['id']}: person importance 非法 {person['importance']!r}")
        for place in event.get("places", []):
            errors.extend(_check_reference_link(place, "place", event["id"]))
        for evidence in event.get("evidence", []):
            errors.extend(_check_reference_link(evidence, "evidence", event["id"]))
            role = evidence.get("evidence_role")
            if role and role not in EVIDENCE_ROLES:
                errors.append(f"events/{event['id']}: evidence_role 非法 {role!r}（只允许 primary/supporting/related）")
            # Evidence 必须体现审核状态
            quality = evidence.get("quality_status") or evidence.get("link_quality_status")
            link_status = evidence.get("link_status")
            if link_status != "needs_linking" and quality not in REVIEWED_STATUSES:
                errors.append(f"events/{event['id']}: evidence 未审核（quality_status={quality!r}, link_status={link_status!r}）")
            # accepted evidence 必须有 source 依据
            if quality in {"reviewed", "verified", "accepted"} and not (evidence.get("work") and evidence.get("term")):
                errors.append(f"events/{event['id']}: accepted evidence 缺少 work/term 来源依据")

    # 7) 孤儿引用（Person/Place 引用已在上方按 link_status 规则检查；这里检查事件内部重复 person/place 条目）
    for event in backbone.events:
        seen_persons: set[str] = set()
        for person in event.get("people", []):
            key = person.get("person_id") or person.get("person_name_raw", "")
            if key in seen_persons:
                errors.append(f"events/{event['id']}: people 重复条目 {key}")
            seen_persons.add(key)
        seen_places: set[str] = set()
        for place in event.get("places", []):
            key = place.get("place_id") or place.get("place_name_raw", "")
            if key in seen_places:
                errors.append(f"events/{event['id']}: places 重复条目 {key}")
            seen_places.add(key)

    # 8) Schema 合规（jsonschema）
    if root is not None:
        errors.extend(_validate_schema_objects(root, backbone))

    # 9) Taxonomy 枚举自洽
    relation_type_ids = {row.get("id") for row in backbone.relation_types}
    for relation_id in RELATION_TYPES:
        if relation_type_ids and relation_id not in relation_type_ids:
            errors.append(f"taxonomy/relation_types: 缺少 {relation_id}")
    return errors


def check_strict_gate(backbone: Backbone, errors: list[str], root: Path | None = None) -> None:
    """Validation Gate：存在阻断性错误时抛出 RuntimeError。"""
    fatal = []
    for error in errors:
        if any(token in error for token in ("ID 重复", "引用不存在", "孤儿", "自引用", "start_year", "link_status=linked 但未提供", "accepted evidence", "evidence 未审核", "date_precision 非法")):
            fatal.append(error)
    if fatal:
        raise RuntimeError("Backbone Validation Gate 失败（构建终止）：\n  " + "\n  ".join(fatal[:50]))