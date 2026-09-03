"""History Backbone —— 中国历史主干 Source of Truth。

Layer 3：Period / Regime / Event / Story 及其桥接（EventPerson / EventPlace /
EventEvidence / EventRelation / StoryEvent）。所有数据来自
`data/curated/history_backbone/` 下的人工整理 YAML。

本模块只加载与组织数据，不负责生成历史：Knowledge Store（Layer 2）可以存在，
但绝不会从这里自动推导 Event / Story。
"""

from .loader import Backbone, load_backbone
from .validate import validate_backbone
from .reference import resolve_references, KnowledgeResolver
from .build import build_backbone, write_manifest, export_parquet, export_json
from .migrate import migrate_legacy_curated
from .coverage import write_backbone_coverage

__all__ = [
    "Backbone",
    "load_backbone",
    "validate_backbone",
    "resolve_references",
    "KnowledgeResolver",
    "build_backbone",
    "write_manifest",
    "export_parquet",
    "export_json",
    "migrate_legacy_curated",
    "write_backbone_coverage",
]