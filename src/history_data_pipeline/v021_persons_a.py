# -*- coding: utf-8 -*-
"""V2.1.1 · 24 位 genuine_missing 补充 Person 规格数据（正典中文名使用简体）。
每条带 source_reference（具体史料/权威参考）与 precision；生卒不详者 year=None。
现代/民国/抗日/日本人物一律中性史实记录，不做价值判断。
"""

from __future__ import annotations

from typing import Any

PERSON_SPECS: dict[str, dict[str, Any]] = {
    # ---------------- 先秦 / 西汉 ----------------
    "curated-person-zhao-kuo": {
        "id": "curated-person-zhao-kuo",
        "name_raw": "赵括",
        "canonical_name_zh_cn": "赵括",
        "traditional_name": "趙括",
        "birth_year": None,
        "death_year": -260,
        "birth_precision": "unknown",
        "death_precision": "year",
        "gender": "male",
        "period_ids": ["period-warring-states"],
        "aliases": ["赵括", "趙括", "马服子"],
        "intro_zh_cn": "战国时赵国将领，赵奢之子；长平之战后期赵军主将，战败被杀。",
        "source_reference": "《史记·白起王翦列传》《史记·廉颇蔺相如列传》；杨宽《战国史》",
    },
    "curated-person-shang-tang": {
        "id": "curated-person-shang-tang",
        "name_raw": "商汤",
        "canonical_name_zh_cn": "商汤",
        "traditional_name": "商湯",
        "birth_year": None,
        "death_year": None,
        "birth_precision": "unknown",
        "death_precision": "unknown",
        "gender": "male",
        "period_ids": ["period-shang"],
        "aliases": ["商湯", "成汤", "成湯", "汤", "湯", "太乙"],
        "intro_zh_cn": "商朝建立者，灭夏建商。生卒年月无可靠史料记载。",
        "source_reference": "《史记·殷本纪》；《尚书·汤誓》；张岂之主编《中国历史·先秦卷》",
    },
    "curated-person-liu-bi": {
        "id": "curated-person-liu-bi",
        "name_raw": "吴王刘濞",
        "canonical_name_zh_cn": "刘濞",
        "traditional_name": "劉濞",
        "birth_year": None,
        "death_year": -154,
        "birth_precision": "unknown",
        "death_precision": "year",
        "gender": "male",
        "period_ids": ["period-western-han"],
        "aliases": ["刘濞", "吴王濞"],
        "intro_zh_cn": "西汉吴王，汉高祖刘邦之三弟刘仲之子。七国之乱首谋，兵败被杀。",
        "source_reference": "《史记·吴王濞列传》；《汉书·荆燕吴传》；白寿彝《中国通史》",
    },
    "curated-person-jia-nanfeng": {
        "id": "curated-person-jia-nanfeng",
        "name_raw": "贾南风",
        "canonical_name_zh_cn": "贾南风",
        "traditional_name": "賈南風",
        "birth_year": None,
        "death_year": 300,
        "birth_precision": "year",
        "death_precision": "year",
        "gender": "female",
        "period_ids": ["period-western-jin"],
        "aliases": ["贾后", "贾皇后"],
        "intro_zh_cn": "西晋惠帝皇后，八王之乱的重要推手，后被杀。",
        "source_reference": "出生于256年左右，《晋书·惠帝纪》《晋书·后妃传》",
    },
    "curated-person-juqu-mujian": {
        "id": "curated-person-juqu-mujian",
        "name_raw": "沮渠牧犍",
        "canonical_name_zh_cn": "沮渠牧犍",
        "traditional_name": "沮渠牧犍",
        "birth_year": None,
        "death_year": 447,
        "birth_precision": "unknown",
        "death_precision": "year",
        "gender": "male",
        "period_ids": ["period-sixteen-kingdoms"],
        "aliases": ["北凉哀王"],
        "intro_zh_cn": "北凉末主（433-439），439年降北魏，后卒（史载447年被赐死）。",
        "source_reference": "《魏书·沮渠蒙逊传》附牧犍；《资治通鉴》卷一二三",
    },
}