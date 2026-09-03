# BACKBONE_COVERAGE

> History Backbone 覆盖报告：按时期组统计 Event / Story 数量。
> 目标：一眼看出哪段历史尚未建设；后续 China History Backbone V1 阶段按缺口补齐 Major Event 主干。

## 总览

- Period：31
- Regime：54
- Event：364
- Story：3

## 按时期组

| 时期组 | Events | Stories |
|---|---:|---:|
| 夏商周 | 21 | 0 |
| 春秋战国 | 61 | 0 |
| 秦汉 | 79 | 1 |
| 魏晋南北朝（三国） | 36 | 1 |
| 魏晋南北朝 | 58 | 0 |
| 隋唐 | 84 | 1 |
| 五代十国 | 15 | 0 |
| 宋辽金夏 | 10 | 0 |
| 元 | 0 | 0 |
| 明 | 0 | 0 |
| 清 | 0 | 0 |
| 近现代 | 0 | 0 |

## 按 Period 的重要性分布

| Period | New | Reused | Total | Critical | Major |
| ------ | --: | -----: | ----: | -------: | ----: |
| 夏 | 0 | 4 | 4 | 1 | 3 |
| 商 | 0 | 4 | 4 | 1 | 3 |
| 西周 | 0 | 13 | 13 | 0 | 13 |
| 春秋 | 0 | 24 | 24 | 1 | 23 |
| 战国 | 0 | 37 | 37 | 4 | 33 |
| 秦 | 0 | 14 | 14 | 0 | 14 |
| 西汉 | 0 | 45 | 45 | 2 | 42 |
| 新 | 0 | 6 | 6 | 2 | 4 |
| 东汉 | 0 | 14 | 14 | 1 | 13 |
| 东汉末 | 0 | 22 | 22 | 0 | 22 |
| 三国 | 0 | 14 | 14 | 1 | 13 |
| 西晋 | 0 | 12 | 12 | 4 | 8 |
| 东晋 | 0 | 8 | 8 | 2 | 6 |
| 十六国 | 0 | 13 | 13 | 0 | 13 |
| 南北朝 | 0 | 25 | 25 | 4 | 21 |
| 隋 | 0 | 24 | 24 | 2 | 22 |
| 唐 | 0 | 60 | 60 | 6 | 54 |
| 五代十国 | 0 | 15 | 15 | 2 | 13 |
| 北宋 | 9 | 0 | 9 | 1 | 8 |
| 辽 | 0 | 1 | 1 | 0 | 1 |

## 缺口提示

- 尚无 Event 的时期组：元, 明, 清, 近现代。
- 下一阶段（China History Backbone V1）应优先为这些时期组补齐 critical/major Event。

## 说明

- 本报告由 `history-data backbone coverage` 或 `history-data backbone build` 生成。
- Event 归属按 events/ 目录约定（PERIOD_DIR_HINTS），可在 taxonomy 调整。

## 最新 Manifest

```json
{
  "periods": 31,
  "regimes": 54,
  "events": 364,
  "stories": 3,
  "story_events": 26,
  "event_relations": 643,
  "event_people": 58,
  "event_places": 26,
  "event_evidence": 26,
  "people": 18,
  "places": 3,
  "works": 30,
  "historical_texts": 0,
  "sources": 7,
  "entity_source_mapping": 21
}
```

