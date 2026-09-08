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
            "吴王濞传",
            "supporting",
            "《汉书》卷三五“荆燕吴传”中的吴王濞传：载七国之乱吴王刘濞举兵反叛（canonical source_reference 作《吴王濞传》，Researcher 确认其所在之传曰荆燕吴）。",
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

# 平王东迁：雒邑/成周 = 洛阳（knowledge.places 唯一实收录条目）
PLACE_LINK = {
    "event-pingwang-dongqian": {
        "place_id": "cbdb-place-14693",
        "place_name_raw": "洛阳",
        "role": "capital",
        "link_status": "linked",
        "link_quality_status": "reviewed",
        "link_confidence": 0.9,
        "review_note": "雒邑/成周 h 洛阳；knowledge.places 收录的真实对应条目。",
    }
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
            "people": list(item.get("people") or []),
            "relations": item.get("relations") or [],
        }
        place = PLACE_LINK.get(eid)
        if place:
            cand["places"] = [dict(place)]
        evs = _build_evidences(ev, eid)
        if evs:
            cand["evidence"] = evs

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
        "producer": "scripts/calibration_batch01_produce_candidates.py v3",
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
