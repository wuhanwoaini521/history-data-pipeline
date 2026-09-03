# -*- coding: utf-8 -*-
"""China History Backbone V1 — Batch 3（东汉末→三国→西晋→东晋/十六国→南北朝→隋统一）。

由 scripts/backbone_batch3_write.py 写入 events/<dir>/（东汉末/三国 → three_kingdoms；
西晋/东晋/十六国/南北朝/隋 → jin_southern_northern）与 reviews。

复用（不重复建档）：
- event-three-yellow-turbans（184 黄巾）/ event-three-dong-zhuo（189 董卓进京）/
  event-three-guandu（200 官渡之战）/ event-three-north-consolidation（200-207 曹操北方势力巩固）/
  event-three-jingzhou-change（208 荆州局势变化）/ event-three-sun-liu-alliance（208 孙刘联盟）/
  event-three-chibi（208 赤壁之战）/ event-three-regime-formation（220-229 三国鼎立格局逐渐形成）
"""

from __future__ import annotations

MODERN = {
    "wj": "王仲荦《魏晋南北朝史》（上海人民出版社）；田余庆《东晋门阀政治》（北京大学出版社）；"
          "周一良《魏晋南北朝史论集》；吕思勉《两晋南北朝史》；白寿彝总主编《中国通史》；张岂之主编《中国历史·隋唐辽宋金元卷》",
    "three": "王仲荦《魏晋南北朝史》；吕思勉《三国史话》及《两晋南北朝史》；翦伯赞《中国史纲要》；白寿彝《中国通史》",
    "suibound": "王仲荦《魏晋南北朝史》；吕思勉《两晋南北朝史》；陈寅恪《隋唐制度渊源略论稿》；白寿彝《中国通史》",
}

W = {
    "housh": ["work-curated-houhanshu"],
    "sanguo": ["work-curated-sanguozhi"],
    "housh_sanguo": ["work-curated-houhanshu", "work-curated-sanguozhi"],
    "jinshu": ["work-curated-jinshu"],
    "jinshu_zizhi": ["work-curated-jinshu", "work-curated-zizhitongjian"],
    "jinshu_songs_etc": ["work-curated-jinshu", "work-curated-songshu", "work-curated-zizhitongjian"],
    "weishu": ["work-curated-weishu"],
    "weishu_zizhi": ["work-curated-weishu", "work-curated-zizhitongjian"],
    "liangchen": ["work-curated-liangshu", "work-curated-chenshu", "work-curated-nanshi"],
    "nanbeishi": ["work-curated-nanshi", "work-curated-beishi"],
    "suishu": ["work-curated-suishu"],
    "zizhi": ["work-curated-zizhitongjian"],
}


def _rel(target, rtype, confidence=None, desc=None):
    item = {"target_event_id": target, "relation_type": rtype}
    if confidence is not None:
        item["confidence"] = confidence
    if desc:
        item["description_zh_cn"] = desc
    return item


def _ev(id_, name, etype, start, end, precision, period, importance, summary,
        source_ref, source_ids, regimes_or_relations=None, relations=None, review_note=None):
    """regimes_or_relations：source_ids 之后的列表参数。

    未声明 regime_ids 的事件直接在该位置传 relations（全部为 dict）；
    声明 regime_ids 的事件传 ['regime-x', ...]（全部为字符串）后跟 [
    relations...]。
    """
    if regimes_or_relations is not None and regimes_or_relations             and all(isinstance(x, str) for x in regimes_or_relations):
        regime_ids = regimes_or_relations
    else:
        regime_ids = []
        relations = relations if relations is not None else (regimes_or_relations or [])
    return {
        "id": id_, "name_zh_cn": name, "event_type": etype,
        "start_year": start, "end_year": end, "date_precision": precision,
        "period_id": period, "importance": importance, "summary_zh_cn": summary,
        "source_ref": source_ref, "source_ids": source_ids,
        "regime_ids": regime_ids or [],
        "relations": relations or [],
        "review_note": review_note,
    }


# ---------------------------------------------------------------------------
# Phase 1 — 东汉末（189–219；复用 黄巾184/董卓进京/官渡/北固/荆州/孙刘/赤壁）
# ---------------------------------------------------------------------------
PHASE_LATE_HAN = [
    _ev("event-shichangshi-zhi-luan", "十常侍之乱（何进召董卓）", "political",
        189, 189, "year", "period-late-eastern-han", "major",
        "中平六年（189年）汉灵帝去世，外戚何进谋诛宦官，召董卓等进京施压；"
        "宦官张让等先发制人杀何进，袁绍等率兵尽诛宦官，东汉宦官集团自此消灭。"
        "何进召边军入京与宫变失控，直接为董卓专权打开了大门。",
        f"古代史料：《后汉书·灵帝纪》《窦何列传》《三国志·魏书·武帝纪》；现代参考：{MODERN['three']}",
        W["housh_sanguo"],
        [_rel("event-three-dong-zhuo", "leads_to", 0.9, desc="何进之死与宫变使董卓得以率军入京")],
        review_note="十常侍与何进之争在前189年；\"十常侍之乱\"为后世对宦官集团专权与终结的概括性名称。"),
    _ev("event-dong-zhuo-fei-di", "董卓废少帝、立献帝", "political",
        189, 189, "year", "period-late-eastern-han", "major",
        "189年董卓入京后，废少帝刘辩、立陈留王刘协（汉献帝），自任相国专权，"
        "逼走袁绍等人。汉廷自此丧失对地方州牧的控制，东汉帝国进入名义共主的阶段。",
        f"古代史料：《后汉书·董卓列传》《三国志·魏书·董卓传》；现代参考：{MODERN['three']}",
        W["housh_sanguo"],
        [_rel("event-three-dong-zhuo", "follows", desc="董卓进京后的废立之举"),
         _rel("event-guan-dong-tao-dong", "leads_to", 0.9, desc="废帝激怒州郡，促成关东联军讨董")],
        review_note="废立事件在189年九月前后；\"董卓废少帝立献帝\"为东汉政治崩解的关键节点。"),
    _ev("event-guan-dong-tao-dong", "关东诸侯讨董", "war",
        190, 190, "year", "period-late-eastern-han", "major",
        "初平元年（190年）正月，关东州郡推袁绍为盟主，集结联军讨伐董卓，"
        "曹操、袁术、公孙瓒等并起。联军内部分裂、各自观望，未能入关击卓，"
        "但董卓被迫迁都长安，东汉朝廷自此流离。",
        f"古代史料：《后汉书·董卓列传》《三国志·魏书·武帝纪》《袁绍传》；现代参考：{MODERN['three']}",
        W["housh_sanguo"],
        [_rel("event-dong-zhuo-fei-di", "follows"),
         _rel("event-dong-zhuo-qian-du", "leads_to", 0.85, desc="联军兵临，董卓焚洛阳西迁长安")],
        review_note="讨董联军成立于190年；期间\"群雄割据\"局面开始形成（袁绍据河北等）。"),
    _ev("event-dong-zhuo-qian-du", "董卓迁都长安", "migration",
        190, 190, "year", "period-late-eastern-han", "major",
        "初平元年（190年）董卓挟献帝迁都长安，悉烧洛阳宫室、发掘陵墓，"
        "驱迫数百万民众西徙，洛阳城遭到毁灭性破坏。东汉两京制度名存实亡。",
        f"古代史料：《后汉书·董卓列传》；现代参考：{MODERN['three']}",
        W["housh"],
        [_rel("event-guan-dong-tao-dong", "follows"),
         _rel("event-dong-zhuo-zhisha", "leads_to", 0.7, desc="迁都后董卓仍专权，旋被王允吕布所杀")],
        review_note="迁都长安在190年四至八月先后；洛阳焚毁为《后汉书》所载，\"百万民众\"系传统记载口径。"),
    _ev("event-dong-zhuo-zhisha", "董卓被杀", "political",
        192, 192, "year", "period-late-eastern-han", "major",
        "初平三年（192年），司徒王允与吕布合谋刺杀董卓，长安城百姓称庆。"
        "董卓死后其部将李傕、郭汜等反攻长安，王允被杀，东汉朝廷落入军阀控制。",
        f"古代史料：《后汉书·董卓列传》《三国志·魏书·吕布传》；现代参考：{MODERN['three']}",
        W["housh_sanguo"],
        [_rel("event-dong-zhuo-qian-du", "follows"),
         _rel("event-li-jue-guo-si", "leads_to", 0.9, desc="董卓死后李傕郭汜火并控制长安")],
        review_note="董卓死于192年四月；王允赦宥之争与西凉军不满为李傕郭汜反攻的背景。"),
    _ev("event-li-jue-guo-si", "李傕郭汜之乱", "political",
        192, 195, "range", "period-late-eastern-han", "major",
        "192年李傕、郭汜攻入长安杀王允、劫持献帝，其后两人火并，"
        "长安遂成废墟，关中户口离散。东汉朝廷在军阀挟持下名存实亡。",
        f"古代史料：《后汉书·董卓列传》《献帝纪》；现代参考：{MODERN['three']}",
        W["housh"],
        [_rel("event-dong-zhuo-zhisha", "follows"),
         _rel("event-xian-di-dong-gui", "leads_to", 0.85, desc="李郭相攻，献帝设法东归洛阳")],
        review_note="李傕郭汜控制长安（192—195）为过程节点；其间献帝谋东归为司马彪记载。"),
    _ev("event-xian-di-dong-gui", "汉献帝东归", "migration",
        195, 196, "range", "period-late-eastern-han", "major",
        "兴平二年（195年）汉献帝在杨奉、董承等护送下逃离长安东归，"
        "辗转经弘农、洛阳，于次年（196年）到达洛阳。献帝东归是东汉皇权最后一次"
        "以独立姿态行动，随即落入曹操控制。",
        f"古代史料：《后汉书·献帝纪》；现代参考：{MODERN['three']}",
        W["housh"],
        [_rel("event-li-jue-guo-si", "follows"),
         _rel("event-caocao-ying-xian-di", "leads_to", 0.9, desc="献帝至洛阳后曹操迎帝迁许")],
        review_note="献帝东归（195—196）过程曲折，兴平二年至建安元年（河阳、洛阳）。"),
    _ev("event-caocao-ying-xian-di", "曹操迎汉献帝至许", "political",
        196, 196, "year", "period-late-eastern-han", "major",
        "建安元年（196年）曹操迎汉献帝都许（今河南许昌），"
        "行\"奉天子以令不臣\"（后世称\"挟天子以令诸侯\"），"
        "随后实行屯田以足军食。曹操由此取得政治与名分上的制高点。",
        f"古代史料：《三国志·魏书·武帝纪》《荀彧传》；现代参考：{MODERN['three']}",
        W["sanguo"],
        [_rel("event-xian-di-dong-gui", "follows"),
         _rel("event-lvbu-baiwang", "precedes", desc="迎献帝后曹操经略豫兖，逐步收平徐州吕布等部")],
        review_note="曹操迎帝都在196年（建安元年）；\"挟天子以令诸侯\"为后人对\"奉天子以令不臣\"的概括。"),
    _ev("event-yuanshu-chengdi", "袁术称帝", "political",
        197, 197, "year", "period-late-eastern-han", "major",
        "建安二年（197年）袁术据淮南称帝，成为汉末群雄中第一个公然僭号称帝者。"
        "袁术称帝遭各方声讨，不久为吕布、曹操等所败，于199年忧愤病死。"
        "此事动摇了汉室残余权威，也开启了群雄自立之年。",
        f"古代史料：《后汉书·袁术传》《三国志·魏书·袁术传》；现代参考：{MODERN['three']}",
        W["housh_sanguo"],
        [_rel("event-lvbu-baiwang", "precedes", desc="袁术败亡与吕布下邳败亡相继发生于199年")],
        review_note="袁术称帝在197年二月；199年败亡。\"玉玺\"之说为后世传述成分居多。"),
    _ev("event-lvbu-baiwang", "吕布败亡（下邳之战）", "war",
        198, 199, "range", "period-late-eastern-han", "major",
        "建安三年（198年）曹操围攻徐州下邳，吕布军被水淹城破，"
        "199年年初吕布被擒杀，其势力彻底覆灭。曹操由此清除后顾之忧，"
        "得以全力应对河北袁绍。",
        f"古代史料：《三国志·魏书·吕布传》《武帝纪》；现代参考：{MODERN['three']}",
        W["sanguo"],
        [_rel("event-caocao-ying-xian-di", "follows"),
         _rel("event-three-guandu", "precedes", desc="吕布既平，曹操转向与袁绍决战官渡")],
        review_note="吕布下邳被围（198年冬至199年初）；\"水淹下邳\"为史载攻城手段。"),
    _ev("event-yuanshi-wajie", "袁氏势力瓦解", "political-military",
        202, 207, "range", "period-late-eastern-han", "major",
        "官渡战后袁绍病卒（202年），其子袁谭、袁尚兄弟内讧，"
        "曹操先后击灭二袁，207年北征乌桓克柳城，袁氏残余势力彻底消灭，"
        "曹操基本统一北方（详见既有 event-three-north-consolidation）。",
        f"古代史料：《三国志·魏书·武帝纪》《袁绍传》；现代参考：{MODERN['three']}",
        W["sanguo"],
        [_rel("event-three-guandu", "follows", desc="官渡之战后袁绍势力走向瓦解"),
         _rel("event-three-north-consolidation", "part_of", 0.7, desc="袁氏败亡为曹操统一北方的重要一步")],
        review_note="袁绍卒于202年、二袁并灭至207年北征乌桓；\"袁氏瓦解\"为这一过程的事件。"),
    _ev("event-liubei-qu-yizhou", "刘备取益州（入蜀）", "war",
        211, 214, "range", "period-late-eastern-han", "major",
        "建安十六年（211年）刘备应刘璋之邀入蜀协防张鲁，次年发动攻蜀战争，"
        "214年克成都，刘璋出降，刘备据有益州。蜀汉立国的基础由此奠定，"
        "三国鼎立的版图格局大体成形。",
        f"古代史料：《三国志·蜀书·先主传》《庞统法正传》；现代参考：{MODERN['three']}",
        W["sanguo"],
        [],
        review_note="刘备取益州过程达三年（211—214）；与孙吴\"借荆州\"争端一并构成吴蜀关系背景。"),
    _ev("event-zhang-song-yin-shu", "张松法正献计引刘备入蜀", "political",
        211, 211, "year", "period-late-eastern-han", "major",
        "建安十六年（211年），益州别驾张松与其党法正等因不满刘璋，"
        "劝说刘璋迎刘备入蜀以拒张鲁、曹公，实为引刘备入主益州之策。"
        "刘备遂率军溯江入蜀，开启对益州的争夺。",
        f"古代史料：《三国志·蜀书·先主传》《张松法正传》；现代参考：{MODERN['three']}",
        W["sanguo"],
        [_rel("event-liubei-qu-yizhou", "leads_to", 0.9, desc="引刘备入蜀直接促成刘备攻取益州")],
        review_note="张松、法正迎刘备（211年）为蜀汉帝业的关键转折；法正后为蜀汉重要谋主。"),
    _ev("event-guan-yu-bei-fa", "关羽北伐襄樊", "war",
        219, 219, "year", "period-late-eastern-han", "major",
        "建安二十四年（219年）关羽自荆州北伐，围樊城、襄阳，"
        "水淹七军擒于禁、斩庞德，\"威震华夏\"，曹操一度欲迁都避之。"
        "关羽北伐是蜀汉势力扩张的顶点，也引发孙权袭荆州的后方危机。",
        f"古代史料：《三国志·蜀书·关羽传》；现代参考：{MODERN['three']}",
        W["sanguo"],
        [_rel("event-lv-meng-xi-jingzhou", "leads_to", 0.9, desc="关羽主力北上，孙权乘虚袭取荆州")],
        review_note="关羽北伐襄樊（219年）为三国鼎立前夕的转折战役；\"水淹七军\"见《关羽传》。"),
    _ev("event-lv-meng-xi-jingzhou", "吕蒙袭取荆州、关羽败亡", "war",
        219, 219, "year", "period-late-eastern-han", "major",
        "建安二十四年（219年）冬，孙权遣吕蒙、陆逊乘关羽北征之机，"
        "以\"白衣渡江\"袭取荆州（江陵），关羽退走麦城，被俘杀。"
        "荆州归吴、关羽身死，蜀汉元气大伤，孙刘联盟破裂，三国疆界自此定型。",
        f"古代史料：《三国志·吴书·吕蒙传》《蜀书·关羽传》；现代参考：{MODERN['three']}",
        W["sanguo"],
        [_rel("event-guan-yu-bei-fa", "follows"),
         _rel("event-yiling-zhizhan", "leads_to", 0.85, desc="荆州之失与关羽之死直接引发夷陵之战")],
        review_note="\"白衣渡江\"袭荆州在219年闰十月前后；关羽被杀于麦城。"),
]

