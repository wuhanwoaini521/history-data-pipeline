"""Final Build：Backbone Validation → Reference Resolution → dist/history.duckdb。

DuckDB 是 Build Artifact，禁止手动 UPDATE；所有修改必须回到 Curated/Review
后重新构建。输出：
- dist/history.duckdb
- dist/parquet/*.parquet
- dist/json/*.json
- dist/manifest.json + dist/manifests/manifest-<version>.json
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .loader import Backbone, load_backbone
from .reference import (
    ResolutionResult,
    knowledge_seed_rows,
    resolve_references,
    supplemental_person_rows,
)
from .validate import check_strict_gate, validate_backbone

CURATED_SOURCE_ID = "source-curated-backbone-v1"
LEGACY_SEMANTIC_SOURCE_ID = "source-curated-semantic-v1"
SUPPLEMENT_SOURCE_ID = "source-curated-person-knowledge-gap"
DEFAULT_VERSION = "2026.09.0"

# 知识库（Layer 2）表在导出清单中的分组
KNOWLEDGE_TABLES = ("sources", "people", "person_aliases", "places", "works", "historical_texts", "entity_source_mapping")

BACKBONE_TABLES = [
    "periods", "regimes", "events", "stories", "story_events",
    "event_relations", "event_person", "event_place", "event_evidence",
    "event_evidence_candidates", "event_text", "event_text_candidates",
]

EXPORT_JSON_GROUPS = {
    "periods": "SELECT * FROM periods ORDER BY id",
    "regimes": "SELECT * FROM regimes ORDER BY id",
    "events": "SELECT * FROM events ORDER BY id",
    "event_relations": "SELECT * FROM event_relations ORDER BY source_event_id, target_event_id",
    "stories": "SELECT * FROM stories ORDER BY id",
    "story_events": "SELECT * FROM story_events ORDER BY story_id, sequence",
    "event_people": "SELECT * FROM event_person ORDER BY event_id, person_id",
    "event_places": "SELECT * FROM event_place ORDER BY event_id, sequence",
    "event_evidence": "SELECT * FROM event_evidence ORDER BY event_id, historical_text_id",
    "people": "SELECT * FROM people ORDER BY id",
    "places": "SELECT * FROM places ORDER BY id",
    "works": "SELECT * FROM works ORDER BY id",
    "historical_texts": "SELECT * FROM historical_texts ORDER BY id",
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _json(value: Any) -> str | None:
    if value is None:
        return None
    return json.dumps(value, ensure_ascii=False) if isinstance(value, (list, dict)) else str(value)


def git_commit(root: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=str(root), capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return None


def read_data_version(root: Path) -> str:
    version_file = root / "DATA_VERSION"
    if version_file.exists():
        value = version_file.read_text(encoding="utf-8").strip()
        if value:
            return value
    return DEFAULT_VERSION


def _sql_path(path: Path) -> str:
    return str(path.resolve()).replace("'", "''")


def _ensure_sources(connection, root: Path, curated_dir: Path) -> None:
    """登记 Layer 1 数据源声明 + 本层 curated 来源。"""
    from ..config import PipelinePaths

    paths = PipelinePaths(root)
    rows = []
    raw_dir = paths.raw
    if raw_dir.exists():
        for dataset_dir in sorted(raw_dir.iterdir()):
            if not dataset_dir.is_dir():
                continue
            for snapshot in sorted(p for p in dataset_dir.iterdir() if p.is_dir()):
                metadata_path = snapshot / "metadata.json"
                if not metadata_path.exists():
                    continue
                metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
                rows.append({
                    "id": f"source-{dataset_dir.name}", "dataset": dataset_dir.name,
                    "original_url": metadata.get("source_url"), "snapshot_version": metadata.get("version"),
                    "dataset_version": metadata.get("version"), "source_type": "official_snapshot",
                    "license": metadata.get("license"), "raw_path": str(snapshot.relative_to(root)),
                    "quality_status": "source_backed",
                })
    # curated backbone 来源
    rows.append({
        "id": CURATED_SOURCE_ID, "dataset": "curated-backbone", "snapshot_version": DEFAULT_VERSION,
        "dataset_version": DEFAULT_VERSION, "source_type": "curated_reference",
        "license": "项目人工整理；需保留依据与来源链", "raw_path": str(curated_dir.relative_to(root)),
        "quality_status": "reviewed",
        "notes": "History Backbone 人工整理数据；不冒充 CBDB/CText 原始数据。",
    })
    rows.append({
        "id": LEGACY_SEMANTIC_SOURCE_ID, "dataset": "curated-semantic-legacy", "snapshot_version": "history-semantic-v1",
        "dataset_version": "history-semantic-v1", "source_type": "curated_reference",
        "license": "项目人工整理；保留依据与来源链", "raw_path": str((root / "data" / "curated").relative_to(root)),
        "quality_status": "legacy",
        "notes": "旧 Semantic Layer V1（legacy/deprecated），仅审计用；新数据以 curated-backbone 为准。",
    })
    rows.append({
        "id": SUPPLEMENT_SOURCE_ID, "dataset": "curated-person-knowledge-gap", "snapshot_version": "v2.1.1",
        "dataset_version": "v2.1.1", "source_type": "curated_reference",
        "license": "项目人工整理；每条均含 source_reference 证据链与 agent 复核",
        "raw_path": str((root / "data" / "curated" / "persons").relative_to(root)),
        "quality_status": "reviewed",
        "notes": "V2.1.1 关键知识缺口恢复：仅 genuinely-missing 的补充 Person；不冒充 CBDB/CText。",
    })
    for row in rows:
        connection.execute("""
            INSERT OR REPLACE INTO sources
              (id,dataset,original_id,original_url,snapshot_version,snapshot_date,dataset_version,source_type,
               license,retrieved_at,raw_file,raw_path,staging_path,quality,quality_status,commercial_use,
               redistribution,attribution,notes)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, [
            row["id"], row["dataset"], None, row.get("original_url"),
            row.get("snapshot_version"), _now()[:10], row.get("dataset_version") or row.get("snapshot_version"),
            row.get("source_type"), row.get("license"), _now(), None, row.get("raw_path"), None,
            row.get("source_type"), row.get("quality_status"), None, "unknown", "required", row.get("notes"),
        ])


