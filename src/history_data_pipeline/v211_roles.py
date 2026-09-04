# -*- coding: utf-8 -*-
"""V2.1.1 · 34 条 scope 的事件级角色数据（精简、低脆性）。

role_zh_cn 由 ROLE_LABEL[role] + side 拼装，避免逐条手写长句。
ROLE_ROWS 与 FROZEN_SCOPE 逐位置一一对应（index 0..33）。
"""

from __future__ import annotations

# (role, side)；与 FROZEN_SCOPE 同顺序
ROLE_ROWS: list[tuple[str, str]] = [
    ("participant", "西晋"),        # 0 贾南风
    ("victim", "北凉"),           # 1 沮渠牧犍
    ("commander", "赵国"),         # 2 赵括
    ("initiator", "后梁"),         # 3 朱温 [resolved]
    ("participant", "大齐"),       # 4 朱温 [resolved]
    ("ruler", "清"),              # 5 慈禧太后
    ("ruler", "北宋"),            # 6 宋徽宗
    ("initiator", "日本"),        # 7 石原莞尔
    ("initiator", "日本"),        # 8 板垣征四郎
    ("official", "中华民国"),      # 9 张学良
    ("ruler", "中华民国"),         # 10 蒋介石
    ("initiator", "日本"),        # 11 松井石根
    ("commander", "日本"),        # 12 谷寿夫
    ("commander", "中华民国"),     # 13 唐生智
    ("initiator", "吴"),          # 14 刘濞（吴王）
    ("official", "秦"),          # 15 李斯 [resolved]
    ("ruler", "清"),             # 16 隆裕太后
    ("political_leader", "中华民国"),  # 17 孙中山
    ("official", "中华民国"),      # 18 宋哲元
    ("official", "中华民国"),      # 19 秦德纯
    ("commander", "日本"),        # 20 牟田口廉也
    ("ruler", "日本"),           # 21 裕仁
    ("ruler", "中华民国"),         # 22 蒋介石
    ("initiator", "商"),          # 23 商汤
    ("political_leader", "中华民国"),  # 24 陈独秀
    ("initiator", "中华民国"),      # 25 张学良
    ("initiator", "中华民国"),      # 26 杨虎城
    ("victim", "中华民国"),        # 27 蒋介石
    ("participant", "中华民国"),    # 28 周恩来
    ("ruler", "更始"),           # 29 刘玄
    ("political_leader", "中华人民共和国"),  # 30 毛泽东
    ("political_leader", "中华人民共和国"),  # 31 周恩来
    ("political_leader", "中华人民共和国"),  # 32 朱德
    ("victim", "北周"),          # 33 周静帝 [resolved]
]

ROLE_LABEL: dict[str, str] = {
    "initiator": "发起者",
    "commander": "军事指挥",
    "ruler": "统治者",
    "victim": "受害者",
    "participant": "参与者",
    "political_leader": "政治领导人",
    "official": "官员",
}

assert len(ROLE_ROWS) == 34, f"ROLE_ROWS 必须 34 项，实际 {len(ROLE_ROWS)}"
assert set(ROLE_LABEL) >= {r for r, _ in ROLE_ROWS}, "存在未知 role 键"


def role_zh_for(i: int) -> str:
    role, side = ROLE_ROWS[i]
    return f"{side}·{ROLE_LABEL[role]}"