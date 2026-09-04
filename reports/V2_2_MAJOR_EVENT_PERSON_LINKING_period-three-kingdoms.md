# V2.2 Major EventPerson Linking — period-three-kingdoms

- gate: `V2_2_PERIOD_THREE_KINGDOMS=TRUE`
- major events: 13 | linked: 7 | links: 7 | empty(allowed): 6

| event | event name | links | persons |
|---|---|---|---|
| event-cao-mao-zhisha | 曹髦被杀（司马昭专权） | 1 | 曹髦 |
| event-gaopingling-zhi-bian | 高平陵之变 | 0 | — |
| event-jiangwei-beifa | 姜维北伐 | 0 | — |
| event-liubei-beng-zhugeliang | 刘备去世、诸葛亮辅政 | 1 | 诸葛亮 |
| event-liubei-chengdi | 刘备称帝、蜀汉建立 | 0 | — |
| event-sunquan-chengdi | 孙权称帝、孙吴建立 | 1 | 孙权 |
| event-three-regime-formation | 三国鼎立格局逐渐形成 | 0 | — |
| event-wei-mie-shu | 魏灭蜀 | 0 | — |
| event-yiling-zhizhan | 夷陵之战 | 0 | — |
| event-zhuge-liang-beifa | 诸葛亮北伐 | 1 | 诸葛亮 |
| event-zhuge-liang-nanzheng | 诸葛亮南征 | 1 | 诸葛亮 |
| event-zhuge-liang-shoubei | 诸葛亮首次北伐（街亭之战） | 1 | 诸葛亮 |
| event-zhuge-liang-zhishi | 诸葛亮病逝五丈原 | 1 | 诸葛亮 |

- 所有链接为 machine exact（时窗唯一）；待 V2.3 人工放行前不进入正式 backbone。
- 空事件 6 个：KB 未命中 / 多候选 / 低置信 / 审阅排除，V2.2 允许 empty EventPerson。
