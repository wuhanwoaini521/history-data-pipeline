# Person Linking V1 风险复核（与 V2.3 汇入）

## 术语纪律

- 机器 = V2.2 `machine_candidate` → `machine_recommend`；本层 = `agent_assisted_review`；
- 只有经过 V2.3 agent 逐条复核且 select 接受者标记 `curated_class=curated_accepted`，进入正式 Backbone。
- 严禁把 agent_assisted 写成 `human_reviewed`；human 复核门留待 V2.4（未执行）。

## 已知风险 / 已知缺口

- agent 拒绝链接数: 13；原因分布: {'背景引用': 11, '相邻事件': 2}
- insufficient 数: {len(insufficient)}
- 知识库缺口: 若干事件主角未在 KB 中单独成 entity（如 隋炀帝 于 event-yangguang-jiwei、徐达 于北征等），formal 层以既有 person 就近承接，见 scope 报告。
- 同名/异代（如 贾南风 采用补充 Person table 唯一 ID；王世充见）—已在 identity evidence 注释。

## 审计项

- 覆盖: 全部 machine 链接均被裁决（assert total_machine==total_review）。
- 正式层不写源 machine；machine 层文件未被修改（只读）。
- V1 冻结（events=618 / 既有 event_person=200）不受影响；V2.3 新增文件仅追加。
