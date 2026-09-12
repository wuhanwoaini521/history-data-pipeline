# Overnight Queue 00 — Baseline

> 生成：2026-09-12 00:xx（Overnight Queue 启动时快照）

## 环境

| 项 | 值 |
|---|---|
| 主仓库分支/commit | `main` @ `403d5fd`（gitlink 指向 22158dc） |
| 子仓库分支/commit | `main` @ `22158dc`（与 origin/main 同步） |
| 工作区 | 主/子仓库均干净，无未提交改动 |
| raw/staging/dist | gitignored（快照与构建产物不入库，符合仓库策略） |
| Python 运行环境 | uv python 3.11 + uv 缓存解包依赖（PYTHONPATH 注入；本机 AppImage binfmt 破坏 venv prefix，详见主报告） |

## 数据基线（Baseline）

| 指标 | 值 |
|---|---:|
| dist historical_texts | 730,128 |
| dist events / evidence | 618 / 130 |
| dist evidence linked | 74 |
| knowledge store texts / chapter_heads | 730,128 / 3,838 |

上一轮（知识层重建）已完成并提交：Queue 1–7 的主体工作在 `22158dc` 落地，
本轮 overnight 以该状态为起点，按 overnight-* 命名重新验证并补齐 Queue 8–11。

## Baseline 测试（Queue 0 快速集）

```
pytest tests/test_source_reference.py tests/test_evidence_link.py
       tests/test_knowledge_build.py tests/test_product_reporting.py
       tests/test_backbone.py
→ 72 passed（3m28s）
```

结论：起点健康，进入 Queue 1。
