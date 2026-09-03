"""JSON Schema 校验：schemas/*.schema.json 是唯一权威字段定义。

本模块负责：
- 从 schemas/ 加载 JSON Schema；
- 用 jsonschema 校验 backbone 文档/条目；
- 输出 schema 校验错误列表。
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

__all__ = ["load_schemas", "validate_document", "SchemaRegistry", "schema_files"]


SCHEMA_NAMES = (
    "period", "regime", "event", "story",
    "event_relation", "event_person", "event_place", "event_evidence",
)


def schema_files(root: Path) -> dict[str, Path]:
    schemas_dir = root / "schemas"
    files: dict[str, Path] = {}
    for name in SCHEMA_NAMES:
        path = schemas_dir / f"{name}.schema.json"
        if path.exists():
            files[name] = path
    return files


class SchemaRegistry:
    def __init__(self, schemas: dict[str, Any]):
        self.schemas = schemas
        try:
            from jsonschema import Draft202012Validator
            self._validator = Draft202012Validator
            self.available = True
        except ImportError:  # pragma: no cover
            self._validator = None
            self.available = False

    def validate(self, name: str, document: Any) -> list[str]:
        if not self.available:
            return [f"jsonschema 未安装，跳过 {name} Schema 校验"]
        schema = self.schemas.get(name)
        if schema is None:
            return [f"schemas/: 缺少 {name}.schema.json"]
        validator = self._validator(schema)
        messages: list[str] = []
        for error in sorted(validator.iter_errors(document), key=lambda e: list(e.path)):
            path = "/".join(str(part) for part in error.path) or "(root)"
            messages.append(f"{name}: {path}: {error.message}")
        return messages


def load_schemas(root: Path) -> SchemaRegistry:
    import json

    schemas: dict[str, Any] = {}
    for name, path in schema_files(root).items():
        schemas[name] = json.loads(path.read_text(encoding="utf-8"))
    registry = SchemaRegistry(schemas)
    return registry


def validate_document(registry: SchemaRegistry, name: str, document: Any) -> list[str]:
    return registry.validate(name, document)