"""修复 major-batch01 append 引入的重复顶层键（people/evidence）。

根因：append-only 写法在已有 `people:`/`evidence:` 的文件尾部再次追加同名键；
PyYAML last-wins 导致旧列表在解析视图中被遮蔽（dist 丢行）。
修复：按文件文本提取同名键的全部块，合并列表（旧在前、新在后；完全相同的条目去重），
       重写为单键；文件头注释保留。
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
EVENTS = ROOT / "data" / "curated" / "history_backbone" / "events"
LIST_KEYS = ("people", "places", "evidence", "relations")
TOP_KEY_RE = re.compile(r"(?m)^([a-z_]+):")


def split_blocks(text: str) -> list[tuple[str, str]]:
    """→ [(key, block_text)]，block_text 含键行本身。"""
    matches = list(TOP_KEY_RE.finditer(text))
    blocks = []
    for idx, m in enumerate(matches):
        start = m.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        blocks.append((m.group(1), text[start:end]))
    return blocks


def merge_file(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    head_lines = []
    for line in text.splitlines():
        if line.startswith("#") or not line.strip():
            head_lines.append(line)
            continue
        break
    head = "\n".join(head_lines).rstrip() + "\n"
    blocks = split_blocks(text)
    merged: dict[str, list] = {}
    stats = {}
    for key, block in blocks:
        if key not in LIST_KEYS:
            continue
        parsed = yaml.safe_load(block)
        items = parsed.get(key) or []
        bucket = merged.setdefault(key, [])
        for item in items:
            if item not in bucket:
                bucket.append(item)
    # 用 yaml 解析整文档（last-wins），再以合并列表覆盖
    doc = yaml.safe_load(text)
    for key, items in merged.items():
        stats[key] = (len(doc.get(key) or []), len(items))
        doc[key] = items
    body = yaml.safe_dump(doc, allow_unicode=True, sort_keys=False,
                          default_flow_style=False, width=10**6)
    path.write_text(head + body, encoding="utf-8")
    return stats


def main() -> int:
    fixed = 0
    for path in sorted(EVENTS.rglob("event-*.yml")):
        text = path.read_text(encoding="utf-8")
        keys = [m.group(1) for m in TOP_KEY_RE.finditer(text)]
        dups = {k for k in keys if keys.count(k) > 1}
        if not dups:
            continue
        stats = merge_file(path)
        fixed += 1
        print(f"fixed {path.name}: {stats}")
    print(f"total fixed: {fixed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
