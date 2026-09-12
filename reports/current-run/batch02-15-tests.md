# Batch 02 · Queue 15 — Full Validation

> 环境：AppImage binfmt 破坏 venv prefix（overnight-10 已知）→ `uv sync --frozen` 生成 `.venv-batch02`，
> 以 uv cpython 3.11.14 + `PYTHONPATH=src:.venv-batch02/lib/python3.11/site-packages` 运行。

## 测试结果

| 套件 | 命令 | 结果 |
|---|---|---|
| Python 全量 | `pytest tests/ -q` | **249 passed / 16 skipped / 0 failed**（253s） |
| — 其中新增 parser 测试 | `pytest tests/test_knowledge_wikisource.py` | **13 passed** |
| Rust workspace | `cargo test --workspace`（self-tools） | **200 passed / 0 failed**（31 application + 70 core + 99 infrastructure） |
| Frontend typecheck | `npx tsc --noEmit`（apps/desktop/ui） | **exit 0** |

16 skip = legacy 全量 Layer-2 测试（需 CBDB/CText raw 数据，本机无）——与 overnight-10 一致，属预期。

## 本轮修的测试（硬编码计数过时；数据合法增长，非实现 bug）

| 测试 | 变化 | 原因 |
|---|---|---|
| test_backbone.py::test_resolution_linked_places | needs_linking 34 → 49 | +15 条 Queue 10/12 Critical 富化地点 |
| test_backbone.py::test_resolution_no_broken | pending 120 → 150 | +30 条 Queue 10 段落锚 evidence（knowledge_db=None 降级口径不变） |
| test_backbone_build.py::test_backbone_build | relations 1057 → 1065；place 37 → 52；evidence 154 → 184 | Queue 2 策展 +8 关系；Queue 10/12 +15 地点；Queue 10 +30 证据 |
| test_backbone_build.py::test_dist_evidence_rows_are_reviewed | anchored 计数改为 DISTINCT (event_id, historical_text_id) | Queue 10 起 claim_field 粒度：同段落锚可支撑多 claim_field（evidence 多行、legacy 镜像一行） |

## 本轮修的实现（发现即修，均有测试覆盖）

| 实现 | 问题 | 修复 |
|---|---|---|
| backbone/build.py（evidence identity） | identity 不含 claim_field，同段落多 claim 证据行合并 | identity 加入 claim_field（Queue 10） |
| backbone/evidence_link.py（apply_links） | 自动重算覆盖 manual 段落锚（Queue 9 事故） | 跳过 `link_method == 'manual'` 行（Queue 9/11） |
| knowledge_wikisource.py（parser） | 多行模板泄漏 / HTML CSS・[编辑] 残留 / `[[Category:]]` 剥离后漏出 | 整文级模板收敛、style/editsection 剥离、命名空间复检（Queue 6/7/10） |

## 新增 source 专项验证（Queue 15 要求）

| 检查 | 结果 |
|---|---|
| deterministic build（连续两次 knowledge build） | texts=730,478 两次一致；id 集合 SHA1 摘要 `beaf13401c111535` 两次一致（当时 350 行；现 362 行为五四页 + 壹號页转正后口径） |
| source metadata 完整 | `data/raw/wikisource/20260912/metadata.json`：source_id/dataset/version/license/acquired_at/manifest/pages[].sha256 齐全 |
| license present | `sources` 表 `source-wikisource` license = 底本逐页判定字符串；manifest 逐页 pd_reason |
| checksum present | `checksum.sha256` 逐文件 sha256；复核 **10/10 verified** |
| parser tests | 新增 `tests/test_knowledge_wikisource.py` ×13 |
| data integrity | dangling evidence anchors **0**；dangling relation targets **0**；历史文本/事件/证据 ID 全域唯一；event_text legacy 镜像与锚点 DISTINCT 对一致（148==148） |

## 重要运行顺序说明（本轮发现）

`test_backbone_build.py` 会调用 `build_backbone(paths)` 直接重建 `dist/history.duckdb`（seed-only，
不含知识层）。因此**测试套件跑完后必须重新执行**：

```bash
history-data backbone --knowledge data/normalized/history.duckdb build
```

本轮已执行并复核：dist historical_texts=730,490、event_evidence=184、event_relations=1065、
dangling=0。下次批次的 CI/运行清单应将「tests → --knowledge rebuild → coverage 报告」固定为顺序。
