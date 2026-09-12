# Overnight Queue 05 — 10 Residual QUARANTINE Re-evaluation

> 重评脚本：`scripts/quarantine_rescore_after_knowledge.py`（确定性、幂等，本轮重跑结果与首评一致）。
> 详细机制见 `reports/current-run/quarantine-after-knowledge-rebuild.md`。

## 逐事件结果（before = 知识层锚定后持久化状态，after = 本轮重算）

| 事件 | before_score | after_score | new_source | new_evidence | linked_chapter | linked_paragraph | final_status |
|---|---:|---:|---|---|---|---|---|
| event-mongol-jianguo 蒙古建国 | 88.7 | 88.7 | 无（维持） | 元史·太祖纪 已锚定 | 本纪/卷一 | p1（章首段） | QUARANTINE |
| event-yuan-jianguo 元朝建立 | 88.7 | 88.7 | 无（维持） | 元史·世祖纪 已锚定 | 本纪/卷四 | p1 | QUARANTINE |
| event-western-xia-jianguo 西夏建国 | 87.7 | 87.7 | 无 | 无（宋史·夏国传不在语料） | — | — | QUARANTINE |
| event-jiuyiba-shibian 九一八事变 | 81.0 | 81.0 | 无 | 无（中华民国史等缺） | — | — | QUARANTINE |
| event-nanjing-datusha 南京大屠杀 | 81.0 | 81.0 | 无 | 无 | — | — | QUARANTINE |
| event-qiqishi-bian 七七事变 | 81.0 | 81.0 | 无 | 无 | — | — | QUARANTINE |
| event-wusi-yundong 五四运动 | 81.0 | 81.0 | 无 | 无 | — | — | QUARANTINE |
| event-xian-shibian 西安事变 | 81.0 | 81.0 | 无 | 无 | — | — | QUARANTINE |
| event-riben-touxiang 日本投降 | 81.0 | 81.0 | 无 | 无 | — | — | QUARANTINE |
| event-xinzhongguo-chengli 新中国成立 | 81.0 | 81.0 | 无 | 无 | — | — | QUARANTINE |

## 结论

- **promoted：0**；**still QUARANTINE：10**；**needs source：7 个 20 世纪事件全部 + 西夏建国**。
- 蒙古/元朝两条已经知识层锚定提分（87.7→88.7），再往上一档需要第二证据章节
  （蒙古秘史/元朝史 章节不可得）→ NEEDS_SOURCE，不硬凑。
- 无人越过 90 阈值，质量门槛未动。

## remaining_missing_fields（全 10 事件共性）

地点、过程、影响均缺失（地点/影响全库性缺口）；20 世纪 7 事件另缺背景/结果章节级证据。

→ 进入 Queue 6。
