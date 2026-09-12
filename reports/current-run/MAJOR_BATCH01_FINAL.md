# History V2 Major Batch 01

> 执行：2026-09-12 · 主题：Major 规模化生产（Critical 收尾后的第一次量产批次）

## Status

**PASS**（50/50 selected 完成；150 milestone 达成；0 数据完整性错误；0 非 source-backed canonical fact）

---

## Git

| 项 | 值 |
|---|---|
| start commit | submodule `58538ba` / main `d94e264`（Queue 0 收尾提交） |
| end commit | submodule `e348903` / main `1f876ab`（gitlink = e348903） |
| workspace status | **main repo clean、submodule clean**（全部已 push，无 force push） |
| 提交节奏 | 1 cluster = 1 commit（A `11caed0` → B `83f7f3e` → C `1671a94` → D `71df504` → E `a89258d` → F `68f282a` → closure `e348903`） |

---

## Batch

```text
selected       = 50
completed      = 50
>=90           = 50
100            = 50
blocked        = 0
needs_source   = 0（批内）
needs_review   = 0（批内）
```

---

## Milestone

```text
complete events:
  Before = 101
  After  = 151

ratio:
  Before = 16.3%
  After  = 24.4%

150 milestone: PASS
```

---

## Evidence

```text
before  = 569（linked 555）
after   = 790（linked 776）
added   = 221 条 manual 段落锚（逐字引文）
```

## Places

```text
before  = 145
after   = 215
added   = 70（YAML，全部 needs_linking + 来源注）
duplicates caught = 0（本批全程 validator 零重复；去重机制延续自 Ready-43 的 5 处修复）
```

## Relations

```text
before  = 1071
after   = 1073
added   = 2（楚汉战争聚合事件 → 鸿门/汉朝建立）
```

## Score

```text
average before = 37.8
average after  = 43.9
（批内 50 事件：22.2 → 100，平均 +77.8/事件）
```

## Coverage（全部 618 events）

| 维度 | Before | After |
|---|---:|---:|
| 背景 | 12.9% | **24.4%** |
| 过程 | 4.7% | **24.4%** |
| 结果 | 14.4% | **24.4%** |
| 影响 | 4.7% | **24.4%** |
| 人物 | 42.9% | **49.7%** |
| 地点 | 10.8% | **24.4%** |
| 证据 | 24.4% | **24.4%** |
| 关联事件 | 98.9% | **99.2%** |

---

## Content Depth

（规则：DEVELOPED = ≥50 字且 ≥2 阶段分隔「。；：—」；只读审计，不改 coverage score）

```text
FULL（100 分）= 151
  ├─ FULL + STRONG            = 43
  └─ FULL + CONTENT_DEPTH_LOW = 108
```

- 本批 50 事件中：3 个 FULL+STRONG，47 个 FULL+CONTENT_DEPTH_LOW（叙述紧凑、单句成分较多，
  待后续批次加深 process/impact 的阶段展开）。**不降 coverage score**，以 `CONTENT_DEPTH_LOW` 单独标记。
- 审计明细：`major01-07-content-depth-audit.md`。

## Cluster Results

| cluster | events | >=90 | 100 | evidence | places | relations | blocked |
|---|---:|---:|---:|---:|---:|---:|---:|
| A 战国变法与争霸 | 9 | 9 | 9 | 41 | 13 | 0 | 0 |
| B 秦帝国 | 9 | 9 | 9 | 39 | 14 | 0 | 0 |
| C 楚汉与西汉前期 | 9 | 9 | 9 | 42 | 13 | 2 | 0 |
| D 汉武帝时代 | 9 | 9 | 9 | 40 | 14 | 0 | 0 |
| E 武帝后期与昭宣 | 7 | 7 | 7 | 29 | 8 | 0 | 0 |
| F 东汉 | 7 | 7 | 7 | 30 | 8 | 0 | 0 |

## Tests

| 套件 | 命令 | 结果 |
|---|---|---|
| Python 全量 | `pytest tests/ -q` | **249 passed / 16 skipped / 0 failed** |
| Rust workspace | `cargo test --workspace` | **200 passed / 0 failed**（31 + 70 + 99） |
| Frontend typecheck | `npx tsc --noEmit` | **exit 0** |

- 唯一 expectation 同步：Rust 语义测试 feishui-zhizhan evidence 3 → 7，已举证为合法数据增长
  （source-batch02 重定位 2 条 + Ready-43 字段锚 4 条 + legacy 1 条，全部 reviewed，无悬空锚）。

## Blockers

| 类型 | 明细 |
|---|---|
| license blocked | 九一八事变、西安事变（冻结，见 major01-01-critical-freeze.md） |
| source missing（整部） | 清实录、明实录、筹办夷务始末、续资治通鉴长编、辛亥革命回忆录（民国/晚清语料层缺口） |
| corpus volume missing | 中华民国 46 major 零命中、晚清 37 major 仅 1 命中、清 19 major 仅 7 命中 |
| manual review required | 14 条 needs_linking（见 source-batch02-result.md）；3 朝北盟会编 term 需人工重述 |
| content depth | 108 个 FULL 事件标记 CONTENT_DEPTH_LOW（含本批 47），待加深 |

## Next Batch（建议，不自动执行）

**Major Batch 02 候选：50 个 READY**（`major01-11-next-candidates.md`）：

| cluster | period | 数量 | 主源 |
|---|---|---:|---|
| G | 唐 | 12 | 旧唐书/新唐书/资治通鉴 |
| H | 明 | 12 | 明史 |
| I | 元 | 10 | 元史 |
| J | 春秋 | 8 | 左传/史记 |
| K | 隋/五代 | 8 | 隋书/旧五代史 |

剩余 READY 总量 = **383**（明 45 / 唐 45 / 元 28 / 战国 24 / 春秋 23 / 隋 22 / 北宋 22 / 南北朝 20 …）——
机制已验证，可按 50/批 持续推进（预期 ≥90 将逐批 +50）。

---

## 报告索引

major01-00-ready43-closure · 01-critical-freeze · 03-selection · 04-cluster-plan · 07-content-depth-audit ·
09-coverage-rebuild · 10-throughput · 11-next-candidates · major01-progress · 本文件。
