"""Backbone 数据加载：从 data/curated/history_backbone/ 读取全部 YAML。"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

EVENT_PERIOD_DIRS = (
    "pre_qin", "chunqiu_zhanguo", "qin_han", "three_kingdoms", "jin_southern_northern",
    "sui_tang", "five_dynasties", "song_liao_xia_jin", "yuan", "ming", "qing", "modern",
)

# Period id 前缀 → 事件目录（只为校验目录归属提供参考，不强制）。
PERIOD_DIR_HINTS: dict[str, str] = {
    "period-antiquity": "pre_qin",
    "period-xia": "pre_qin",
    "period-shang": "pre_qin",
    "period-western-zhou": "pre_qin",
    "period-spring-autumn": "chunqiu_zhanguo",
    "period-warring-states": "chunqiu_zhanguo",
    "period-qin": "qin_han",
    "period-western-han": "qin_han",
    "period-xin": "qin_han",
    "period-eastern-han": "qin_han",
    "period-late-eastern-han": "three_kingdoms",
    "period-three-kingdoms": "three_kingdoms",
    "period-western-jin": "jin_southern_northern",
    "period-eastern-jin": "jin_southern_northern",
    "period-sixteen-kingdoms": "jin_southern_northern",
    "period-northern-southern": "jin_southern_northern",
    "period-sui": "sui_tang",
    "period-tang": "sui_tang",
    "period-five-dynasties-ten-kingdoms": "five_dynasties",
    "period-northern-song": "song_liao_xia_jin",
    "period-southern-song": "song_liao_xia_jin",
    "period-liao": "song_liao_xia_jin",
    "period-western-xia": "song_liao_xia_jin",
    "period-jin": "song_liao_xia_jin",
    "period-song-liao-jin": "song_liao_xia_jin",
    "period-yuan": "yuan",
    "period-ming": "ming",
    "period-qing": "qing",
    "period-late-qing": "qing",
    "period-republic": "modern",
    "period-modern": "modern",
}


def read_yaml(path: Path) -> Any:
    if yaml is None:
        raise RuntimeError("缺少 PyYAML，请安装 history-data-pipeline/requirements.txt")
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


@dataclass
class Backbone:
    root: Path
    taxonomy_dir: Path
    periods: list[dict[str, Any]] = field(default_factory=list)
    regimes: list[dict[str, Any]] = field(default_factory=list)
    event_types: list[dict[str, Any]] = field(default_factory=list)
    relation_types: list[dict[str, Any]] = field(default_factory=list)
    quality_statuses: list[dict[str, Any]] = field(default_factory=list)
    events: list[dict[str, Any]] = field(default_factory=list)
    stories: list[dict[str, Any]] = field(default_factory=list)

    # ---- 索引 ----
    @property
    def period_ids(self) -> set[str]:
        return {row["id"] for row in self.periods}

    @property
    def regime_ids(self) -> set[str]:
        return {row["id"] for row in self.regimes}

    @property
    def event_ids(self) -> set[str]:
        return {row["id"] for row in self.events}

    @property
    def story_ids(self) -> set[str]:
        return {row["id"] for row in self.stories}

    def event(self, event_id: str) -> dict[str, Any] | None:
        return next((row for row in self.events if row["id"] == event_id), None)

    def story(self, story_id: str) -> dict[str, Any] | None:
        return next((row for row in self.stories if row["id"] == story_id), None)


def _iter_yaml_files(directory: Path) -> list[Path]:
    if not directory.exists():
        return []
    return sorted(path for path in directory.rglob("*.yml") if path.is_file())


def _load_taxonomy(backbone: Backbone) -> None:
    periods_path = backbone.taxonomy_dir / "periods.yml"
    regimes_path = backbone.taxonomy_dir / "regimes.yml"
    event_types_path = backbone.taxonomy_dir / "event_types.yml"
    relation_types_path = backbone.taxonomy_dir / "relation_types.yml"
    quality_status_path = backbone.taxonomy_dir / "quality_status.yml"
    for path, attr, key in (
        (periods_path, "periods", "periods"),
        (regimes_path, "regimes", "regimes"),
        (event_types_path, "event_types", "event_types"),
        (relation_types_path, "relation_types", "relation_types"),
        (quality_status_path, "quality_statuses", "quality_status"),
    ):
        doc = read_yaml(path) if path.exists() else {}
        setattr(backbone, attr, list(doc.get(key, [])))


def _load_events(backbone: Backbone) -> None:
    events_dir = backbone.root / "data" / "curated" / "history_backbone" / "events"
    for path in _iter_yaml_files(events_dir):
        doc = read_yaml(path)
        rows = doc.get("events", [doc]) if isinstance(doc.get("events"), list) else [doc]
        for row in rows:
            if isinstance(row, dict) and row.get("id"):
                row["_file"] = str(path.relative_to(backbone.root))
                backbone.events.append(row)


def _load_stories(backbone: Backbone) -> None:
    stories_dir = backbone.root / "data" / "curated" / "history_backbone" / "stories"
    for path in _iter_yaml_files(stories_dir):
        doc = read_yaml(path)
        rows = doc.get("stories", [doc]) if isinstance(doc.get("stories"), list) else [doc]
        for row in rows:
            if isinstance(row, dict) and row.get("id"):
                row["_file"] = str(path.relative_to(backbone.root))
                backbone.stories.append(row)


def load_backbone(root: Path) -> Backbone:
    """加载完整 Backbone（taxonomy + events + stories）。"""
    taxonomy_dir = root / "data" / "curated" / "history_backbone" / "taxonomy"
    backbone = Backbone(root=root, taxonomy_dir=taxonomy_dir)
    _load_taxonomy(backbone)
    _load_events(backbone)
    _merge_external_event_person(backbone)
    _load_stories(backbone)
    return backbone


def _merge_external_event_person(backbone: Backbone) -> None:
    """V2.1：并入独立 V2 层 Accepted EventPerson（data/curated/history_backbone/event_person/）。

    V1 Event YAML（events/）保持冻结；本层为 V2 扩展源。同一 (event_id, person_id)
    以内联为主、外部为补（不重复插入）。
    """
    store_dir = backbone.root / "data" / "curated" / "history_backbone" / "event_person"
    if not store_dir.exists():
        return
    by_id = {row["id"]: row for row in backbone.events}
    for path in _iter_yaml_files(store_dir):
        doc = read_yaml(path)
        eid = doc.get("event_id")
        if eid not in by_id:
            continue
        existing = {p.get("person_id") for p in (by_id[eid].get("people") or [])}
        people = by_id[eid].setdefault("people", [])
        for person in doc.get("people", []):
            if person.get("person_id") and person["person_id"] not in existing:
                # V1 event.schema.json 冻结：只并入 schema 兼容字段；
                # identity/event_evidence/resolution 等完整性字段保留在 store 与 reviews（§55 provenance）。
                inline = {k: person[k] for k in (
                    "person_id", "person_name_raw", "role", "role_zh_cn", "side", "importance",
                    "link_status", "link_quality_status", "link_confidence", "review_note"
                ) if k in person}
                inline["review_note"] = (inline.get("review_note") or "") + f" [V2 source={path.name}]"
                people.append(inline)
                existing.add(person["person_id"])