# ---------------------------------------------------------------------------
# Phase 2 — 三国（220–263）
# ---------------------------------------------------------------------------
PHASE_THREE_KINGDOMS = [
    _ev("event-caopi-dai-han", "曹丕代汉、曹魏建立", "dynastic-transition",
        220, 220, "year", "period-three-kingdoms", "critical",
        "建安二十五年（220年）正月曹操去世，十月曹丕接受汉献帝禅让称帝，"
        "改元黄初，国号魏，东汉正式灭亡。"
        "曹丕代汉是三国鼎立格局在名分上的确立，也是\"禅让\"改朝模式的重要案例。",
        f"古代史料：《三国志·魏书·文帝纪》《后汉书·献帝纪》；现代参考：{MODERN['three']}",
        W["sanguo"],
        ["regime-cao-wei"],
        [_rel("event-lv-meng-xi-jingzhou", "follows"),
         _rel("event-liubei-chengdi", "leads_to", 0.85, desc="曹魏代汉后刘备亦践祚称帝以继汉统")],
        review_note="曹丕代汉在220年十月（延康元年/黄初元年）；\"魏受汉禅\"为通行表述。"),
    _ev("event-liubei-chengdi", "刘备称帝、蜀汉建立", "dynastic-transition",
        221, 221, "year", "period-three-kingdoms", "major",
        "章武元年（221年）四月，刘备在成都称帝，国号汉（史称蜀汉或季汉），"
        "宣称继承汉统。蜀汉建立与曹魏并峙，三国政权结构完成三分之二。",
        f"古代史料：《三国志·蜀书·先主传》；现代参考：{MODERN['three']}",
        W["sanguo"],
        ["regime-shu-han"],
        [_rel("event-caopi-dai-han", "follows", desc="魏代汉后刘备继汉统称帝"),
         _rel("event-yiling-zhizhan", "leads_to", 0.8, desc="刘备称帝后发动伐吴之役（夷陵之战）")],
        review_note="刘备221年称帝（章武元年）；国号\"汉\"而史称蜀汉。"),
    _ev("event-yiling-zhizhan", "夷陵之战", "war",
        221, 222, "range", "period-three-kingdoms", "major",
        "章武元年至二年（221—222年），刘备以复关羽之仇、夺荆州为名东征孙吴，"
        "陆逊在夷陵（今湖北宜昌一带）以逸待劳，火攻大破蜀军，刘备败退白帝城。"
        "夷陵之战巩固了吴对荆州的占有，三国疆界由此长期稳定。",
        f"古代史料：《三国志·吴书·陆逊传》《蜀书·先主传》；现代参考：{MODERN['three']}",
        W["sanguo"],
        ["regime-shu-han", "regime-eastern-wu"],
        [_rel("event-lv-meng-xi-jingzhou", "follows"),
         _rel("event-liubei-beng-zhugeliang", "leads_to", 0.85, desc="夷陵败后刘备病逝，诸葛亮受命辅政")],
        review_note="夷陵之战（221—222）以陆逊火攻大捷终；刘备欲取荆州与报关羽之仇并见《三国志》。"),
    _ev("event-liubei-beng-zhugeliang", "刘备去世、诸葛亮辅政", "political",
        223, 223, "year", "period-three-kingdoms", "major",
        "章武三年（223年）四月刘备病逝于白帝城，太子刘禅即位，"
        "诸葛亮受遗诏辅政，\"政事无巨细，咸决于亮\"。"
        "诸葛亮掌权后与孙吴重结联盟，稳定蜀汉内外局势。",
        f"古代史料：《三国志·蜀书·诸葛亮传》《先主传》；现代参考：{MODERN['three']}",
        W["sanguo"],
        ["regime-shu-han"],
        [_rel("event-yiling-zhizhan", "follows"),
         _rel("event-zhuge-liang-nanzheng", "leads_to", 0.8, desc="辅政后先平定南中再北伐")],
        review_note="223年刘备托孤白帝城；王连、邓芝等恢复吴蜀联盟属辅政要务。"),
    _ev("event-zhuge-liang-nanzheng", "诸葛亮南征", "war",
        225, 225, "year", "period-three-kingdoms", "major",
        "建兴三年（225年）诸葛亮率军南征，平定南中（今云贵一带）雍闿、高定、孟获等反叛，"
        "\"七擒孟获\"传说载于《汉晋春秋》等后出文献。南征稳定后方，"
        "为北伐中原解除后顾之忧。",
        f"古代史料：《三国志·蜀书·诸葛亮传》；现代参考：{MODERN['three']}",
        W["sanguo"],
        ["regime-shu-han"],
        [_rel("event-liubei-beng-zhugeliang", "follows"),
         _rel("event-zhuge-liang-beifa", "leads_to", 0.8, desc="平定南中后诸葛亮全力北伐")],
        review_note="南征在225年（建兴三年）；\"七擒孟获\"出自《华阳国志》《汉晋春秋》（后出文献），非《三国志》本体记载。"),
    _ev("event-zhuge-liang-beifa", "诸葛亮北伐", "war",
        228, 234, "range", "period-three-kingdoms", "major",
        "建兴六年至十二年（228—234年），诸葛亮五次出兵北伐曹魏，"
        "多为粮尽退兵，未能实现\"兴复汉室\"目标。本事件为 aggregate，"
        "子事件（首次北伐、五丈原）经 part_of 关联，历次战役细节不在主干单列。",
        f"古代史料：《三国志·蜀书·诸葛亮传》；现代参考：{MODERN['three']}",
        W["sanguo"],
        ["regime-shu-han"],
        [_rel("event-zhuge-liang-nanzheng", "follows"),
         _rel("event-zhuge-liang-zhishi", "precedes", desc="北伐至五丈原诸葛亮病逝而止")],
        review_note="诸葛亮北伐（228—234）为五次出兵的 process；具体战役（街亭、陈仓等）见子事件与 review。"),
    _ev("event-zhuge-liang-shoubei", "诸葛亮首次北伐（街亭之战）", "war",
        228, 228, "year", "period-three-kingdoms", "major",
        "建兴六年（228年）诸葛亮第一次北伐，南安、天水、安定三郡响应，"
        "马谡违令失守街亭致全局失利，诸葛亮被迫退军并斩马谡。"
        "首出祁山虽功亏一篑，但\"三郡响应\"显示北伐的战略冲击。",
        f"古代史料：《三国志·蜀书·诸葛亮传》《马谡传》；现代参考：{MODERN['three']}",
        W["sanguo"],
        ["regime-shu-han"],
        [_rel("event-zhuge-liang-beifa", "part_of", 0.9, desc="首次北伐为诸葛亮北伐的起点"),
         _rel("event-zhuge-liang-zhishi", "precedes")],
        review_note="街亭之败与\"挥泪斩马谡\"记载见《三国志》及《襄阳记》等；\"空城计\"为《三国演义》演绎非正史。"),
    _ev("event-zhuge-liang-zhishi", "诸葛亮病逝五丈原", "political",
        234, 234, "year", "period-three-kingdoms", "major",
        "建兴十二年（234年）诸葛亮率军出斜谷进驻五丈原，与司马懿对峙百余日，"
        "八月病逝于军中，\"出师未捷身先死\"。诸葛亮去世后蜀汉由姜维等主持北伐，"
        "蜀汉国力渐衰。",
        f"古代史料：《三国志·蜀书·诸葛亮传》；现代参考：{MODERN['three']}",
        W["sanguo"],
        ["regime-shu-han"],
        [_rel("event-zhuge-liang-beifa", "part_of", 0.9, desc="第五次北伐以诸葛亮病逝告终"),
         _rel("event-jiangwei-beifa", "leads_to", 0.7, desc="诸葛亮之后姜维主持蜀汉北伐")],
        review_note="诸葛亮卒于234年八月（建兴十二年）；其政治与军事遗产深刻影响蜀汉内外。"),
    _ev("event-jiangwei-beifa", "姜维北伐", "war",
        247, 262, "range", "period-three-kingdoms", "major",
        "延熙至景耀年间（约247—262年），姜维多次出兵北伐曹魏，"
        "虽屡有胜绩却耗损蜀汉国力，\"费祎常制姜维\"之说反映朝中分歧。"
        "姜维北伐延续蜀汉进取战略，但未能改变魏强蜀弱的总体格局。",
        f"古代史料：《三国志·蜀书·姜维传》；现代参考：{MODERN['three']}",
        W["sanguo"],
        ["regime-shu-han"],
        [_rel("event-zhuge-liang-zhishi", "follows"),
         _rel("event-wei-mie-shu", "precedes", desc="姜维北伐终未能阻魏军灭蜀")],
        review_note="姜维北伐为多次出兵的过程（约247—262），本节点为 process 事件，未逐役单列。"),
    _ev("event-gaopingling-zhi-bian", "高平陵之变", "political",
        249, 249, "year", "period-three-kingdoms", "major",
        "正始十年（249年）正月，司马懿趁曹爽兄弟陪同少帝曹芳往高平陵祭陵之机，"
        "发动政变控制洛阳，收捕曹爽等并族诛，曹魏军政大权自此落入司马氏。"
        "高平陵之变是曹魏政权由曹氏向司马氏转移的决定性节点，也是三国史的重要转折。",
        f"古代史料：《三国志·魏书·曹爽传》《晋书·宣帝纪》；现代参考：{MODERN['three']}",
        W["sanguo"],
        ["regime-cao-wei"],
        [_rel("event-jiangwei-beifa", "precedes"),
         _rel("event-cao-mao-zhisha", "leads_to", 0.85, desc="司马氏掌权后继续清除曹氏势力（曹髦被杀）")],
        review_note="高平陵之变在249年正月（正始十年）；司马懿诛曹爽\"夷三族\"为《三国志》《晋书》共载。"),
    _ev("event-cao-mao-zhisha", "曹髦被杀（司马昭专权）", "political",
        260, 260, "year", "period-three-kingdoms", "major",
        "甘露五年（260年）魏帝曹髦不甘坐收，率宿卫攻司马昭府第，"
        "被贾充指使成济刺死。曹髦\"司马昭之心，路人所知也\"之语见于《汉晋春秋》。"
        "弑君事件显示司马氏废立已不可逆转，曹魏皇权名存实亡。",
        f"古代史料：《三国志·魏书·高贵乡公纪》《晋书·文帝纪》；现代参考：{MODERN['three']}",
        W["sanguo"],
        ["regime-cao-wei"],
        [_rel("event-gaopingling-zhi-bian", "follows"),
         _rel("event-wei-mie-shu", "precedes", desc="曹氏皇权衰微后司马氏灭蜀以积代魏之资")],
        review_note="曹髦之死在260年（甘露五年）；\"司马昭之心\"语出《汉晋春秋》，非《三国志》正文。"),
    _ev("event-sunquan-chengdi", "孙权称帝、孙吴建立", "dynastic-transition",
        229, 229, "year", "period-three-kingdoms", "major",
        "黄龙元年（229年）四月孙权称帝，国号吴，都建业。"
        "孙权称帝后三国鼎立的名分结构完全确立（魏、汉、吴并立）。",
        f"古代史料：《三国志·吴书·孙权传》；现代参考：{MODERN['three']}",
        W["sanguo"],
        ["regime-eastern-wu"],
        [_rel("event-zhuge-liang-beifa", "precedes", desc="吴蜀联盟维持下孙权称帝与蜀汉并称二帝")],
        review_note="孙权229年称帝（黄龙元年）；吴自222年已建号黄武，称帝则迟至229年。"),
    _ev("event-wei-mie-shu", "魏灭蜀", "war",
        263, 263, "year", "period-three-kingdoms", "major",
        "景元四年（263年）司马昭遣钟会、邓艾、诸葛绪三路伐蜀，"
        "邓艾偷渡阴平直取成都，刘禅出降，蜀汉灭亡。"
        "魏灭蜀使三国并立变为魏吴对峙，为司马氏代魏扫清最大障碍。",
        f"古代史料：《三国志·魏书·钟会邓艾传》《蜀书·后主传》；现代参考：{MODERN['three']}",
        W["sanguo"],
        ["regime-cao-wei", "regime-shu-han"],
        [_rel("event-jiangwei-beifa", "follows"),
         _rel("event-sima-yan-dai-wei", "leads_to", 0.9, desc="灭蜀积功，司马昭进封晋王，其子司马炎代魏")],
        review_note="魏灭蜀在263年（景元四年）；\"蜀汉\"终、姜维诈降被杀。灭蜀之役为三国格局终结第一步。"),
]

