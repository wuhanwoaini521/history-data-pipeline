"""Batch 02 · Queue 11 — Legacy evidence 重定位（22 条 pending_knowledge → 新锚点）。

分级规则（docs/source-acquisition-policy.md + Queue 11 指令）：
- 旧 text-niutrans-* id 在新知识层全部悬空（非同一快照的路径散列），不可用 id 等价恢复。
- 重定位按「语料内容核实」执行：在 work 内以章节上下文 + 核心叙事定位段落，
  逐条人工复核（review_note 附逐字引文与判定理由），方法记为 manual（人工核定段落锚）。
- 无法定位核心段落者保持 pending_knowledge，列入 manual_candidate（报告），不自动绑定。
- fuzzy（段级相似）不作为绑定依据，仅报告。

写回方式：YAML priority——改 evidence 行字段（historical_text_id/chapter_anchor/
link_method/link_confidence/link_status/link_quality_status/review_note）。
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
EVENTS = ROOT / "data" / "curated" / "history_backbone" / "events"

# event_id -> (work, term, method, conf, anchor, tid, quote, rationale)
RECOVERIES: dict[str, dict] = {
    "event-chuhan-gaixia": dict(work="资治通鉴", term="垓下", conf=0.9, anchor="汉纪/汉纪三#p15",
        tid="text-niutrans-fe7ac9824979810edc02",
        quote="十二月，项王至垓下，兵少，食尽，与汉战不胜，入壁；汉军及诸侯兵围之数重。",
        rationale="资治通鉴汉纪三垓下之战核心叙事（围垓下段）"),
    "event-chuhan-julu": dict(work="史记", term="巨鹿", conf=0.9, anchor="十二本纪/项羽本纪#p149",
        tid="text-niutrans-a9b492a7760a44a40d88",
        quote="项羽乃悉引兵渡河，皆沉船，破釜甑，烧庐舍，持三日粮，以示士卒必死，无一还心。",
        rationale="项羽本纪巨鹿之战核心段（破釜沉舟）"),
    "event-chuhan-pengcheng": dict(work="史记", term="彭城", conf=0.9, anchor="十二本纪/高祖本纪#p291",
        tid="text-niutrans-cf1616150fc6dc30426a",
        quote="汉王以故得劫五诸侯兵，遂入彭城。",
        rationale="高祖本纪彭城之战入城段"),
    "event-chuhan-qin-fall": dict(work="史记", term="子婴", conf=0.9, anchor="十二本纪/高祖本纪#p186",
        tid="text-niutrans-6c0c5c66bca3e3dcb823",
        quote="秦王子婴素车白马，系颈以组，封皇帝玺符节，降轵道旁。",
        rationale="高祖本纪秦亡（子婴出降）核心段"),
    "event-chuhan-qin-revolt": dict(work="史记", term="陈胜", conf=0.9, anchor="三十世家/陈涉世家#p32",
        tid="text-niutrans-e9c4607a4ed7ee60f5a6",
        quote="且壮士不死即已，死即举大名耳，王侯将相宁有种乎！",
        rationale="陈涉世家大泽乡起义核心段"),
    "event-chuhan-xingyang": dict(work="资治通鉴", term="荥阳", conf=0.9, anchor="汉纪/汉纪二#p67",
        tid="text-niutrans-4861fc99aa1261c7ced3",
        quote="汉王收诸侯，还守成皋、荥阳，下蜀、汉之粟，深沟壁垒，分卒守徼乘塞。",
        rationale="通鉴汉纪二荥阳成皋相持段"),
    "event-hongmen": dict(work="史记", term="鸿门", conf=0.9, anchor="十二本纪/项羽本纪#p199",
        tid="text-niutrans-4d1d69a992f26f8293a6",
        quote="当是时，项羽兵四十万，在新丰鸿门，沛公兵十万，在霸上。",
        rationale="项羽本纪鸿门对峙核心段"),
    "event-three-chibi": dict(work="三国志", term="赤壁", conf=0.9, anchor="吴书/吴主传#p32",
        tid="text-niutrans-bcffeeda47097881fac2",
        quote="瑜、普为左右督，各领万人，与备俱进，遇於赤壁，大破曹公军。",
        rationale="吴主传赤壁破曹核心段"),
    "event-three-guandu": dict(work="资治通鉴", term="官渡", conf=0.9, anchor="汉纪/汉纪五十五#p324",
        tid="text-niutrans-2b40fe3e825750663819",
        quote="袁氏辎重万馀乘，在故市、乌巢，屯军无严备，若以轻兵袭之，不意而至，燔其积聚，不过三日，袁氏自败也。",
        rationale="通鉴汉纪五十五乌巢之计（官渡决战核心）"),
    "event-three-regime-formation": dict(work="三国志", term="黄初", conf=0.9, anchor="蜀书/先主传#p225",
        tid="text-niutrans-ea96131ea07df31f3667",
        quote="臣等谨与博士许慈、议郎孟光，建立礼仪，择令辰，上尊号。 即皇帝位於成都武担之南。",
        rationale="先主传刘备称帝（三国鼎立完成之标志）"),
    "event-three-jingzhou-change": dict(work="三国志", term="荆州", conf=0.9, anchor="蜀书/先主传#p84",
        tid="text-niutrans-3f854c1cebf25deaf613",
        quote="曹公南征表，会表卒，子琮代立，遣使请降。",
        rationale="先主传荆州易主（208 局势变化核心）"),
    "event-three-north-consolidation": dict(work="三国志", term="曹操", conf=0.85, anchor="魏书/武帝纪#p387",
        tid="text-niutrans-2fe875d7c6a090272092",
        quote="九月，公引兵自柳城还，康即斩尚、熙及速仆丸等，传其首。",
        rationale="武帝纪河北平定终局（袁氏覆灭，曹操北方巩固）"),
    "event-three-yellow-turbans": dict(work="后汉书", term="黄巾", conf=0.9, anchor="列传/皇甫嵩朱俊列传#p20",
        tid="text-niutrans-d60a7e4565a9c7a6bee6",
        quote="皆着黄巾为标帜，时人谓之 黄巾 ，亦名 蛾贼 。",
        rationale="皇甫嵩传黄巾标帜与起事记载"),
    "event-anlu-changan": dict(work="资治通鉴", term="长安", conf=0.85, anchor="唐纪/唐纪三十四#p204",
        tid="text-niutrans-eb9af9eebf6d1cd71636",
        quote="贼入长安方虏掠，未暇徇地，乘此速往就之，徐图大举，此上策也。",
        rationale="通鉴唐纪三十四贼入长安（长安失守）"),
    "event-anlu-xuanzong-shu": dict(work="资治通鉴", term="蜀", conf=0.9, anchor="唐纪/唐纪三十四#p132",
        tid="text-niutrans-60170da0c721234bc011",
        quote="丙申，至马嵬驿，将士饥疲，皆愤怒。",
        rationale="通鉴唐纪三十四玄宗西行至马嵬（入蜀途中核心）"),
    "event-anlu-tongguan": dict(work="资治通鉴", term="潼关", conf=0.85, anchor="唐纪/唐纪三十四#p21",
        tid="text-niutrans-954521afe14dcf226ae4",
        quote="今守潼关，数月不能进，北路已绝，诸军四合，吾所有者止汴、郑数州而已，万全何在？",
        rationale="通鉴唐纪三十四潼关对峙（失守前夕）"),
    "event-anlu-three-frontiers": dict(work="旧唐书", term="禄山", conf=0.95, anchor="列传/卷一百五十#p44",
        tid="text-niutrans-928b1cd55141795ed818",
        quote="兼三道节度，进奏无不允。",
        rationale="旧唐书安禄山传兼三道节度（三镇节度核心句）"),
    "event-anlu-shi-siming": dict(work="资治通鉴", term="史思明", conf=0.9, anchor="唐纪/唐纪三十七#p4",
        tid="text-niutrans-0ace3ebee9c2275397cf",
        quote="春，正月，己巳朔，史思明筑坛于魏州城北，自称大圣燕王；以周挚为行军司马。",
        rationale="通鉴唐纪三十七史思明称王（叛军核心叙事）"),
    "event-anlu-luoyang": dict(work="旧唐书", term="洛阳", conf=0.9, anchor="本纪/卷九#p388",
        tid="text-niutrans-3d334bb7fa0ce5c821fd",
        quote="丁酉，禄山陷东京，杀留守李憕、中丞卢奕、判官蒋清。",
        rationale="旧唐书玄宗纪禄山陷东京（洛阳失守核心段）"),
    "event-anlu-pacification": dict(work="旧唐书", term="思明", conf=0.85, anchor="本纪/卷十一#p92",
        tid="text-niutrans-2e5651d41a2967b20284",
        quote="闰月戊申，以史朝义下降将李宝臣为检校礼部尚书、兼御史大夫、恆州刺史、清河郡王，充成德军节度使。",
        rationale="旧唐书代宗纪史朝义败降后降将安置（安史之乱平定）"),
    "event-three-dong-zhuo": dict(work="资治通鉴", term="董卓", conf=0.9, anchor="汉纪/汉纪五十一#p219",
        tid="text-niutrans-725f295380e318748fd0",
        quote="董卓至显阳苑，远见火起，知有变，引兵急进；未明，到城西，闻帝在北，因与公卿往奉迎于北芒阪下。",
        rationale="通鉴汉纪五十一董卓率兵入京奉迎天子（进京核心段）"),
}


def main() -> int:
    import sys as _sys
    _sys.path.insert(0, str(ROOT / "src"))
    from history_data_pipeline.backbone.evidence_link import _load_event_yaml

    by_event: dict[str, list[dict]] = {}
    for eid, r in RECOVERIES.items():
        by_event.setdefault(eid, []).append(r)
    updated = 0
    for path in EVENTS.rglob("event-*.yml"):
        doc, (head_block, tail_block) = _load_event_yaml(path)
        eid = doc.get("id") if doc else None
        if eid not in by_event:
            continue
        matches = by_event[eid]
        changed = False
        for evidence in doc.get("evidence") or []:
            if evidence.get("link_status") != "pending_knowledge":
                continue
            for r in matches:
                if evidence.get("work") == r["work"] and (evidence.get("term") or "") == r["term"]:
                    evidence["historical_text_id"] = r["tid"]
                    evidence["chapter_anchor"] = r["anchor"]
                    evidence["link_method"] = "manual"
                    evidence["link_status"] = "linked"
                    evidence["link_confidence"] = r["conf"]
                    evidence["link_quality_status"] = "reviewed"
                    evidence["review_note"] = (
                        f"batch02-11：legacy 悬空锚重定位（章节+内容双核实）：{r['rationale']}。"
                        f"引文：「{r['quote']}」；anchor=段落精确锚。"
                    )
                    changed = True
                    updated += 1
                    break
        if changed:
            yaml_text = head_block + yaml.safe_dump(doc, allow_unicode=True, sort_keys=False,
                                                    default_flow_style=False, width=10**6) + tail_block
            path.write_text(yaml_text, encoding="utf-8")
            print(f"recovered {eid}")
    print(f"total recovered: {updated}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
