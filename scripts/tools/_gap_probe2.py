# -*- coding: utf-8 -*-
"""Full probe: people + person_aliases for all 34 gap names (simp/trad). Only reads KB."""
import sys
import duckdb
import opencc

sys.stdout.reconfigure(encoding="utf-8")
con = duckdb.connect("data/normalized/history.duckdb", read_only=True)
conv = opencc.OpenCC("s2t")

# (event, unique raw name)
RAW = [
    ("event-bawang-zhi-luan", "贾南风"),
    ("event-beiwei-tongyi-beifang", "沮渠牧犍"),
    ("event-changping-zhizhan", "赵括"),
    ("event-houliang-dai-tang", "朱温"),
    ("event-huangchao-qiyi", "朱温"),
    ("event-jiawu-zhanzheng", "慈禧太后"),
    ("event-jingkang-zhi-bian", "宋徽宗"),
    ("event-jiuyiba-shibian", "石原莞尔"),
    ("event-jiuyiba-shibian", "板垣征四郎"),
    ("event-jiuyiba-shibian", "张学良"),
    ("event-jiuyiba-shibian", "蒋介石"),
    ("event-nanjing-datusha", "松井石根"),
    ("event-nanjing-datusha", "谷寿夫"),
    ("event-nanjing-datusha", "唐生智"),
    ("event-qiguo-zhi-luan", "吴王刘濞"),
    ("event-qin-tongyi", "李斯"),
    ("event-qingdi-tuiwei", "隆裕太后"),
    ("event-qingdi-tuiwei", "孙中山"),
    ("event-qiqishi-bian", "宋哲元"),
    ("event-qiqishi-bian", "秦德纯"),
    ("event-qiqishi-bian", "牟田口廉也"),
    ("event-riben-touxiang", "裕仁"),
    ("event-shangtang-miexia", "商汤"),
    ("event-wusi-yundong", "陈独秀"),
    ("event-xian-shibian", "杨虎城"),
    ("event-xin-mie", "刘玄"),
    ("event-xinzhongguo-chengli", "朱德"),
    ("event-xinzhongguo-chengli", "毛泽东"),
    ("event-xinzhongguo-chengli", "周恩来"),
    ("event-yangjian-dai-beizhou", "周静帝"),
]


def probe(name: str):
    trad = conv.convert(name)
    out = {}
    q = ("SELECT id, canonical_name_zh_cn, birth_year, death_year, dynasty_ids "
         "FROM people WHERE canonical_name_zh_cn LIKE ? OR search_name LIKE ? "
         "ORDER BY canonical_name_zh_cn LIMIT 10")
    out["people_simp"] = con.execute(q, (f"%{name}%", f"%{name}%")).fetchall()
    out["people_trad"] = con.execute(q, (f"%{trad}%", f"%{trad}%")).fetchall()
    out["alias"] = con.execute(
        "SELECT pa.person_id, pa.alias, pa.alias_type, p.canonical_name_zh_cn, p.birth_year, p.death_year "
        "FROM person_aliases pa LEFT JOIN people p ON p.id=pa.person_id "
        "WHERE pa.alias LIKE ? OR pa.alias_zh_cn LIKE ? LIMIT 10",
        (f"%{name}%", f"%{trad}%")).fetchall()
    return out


seen = set()
for ev, name in RAW:
    key = name
    if key in seen:
        continue
    seen.add(key)
    r = probe(name)
    print("=" * 30)
    print(f"{ev} | {name} (trad {conv.convert(name)})")
    for k in ("people_simp", "people_trad", "alias"):
        vs = r[k]
        print(f"  {k}: {len(vs)}")
        for v in vs[:10]:
            print("     ", v)