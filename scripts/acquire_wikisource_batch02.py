"""Source Batch 02 — 清史稿/晋书/旧唐书 目标卷采集（长任务 Phase A）。

政策同 docs/source-acquisition-policy.md：remote → raw snapshot → checksum → parser。
快照版本：data/raw/wikisource/20260912b/（与 batch01 20260912 并存，parser 支持多快照）。
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API = "https://zh.wikisource.org/w/api.php"
USER_AGENT = "history-data-pipeline/0.2 (source-acquisition; contact: project maintainer)"

# (title, file, 底本层级 hint)
PAGES: list[tuple[str, str]] = [
    # 清史稿 · 本纪
    ("清史稿/卷2",   "pages/qsg_002_taizong_1.wikitext"),
    ("清史稿/卷3",   "pages/qsg_003_taizong_2.wikitext"),
    ("清史稿/卷17",  "pages/qsg_017_xuanzong_1.wikitext"),
    ("清史稿/卷18",  "pages/qsg_018_xuanzong_2.wikitext"),
    ("清史稿/卷19",  "pages/qsg_019_xuanzong_3.wikitext"),
    ("清史稿/卷20",  "pages/qsg_020_wenzong.wikitext"),
    ("清史稿/卷21",  "pages/qsg_021_muzong_1.wikitext"),
    ("清史稿/卷22",  "pages/qsg_022_muzong_2.wikitext"),
    ("清史稿/卷23",  "pages/qsg_023_dezong_1.wikitext"),
    ("清史稿/卷24",  "pages/qsg_024_dezong_2.wikitext"),
    ("清史稿/卷25",  "pages/qsg_025_xuantong.wikitext"),
    # 清史稿 · 列传
    ("清史稿/卷405", "pages/qsg_405_zengguofan.wikitext"),
    ("清史稿/卷411", "pages/qsg_411_lihongzhang.wikitext"),
    ("清史稿/卷412", "pages/qsg_412_zuozongtang.wikitext"),
    ("清史稿/卷474", "pages/qsg_474_wusangui.wikitext"),
    ("清史稿/卷475", "pages/qsg_475_hongxiuquan.wikitext"),
    # 晋书（补 NiuTrans 缺卷；work→work-curated-jinshu）
    ("晉書/卷003",  "pages/js_003_wudi.wikitext"),
    ("晉書/卷005",  "pages/js_005_mindi.wikitext"),
    ("晉書/卷006",  "pages/js_006_yuandi.wikitext"),
    ("晉書/卷042",  "pages/js_042_wangjun.wikitext"),
    ("晉書/卷059",  "pages/js_059_bawang.wikitext"),
    ("晉書/卷079",  "pages/js_079_xiexuan.wikitext"),
    ("晉書/卷103",  "pages/js_103_liuyao.wikitext"),
    ("晉書/卷113",  "pages/js_113_fujian_1.wikitext"),
    ("晉書/卷114",  "pages/js_114_fujian_2.wikitext"),
    # 旧唐书（补缺卷；work→work-curated-jiutangshu）
    ("舊唐書/卷19下",  "pages/jts_019b_xizong.wikitext"),
    ("舊唐書/卷194上", "pages/jts_194a_tujue.wikitext"),
    ("舊唐書/卷200下", "pages/jts_200b_huangchao.wikitext"),
]


def _api(params: dict) -> dict:
    request = urllib.request.Request(API + "?" + urllib.parse.urlencode(params),
                                     headers={"User-Agent": USER_AGENT})
    delay = 5.0
    for attempt in range(6):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            if error.code == 429 and attempt < 5:
                print(f"  [429] retry in {delay:.0f}s", flush=True)
                time.sleep(delay)
                delay *= 2
                continue
            raise
    raise RuntimeError("unreachable")


def fetch(title: str) -> str:
    data = _api({"action": "query", "prop": "revisions", "titles": title, "rvslots": "main",
                 "rvprop": "content", "redirects": 1, "format": "json", "formatversion": 2})
    page = data["query"]["pages"][0]
    if "missing" in page:
        raise RuntimeError(f"页面不存在: {title}")
    return page["revisions"][0]["slots"]["main"]["content"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", default="20260912b")
    args = parser.parse_args()
    snapshot = ROOT / "data" / "raw" / "wikisource" / args.version
    (snapshot / "pages").mkdir(parents=True, exist_ok=True)
    acquired_at = dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    records = []
    for title, rel in PAGES:
        target = snapshot / rel
        if target.exists():
            print(f"[keep] {title}")
        else:
            content = fetch(title)
            target.write_text(content, encoding="utf-8")
            print(f"[{len(content):>7}] {title} -> {rel}", flush=True)
            time.sleep(1.6)
        records.append({
            "title": title, "file": rel,
            "resolved_title": title,
            "fetch_format": "wikitext",
            "download_url": API + "?" + urllib.parse.urlencode(
                {"action": "query", "prop": "revisions", "titles": title, "rvslots": "main",
                 "rvprop": "content", "format": "json", "formatversion": 2}),
            "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
            "size_bytes": target.stat().st_size,
            "encoding": "utf-8",
            "format": "text/x-wikitext",
            "license": "public_domain",
            "canonical_use": "allowed",
        })
    (snapshot / "checksum.sha256").write_text(
        "".join(f"{r['sha256']}  {r['file']}\n" for r in records), encoding="utf-8")
    metadata = {
        "source_id": "source-wikisource", "dataset": "wikisource", "version": args.version,
        "acquired_at": acquired_at, "acquisition_tool": "scripts/acquire_wikisource_batch02.py",
        "source_url": "https://zh.wikisource.org/",
        "license": "底本判定：清史稿（民国官修，PD）/ 晋书（唐修，PD）/ 旧唐书（五代修，PD）；载体排版 CC BY-SA 不改变底本判定",
        "batch": "batch02-qingshigao-jinshu-jiutangshu",
        "pages": records,
    }
    (snapshot / "metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
                                             encoding="utf-8")
    print(f"snapshot: {snapshot} | pages: {len(records)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
