"""Source Batch 02 · needs_linking 重定位（晋书/旧唐书/后汉书/旧五代史/明史/魏书/清史稿已入库）。

Queue 11 同法：work 内章节+内容双核实，manual 段落锚 + 逐字引文；不改写 legacy work/term 声明。
"""
from __future__ import annotations
import sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
EVENTS = ROOT / "data" / "curated" / "history_backbone" / "events"

RELOCATE: dict[str, list[dict]] = {
    "event-bawang-zhi-luan": [dict(work="晋书", term="八王列传", tid="text-wikisource-f21d763277cdfff4294d",
        anchor="列传/八王列传#p33", quote="时齊王冏、河間王顒、成都王穎並擁強兵，各據一方。")],
    "event-dongjin-jianguo": [dict(work="晋书", term="元帝纪", tid="text-wikisource-0b643f82143521fa7eaa",
        anchor="帝纪/元帝纪#p4", quote="永嘉初，用王導計，始鎮建鄴……賓禮名賢，存問風俗，江东歸心焉。")],
    "event-feishui-zhizhan": [
        dict(work="晋书", term="谢玄传", tid="text-wikisource-da3dd5860fbd4f1e1615",
             anchor="列传/谢玄传#p32", quote="及苻堅自率兵次於项城，眾号百萬……詔以玄为前鋒。"),
        dict(work="晋书", term="苻坚载记", tid="text-wikisource-348444e7ba4426c3c1f4",
             anchor="载记/苻坚载记下#p18", quote="謝玄、謝琰勒卒數萬，陣以待之。")],
    "event-jin-mie-wu": [
        dict(work="晋书", term="武帝纪", tid="text-wikisource-de22c2daa7dbb1bb301b",
             anchor="帝纪/武帝纪#p153", quote="十一月，大舉伐吳，遣鎮軍將軍、琅邪王伷出涂中……"),
        dict(work="晋书", term="王濬传", tid="text-wikisource-1fc1bf754f21fb922f65",
             anchor="列传/王濬传#p5", quote="既而王濬破石頭，降孫皓，威名益振。"),
        dict(work="三国志", term="孙皓传", tid="text-niutrans-8ee996e48d36905af934",
             anchor="吴书/三嗣主传#p354", quote="孙皓穷迫归降，前诏待之以不死……其赐号为归命侯。")],
    "event-xijin-mie-wang": [dict(work="晋书", term="愍帝纪", tid="text-wikisource-0c95405959e570458b53",
        anchor="帝纪/愍帝纪#p102", quote="八月，刘曜逼京師，內外斷絕……麴允与公卿守長安小城以自固。")],
    "event-yongjia-zhi-luan": [dict(work="晋书", term="愍帝纪", tid="text-wikisource-12c7d07e70173ada95b9",
        anchor="帝纪/愍帝纪#p101", quote="秋七月，刘曜攻北地……曜進至涇陽，渭北諸城悉潰。")],
    "event-huangchao-qiyi": [
        dict(work="旧唐书", term="僖宗纪", tid="text-wikisource-1d473e4764c6d2e3f9fa",
             anchor="本纪/僖宗纪#p67", quote="己巳，賊陷东都……丙子，攻潼关，守关諸將望風自潰。"),
        dict(work="旧唐书", term="黄巢传", tid="text-wikisource-3c92003bf43ceff24b74",
             anchor="列传/黄巢传#p42", quote="一旦長驅江表，徑入关中。")],
    "event-tang-mie-dong-tujue": [dict(work="旧唐书", term="突厥传", tid="text-wikisource-96804b06b0d62abea878",
        anchor="列传/突厥传#p26", quote="及其国亂，諸部多歸中国，唯思摩隨逐頡利，竟与同擒。")],
    "event-qian-du-beijing": [dict(work="明史", term="地理志", tid="text-niutrans-03e94309ded1feb48be6",
        anchor="志/卷四十八#p169", quote="永乐元年，以北平为北京，置北京行部尚书二人。")],
    "event-beiwei-tongyi-beifang": [dict(work="魏书", term="沮渠蒙逊载记", tid="text-niutrans-77b4af938ecd3c772f8f",
        anchor="帝纪/卷四#p304", quote="是歲，沮渠蒙遜死，以其子牧犍为車騎大將軍，改封河西王。")],
    "event-caopi-dai-han": [dict(work="后汉书", term="献帝纪", tid="text-niutrans-4ab573bae8e0325e68fe",
        anchor="本纪/孝献帝纪#p267", quote="冬十月乙卯，皇帝遜位，魏王丕稱天子。")],
    "event-guo-wei-dai-han": [dict(work="旧五代史", term="周太祖纪", tid="text-niutrans-1a2cd0882143bb3b3936",
        anchor="后周/太祖纪一#p133", quote="今則軍民愛戴，朝野推崇，宜總萬機，以允群議，可監國。")],
}

def main() -> int:
    sys.path.insert(0, str(ROOT / "src"))
    from history_data_pipeline.backbone.evidence_link import _load_event_yaml
    changed = 0
    for eid, rows in RELOCATE.items():
        for path in EVENTS.rglob(f"{eid}.yml"):
            doc, (head, tail) = _load_event_yaml(path)
            dirty = False
            for e in doc.get("evidence") or []:
                if e.get("link_status") != "needs_linking":
                    continue
                for r in rows:
                    term = e.get("term") or ""
                    if e.get("work") == r["work"] and (r["term"] in term or term in r["term"]):
                        e["historical_text_id"] = r["tid"]
                        e["chapter_anchor"] = r["anchor"]
                        e["link_method"] = "manual"
                        e["link_status"] = "linked"
                        e["link_confidence"] = 0.9
                        e["link_quality_status"] = "reviewed"
                        e["review_note"] = (f"source-batch02：源入库后重定位（章节+内容双核实）。"
                                            f"引文：「{r['quote']}」；anchor=段落精确锚。")
                        dirty = True
                        changed += 1
                        break
            if dirty:
                path.write_text(head + yaml.safe_dump(doc, allow_unicode=True, sort_keys=False,
                                                       default_flow_style=False, width=10**6) + tail,
                                encoding="utf-8")
    print(f"relocated: {changed}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
