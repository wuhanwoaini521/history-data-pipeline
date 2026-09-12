# Major Batch 01 · Queue 10 — Throughput Metrics

## 总吞吐

| 指标 | 值 |
|---|---:|
| selected events | 50 |
| completed events | **50（100%）** |
| ≥90 | 50 |
| 100 分 | **50** |
| blocked / needs_source / needs_review | 0 / 0 / 0 |
| evidence added（manual 锚） | **221** |
| places added（YAML） | 70 |
| people added（YAML, needs_linking） | 90 |
| relations added | 2（楚汉战争聚合事件） |
| source hit rate | **100%**（50/50 selected 均有语料源命中；池层面 433/555 = 78%） |
| average evidence per completed event | **4.4** |
| average new place per event | 1.4 |
| average score gain per event | +77.8（22.2 → 100） |
| 全程 validation errors | 0（过程中修复：claim_field 枚举 2 处；place 重复 5+3+3+1 处） |

## 按 cluster

| cluster | events | >=90 | 100 | evidence | places | relations | blocked |
|---|---:|---:|---:|---:|---:|---:|---:|
| A 战国变法与争霸 | 9 | 9 | 9 | 41 | 13 | 0 | 0 |
| B 秦帝国 | 9 | 9 | 9 | 39 | 14 | 0 | 0 |
| C 楚汉与西汉前期 | 9 | 9 | 9 | 42 | 13 | 2 | 0 |
| D 汉武帝时代 | 9 | 9 | 9 | 40 | 14 | 0 | 0 |
| E 武帝后期与昭宣 | 7 | 7 | 7 | 29 | 8 | 0 | 0 |
| F 东汉 | 7 | 7 | 7 | 30 | 8 | 0 | 0 |

## 效率洞察（供下批参考）

- **生产效率最高的源**：史记（A–D 四 cluster 全部依靠史记主篇 + 少量通鉴/汉书），
  单事件平均 4–5 锚、零 blocked；后汉书（E/F）同样一次通过。
- **最高价值篇目**：商君列传/孙子吴起列传/田单列传/秦始皇本纪/蒙恬列传/高祖本纪/孝文本纪/
  匈奴列传/卫将军骠骑列传/大宛列传/平津侯主父列传 + 汉书武帝纪/董仲舒传/霍光传 + 后汉书光武帝纪/班梁列传/党锢列传。
- **source gap 最大的时期**：中华民国（46 major，0 命中）、晚清（37 major，1 命中）、清（19 major，7 命中）
  ——需 source 层突破（清实录/民国文献许可）。
- **下一批最高效方向**：明（45 READY）、唐（45 READY）、元（28 READY）——语料（明史/旧唐书新唐书通鉴/元史）齐备，
  与 A–F 同机制可直接规模化。
