# Batch 02 · Queue 12 — Places Improvement（仅 Critical）

> 范围：只为本轮 Critical 富化补必要地点；不做全量 places 扩张。
> 规则：区分 historical place / modern place；无可信来源**不猜 coordinates**；不把历史地名全部映射成现代城市。

## 本轮新增地点关联（event_place 37 → 52，全部 needs_linking + 来源注）

| event | place | place_type（历史属性） | role | 来源注（同条写入 review_note） |
|---|---|---|---|---|
| event-western-xia-jianguo | 鄜延 | 宋边路分（历史行政区） | region | 宋史·夏国传上「與諸豪歃血約先攻鄜延」 |
| event-western-xia-jianguo | 延州 | 宋边州城 | battlesite | 同上「破安遠、塞門、永平諸砦，圍延州」 |
| event-western-xia-jianguo | 三川口 | 战场（川口地形） | battlesite | 同上「設伏三川口，執劉平、石元孫」 |
| event-western-xia-jianguo | 五台山 | 山（宗教地） | location | 同上「表遣使詣五臺山供佛寶，欲窺河東道路」 |
| event-qiqishi-bian | 卢沟桥 | 桥/战场（京畿要冲） | battlesite | 對盧溝橋事件之嚴正聲明 p4 |
| event-qiqishi-bian | 北平 | 城市（故都/军事重镇） | city | 同上「百年故都，北方政治文化的中心與軍事重鎮」 |
| event-qiqishi-bian | 冀东 | 区域（伪组织所在） | region | 同上「要擴大冀東偽組織」 |
| event-riben-touxiang | 东京湾 | 海湾（签署地） | location | 降伏文書 p9「簽字於一九四五年九月二日九時四分在日本東京灣」 |
| event-nanjing-datusha | 南京 | 城市（首都，时为抗战中心） | city | 審字第壹號 p6「分竄京市各區」 |
| event-nanjing-datusha | 中华门 | 城门/战场 | battlesite | 同上「攻陷中華門…即開始屠殺」 |
| event-nanjing-datusha | 下关草鞋峡 | 江边屠杀遗址 | battlesite | 同上 p7「下關草鞋峽等處…集體殺戮及焚屍滅跡」 |
| event-xinzhongguo-chengli | 北京 | 首都（1949 定都） | capital | 中央人民政府公告 p7「決定北京爲中華人民共和國的首都」 |
| event-wusi-yundong | 青岛 | 城市（和会交涉标的） | city | 五四運動宣言 p1「要求並吞青島」 |
| event-wusi-yundong | 山东 | 区域（和会交涉标的） | region | 同上「管理山東一切權利」 |
| event-wusi-yundong | 北京 | 城市（执笔/印发地） | city | 同上罗注「回到漢花園北京大學新潮社」 |

## 数据政策执行说明

- **historical vs modern 区分**：全部条目按底本语境登记历史属性（宋边路分/城门/故都/和会标的等），
  description 与 review_note 只复述来源文本，不做「历史地名 → 现代城市」的强制映射
  （如 延州、鄜延、冀东、下关草鞋峡 等均按历史称谓登记）。
- **coordinates**：未收录任何坐标——本轮来源不含可核实坐标数据；政策禁止臆测（`places` 表中
  仅有的 3 条既有坐标条目不受影响）。
- **规范实体（places 表）暂不新增**：这 15 条是事件—地点关联（event_place），保持
  `link_status: needs_linking`，等待地理实体解析（CHGIS 手工导入通道 / 后续批次）再升级为
  canonical place（含 historical_name / modern_name / place_type / 坐标）。

## 汇总

| 指标 | Before | After |
|---|---:|---:|
| event_place 总数 | 37 | **52** |
| needs_linking | 34 | 49 |
| linked | 3 | 3 |
| 涉及事件 | — | 6 个本轮关闭的 Critical |
