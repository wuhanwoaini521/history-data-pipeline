# -*- coding: utf-8 -*-
"""V2.1.1 临时分析工具：探测 34 个 not_found 名字在 Knowledge Store 的存在性。
只读，不产出正式报告。"""
import sys
import duckdb
import opencc

sys.stdout.reconfigure(encoding="utf-8")
con = duckdb.connect("data/normalized/history.duckdb", read_only=True)
conv = opencc.OpenCC("s2t")

names = ["贾南风", "沮渠牧犍", "赵括", "朱温", "慈禧太后", "宋徽宗", "宋钦宗",
         "石原莞尔", "板垣征四郎", "张学良", "蒋介石", "松井石根", "谷寿夫", "唐生智",
         "刘濞", "李斯", "隆裕太后", "孙中山", "宋哲元", "秦德纯", "牟田口廉也",
         "裕仁", "商汤", "陈独秀", "刘玄", "朱德", "周静帝", "宇文阐", "赵佶", "赵桓",
         "李渊", "李世民", "毛澤東", "周恩来", "溥仪", "袁世凯"]


def probe(name: str):
    trad = conv.convert(name)
    q = ("SELECT id, canonical_name_zh_cn, name_raw, traditional_name, birth_year, death_year "
         "FROM people WHERE canonical_name_zh_cn LIKE ? OR search_name LIKE ? "
         "ORDER BY canonical_name_zh_cn LIMIT 8")
    out = {
        "name": name,
        "people_simp": con.execute(q, (f"%{name}%", f"%{name}%")).fetchall(),
        "people_trad": con.execute(q, (f"%{trad}%", f"%{trad}%")).fetchall(),
        "aliases": con.execute(
            "SELECT person_id, alias, alias_type FROM person_aliases "
            "WHERE alias LIKE ? OR alias_zh_cn LIKE ? LIMIT 8",
            (f"%{name}%", f"%{trad}%")).fetchall(),
    }
    return out


for name in names:
    r = probe(name)
    print("=" * 28)
    print(f"NAME {name} (trad={r['trad']})" if False else f"NAME {name}")
    for k in ("people_simp", "people_trad", "aliases"):
        vs = r[k]
        print(" ", k, len(vs))
        for v in vs[:8]:
            if k == "aliases":
                print("     ALIAS", v)
            else:
                print("     RN", v)