def _insert_taxonomy(connection, backbone: Backbone) -> None:
    for period in backbone.periods:
        connection.execute("""
            INSERT OR REPLACE INTO periods
              (id,name_zh_cn,name_raw,start_year,end_year,date_precision,description_zh_cn,quality_status,
               source_type,source_reference,source_ids)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)
        """, [
            period["id"], period["name_zh_cn"], period.get("name_raw") or period["name_zh_cn"],
            period.get("start_year"), period.get("end_year"), period.get("date_precision"),
            period.get("description_zh_cn"), period.get("quality_status", "reviewed"),
            period.get("source_type", "curated_reference"), period.get("source_reference"),
            _json(period.get("source_ids") or [CURATED_SOURCE_ID]),
        ])
    for regime in backbone.regimes:
        connection.execute("""
            INSERT OR REPLACE INTO regimes
              (id,name_zh_cn,name_raw,start_year,end_year,date_precision,period_id,parent_regime_id,
               capital_place_id,parent_dynasty_id,description_zh_cn,quality_status,source_type,source_reference,source_ids)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, [
            regime["id"], regime["name_zh_cn"], regime.get("name_raw") or regime["name_zh_cn"],
            regime.get("start_year"), regime.get("end_year"), regime.get("date_precision"),
            regime.get("period_id"), regime.get("parent_regime_id"), regime.get("capital_place_id"),
            regime.get("parent_dynasty_id"), regime.get("description_zh_cn"),
            regime.get("quality_status", "reviewed"), regime.get("source_type", "curated_reference"),
            regime.get("source_reference"), _json(regime.get("source_ids") or [CURATED_SOURCE_ID]),
        ])


def _insert_knowledge(connection, result: ResolutionResult, real_knowledge_db: Path | None) -> None:
    people, places, works = knowledge_seed_rows(result)
    if real_knowledge_db and real_knowledge_db.exists():
        # 正式知识库（Layer 2）存在时，先并入真实知识库实体（seed 只补缺失）。
        # 仅当通过 --knowledge 显式指定（默认构建为 seed-only，见 docs/HISTORY_BACKBONE.md：
        # Evidence 与文本语料等待知识库重建）。
        for table in ("people", "places", "works", "historical_texts", "person_aliases", "entity_source_mapping"):
            connection.execute(f"ATTACH '{_sql_path(real_knowledge_db)}' AS knowledge (READ_ONLY)")
            try:
                connection.execute(f"INSERT OR REPLACE INTO {table} SELECT * FROM knowledge.{table}")
            finally:
                connection.execute("DETACH knowledge")
    for row in people:
        connection.execute("""
            INSERT OR REPLACE INTO people
              (id,canonical_name_zh_cn,name_raw,quality_status,created_from_source,search_name,search_aliases,search_text)
            VALUES (?,?,?,?,?,?,?,?)
        """, [row["id"], row["canonical_name_zh_cn"], row["name_raw"], row["quality_status"],
              row["created_from_source"], row["search_name"], row["search_aliases"], row["search_text"]])
        connection.execute("""
            INSERT OR REPLACE INTO entity_source_mapping (entity_type,entity_id,source_id,external_id,match_type,confidence)
            VALUES ('person',?,?,?,?,?)
        """, [row["id"], CURATED_SOURCE_ID, row["id"], "curated", 1.0])
    for row in places:
        connection.execute("""
            INSERT OR REPLACE INTO places
              (id,canonical_name_zh_cn,historical_name,place_type,source_id,external_id,quality_status)
            VALUES (?,?,?,?,?,?,?)
        """, [row["id"], row["canonical_name_zh_cn"], row["historical_name"], row["place_type"],
              row["source_id"], row["external_id"], row["quality_status"]])
        connection.execute("""
            INSERT OR REPLACE INTO entity_source_mapping (entity_type,entity_id,source_id,external_id,match_type,confidence)
            VALUES ('place',?,?,?,?,?)
        """, [row["id"], CURATED_SOURCE_ID, row["id"], "curated", 1.0])
    for row in works:
        connection.execute("""
            INSERT OR REPLACE INTO works
              (id,title,title_raw,title_zh_cn,source_ids,source_id,quality_status)
            VALUES (?,?,?,?,?,?,?)
        """, [row["id"], row["title"], row["title_raw"], row["title_zh_cn"],
              json.dumps([CURATED_SOURCE_ID], ensure_ascii=False),
              row["source_id"], row["quality_status"]])


def _event_identity(columns: tuple[str, ...]) -> str:
    return hashlib.sha1("|".join(columns).encode("utf-8")).hexdigest()[:24]


def _insert_backbone(connection, backbone: Backbone) -> None:
    event_by_id = {event["id"]: event for event in backbone.events}
    for story in backbone.stories:
        connection.execute("""
            INSERT OR REPLACE INTO stories
              (id,title_zh_cn,title_raw,start_year,end_year,summary_zh_cn,background_zh_cn,result_zh_cn,
               story_type,importance,period_id,period_ids,quality_status,source_type,source_reference,source_ids,usable)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, [
            story["id"], story["title_zh_cn"], story.get("title_raw") or story["title_zh_cn"],
            story.get("start_year"), story.get("end_year"), story.get("summary_zh_cn"),
            story.get("background_zh_cn"), story.get("result_zh_cn"), story.get("story_type"),
            story.get("importance", "major"), story.get("period_id"),
            _json(story.get("period_ids") or [story.get("period_id")]),
            story.get("quality_status", "reviewed"), story.get("source_type", "curated_reference"),
            story.get("source_reference"), _json(story.get("source_ids") or [CURATED_SOURCE_ID]),
            bool(story.get("events")),
        ])
    for event in backbone.events:
        connection.execute("""
            INSERT OR REPLACE INTO events
              (id,name_zh_cn,name_raw,event_type,start_year,start_month,start_day,end_year,end_month,end_day,
               date_precision,period_id,period_ids,regime_id,regime_ids,summary_zh_cn,background_zh_cn,
               result_zh_cn,importance,quality_status,source_type,source_reference,source_ids,search_name,search_text)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, [
            event["id"], event["name_zh_cn"], event.get("name_raw") or event["name_zh_cn"],
            event.get("event_type"), event.get("start_year"), event.get("start_month"), event.get("start_day"),
            event.get("end_year", event.get("start_year")), event.get("end_month"), event.get("end_day"),
            event.get("date_precision"), event.get("period_id"),
            _json(event.get("period_ids") or [event.get("period_id")]), None,
            _json(event.get("regime_ids")), event.get("summary_zh_cn"), event.get("background_zh_cn"),
            event.get("result_zh_cn"), event.get("importance", "major"), event.get("quality_status", "reviewed"),
            event.get("source_type", "curated_reference"), event.get("source_reference"),
            _json(event.get("source_ids") or [CURATED_SOURCE_ID]), event["name_zh_cn"],
            " ".join(filter(None, [event["name_zh_cn"], event.get("summary_zh_cn"), event.get("result_zh_cn")])),
        ])
        for person in event.get("people", []):
            connection.execute("""
                INSERT OR REPLACE INTO event_person
                  (event_id,person_id,role,role_zh_cn,side,importance,description,source_type,source_id,quality_status,
                   link_quality_status,link_confidence,link_reason)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, [
                event["id"], person.get("person_id"), person.get("role", "participant"),
                person.get("role_zh_cn") or person.get("role", "参与者"), person.get("side"),
                person.get("importance", "major"), person.get("description"),
                "curated_reference", person.get("source_id") or CURATED_SOURCE_ID,
                person.get("quality_status", "reviewed"), person.get("link_quality_status"),
                person.get("link_confidence"), person.get("review_note"),
            ])
        for place in event.get("places", []):
            identity = _event_identity((event["id"], place.get("place_id") or "", place.get("place_name_raw", ""), place.get("role", "location")))
            connection.execute("""
                INSERT OR REPLACE INTO event_place
                  (id,event_id,place_id,place_name_raw,role,sequence,description,description_zh_cn,source_type,source_id,
                   quality_status,link_status,link_quality_status,link_confidence,link_reason)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, [
                f"event-place-{identity}", event["id"], place.get("place_id"), place.get("place_name_raw"),
                place.get("role", "location"), place.get("sequence", 1), None, place.get("description_zh_cn"),
                "curated_reference", place.get("source_id") or CURATED_SOURCE_ID,
                place.get("quality_status", "reviewed"), place.get("link_status", "needs_linking"),
                place.get("link_quality_status"), place.get("link_confidence"), place.get("review_note"),
            ])
        for evidence in event.get("evidence", []):
            identity = _event_identity((event["id"], evidence.get("historical_text_id") or "", evidence.get("work", ""), evidence.get("term", "")))
            connection.execute("""
                INSERT OR REPLACE INTO event_evidence
                  (id,event_id,historical_text_id,work,term,chapter_hint,context_keywords,evidence_role,link_status,
                   link_quality_status,link_confidence,review_note,source_type,source_id,quality_status,rejected_text_ids)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, [
                f"event-evidence-{identity}", event["id"], evidence.get("historical_text_id"),
                evidence.get("work"), evidence.get("term"), evidence.get("chapter_hint"),
                _json(evidence.get("context_keywords")), evidence.get("evidence_role", "supporting"),
                evidence.get("link_status", "pending_knowledge"), evidence.get("link_quality_status"),
                evidence.get("link_confidence"), evidence.get("review_note"),
                "curated_reference", evidence.get("source_id") or CURATED_SOURCE_ID,
                evidence.get("quality_status", "reviewed"), _json(evidence.get("rejected_text_ids")),
            ])
        # outgoing relations 以本 event 为 source
        for relation in event.get("relations", []):
            connection.execute("""
                INSERT OR REPLACE INTO event_relations
                  (source_event_id,target_event_id,relation_type,confidence,description_zh_cn,source_type,source_id,source_ids,quality_status)
                VALUES (?,?,?,?,?,?,?,?,?)
            """, [
                event["id"], relation["target_event_id"], relation["relation_type"],
                relation.get("confidence"), relation.get("description_zh_cn"),
                "curated_reference", relation.get("source_id") or CURATED_SOURCE_ID,
                _json(relation.get("source_ids") or [CURATED_SOURCE_ID]),
                relation.get("quality_status", "reviewed"),
            ])
    # story_events
    for story in backbone.stories:
        for item in story.get("events", []):
            connection.execute("""
                INSERT OR REPLACE INTO story_events
                  (story_id,event_id,sequence,role,importance,transition_text_zh_cn,quality_status)
                VALUES (?,?,?,?,?,?,?)
            """, [
                story["id"], item["event_id"], item.get("sequence"), item.get("role"),
                item.get("importance", "major"), item.get("transition_text_zh_cn"), "reviewed",
            ])


