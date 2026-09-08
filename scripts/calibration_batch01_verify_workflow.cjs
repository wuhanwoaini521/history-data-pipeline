// Calibration Batch 01 - Independent Verification + Audit (ASCII-only; no CJK anywhere)
// Dispatch 10 Verifier children (agent: researcher - has web tools for glyph checks)
// plus 1 Auditor on a deterministic 3-event sample, then aggregate verdicts.

const PAIRS = [
  ["event-shangtang-miexia", "data/curated/history_backbone/events/pre_qin/event-shangtang-miexia.yml"],
  ["event-wuwang-fazhou", "data/curated/history_backbone/events/pre_qin/event-wuwang-fazhou.yml"],
  ["event-pingwang-dongqian", "data/curated/history_backbone/events/chunqiu_zhanguo/event-pingwang-dongqian.yml"],
  ["event-sanjia-fenjin", "data/curated/history_backbone/events/chunqiu_zhanguo/event-sanjia-fenjin.yml"],
  ["event-changping-zhizhan", "data/curated/history_backbone/events/chunqiu_zhanguo/event-changping-zhizhan.yml"],
  ["event-qin-mie-liuguo", "data/curated/history_backbone/events/chunqiu_zhanguo/event-qin-mie-liuguo.yml"],
  ["event-qin-tongyi", "data/curated/history_backbone/events/chunqiu_zhanguo/event-qin-tongyi.yml"],
  ["event-qiguo-zhi-luan", "data/curated/history_backbone/events/qin_han/event-qiguo-zhi-luan.yml"],
  ["event-mobei-zhizhan", "data/curated/history_backbone/events/qin_han/event-mobei-zhizhan.yml"],
  ["event-wangmang-chengdi", "data/curated/history_backbone/events/qin_han/event-wangmang-chengdi.yml"],
];
const VOUT = "reports/current-run/verification";
const BRIEF = "reports/current-run/research-brief-batch01.md";

function makeVerifierTask(eid, canonical, itemNo, total) {
  const lines = [];
  lines.push("ROLE: Independent Verifier (AGENTS.md section 5). You verify ONE historical record for calibration batch 01. You are item " + itemNo + " of " + total + ".");
  lines.push("You must NOT assume the Producer is correct. You are an independent reviewer.");
  lines.push("Work in the repository at D:/code/self-github/self-tools/history-data-pipeline");
  lines.push("CANDIDATE FILE (Producer's enriched record): data/candidates/calibration_batch01/" + eid + ".yml");
  lines.push("CANONICAL FILE (the repository source of truth): " + canonical);
  lines.push("RESEARCH BRIEF (Researcher artifact; READ FIRST): " + BRIEF);
  lines.push("STEPS:");
  lines.push(" 1) Read the candidate and the canonical file. For every field the candidate copies from canonical (name_zh_cn, event_type, start_year, end_year, summary_zh_cn, background_zh_cn, result_zh_cn, source_reference, source_ids, every people person_name_raw, every evidence work/term/chapter_hint/evidence_role and the places id), compare character-for-character with the canonical. Any difference = a corruption finding. A differing Han character where the canonical is shorter, longer or differently shaped is a HARD FAIL (cite the exact differing value).");
  lines.push(" 2) Glyph confirmation: open the research brief, find this event's section, and identify the canonical source URL(s) it cites (usually ctext.org or an official/institutional page; some are Wikipedia/Zhihu secondary). Fetch those URLs with your fetch tool. Confirm that every text title, author, and chapter the candidate cites (evidence.work, evidence.term, evidence.chapter_hint, and the source_reference) matches the fetched page's exact Han character sequence. If you cannot confirm a glyph, mark it unconfirmed and do NOT claim it is correct.");
  lines.push(" 3) Doubling: verify there is no unsupported invention: no fabricated coordinates, no fabricated chapter, no fabricated person/place id, no fabricated link_status. historical_text_id must be null. link_status for evidence must be needs_linking. Any fabricated locator/ID = HARD FAIL.");
  lines.push(" 4) Dates: start_year <= end_year; if any source dispute on a date is recorded, it may be fine but note it.");
  lines.push(" 5) Independent source count: candidates with two independent classical anchors are stronger than one; report whether the evidence chain is genuinely from independent sources versus one source transcribed twice.");
  lines.push("OUTPUT CONTRACT (do exactly this):");
  lines.push(" (a) Write a JSON artifact to " + VOUT + "/" + eid + ".json with keys: eid, verdict (PASS|WARN|FAIL), checks {verbatim, glyphs, grounding, links, temporal}, source_urls_fetched, reasons (array of strings), notes.");
  lines.push(" (b) Reply with exactly ONE line, JSON: {\"key\":\"" + eid + "\",\"verdict\":\"PASS|WARN|FAIL\",\"reason\":\"<one concise sentence>\"}");
  return lines.join("\n");
}