# ---------------------------------------------------------------------------
# Phase 3 — 西晋（265–316）
# ---------------------------------------------------------------------------
PHASE_WESTERN_JIN = [
    _ev("event-sima-yan-dai-wei", "司马炎代魏、西晋建立", "dynastic-transition",
        265, 265, "year", "period-western-jin", "major",
        "泰始元年（265年）司马炎接受魏元帝禅让称帝，国号晋（西晋），"
        "定都洛阳。司马氏经高平陵之变、灭蜀立晋，完成\"以晋代魏\"。",
        f"古代史料：《晋书·武帝纪》《三国志·魏书·文帝纪》所记禅代系谱；现代参考：{MODERN['wj']}",
        W["jinshu_zizhi"],
        ["regime-western-jin"],
        [_rel("event-wei-mie-shu", "follows", desc="魏灭蜀后司马氏稳固权威、代魏建晋"),
         _rel("event-jin-mie-wu", "leads_to", 0.9, desc="西晋建立后统一三国，晋灭吴")],
        review_note="司马炎代魏在265年（泰始元年），西晋建立与代魏为同一事件的两个面向，未分列为两 Event。"),
    _ev("event-jin-mie-wu", "晋灭吴、西晋统一", "war",
        280, 280, "year", "period-western-jin", "critical",
        "太康元年（280年）晋武帝发六路大军伐吴，王濬楼船径取建业，孙皓出降，吴亡。"
        "晋灭吴结束三国鼎立，西晋完成全国统一，"
        "中国自东汉末动荡以来首次重归一统。",
        f"古代史料：《晋书·武帝纪》《王濬传》《三国志·吴书·孙皓传》；现代参考：{MODERN['wj']}",
        W["jinshu_zizhi"],
        ["regime-western-jin"],
        [_rel("event-sima-yan-dai-wei", "follows", desc="西晋立国十五年后灭吴统一"),
         _rel("event-jin-wudi-beng", "precedes", desc="统一后晋武帝晚年政治走向腐化")],
        review_note="晋灭吴在280年（太康元年）；\"王濬楼船下益州\"为《王濬传》记载。西晋统一与灭吴为同一节点，未拆分重复。"),
    _ev("event-jin-wudi-beng", "晋武帝去世、惠帝即位", "political",
        290, 290, "year", "period-western-jin", "major",
        "太熙元年（290年）晋武帝司马炎去世，太子司马衷（惠帝）即位，"
        "杨太后之父杨骏辅政。惠帝\"何不食肉糜\"反映其昏弱，"
        "皇权真空为贾后干政与八王之乱埋下伏笔。",
        f"古代史料：《晋书·武帝纪》《惠帝纪》《贾后传》；现代参考：{MODERN['wj']}",
        W["jinshu"],
        ["regime-western-jin"],
        [_rel("event-jin-mie-wu", "follows"),
         _rel("event-bawang-zhi-luan", "leads_to", 0.85, desc="武帝去世、惠帝暗弱，诸王与贾后卷入权力斗争")],
        review_note="晋武帝崩于290年（太熙元年）；杨骏辅政旋即被诛属八王之乱序幕。"),
    _ev("event-bawang-zhi-luan", "八王之乱", "political-military",
        291, 306, "range", "period-western-jin", "critical",
        "元康元年至光熙元年（291—306年），西晋宗室诸王（汝南王亮、楚王玮、"
        "赵王伦、齐王冏、长沙王乂、成都王颖、河间王颙、东海王越）围绕皇权反复混战，"
        "史称\"八王之乱\"。战乱使西晋国力耗竭、社会秩序崩坏，"
        "并直接诱发五部匈奴等北方民族力量起兵，最终导致西晋灭亡。",
        f"古代史料：《晋书·孝惠帝纪》《八王列传》；现代参考：{MODERN['wj']}",
        W["jinshu"],
        ["regime-western-jin"],
        [_rel("event-jin-wudi-beng", "follows"),
         _rel("event-yongjia-zhi-luan", "leads_to", 0.9, desc="八王之乱耗尽西晋力量，直接导向永嘉之祸")],
        review_note="八王之乱（291—306）为宗室诸王争夺皇权的长期混战（aggregate）；八王名单与排序各史记载略有出入，子事件见 part_of 关联。"),
    _ev("event-jia-hou-gan-zheng", "贾后干政与政变", "political",
        291, 300, "range", "period-western-jin", "major",
        "八王之乱初期，惠帝皇后贾南风于291年联合楚王玮诛杀杨骏夺权，"
        "继而专擅朝政十余年，300年为赵王伦所诛。贾后干政是八王之乱第一阶段的核心，"
        "反映外戚、后妃与宗室三方争夺皇权。",
        f"古代史料：《晋书·贾后传》《惠帝纪》；现代参考：{MODERN['wj']}",
        W["jinshu"],
        ["regime-western-jin"],
        [_rel("event-bawang-zhi-luan", "part_of", 0.9, desc="贾后干政为八王之乱的序幕与第一阶段")],
        review_note="贾后诛杨骏在291年（元康元年）；300年赵王伦杀贾后。\"太子废立\"之争为其间重要事件。"),
    _ev("event-zhaowang-lun-chengdi", "赵王伦篡位", "political",
        301, 301, "year", "period-western-jin", "major",
        "永康二年（301年）正月，赵王司马伦废惠帝自立称帝，"
        "三月齐王冏、成都王颖、河间王颙等起兵讨伐，四月伦败废，惠帝复位。"
        "赵王伦篡位是八王之乱中唯一一次宗王正式称帝，诸王从此名分尽失、各怀异志。",
        f"古代史料：《晋书·赵王伦传》；现代参考：{MODERN['wj']}",
        W["jinshu"],
        ["regime-western-jin"],
        [_rel("event-bawang-zhi-luan", "part_of", 0.9, desc="赵王伦篡位为八王之乱第二阶段"),
         _rel("event-jia-hou-gan-zheng", "follows")],
        review_note="赵王伦称帝在301年（永康二年）；其\"篡逆\"与讨伐体系为八王混战的转折。"),
    _ev("event-sima-yue-pingluan", "东海王司马越定乱", "political",
        306, 306, "year", "period-western-jin", "major",
        "光熙元年（306年）东海王司马越控制朝廷、毒杀惠帝、立怀帝，"
        "八王之乱至此结束。但西晋经此乱已大伤元气，宗室自相残杀耗尽统治基础，"
        "北方各族人民的反抗随即爆发。",
        f"古代史料：《晋书·东海王越传》《惠帝纪》；现代参考：{MODERN['wj']}",
        W["jinshu"],
        ["regime-western-jin"],
        [_rel("event-bawang-zhi-luan", "part_of", 0.9, desc="司马越定乱为八王之乱收尾"),
         _rel("event-zhaowang-lun-chengdi", "follows")],
        review_note="司马越于306年（光熙元年）结束八王之乱；其掌权后西晋仍以司马越为中心延续数年。"),
    _ev("event-li-te-qiyi", "李特流民起义（益州）", "rebellion",
        301, 303, "range", "period-western-jin", "major",
        "永宁元年（301年）益州流民领袖李特领导流民武装反抗西晋苛政，"
        "先后败赵廞、击败罗尚，303年兵败被杀，其子李雄继之并于306年建立成汉。"
        "李特起义是西晋末年北方流民与民族矛盾激化的早期信号之一。",
        f"古代史料：《晋书·李特载记》《华阳国志》追述；现代参考：{MODERN['wj']}",
        W["jinshu_zizhi"],
        ["regime-western-jin"],
        [_rel("event-bawang-zhi-luan", "follows", desc="西晋乱局中地方反抗抬头"),
         _rel("event-liu-yuan-qibing", "precedes", desc="流民反抗与五部匈奴起兵同为西晋末动荡")],
        review_note="李特起义（301—303）为成汉政权的先声；\"流民\"问题贯穿西晋末年。"),
    _ev("event-liu-yuan-qibing", "刘渊起兵、汉赵政权建立", "dynastic-transition",
        304, 308, "range", "period-western-jin", "major",
        "永兴元年（304年）匈奴五部之左部帅刘渊在离石起兵，建国号汉，"
        "自称汉王，追尊刘禅为孝怀皇帝以承汉统；308年称帝。"
        "刘渊建汉（后史称汉赵或前赵）是西晋崩溃中北方胡族政权建立的标志，"
        "此后北方持续陷入多政权并立。",
        f"古代史料：《晋书·刘元海载记》；现代参考：{MODERN['wj']}",
        W["jinshu"],
        ["regime-han-zhao"],
        [_rel("event-bawang-zhi-luan", "follows", desc="八王之乱中诸王争结刘渊，助其坐大"),
         _rel("event-yongjia-zhi-luan", "leads_to", 0.85, desc="刘渊汉军南下攻晋，引发永嘉之乱")],
        review_note="刘渊304年建汉称汉王、308年称帝；后世以\"汉赵/前赵\"称其政权（刘曜319年改国号赵）。名字沿用史界通行称谓（§41）。"),
    _ev("event-yongjia-zhi-luan", "永嘉之乱", "war",
        311, 316, "range", "period-western-jin", "critical",
        "永嘉五年至建兴四年（311—316年），汉赵军攻破洛阳（311年）、"
        "掳晋怀帝，其后又陷长安（316年）虏愍帝，西晋灭亡。"
        "永嘉之乱（本事件为过程 aggregate）标志西晋统治在北方的彻底崩溃与"
        "\"衣冠南渡\"之始。",
        f"古代史料：《晋书·孝怀帝纪》《愍帝纪》；现代参考：{MODERN['wj']}",
        W["jinshu"],
        ["regime-han-zhao"],
        [_rel("event-liu-yuan-qibing", "follows"),
         _rel("event-luoyang-xianshi", "part_of", 0.9, desc="洛阳失陷为永嘉之乱核心节点"),
         _rel("event-xijin-mie-wang", 0.85, "part_of", desc="长安陷落西晋灭亡为永嘉之乱终点")],
        review_note="永嘉之乱起止口径：本事件将\"洛阳破（311）至长安破西晋亡（316）\"作为过程，\\\"永嘉\"为怀帝年号（307—313）。注意\"五胡乱华\"一词为后世史论传统提法，本 Backbone 采用\"永嘉之乱/十六国政权并立\"等可验证表述（§42）。"),
    _ev("event-luoyang-xianshi", "洛阳失陷、晋怀帝被俘", "war",
        311, 311, "year", "period-western-jin", "major",
        "永嘉五年（311年）刘聪遣刘曜、石勒等攻晋，六月破洛阳，"
        "俘晋怀帝（次年遇害），纵兵烧掠宫室，掳王公士民数万。"
        "洛阳失陷是西晋政治中心及北方秩序的毁灭性打击。",
        f"古代史料：《晋书·孝怀帝纪》《刘聪载记》；现代参考：{MODERN['wj']}",
        W["jinshu"],
        ["regime-han-zhao"],
        [_rel("event-yongjia-zhi-luan", "part_of", 0.95, desc="洛阳失陷为永嘉之乱关键子事件"),
         _rel("event-xijin-mie-wang", 0.85, "leads_to", desc="洛阳既破，西晋仅存长安残余")],
        review_note="洛阳破于311年六月（永嘉五年）；怀帝被掳次年遇害。\"刘曜石勒抢略\"细节见《载记》。"),
    _ev("event-xijin-mie-wang", "长安陷落、西晋灭亡", "war",
        316, 316, "year", "period-western-jin", "critical",
        "建兴四年（316年）刘曜围长安，晋愍帝出降，西晋灭亡。"
        "西晋亡国为\"永嘉之乱\"的终点，也标志北方进入\"十六国\"多政权并立时代，"
        "而南方则孕育出东晋政权。",
        f"古代史料：《晋书·愍帝纪》《刘曜载记》；现代参考：{MODERN['wj']}",
        W["jinshu"],
        ["regime-han-zhao"],
        [_rel("event-luoyang-xianshi", 0.9, "follows"),
         _rel("event-dongjin-jianguo", 0.85, "leads_to", desc="西晋亡后司马睿在建康立东晋")],
        review_note="长安陷于316年十一月，愍帝被虏（318年遇害）；54年（280—316）一统局面终结。"),
]

