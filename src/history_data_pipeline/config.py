from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PipelinePaths:
    root: Path

    @property
    def raw(self) -> Path:
        return self.root / "data" / "raw"

    @property
    def staging(self) -> Path:
        return self.root / "data" / "staging"

    @property
    def normalized(self) -> Path:
        return self.root / "data" / "normalized"

    @property
    def exports(self) -> Path:
        return self.root / "data" / "exports"

    @property
    def reports(self) -> Path:
        return self.root / "data" / "reports"

    @property
    def logs(self) -> Path:
        return self.root / "data" / "logs"

    @property
    def database(self) -> Path:
        return self.normalized / "history.duckdb"

    # ---- Layer 3：History Backbone（curated Source of Truth） ----

    @property
    def curated_backbone(self) -> Path:
        return self.root / "data" / "curated" / "history_backbone"

    @property
    def backbone_taxonomy(self) -> Path:
        return self.curated_backbone / "taxonomy"

    @property
    def backbone_events(self) -> Path:
        return self.curated_backbone / "events"

    @property
    def backbone_stories(self) -> Path:
        return self.curated_backbone / "stories"

    # ---- Candidate / Review 流程 ----

    @property
    def candidates(self) -> Path:
        return self.root / "data" / "candidates"

    @property
    def data_reviews(self) -> Path:
        return self.root / "data" / "reviews"

    # ---- Layer 4：Product Exports（应用只读这里） ----

    @property
    def dist(self) -> Path:
        return self.root / "dist"

    @property
    def dist_database(self) -> Path:
        return self.dist / "history.duckdb"

    @property
    def dist_parquet(self) -> Path:
        return self.dist / "parquet"

    @property
    def dist_json(self) -> Path:
        return self.dist / "json"

    @property
    def dist_manifests(self) -> Path:
        return self.dist / "manifests"

    def ensure(self) -> None:
        for path in (self.raw, self.staging, self.normalized, self.exports, self.reports, self.logs):
            path.mkdir(parents=True, exist_ok=True)

    def ensure_dist(self) -> None:
        for path in (self.dist, self.dist_parquet, self.dist_json, self.dist_manifests):
            path.mkdir(parents=True, exist_ok=True)


DATASETS = ("cbdb", "chgis", "ctext", "classical-modern", "wikipedia", "wikisource")
