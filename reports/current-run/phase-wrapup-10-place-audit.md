# Phase Wrap-up · Q10 — Place Final Audit

- event_place（YAML places 登记）：**308**
- 同名重复（同事件内 place_name_raw 重复）：**0**
- 规范地名表重复（places 表 name 重复）：**0**
- dangling place：**0**（event_place 表全部行均可回溯到事件或规范地名表）

## 结论

- 同事件同名地点重复为 0（历轮出现的「同名地点重复」问题在本轮审计中未复现）。
- 历史地名与现代地名未混用：YAML 中 place_name_raw 一律用历史地名，modern mapping 交由 canonical places 表；needs_linking 为合法状态。
- 本轮未新增 place 去重操作（无重复可去）。