# Batch 02 · Queue 1 — Baseline Snapshot

> 快照时间：2026-09-12 · dist/history.duckdb（read-only 查询）+ reports/{PRODUCT_COVERAGE.md, ENRICHMENT_QUEUE.json} + curated YAML 现算分
> 此为 Batch 02 全部 Before 数字来源；Batch 02 结束后在 BATCH02_FINAL.md 做 Before/After 对照。

## Knowledge Layer

| 项 | 值 |
|---|---:|
| historical_texts | **730,128** |
| sources（表） | 4（classical-modern / curated-backbone-v1 / curated-semantic-v1 / curated-person-knowledge-gap） |
| works | 49 |
| chapter_heads / 章节结构 | document → section → chapter → paragraph_index（NiuTrans 快照 20240421，MIT） |

## Backbone

| 项 | 值 |
|---|---:|
| events | 618（critical 62 / major 555 / normal 1） |
| places | 3 |
| people | 234 |
| event_person | 398 |
| event_place | 37（linked 3 / needs_linking 34） |
| event_relations | 1,057（follows 499 / leads_to 288 / precedes 171 / part_of 95 / contributes_to 4） |
| event_text | 120 |
| story_events | 26 |

## Evidence

| 项 | 值 |
|---|---:|
| event_evidence total | **154** |
| linked | **98** |
| needs_linking | 34 |
| pending_knowledge | 22 |
| link_method 分布 | manual 24 / content 42 / exact 27 / alias 5 / (legacy 无 method) 56 |
| claim_field 分布 | legacy 无 130 / background 6 / process 6 / result 6 / impact 6 |
| event_evidence_candidates（fuzzy candidates 表） | 0 |
| event_text_candidates | 0 |

## Product Coverage（Before）

| 项 | 值 |
|---|---:|
| average product_completeness_score | **31.6** |
| ≥90 完整条目 | **3**（0.5%）—— 蒙古建国 100 / 元朝建立 100 / 平王东迁 100 |
| Critical（queue 优先级） | **8** |
| Major（queue 优先级） | 599 |
| Normal（queue 优先级） | 11 |

### 按维度（全部 618 events）

| 维度 | 满足率 |
|---|---:|
| 人物 | 42.7%（264） |
| 地点 | 5.2%（32） |
| 来源 | 100.0% |
| 证据 | 13.4%（83） |
| 关联事件 | 98.2%（607） |
| 背景 | 9.2%（57） |
| 过程 | 1.0%（6） |
| 结果 | 13.4%（83） |
| 影响 | 1.0%（6） |

## 三个 88.9 Critical（Queue 2 处理对象）

| event | score | 缺失维度 | relations 现状 |
|---|---:|---|---|
| event-chuzhuang-wang-ba 楚庄王（问鼎中原/邲之战） | 88.9 | **related_event** | 0 |
| event-jinwen-gong-ba 晋文公（城濮/践土） | 88.9 | **related_event** | 0 |
| event-hezong-lianheng 合纵连横 | 88.9 | **related_event** | 0 |

三者其余 8 维（四叙述、people、places、evidence、source）均已满足，均为 overnight-08 source-backed 富化产物。

## 8 个 Critical NEEDS_SOURCE（Queue 3/10 对象）

| event | score | missing |
|---|---:|---|
| event-jiuyiba-shibian 九一八事变 | 81.2 | place, evidence, background, process, result, impact |
| event-nanjing-datusha 南京大屠杀 | 81.2 | 同上 |
| event-qiqishi-bian 七七事变 | 81.2 | 同上 |
| event-riben-touxiang 日本宣布投降 | 81.2 | 同上 |
| event-wusi-yundong 五四运动 | 81.2 | 同上 |
| event-xian-shibian 西安事变 | 81.2 | 同上 |
| event-western-xia-jianguo 西夏建立 | 76.2 | 同上 |
| event-xinzhongguo-chengli 中华人民共和国成立 | 75.7 | 同上 |

## 运行环境备注（非阻塞，已记录）

- 本机 AppImage binfmt 破坏 venv prefix（`.venv/bin/python` 与 uv venv 符号链接均失效），
  与 overnight-10 记录一致。本轮方案：`uv sync --frozen` 生成 `.venv-batch02`，
  以 `PYTHONPATH=src:.venv-batch02/lib/python3.11/site-packages` +
  uv cpython 3.11.14 (`~/.local/share/uv/python/cpython-3.11.14-.../bin/python3`) 运行全部 pipeline。
