# CONTENT_DEPTH_REPORT — Content Depth Gate V1（Major Batch 02 + Depth Sprint 01 后）

> 工具：`scripts/content_depth_gate_v1.py`（audit-only，不改 schema、不改 canonical 数据）
> 原始数据：`reports/current-run/content-depth-gate-v1.json`；队列：`reports/current-run/DEPTH_ENRICHMENT_QUEUE.json`
> 生成时点：Major Batch 02（30 新 Major）+ Content Depth Sprint 01（20 事件）完成后

## 1. 门禁定义（V1，透明可重复）

12 分制，仅对 coverage=100（FULL）事件评级：

| 维度 | STRONG(2) | ADEQUATE(1) | WEAK(0) |
|---|---|---|---|
| background / process / result / impact | 长度≥90 且 阶段数≥3 | ≥40 且 ≥2 | 其余 |
| evidence（核心 claim_field 覆盖数） | ≥4 | 3 | ≤2 |
| context（relations 数） | ≥2 | 1 | 0 |

总判：`pts≥8 且 process/impact/evidence 非 WEAK → STRONG`；`pts≥5 → ADEQUATE`；否则 `CONTENT_DEPTH_LOW`。
（阶段数 = 以 。；：— 切分后 ≥6 字的片段数；不写字数硬性阈值以外的规则。）

## 2. 总览（baseline → now）

| 状态 | 基线（Batch01 后） | 现在 | 变化 |
|---|---|---|---|
| STRONG | 20 | **70** | +50（新 Major 30 + Depth Sprint 20） |
| ADEQUATE | 111 | 92 | −19（20 深度事件升 STRONG，1 LOW 升 ADEQUATE） |
| CONTENT_DEPTH_LOW | 20 | 19 | −1 |
| INCOMPLETE（coverage<100） | 467 | 437 | −30（30 新 Major 达 100） |
| **FULL（coverage=100）** | **151** | **181** | **+30** |

全局：618 事件；coverage mean 47.5；FULL 占比 29.3%。

## 3. Depth Sprint 01（20 事件，全部 STRONG）

| 组 | 事件 | 结果 |
|---|---|---|
| D1 先秦秦汉 | 秦灭六国 / 秦统一 / 三家分晋 / 七国之乱 / 漠北之战 | 20/20 → STRONG（四段均≥90） |
| D2 晋群 | 八王之乱 / 东晋建立 / 晋灭吴 / 西晋灭亡 / 永嘉之乱 | 同上 |
| D3 南北朝隋 | 北魏分裂 / 北周灭北齐 / 侯景之乱 / 隋灭陈 | 同上 |
| D4 唐宋明 | 后梁代唐 / 陈桥兵变 / 靖康之变 / 崖山海战 / 土木堡之变 / 萨尔浒之战 | 同上 |

做法（不使用 summary 拆句、不机械扩写）：
1. 诊断：四段长度/阶段数 + claim_field 覆盖 + relations 数；
2. 在既有语料中检索补锚（史记/汉书/通鉴/三国志—隋书—明史一线），共新增 evidence 118 条（含 claim_field）；
3. 以新增锚点重写四段为阶段化叙事（每段可回溯到具体段落锚）；
4. 补 context relations（causes/leads_to/follows 等）；
5. 复跑门禁复评。

## 4. 反注水验证（Q10）

- **summary 拆句检查**：全库 618 事件，四段中任一段与 summary 逐字相同者 **0**；
- **跨段重复检查**：同一事件四段互为重复者 **0**；
- **综述性修复**：本批发现 4 个 legacy 事件（第一次鸦片战争/清帝退位/三藩之乱/武昌起义）的 background 与 result 为同一段（summary 拆句残留），已按既有锚点重写为「背景/结果」二段并保留原始证据，复检通过；
- Impact 段不出现「具有重要意义/产生深远影响/促进历史发展」类空话（专项 grep 0 命中，见 §6 校验命令）。

## 5. 剩余深度队列（DEPTH_ENRICHMENT_QUEUE.json）

- LOW 19：qin 7（北击匈奴/南征百越/始皇崩/书同文/统一度量衡/修长城/沙丘之变）+ Han 系 6 + 三国-唐 6（详见队列 JSON）；
- ADEQUATE 92：western-han 30 为最大块（多为人物/制度短事件），tang 12、ming 8、eastern-han 8 次之；
- 队列已按 importance（critical>major）+ 不足分排序，可直接作为 Depth Sprint 02 的输入。

## 6. 校验命令（可重复）

```bash
python scripts/content_depth_gate_v1.py --detail      # 复算门禁 + LOW 明细
python scripts/anchor_lookup.py <work> <regex>        # 语料锚点定位（audit-only）
python scripts/para_dump.py <work> <chapter> --from N --to M
grep -rn "具有重要意义\|产生深远影响\|促进历史发展" data/curated/history_backbone/events | wc -l   # 期望 0 命中（impact 空话）
```

## 7. 结论

- Content Depth Gate V1 的 STRONG 档从 20 提升到 70，ADR 与 LOW 显著下降；
- 全库 FULL 事件（100 分）中 STRONG 占比 70/181 = 38.7%（基线 20/151 = 13.2%）；
- 门禁保持 audit-only，未改 canonical schema；后续批次可直接以队列 JSON 继续收敛 ADEQUATE/LOW。
