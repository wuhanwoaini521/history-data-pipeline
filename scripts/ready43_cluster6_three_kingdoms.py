"""Ready-43 · Cluster 6：三国群 8 事件（赤壁/董卓进京/官渡/荆州/北方巩固/鼎立形成/黄巾/孙刘联盟）。"""
from __future__ import annotations
import sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
EVENTS = ROOT / "data" / "curated" / "history_backbone" / "events"

def ev(work, term, anchor, tid, field, role, quote, note=""):
    return {"work": work, "term": term, "historical_text_id": tid, "chapter_anchor": anchor,
        "claim_field": field, "evidence_role": role, "link_status": "linked",
        "link_method": "manual", "link_confidence": 1.0, "link_quality_status": "reviewed",
        "context_keywords": [],
        "review_note": f"ready43-c6：{work}源引文：「{quote}」；claim_field={field}；anchor=段落精确锚。{note}"}

BLOCKS = {
 "three_kingdoms/event-three-chibi.yml": {
  "background_zh_cn": "备进住夏口，使诸葛亮诣权，权遣周瑜、程普等行——孙刘结盟共拒曹操，赤壁战云既合。",
  "process_zh_cn": "瑜、普为左右督，各领万人，与备俱进，遇于赤壁，大破曹公军。",
  "result_zh_cn": "公至赤壁，与备战，不利；于是大疫，吏士多死者，乃引军还——曹军北退。",
  "impact_zh_cn": "琦病死，群下推先主为荆州牧，治公安——赤壁之后刘备据荆州立足，三分之势自此肇基。",
  "places": [
   {"place_name_raw": "赤壁", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "孙刘联军大破曹军之地", "review_note": "ready43-c6：三国志·吴主传「遇於赤壁，大破曹公军」"},
   {"place_name_raw": "夏口", "role": "city", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "刘备驻军、诸葛亮使吴之地", "review_note": "ready43-c6：三国志·吴主传「备进住夏口」"},
  ],
  "evidence": [
   ev("三国志", "吴主传", "吴书/吴主传#p30", "text-niutrans-dd5ba835f14e46c0d920", "background", "primary",
      "备进住夏口，使诸葛亮诣权，权遣周瑜、程普等行。"),
   ev("三国志", "吴主传", "吴书/吴主传#p32", "text-niutrans-bcffeeda47097881fac2", "process", "primary",
      "瑜、普为左右督，各领万人，与备俱进，遇於赤壁，大破曹公军。"),
   ev("三国志", "武帝纪", "魏书/武帝纪#p402", "text-niutrans-a31fa38e83cba1481f0b", "result", "primary",
      "公至赤壁，与备战，不利。于是大疫，吏士多死者，乃引军还。"),
   ev("三国志", "先主传", "蜀书/先主传#p102", "text-niutrans-0058cd9602f4e850d94c", "impact", "primary",
      "琦病死，群下推先主为荆州牧，治公安。"),
  ],
 },
 "three_kingdoms/event-three-dong-zhuo.yml": {
  "background_zh_cn": "何进召卓使将兵诣京师——外戚与宦官相争，董卓应召引兵向洛，祸乱之门自开。",
  "process_zh_cn": "董卓至显阳苑，远见火起，知有变，引兵急进；未明到城西，闻帝在北，因与公卿往奉迎于北芒阪下。",
  "result_zh_cn": "甲戌，卓复会群僚于崇德前殿，胁太后策废少帝：「今废为弘农王，立陈留王协为帝」；袁隗解帝玺绶以奉陈留王——董卓擅行废立。",
  "impact_zh_cn": "癸酉，董卓使郎中令李儒鸩杀弘农王辩——废帝见杀，关东诸侯由此起兵，东汉中央权威崩解。",
  "places": [
   {"place_name_raw": "洛阳", "role": "capital", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "董卓入京、废立之地", "review_note": "ready43-c6：通鉴汉纪五十一「卓复会群僚于崇德前殿」"},
   {"place_name_raw": "北芒阪", "role": "location", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "董卓奉迎少帝之处", "review_note": "ready43-c6：通鉴汉纪五十一「奉迎于北芒阪下」"},
  ],
  "evidence": [
   ev("资治通鉴", "汉纪五十一", "汉纪/汉纪五十一#p162", "text-niutrans-f455552515745b0ab0d6", "background", "primary",
      "何进召卓使将兵诣京师。"),
   ev("资治通鉴", "汉纪五十一", "汉纪/汉纪五十一#p219", "text-niutrans-725f295380e318748fd0", "process", "primary",
      "董卓至显阳苑，远见火起，知有变，引兵急进……奉迎于北芒阪下。"),
   ev("资治通鉴", "汉纪五十一", "汉纪/汉纪五十一#p262", "text-niutrans-6586d08ac52da694f164", "result", "primary",
      "甲戌，卓复会群僚于崇德前殿，遂胁太后策废少帝……今废为弘农王，立陈留王协为帝。"),
   ev("资治通鉴", "汉纪五十一", "汉纪/汉纪五十一#p330", "text-niutrans-2cacc310917d4c7afc4a", "impact", "primary",
      "癸酉，董卓使郎中令李儒鸩杀弘农王辩。"),
  ],
 },
 "three_kingdoms/event-three-guandu.yml": {
  "background_zh_cn": "曹操还军官渡，绍乃议攻许，田丰谏之以持久——袁绍倾河北之众南下，两雄决战在即。",
  "process_zh_cn": "袁氏辎重万余乘在故市、乌巢，屯军无严备，曹操以轻兵袭之，不意而至、燔其积聚。",
  "result_zh_cn": "士卒皆殊死战，遂大破之，斩琼等、尽燔其粮谷；于是绍军惊扰大溃，绍及谭等幅巾乘马、与八百骑渡河。",
  "impact_zh_cn": "官渡之败使袁绍元气大伤，河北由盛转衰——曹操由此奠定统一北方之势。",
  "places": [
   {"place_name_raw": "官渡", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "决战之地", "review_note": "ready43-c6：通鉴汉纪五十五「曹操还军官渡」"},
   {"place_name_raw": "乌巢", "role": "battlesite", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "袁氏辎重屯所：曹操轻兵焚粮", "review_note": "ready43-c6：通鉴汉纪五十五「袁氏辎重万馀乘，在故市、乌巢」"},
  ],
  "evidence": [
   ev("资治通鉴", "汉纪五十五", "汉纪/汉纪五十五#p195", "text-niutrans-0f73f873c122629ca8f7", "background", "primary",
      "曹操还军官渡，绍乃议攻许，田丰曰……"),
   ev("资治通鉴", "汉纪五十五", "汉纪/汉纪五十五#p324", "text-niutrans-2b40fe3e825750663819", "process", "primary",
      "袁氏辎重万馀乘，在故市、乌巢，屯军无严备，若以轻兵袭之……不过三日，袁氏自败也。"),
   ev("资治通鉴", "汉纪五十五", "汉纪/汉纪五十五#p338", "text-niutrans-a1207db255ef5abeb519", "result", "primary",
      "士卒皆殊死战，遂大破之，斩琼等，尽燔其粮谷。"),
   ev("资治通鉴", "汉纪五十五", "汉纪/汉纪五十五#p343", "text-niutrans-6dbd12c6f310f01f4186", "impact", "primary",
      "于是绍军惊扰，大溃，绍及谭等幅巾乘马，与八百骑渡河。"),
  ],
 },
 "three_kingdoms/event-three-jingzhou-change.yml": {
  "background_zh_cn": "曹公南征表，会表卒，子琮代立、遣使请降——刘表之死与荆州易帜，中原兵锋直指江汉。",
  "process_zh_cn": "过襄阳，诸葛亮说先主攻琮「荆州可有」；乃驻马呼琮，琮惧不能起。",
  "result_zh_cn": "琦病死，群下推先主为荆州牧，治公安——刘备取荆州南部为基业。",
  "impact_zh_cn": "二十年，孙权以先主已得益州，使使报欲得荆州；先主言「须得凉州，当以荆州相与」——借荆州之争自此成为孙刘联盟的裂痕。",
  "places": [
   {"place_name_raw": "襄阳", "role": "city", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "刘琮降曹、先主过境之地", "review_note": "ready43-c6：三国志·先主传「过襄阳，诸葛亮说先主攻琮」"},
   {"place_name_raw": "公安", "role": "city", "link_status": "needs_linking", "sequence": 2,
    "description_zh_cn": "先主治所（荆州牧）", "review_note": "ready43-c6：三国志·先主传「治公安」"},
  ],
  "evidence": [
   ev("三国志", "先主传", "蜀书/先主传#p84", "text-niutrans-3f854c1cebf25deaf613", "background", "primary",
      "曹公南征表，会表卒，子琮代立，遣使请降。"),
   ev("三国志", "先主传", "蜀书/先主传#p86", "text-niutrans-d38c7a9e6f352dddbfb9", "process", "primary",
      "过襄阳，诸葛亮说先主攻琮，荆州可有。"),
   ev("三国志", "先主传", "蜀书/先主传#p102", "text-niutrans-0058cd9602f4e850d94c", "result", "primary",
      "琦病死，群下推先主为荆州牧，治公安。"),
   ev("三国志", "先主传", "蜀书/先主传#p140", "text-niutrans-1db653c6339964a14e0d", "impact", "primary",
      "二十年，孙权以先主已得益州，使使报欲得荆州。"),
   ev("三国志", "先主传", "蜀书/先主传#p141", "text-niutrans-4b21c05dcebff86b6d45", "impact", "supporting",
      "须得凉州，当以荆州相与。"),
  ],
 },
 "three_kingdoms/event-three-north-consolidation.yml": {
  "background_zh_cn": "夏四月，曹操进军邺——袁氏根本之地，河北决战之地。",
  "process_zh_cn": "公之去邺而南也，谭、尚争冀州，谭为尚所败、走保平原——袁氏兄弟阋墙，曹操乘之。",
  "result_zh_cn": "九月，公引兵自柳城还，康即斩尚、熙及速仆丸等，传其首——袁氏覆灭，河北悉平。",
  "impact_zh_cn": "汉罢三公官、置丞相、御史大夫——北方既固，曹操中枢集权，为南征与魏室肇基铺路。",
  "places": [
   {"place_name_raw": "邺", "role": "city", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "袁氏根本、曹操进军所向", "review_note": "ready43-c6：三国志·武帝纪「进军邺」"},
  ],
  "evidence": [
   ev("三国志", "武帝纪", "魏书/武帝纪#p287", "text-niutrans-e06fe7ca44eb46103b34", "background", "primary",
      "夏四月，进军邺。"),
   ev("三国志", "武帝纪", "魏书/武帝纪#p296", "text-niutrans-cc764bc13a73b893b211", "process", "primary",
      "公之去邺而南也，谭、尚争冀州，谭为尚所败，走保平原。"),
   ev("三国志", "武帝纪", "魏书/武帝纪#p387", "text-niutrans-2fe875d7c6a090272092", "result", "primary",
      "九月，公引兵自柳城还，康即斩尚、熙及速仆丸等，传其首。"),
   ev("三国志", "武帝纪", "魏书/武帝纪#p392", "text-niutrans-9a55eec4ee1b24556fa9", "impact", "primary",
      "汉罢三公官，置丞相、御史大夫。"),
  ],
 },
 "three_kingdoms/event-three-regime-formation.yml": {
  "background_zh_cn": "冬，魏嗣王称尊号、改元为黄初——曹丕代汉，三国鼎立的第一块基石落定。",
  "process_zh_cn": "先主即皇帝位于成都武担之南，国号汉（蜀汉）——汉室旗号重建于西南。",
  "result_zh_cn": "黄龙元年春，公卿百司皆劝权正尊号（孙权称帝于武昌）——魏、汉、吴三方帝号并立。",
  "impact_zh_cn": "史评孙权「自擅江表，成鼎峙之业」——三国鼎立格局正式形成，与魏汉吴三方并立之局延续四十余年。",
  "relations": [
   {"target_event_id": "event-caopi-dai-han", "relation_type": "follows", "confidence": 0.9,
    "description_zh_cn": "曹丕代汉（220）为鼎立格局的第一块基石，蜀汉、东吴相继称帝。"},
   {"target_event_id": "event-three-chibi", "relation_type": "follows", "confidence": 0.8,
    "description_zh_cn": "赤壁之战奠定南北分立的军事基础，鼎立格局由此肇基。"},
  ],
  "places": [
   {"place_name_raw": "成都", "role": "capital", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "先主（蜀汉）即皇帝位之地", "review_note": "ready43-c6：三国志·先主传「即皇帝位於成都武担之南」"},
  ],
  "evidence": [
   ev("三国志", "吴主传", "吴书/吴主传#p87", "text-niutrans-736750be99de3559a5d8", "background", "primary",
      "冬，魏嗣王称尊号，改元为黄初。"),
   ev("三国志", "先主传", "蜀书/先主传#p225", "text-niutrans-ea96131ea07df31f3667", "process", "primary",
      "即皇帝位於成都武担之南。"),
   ev("三国志", "吴主传", "吴书/吴主传#p197", "text-niutrans-73eeecde13d1b401af18", "result", "primary",
      "黄龙元年春，公卿百司皆劝权正尊号。"),
   ev("三国志", "吴主传", "吴书/吴主传#p430", "text-niutrans-6d594a1052f3b290e676", "impact", "primary",
      "故能自擅江表，成鼎峙之业。"),
  ],
 },
 "three_kingdoms/event-three-yellow-turbans.yml": {
  "background_zh_cn": "郎中张钧上书言「张角所以能兴兵作乱，万人所以乐附之者，其源皆由十常侍多放父兄子弟……辜榷财利，侵掠百姓」——宦官乱政为黄巾之乱之由。",
  "process_zh_cn": "皆着黄巾为标帜，时人谓之黄巾，亦名「蛾贼」——以宗教符水聚众，旬月之间天下响应。",
  "result_zh_cn": "官军大举反扑：以嵩为左中郎将，与朱俊共发五校、三河骑士及募精勇合四万余人，共讨颍川黄巾；嵩、俊乘胜进讨汝南、陈国黄巾。",
  "impact_zh_cn": "黄巾虽平而天下残破：青、徐士庶避黄巾之难归刘虞者百余万口——流民百万、州郡割据，东汉统治自此瓦解，群雄逐鹿之局开启。",
  "places": [
   {"place_name_raw": "颍川", "role": "battlesite", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "黄巾主力所在，嵩俊进讨之地", "review_note": "ready43-c6：后汉书·皇甫嵩传「共讨颍川黄巾」"},
  ],
  "evidence": [
   ev("后汉书", "宦者列传", "列传/宦者列传#p318", "text-niutrans-5572c9655dc6f0c571da", "background", "primary",
      "窃惟张角所以能兴兵作乱，万人所以乐附之者，其源皆由十常侍多放父兄、子弟、婚亲、宾客典据州郡。"),
   ev("后汉书", "皇甫嵩传", "列传/皇甫嵩朱俊列传#p20", "text-niutrans-d60a7e4565a9c7a6bee6", "process", "primary",
      "皆着黄巾为标帜，时人谓之 黄巾 ，亦名 蛾贼 。"),
   ev("后汉书", "皇甫嵩传", "列传/皇甫嵩朱俊列传#p29", "text-niutrans-97f619cecee34e75cdcd", "result", "primary",
      "以嵩为左中郎将……共发五校、三河骑士及募精勇，合四万余人，嵩、俊各统一军，共讨颍川黄巾。"),
   ev("后汉书", "皇甫嵩传", "列传/皇甫嵩朱俊列传#p36", "text-niutrans-925dfa8d75ac9e721851", "result", "supporting",
      "嵩、俊乘胜进讨汝南、陈国黄巾。"),
   ev("后汉书", "刘虞传", "列传/刘虞公孙瓚陶谦列传#p26", "text-niutrans-e9d109bbe481411caefc", "impact", "primary",
      "青、徐士庶避黄巾之难归虞者百余万口。"),
  ],
 },
 "three_kingdoms/event-three-sun-liu-alliance.yml": {
  "background_zh_cn": "刘备为曹公所破，欲引南渡江，与鲁肃遇于当阳，遂共图计、进住夏口——败军之际孙刘使者相遇，联盟之议起。",
  "process_zh_cn": "备使诸葛亮诣权，权遣周瑜、程普等行——江东决意出兵，联军成形。",
  "result_zh_cn": "瑜、普为左右督各领万人，与备俱进，遇于赤壁，大破曹公军——联盟取得决定性胜利。",
  "impact_zh_cn": "联盟之利与隙并生：先主得荆州立足，而孙权后以「欲得荆州」与先主相争——孙刘联盟自此在共抗曹操与荆州之争间摇摆。",
  "places": [
   {"place_name_raw": "当阳", "role": "location", "link_status": "needs_linking", "sequence": 1,
    "description_zh_cn": "刘备与鲁肃相遇定计之地", "review_note": "ready43-c6：三国志·周瑜传「与鲁肃遇於当阳，遂共图计」"},
  ],
  "evidence": [
   ev("三国志", "周瑜传", "吴书/周瑜鲁肃吕蒙传#p52", "text-niutrans-", "background", "primary",
      "时刘备为曹公所破，欲引南渡江，与鲁肃遇於当阳，遂共图计。"),
   ev("三国志", "吴主传", "吴书/吴主传#p30", "text-niutrans-dd5ba835f14e46c0d920", "process", "primary",
      "备进住夏口，使诸葛亮诣权，权遣周瑜、程普等行。"),
   ev("三国志", "吴主传", "吴书/吴主传#p32", "text-niutrans-bcffeeda47097881fac2", "result", "primary",
      "瑜、普为左右督，各领万人，与备俱进，遇於赤壁，大破曹公军。"),
   ev("三国志", "先主传", "蜀书/先主传#p140", "text-niutrans-1db653c6339964a14e0d", "impact", "primary",
      "二十年，孙权以先主已得益州，使使报欲得荆州。"),
  ],
 },
}

