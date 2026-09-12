# Overnight Queue 10 — Full Test Suite

> 原则：不改断言迁就错误；实现 bug 修实现；测试计数过时（数据合法增长）修测试并在此说明。

## 结果总览

| 套件 | 命令 | 结果 |
|---|---|---|
| Python 全量 | `pytest tests/ -q` | **236 passed / 16 skipped / 0 failed**（最终轮；见下方修复说明） |
| Rust workspace | `cargo test --workspace` | **200 passed / 0 failed**（31 + 70 + 99） |
| Frontend typecheck | `npx tsc --noEmit`（apps/desktop/ui） | **exit 0** |

16 个 skip = legacy 全量 Layer-2 测试（需 CBDB/CText raw 数据，本机无；skip 条件已由
前轮从"文件存在"收紧为"存在且含 people"，属预期跳过）。

## 本轮修的测试（均属"硬编码计数过时"，非实现 bug）

| 测试 | 变化 | 原因 |
|---|---|---|
| test_backbone.py::test_resolution_linked_places | needs_linking 23 → 34 | +11 条 overnight-08 source-backed 新地点（needs_linking） |
| test_backbone.py::test_resolution_no_broken | pending 96 → 120 | +24 条 overnight-08 新 evidence 行（seed-only 解析下降级 pending） |
| test_backbone_build.py::test_backbone_build | event_place 26 → 37 | 同地点新增 |
| test_backbone_build.py::test_backbone_build | event_evidence 130 → 154 | +24 条 claim_field 证据（6 事件 × 4 维） |

## 本轮修的实现（Queue 8 过程中发现）

| 实现 | 问题 | 修复 |
|---|---|---|
| build.py `_insert_backbone` | 内联 needs_linking 人物（person_id=null）触发 dist event_person
  主键 NOT NULL 约束 → build 崩溃 | 跳过未解析身份的人物行（name_raw 保留于 curated YAML +
  reference 统计；不伪造 person_id） |

## 前轮遗留修复（commit 22158dc / 本轮早前）

- 依赖环境：本机 AppImage binfmt 破坏 venv prefix → uv python 3.11 + 缓存解包依赖 + PYTHONPATH
- fuzzy-never-links 回归、schema（chapter_anchor/claim_field/link_method）、legacy 测试 skip 收紧、
  v22 NameIndex 回落 dist（详见 knowledge-rebuild-final.md §五）
