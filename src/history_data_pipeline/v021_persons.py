# -*- coding: utf-8 -*-
"""V2.1.1 · 补充 Person 规格汇总（合并批次 A-D 并做一致性校验）。"""

from __future__ import annotations

from typing import Any

from .v021_persons_a import PERSON_SPECS as _A
from .v021_persons_b import PERSON_SPECS as _B
from .v021_persons_c import PERSON_SPECS as _C
from .v021_persons_d import PERSON_SPECS as _D

PERSON_SPECS: dict[str, dict[str, Any]] = {}
for _part in (_A, _B, _C, _D):
    for _pid, _spec in _part.items():
        if _pid in PERSON_SPECS:
            raise ValueError(f"duplicate person id: {_pid}")
        PERSON_SPECS[_pid] = _spec

_REQUIRED_KEYS = {
    "id", "name_raw", "canonical_name_zh_cn", "traditional_name",
    "birth_year", "death_year", "birth_precision", "death_precision",
    "gender", "period_ids", "aliases", "intro_zh_cn", "source_reference",
}

for _pid, _spec in PERSON_SPECS.items():
    missing = _REQUIRED_KEYS - set(_spec)
    if missing:
        raise ValueError(f"{_pid} 缺字段 {sorted(missing)}")
    if _spec["id"] != _pid:
        raise ValueError(f"{_pid}: id 字段与 key 不一致")
    if not (isinstance(_spec["aliases"], list) and _spec["aliases"]):
        raise ValueError(f"{_pid}: aliases 不能为空")
    if not _spec["canonical_name_zh_cn"] or not _spec["intro_zh_cn"]:
        raise ValueError(f"{_pid}: 中文名/简介不能为空")

REQUIRED_24: set[str] = {
    "curated-person-zhao-kuo", "curated-person-shang-tang", "curated-person-liu-bi",
    "curated-person-jia-nanfeng", "curated-person-juqu-mujian", "curated-person-songhuizong",
    "curated-person-cixi-taihou", "curated-person-sun-yat-sen", "curated-person-longyu",
    "curated-person-chen-duxiu", "curated-person-zhang-xueliang", "curated-person-chiang-kai-shek",
    "curated-person-yang-hucheng", "curated-person-zhou-enlai", "curated-person-mao-zedong",
    "curated-person-song-zheyuan", "curated-person-qin-dechun", "curated-person-tang-shengzhi",
    "curated-person-ishihara-kanji", "curated-person-itagaki-seishiro",
    "curated-person-matsui-iwane", "curated-person-tani-hisao",
    "curated-person-mutaguchi-renya", "curated-person-hirohito",
}

if set(PERSON_SPECS) != REQUIRED_24:
    raise ValueError(
        f"补充 Person 集合不一致: 实际={sorted(PERSON_SPECS)}\n期望={sorted(REQUIRED_IDS)}"
    )

__all__ = ["PERSON_SPECS"]