# Batch 02 · Queue 10 — Critical Recheck（8 → 2）

> 新语料：`source-wikisource`（wikisource/20260912，10 页 manifest / 9 页入库，Quality Gate PASS）。
> 规则执行：只用语料内段落写 canonical 字段；无来源者保持 NEEDS_SOURCE，不用模型常识补齐。

## 结果总表

| event | before_score | after_score | new_source | new_evidence | fields_improved | still_missing | status |
|---|---:|---:|---|---:|---|---|---|
| event-western-xia-jianguo 李元昊称帝、西夏建立 | 22.2 | **100.0** | 宋史·夏国传上（卷485） | 5 | bg/process/result/impact/place | — | ✅ closed |
| event-qiqishi-bian 七七事变（卢沟桥事变） | 22.2 | **100.0** | 對盧溝橋事件之嚴正聲明（1937-07-17 庐山谈话） | 4 | 同上 | — | ✅ closed |
| event-riben-touxiang 日本宣布投降 | 22.2 | **100.0** | 降伏文書（1945-09-02） | 6 | 同上 | — | ✅ closed |
| event-nanjing-datusha 南京大屠杀 | 22.2 | **100.0** | 谷寿夫案判决书（審字第壹號）+ 百人斩判决（審字第十三號） | 5 | 同上 | — | ✅ closed |
| event-xinzhongguo-chengli 中华人民共和国成立 | 22.2 | **100.0** | 中央人民政府公告 + 共同纲领 | 5 | 同上 | — | ✅ closed |
| event-wusi-yundong 五四运动 | 22.2 | **100.0** | 五四運動宣言（罗家伦，1919） | 5 | 同上 | — | ✅ closed |
| event-jiuyiba-shibian 九一八事变 | 22.2 | 22.2 | 无（许可不明） | 0 | — | people/place/evidence/bg/process/result/impact | ⛔ NEEDS_SOURCE |
| event-xian-shibian 西安事变 | 22.2 | 22.2 | 无（首选文献缺失、张署名权利未满期） | 0 | — | 同上 | ⛔ NEEDS_SOURCE |

- before_score 为 product_completeness_score（9 维等权）。8 个事件 before 均 22.2（仅 source+related_event 两维满足）；
  6 个关闭事件本轮补齐 people/place/evidence/四叙述共 7 维（HEAD 版本实算复核）。
- 新增 evidence 30 条（Claim_field：background 6 / process 6 / result 7 / impact 6 + overnight-08 之外的 supporting），
  全部 `link_method: manual` 段落精确锚（`chapter_anchor#pN`），review_note 附逐字引文。
- dist event_evidence：154 → **184**；event_place：37 → **52**（needs_linking 49）。

## 证据锚点抽样（每条均可在语料回查）

| event | claim | 锚 | 引文 |
|---|---|---|---|
| 西夏建国 | process | 宋史 卷485 #p66 | 「宋寶元元年……遂築壇受冊，即皇帝位，時年三十。」 |
| 西夏建国 | result | 宋史 卷485 #p68 | 「國稱大夏，年號天授禮法延祚……許以西郊之地，冊為南面之君。」 |
| 七七事变 | impact | 對盧溝橋事件之嚴正聲明 #p12 | 「如果戰端一開，那就是地無分南北，年無分老幼，無論何人，皆有守土抗戰之責任。」 |
| 日本投降 | impact | 降伏文書 #p9 | 「簽字於一九四五年九月二日九時四分在日本東京灣。」 |
| 南京大屠杀 | result | 審字第壹號 #p7 | 「被害總數達三十余萬人。」 |
| 新中国成立 | result | 中央人民政府公告 #p7 | 「組成中央人民政府委員會，宣告中華人民共和國的成立。」 |
| 五四运动 | impact | 五四運動宣言 #p6（罗家伦注） | 「這是五四那天唯一的印刷品……寫時所凝結的卻是大家的願望和熱情。」 |

## 未关闭项说明（诚实记录）

- **九一八事变**：wikisource 仅有政党决议（1931-09-22），是否属著作权法第 5 条官方文件存在解释空间 → 不据此写字段（batch02-03 A7）。
- **西安事变**：张学良杨虎城通电在 wikisource 无页面；张学良（卒 2001）署名文献保护期未满 → 不写（batch02-03 A8）。
  两者保持 NEEDS_SOURCE，等待许可明确的档案文献（如影印本公版）接入。

## 过程问题与修复（本轮内）

1. `event_evidence` id 公式原不含 `claim_field`，同段落支撑多字段时证据行合并（2 行丢失）。
   已修为含 claim_field 的 identity（build.py），dist 重建后 30 条新增证据全部保留（184 条）。
2. 五四運動宣言页在 Queue 5 标记 gated_pending_review；取回核实署名（罗家伦，卒 1969 → 2020 起 PD）
   后转为 allowed 并接入（356→362 段落）。
3. 投降书页尾 `[[Category:…]]` 链接剥离后漏出命名空间行（2 行）；parser 已加剥离后前缀复检。