# ---------------------------------------------------------------------------
# Phase 4 — 东晋 / 十六国（317–439）
# ---------------------------------------------------------------------------
PHASE_EASTERN_JIN_16K = [
    _ev("event-dongjin-jianguo", "东晋建立", "dynastic-transition",
        317, 317, "year", "period-eastern-jin", "critical",
        "建武元年（317年）司马睿在建康（今南京）即晋王位，次年称帝，"
        "史称东晋。东晋建立承接\"衣冠南渡\"，以建康为政治中心，"
        "形成与北方十六国并行的\"南北分治\"格局，中国历史进入东晋十六国阶段。",
        f"古代史料：《晋书·元帝纪》；现代参考：{MODERN['wj']}",
        W["jinshu"],
        ["regime-eastern-jin"],
        [_rel("event-xijin-mie-wang", "follows", desc="西晋亡后司马睿重建晋朝于江南"),
         _rel("event-zuti-beifa", 0.7, "precedes", desc="东晋初年祖逖等北伐恢复中原政策")],
        review_note="司马睿317年称晋王、318年称帝，通行以317年为东晋建立；\"王与马共天下\"反映侨姓门阀与皇权共治格局。"),
    _ev("event-zuti-beifa", "祖逖北伐", "war",
        319, 321, "range", "period-eastern-jin", "major",
        "建兴四年至大兴四年（约319—321年）祖逖率部渡江北伐，"
        "收复黄河以南豫州等地，颇得民心；受朝廷掣肘，321年病逝，"
        "所复之地旋失。祖逖北伐是东晋前期最有名的北伐行动，"
        "反映\"收复中原\"与\"偏安江左\"之间的政治张力。",
        f"古代史料：《晋书·祖逖传》；现代参考：{MODERN['wj']}",
        W["jinshu"],
        ["regime-eastern-jin"],
        [_rel("event-dongjin-jianguo", "follows", desc="东晋立国之初的北伐努力"),
         _rel("event-wangdun-zhi-luan", 0.6, "precedes", desc="北伐受阻与朝廷内斗相伴随")],
        review_note="祖逖北伐（约319—321）为过程事件；\"闻鸡起舞\"\"中流击楫\"为后世传述典故。"),
    _ev("event-wangdun-zhi-luan", "王敦之乱", "political",
        322, 324, "range", "period-eastern-jin", "major",
        "永昌元年至太宁二年（322—324年）荆州都督王敦两次举兵东下，"
        "攻入建康，专权自用，死后叛军为朝廷所平。"
        "王敦之乱是东晋门阀政治下，以地方军事长官挑战皇权与朝臣格局的代表事件。",
        f"古代史料：《晋书·王敦传》《元帝纪》；现代参考：{MODERN['wj']}",
        W["jinshu"],
        ["regime-eastern-jin"],
        [_rel("event-zuti-beifa", "follows"),
         _rel("event-sujun-zhi-luan", 0.6, "precedes", desc="王敦乱后不久苏峻又乱")],
        review_note="王敦之乱（322—324）两次举兵；\"王与马共天下\"背景下，王敦之乱反映士族内部矛盾。"),
    _ev("event-sujun-zhi-luan", "苏峻之乱", "war",
        327, 329, "range", "period-eastern-jin", "major",
        "咸和二年至四年（327—329年）历阳内史苏峻与祖约联合举兵，"
        "攻陷建康、逼走朝廷，后被陶侃、温峤等击败收复京城。"
        "苏峻之乱进一步确立以建康为中心的中央权威与地方军事力量的博弈格局。",
        f"古代史料：《晋书·苏峻传》《成帝纪》；现代参考：{MODERN['wj']}",
        W["jinshu"],
        ["regime-eastern-jin"],
        [_rel("event-wangdun-zhi-luan", "follows", desc="继王敦之乱后的又一次武力挑战中央"),
         _rel("event-shi-le-hou-zhao", 0.6, "precedes", desc="同时期北方后赵崛起")],
        review_note="苏峻之乱（327—329）攻破建康；陶侃温峤平乱后东晋中央权威有所恢复。"),
    _ev("event-shi-le-hou-zhao", "石勒建立后赵", "dynastic-transition",
        319, 319, "year", "period-sixteen-kingdoms", "major",
        "太兴二年（319年）石勒自号赵王，建立后赵政权于河北，"
        "都襄国（今河北邢台）。石勒原为汉赵部将，其自立使北方形成汉赵（前赵）"
        "与后赵并立的格局。",
        f"古代史料：《晋书·石勒载记》；现代参考：{MODERN['wj']}",
        W["jinshu"],
        ["regime-later-zhao"],
        [_rel("event-liu-yuan-qibing", "follows", desc="石勒自汉赵中脱离自立"),
         _rel("event-hou-zhao-bingqian-zhao", 0.7, "precedes", desc="后赵渐强并最终灭前赵")],
        review_note="石勒319年称赵王（都襄国）；\"胡羯\"人口政策与后赵兴衰见《石勒载记》。"),
    _ev("event-hou-zhao-bingqian-zhao", "后赵灭前赵", "war",
        329, 329, "year", "period-sixteen-kingdoms", "major",
        "太和四年（329年）石勒遣石虎攻灭刘曜的前赵，改称天王，都鄴，"
        "后赵基本统一北方除辽东、凉州以外的大部分地区。"
        "此后北方进入后赵一家独大的时期，直至石虎暴政引发动荡。",
        f"古代史料：《晋书·石勒载记》《刘曜载记》；现代参考：{MODERN['wj']}",
        W["jinshu"],
        ["regime-later-zhao"],
        [_rel("event-shi-le-hou-zhao", "follows"),
         _rel("event-ran-wei", 0.7, "precedes", desc="后赵石虎死后北方再乱（冉魏）")],
        review_note="后赵灭前赵在329年；石勒死后石虎（季龙）夺权，349年石虎死，北方陷入新动荡。"),
    _ev("event-ran-wei", "冉魏建立与北方动荡", "political",
        350, 352, "range", "period-sixteen-kingdoms", "major",
        "后赵石虎死后诸子争立，350年将领冉闵（石闵）据邺建立冉魏，"
        "其间发生针对胡羯的排压与屠杀（史称\"杀胡\"，后世史论对其性质多歧见），"
        "北方人口锐减、各族武装混战。352年冉魏为前燕慕容恪所灭。"
        "冉魏之短暂政权反映后赵崩溃后北方社会的极端动荡。",
        f"古代史料：《晋书·石季龙载记》《慕容儁载记》；现代参考：{MODERN['wj']}",
        W["jinshu"],
        ["regime-later-zhao"],
        [_rel("event-hou-zhao-bingqian-zhao", "follows", desc="后赵内乱孕育冉闵崛起"),
         _rel("event-qian-yan-qiang", 0.7, "precedes", desc="冉魏亡于前燕扩张")],
        review_note="冉魏（350—352）为极短命政权；\"杀胡\"之记述涉及古代民族冲突，本库以中性史述记录并注明现代史论多角度解读（§41）。"),
    _ev("event-qian-yan-qiang", "前燕崛起", "dynastic-transition",
        337, 352, "range", "period-sixteen-kingdoms", "major",
        "东晋咸康三年（337年）慕容皝自称燕王，建立前燕于辽东，"
        "至352年慕容儁灭冉魏入主中原。前燕是鲜卑慕容部建立的强盛政权，"
        "其后统一关东大部，成为北方主要力量之一。",
        f"古代史料：《晋书·慕容皝载记》《慕容儁载记》；现代参考：{MODERN['wj']}",
        W["jinshu"],
        ["regime-former-yan"],
        [_rel("event-ran-wei", "follows", desc="前燕乘后赵内乱进入中原"),
         _rel("event-qian-qin-mie-qian-yan", 0.7, "precedes", desc="前燕全盛后为前秦所灭")],
        review_note="前燕建国（337）与入主中原（352）为过程；370年为前秦所灭。"),
    _ev("event-fu-jian-wangmeng", "苻坚即位、王猛辅政", "political",
        357, 357, "year", "period-sixteen-kingdoms", "major",
        "升平元年（357年）苻坚击杀暴虐的苻生即前秦天王位，"
        "重用汉人谋臣王猛，励精图治。苻坚—王猛君臣组合是前秦急速崛起的关键。",
        f"古代史料：《晋书·苻坚载记》《王猛传》；现代参考：{MODERN['wj']}",
        W["jinshu"],
        ["regime-former-qin"],
        [_rel("event-qian-yan-qiang", "precedes"),
         _rel("event-wangmeng-gaige", 0.9, "leads_to", desc="苻坚即位后王猛主持改革")],
        review_note="苻坚357年得位（升平元年/永兴元年）；王猛辅政方针（抑制豪强、劝课农桑）见《载记》。"),
    _ev("event-wangmeng-gaige", "王猛改革", "reform",
        357, 375, "range", "period-sixteen-kingdoms", "major",
        "苻坚在位前期（357—375年），王猛任中书令、司隶校尉等，"
        "整饬吏治、抑制豪强、劝课农桑、兴办学校，前秦经济军事实力大增。"
        "王猛改革是十六国时期少见而成功的汉族士人主持的制度改革。",
        f"古代史料：《晋书·苻坚载记》《王猛传》；现代参考：{MODERN['wj']}",
        W["jinshu"],
        ["regime-former-qin"],
        [_rel("event-fu-jian-wangmeng", "follows"),
         _rel("event-qian-qin-tongyi", 0.85, "leads_to", desc="王猛改革为前秦统一北方奠定基础")],
        review_note="王猛改革（357—375）为过程节点；375年王猛去世，前秦统一后战略由苻坚主导。"),
    _ev("event-qian-qin-mie-qian-yan", "前秦灭前燕", "war",
        370, 370, "year", "period-sixteen-kingdoms", "major",
        "太和五年（370年）苻坚遣王猛率军伐前燕，克邺城，俘慕容暐，前燕灭亡。"
        "前秦灭前燕后囊括关东富庶之地，成为十六国中最强大的政权。",
        f"古代史料：《晋书·苻坚载记》《慕容暐载记》；现代参考：{MODERN['wj']}",
        W["jinshu"],
        ["regime-former-qin"],
        [_rel("event-wangmeng-gaige", "follows"),
         _rel("event-qian-qin-tongyi", 0.95, "leads_to", desc="灭前燕为前秦统一北方关键一步")],
        review_note="前秦灭前燕在370年（太和五年）；王猛领军伐燕为苻坚统一战略骨干。"),
    _ev("event-qian-qin-tongyi", "前秦统一北方", "war",
        376, 376, "year", "period-sixteen-kingdoms", "major",
        "太元元年（376年）前秦连灭前凉、代国（鲜卑拓跋部），"
        "基本统一北方。自西晋灭亡以来，北方首次出现覆盖大部地区的统一政权——前秦，"
        "为其后南下攻晋（淝水之战）准备了条件。",
        f"古代史料：《晋书·苻坚载记》；现代参考：{MODERN['wj']}",
        W["jinshu_zizhi"],
        ["regime-former-qin"],
        [_rel("event-qian-qin-mie-qian-yan", "follows"),
         _rel("event-feishui-zhizhan", "leads_to", 0.9, desc="统一北方后苻坚东下攻晋，决战淝水")],
        review_note="前秦统一北方在376年（灭前凉、代）；\"统一北方\"为过程事件，未拆分灭凉/灭代两幕。"),
    _ev("event-feishui-zhizhan", "淝水之战", "war",
        383, 383, "year", "period-eastern-jin", "critical",
        "太元八年（383年）前秦苻坚大举南征东晋，"
        "东晋谢安、谢玄以八万北府兵在淝水（今安徽寿县一带）大败前秦军，"
        "前秦号称百万之众土崩瓦解。淝水之战保住东晋半壁江山，"
        "并直接导致前秦崩裂、北方再度分裂，南北对峙格局由此长期延续。",
        f"古代史料：《晋书·苻坚载记》《谢玄传》《资治通鉴·晋纪》；现代参考：{MODERN['wj']}",
        W["jinshu_zizhi"],
        ["regime-eastern-jin", "regime-former-qin"],
        [_rel("event-qian-qin-tongyi", "follows", desc="前秦统一后南征东晋"),
         _rel("event-qian-qin-wajie", 0.9, "leads_to", desc="淝水败绩直接引发前秦瓦解")],
        review_note="淝水之战在383年十一月；前秦兵力\"号称百万\"与实际兵力存在记载差异；\"草木皆兵\"\"风声鹤唳\"为典故化描述。东晋与前秦为两国政权（regime_ids 并列）。"),
    _ev("event-qian-qin-wajie", "前秦瓦解", "political",
        384, 394, "range", "period-sixteen-kingdoms", "major",
        "淝水之战后，前秦统治下的各族首领纷纷自立：慕容垂称后燕（384）、"
        "姚苌称后秦（384）、苻坚为姚苌所擒杀（385）；"
        "至394年慕容垂灭西燕、姚兴灭前秦，前秦彻底灭亡。"
        "前秦瓦解使北方重新陷入十几个政权并立的\"复分裂\"状态。",
        f"古代史料：《晋书·苻坚载记》《姚苌载记》《慕容垂载记》；现代参考：{MODERN['wj']}",
        W["jinshu"],
        ["regime-former-qin"],
        [_rel("event-feishui-zhizhan", "follows"),
         _rel("event-hou-yan-jianli", 0.8, "leads_to", desc="前秦瓦解后后燕后秦等政权并立")],
        review_note="前秦瓦解（384—394）为过程；各族复国与自立说明淝水败后前秦统治根基（民族关系）之脆弱。"),
    _ev("event-hou-yan-jianli", "后燕建立", "dynastic-transition",
        384, 384, "year", "period-sixteen-kingdoms", "major",
        "慕容垂于太元九年（384年）称燕王，重建燕政权（后燕），都中山。"
        "后燕吸取前秦复置诸州经验，一度控制河北、山东大部，"
        "是淝水后北方最强大的政权，最终败于北魏（参合陂之战）。",
        f"古代史料：《晋书·慕容垂载记》；现代参考：{MODERN['wj']}",
        W["jinshu"],
        ["regime-later-yan"],
        [_rel("event-qian-qin-wajie", "follows"),
         _rel("event-beiwei-mie-hou-yan", 0.7, "precedes", desc="后燕成为北魏扩张的主要对手")],
        review_note="慕容垂384年称王（都中山）；395年参合陂之战败于北魏，396年北魏大举攻燕，398年慕容宝弃中山。"),
    _ev("event-hou-qin-jianli", "后秦建立", "dynastic-transition",
        384, 384, "year", "period-sixteen-kingdoms", "major",
        "羌族首领姚苌于384年称帝建国（后秦），都长安，"
        "385年擒杀苻坚。后秦经姚兴发展，领有关中西部与河洛，"
        "417年为刘裕北伐所灭。",
        f"古代史料：《晋书·姚苌载记》《姚兴载记》；现代参考：{MODERN['wj']}",
        W["jinshu"],
        ["regime-later-qin"],
        [_rel("event-qian-qin-wajie", "follows"),
         _rel("event-liuyu-beifa", 0.7, "precedes", desc="后秦为刘裕北伐所灭（417）")],
        review_note="姚苌384年建国、385年杀苻坚；后秦灭于417年（刘裕北伐）。"),
    _ev("event-beiwei-jianguo", "拓跋珪重建代国、北魏建立", "dynastic-transition",
        386, 386, "year", "period-sixteen-kingdoms", "major",
        "登国元年（386年）拓跋珪在牛川重建代国，随即改称魏，"
        "都盛乐，后迁平城（398年）。北魏的建立标志着拓跋鲜卑由部落联盟"
        "走向国家政权，并逐步成为统一北方的主导力量。",
        f"古代史料：《魏书·太祖纪》；现代参考：{MODERN['wj']}",
        W["weishu"],
        ["regime-northern-wei"],
        [_rel("event-qian-qin-wajie", "precedes", desc="前秦崩溃中拓跋部重建政权"),
         _rel("event-beiwei-mie-hou-yan", 0.8, "leads_to", desc="北魏先破后燕（参合陂）再定关东")],
        review_note="拓跋珪386年建魏（登国元年）；\"代国\"为前秦所并之前的旧号。398年迁都平城、称帝（皇始）。"),
    _ev("event-beiwei-mie-hou-yan", "北魏击灭后燕（参合陂之战）", "war",
        395, 398, "range", "period-sixteen-kingdoms", "major",
        "皇始元年（395年）北魏与后燕会战参合陂，慕容宝军主力几尽，"
        "396年拓跋珪率大军攻燕，398年克中山、檀州，后燕分裂（慕容德南奔建南燕）。"
        "北魏击灭后燕后取得河北、山西，成为北方最强的政权。",
        f"古代史料：《魏书·太祖纪》；现代参考：{MODERN['wj']}",
        W["weishu"],
        ["regime-northern-wei", "regime-later-yan"],
        [_rel("event-beiwei-jianguo", "follows"),
         _rel("event-beiwei-tongyi-beifang", 0.8, "leads_to", desc="灭后燕为北魏统一北方的关键一步")],
        review_note="参合陂之战在395年；398年北魏取中山（后燕都），后燕分裂为北燕、南燕等。"),
    _ev("event-beiwei-tongyi-beifang", "北魏统一北方（灭北凉）", "war",
        439, 439, "year", "period-northern-southern", "critical",
        "太延五年（439年）北魏太武帝拓跋焘西征，克姑臧，北凉沮渠牧犍出降，"
        "十六国中最后一个政权被灭，北魏统一北方（此前已灭胡夏431、北燕436）。"
        "自此中国北方重归一统，与南方刘宋并峙，南北朝对峙格局正式确立。",
        f"古代史料：《魏书·世祖纪》《沮渠蒙逊载记》；现代参考：{MODERN['wj']}",
        W["weishu"],
        ["regime-northern-wei", "regime-northern-liang"],
        [_rel("event-beiwei-mie-hou-yan", "follows"),
         _rel("event-xiaowendi-gaige", "leads_to", 0.7, desc="北魏统一北方后向中原制度转型（孝文帝改革）")],
        review_note="北魏统一北方在439年（灭北凉）；年初已灭胡夏、北燕。本事件兼为\"北魏灭北凉\"与\"北魏统一北方\"两个面向的合一节点（§48 粒度判断）。period 取 period-northern-southern（南北对峙确立），十六国 Period（304—439）之末年代口径见 REVIEW。"),
    _ev("event-huan-wen-beifa", "桓温北伐", "war",
        354, 369, "range", "period-eastern-jin", "major",
        "永和十年至太和四年（354—369年）东晋权臣桓温三次北伐："
        "354年伐前秦至灞上、356年收复洛阳、369年伐前燕败于枋头。"
        "桓温北伐使\"桓温\"成为门阀政治下东晋最有实力的军事领袖，"
        "其禅代意图最终被制。",
        f"古代史料：《晋书·桓温传》；现代参考：{MODERN['wj']}",
        W["jinshu"],
        ["regime-eastern-jin"],
        [_rel("event-sujun-zhi-luan", "follows"),
         _rel("event-sunen-luxun", 0.6, "precedes", desc="桓温之后东晋末年孙恩卢循起事")],
        review_note="桓温三次北伐（354、356、369）为过程；\"北伐\"与\"代晋\"之心（\"桓温将移晋祚\"）见《晋书》。"),
    _ev("event-sunen-luxun", "孙恩卢循起义", "rebellion",
        399, 411, "range", "period-eastern-jin", "major",
        "隆安三年至义熙七年（399—411年）天师道首领孙恩、卢循相继领导东南沿海起义，"
        "孙恩一度逼近建康，402年孙恩败死，卢循续之，至411年为刘裕所灭。"
        "起义沉重打击东晋门阀世家，为刘裕崛起扫除障碍。",
        f"古代史料：《晋书·孙恩传》《卢循传》；现代参考：{MODERN['wj']}",
        W["jinshu_zizhi"],
        ["regime-eastern-jin"],
        [_rel("event-huan-wen-beifa", "follows", desc="东晋末年天师道起事"),
         _rel("event-liuyu-beifa", 0.7, "leads_to", desc="孙恩卢循之乱中刘裕声望鹊起")],
        review_note="孙恩卢循起义（399—411）为过程；刘裕平乱积功，为其后篡晋建立基础。"),
    _ev("event-liuyu-beifa", "刘裕北伐（灭南燕、后秦）", "war",
        409, 417, "range", "period-eastern-jin", "major",
        "义熙五年至十三年（409—417年）刘裕先后北伐："
        "409—410年灭南燕，416—417年灭后秦、克长安。"
        "刘裕北伐是东晋建国以来规模最大、战果最著的北伐，"
        "使其军政威望达到顶点，为代晋建宋奠定基础。",
        f"古代史料：《宋书·武帝纪》《晋书·安帝纪》；现代参考：{MODERN['wj']}",
        W["jinshu_zizhi"],
        ["regime-eastern-jin"],
        [_rel("event-sunen-luxun", "follows", desc="刘裕平孙恩卢循后主持北伐"),
         _rel("event-liuyu-dai-jin", 0.9, "leads_to", desc="两次北伐成功直接铺垫刘裕代晋")],
        review_note="刘裕北伐（409—417）为过程事件；417年灭后秦后其留守长安之部旋败，但代晋大势已定。"),
]

