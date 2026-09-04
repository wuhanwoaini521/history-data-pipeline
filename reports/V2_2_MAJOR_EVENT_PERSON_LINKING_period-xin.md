# V2.2 Major EventPerson Linking — period-xin

- gate: `V2_2_PERIOD_XIN=TRUE`
- major events: 4 | linked: 3 | links: 3 | empty(allowed): 1

| event | event name | links | persons |
|---|---|---|---|
| event-chimei-qiyi | 赤眉起义 | 0 | — |
| event-kunyang-zhizhan | 昆阳之战 | 1 | 王莽 |
| event-lvlin-qiyi | 绿林起义 | 1 | 王莽 |
| event-xin-gaizhi | 王莽改制（新朝制度变革） | 1 | 王莽 |

- 所有链接为 machine exact（时窗唯一）；待 V2.3 人工放行前不进入正式 backbone。
- 空事件 1 个：KB 未命中 / 多候选 / 低置信 / 审阅排除，V2.2 允许 empty EventPerson。
