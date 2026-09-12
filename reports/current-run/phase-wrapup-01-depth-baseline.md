# Phase Wrap-up · Q1 — Depth Metrics Rebuild（真实复算，不用旧报告数字）

工具：`scripts/content_depth_gate_v1.py`（audit-only）；原始数据 `content-depth-gate-v1.json`。

## 总览

| 状态 | 数量 |
|---|---|
| FULL（coverage=100） | 181 |
| STRONG | 70 |
| ADEQUATE | 92 |
| CONTENT_DEPTH_LOW | 19 |
| INCOMPLETE | 437 |

## 维度弱点统计（仅 FULL 事件）

| 维度 | WEAK 数 | 备注 |
|---|---|---|
| background | 53 | LOW 事件占 17 |
| process | 64 | 最主要短板（叙事无阶段化） |
| result | 89 | 最多——多数事件 result 未与 summary 分离 |
| impact | 21 | 相对最好 |
| evidence（核心 claim_field <3） | 0 | 证据层健康 |
| context（relations=0） | 0 | 无孤立事件 |

## 19 个 CONTENT_DEPTH_LOW（按 pts 排序）

qin 系 7：qin-beiji-xiongnu / qin-nanzheng-baiyue / qin-shihuang-beng / qin-shutongwen / qin-tongyi-duliangheng / qin-xiu-changcheng / shaqiu-zhengbian
战国 3：guiling-zhizhan / likui-bianfa / wuqi-bianfa
汉 3：han-dingdu-changan / han-yuandi-jiwei / hanwudi-jiwei
三国 2：three-guandu / three-north-consolidation
唐 2：anlu-shi-siming / anlu-xuanzong-shu
明 2：lizicheng-gong-beijing / zhuyuanzhang-chendi

分类（Q3）：A 可至 STRONG 15 / B 可至 ADEQUATE 3 / C ADEQUATE_NATURAL 1 / D SOURCE_LIMITED 0（实测后微调，见 Q5 报告）。
