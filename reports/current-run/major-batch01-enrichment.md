# Major Batch 01 — READY 17 Enrichment Result

> 承接 batch02-14 选择（READY 16 + 补链接后并入的收复长安），执行「下一轮正式 enrichment」。
> 规则与 Queue 10 相同：叙述句全部可回溯到 review_note 逐字引文；已有 reviewed 字段不覆盖；
> legacy result 短句保留并补锚。写入 append-only（并进行了一次重复键修复，见文末）。

## 结果总表

| event | before | after | evidence rows（新增） | 关键锚 |
|---|---:|---:|---:|---|
| event-chuhan-julu 巨鹿之战 | 66.7 | **100.0** | +5 | 项羽本纪#p114/p149/p150/p156（章邯围钜鹿→沉船→九战虏王离→诸侯膝行） |
| event-hongmen 鸿门宴 | 66.7 | **100.0** | +5 | 项羽本纪#p197/p252/p279/p284/p286（曹无伤告密→樊哙闯帐→脱身→碎玉斗） |
| event-chuhan-pengcheng 彭城之战 | 66.7 | **100.0** | +4 | 高祖本纪#p291/p292/p293/p294（入彭城→睢水大战→家眷被质→诸侯背汉） |
| event-chuhan-xingyang 荥阳对峙 | 66.7 | **100.0** | +4 | 汉纪二#p67/p158/p160/p177（深沟壁垒→纪信诳楚→汉王遁去→楚拔荥阳） |
| event-chuhan-gaixia 垓下之战 | 66.7 | **100.0** | +4 | 项羽本纪#p490/p491 + 汉纪三#p16 + 项羽本纪#p534（会师→围数重→四面楚歌→自刎） |
| event-chuhan-han-foundation 刘邦建立汉朝 | 66.7 | **100.0** | +4 | 汉纪三#p70/p71/p72/p73（诸侯请尊→即位于汜水之阳→定后妃名号→封长沙王） |
| event-chuhan-qin-revolt 秦末起义 | 66.7 | **100.0** | +5 | 高祖本纪#p65 + 陈涉世家#p10/p45/p46 + 秦始皇本纪#p537（张楚→大泽乡之谋→立王→天下响应） |
| event-chuhan-qin-fall 秦朝灭亡 | 66.7 | **100.0** | +4 | 高祖本纪#p185/p186/p190 + 项羽本纪#p288（至霸上→子婴降→封府库→屠咸阳焚宫） |
| event-anlu-uprising 安禄山起兵 | 66.7 | **100.0** | +4 | 唐纪三十三#p119/p125/p136 + 旧唐书卷九#p376（诈敕→铁舆南下→唐廷应变） |
| event-anlu-three-frontiers 兼领三镇 | 66.7 | **100.0** | +4 | 旧唐书卷150#p19/p21/p40/p44（平卢→范阳→河东→「兼三道节度」） |
| event-anlu-luoyang 洛阳失守 | 66.7 | **100.0** | +4 | 唐纪三十三#p141/p180 + 旧唐书卷九#p388 + 唐纪三十四#p13 |
| event-anlu-tongguan 潼关失守 | 66.7 | **100.0** | +4 | 唐纪三十四#p21/p54/p61/p298（对峙→乾祐据险→伏兵大败官军→四方闻失守） |
| event-anlu-changan 长安失守 | 66.7 | **100.0** | +4 | 唐纪三十四#p104/p204/p271/p368（出延秋门→贼入长安→肃宗灵武即位→诸道心坚） |
| event-anlu-xuanzong-shu 玄宗入蜀 | 66.7 | **100.0** | +4 | 唐纪三十四#p91/p132/p190/p330（幸蜀之策→马嵬→整军→至成都千三百人） |
| event-anlu-changan-recapture 收复长安 | 66.7 | **100.0** | +4（+1 pending 关闭） | 唐纪三十六#p16/p19/p24/p26（三军部署→嗣业肉袒执刀→斩首六万→贼弃城走） |
| event-anlu-shi-siming 史思明再叛 | 66.7 | **100.0** | +4 | 唐纪三十六#p338 + 唐纪三十七#p4/p47/p57（降唐→筑坛称王→与庆绪决裂） |
| event-anlu-pacification 安史之乱平定 | 55.6 | **100.0** | +4 + 2 relations | 唐纪三十八#p291/p375 + 旧唐书卷十一#p92 + 唐纪三十九#p5（借回纥兵→朝义缢死→降将授藩镇） |

**17/17 达成 100.0**；新增 evidence 71 条（楚汉 35 + 安史 36），全部 `link_method: manual` 段落锚。

## 附带成果

- **pending_knowledge 清零（1 → 0）**：anlu-changan-recapture 的 legacy 悬空锚（资治通鉴·郭子仪）
  锚定唐纪三十六#p26「贼弃城走矣，请以二百骑追之」（收复长安之证），Queue 11 遗留的 manual_candidate 关账。
- anlu-pacification 补 2 条策展关系（follows 史思明再叛 / follows 安禄山起兵），related_event 维度补齐。
- dist：event_evidence **255**（linked 221 / needs_linking 34）· event_relations **1,067** ·
  event_person 398（legacy 人物行全部保留）· historical_texts 730,490 不变。
- 产品覆盖：**≥90 从 12 → 29**（major 群 3 → 20）；average 32.3 → **33.2**；
  过程维度 1.9% → **4.7%**、影响 1.9% → **4.7%**、背景 10.2% → **12.9%**、关联事件 98.7% → **98.9%**。

## 过程事故与修复（记录在案）

- **重复顶层键事故**：append-only 富化在已有 `people:`/`evidence:` 的 17 个文件尾部再次追加同名键，
  PyYAML last-wins 使旧列表（Queue 11 恢复的 legacy 锚、legacy people）在解析视图中被遮蔽，
  dist 一度丢失 17 条旧 evidence。
- **修复**：`scripts/fix_duplicate_top_keys.py` 提取同名键全部块 → 合并列表（旧前新后、完全同项去重）
  → 重写单键（头注释保留）；复核 0 重复键；dist 重建后 evidence=255（无遮蔽）、event_person=398（不变）。
  该脚本与检测逻辑保留，供后续 append 富化前预检。

## 测试

- `pytest tests/ -q` **249 passed / 16 skipped / 0 failed**（全量；test_backbone 30 + test_backbone_build 5 计入）。
- 计数更新：pending 150 → 221（evidence 总量 255 - needs_linking 34）；relations 1065 → 1067；
  evidence 184 → 255。均为数据合法增长。

## 剩余 READY/PARTIAL 队列

- PARTIAL_SOURCE 9：唐 1（已在本次关闭→现 READY 状态无残留）+ 明 6（明史在库、待链接）+ 西汉 2。
- NEEDS_SOURCE 5：晚清（清实录/清史稿）。
