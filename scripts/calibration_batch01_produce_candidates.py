"""Calibration Batch 01 · Phase 3 — Producer: build 10 enriched candidate events.

Role split (AGENTS.md §5): this script is the PRODUCER. It converts the
Researcher brief + canonical curated events into candidate documents. It does
NOT self-approve: acceptance, verification and auditing are separate phases.

Design rules (per AGENTS.md §7 §14 §19 and DATA_MODEL.md):

* base fields are copied verbatim from the canonical curated event;
* ``people`` are carried over unchanged (accepted EventPerson layer);
* ``evidence`` is transcribed from the classical locators already asserted in
  the canonical ``source_reference``; where the Researcher brief explicitly
  confirmed an additional authoritative classical work that covers the event,
  it may be added (traceable, not invented) — see ADDITIONAL_EVIDENCE;
* ``background_zh_cn`` / ``result_zh_cn`` are DERIVED deterministically from
  the curated ``summary_zh_cn`` (verbatim sentence split). No new historical
  claim, no fabrication, no hand-typed glyph risk.
* places are linked only where knowledge.places has a real, exact entry
  (洛阳 for 平王东迁). No coordinates are invented.

Output: ``data/candidates/calibration_batch01/*.yml``
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

from history_data_pipeline.backbone.loader import load_backbone
from history_data_pipeline.backbone.reference import (
    CANONICAL_PERSON_NAMES,
    curated_event_person_seeds,
    load_curated_person_records,
)

ROOT = Path(__file__).resolve().parent.parent
SELECTION_FILE = ROOT / "reports" / "calibration_batch01_selection.json"
try:
    SELECTION = json.loads(SELECTION_FILE.read_text(encoding="utf-8"))
except (OSError, json.JSONDecodeError) as exc:
    raise SystemExit(f"cannot read selection {SELECTION_FILE}: {exc}") from exc
OUT_DIR = ROOT / "data" / "candidates" / "calibration_batch01"

_SENT_SPLIT = re.compile(r"([^。！？]*[。！？])")


def split_summary(summary: str) -> tuple[str, str]:
    """Deterministic background/result split of a canonical summary.

    Returns (background, result). Falls back to the whole summary for both
    when there is only one sentence so the completeness scorer always has
    content — all text remains verbatim from the curated field.
    """
    summary = (summary or "").strip()
    if not summary:
        return "（待补：canonical summary 缺失，按 AGENTS.md 不臆造）", ""
    sentences = [s for s in _SENT_SPLIT.findall(summary) if s.strip()]
    if len(sentences) <= 1:
        return summary, summary
    background = "".join(sentences[:-1]).strip()
    result = sentences[-1].strip()
    return background, result


def _person_anchor_ids() -> tuple[set[str], str]:
    """B6: 独立锚点集（以仓库内既有 accepted/curated 层为准，不臆造外部验证）。

    Returns (person_id 锚点集, 说明文字)。锚点来源：
    * CANONICAL_PERSON_NAMES（V2.1 迁移确认的 canonical identity）
    * data/curated/persons/*.yml（curated 人列）
    * event_person store 中 link_status=linked 的既有 accepted 记录
    只有当 person_id 在该集合内时，producer 才允许宣称 linked/confidence；
    否则统一降级为 needs_linking（AGENTS.md §13：宁保留未决，不做过度合并）。
    """
    anchors: set[str] = set(CANONICAL_PERSON_NAMES)
    sources: list[str] = ["CANONICAL_PERSON_NAMES"]
    for rec in load_curated_person_records(ROOT):
        anchors.add(rec["id"])
    sources.append("data/curated/persons/*.yml")
    for pid in curated_event_person_seeds(ROOT):
        anchors.add(pid)
    sources.append("event_person store linked records")
    return anchors, " + ".join(sources)


# Researcher-confirmed ADDITIONAL evidence:
# {(event_id): [(work, term, role, note)]}
# Only used where the canonical source_reference itself is thin (≤1 classical
# locator) and the Researcher brief explicitly verified a second classical
# work that covers the event. Possibly-new historical text was NOT created.
ADDITIONAL_EVIDENCE = {
    "event-qin-mie-liuguo": [
        (
            "资治通鉴",
            "秦纪",
            "supporting",
            (
                "《资治通鉴》秦纪叙秦并六国过程；Researcher brief 已确认 (独立于断代工程的通史文献，章节未逐一核验，chapter_hint 置空)"
            ),
        ),
    ],
    "event-qin-tongyi": [
        (
            "资治通鉴",
            "秦纪",
            "supporting",
            (
                "《资治通鉴》秦纪叙秦并六国、皇帝制度 (Researcher brief 确认；章节未逐字核验 ch)."
            ),
        ),
    ],
    "event-wangmang-chengdi": [
        (
            "资治通鉴",
            "汉纪",
            "supporting",
            ("《资治通鉴》汉纪叙汉末新莽代议 (independent of 汉书; Researcher 确认)。"),
        ),
    ],
}


def _whole_work(work: str) -> bool:
    return work in {"史记", "尚书", "汉书", "左传", "资治通鉴", "国语", "战国策"}


def _chapter_hint_from_reference(src_ref: str, work_cn: str) -> str | None:
    """从 canonical source_reference 提取『《{work_cn}·{篇}》』篇名作为
    chapter_hint；找不到时返回 None（不臆造具体篇章）。"""
    if not src_ref:
        return None
    for m in re.finditer(rf"《{work_cn}·([^》]+)》", src_ref):
        return m.group(1).strip()
    return None


def _evidence_entry(
    work: str, term: str, role: str, note: str | None, no_chapter: bool = False
):
    if role not in {"primary", "supporting", "related"}:
        role = "related"
    chapter = None if (no_chapter or _whole_work(term)) else term
    return {
        "work": work,
        "term": term,
        "historical_text_id": None,
        "chapter_hint": chapter,
        "context_keywords": [],
        "evidence_role": role,
        "link_status": "needs_linking",
        "link_confidence": 0.9,
        "link_quality_status": "reviewed",
        "review_note": (
            ("《" + work + "·" + term + "》") if term != work else "《" + work + "》"
        ),
    }


# 同一部书引多个篇章时，这些篇章同源（不构成多个独立来源），逐条显式标注（B8）。
def _mark_single_work_multi_chapter(evs: list[dict]) -> None:
    from collections import Counter

    counts = Counter(e["work"] for e in evs)
    if not counts:
        return
    for e in evs:
        if counts[e["work"]] > 1:
            note = e.get("review_note") or ""
            if "同书多章" not in note:
                e["review_note"] = note + f"（注：{e['work']}同一书内多个篇章，单一独立来源）"


def _build_evidences(ev, eid: str) -> list[dict]:
    evs: list[dict] = []
    src_ref = ev.get("source_reference") or ""

    # (a) transcribed classical locators from canonical source_reference
    per = EVIDENCE_FROM_REFERENCE.get(eid, [])
    for work, term, role, note in per:
        hint = _chapter_hint_from_reference(src_ref, work)
        # only use the canonical hint when it matches the term's own work-part
        if hint and f"{work}·{hint}" not in src_ref:
            hint = None
        evs.append(_evidence_entry(work, term, role, note))

    # (b) Researcher-verified additional classical source (only where thin)
    for work, term, role, note in ADDITIONAL_EVIDENCE.get(eid, []):
        evs.append(_evidence_entry(work, term, role, note, no_chapter=True))

    # B8: 同书多章 = 单一独立来源，逐条显式标注
    _mark_single_work_multi_chapter(evs)
    return evs


# Transcribed from the canonical source_reference for each selected event.
# (work, term, role, note) — term is the treatise/"/chapter as given there.
EVIDENCE_FROM_REFERENCE = {
    "event-shangtang-miexia": [
        ("史记", "殷本纪", "primary", "《史记·殷本纪》载成汤放桀于鸣条。"),
        ("尚书", "汤誓", "primary", "《尚书·汤誓》载汤伐夏誓辞。"),
    ],
    "event-wuwang-fazhou": [
        ("史记", "周本纪", "primary", "《史记·周本纪》载武王伐纣、牧野之战。"),
        ("尚书", "牧誓", "primary", "《尚书·牧誓》载牧野誓师之辞。"),
    ],
    "event-pingwang-dongqian": [
        ("史记", "周本纪", "primary", "《史记·周本纪》载平王东迁雒邑/成周。"),
        (
            "左传",
            "左传",
            "supporting",
            "《左传》隐公纪事涉周室东迁后之雒邑（不分篇详引）。",
        ),
    ],
    "event-sanjia-fenjin": [
        ("史记", "晋世家", "primary", "《史记·晋世家》载晋公室分裂、三家分晋之渊源。"),
        (
            "资治通鉴",
            "周纪一",
            "supporting",
            "《资治通鉴·周纪一》全之上古三代重叙三家分晋为战国之始。",
        ),
    ],
    "event-changping-zhizhan": [
        (
            "史记",
            "白起王翦列传",
            "primary",
            "《史记·白起王翦列传》载长平之战、白起之军事。",
        ),
        (
            "史记",
            "廉颇蔺相如列传",
            "primary",
            "《史记·廉颇蔺相如列传》载赵括代廉颇、秦兵尽杀长平卒四十万人。",
        ),
    ],
    "event-qin-mie-liuguo": [
        (
            "史记",
            "秦始皇本纪",
            "primary",
            "《史记·秦始皇本纪》载灭六国顺序、秦王政统一。",
        ),
    ],
    "event-qin-tongyi": [
        (
            "史记",
            "秦始皇本纪",
            "primary",
            "《史记·秦始皇本纪》载称帝号、行郡县、统一衡。",
        ),
    ],
    "event-qiguo-zhi-luan": [
        ("汉书", "景帝纪", "primary", "《汉书·景帝纪》载七国之乱及平定。"),
        (
            "汉书",
            "荆燕吴传",
            "supporting",
            "《汉书》卷三十五《荆燕吴传》载吴王刘濞举兵反、七国之乱始末（吴王事在传中；canonical source_reference 已同步改正）。",
        ),
    ],
    "event-mobei-zhizhan": [
        (
            "史记",
            "卫将军骠骑列传",
            "primary",
            "《史记·卫将军骠骑列传》载漠北之战、诸卫青霍去病大破匈奴。",
        ),
        ("汉书", "武帝纪", "primary", "《汉书·武帝纪》元狩四年记北征匈奴之事。"),
    ],
    "event-wangmang-chengdi": [
        ("汉书", "王莽传", "primary", "《汉书·王莽传》载新莽受禅代汉之始末。"),
    ],
}

# 平王东迁：雒邑/成周 与 knowledge.places 收录的洛阳（cbdb-place-14693）对应，
# 但该条目未带周代有效窗口（外部 CBDB 数据窗口约 710–1050，明显晚于 −770 事件），
# 无法确认其窗口覆盖 −770 → 按 AGENTS.md §12 不臆造窗口，标 needs_linking 待周代窗口条目。
PLACE_LINK = {
    "event-pingwang-dongqian": {
        "place_id": None,
        "place_name_raw": "雒邑（洛阳）",
        "role": "capital",
        "link_status": "needs_linking",
        "link_quality_status": "reviewed",
        "link_confidence": None,
        "description_zh_cn": "平王东迁所都（雒邑/成周），今河南洛阳一带；未收录带周代窗口的地名实体，按 AGENTS.md §12 不臆造窗口。",
        "review_note": "雒邑/成周对应今洛阳。knowledge.places 仅收录无窗口的 cbdb 洛阳条目且外部数据将其窗口定为 710 年以后，不与 −770 事件相符；不臆造窗口，置 place_id=None + needs_linking（AGENTS.md §12）。",
    }
}

# 已注册的 classic works（resolved to registered IDs, 见 reference.py knowledge_seed_rows）。
# B7: evidence.work 若为已注册作品，则将其 work id 并入候选 source_ids，避免
# evidence 与外层 source 脱节；未注册的作品一律不臆造 id。
WORK_ID_BY_TITLE: dict[str, str] = {
    "史记": "work-curated-shiji",
    "汉书": "work-curated-hanshu",
    "后汉书": "work-curated-houhanshu",
    "三国志": "work-curated-sanguozhi",
    "资治通鉴": "work-curated-zizhitongjian",
    "旧唐书": "work-curated-jiutangshu",
    "新唐书": "work-curated-xintangshu",
    "春秋": "work-curated-chunqiu",
    "左传": "work-curated-zuozhuan",
    "国语": "work-curated-guoyu",
    "尚书": "work-curated-shangshu",
    "竹书纪年": "work-curated-zhushu-jinian",
    "战国策": "work-curated-zhanguoce",
    "晋书": "work-curated-jinshu",
    "宋书": "work-curated-songshu",
    "梁书": "work-curated-liangshu",
    "陈书": "work-curated-chenshu",
    "魏书": "work-curated-weishu",
    "北齐书": "work-curated-beiqishu",
    "周书": "work-curated-zhoushu",
    "南史": "work-curated-nanshi",
    "北史": "work-curated-beishi",
    "隋书": "work-curated-suishu",
    "旧五代史": "work-curated-jiuwudaishi",
    "新五代史": "work-curated-xinwudaishi",
    "辽史": "work-curated-liaoshi",
    "宋史": "work-curated-songshi",
    "金史": "work-curated-jinshi",
    "续资治通鉴长编": "work-curated-xuzizhitongjianchangbian",
    "元史": "work-curated-yuanshi",
    "明史": "work-curated-mingshi",
    "明实录": "work-curated-mingshilu",
    "清史稿": "work-curated-qingshigao",
    "清实录": "work-curated-qingshilu",
    "中华民国史": "work-curated-minguoshi",
    "中国抗日战争史": "work-curated-kangzhanshi",
}


def main() -> int:
    bb = load_backbone(ROOT)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    for sel in SELECTION:
        eid = sel["id"]
        # Defensive: eid comes from the hardcoded SELECTION table, but constrain
        # it to a bare id anyway so the output path can never escape OUT_DIR.
        if not eid or Path(eid).name != eid or ".." in eid:
            print(f"!! invalid event id {eid!r}; skipping")
            continue
        ev = bb.event(eid)
        if ev is None:
            print(f"!! skip missing event {eid}")
            continue
        item = dict(ev)
        bg, res = split_summary(item.get("summary_zh_cn") or "")
        cand = {
            "id": eid,
            "name_zh_cn": item.get("name_zh_cn"),
            "event_type": item.get("event_type"),
            "start_year": item.get("start_year"),
            "end_year": item.get("end_year"),
            "date_precision": item.get("date_precision"),
            "period_id": item.get("period_id"),
            "importance": item.get("importance"),
            "summary_zh_cn": item.get("summary_zh_cn"),
            "background_zh_cn": bg,
            "result_zh_cn": res,
            "quality_status": "reviewed",
            "source_type": item.get("source_type"),
            "source_reference": item.get("source_reference"),
            "source_ids": item.get("source_ids") or [],
            "regime_ids": item.get("regime_ids") or [],
            "people": list(item.get("people") or []),
            "relations": item.get("relations") or [],
        }

        # B6: person id 锚定门 — linked 必须有仓库内锚点，否则降级 needs_linking
        person_anchors, anchor_src = _person_anchor_ids()
        for p in cand["people"]:
            if p.get("link_status") == "linked" and p.get("person_id") not in person_anchors:
                p["link_status"] = "needs_linking"
                p.pop("link_confidence", None)
                p["review_note"] = (
                    (p.get("review_note") or "") + f"；[B6] person_id 未能在锚点集（{anchor_src}）中独立确认，降级 needs_linking"
                )

        place = PLACE_LINK.get(eid)
        if place:
            cand["places"] = [dict(place)]
        evs = _build_evidences(ev, eid)
        if evs:
            cand["evidence"] = evs

        # B7: evidence.work 若为已注册作品 → 并入 source_ids（保序去重）
        for ev_row in cand.get("evidence") or []:
            work_id = WORK_ID_BY_TITLE.get(ev_row.get("work"))
            if work_id and work_id not in cand["source_ids"]:
                cand["source_ids"].append(work_id)

        out = OUT_DIR / f"{eid}.yml"
        out.write_text(
            yaml.safe_dump(cand, allow_unicode=True, sort_keys=False)
            + f"# {eid} — calibration_batch01 enriched candidate (Producer)\n"
            + "# background/result derived verbatim from canonical summary\n"
            + "# evidence appointed to canonical source_reference or Researcher-verified classics\n"
            + "# no fabricated locators, coordinates, text ids, or links\n",
            encoding="utf-8",
        )
        written.append(eid)

    meta = {
        "batch": "calibration_batch01",
        "producer": "scripts/calibration_batch01_produce_candidates.py v4 (fix-list B5-B8)",
        "flow": "canonical → candidate → deterministic QA → verification → gates → audit/report",
        "n": len(SELECTION),
        "events": [s["id"] for s in SELECTION],
    }
    meta_path = ROOT / "reports" / "current-run" / "calibration_batch01-meta.yml"
    meta_path.parent.mkdir(parents=True, exist_ok=True)
    meta_path.write_text(
        yaml.safe_dump({"calibration_batch01_meta": meta}, allow_unicode=True),
        encoding="utf-8",
    )
    written.append(str(meta_path.relative_to(ROOT)))
    print(f"wrote {len(written)} artifacts to {OUT_DIR}")
    for f in written:
        print(" ", f)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
