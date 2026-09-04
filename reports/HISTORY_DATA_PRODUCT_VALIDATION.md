# HISTORY_DATA_PRODUCT_VALIDATION — 数据产品验收报告

- 生成时间: 2026-09-04T07:32:04+00:00
- 模式: DATA VALIDATION MODE · READ ONLY
- Gates: CHINA_HISTORY_BACKBONE_V1_FROZEN=True, PERSON_LINKING_V1_READY=True, HISTORY_DATA_PRODUCT_VALIDATION_READY=True

## 1. 基础层 (Backbone linked data)

| 项目 | 数值 |
| --- | --- |
| Event Count | 618 |
| Critical | 62 |
| Major | 555 |
| Normal | 1 |
| Period Count | 31 |
| Regime Count | 64 |
| Formal EventPerson | 398 (234 个唯一人物) |
| Events With Person | 261 / 618 |
| Events With Place (formal) | 26 / 618 |
| Events With Evidence | 26 / 618 |
| Event Relations | 1062 |
| Events With Relations | 614 / 618 |
| Events With Source | 618 / 618 |
| Timeline Range | 前2070 → 1949 |

## 2. Knowledge Store (原始知识库，尚未全量接入 Backbone)

| 层 | people | person_aliases | places | historical_texts | works | sources |
| --- | --- | --- | --- | --- | --- | --- |
| Knowledge Store | 676427 | 208624 | 31978 | 972467 | 27394 | 6 |
| Backbone linked | 234 | — | 26·行 | 26·事件 | 36 | — |

> 注意: 知识库总量≠已关联。例如 historical_texts=972467 是知识库收录数，实际仅 26 个 Event 有 EventEvidence 关联

## 3. Critical / Major 覆盖率

| Coverage | Critical (62) | Major (555) |
| --- | --- | --- |
| Person linked | 61 / 62 | 199 / 555 |
| Place linked | 0 / 62 | 25 / 555 |
| Evidence linked | 0 / 62 | 25 / 555 |
| Relations | 62 / 62 | 551 / 555 |
| Source | 62 / 62 | 555 / 555 |

## 4. 15 个验收样本 · Product Usefulness (等待用户验收)

| # | Event | Date | Summary | Person | Relation | Source | Product Useful? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 武王伐纣 | 前1046 | 有 | 1 人 | 有 | 47 条 | pending_user_review |
| 2 | 长平之战 | 前260 | 有 | 2 人 | 有 | 22 条 | pending_user_review |
| 3 | 秦统一六国（秦帝国建立） | 前221 | 有 | 2 人 | 有 | 22 条 | pending_user_review |
| 4 | 赤壁之战 | 208 | 有 | 4 人 | 有 | 30 条 | pending_user_review |
| 5 | 淝水之战 | 383 | 有 | 3 人 | 有 | 53 条 | pending_user_review |
| 6 | 玄武门之变 | 626 | 有 | 4 人 | 有 | 57 条 | pending_user_review |
| 7 | 安禄山起兵 | 755 | 有 | 2 人 | 有 | 30 条 | pending_user_review |
| 8 | 靖康之变、北宋灭亡 | 1127 | 有 | 4 人 | 有 | 24 条 | pending_user_review |
| 9 | 崖山海战、南宋灭亡 | 1279 | 有 | 3 人 | 有 | 48 条 | pending_user_review |
| 10 | 鄱阳湖之战、陈友谅覆灭 | 1363 | 有 | 2 人 | 有 | 24 条 | pending_user_review |
| 11 | 土木堡之变 | 1449 | 有 | 3 人 | 有 | 50 条 | pending_user_review |
| 12 | 第一次鸦片战争 | 1840 | 有 | 2 人 | 有 | 53 条 | pending_user_review |
| 13 | 甲午战争（中日战争） | 1894 | 有 | 4 人 | 有 | 53 条 | pending_user_review |
| 14 | 武昌起义 | 1911 | 有 | 2 人 | 有 | 27 条 | pending_user_review |
| 15 | 中华人民共和国成立 | 1949 | 有 | 2 人 | 有 | 26 条 | pending_user_review |

> Agent 不替用户决定; 每行 `Product Useful?` 默认 pending_user_review。

## 5. 重要提示
- Timeline 起止: 前2070 → 1949
- 事件全部有 summary/period/source (见 ANOMALIES 报告扫描确认)

---
本报告由 tools/history-preview/build_preview.py 自动生成 (READ ONLY)。