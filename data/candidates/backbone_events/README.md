# backbone_events Candidates（Batch 1 先秦）

本目录保存 China History Backbone V1 Batch 1 的 Event 候选清单。

- `pre_qin_candidates.yml`：Phase A（上古/夏/商/西周）候选
- `chunqiu_zhanguo_candidates.yml`：Phase B（春秋）+ Phase C（战国）候选

流程：候选（AI 整理，非历史事实来源）→ `data/reviews/accepted/` 人工 review →
accepted 后写入 `data/curated/history_backbone/events/`。
AI 只整理与筛选候选；历史事实依据以 `source_reference` 中列出的古代史料与
现代历史参考为准。
