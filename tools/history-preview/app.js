"use strict";
/* =====================================================================
   HISTORY_DATA_PRODUCT_VALIDATION viewer — pure vanilla JS, READ ONLY.
   Reads the pre-built JSON in tools/history-preview/data/.
   Never writes any store.  Serve from tools/history-preview/ with:
        python -m http.server 8080
   ===================================================================== */

const DATA = {
  overview: null, events: [], periods: [], regimes: [], relations: [],
  samples: [], completeness: null, person_linking: null, timeline: null,
  regime_tree: [], people: [], eventsById: {}, personById: {},
  periodById: {}, regimeById: {}
};

const KIND_LABEL = { cbdb: "CBDB", ctext: "CText", curated: "Curated Supplemental" };

/* ------------------------------------------------------------- helpers */
function es(s) { return s == null ? "" : String(s).replace(/[&<>"']/g, c =>
  ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])); }
function fmtYear(y) {
  if (y === null || y === undefined || y === "" || isNaN(+y)) return "—";
  return +y < 0 ? "前" + (-y) : String(+y);
}
function fmtDate(e) {
  if (e.start == null && e.end == null) return "—";
  if (e.start === e.end) return fmtYear(e.start);
  return fmtYear(e.start) + " → " + fmtYear(e.end);
}
const fmtN = n => (n == null ? 0 : Number(n).toLocaleString("en-US"));

function impBadge(e) {
  const k = String(e.importance || "").toLowerCase();
  const cls = k === "critical" ? "b-crit" : k === "major" ? "b-major" : "b-normal";
  return `<span class="badge ${cls}">${es(k)}</span>`;
}
function kindBadge(kind) {
  const k = (kind || "").toLowerCase();
  const cls = k === "cbdb" ? "b-cbdb" : k === "ctext" ? "b-ctext" : "b-curated";
  return `<span class="badge ${cls}">${es(KIND_LABEL[k] || k || "?")}</span>`;
}
function periodName(id) { const p = DATA.periodById[id]; return p ? p.name : (id || "—"); }
function regimeNames(ids) {
  return (ids || []).map(i => { const r = DATA.regimeById[i]; return r ? r.name : i; }).join("、") || "—";
}
function barRow(label, value, max) {
  const pc = max ? Math.round((value / max) * 100) : 0;
  return `<div class="bar-row"><div class="bl">${label}</div>` +
    `<div class="bar"><i style="width:${pc}%"></i></div><div class="bv">${value}</div></div>`;
}
function histogram(o) {
  const max = Math.max.apply(null, Object.values(o || {}).concat(0));
  return Object.entries(o || {}).sort((a, b) => +a[0] - +b[0])
    .map(([k, v]) => barRow(es(k + " 年代"), v, max)).join("");
}

