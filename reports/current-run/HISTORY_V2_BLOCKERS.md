# HISTORY V2 BLOCKERS（阶段遗留清单）

## License Blocked（许可受限，禁止接入文本）

- 九一八事变 — source 许可未明，保持 NEEDS_SOURCE
- 西安事变 — source 许可未明，保持 NEEDS_SOURCE

## Source gaps（缺源，待 Source Expansion）

| 缺口 | 影响 |
|---|---|
| 清实录 / 光绪朝档案 | 晚清系列事件的段落锚 |
| 明实录 | 明初若干事件的编年锚（现多用明史本纪替代） |
| 续资治通鉴长编 | 北宋事件密度提升 |
| 民国官方文书/报刊 | 民国系列（现多为大纲级） |
| 元史·顺帝纪 / 河渠志 | 元末与治河事件（贾鲁治河以河平碑代锚） |
| 日本书纪 | 白江口之役日方记载 |

## needs_linking（合法状态，非错误）

- evidence 中 needs_linking：**14** 条；事件/人物/地点 needs_linking 见 resolve_references 统计。
- 涉及：三朝北盟会编, 周书, 明实录, 晋书, 清实录, 筹办夷务始末, 续资治通鉴长编, 辛亥革命回忆录

## Source-limited events

- **SOURCE_LIMITED（深度分类）**：1 个 —— 详见 DEPTH_BACKLOG_V2.json（P3）。
- 代表：吴起变法（史记仅 4 处短引）、晚清系列（清实录未入藏）。

## 说明

- 以上均为**已登记、已分类**的债务；不影响 Phase 1 验收（架构/知识层/证据层/门禁/测试均 PASS）。
