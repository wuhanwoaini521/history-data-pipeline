# HISTORY_BACKBONE

History Backbone 是**中国历史主干 Source of Truth**，位于：

```text
data/curated/history_backbone/
├── taxonomy/
│   ├── periods.yml         历史浏览与组织单位（31 个，含上古/辽/西夏/金）
│   ├── regimes.yml         具体政权（31 个，独立于 Period）
│   ├── event_types.yml     事件类型枚举
│   ├── relation_types.yml  事件关系白名单（8 种）
│   └── quality_status.yml  quality/link_status/importance 枚举
├── events/
│   ├── pre_qin/  chunqiu_zhanguo/  qin_han/  three_kingdoms/
│   ├── jin_southern_northern/  sui_tang/  five_dynasties/
│   ├── song_liao_xia_jin/  yuan/  ming/  qing/  modern/
│   └── <event_id>.yml      每个 Event 一个文件
├── stories/
│   └── <period_dir>/<story_id>.yml    Story 只存阅读顺序（StoryEvent）
└── reviews/                 审核记录说明（实际决策在 data/reviews/）
```

## Period 是浏览单位，Regime 是政权

```yaml
# period: 三国
# regimes: 曹魏 / 蜀汉 / 东吴
```

```yaml
# period: 宋辽金时期（或独立 北宋/辽/西夏/金/南宋）
# regimes: 北宋 / 辽 / 西夏 / 金 / 南宋
```

不能继续依赖单一 Dynasty 字段表达中国历史。

## Event 是骨架

Event 表示「相对明确发生过的历史事实节点」（商汤灭夏、巨鹿之战、赤壁之战、
安史之乱…）。优先级：**Event > Story**。

一个 Event YAML 文件例（节选）：

```yaml
id: event-three-chibi
name_zh_cn: 赤壁之战
event_type: war
start_year: 208
end_year: 208
date_precision: year
period_id: period-late-eastern-han
regime_ids: []
importance: major
quality_status: reviewed
people:            # EventPerson
  - person_id: cbdb-person-30257
    person_name_raw: 曹操
    role: commander
    link_status: linked
places:            # EventPlace
  - place_id: null
    place_name_raw: 赤壁
    link_status: needs_linking
evidence:          # EventEvidence（原 EventText）
  - historical_text_id: text-niutrans-01944969510a3280e6a5
    work: 三国志
    term: 赤壁
    evidence_role: primary
    link_status: pending_knowledge
relations:         # EventRelation（source = 本 Event）
  - target_event_id: event-three-regime-formation
    relation_type: leads_to
    confidence: 0.85
```

## Reviewer 流程（Candidate 永远不能直接进入正式 Backbone）

```text
candidate（data/candidates/）
   ↓
review（data/reviews/pending → accepted / rejected）
   ↓
accepted
   ↓
history_backbone（正式 Event/关系写入事件 YAML）
```

## 迁移状态

- 三个 Story（楚汉争霸 / 三国格局形成 / 安史之乱）及其 26 个 Event 已从
  legacy `data/curated/stories.yml` 迁移到本目录（`backbone migrate`）。
- 旧 `stories.yml` 保留为 legacy 审计源，未删除。
- Person/Place 链接沿用 legacy QA 结论（linked / needs_linking）；
  Evidence 等待知识库重建（`pending_knowledge`）。

当前覆盖情况见 `reports/BACKBONE_COVERAGE.md`。