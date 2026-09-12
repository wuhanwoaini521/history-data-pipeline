# Major Batch 01 · Queue 0 — Workspace Closure（Ready-43 提交）

> 执行：2026-09-12 · 项目现有提交风格（feat/chore + 范围 + 摘要）

## Git 状态审计（提交前）

| 仓库 | 状态 |
|---|---|
| self-tools | `main` @ `403d5fd`（与 origin 一致）；除子模块指针外 clean |
| history-data-pipeline | `main` @ `22158dc`；dirty：111 modified + 53 untracked（全部为 Batch 02/Ready-43 产物） |

## 提交前验证（Queue 0.1）

| 检查 | 结果 |
|---|---|
| `backbone validate` | **Validation OK**（periods=31 regimes=64 events=618 stories=3） |
| dangling evidence anchor | **0** |
| dangling relation | **0** |
| duplicate place（YAML 级复查） | **0** |
| duplicate ID（texts/events/evidence） | **0**（733,372 / 618 / 569 全域唯一） |
| event_text mirror mismatch | **0**（503 == 503） |
| targeted tests | 7 passed（validate_clean / resolution / build / 计数） |

## 计数修改的合法性说明（非掩盖失败）

| 断言 | 旧值 → 新值 | 依据 |
|---|---|---|
| event_evidence | 373 → **569** | Ready-43 六 cluster 新增 196 条 manual 锚 |
| event_place | 95 → **145** | Ready-43 新地点登记（-5 去重后） |
| event_relations | 1067 → **1071** | 鼎立形成 +2 / 楚汉余波 +2 |
| pending_knowledge（无 knowledge_db 时） | 359 → **555** | 569 - 14 needs_linking |
| needs_linking places | 92 → **142** | 同上（places 145 = 3 linked + 142） |

以上均为 dist 实测值变化，测试 expectation 同步，不存在隐藏失败。

## 提交记录

| 仓库 | commit | 内容 |
|---|---|---|
| history-data-pipeline | `58538ba` | `feat(history): Batch 02 + Ready-43 - critical closure 60/62, coverage 101 (16.3%), source batch 02`（165 files, +20,687/−6,982） |
| self-tools | `d94e264` | `chore: bump history-data-pipeline to 58538ba (...)` |

- push：先子模块（22158dc..58538ba）后主仓库（403d5fd..d94e264）；无 force push。
- **最终：main repo clean、submodule clean。**

## 附注

- `data/raw/` 依项目策略不入 Git（大数据集由 manifest + acquisition script 重建）；
  新增的 `scripts/acquire_wikisource_batch01/02.py` + `config/wikisource_batch0*.json` +
  `docs/source-acquisition-policy.md` 已入库，快照可离线重建（checksum 随 metadata.json 落盘于 raw 目录）。
- `.venv-batch02/`（本机 AppImage 环境绕行用）已加入 .gitignore，不入库。
