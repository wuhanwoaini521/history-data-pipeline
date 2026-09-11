"""Knowledge Layer 构建测试：解析层级 / ID 确定性 / 重复 build 幂等（Gate D）。"""

from __future__ import annotations

import json
from pathlib import Path

import duckdb
import pytest

from history_data_pipeline.config import PipelinePaths
from history_data_pipeline.knowledge_build import (
    build_knowledge_store,
    iter_bilingual_texts,
    iter_classical_texts,
)


@pytest.fixture()
def snapshot(tmp_path: Path) -> Path:
    """合成一个最小 NiuTrans 快照（双语数据 + 古文原文各一书）。"""
    snapshot_dir = tmp_path / "data" / "raw" / "classical-modern" / "20240421"
    bilingual = snapshot_dir / "repository" / "双语数据" / "测试正史" / "本纪" / "卷一"
    bilingual.mkdir(parents=True)
    (bilingual / "source.txt").write_text("太祖之法度森严。\n帝曰天下大乱。\n\n（空行不计）\n", encoding="utf-8")
    (bilingual / "target.txt").write_text("太祖的法度严整。\n皇帝说天下大乱。\n\n（空行不计）\n", encoding="utf-8")
    (bilingual / "数据来源.txt").write_text("来源：测试快照", encoding="utf-8")
    classical = snapshot_dir / "repository" / "古文原文" / "三朝北盟会编" / "卷一"
    classical.mkdir(parents=True)
    (classical / "text.txt").write_text("会编卷一正文。\n第二行。", encoding="utf-8")
    (snapshot_dir / "metadata.json").write_text(
        json.dumps({"dataset": "classical-modern", "version": "20240421"}, ensure_ascii=False),
        encoding="utf-8",
    )
    return snapshot_dir


def _paths(tmp_path: Path) -> PipelinePaths:
    return PipelinePaths(tmp_path)


def test_iter_bilingual_hierarchy(snapshot: Path):
    rows = list(iter_bilingual_texts(snapshot))
    # 4 行原文：第 3 行为空（source/target 均空）被跳过 → 3 行有效句对
    assert len(rows) == 3
    first = rows[0]
    assert first["title_zh_cn"] == "测试正史"
    assert first["section"] == "本纪"
    assert first["chapter"] == "卷一"
    assert first["paragraph_index"] == 1
    assert first["translation_zh_cn"] == "太祖的法度严整。"
    assert first["notes_zh_cn"] == "来源：测试快照"
    # ID 确定性：source_path + 行号
    assert first["id"].startswith("text-niutrans-")
    assert first["id"] == list(iter_bilingual_texts(snapshot))[0]["id"]


def test_iter_classical_books_scope(snapshot: Path):
    rows = list(iter_classical_texts(snapshot, books=("三朝北盟会编",)))
    assert len(rows) == 2
    assert rows[0]["section"] == "古文原文"
    assert rows[0]["translation_zh_cn"] is None
    # 未列出的书不导入
    assert list(iter_classical_texts(snapshot, books=("不存在的书",))) == []


def test_build_knowledge_store_idempotent(tmp_path: Path, snapshot: Path):
    paths = PipelinePaths(tmp_path)
    manifest = build_knowledge_store(paths, output=paths.database)
    assert manifest["texts_bilingual"] == 3
    assert manifest["texts_classical"] == 2

    def counts():
        with duckdb.connect(str(paths.database), read_only=True) as connection:
            texts = connection.execute(
                "SELECT COUNT(*), COUNT(DISTINCT id) FROM historical_texts"
            ).fetchone()
            works = connection.execute("SELECT COUNT(*) FROM works").fetchone()[0]
        return {"texts": texts[0], "distinct": texts[1], "works": works}

    first_counts = counts()
    assert first_counts["texts"] == first_counts["distinct"] == 5
    # 第二次 build（同输入）→ 计数不变、无重复 id（Gate D）
    build_knowledge_store(paths, output=paths.database)
    assert counts() == first_counts


def test_curated_work_remap(tmp_path: Path, snapshot: Path, monkeypatch):
    from history_data_pipeline.backbone.reference import CURATED_WORK_SEEDS

    curated_titles = {row["title"] for row in CURATED_WORK_SEEDS}
    # 合成快照里的书名不在 curated 表 → 走 work-niutrans-*；命中的书 → work-curated-*
    rows = list(iter_bilingual_texts(snapshot))
    book_id = rows[0]["book_id"]
    if "测试正史" in curated_titles:
        assert book_id.startswith("work-curated-")
    else:
        assert book_id.startswith("work-niutrans-")
    paths = PipelinePaths(tmp_path)
    build_knowledge_store(paths, output=paths.database)
    with duckdb.connect(str(paths.database), read_only=True) as connection:
        work_ids = {row[0] for row in connection.execute("SELECT id FROM works").fetchall()}
    # 该书 book_id 必须能解析到 works 行（join 不断链）
    assert book_id in work_ids