def _materialize_legacy_event_text(connection) -> None:
    """Legacy 兼容：event_evidence → event_text（旧表名）。dist 主数据源是 event_evidence。

    仅镜像已锚定历史文本的证据（historical_text_id 非空）：event_text 以
    (event_id, historical_text_id) 为主键，无法表达尚未关联具体文本的证据；
    此类（含 pending_knowledge / needs_linking 状态的）证据完整保留于 event_evidence。
    """
    connection.execute("""
        INSERT OR REPLACE INTO event_text
          (event_id,historical_text_id,role,sequence,description_zh_cn,source_type,source_id,quality_status,
           source_quality_status,link_quality_status,link_confidence,link_reason)
        SELECT event_id,historical_text_id,evidence_role,1,coalesce(review_note,''),source_type,source_id,
               quality_status,'source_backed' AS source_quality_status,link_quality_status,link_confidence,review_note
        FROM event_evidence
        WHERE historical_text_id IS NOT NULL
    """)


def _insert_supplemental_persons(connection, root: Path) -> None:
    """V2.1.1 · 写入补充 Person（people + person_aliases + entity_source_mapping）。"""
    people, aliases = supplemental_person_rows(root)
    for row in people:
        connection.execute("""
            INSERT OR REPLACE INTO people
              (id,canonical_name_zh_cn,name_raw,traditional_name,birth_year,death_year,
               birth_precision,death_precision,gender,period_ids,intro_zh_cn,quality_status,
               created_from_source,search_name,search_aliases,search_text)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, [
            row["id"], row["canonical_name_zh_cn"], row["name_raw"], row["traditional_name"],
            row["birth_year"], row["death_year"], row["birth_precision"], row["death_precision"],
            row["gender"], row["period_ids"], row["intro_zh_cn"], row["quality_status"],
            row["created_from_source"], row["search_name"], row["search_aliases"], row["search_text"],
        ])
        sid = row["source_id"]
        connection.execute("""
            INSERT OR REPLACE INTO entity_source_mapping (entity_type,entity_id,source_id,external_id,match_type,confidence)
            VALUES ('person',?,?,?,?,?)
        """, [row["id"], sid, row["id"], "curated", 1.0])
    for a in aliases:
        connection.execute("""
            INSERT OR REPLACE INTO person_aliases (person_id,alias,alias_zh_cn,alias_type,source,source_id,external_id)
            VALUES (?,?,?,?,?,?,?)
        """, [a["person_id"], a["alias"], a["alias_zh_cn"], a["alias_type"], a["source"], a["source_id"], a["external_id"]])


def _build_duckdb(paths, backbone: Backbone, result: ResolutionResult, real_knowledge_db: Path | None) -> Path:
    import duckdb

    from ..database import SCHEMA_SQL

    paths.ensure_dist()
    target = paths.dist_database
    building = target.with_name("history.building.duckdb")
    if building.exists():
        building.unlink()
    connection = duckdb.connect(str(building))
    try:
        connection.execute(SCHEMA_SQL)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS event_evidence (
              id VARCHAR PRIMARY KEY, event_id VARCHAR NOT NULL, historical_text_id VARCHAR,
              work VARCHAR, term VARCHAR, chapter_hint VARCHAR, context_keywords VARCHAR,
              evidence_role VARCHAR NOT NULL, link_status VARCHAR, link_quality_status VARCHAR,
              link_confidence DOUBLE, review_note VARCHAR, source_type VARCHAR, source_id VARCHAR,
              quality_status VARCHAR, rejected_text_ids VARCHAR
            )
        """)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS event_evidence_candidates (
              event_id VARCHAR, historical_text_id VARCHAR, work VARCHAR, term VARCHAR,
              link_quality_status VARCHAR, link_confidence DOUBLE, link_reason VARCHAR,
              PRIMARY KEY(event_id, historical_text_id)
            )
        """)
        connection.execute("CREATE INDEX IF NOT EXISTS idx_event_evidence_event ON event_evidence(event_id)")
        _ensure_sources(connection, paths.root, paths.curated_backbone)
        _insert_taxonomy(connection, backbone)
        _insert_knowledge(connection, result, real_knowledge_db)
        _insert_supplemental_persons(connection, paths.root)
        _insert_backbone(connection, backbone)
        _materialize_legacy_event_text(connection)
        connection.execute("CHECKPOINT")
    finally:
        connection.close()
    if target.exists():
        previous = target.with_name("history.previous.duckdb")
        if previous.exists():
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            archived = target.with_name(f"history.previous.{stamp}.duckdb")
            previous.replace(archived)
        target.replace(previous)
    os.replace(building, target)
    return target


def _table_count(connection, table: str) -> int:
    try:
        return int(connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0])
    except Exception:
        return 0


def export_parquet(database: Path, output_dir: Path, tables: tuple[str, ...] = ()) -> int:
    import duckdb

    output_dir.mkdir(parents=True, exist_ok=True)
    tables = tables or tuple(BACKBONE_TABLES) + KNOWLEDGE_TABLES
    count = 0
    with duckdb.connect(str(database), read_only=True) as connection:
        for table in tables:
            try:
                row_count = connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            except Exception:
                continue
            if row_count == 0 and table not in ("event_text_candidates", "event_evidence_candidates", "person_aliases"):
                continue
            target = output_dir / f"{table}.parquet"
            temporary = output_dir / f".{table}.parquet.tmp"
            connection.execute(f"COPY {table} TO ? (FORMAT PARQUET, COMPRESSION ZSTD)", [str(temporary)])
            os.replace(temporary, target)
            count += 1
    return count


def export_json(database: Path, output_dir: Path) -> int:
    import duckdb

    output_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    with duckdb.connect(str(database), read_only=True) as connection:
        for name, sql in EXPORT_JSON_GROUPS.items():
            rows = connection.execute(sql).fetchall()
            columns = [item[0] for item in connection.execute(sql).description]
            records = [dict(zip(columns, row)) for row in rows]
            target = output_dir / f"{name}.json"
            target.write_text(json.dumps(records, ensure_ascii=False, indent=1, default=str) + "\n", encoding="utf-8")
            count += len(records)
    return count


def write_manifest(paths, backbone: Backbone, result: ResolutionResult, database: Path, version: str,
                   built_at: str, commit: str | None) -> dict[str, Any]:
    import duckdb

    with duckdb.connect(str(database), read_only=True) as connection:
        counts = {
            "periods": _table_count(connection, "periods"),
            "regimes": _table_count(connection, "regimes"),
            "events": _table_count(connection, "events"),
            "stories": _table_count(connection, "stories"),
            "story_events": _table_count(connection, "story_events"),
            "event_relations": _table_count(connection, "event_relations"),
            "event_people": _table_count(connection, "event_person"),
            "event_places": _table_count(connection, "event_place"),
            "event_evidence": _table_count(connection, "event_evidence"),
            "people": _table_count(connection, "people"),
            "places": _table_count(connection, "places"),
            "works": _table_count(connection, "works"),
            "historical_texts": _table_count(connection, "historical_texts"),
            "sources": _table_count(connection, "sources"),
            "entity_source_mapping": _table_count(connection, "entity_source_mapping"),
        }
    manifest = {
        "version": version,
        "data_version": version,
        "built_at": built_at,
        "git_commit": commit,
        "build_commit": commit,
        "pipeline": "history-data backbone build",
        "counts": counts,
        "summary_counts": {
            "period_count": counts["periods"],
            "regime_count": counts["regimes"],
            "event_count": counts["events"],
            "critical_count": sum(1 for e in backbone.events if e.get("importance") == "critical"),
            "major_count": sum(1 for e in backbone.events if e.get("importance") == "major"),
            "story_count": counts["stories"],
            "relation_count": counts["event_relations"],
            "source_count": counts["sources"],
        },
        "coverage_by_layer": {
            "layer1_source": {"raw_snapshots": len(list((paths.raw).glob("*/*")) ) if paths.raw.exists() else 0},
            "layer2_knowledge": {key: counts[key] for key in ("people", "places", "works", "historical_texts", "sources", "entity_source_mapping")},
            "layer3_backbone": {key: counts[key] for key in ("periods", "regimes", "events", "stories", "story_events", "event_relations", "event_people", "event_places", "event_evidence")},
        },
        "reference_resolution": {
            "knowledge_available": result.knowledge_available,
            "persons": result.persons,
            "places": result.places,
            "evidences": result.evidences,
            "broken": len(result.broken),
            "pending": len(result.pending),
        },
        "by_period_group": _coverage_by_group(backbone),
    }
    paths.dist.mkdir(parents=True, exist_ok=True)
    paths.dist_manifests.mkdir(parents=True, exist_ok=True)
    (paths.dist / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (paths.dist_manifests / f"manifest-{version}.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def _coverage_by_group(backbone: Backbone) -> dict[str, dict[str, int]]:
    from .loader import PERIOD_DIR_HINTS

    groups = ("pre_qin", "chunqiu_zhanguo", "qin_han", "three_kingdoms", "jin_southern_northern",
              "sui_tang", "five_dynasties", "song_liao_xia_jin", "yuan", "ming", "qing", "modern")
    coverage = {group: {"events": 0, "stories": 0} for group in groups}
    for event in backbone.events:
        period_id = event.get("period_id", "")
        group = PERIOD_DIR_HINTS.get(period_id, "pre_qin")
        if group in coverage:
            coverage[group]["events"] += 1
    story_groups = {"qin_han", "three_kingdoms", "sui_tang"}
    for story in backbone.stories:
        period_id = story.get("period_id", "")
        group = PERIOD_DIR_HINTS.get(period_id, "pre_qin")
        if group in coverage:
            coverage[group]["stories"] += 1
    return coverage


def build_backbone(paths, knowledge_db: Path | None = None) -> dict[str, Any]:
    """完整 pipeline：load → validate（Gate）→ resolve（Gate）→ build → export → manifest。"""
    backbone = load_backbone(paths.root)
    errors = validate_backbone(backbone, paths.root)
    check_strict_gate(backbone, errors, paths.root)
    result = resolve_references(backbone, knowledge_db)
    if result.broken:
        raise RuntimeError(
            "Reference Resolution Gate 失败（构建终止）：\n  " + "\n  ".join(result.broken[:50])
        )
    version = read_data_version(paths.root)
    built_at = _now()
    commit = git_commit(paths.root)
    database = _build_duckdb(paths, backbone, result, knowledge_db)
    export_parquet(database, paths.dist_parquet)
    export_json(database, paths.dist_json)
    # China History Backbone V1：Major Timeline（critical+major，按 start_year 排序）
    from .timeline import write_major_timeline_json

    write_major_timeline_json(paths.dist_json, backbone, version)
    manifest = write_manifest(paths, backbone, result, database, version, built_at, commit)
    return manifest