# 补一个缺失的 text_id（周瑜传 p52）
try:
    import duckdb as _dd
    _con = _dd.connect(str(ROOT / "data" / "normalized" / "history.duckdb"), read_only=True)
    _r = _con.execute("SELECT id FROM historical_texts WHERE title_zh_cn='三国志' AND section='吴书' AND chapter='周瑜鲁肃吕蒙传' AND paragraph_index=52").fetchone()
    _con.close()
    if _r:
        BLOCKS["three_kingdoms/event-three-sun-liu-alliance.yml"]["evidence"][0]["historical_text_id"] = _r[0]
        print(f"resolved 周瑜传#p52 id: {_r[0]}")
except Exception as exc:  # pragma: no cover
    print("id lookup failed:", exc)


def main() -> int:
    applied = 0
    for rel, block in BLOCKS.items():
        path = EVENTS / rel
        if not path.exists():
            print(f"MISSING {rel}"); continue
        if yaml.safe_load(path.read_text()).get("process_zh_cn"):
            print(f"SKIP {rel}"); continue
        with path.open("a", encoding="utf-8") as s:
            s.write("\n" + yaml.safe_dump(block, allow_unicode=True, sort_keys=False, default_flow_style=False, width=10**6))
        applied += 1
        print(f"appended {rel}")
    print(f"total: {applied}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