/* ------------------------------------------------------------- routing */
const TABS = ["overview", "events", "samples", "people", "regimes", "completeness", "reports"];
function renderTab(tab) {
  document.querySelectorAll("#tabs .tab").forEach(b => b.classList.toggle("on", b.dataset.tab === tab));
  const app = document.getElementById("app");
  const R = { overview: renderOverview, events: renderEvents, samples: renderSamples,
              people: renderPeople, regimes: renderRegimes, completeness: renderCompleteness,
              reports: renderReports };
  (R[tab] || renderOverview)(app);
}
function route() {
  const dd = document.getElementById("detail-drawer");
  const h = location.hash || "#/overview";
  let m = h.match(/^#\/event\/(.+)$/);
  if (m) {
    const id = decodeURIComponent(m[1]);
    if (DATA.eventsById[id]) openEvent(id, false);
    renderTab("events");
    return;
  }
  m = h.match(/^#\/sample\/(\d+)$/);
  if (dd) dd.classList.add("hidden");
  if (m) { renderTab("samples"); if (DATA.samples[+m[1]]) selectSample(+m[1]); return; }
  const tab = (h.replace(/^#\//, "") || "overview").split(/[/?]/)[0];
  renderTab(TABS.includes(tab) ? tab : "overview");
}

/* ------------------------------------------------------------- drawer */
function openEvent(id, setHash) {
  const ev = DATA.eventsById[id];
  if (!ev) return;
  if (setHash !== false) location.hash = "#/event/" + encodeURIComponent(id);
  const el = document.getElementById("detail-drawer");
  el.innerHTML = detailHTML(ev);
  const raw = el.querySelector("#raw-json");
  if (raw) raw.textContent = JSON.stringify(ev, null, 2);
  el.classList.remove("hidden");
  const btn = el.querySelector(".detail-close");
  if (btn) btn.addEventListener("click", closeDrawer);
}
function closeDrawer() {
  document.getElementById("detail-drawer").classList.add("hidden");
  if (location.hash.startsWith("#/event/")) history.replaceState(null, "", "#/events");
}

/* ------------------------------------------------------------- overview */
function renderOverview(app) {
  const b = DATA.overview.backbone, ks = DATA.overview.knowledge_store;
  let h = `<h2 class="section-title">数据总览 · Validation Overview</h2>` +
    `<div class="grid-cards">
      <div class="stat crit"><div class="num">${fmtN(b.events)}</div><div class="lab">累计事件</div></div>
      <div class="stat crit"><div class="num">${fmtN(b.critical)}</div><div class="lab">Critical</div></div>
      <div class="stat major"><div class="num">${fmtN(b.major)}</div><div class="lab">Major</div></div>
      <div class="stat normal"><div class="num">${fmtN(b.normal)}</div><div class="lab">Normal</div></div>
      <div class="stat"><div class="num">${fmtN(b.periods)}</div><div class="lab">Periods</div></div>
      <div class="stat"><div class="num">${fmtN(b.regimes)}</div><div class="lab">Regimes</div></div>
      <div class="stat major"><div class="num">${fmtN(b.event_relations)}</div><div class="lab">EventRelation</div></div>
      <div class="stat major"><div class="num">${fmtN(b.event_person)}</div><div class="lab">EventPerson<br><span class="muted">${fmtN(b.unique_persons)} 唯一人物</span></div></div>
    </div>`;
  h += `<div class="card"><h3>时间跨度 Timeline</h3><div class="muted">
    <b>${fmtYear(b.timeline_start)} → ${fmtYear(b.timeline_end)}</b> ·
    ${fmtN(b.events)} 个事件按每 100 年分布（见下方直方图 / 「完整性」页）。</div></div>`;
  h += `<div class="card"><h3>Backbone linked data（验收依据为本层）</h3><table>
    <tr><th>指标</th><th>数值</th></tr>
    <tr><td>Event Count</td><td>${fmtN(b.events)}</td></tr>
    <tr><td>Critical / Major / Normal</td><td>${fmtN(b.critical)} / ${fmtN(b.major)} / ${fmtN(b.normal)}</td></tr>
    <tr><td>Period Count</td><td>${fmtN(b.periods)}</td></tr>
    <tr><td>Regime Count</td><td>${fmtN(b.regimes)}</td></tr>
    <tr><td>Formal EventPerson</td><td>${fmtN(b.event_person)}</td></tr>
    <tr><td>Unique Persons</td><td>${fmtN(b.unique_persons)}</td></tr>
    <tr><td>EventPlace 行</td><td>${fmtN(b.event_place_row)}</td></tr>
    <tr><td>EventEvidence</td><td>${fmtN(b.event_evidence)}</td></tr>
    <tr><td>EventRelation</td><td>${fmtN(b.event_relations)}</td></tr>
    <tr><td>Works 关联</td><td>${fmtN(b.works)}</td></tr>
  </table></div>`;
  h += `<div class="card"><h3>Knowledge Store（知识库原始规模，非 Backbone）</h3><table>
    <tr><th>层</th><th>people</th><th>person_aliases</th><th>places</th><th>historical_texts</th><th>works</th><th>sources</th></tr>
    <tr><td>Knowledge Store</td><td>${fmtN(ks.people)}</td><td>${fmtN(ks.person_aliases)}</td><td>${fmtN(ks.places)}</td><td>${fmtN(ks.historical_texts)}</td><td>${fmtN(ks.works)}</td><td>${fmtN(ks.sources)}</td></tr>
    <tr><td>Backbone 已关联</td><td>${fmtN(b.unique_persons)}</td><td>—</td><td>${fmtN(b.event_place_row)} 行</td><td>${fmtN(b.event_evidence)} 事件</td><td>${fmtN(b.works)}</td><td>—</td></tr>
    </table>
    <div class="missing">⚠ 知识库原始收录（含 3rd party，如 CBDB 收录人物 676,427 / 别名 208,624）仅供了解体量，
    不得作为 Backbone 验收证据；验收只看上一表 Backbone 一列。</div></div>`;
  h += `<div class="card"><h3>每 100 年事件密度</h3>${histogram(DATA.timeline.per_100)}</div>`;
  app.innerHTML = h;
}

/* ============================================================ events */
let evState = { period: "", imp: "", q: "" };
function eventRowHTML(e) {
  const plen = e.persons ? e.persons.length : e.person_count || 0;
  const p1 = plen ? `<span class="badge b-ok">${plen} 人</span>` : `<span class="badge b-off">无人物</span>`;
  const p2 = e.has_place ? `<span class="badge b-ok">有地点</span>`
    : (e.has_place_row ? `<span class="badge b-warn">地点待关联</span>` : `<span class="badge b-off">缺地点</span>`);
  const p3 = e.has_evidence ? `<span class="badge b-ok">证据 ${e.evidences.length}</span>` : `<span class="badge b-off">无证据</span>`;
  const p4 = e.has_relation ? `<span class="badge b-ok">相关</span>` : `<span class="badge b-off">无关联</span>`;
  return `<div class="event-row" onclick="openEvent('${e.id}')">
    <div class="top"><span class="nm">${es(e.name)} ${impBadge(e)}</span>
      <span class="sub">${es(String(e.type || "").replace(/-/g, " "))} · ${fmtDate(e)}</span></div>
    <div class="sub">${es(periodName(e.period_id))} · ${p1} ${p2} ${p3} ${p4} ·
      <span class="kbd">${es(e.id)}</span></div>
    ${e.summary ? `<div class="summary">${es(e.summary).slice(0, 170)}${e.summary.length > 170 ? "…" : ""}</div>` : ""}
  </div>`;
}
function renderEvents(app) {
  let list = DATA.events.filter(e => {
    if (evState.period && e.period_id !== evState.period) return false;
    if (evState.imp && String(e.importance || "").toLowerCase() !== evState.imp) return false;
    const q = evState.q.trim().toLowerCase();
    if (q && !(e.name && e.name.toLowerCase().includes(q)) &&
        !(e.summary && e.summary.toLowerCase().includes(q))) return false;
    return true;
  });
  list = [...list].sort((a, b) => (a.start || 0) - (b.start || 0));
  const ps = [...DATA.periods].sort((a, b) => (a.start || 0) - (b.start || 0));
  let h = `<h2 class="section-title">事件时间线（${fmtN(list.length)} / ${fmtN(DATA.events.length)}）</h2>
    <div class="toolbar">
      <input class="search-inp" id="ev-search" type="search" placeholder="搜索名称 / 摘要…" value="${es(evState.q)}">
      <select id="ev-period"><option value="">全部时期</option>${ps.map(p => `<option value="${p.id}" ${evState.period === p.id ? "selected" : ""}>${es(p.name)}</option>`).join("")}</select>
      <select id="ev-imp"><option value="">全部优先级</option>
        <option value="critical" ${evState.imp === "critical" ? "selected" : ""}>Critical</option>
        <option value="major" ${evState.imp === "major" ? "selected" : ""}>Major</option>
        <option value="normal" ${evState.imp === "normal" ? "selected" : ""}>Normal</option></select>
      <button class="ghost" id="ev-clear">重置</button></div>`;
  h += list.map(eventRowHTML).join("") || `<div class="none">无匹配事件。</div>`;
  app.innerHTML = h;
  document.getElementById("ev-search").addEventListener("input", e => { evState.q = e.target.value; renderEvents(app); });
  document.getElementById("ev-period").addEventListener("change", e => { evState.period = e.target.value; renderEvents(app); });
  document.getElementById("ev-imp").addEventListener("change", e => { evState.imp = e.target.value; renderEvents(app); });
  document.getElementById("ev-clear").addEventListener("click", () => { evState = { period: "", imp: "", q: "" }; renderEvents(app); });
}

/* ------------------------------------------------------------- detail */
function personItemHTML(p) {
  const info = DATA.personById[p.person_id] || {};
  const meta = [
    p.role_zh_cn || (p.role ? p.role : ""),
    p.side ? "阵营 " + p.side : "",
    p.source ? "来源 " + p.source : "",
    p.confidence != null ? "置信 " + p.confidence : ""
  ].filter(Boolean).join(" · ");
  const kb = ["birth", "death", "aggregate_events"].map(k =>
    `<span class="kbd">${es(k)}=${es(info[k] == null ? "−" : info[k])}</span>`).join(" ");
  return `<div class="person-item">
    <div class="top">${kindBadge(p.kind || p.kind_label)} <b>${es(p.name)}</b>
      <span class="pid">${es(p.person_id)}</span></div>
    <div class="meta">${es(meta)}</div>
    <div class="meta">${kb}</div>
    ${p.description ? `<div class="meta">${es(p.description)}</div>` : ""}
  </div>`;
}
function placeHTML(e) {
  if (!e.places || !e.places.length)
    return `<div class="missing">⚠️ 该事件无地点行（Place 缺失 / needs_linking 未填）。</div>`;
  return e.places.map(p => `<div class="person-item"><div class="top"><b>${es(p.name || "(未命名)")}</b>
    ${p.status === "linked" ? `<span class="badge b-ok">linked 已确认</span>` : `<span class="badge b-warn">needs_linking 待关联</span>`}</div>
    ${p.note ? `<div class="meta">备注：${es(p.note)}</div>` : ""}</div>`).join("");
}
function evidenceHTML(evs, srcRef) {
  // 区分「数据来源 / Provenance」(source_*) 与「史料线索 / Historical Evidence」
  if (!evs || !evs.length) {
    // legacy source_reference 里若已含史料暗示，则非“完全无证据”
    const hint = (srcRef && /史料|原文|证据|historical|evidence/i.test(srcRef)) ?
      ` <div class="meta">史料线索见 source_reference：${es(srcRef)}</div>` : "";
    return `<div class="missing">正式原文证据 EventEvidence 尚未建立</div>${hint}`;
  }
  return `<table><tr><th>文献</th><th>篇/卷</th><th>章节</th><th>关键词</th><th>角色</th></tr>` +
    evs.map(v => `<tr><td>${es(v.work)}</td><td>${es(v.term)}</td><td>${es(v.chapter)}</td><td>${es(v.keywords)}</td><td>${es(v.role)}</td></tr>`).join("") + `</table>`;
}
function relationHTML(e) {
  // Relations reference stable canonical event IDs (never array indices),
  // so resolve them through DATA.eventsById, not DATA.events[<row/index>].
  const relChip = (rel, otherId, arrow) => {
    const ev = DATA.eventsById[otherId];
    if (!ev) return `<span class="chip">${es(rel)} ${arrow} ${es(otherId)} <span class="kbd">未解析</span></span>`;
    return `<span class="chip">${es(rel)} ${arrow} <a href="#/event/${encodeURIComponent(ev.id)}">${es(ev.name)}</a>` +
      `<span class="kbd">${es(ev.id)}${ev.start != null ? " · " + fmtYear(ev.start) : ""}</span></span>`;
  };
  const part = [];
  if (e.relations_in && e.relations_in.length)
    part.push(`<div class="person-item"><div class="meta"><b>前序来源 (rel-in)</b></div><div class="top">` +
      e.relations_in.map(r => relChip(r.rel, r.source, "←")).join(" ") + `</div></div>`);
  if (e.relations_out && e.relations_out.length)
    part.push(`<div class="person-item"><div class="meta"><b>后继去向 (rel-out)</b></div><div class="top">` +
      e.relations_out.map(r => relChip(r.rel, r.target, "→")).join(" ") + `</div></div>`);
  if (!part.length) part.push(`<div class="missing">无关联事件（EventRelation 缺失）。</div>`);
  return part.join("");
}
function srcHTML(e) {
  let ids = "";
  try { ids = JSON.parse(e.source_ids || "[]").join(", "); } catch (err2) { ids = e.source_ids || ""; }
  return `<div class="person-item">
    <div class="meta"><b>source_type</b> · ${es(e.source_type || "—")}</div>
    <div class="meta"><b>source_reference</b> · ${es(e.source_reference || "—")}</div>
    <div class="meta"><b>source_ids</b> · <span class="mono">${es(ids)}</span></div></div>`;
}
function detailHTML(e) {
  const peopleBlock = (e.persons && e.persons.length)
    ? e.persons.map(personItemHTML).join("")
    : `<div class="missing">⚠ 该事件无 EventPerson 关联（人物缺失）。</div>`;
  return `<button class="detail-close" title="关闭">✕</button>
    <h2>${es(e.name)} ${impBadge(e)}</h2>
    <div class="detail-id">${es(e.id)}</div>
    <div class="muted" style="margin:6px 0">${fmtDate(e)} · ${es(periodName(e.period_id))} · 政权 ${es(regimeNames(e.regime_ids))}</div>
    <h4>基本信息</h4><dl class="kv">
      <dt>name</dt><dd>${es(e.name)}</dd>
      <dt>name_raw</dt><dd>${es(e.name_raw || "—")}</dd>
      <dt>type</dt><dd>${es(e.type || "—")}</dd>
      <dt>start / end</dt><dd>${fmtDate(e)} (${es(e.date_precision || "—")})</dd>
      <dt>importance</dt><dd>${es(e.importance || "—")}</dd>
      <dt>quality</dt><dd>${es(e.quality || "—")}</dd>
      <dt>period_id</dt><dd>${es(e.period_id)}</dd>
      <dt>regime_ids</dt><dd>${es(JSON.stringify(e.regime_ids || []))}</dd></dl>
    <h4>摘要 summary</h4><div>${es(e.summary || `<i class="none">（无摘要）</i>`)}</div>
    <h4>背景 background</h4><div>${e.background ? es(e.background) : `<i class="none">（库内 background 为空 — 见 ANOMALIES）</i>`}</div>
    <h4>结果 result</h4><div>${e.result ? es(e.result) : `<i class="none">（库内 result 为空）</i>`}</div>
    <h4>人物与会者（${fmtN(e.persons ? e.persons.length : 0)}）</h4>${peopleBlock}
    <h4>地点 places（${fmtN(e.places ? e.places.length : 0)}）</h4>${placeHTML(e)}
    <h4>数据来源 / Provenance</h4>${srcHTML(e)}
    <h4>史料线索 / Historical Evidence</h4>${evidenceHTML(e.evidences, e.source_reference)}
    <h4>事件关联 EventRelation</h4>${relationHTML(e)}
    <h4>原始记录 Raw JSON</h4><pre class="json" id="raw-json"></pre>`;
}

/* ------------------------------------------------------------- samples */
const VKEY = "hdpp-verdicts-v1";
let currentSampleIdx = 0;
function getVerdicts() { try { return JSON.parse(localStorage.getItem(VKEY) || "{}"); } catch (e3) { return {}; } }
function setVerdict(id, v) { const o = getVerdicts(); o[id] = v; localStorage.setItem(VKEY, JSON.stringify(o)); }
function renderSamples(app) {
  const idx = currentSampleIdx >= 0 ? currentSampleIdx : (DATA.samples.length ? 0 : -1);
  const V = getVerdicts();
  let h = `<h2 class="section-title">15 个验收样本 · Acceptance Samples（ID 从库内查询）</h2>
    <div class="message">⚠ 左侧为 15 个代表事件（含 武王伐纣、秦统一、长平之战、赤壁、淝水、玄武门之变、安史之乱、靖康、崖山、鄱阳湖、土木堡、鸦片战争、甲午、武昌起义、新中国成立），
    右侧逐项验收并给出「可用 / 数据不足 / 待验收」，只存于浏览器 localStorage，不写入数据。</div>
    <div class="samples-wrap"><div class="sample-list">`;
  DATA.samples.forEach((s, i) => {
    const ev = DATA.eventsById[s.id] || DATA.events[s.index];
    if (!ev) return;
    const v = V[s.id] || "pending";
    const cls = v === "ok" ? "b-ok" : v === "bad" ? "b-crit" : "b-warn";
    h += `<button class="sample-it ${i === idx ? "active" : ""}" onclick="selectSample(${i})">
      <div class="nm">${i + 1}. ${es(s.name)}</div>
      <div class="st">${es(s.label || "")} · ${fmtDate(ev)} · <span class="badge ${cls}">${v}</span></div>
    </button>`;
  });
  h += `</div><div id="sample-detail"></div></div>`;
  app.innerHTML = h;
  renderSampleDetail(Math.max(0, idx));
}
function selectSample(i) {
  if (!DATA.samples[i]) return;
  currentSampleIdx = i;
  location.hash = "#/sample/" + i;
  renderSamples(document.getElementById("app"));
}
function renderSampleDetail(i) {
  const s = DATA.samples[i];
  const el = document.getElementById("sample-detail");
  if (!s || !el) return;
  const ev = DATA.eventsById[s.id] || DATA.events[s.index];
  if (!ev) { el.innerHTML = `<div class="none">未找到该样本事件。</div>`; return; }
  const v = getVerdicts()[s.id] || "pending";
  el.innerHTML = `<div class="card">
    <div class="muted">${es(s.id)} · 数组 index ${s.index}</div>
    <h2>${es(ev.name)} ${impBadge(ev)}</h2>
    <div class="muted">${fmtDate(ev)} · ${es(periodName(ev.period_id))}</div>
    <div class="summary" style="margin:8px 0">${es(ev.summary || "")}</div>
    <div class="verdict">
      <button class="${v === "ok" ? "on-ok" : ""}" onclick="setVerdict('${s.id}','ok');renderSampleDetail(${i})">✓ 可用</button>
      <button class="${v === "bad" ? "on-bad" : ""}" onclick="setVerdict('${s.id}','bad');renderSampleDetail(${i})">✗ 数据不足</button>
      <button class="${v === "pending" ? "on-pending" : ""}" onclick="setVerdict('${s.id}','pending');renderSampleDetail(${i})">⏳ 待验收</button>
    </div>
    <h4>人员（${ev.persons ? ev.persons.length : 0}）</h4>
    ${(ev.persons && ev.persons.length) ? ev.persons.map(personItemHTML).join("") : `<div class="missing">无人员</div>`}
    <h4>Source</h4>${srcHTML(ev)}
    <h4>关联</h4>${relationHTML(ev)}
    <h4>原始 JSON</h4><pre class="json">${es(JSON.stringify(ev, null, 2))}</pre>
  </div>`;
}

/* -------------------------------------------------------------- people */
function renderPeople(app) {
  const pl = DATA.person_linking || {};
  const byKind = pl.unique_by_kind || {};
  const kMax = Math.max(0, ...Object.values(byKind));
  const tops = pl.top_persons || [];
  let h = `<h2 class="section-title">人物关联统计 · Person Linking</h2>
    <div class="grid-cards">
      <div class="stat major"><div class="num">${fmtN(pl.total_event_person)}</div><div class="lab">EventPerson 行</div></div>
      <div class="stat"><div class="num">${fmtN(pl.unique_persons ? pl.unique_persons.length : 0)}</div><div class="lab">唯一人物</div></div>
      <div class="stat"><div class="num">${fmtN(pl.events_with_person)}</div><div class="lab">含人物事件</div></div>
      <div class="stat"><div class="num">${fmtN(pl.events_without_person)}</div><div class="lab">无人物事件</div></div>
    </div>
    <div class="card"><h3>人物来源类型</h3>${Object.entries(byKind).map(([k, val]) => barRow(es(KIND_LABEL[k] || k), val, kMax)).join("")}</div>
    <div class="card"><h3>Top 30 人物（按事件数）</h3><table><tr><th>#</th><th>人物</th><th>来源</th><th>ID</th><th>事件数</th><th>生 / 卒</th></tr>` +
    tops.slice(0, 30).map((p, i) => `<tr><td>${i + 1}</td><td>${es(p.name)}</td><td>${kindBadge(p.kind || p.kind_label)}</td><td class="mono">${es(p.person_id)}</td><td>${fmtN(p.aggregate_events)}</td><td>${p.birth ? fmtYear(p.birth) : "—"} ~ ${p.death ? fmtYear(p.death) : "—"}</td></tr>`).join("") + `</table></div>`;
  h += `<div class="card"><h3>Top 事件（按人数）</h3><table><tr><th>事件</th><th>人数</th></tr>` +
    (pl.top_events_by_person || []).map(x => `<tr><td><a href="#/event/${encodeURIComponent(x.id)}">${es(x.name)}</a></td><td>${x.persons}</td></tr>`).join("") + `</table></div>`;
  app.innerHTML = h;
}

/* ------------------------------------------------------------ regimes */
function renderRegimes(app) {
  const byP = {};
  DATA.regime_tree.forEach(g => { byP[g.period_id] = g; });
  let h = `<h2 class="section-title">政权视图 · Regimes（按时期分组，Period ≠ Regime 设计）</h2>
    <div class="muted">说明：一个时期可对应一个或多个政权（如 三国=魏蜀吴；北宋+辽 并存；南宋+金 并存；五代十国等）。
    多政权并存行以紫色边框标识。</div>`;
  [...DATA.periods].sort((a, b) => (a.start || 0) - (b.start || 0)).forEach(p => {
    const g = byP[p.id];
    const rl = g ? g.regimes : [];
    const multi = rl.length > 1;
    h += `<div class="regime-period"><div style="display:flex;gap:10px;align-items:center">
      <b style="min-width:120px">${es(p.name)}</b><span class="kbd">${es(p.id)}</span>
      <span class="muted">${fmtYear(p.start)} → ${fmtYear(p.end)}</span>
      ${multi ? `<span class="badge b-warn">多政权并存 (${rl.length})</span>` : ""}
      </div><div class="top">${rl.length ? rl.map(r => {
        const subs = (r.sub || []).map(x => x.name).join(" / ");
        return `<span class="chip ${multi ? "multi" : ""}"><b>${es(r.name)}</b>${subs ? ` <span class="muted">(${es(subs)})</span>` : ""}</span>`;
      }).join(" ") : `<span class="muted">（本时期未设 regime）</span>`}</div>
      ${p.description ? `<div class="muted">${es(p.description)}</div>` : ""}</div>`;
  });
  app.innerHTML = h;
}

/* ---------------------------------------------------------- completeness */
function renderCompleteness(app) {
  const c = DATA.completeness || {};
  const COV = ["with_person", "with_place_row", "with_evidence", "with_relation", "with_source"];
  let h = `<h2 class="section-title">完整性 · Completeness</h2><div class="muted">按优先级统计已关联覆盖。</div>`;
  h += `<div class="card"><h3>总体 Overall</h3>${COV.map(k => barRow(k, c.overall[k], c.overall.total)).join("")}</div>`;
  ["critical", "major"].forEach(grp => {
    const d = c[grp] || {};
    h += `<div class="card"><h3>${grp}（${fmtN(d.total)}）</h3>${COV.map(k => barRow(k, d[k] || 0, d.total)).join("")}</div>`;
  });
  h += `<div class="card"><h3>时期分布</h3><table><tr><th>时期</th><th>Critical</th><th>Major</th><th>Normal</th><th>合计</th></tr>` +
    (c.per_period || []).map(p => `<tr><td>${es(p.name)}</td><td>${fmtN(p.critical)}</td><td>${fmtN(p.major)}</td><td>${fmtN(p.normal)}</td><td><b>${fmtN(p.total)}</b></td></tr>`).join("") + `</table></div>`;
  h += `<div class="card"><h3>每百年事件密度</h3>${histogram(DATA.timeline.per_100)}</div>`;
  h += `<div class="two-col"><div class="card"><h3>事件类型分布</h3>${(c.type_dist || []).map(t => barRow(es(t.type), t.count, (c.type_dist || [])[0].count)).join("")}</div>`;
  h += `<div class="card"><h3>Source 类型分布</h3>${(c.source_dist || []).map(t => barRow(es(t.source), t.count, (c.source_dist || [])[0].count)).join("")}</div></div>`;
  app.innerHTML = h;
}
/* ------------------------------------------------------------- reports */
function renderReports(app) {
  let h = `<h2 class="section-title">自动报告</h2><div class="muted">由 build_preview.py 自动生成（READ ONLY），与仓库内 reports/ 相同内容。</div>`;
  h += `<div class="card"><h3>HISTORY_DATA_PRODUCT_VALIDATION.md</h3><pre class="report" id="report-val">加载中…</pre></div>`;
  h += `<div class="card"><h3>HISTORY_PRODUCT_DATA_ANOMALIES.md</h3><pre class="report" id="report-anom">加载中…</pre></div>`;
  app.innerHTML = h;
  fetch("data/report_validation.md").then(r => r.text()).then(t => { document.getElementById("report-val").textContent = t; });
  fetch("data/report_anomalies.md").then(r => r.text()).then(t => { document.getElementById("report-anom").textContent = t; });
}

/* ================================================================= boot */
async function loadAll() {
  const files = ["overview.json", "events.json", "periods.json", "regimes.json",
    "completeness.json", "person_linking.json", "timeline.json",
    "regime_tree.json", "people.json", "samples.json", "relations.json"];
  const loaded = await Promise.all(files.map(f => fetch("data/" + f).then(r => r.json())));
  [DATA.overview, DATA.events, DATA.periods, DATA.regimes, DATA.completeness,
   DATA.person_linking, DATA.timeline, DATA.regime_tree, DATA.people, DATA.samples, DATA.relations] = loaded;
  DATA.eventsById = {}; DATA.personById = {}; DATA.periodById = {}; DATA.regimeById = {};
  DATA.events.forEach(e => { DATA.eventsById[e.id] = e; });
  DATA.periods.forEach(p => { DATA.periodById[p.id] = p; });
  DATA.regimes.forEach(r => { DATA.regimeById[r.id] = r; });
  (DATA.people || []).forEach(p => { DATA.personById[p.person_id] = p; });
  DATA.regime_tree = DATA.regime_tree || [];
  const gates = document.getElementById("gates");
  if (gates && DATA.overview.gates) {
    gates.innerHTML = Object.entries(DATA.overview.gates)
      .map(([k, v]) => `<div>${es(k)} = <b>${v ? "TRUE" : "false"}</b></div>`).join("");
    gates.classList.add("on");
  }
}
function boot() {
  document.querySelectorAll("#tabs .tab").forEach(b =>
    b.addEventListener("click", () => { location.hash = "#/" + b.dataset.tab; }));
  window.addEventListener("hashchange", route);
}
async function app() {
  await loadAll();
  route();
}

// boot inside DOM ready; boot() only binds events, safe to call after parse,
// but guard for elements. We attach after DOM ready via script at end of body.
boot();
if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", app);
else app();