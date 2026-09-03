# CONTRIBUTING_DATA（贡献数据指南）

本仓库是中国历史的数据 Source of Truth。新增/修改**Event**、**Story**、
**Person/Place/HistoricalText 关联**都必须遵守本流程。

## 0. 铁律

1. **Event > Story**：先有经过确认的 Event，再组织 Story。
2. **Knowledge Store 不生成历史**：禁止
   `HistoricalText → 关键词匹配 → 自动生成 Event`，也禁止
   `Person + Place + Text → 自动拼 Story`。
3. **错误链接比 NULL 更严重**：不确定就
   `person_name_raw + person_id: null + link_status: needs_linking`。
4. **Candidates 永不直接进入正式 Backbone**：必须先 review。
5. **DuckDB 是构建产物**：改数据只能改 YAML/Review，然后重新 build。

## 1. 新增一个 Event（例如赤壁之战）

**Event YAML**：`data/curated/history_backbone/events/<时期目录>/<event_id>.yml`

```yaml
id: event-chibi
name_zh_cn: 赤壁之战
event_type: war
start_year: 208
end_year: 208
date_precision: year
period_id: period-late-eastern-han
regime_ids: []
importance: major
summary_zh_cn: 东汉末年曹操南下过程中与孙权、刘备联军发生的重要战役。
quality_status: reviewed
people:
  - {person_id: null, person_name_raw: 曹操, role: commander, link_status: needs_linking}
places:
  - {place_id: null, place_name_raw: 赤壁, role: 战场, link_status: needs_linking}
evidence:
  - {work: 三国志, term: 赤壁, evidence_role: primary, link_status: pending_knowledge}
relations:
  - {target_event_id: event-xxx, relation_type: leads_to, confidence: 0.8}
```

标准工作流（第十节）：

```text
1. 新增 Event YAML
2. history-data backbone validate          # 通过后再继续
3. 查 Person Candidate（data/candidates/event_person/）
4. 人工确认 Person → 填 person_id + link_status: linked
5. 查 Place Candidate（data/candidates/event_place/）
6. 人工确认 Place → 填 place_id + link_status: linked
7. 查 HistoricalText Candidate（data/candidates/event_evidence/）
8. Review Evidence → link_status: linked / pending_knowledge + review_note
9. history-data backbone build
10. history-data backbone qa + pytest
11. commit
```

**（3）–（8）中任何一步无法确认，就保留 `link_status: needs_linking`，
不要强行匹配。**

## 2. 新增 Story

`data/curated/history_backbone/stories/<时期目录>/<story_id>.yml`

```yaml
id: story-chu-han
title_zh_cn: 楚汉争霸
period_id: period-qin
start_year: -209
end_year: -202
story_type: political-military
importance: major
events:
  - {event_id: event-julu, sequence: 1}
  - {event_id: event-gaixia, sequence: 2}
```

- Story 顺序是 **curated editorial layer**，允许人工整理；
- `sequence` 必须连续正整数且唯一；
- 引用的 Event 必须已存在于 `events/`。

## 3. 修改 Event

- 只改 YAML（不手动 UPDATE DuckDB）；
- 改完跑 `backbone validate` + `backbone build`；
- 如果有争议，先在 `data/reviews/pending/` 挂 review 记录，结论写入
  `data/reviews/accepted|rejected/`，再改正式 YAML。

## 4. 关联 Person / Place / HistoricalText

| 目的 | 去哪里 | 状态 |
|---|---|---|
| Person 关联 | Event YAML `people[]` | `link_status: linked | needs_linking` |
| Place 关联 | Event YAML `places[]` | 同上（place_id 只允许 knowledge.place.id）|
| 史料证据 | Event YAML `evidence[]` | `evidence_role: primary \| supporting \| related` |
| 自动候选 | `data/candidates/event_*` | 永远 `candidate`，需 review |

## 5. 提交 Review

```text
history-data backbone validate --json   # 看当前错误与引用状态
history-data backbone qa                # 看 person/place/evidence 解析统计
```

Review 决策文件：

```jsonc
{
  "review_status": "accepted",        // 或 rejected / pending
  "decision": "...",
  "review_note": "对照三国志·周瑜传……",
  "reviewed_by": "<你的名字>"
}
```

写入 `data/reviews/accepted/<event_id>.review.json` 或
`data/reviews/rejected/<event_id>.review.json`。

## 6. 重建与发布

```bash
history-data backbone validate
history-data backbone build     # 生成 dist/history.duckdb + manifest + parquet/json
history-data backbone coverage  # 更新 reports/BACKBONE_COVERAGE.md
pytest
```

发布详见 `docs/RELEASE_PROCESS.md`。