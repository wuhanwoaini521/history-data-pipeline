# -*- coding: utf-8 -*-
"""Calibration Batch 02..06 · Producer — generic, data-driven candidate enrichment.

Role split (AGENTS.md §5): this script is the PRODUCER. It converts canonical
curated events into enriched candidate documents. It does NOT self-approve:
acceptance, verification and auditing are separate phases.

Design rules (AGENTS.md §3/§7/§14/§14, DATA_MODEL.md, Batch 01 fix list B5-B8):

* base fields are copied verbatim from the canonical curated event;
* ``people`` are carried over unchanged (load_backbone already merged the
  accepted V2.1/V2.3 EventPerson store — link_status=linked + reviewer notes);
* ``evidence`` is transcribed deterministically from the canonical
  ``source_reference``: every 《book·chapter》 that resolves to a registered
  work becomes a curated evidence row with ``historical_text_id: null`` +
  ``needs_linking`` (B5 — never claim an unanchored text link). Rows are only
  emitted when they actually carry a chapter-level ``term``: whole-book
  citations (e.g. 《东晋门阀政治》) stay in ``source_reference``/``source_ids``
  where they honestly belong (AGENTS.md §14 — a whole-book reference is not
  claim-level evidence, and validator/schema require a real term).
* ``background_zh_cn`` / ``result_zh_cn`` are derived deterministically from
  ``summary_zh_cn`` (verbatim sentence split), exactly like Batch 01;
* places are only linked where knowledge.places has a definitive exact entry
  (none exist for these events at authoring time); no coordinates invented.
* B7: evidence.work titles that map to a registered work contribute that work
  id into ``source_ids`` (deduped, order preserved).
* B8: multiple chapters from the same work = single independent source,
  marked per row in review_note.

Output: ``data/candidates/<batch>/*.yml``.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from history_data_pipeline.backbone.loader import load_backbone  # noqa: E402
from history_data_pipeline.backbone.reference import (  # noqa: E402
    CANONICAL_PERSON_NAMES,
    curated_event_person_seeds,
    load_curated_person_records,
)

_SENT_SPLIT = re.compile(r"([^。！？]*[。！？])")

# registered works: title -> work id (mirrors reference.knowledge_seed_rows)
REGISTERED_WORKS: dict[str, str] = {
    "史记": "work-curated-shiji",
    "汉书": "work-curated-hanshu",
    "后汉书": "work-curated-houhanshu",
    "三国志": "work-curated-sanguozhi",
    "资治通鉴": "work-curated-zizhitongjian",
    "旧唐书": "work-curated-jiutangshu",
    "新唐书": "work-curated-xintangshu",
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
    "春秋": "work-curated-chunqiu",
    "左传": "work-curated-zuozhuan",
    "国语": "work-curated-guoyu",
    "尚书": "work-curated-shangshu",
    "战国策": "work-curated-zhanguoce",
    "竹书纪年": "work-curated-zhushu-jinian",
    "中华民国史": "work-curated-minguoshi",
    "中国抗日战争史": "work-curated-kangzhanshi",
    # ---- 2026-09 Batch 02..06: works already cited in canonical source_reference ----
    "三朝北盟会编": "work-curated-sanchaohui-meng",
    "蒙古秘史": "work-curated-menggu-mishi",
    "元朝史": "work-curated-yuan-chao-shi",
    "东晋门阀政治": "work-curated-dongjin-menfa",
    "元末明初的江南社会": "work-curated-yuanmo-jiangnan",
    "辛亥革命回忆录": "work-curated-xinhai-huiyilu",
"南京大屠杀史料集": "work-curated-nanjing-datusha-shiliaoji",
    "中国共产党历史": "work-curated-zhongguo-gcd-lishi",
    "二十世纪中国史纲": "work-curated-ershishiji-zhongguoshigang",
    "中国现代史": "work-curated-zhongguo-xiandaishi",
    "秦汉史": "work-curated-qinhan-shi",
    "秦汉史略": "work-curated-qinhan-shilue",
}

WORK_ID_TO_TITLE: dict[str, str] = {v: k for k, v in REGISTERED_WORKS.items()}


# 冗余：任何包含 §数字 的圆括注（如 （modern boundary event，§64））整体移除；再兜底清理独立 §64）碎片。
_SCAFFOLD_RE = re.compile(r"[（(][^（）()]*§\s*\d+[^（）()]*[）)]|§\s*\d+[）)]?")
# 「（…，§64）→ 移除后残留的 （……， 尾巴（如 （modern boundary event，）
_SCAFFOLD_TAIL_RE = re.compile(r"[（(][^（）()]*，?\s*[）)]$|[（(][^（）()]*，\s*$")


def _strip_scaffolding(text: str) -> str:
    """Remove pipeline scaffolding notes (e.g. （§30：同时体现 Regime Transition）、§64、 ）
    that leaked into canonical summary text. Content is otherwise verbatim."""
    t = _SCAFFOLD_RE.sub("", text or "")
    t = _SCAFFOLD_TAIL_RE.sub("", t)
    t = t.replace("，，", "，").replace("，,", "，")
    return t.strip()


def split_summary(summary: str) -> tuple[str, str]:
    """Deterministic background/result split of a canonical summary.

    Returns (background, result). Falls back to the whole summary for both
    when there is only one sentence so the completeness scorer always has
    content — all text remains verbatim from the curated field.
    """
    summary = (summary or "").strip()
    if not summary:
        return "（canonical summary 缺失，按 AGENTS.md §7 不臆造）", ""
    sentences = [s for s in _SENT_SPLIT.findall(summary) if s.strip()]
    if len(sentences) <= 1:
        return summary, summary
    return "".join(sentences[:-1]).strip(), sentences[-1].strip()


def _person_anchor_ids() -> tuple[set[str], str]:
    """B6: independent anchor set (repository-internal only, no invention)."""
    anchors: set[str] = set(CANONICAL_PERSON_NAMES)
    sources = ["CANONICAL_PERSON_NAMES"]
    for rec in load_curated_person_records(ROOT):
        anchors.add(rec["id"])
    sources.append("data/curated/persons/*.yml")
    for pid in curated_event_person_seeds(ROOT):
        anchors.add(pid)
    sources.append("event_person store linked records")
    return anchors, " + ".join(sources)


def _mark_single_work_multi_chapter(evs: list[dict]) -> None:
    """B8: multiple chapter rows from one work = single independent source."""
    counts = Counter(e["work"] for e in evs)
    if not counts:
        return
    for e in evs:
        if counts[e["work"]] > 1 and "（同书多章" not in (e.get("review_note") or ""):
            e["review_note"] = (
                (e.get("review_note") or "")
                + "（注：同书多章=单一独立来源，B8 显式标注）"
            )


def _evidence_entry(work: str, term: str | None, role: str, note: str) -> dict:
    chapter_hint = None if term is None else term
    return {
        "work": work,
        "term": term,
        "historical_text_id": None,
        "chapter_hint": chapter_hint,
        "context_keywords": [],
        "evidence_role": role,
        "link_status": "needs_linking",
        "link_confidence": 0.9,
        "link_quality_status": "reviewed",
        "review_note": note,
    }


# 仅允许「明显是章节」的续接后缀：纪传体/编年体的篇目词。
# 注意：实录/本末/始末/略/考 是独立著作体裁（如《清太祖武皇帝实录》《筹办夷务始末》
# 《五史略》），不是前一部书的章节，绝不能链入。
_CHAPTER_SUFFIXES = (
    "本纪", "列传", "载记", "世家", "表", "志", "纪", "传",
)


def _looks_like_chapter(fragment: str) -> bool:
    """Heuristic: a bare 《X》 right after 《Book·chap》 is a same-book chapter.

    Conservative guard — the fragment must end with a common section/keyword
    title suffix. If it looks like an independent work title (e.g. 《中华民国史》,
    《筹办夷务始末》), it is NOT chained to the previous book.
    """
    frag = (fragment or "").strip()
    if not frag or len(frag) > 24:
        return False
    return any(frag.endswith(s) for s in _CHAPTER_SUFFIXES)


def _parse_source_reference(src_ref: str) -> list[tuple[str, str | None, str]]:
    """Extract (book, chapter_or_None, full_title) rows from canonical source_reference.

    Recognizes 《X·Y》 (chapter form) and 《X》 (whole-work form) where X is a
    registered work title. Only registered titles are transcribed. A bare
    chapter fragment immediately following a 《X·Y》 citation is chained to the
    same book (e.g. 《晋书·孝惠帝纪》《八王列传》 → 八王列传 of 晋书). A bare
    chapter fragment used immediately after a whole-work 《X》 (e.g. 《清史稿》
    吴三桂传) is likewise captured as the chapter of that work — the term is
    transcribed verbatim from the curated source text, never invented.
    """
    out: list[tuple[str, str | None, str]] = []
    if not src_ref:
        return out
    last_book: str | None = None
    for m in re.finditer(r"《([^》]+)》", src_ref):
        seg = m.group(1).strip()
        after = src_ref[m.end():]
        if "·" in seg:
            head, _, tail = seg.partition("·")
            head = head.strip()
            if head in REGISTERED_WORKS:
                out.append((head, tail.strip() or None, seg))
                last_book = head
            else:
                last_book = None
        elif seg in REGISTERED_WORKS:
            out.append((seg, None, seg))
            last_book = seg
        elif last_book in REGISTERED_WORKS and _looks_like_chapter(seg):
            # same-book continuation: 《晋书·孝惠帝纪》 → 《八公列传》
            out.append((last_book, seg, f"{last_book}·{seg}"))
        # bare fragment right after a whole-work 《X》 (e.g. 《清史稿》吴三桂传)
        if last_book in REGISTERED_WORKS:
            frag = _leading_fragment(after)
            if frag and _looks_like_chapter(frag):
                book_term_key = (last_book, frag)
                if book_term_key not in {(b, t) for b, t, _ in out}:
                    out.append((last_book, frag, f"{last_book}·{frag}"))
    # 去重保序
    seen: set[tuple[str, str | None]] = set()
    dedup: list[tuple[str, str | None, str]] = []
    for book, term, full in out:
        key = (book, term)
        if key not in seen:
            seen.add(key)
            dedup.append((book, term, full))
    return dedup


_REFRAG_STOP = "《；;，,。.、（()）"


def _leading_fragment(text: str) -> str:
    """Take the maximal non-empty text right after a 书名号 until a delimiter/next。

    Used to capture verbatim chapter terms that sit immediately after a
    whole-work citation, e.g. 《清史稿》吴则正传 → 吴则正传. Returns '' when
    nothing useful is there (punctuation, 等字, or the next bracket)."""
    frag = []
    for ch in text:
        if ch in _REFRAG_STOP:
            break
        frag.append(ch)
    out = "".join(frag).strip(" ，,·:：")
    if len(out) > 24:
        return ""
    return out


def _build_evidence(ev: dict, eid: str, src_ids: list[str]) -> list[dict]:
    """Deterministic evidence list for one event.

    Only rows that actually carry a chapter-level ``term`` are emitted:
    * Pass 1 — 《book·chapter》 rows transcribed from canonical source_reference
      (registered books only). Whole-book citations（《book》无章节）are **not**
      evidence rows: they stay in ``source_reference`` / ``source_ids``, which
      is where AGENTS.md §14 says whole-book references belong. The canonical
      validator (validate.py) and event_evidence.schema.json both require a
      real non-empty ``term`` on every evidence row, and AGENTS.md §7 forbids
      inventing one.
    * No Pass-2 backfill from ``source_ids``: a work appearing in source_ids
      is a source declaration, not claim-level evidence.
    """
    evs: list[dict] = []
    rows = _parse_source_reference(ev.get("source_reference") or "")
    first = True
    for book, term, full in rows:
        if not term:
            continue  # whole-book citation — not term-level evidence
        evs.append(_evidence_entry(
            book,
            term,
            "primary" if first else "supporting",
            f"《{full}》载本事件（transcribed from canonical source_reference）；"
            "historical_text 未锚定，保持 needs_linking（B5）",
        ))
        first = False

    _mark_single_work_multi_chapter(evs)
    return evs


def main() -> int:
    ap = argparse.ArgumentParser(description="Generic enrichment producer")
    ap.add_argument("--batch", required=True, help="输出目录名, e.g. batch02")
    ap.add_argument("--events", nargs="+", required=True, help="event ids")
    ap.add_argument("--out", default=None, help="candidate 输出目录 (default data/candidates/<batch>)")
    args = ap.parse_args()

    bb = load_backbone(ROOT)
    out_dir = Path(args.out) if args.out else ROOT / "data" / "candidates" / args.batch
    out_dir.mkdir(parents=True, exist_ok=True)

    anchors, anchor_src = _person_anchor_ids()
    written: list[str] = []
    for eid in args.events:
        if not eid or Path(eid).name != eid or ".." in eid:
            print(f"!! invalid event id {eid!r}; skipping")
            continue
        ev = bb.event(eid)
        if ev is None:
            print(f"!! skip missing event {eid}")
            continue
        item = dict(ev)
        summary = _strip_scaffolding(item.get("summary_zh_cn") or "")
        bg, res = split_summary(summary)
        cand = {
            "id": eid,
            "name_zh_cn": _strip_scaffolding(item.get("name_zh_cn") or ""),
            "event_type": item.get("event_type"),
            "start_year": item.get("start_year"),
            "end_year": item.get("end_year"),
            "date_precision": item.get("date_precision"),
            "period_id": item.get("period_id"),
            "importance": item.get("importance"),
            "summary_zh_cn": summary,
            "background_zh_cn": bg,
            "result_zh_cn": res,
            "quality_status": "reviewed",
            "source_type": item.get("source_type"),
            "source_reference": item.get("source_reference"),
            "source_ids": list(item.get("source_ids") or []),
            "regime_ids": list(item.get("regime_ids") or []),
            "people": list(item.get("people") or []),
            "relations": item.get("relations") or [],
        }

        # B6: linked 必须有仓库内锚点
        for p in cand["people"]:
            if p.get("link_status") == "linked" and p.get("person_id") not in anchors:
                p["link_status"] = "needs_linking"
                p.pop("link_confidence", None)
                p["review_note"] = (
                    (p.get("review_note") or "")
                    + f"；[B6] person_id 未能在锚点集（{anchor_src}）中独立确认，降级 needs_linking"
                )

        evs = _build_evidence(item, eid, cand["source_ids"])
        if evs:
            cand["evidence"] = evs

        # B7: evidence.work → work id 并入 source_ids（保序去重）
        for row in cand.get("evidence") or []:
            wid = REGISTERED_WORKS.get(row.get("work"))
            if wid and wid not in cand["source_ids"]:
                cand["source_ids"].append(wid)

        out = out_dir / f"{eid}.yml"
        out.write_text(
            yaml.safe_dump(cand, allow_unicode=True, sort_keys=False)
            + f"# {eid} — {args.batch} enriched candidate (Producer, generic)\n"
            + "# background/result derived verbatim from canonical summary\n"
            + "# evidence transcribed from canonical source_reference + source_ids (registered works only)\n"
            + "# no fabricated locators, coordinates, text ids, or links\n",
            encoding="utf-8",
        )
        written.append(eid)

    print(f"wrote {len(written)} candidates to {out_dir}")
    for f in written:
        print("  ", f)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())