function makeAuditorTask(sampleIds, verifierSummary) {
  const lines = [];
  lines.push("ROLE: Independent Auditor (AGENTS.md section 18). You sample-audit a subset of the already-verified candidates from calibration batch 01.");
  lines.push("You must NOT simply repeat the Verifier results. You independently re-verify each sampled record from the primary repository files and the research brief, looking for systematic errors the Verifier or Producer may have missed.");
  lines.push("Working dir: D:/code/self-github/self-tools/history-data-pipeline");
  lines.push("SAMPLED EVENT IDS (comma list): " + sampleIds.join(","));
  lines.push("VERIFIER SUMMARY (for context only, do not trust it): " + verifierSummary);
  lines.push("For each sampled event id:");
  lines.push("  - read data/candidates/calibration_batch01/<id>.yml and its canonical counterpart under data/curated/history_backbone/events/");
  lines.push("  - independently confirm dates plausibly, name correctness, source independence, and that the candidate is genuinely derived from the canonical (no invented enrichment).");
  lines.push("  - confirm the claim_type/evidence linkage is not overstated; confirm not fabricated locators.");
  lines.push("  - Do not rely on the earlier Verifier's conclusion; reach your own.");
  lines.push("OUTPUT: (a) write a JSON artifact to " + VOUT + "/auditor.json with keys: sampled_ids, per_event (map id -> {verdict, reasons}), recurring_patterns (array), systemic_concerns (string or null), overall (string).");
  lines.push(" (b) Reply exactly ONE line JSON: {\"key\":\"auditor\",\"verdict\":\"PASS|WARN|FAIL\",\"reason\":\"...\"}");
  return lines.join("\n");
}

// Deterministic 3-item sample across 10 events (simple LCG, no randomness)
function pickSample(ids, n, seed) {
  const s = seed >>> 0;
  let x = (s * 9301 + 49297) % 233280;
  const pool = ids.slice();
  const out = [];
  while (out.length < n && pool.length > 0) {
    x = (x * 9301 + 49297) % 233280;
    const idx = Math.floor((x / 233280) * pool.length);
    out.push(pool.splice(idx, 1)[0]);
  }
  return out;
}

// discover canonical path for auditor from id (mirror of PAIRS), no longer needed
const total = PAIRS.length;
const childJobs = PAIRS.map((row, i) => ({
    key: "verifier-" + row[0],
    agent: "researcher",
    task: makeVerifierTask(row[0], row[1], i + 1, total),
    output: VOUT + "/" + row[0] + ".json",
  }));

const results = await runs.all(childJobs);
const parsed = [];
for (let i = 0; i < results.length; i++) {
  const r = results[i];
  const id = PAIRS[i] ? PAIRS[i][0] : ("item" + i);
  parsed.push({ id: id, rawStatus: r ? r.status : "missing", note: r ? (r.output || r) : null });
}

// Auditor on a 3-id sample
const ids = PAIRS.map((row) => row[0]);
const sample = pickSample(ids, 3, 1);
let verifierLine = "";
parsed.forEach((p) => { verifierLine += p.id + ":" + (p.note ? "ok" : "empty") + "; "; });

let audit = null;
try {
  audit = await runs.run("auditor", {
    agent: "researcher",
    task: makeAuditorTask(sample, verifierLine),
    output: VOUT + "/auditor.json",
  });
} catch (e) {
  audit = { status: "error", error: String(e) };
}

// Group verdicts for the summary
const summary = { verifiers: parsed, auditor: audit, sample: sample };
emit(JSON.stringify(summary, null, 2));
return summary;