# ---------------------------------------------------------------------------
# Phase 5 — 南北朝（420–577）
# ---------------------------------------------------------------------------
PHASE_NORTHERN_SOUTHERN = [
    _ev("event-liuyu-dai-jin", "刘裕代晋、刘宋建立", "dynastic-transition",
        420, 420, "year", "period-northern-southern", "major",
        "元熙二年（420年）刘裕接受晋恭帝禅让称帝，国号宋（刘宋），都建康。"
        "刘裕代晋结束了东晋百余年门阀政治，南朝自此开始，"
        "中国历史进入南北朝时代（与北方的北魏并峙）。",
        f"古代史料：《宋书·武帝纪》；现代参考：{MODERN['wj']}",
        W["jinshu_zizhi"],
        ["regime-liu-song"],
        [_rel("event-liuyu-beifa", "follows", desc="北伐功成后刘裕代晋建宋"),
         _rel("event-beiwei-tongyi-beifang", "precedes", desc="宋与北魏南北并峙")],
        review_note="刘裕420年受禅称帝（永初元年）；\"刘宋\"为史称以别于赵宋。"),
    _ev("event-yuanjia-zhizhi", "元嘉之治", "political",
        424, 453, "range", "period-northern-southern", "major",
        "宋文帝在位（424—453年）期间，免除苛税、劝课农桑、整顿吏治，"
        "政治相对安定，史称\"元嘉之治\"（属后世概括）。"
        "元嘉中后期因北伐失利与内部动乱而转衰。",
        f"古代史料：《宋书·文帝纪》；现代参考：{MODERN['wj']}",
        W["jinshu_zizhi"],
        ["regime-liu-song"],
        [_rel("event-liuyu-dai-jin", "follows"),
         _rel("event-yuanjia-beifa", 0.7, "precedes", desc="元嘉之治后期转入北伐与衰败")],
        review_note="元嘉之治（424—453）为治世概括（同\"文景之治\"处理），不作单一精确事件。"),
    _ev("event-yuanjia-beifa", "元嘉北伐", "war",
        430, 452, "range", "period-northern-southern", "major",
        "元嘉七年至二十九年（430—452年）宋文帝两度大规模北伐北魏，"
        "均遭惨败：450年拓跋焘南侵至瓜步，刘宋江北残破。"
        "元嘉北伐失败宣告\"元嘉之治\"的军事幻想破灭，南朝防势自此转入守势。",
        f"古代史料：《宋书·文帝纪》《索虏传》；现代参考：{MODERN['wj']}",
        W["jinshu_zizhi"],
        ["regime-liu-song", "regime-northern-wei"],
        [_rel("event-yuanjia-zhizhi", "follows"),
         _rel("event-xiaodaocheng-dai-song", 0.5, "precedes", desc="北伐失利后刘宋内乱频繁，终为萧道成所代")],
        review_note="元嘉北伐（430、450两次）为过程事件；450年之役为南北战争最烈者之一，\"元嘉草草\"为后世咏叹。"),
    _ev("event-zhongli-zhizhan", "钟离之战", "war",
        507, 507, "year", "period-northern-southern", "major",
        "天监六年（507年）北魏以数十万大军围梁钟离（今安徽凤阳东北），"
        "梁将韦睿、曹景宗督北府诸军大破之，魏军死伤惨重。"
        "钟离之战是梁魏战争中的决定性胜利，巩固了梁在淮南的统治。",
        f"古代史料：《梁书·韦睿传》《北魏·世宗纪》；现代参考：{MODERN['wj']}",
        W["liangchen"],
        ["regime-liang", "regime-northern-wei"],
        [_rel("event-xiaoyan-dai-qi", "follows", desc="梁立国后与北魏的决战")],
        review_note="钟离之战在507年（天监六年）；\"钟离之役\"为梁魏间最著名战役之一。"),
    _ev("event-xiaodaocheng-dai-song", "萧道成代宋、南齐建立", "dynastic-transition",
        479, 479, "year", "period-northern-southern", "major",
        "昇明三年（479年）萧道成受宋顺帝禅让称帝，国号齐（南齐），都建康。"
        "南齐建立继刘宋之后，延续南朝政权更替的模式。",
        f"古代史料：《南齐书·高帝纪》；现代参考：{MODERN['wj']}",
        W["liangchen"],
        ["regime-southern-qi"],
        [_rel("event-yuanjia-beifa", "follows", desc="刘宋末世内乱后权臣萧道成代宋"),
         _rel("event-xiaoyan-dai-qi", 0.7, "leads_to", desc="南齐宗室内乱为萧衍代齐创造条件")],
        review_note="萧道成479年即位（建元元年）；南齐传七主，历约二十三年。"),
    _ev("event-xiaoyan-dai-qi", "萧衍代齐、梁建立", "dynastic-transition",
        502, 502, "year", "period-northern-southern", "major",
        "天监元年（502年）萧衍受齐和帝禅让称帝，国号梁，都建康。"
        "萧衍在位近五十年（502—549年），前期政治较清明、文化鼎盛，"
        "后期佞佛失政，为侯景之乱留下隐患。",
        f"古代史料：《梁书·武帝纪》；现代参考：{MODERN['wj']}",
        W["liangchen"],
        ["regime-liang"],
        [_rel("event-xiaodaocheng-dai-song", "follows"),
         _rel("event-houjing-zhi-luan", 0.8, "leads_to", desc="萧衍晚年接纳侯景，招致侯景之乱")],
        review_note="萧衍502年即位（天监元年）；梁朝后半期\"侯景之乱\"（548—552）几乎摧毁其政权。"),
    _ev("event-houjing-zhi-luan", "侯景之乱", "war",
        548, 552, "range", "period-northern-southern", "critical",
        "太清二年至承圣元年（548—552年），北魏降将侯景反梁，"
        "围建康、破台城，梁武帝饿死（549年），江南文物尽焚、人口锐减。"
        "侯景之乱是南朝由盛转衰的总爆发：梁朝统治瓦解、南朝再也无力抗衡北朝，"
        "并催生陈朝与北周、北齐南北格局的新一轮洗牌。",
        f"古代史料：《梁书·武帝纪》《侯景传》；现代参考：{MODERN['wj']}",
        W["liangchen"],
        ["regime-liang"],
        [_rel("event-xiaoyan-dai-qi", "follows", desc="萧衍晚年失政、纳降侯景"),
         _rel("event-houjing-po-taicheng", "part_of", 0.95, desc="台城陷落梁武帝去世为侯景之乱核心阶段"),
         _rel("event-xiwei-po-jiangling", "part_of", 0.7, desc="侯景之乱后西魏破江陵梁亡为余波")],
        review_note="侯景之乱（548—552）为 process+aggregate；梁武帝饿死台城、建康湮灭、江陵之乱均为其组成部分。南朝衰势自此不可逆。"),
    _ev("event-houjing-po-taicheng", "侯景破台城、梁武帝去世", "war",
        549, 549, "year", "period-northern-southern", "major",
        "太清三年（549年）侯景攻破建康台城，梁武帝萧衍饿死宫阙，"
        "侯景控制建康及三吴。建康作为南朝政治文化中心遭受空前浩劫，"
        "\"石头城下水横流，台城上草萋萋\"成为乱世写照。",
        f"古代史料：《梁书·武帝纪》《侯景传》；现代参考：{MODERN['wj']}",
        W["liangchen"],
        ["regime-liang"],
        [_rel("event-houjing-zhi-luan", "part_of", 0.95, desc="台城陷落为侯景之乱决定性阶段")],
        review_note="台城破于549年三月，梁武帝饿死于五月；建康宫阙被焚。"),
    _ev("event-xiwei-po-jiangling", "西魏破江陵、梁灭亡", "war",
        554, 554, "year", "period-northern-southern", "major",
        "承圣三年（554年）西魏于谨、杨忠攻破江陵，杀梁元帝萧绎，"
        "梁政权至此实质灭亡（萧詧在江陵立西梁为附庸）。"
        "侯景之乱后梁宗室相攻，江陵陷落使南朝最后抵抗力量丧失，"
        "南方转入陈朝重建阶段。",
        f"古代史料：《梁书·元帝纪》《周书·文帝纪》；现代参考：{MODERN['wj']}",
        W["liangchen"],
        ["regime-liang", "regime-western-wei"],
        [_rel("event-houjing-zhi-luan", "follows", desc="侯景之乱后梁室相攻、江陵被破"),
         _rel("event-chenbaxian-jianzhen", 0.6, "leads_to", desc="梁亡后陈霸先在建康建陈")],
        review_note="江陵破于554年十一月（承圣三年）；\"江陵焚书\"与萧绎焚毁藏书为文化史上重大损失之记载。"),
    _ev("event-chenbaxian-jianzhen", "陈霸先建立陈朝", "dynastic-transition",
        557, 557, "year", "period-northern-southern", "major",
        "太平二年（557年）陈霸先受梁敬帝禅让称帝，国号陈，都建康。"
        "陈朝为南朝最后一个政权，地域已缩小到长江下游一带，"
        "后期无力与北朝争衡，直至589年为隋所灭。",
        f"古代史料：《陈书·高祖纪》；现代参考：{MODERN['wj']}",
        W["liangchen"],
        ["regime-chen"],
        [_rel("event-xiwei-po-jiangling", "follows", desc="梁亡后陈霸先建陈"),
         _rel("event-sui-mie-chen", 0.6, "precedes", desc="陈朝后期为隋所并（589）")],
        review_note="陈霸先557年即位（永定元年）；陈后主陈叔宝（569—589年在位）之世陈朝由盛转衰。"),
    _ev("event-xiaowendi-gaige", "北魏孝文帝改革", "reform",
        471, 499, "range", "period-northern-southern", "major",
        "北魏献文帝、孝文帝时期（471—499年），冯太后临朝与孝文帝亲政相继推进汉化改革："
        "行均田制、三长制、俸禄制，493年迁都洛阳，"
        "其后改革官制、禁胡服、断北语、改汉姓、定门第。"
        "本事件为 aggregate，具体节点（迁都/汉化）见 part_of 子事件。",
        f"古代史料：《魏书·高祖纪》《冯太后传》；现代参考：{MODERN['wj']}",
        W["weishu"],
        ["regime-northern-wei"],
        [_rel("event-beiwei-tongyi-beifang", "follows", desc="统一北方后转向中原化改革"),
         _rel("event-luzhen-qiyi", 0.5, "leads_to", desc="汉化改革加强洛阳权贵而削弱六镇军镇，为六镇起义埋因")],
        review_note="孝文帝改革（471—499）跨度大（冯太后与孝文帝两阶段），均田、三长、迁都、汉化各为组成部分；\"彻底汉化\"之争为现代史学议题（见 WEI_JIN_NORTHERN_SOUTHERN_BACKBONE_REVIEW.md）。"),
    _ev("event-qian-du-luoyang", "孝文帝迁都洛阳", "migration",
        493, 493, "year", "period-northern-southern", "major",
        "太和十七年（493年）孝文帝以南伐为名率众迁都洛阳，"
        "鲜卑贵族随之定居中原。迁都洛阳是孝文帝汉化改革的关键一步，"
        "使北魏政治中心自平城转向洛阳，加速鲜卑社会的中原化进程。",
        f"古代史料：《魏书·高祖纪》；现代参考：{MODERN['wj']}",
        W["weishu"],
        ["regime-northern-wei"],
        [_rel("event-xiaowendi-gaige", "part_of", 0.95, desc="迁都洛阳为孝文帝改革重要环节")],
        review_note="迁都洛阳在493年（太和十七年）；\"以南伐为名\"之掩饰反映了旧贵族的阻力。"),
    _ev("event-taihe-hanhua", "孝文帝汉化改革（改官制、禁胡服胡语、改汉姓）", "reform",
        494, 499, "range", "period-northern-southern", "major",
        "迁洛后孝文帝推行全面汉化：494年起改革官制、禁胡服、断北语，"
        "496年改拓跋氏为元氏并定鲜卑勋贵汉姓、按门第仕进。"
        "汉化改革促进民族融合，也使六镇军人地位与待遇相对下降，"
        "为日后六镇起义与北魏分裂埋下深层矛盾。",
        f"古代史料：《魏书·高祖纪》；现代参考：{MODERN['wj']}",
        W["weishu"],
        ["regime-northern-wei"],
        [_rel("event-qian-du-luoyang", "follows", desc="迁洛后全面汉化"),
         _rel("event-xiaowendi-gaige", "part_of", 0.95, desc="汉化改革为孝文帝改革核心环节")],
        review_note="汉化改革（494—499）为过程；\"禁断北语\"\"改汉姓\"等令具体见于《魏书》，与六镇矛盾之关联为现代史学强调。"),
    _ev("event-luzhen-qiyi", "六镇起义", "rebellion",
        523, 525, "range", "period-northern-southern", "major",
        "正光四年（523年）沃野镇镇兵破六韩拔陵领导起义，"
        "六镇（北魏北边防戍军镇）相继响应，北魏朝廷镇压不力，"
        "被迫诏准胡汉通婚、募镇民为兵。六镇起义动摇了北魏统治根基，"
        "并孕育了北魏末年的军阀化。",
        f"古代史料：《魏书·肃宗纪》《尔朱荣传》；现代参考：{MODERN['wj']}",
        W["weishu"],
        ["regime-northern-wei"],
        [_rel("event-taihe-hanhua", "follows", desc="汉化改革与镇将矛盾积累引发六镇之乱"),
         _rel("event-heyin-zhi-bian", 0.7, "leads_to", desc="六镇乱后尔朱荣势力北上，制造河阴之变")],
        review_note="六镇起义（523—525，至528年前后诸镇相继）为过程；起义军之东、西分化为后来高欢、宇文泰两系师承。"),
    _ev("event-heyin-zhi-bian", "河阴之变", "political",
        528, 528, "year", "period-northern-southern", "major",
        "武泰元年（528年）尔朱荣在河阴（今河南孟津东北）发动政变，"
        "沉杀胡太后及幼主，并屠杀朝臣两千余人（\"河阴之变\"）。"
        "此变使北魏洛阳朝廷元气大伤，军政大权为尔朱氏掌握，"
        "直接促成北魏末年的政体重构与分裂。",
        f"古代史料：《魏书·孝明纪》《尔朱荣传》；现代参考：{MODERN['wj']}",
        W["weishu"],
        ["regime-northern-wei"],
        [_rel("event-luzhen-qiyi", "follows"),
         _rel("event-gaohuan-qibing", 0.8, "leads_to", desc="尔朱氏霸政下高欢起兵讨尔朱、东魏得立")],
        review_note="河阴之变在528年四月（武泰元年）；\"二千余人\"为史载数目，具体或有出入。"),
    _ev("event-gaohuan-qibing", "高欢起兵讨尔朱氏", "war",
        531, 534, "range", "period-northern-southern", "major",
        "531年高欢以东魏（河北）为基地起兵讨伐尔朱氏，"
        "532年攻入洛阳立孝武帝（北魏末帝）；534年孝武帝西奔长安投宇文泰，"
        "高欢另立孝静帝、迁都邺，北魏就此分裂为东西。"
        "高欢势力为后来东魏—北齐的政治军事基础。",
        f"古代史料：《魏书·孝静纪》《周书·文帝纪》；现代参考：{MODERN['wj']}",
        W["weishu_zizhi"],
        ["regime-northern-wei"],
        [_rel("event-heyin-zhi-bian", "follows"),
         _rel("event-beiwei-fenlie", 0.9, "leads_to", desc="高欢与宇文泰分庭抗礼导致北魏分裂")],
        review_note="高欢起兵（531—534）为过程；孝武西奔与东魏建都邺在534年。"),
    _ev("event-beiwei-fenlie", "北魏分裂为东魏西魏", "political",
        534, 535, "range", "period-northern-southern", "critical",
        "永熙三年（534年）北魏孝武帝西奔长安（宇文泰），高欢立元善见"
        "为帝（东魏）、都邺；535年宇文泰立元宝炬为帝（西魏）、都长安。"
        "北魏正式分裂为东魏与西魏两个并行政权，中国北方由此形成两强对峙，"
        "并分别过渡到北齐与北周。",
        f"古代史料：《魏书·孝静纪》《周书·文帝纪》；现代参考：{MODERN['wj']}",
        W["weishu_zizhi"],
        ["regime-northern-wei"],
        [_rel("event-gaohuan-qibing", "follows", desc="高欢、宇文泰分割北魏"),
         _rel("event-gaoyang-dai-dongwei", 0.7, "leads_to", desc="东魏过渡到北齐"),
         _rel("event-yuwenjue-dai-xiwei", 0.7, "leads_to", desc="西魏过渡到北周")],
        review_note="北魏分裂（534—535）为结构事件：东魏（534—550，都邺）、西魏（535—557，都长安）并行；\"parallel regime\" 由 Regime 数据（parent_regime_id）与事件 regime_ids 共同表达（§27/§36）。"),
    _ev("event-yubi-zhizhan", "玉壁之战", "war",
        546, 546, "year", "period-northern-southern", "major",
        "武定四年（546年）东魏高欢率大军围攻西魏玉壁（今山西稷山西南），"
        "北周名将韦孝宽固守五十余日，高欢败归，次年病死。"
        "玉壁之战是东西魏最具决定性的攻防战，阻遏了东魏吞并西魏的企图。",
        f"古代史料：《周书·韦孝宽传》《北齐书·神武纪》；现代参考：{MODERN['wj']}",
        W["nanbeishi"],
        ["regime-eastern-wei", "regime-western-wei"],
        [_rel("event-beiwei-fenlie", "follows", desc="东西魏对峙中的关键战役"),
         _rel("event-fubing-zhi", 0.6, "precedes", desc="西魏守城取胜强化府兵制构建")],
        review_note="玉壁之战在546年（东西魏第三次大战）；韦孝宽守城战为古代攻城战典型战例。"),
    _ev("event-fubing-zhi", "西魏府兵制创建", "reform",
        543, 550, "range", "period-northern-southern", "major",
        "西魏大统年间（约543—550年）宇文泰仿周礼建置六军，"
        "以柱国、大将军分统府兵，创立\"府兵制\"（六柱国十二大将军），"
        "兵农合一的府兵体系成为其后北周、隋唐军制的源头。",
        f"古代史料：《周书·文帝纪》；现代参考：{MODERN['wj']}；陈寅恪《隋唐制度渊源略论稿》",
        W["suishu"],
        ["regime-western-wei"],
        [_rel("event-yuwenjue-dai-xiwei", 0.7, "leads_to", desc="府兵制建设为北周取代西魏提供军力")],
        review_note="府兵制创立具体年代（约543—550）诸书略有出入，取 range；\"六柱国\"制为北周武功基础（§28：以制度形成节点立项，不作制度概念泛化）。"),
    _ev("event-gaoyang-dai-dongwei", "高洋代东魏、北齐建立", "dynastic-transition",
        550, 550, "year", "period-northern-southern", "major",
        "天保元年（550年）高欢之子高洋废东魏孝静帝自立，国号齐（北齐），都邺。"
        "北齐建立东西对峙中的东系政权，其季年昏乱，577年为北周所灭。",
        f"古代史料：《北齐书·文宣帝纪》；现代参考：{MODERN['wj']}",
        W["nanbeishi"],
        ["regime-northern-qi"],
        [_rel("event-beiwei-fenlie", "follows", desc="东魏禅让为北齐"),
         _rel("event-beizhou-mie-beiqi", 0.6, "leads_to", desc="北齐最终亡于北周（577）")],
        review_note="高洋550年受禅（天保元年）；北齐\"禽兽王朝\"之评价属后世史论，本库以史实记录为主。"),
    _ev("event-yuwenjue-dai-xiwei", "宇文觉代西魏、北周建立", "dynastic-transition",
        557, 557, "year", "period-northern-southern", "major",
        "恭帝三年十二月（557年）宇文泰之子宇文觉废西魏恭帝自立，国号周（北周），都长安。"
        "北周建立后由宇文护专权，历经武成、保定、天和年间，至周武帝亲政才走向强盛。",
        f"古代史料：《周书·闵帝纪》；现代参考：{MODERN['wj']}",
        W["nanbeishi"],
        ["regime-northern-zhou"],
        [_rel("event-beiwei-fenlie", "follows", desc="西魏禅让为北周"),
         _rel("event-zhouwudi-qinzheng", 0.7, "leads_to", desc="北周经宇文护专权至周武帝亲政改革")],
        review_note="宇文觉557年即位（周闵帝元年）；宇文护专权至572年被周武帝诛杀。"),
    _ev("event-zhouwudi-qinzheng", "周武帝亲政与改革", "reform",
        572, 578, "range", "period-northern-southern", "major",
        "建德元年（572年）周武帝宇文邕诛杀权臣宇文护，正式亲政，"
        "实行改革：整顿府兵、褒奖农桑、灭佛（574年）以充实国力，"
        "并积极备战东伐。周武帝改革使北周国力反超北齐，为统一北方奠定基础。",
        f"古代史料：《周书·武帝纪》；现代参考：{MODERN['wj']}",
        W["nanbeishi"],
        ["regime-northern-zhou"],
        [_rel("event-yuwenjue-dai-xiwei", "follows", desc="北周自宇文护专权走向周武帝亲政"),
         _rel("event-beizhou-mie-beiqi", 0.9, "leads_to", desc="周武帝改革后出兵灭北齐")],
        review_note="周武帝亲政（572）、灭佛（574）、灭齐（575—577）为过程；\"求高僧灭佛誉\"与灭佛动机之讨论见现代史学。"),
    _ev("event-beizhou-mie-beiqi", "北周灭北齐", "war",
        576, 577, "range", "period-northern-southern", "critical",
        "建德五年至六年（576—577年）周武帝亲率大军伐齐，"
        "破晋阳、克邺，北齐后主被俘，北齐灭亡，北周统一北方。"
        "北周灭北齐结束北方东西对峙，北方重归一统，为隋朝取代北周并统一全国铺平道路。",
        f"古代史料：《周书·武帝纪》《北齐书·后主纪》；现代参考：{MODERN['wj']}",
        W["nanbeishi"],
        ["regime-northern-zhou", "regime-northern-qi"],
        [_rel("event-zhouwudi-qinzheng", "follows", desc="周武帝改革后大举灭齐"),
         _rel("event-yangjian-dai-beizhou", 0.7, "leads_to", desc="统一北方的北周旋即被杨坚代周（隋）")],
        review_note="北周灭北齐（576—577）之\"北周统一北方\"为同一节点之两个面向；周灭齐后更定户籍、推行府兵，北方制度整合完成。"),
]

