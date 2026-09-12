"""Source Expansion Batch 01 — zh.wikisource raw snapshot 采集（Queue 5）。

政策依据：docs/source-acquisition-policy.md（remote → raw snapshot → checksum）。
- 只抓 manifest 列出的页；写入 data/raw/wikisource/<version>/，原始字节 immutable。
- 不做任何解析/清洗 —— wikitext 原样落盘；解析在 Queue 6 parser 中进行。
- 逐文件 sha256 + 尺寸写入 checksum.sha256 与 metadata.json。
- 幂等：重复执行对已存在文件不覆盖（--force 除外），快照目录不可变。

用法：
    .venv python scripts/acquire_wikisource_batch01.py --version 20260912
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
MANIFEST_PATH = ROOT / "config" / "wikisource_batch01_manifest.json"
API = "https://zh.wikisource.org/w/api.php"
USER_AGENT = "history-data-pipeline/0.2 (source-acquisition; contact: project maintainer)"


def _api_request(params: dict) -> dict:
    request = urllib.request.Request(API + "?" + urllib.parse.urlencode(params),
                                     headers={"User-Agent": USER_AGENT})
    delay = 5.0
    for attempt in range(5):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            if error.code == 429 and attempt < 4:
                print(f"  [429 rate-limited] retry in {delay:.0f}s …")
                time.sleep(delay)
                delay *= 2
                continue
            raise
    raise RuntimeError("unreachable")


def api_raw_wikitext(title: str) -> tuple[str, str]:
    """取指定页当前修订的原始 wikitext；返回 (content, resolved_title)。"""
    params = {
        "action": "query",
        "prop": "revisions",
        "titles": title,
        "rvslots": "main",
        "rvprop": "content",
        "redirects": 1,
        "format": "json",
        "formatversion": 2,
    }
    data = _api_request(params)
    page = data["query"]["pages"][0]
    if "missing" in page:
        raise RuntimeError(f"页面不存在: {title}")
    revision = page["revisions"][0]
    return revision["slots"]["main"]["content"], page["title"]


def api_rendered_html(title: str) -> tuple[str, str]:
    """取渲染 HTML（展开 <pages> 扫描转写等）；仅当 wikitext 不含正文时使用。

    返回 (html, resolved_title)。HTML 仅为 PD 底本正文的载体形态，
    解析时按确定性规则抽取段落（Queue 7 校验模板残留）。
    """
    params = {
        "action": "parse",
        "page": title,
        "prop": "text",
        "redirects": 1,
        "format": "json",
        "formatversion": 2,
    }
    data = _api_request(params)
    parse = data["parse"]
    return parse["text"], parse["title"]


def detect_format(content: str) -> str:
    """从内容探测形态（渲染 HTML 以块级标签开头为特征；wikitext 以模板/文本开头）。"""
    head = content.lstrip()[:60].lower()
    if head.startswith(("<!doctype", "<html", "<div", "<section")) \
            or "mw-parser-output" in content[:8000]:
        return "html_rendered"
    return "wikitext"


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", required=True, help="快照版本目录名，如 20260912")
    parser.add_argument("--force", action="store_true", help="覆盖已存在文件（默认拒绝）")
    args = parser.parse_args()

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    snapshot = ROOT / "data" / "raw" / "wikisource" / args.version
    pages_dir = snapshot / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)

    acquired_at = dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    records = []
    for page in manifest["pages"]:
        target = snapshot / page["file"]
        if target.exists() and not args.force:
            content = target.read_text(encoding="utf-8")
            resolved = page["title"]
            fmt = detect_format(content)
            print(f"[keep-existing/{fmt}] {page['title']} -> {page['file']}")
        else:
            raw_probe, resolved = api_raw_wikitext(page["title"])
            if "<pages " in raw_probe:
                # 扫描件转写页：wikitext 无正文，取渲染 HTML（展开转写）
                content, resolved = api_rendered_html(page["title"])
                print(f"[fetched {len(content):>7} chars/html] {page['title']} -> {page['file']}")
            else:
                content, resolved = raw_probe, resolved
                print(f"[fetched {len(content):>7} chars] {page['title']} -> {page['file']}")
            target.write_text(content, encoding="utf-8")
            fmt = detect_format(content)
        records.append({
            **page,
            "resolved_title": resolved,
            "fetch_format": fmt,
            "download_url": API + "?" + urllib.parse.urlencode({
                "action": "query", "prop": "revisions", "titles": page["title"],
                "rvslots": "main", "rvprop": "content", "format": "json", "formatversion": 2,
            }),
            "sha256": sha256_of(target),
            "size_bytes": target.stat().st_size,
            "encoding": "utf-8",
            "format": "text/x-wikitext" if fmt == "wikitext" else "text/html",
        })


    (snapshot / "checksum.sha256").write_text(
        "".join(f"{r['sha256']}  {r['file']}\n" for r in records), encoding="utf-8")
    metadata = {
        "source_id": manifest["source_id"],
        "dataset": manifest["dataset"],
        "manifest_version": manifest["manifest_version"],
        "manifest": "config/wikisource_batch01_manifest.json",
        "policy": manifest["policy"],
        "source_url": "https://zh.wikisource.org/",
        # backbone build _ensure_sources 读取以下两个键自动注册 source 行
        "version": args.version,
        "license": manifest.get("license_summary"),
        "acquired_at": acquired_at,
        "snapshot_version": args.version,
        "acquisition_tool": "scripts/acquire_wikisource_batch01.py",
        "user_agent": USER_AGENT,
        "carrier_license_note": manifest["carrier"]["license_note"],
        "pages": records,
    }
    (snapshot / "metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\nsnapshot: {snapshot}")
    print(f"pages: {len(records)} | checksum.sha256 + metadata.json written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
