# Batch 02 · Queue 9 — Evidence Relink

> 命令：`backbone link-evidence`（dry-run）→ `--apply` → 事故恢复 → dist 重建。
> 机制保持：alias → exact → normalized volume/chapter → content → fuzzy（fuzzy 永远 candidate-only）。

## Linking 结果（apply 后终态）

| 指标 | Before（baseline） | After（本轮 relink 后） |
|---|---:|---:|
| event_evidence total | 154 | 154（新增 evidence 属 Queue 10 策展，此处先复核既有链路） |
| linked | 98 | 98 |
| link_method=manual（段落精确锚） | 24 | **24（恢复后保持）** |
| link_method=exact | 27 | 27 |
| link_method=content | 42 | 42 |
| link_method=alias | 5 | 5 |
| needs_linking | 34 | 34 |
| pending_knowledge | 22 | 22 |
| fuzzy candidates（写回） | 0 | **0（fuzzy 永不写回，规则保持）** |
| chapter_anchor 带 #p（段落级） | 24 | **24** |

## 对新语料的匹配面

新入语料的 350 行（wikisource）不自动产生新链接：既有 34 条 needs_linking / 22 条 pending
均指向清实录/清史稿/明实录/晋书/旧唐书缺卷等**真正缺失的著作**（见 batch02-03 inventory），
新 source 与它们不重叠；27 条 fuzzy_candidate 全部保持报告态（未写回，符合 Rule 5）。

unmatched 29 条与新 source 无交集（著作名未命中语料：清实录×5、清史稿×3、明实录×2、
晋书×5、旧唐书×4、筹办夷务始末/辛亥革命回忆录/续资治通鉴长编/三国志·吴书 等）。

## 事故与恢复（记录在案）

1. **事故**：`link-evidence --apply` 将 overnight-08 的 24 条 `link_method: manual`
   段落精确锚（4 事件 × 4 维，各不相同的 text_id + `chapter_anchor#pN`）**重算为章级 exact 锚**
   ——4 条 evidence 的 historical_text_id 塌缩为同一章首段 id，丢失段落级坐标。
   根因：apply_links 对已带 manual 锚的行同样执行锚定重算（机制未区分 manual 特权）。
2. **恢复**：从 `dist/history.previous.duckdb`（overnight-08 终态备份）读取 24 条 manual 行的
   `historical_text_id / chapter_anchor / link_method / confidence`，按
   (event_id, work, term, claim_field) 精确写回 YAML；同时从 HEAD 恢复 6 个被
   safe_dump 重写丢失的 YAML 头注释。
3. **验证**：`backbone validate` OK；dist 重建后 `chapter_anchor LIKE '%#p%'` = 24，
   methods 分布回到 baseline；事件 YAML relations/evidence/narrative 完整性复查通过。
4. **遗留建议**（本轮不改机制）：`apply_links` 应跳过 `link_method == 'manual'` 的行
   （manual 锚为人工段落级证据，自动重算只能降级）。已记入 BATCH02_FINAL Blockers/改进项。