# ---------------------------------------------------------------------------
# Phase 6 — 隋统一（580–589）
# ---------------------------------------------------------------------------
PHASE_SUI_UNIFICATION = [
    _ev("event-yangjian-zhuanquan", "杨坚辅政掌权", "political",
        580, 581, "range", "period-northern-southern", "major",
        "大象二年（580年）北周宣帝去世，幼主静帝即位，"
        "外戚杨坚以大丞相、假黄钺总揽军政，清除尉迟迥、王谦等反对势力，"
        "实际控制北周政权。杨坚掌权为代周建隋扫清障碍。",
        f"古代史料：《周书·宣帝纪》《隋书·高祖纪》；现代参考：{MODERN['suibound']}",
        W["suishu"],
        ["regime-northern-zhou"],
        [_rel("event-beizhou-mie-beiqi", "follows", desc="北周统一北方后杨坚以外戚掌权"),
         _rel("event-yangjian-dai-beizhou", 0.95, "leads_to", desc="掌权一年后杨坚代周建隋")],
        review_note="杨坚辅政在580年（大象二年）；\"年幼静帝\"与\"外戚辅政\"模式为南北朝禅代之延续。"),
    _ev("event-yangjian-dai-beizhou", "杨坚代北周、隋朝建立", "dynastic-transition",
        581, 581, "year", "period-sui", "critical",
        "开皇元年（581年）杨坚废周静帝自立，国号隋，都大兴（长安）。"
        "隋朝建立标志北朝政权更替完成，南北统一已进入最后阶段。"
        "杨坚代周与隋建立为同一节点（§48 粒度判断）。",
        f"古代史料：《隋书·高祖纪》《周书·静帝纪》；现代参考：{MODERN['suibound']}",
        W["suishu"],
        ["regime-sui"],
        [_rel("event-yangjian-zhuanquan", "follows"),
         _rel("event-sui-mie-xiliang", 0.7, "leads_to", desc="隋建立后先平西梁再图江南")],
        review_note="杨坚581年受禅（开皇元年）；隋朝承北周而统一南北，为中华再统之关键节点。"),
    _ev("event-sui-mie-xiliang", "隋灭西梁", "war",
        587, 587, "year", "period-sui", "major",
        "开皇七年（587年）隋文帝命萧岿之孙萧琮入朝，随即废西梁（江陵小朝廷），"
        "北周以来依附于隋的傀儡政权被吞并。隋前期遂完成对长江中游的肃清，"
        "为南征陈朝扫清侧翼。",
        f"古代史料：《隋书·高祖纪》；现代参考：{MODERN['suibound']}",
        W["suishu"],
        ["regime-sui"],
        [_rel("event-yangjian-dai-beizhou", "follows", desc="隋代周后收西梁"),
         _rel("event-sui-mie-chen", 0.95, "leads_to", desc="灭西梁为灭陈铺平道路")],
        review_note="西梁（555—587）为北周/隋所立傀儡政权；587年废国。"),
    _ev("event-sui-mie-chen", "隋灭陈、隋统一", "war",
        589, 589, "year", "period-sui", "critical",
        "开皇九年（589年）隋文帝发五十一万大军南下，韩擒虎、贺若弼渡江克建康，"
        "陈后主被俘，陈朝灭亡。隋灭陈结束自西晋以来近三百年（280—589）的分裂局面，"
        "中国重新实现大一统。",
        f"古代史料：《隋书·高祖纪》《陈书·后主纪》；现代参考：{MODERN['suibound']}",
        W["suishu"],
        ["regime-sui"],
        [_rel("event-sui-mie-xiliang", "follows", desc="灭陈前已完成对江南侧翼之肃清"),
         _rel("event-chenbaxian-jianzhen", "precedes", desc="陈朝自557年建立，589年亡")],
        review_note="隋灭陈在589年正月（开皇九年）；\"韩擒虎夜入朱雀门\"\"后庭花\"为后世传述。本事件兼\"隋灭陈\"与\"隋统一\"两个面向，一次建档（§48）。"),
]

ALL_PHASES = [
    ("three_kingdoms", "Phase 1 东汉末", PHASE_LATE_HAN),
    ("three_kingdoms", "Phase 2 三国", PHASE_THREE_KINGDOMS),
    ("jin_southern_northern", "Phase 3 西晋", PHASE_WESTERN_JIN),
    ("jin_southern_northern", "Phase 4 东晋/十六国", PHASE_EASTERN_JIN_16K),
    ("jin_southern_northern", "Phase 5 南北朝", PHASE_NORTHERN_SOUTHERN),
    ("jin_southern_northern", "Phase 6 隋统一", PHASE_SUI_UNIFICATION),
]

PHASES = {
    "LATE_HAN": PHASE_LATE_HAN,
    "THREE_KINGDOMS": PHASE_THREE_KINGDOMS,
    "WESTERN_JIN": PHASE_WESTERN_JIN,
    "EASTERN_JIN_16K": PHASE_EASTERN_JIN_16K,
    "NORTHERN_SOUTHERN": PHASE_NORTHERN_SOUTHERN,
    "SUI_UNIFICATION": PHASE_SUI_UNIFICATION,
}


def all_events():
    return [(dir_, label, ev) for dir_, label, events in ALL_PHASES for ev in events]