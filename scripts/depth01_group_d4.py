"""Depth Sprint 01 · D4（唐宋明 6 事件）——后梁代唐/陈桥兵变/靖康之变/崖山海战/土木堡之变/萨尔浒之战。"""
from __future__ import annotations
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _depth_util import apply, ev  # noqa: E402

TAG = "depth01-D4"

PATCH = {
 "five_dynasties/event-houliang-dai-tang.yml": {
  "background_zh_cn": "黄巢乱后，朱全忠以宣武节度使起于汴：既平秦宗权，而「朱全忠连兵十万，吞噬河南，兖、郓、青、徐之间，血战不解」——唐祚之危已系于汴帅。"
                      "全忠进位守中书令、进封东平王，又上表请以关东藩镇除用朝廷名德为节度观察使，朝政之权浸移于外。",
  "process_zh_cn": "天祐四年正月，梁王休兵于贝州，以潞州内叛、威望大沮，「恐中外因此离心，欲速受禅以镇之」；宰相薛贻矩还言于帝曰「元帅有受禅之意矣」。"
                   "唐大臣共奏请昭宣帝逊位，帝乃下诏以二月禅位于梁，又诏礼部尚书苏循赍百官诣大梁。",
  "result_zh_cn": "甲辰，唐昭宣帝降御札禅位于梁；庚戌，梁王始御金祥殿，受百官称臣，下书称教令，自称曰寡人；壬戌，梁王更名晃——"
                  "唐祚三百年前后而终，后梁受禅而立，中国进入五代之世。",
  "impact_zh_cn": "唐之亡使中原五朝迭兴、十国割据，直至宋初方复一统；朱全忠以藩镇之兵移唐祚，旧唐书史臣论曰「朱全忠连兵十万，吞噬河南……唐祚以至于亡」，"
                  "为兵权下移则国祚随之之实例，五代武人政治之弊亦自此始。",
  "evidence": [
   ev("旧唐书", "哀帝纪", "本纪/卷二十#p45", "text-niutrans-715c152a2c2a0db0c010", "background", "primary",
      "宗权既平，而硃全忠连兵十万，吞噬河南，兗、郓、青、徐之间，血战不解，唐祚以至于亡。", TAG),
   ev("旧唐书", "哀帝纪", "本纪/卷二十#p48", "text-niutrans-bf4a50f24feb72d86f0f", "background", "supporting",
      "四月壬戌朔，以宣武淮南等节度副大使……硃全忠为检校太尉、中书令，进封东平王，仍赐赏军钱十万贯。", TAG),
   ev("资治通鉴", "后梁纪一", "后梁纪/后梁纪一#p27", "text-niutrans-328644bb1f979b0cd818", "process", "primary",
      "恐中外因此离心，欲速受禅以镇之。", TAG),
   ev("资治通鉴", "后梁纪一", "后梁纪/后梁纪一#p35", "text-niutrans-c75e7ea41e029e21dbc5", "process", "supporting",
      "帝乃下诏，以二月禅位于梁，又遣宰相以书谕王；王辞。", TAG),
   ev("资治通鉴", "后梁纪一", "后梁纪/后梁纪一#p44", "text-niutrans-3a64d3cfcbd8e96ae248", "result", "primary",
      "甲辰，唐昭宣帝降御札禅位于梁。", TAG),
   ev("资治通鉴", "后梁纪一", "后梁纪/后梁纪一#p68", "text-niutrans-1a388d5c1628bca6be81", "result", "supporting",
      "庚戌，梁王始御金祥殿，受百官称臣，下书称教令，自称曰寡人。", TAG),
   ev("资治通鉴", "后梁纪一", "后梁纪/后梁纪一#p76", "text-niutrans-99c6c2319135edc7deb8", "result", "supporting",
      "壬戌，梁王更名晃。", TAG),
   ev("旧唐书", "哀帝纪", "本纪/卷二十#p82", "text-niutrans-07869a47436206f209bb", "background", "supporting",
      "三月丁亥朔，硃全忠上表：关东籓镇，请除用朝廷名德为节度观察使。", TAG),
  ],
  "relations": [
   {"target_event_id": "event-huangchao-qiyi", "relation_type": "follows",
    "description_zh_cn": "黄巢之乱后藩镇坐大，朱全忠遂移唐祚"},
  ],
 },
 "song_liao_xia_jin/event-chenqiao-bingbian.yml": {
  "background_zh_cn": "后周世宗崩，恭帝幼冲，禁军诸校为朝局轻重：世宗尝召禁军诸校宴射苑中，赏赍有加，禁军之柄已为改朝换代之枢。"
                      "太祖赵匡胤以北征为名率师出京师——「及太祖北征，为六师推戴，自陈桥还府署」，兵变之机已伏。",
  "process_zh_cn": "大军次陈桥驿，「军中知星者苗训引门吏楚昭辅视日下复有一日，黑光摩荡者久之」——天象之说以动众心；"
                   "诸校露刃列于庭曰「诸军无主，愿策太尉为天子」，将士拥立，太祖乃还师入京。",
  "result_zh_cn": "太祖即位，尊符太后为皇太后：「及太祖自陈桥还京师，人走报太后曰：点检已作天子。太后曰：吾儿素有大志，今果然」；"
                  "后周恭帝逊位，宋受禅而立，改元建隆，五代之局自此收束。",
  "impact_zh_cn": "陈桥兵变以兵不血刃而成禅代，宋室惩五代武人拥立之弊，遂收兵权、重文治，强干弱枝之策行于一代；"
                  "宋代文官政治与「与士大夫共治」之局皆肇于此，而其重文抑武之偏亦伏后来边患之因。",
  "evidence": [
   ev("宋史", "列传", "列传/卷八#p31", "text-niutrans-9757352faa000078d4b1", "background", "primary",
      "及太祖北征，为六师推戴，自陈桥还府署。", TAG),
   ev("宋史", "太祖纪", "本纪/卷一#p58", "text-niutrans-d77239ac01d51edaffc5", "process", "primary",
      "次陈桥驿，军中知星者苗训引门吏楚昭辅视日下复有一日，黑光摩荡者久之。", TAG),
   ev("宋史", "太祖纪", "本纪/卷一#p61", "text-niutrans-d9073d6ee9be627e6b3f", "process", "primary",
      "诸校露刃列于庭，曰：诸军无主，愿策太尉为天子。", TAG),
   ev("宋史", "后妃传", "列传/卷一#p8", "text-niutrans-af4359b47829b0798d2b", "result", "primary",
      "及太祖自陈桥还京师，人走报太后曰：点检已作天子。太后曰：吾儿素有大志，今果然。太祖即位，尊为皇太后。", TAG),
   ev("宋史", "列传", "列传/卷九#p27", "text-niutrans-c8512bdf82586f326f99", "background", "supporting",
      "世宗召禁军诸校宴射苑中，审琦连中的，世宗嘉之，赏赍有加。", TAG),
  ],
  "relations": [
   {"target_event_id": "event-houliang-dai-tang", "relation_type": "follows",
    "description_zh_cn": "五代武人拥立之局，至陈桥而终，宋室代周"},
  ],
 },
 "song_liao_xia_jin/event-jingkang-zhi-bian.yml": {
  "background_zh_cn": "宋廷和战不决：金人两至都城，「中国之御四裔，能守而后可战，能战而后可和，而靖康之末皆失之」；"
                      "靖康元年，金人入青城、攻朝阳门，京城危急，钦宗下诏亲征，而大臣议论纷然，战守之策莫衷一是。",
  "process_zh_cn": "靖康元年闰十一月，「秦元领保甲斩关遁，京城陷」；金人邀上皇出郊，戊午钦宗如青城，帝在青城。"
                   "二年二月丁卯，金人要上皇如青城；辛未，金人逼上皇召皇后、皇太子入青城——二帝及后妃皇族尽为金人所执。",
  "result_zh_cn": "二帝北狩、皇族播迁：宋臣追论之曰「昨者城下之战，诡诈百出，二帝北狩，皇族播迁，宗社之危，已绝而续」；"
                  "北宋百七十年而亡，康王构即位于南京，是为南宋，中兴之局始于危亡之际。",
  "impact_zh_cn": "靖康之变为中国历史之巨创：「国家二百年太平之基……二圣北狩之痛，汉、唐之所未有也」，中原沦于金，宋室南渡，"
                  "南北对峙历百五十年；士人复仇之论与理学之兴起皆与此痛相关，南宋一朝之政治与文教皆以此为底色。",
  "evidence": [
   ev("宋史", "列传", "列传/卷一百一十七#p176", "text-niutrans-072844fac74246283a35", "background", "primary",
      "谓中国之御四裔，能守而后可战，能战而后和，而靖康之末皆失之。", TAG),
   ev("宋史", "钦宗纪", "本纪/卷二十三#p346", "text-niutrans-9fbb8a153d1a1213db36", "process", "supporting",
      "乙未，金人入青城，攻朝阳门。", TAG),
   ev("宋史", "钦宗纪", "本纪/卷二十三#p379", "text-niutrans-38eb9032b6d3b0f3c2be", "process", "primary",
      "秦元领保甲斩关遁，京城陷。", TAG),
   ev("宋史", "钦宗纪", "本纪/卷二十三#p388", "text-niutrans-e1ba20d1c11c20c4a36a", "process", "primary",
      "辛酉，帝如青城。", TAG),
   ev("宋史", "钦宗纪", "本纪/卷二十三#p422", "text-niutrans-3a9a3bf347011d21a3b9", "result", "primary",
      "辛未，金人逼上皇召皇后、皇太子入青城。", TAG),
   ev("宋史", "列传", "列传/卷一百八十七#p41", "text-niutrans-e705940f4ef7339233a9", "result", "supporting",
      "昨者城下之战，诡诈百出，二帝北狩，皇族播迁，宗社之危，已绝而续。", TAG),
   ev("宋史", "列传", "列传/卷一百九十五#p14", "text-niutrans-b9e3fa2d7cd4085b997e", "impact", "primary",
      "国家二百年太平之基，三代之所无也；二圣北狩之痛，汉、唐之所未有也。", TAG),
   ev("宋史", "列传", "列传/卷一百九十五#p128", "text-niutrans-0d676959fc7abb16d02f", "impact", "supporting",
      "其一曰：二圣北狩之痛，盖国家之大耻，而天下之公愤也。", TAG),
  ],
  "relations": [
   {"target_event_id": "event-jianyan-nandu", "relation_type": "leads_to",
    "description_zh_cn": "二帝北狩后康王南渡，南宋立于江左"},
  ],
 },
 "song_liao_xia_jin/event-yanya-haizhan.yml": {
  "background_zh_cn": "宋主纳土降元之后，宋臣拥二王南走：至元十五年四月，「昺徙居崖山，升广州为翔龙府」；"
                      "世杰以碙洲不可居，徙王新会之崖山，结大舶千余艘作水寨据险以守——张弘范、李恒奉命征崖山。",
  "process_zh_cn": "十六年正月壬戌，张弘范兵至崖山；或谓世杰曰「北兵以舟师塞海口，则我不能进退，盍先据海口」，世杰不听。"
                   "二月癸未，弘范等攻崖山，世杰败，走卫王舟；弘范得世杰之甥韩，命以官，使三至招之，世杰历数古忠臣曰「吾知降，生且富贵，但为主死不移耳」。",
  "result_zh_cn": "崖山破，陆秀夫走卫王舟，「度不可脱，乃杖剑驱妻子入海，即负王赴海死，年四十四」；世杰、刘义各断维去，"
                  "宋之宗社遂绝——元一统南北，宋三百二十年而亡，中国历史上第一次由北方民族完成南北一统。",
  "impact_zh_cn": "崖山海战为宋亡之终局，亦为元大一统之标志：海上之役见宋末舟师之盛与水战规模之空前，"
                  "此后明之复国与士人「崖山之后」之痛皆系于此；有元一代之南北一统与中外交通之盛均以此为始。",
  "evidence": [
   ev("宋史", "本纪", "本纪/卷四十七#p612", "text-niutrans-ece427e67b5cba9de965", "background", "primary",
      "己未，昺徙居崖山，升广州为翔龙府。", TAG),
   ev("宋史", "忠义传", "列传/卷二百一十#p66", "text-niutrans-5459278a948791b57ad3", "background", "supporting",
      "世杰以碙洲不可居，徙王新会之崖山。", TAG),
   ev("宋史", "本纪", "本纪/卷四十七#p625", "text-niutrans-82c7b57f1e731c88fc7e", "process", "primary",
      "十六年正月壬戌，张弘范兵至崖山。", TAG),
   ev("宋史", "忠义传", "列传/卷二百一十#p70", "text-niutrans-03b009e77e502b03954e", "process", "supporting",
      "明年，元帅张弘范等兵至崖山，或谓世杰曰：北兵以舟师塞海口，则我不能进退，盍先据海口。", TAG),
   ev("宋史", "忠义传", "列传/卷二百一十#p75", "text-niutrans-afe482e8b7bc526548ff", "process", "supporting",
      "弘范得世杰甥韩，命以官，使三至招之，世杰历数古忠臣曰：吾知降，生且富贵，但为主死不移耳。二月癸未，弘范等攻崖山，世杰败，走卫王舟。", TAG),
   ev("宋史", "忠义传", "列传/卷二百一十#p102", "text-niutrans-4d030cf8c8015e2f6da1", "result", "primary",
      "至元十六年二月，崖山破，秀夫走卫王舟，而世杰、刘义各断维去，秀夫度不可脱，乃杖剑驱妻子入海，即负王赴海死，年四十四。", TAG),
   ev("元史", "列传", "列传/卷三十九#p91", "text-niutrans-cd6217ec170b856c9e8d", "result", "supporting",
      "十六年，从攻崖山，弘范命渊领后翼军，水战有功。", TAG),
  ],
 },
 "ming/event-tumu-bao-zhibian.yml": {
  "background_zh_cn": "正统十四年，瓦剌也先贡马，王振减其直，使者恚而去；秋七月，也先大举入寇，王振挟帝亲征。"
                      "成国公朱勇等白事咸膝行进，尚书邝埜、王佐忤振意罚跪草中，其党钦天监正彭德清以天象谏，振终弗从——军政尽出于宦寺，败征已见。",
  "process_zh_cn": "八月己酉，帝驻大同，振益欲北；镇守太监郭敬以敌势告，振始惧，乃班师。"
                   "振初议道紫荆关、由蔚州邀帝幸其第，既恐蹂乡稼，复改道宣府——「军士纡回奔走，壬戌始次土木」；瓦剌兵追至，师大溃，帝蒙尘，振乃为乱兵所杀。",
  "result_zh_cn": "败报闻，百官恸哭，都御史陈镒等廷奏振罪，给事中王竑等立击杀马顺及毛、王二中官；郕王命脔王山于市，并振党诛之，振族无少长皆斩；"
                  "籍振家，得金银六十余库、玉盘百、珊瑚高六七尺者二十余株——土木之败使明廷精锐尽丧、英宗北狩。",
  "impact_zh_cn": "土木之变后明廷战守之局转为京师防御，于谦等立郕王而固守，明祚获安；然英宗北狩一年而还、南宫幽居，遂启八年后夺门之变，"
                  "明廷自此由开国进取转为内敛守成，宦官之祸亦由此为朝野所切齿。",
  "evidence": [
   ev("明史", "英宗前纪", "本纪/卷十#p274", "text-niutrans-22bc07d53023ec3bd799", "background", "primary",
      "秋七月己丑，瓦剌也先寇大同，参将吴浩战死，下诏亲征。", TAG),
   ev("明史", "宦官传", "列传/卷一百九十二#p112", "text-niutrans-b67babba504f6b0d13b4", "background", "primary",
      "十四年，其太师也先贡马，振减其直，使者恚而去。", TAG),
   ev("明史", "宦官传", "列传/卷一百九十二#p123", "text-niutrans-5e396c8b69cc5d382d0e", "process", "primary",
      "军士纡回奔走，壬戌始次土木。", TAG),
   ev("明史", "英宗前纪", "本纪/卷十#p290", "text-niutrans-51c128b7b387dfaf7658", "process", "primary",
      "辛酉，次土木，被围。", TAG),
   ev("明史", "宦官传", "列传/卷一百九十二#p125", "text-niutrans-e5dfcd629ee435a7dcff", "result", "primary",
      "帝蒙尘，振乃为乱兵所杀。", TAG),
   ev("明史", "宦官传", "列传/卷一百九十二#p126", "text-niutrans-8066d3b60bd2e2fbcc7d", "result", "supporting",
      "败报闻，百官恸哭，都御史陈镒等廷奏振罪，给事中王竑等立击杀马顺及毛、王二中官。", TAG),
   ev("明史", "宦官传", "列传/卷一百九十二#p128", "text-niutrans-a6d67526bafe93264bef", "result", "supporting",
      "振擅权七年，籍其家，得金银六十余库，玉盘百，珊瑚高六七尺者二十余株，他珍玩无算。", TAG),
   ev("明史", "于谦传", "列传/卷五十八#p47", "text-niutrans-985211e7456ae544a5a7", "impact", "primary",
      "及驾陷土木，京师大震，众莫知所为。", TAG),
   ev("明史", "于谦传", "列传/卷五十八#p50", "text-niutrans-5b6401cef831f1bc05ff", "impact", "supporting",
      "谦厉声曰：言南迁者，可斩也。", TAG),
  ],
  "relations": [
   {"target_event_id": "event-duomen-zhibian", "relation_type": "causes",
    "description_zh_cn": "英宗北狩还而幽居南宫，遂启夺门之变"},
  ],
 },
 "ming/event-saerhu-zhizhan.yml": {
  "background_zh_cn": "万历四十六年，帝念辽警，召刘綎为左府佥书；明年二月，经略杨镐令綎及杜松、李如柏、马林四路出师——"
                      "四路合击后金之策既定，而师期先泄、道险粮艰，诸将各不相统。",
  "process_zh_cn": "四路分进：杜松遇大清兵于吉林崖，战死；马林败没于开原之役；刘綎一路「已深入三百里，杜松军覆犹不知」，遂为后金各个击破；"
                   "杨镐闻杜松、马林师败，驰召綎及李如柏还——四路之师先后败没，萨尔浒遂为明军之覆师。",
  "result_zh_cn": "萨尔浒大败、开原继陷之后，明廷以大理寺丞熊廷弼为兵部右侍郎兼右佥都御史经略辽东；"
                  "明军主力尽丧，辽东战局由攻转守，后金之势遂不可遏。",
  "impact_zh_cn": "萨尔浒之战为明清易代第一役：明之四路丧师使辽东精锐尽失，此后加派辽饷、民困而流寇起，内外交病；"
                  "后金由守转攻，二十余年间入关定鼎——论明之亡者必自萨尔浒始。",
  "evidence": [
   ev("明史", "刘綎传", "列传/卷一百三十五#p132", "text-niutrans-674aa43c52bc6d33ae49", "background", "primary",
      "四十六年，帝念辽警，召为左府佥书。明年二月，经略杨镐令綎及杜松、李如柏、马林四路出师。", TAG),
   ev("明史", "神宗纪", "本纪/卷二十一#p295", "text-niutrans-9415b08cc2033d7dd98b", "process", "primary",
      "三月甲早，杜松遇大清兵于吉林崖，战死。", TAG),
   ev("明史", "刘綎传", "列传/卷一百三十五#p140", "text-niutrans-8e95332d60fcd51b8994", "process", "primary",
      "綎已深入三百里，杜松军覆犹不知。", TAG),
   ev("明史", "刘綎传", "列传/卷一百三十五#p153", "text-niutrans-4f41124ba788f54219c5", "process", "supporting",
      "杨镐闻杜松、马林师败，驰召綎及李如柏还。", TAG),
   ev("明史", "神宗纪", "本纪/卷二十一#p300", "text-niutrans-c2e16e42017a6184e1fc", "result", "supporting",
      "六月丁卯，大清兵克开原，马林败没。", TAG),
   ev("明史", "神宗纪", "本纪/卷二十一#p301", "text-niutrans-1794875726f0dbe3f8b0", "result", "primary",
      "癸酉，大理寺丞熊廷弼为兵部右侍郎兼右佥都御史，经略辽东。", TAG),
  ],
  "relations": [
   {"target_event_id": "event-houjin-jianguo", "relation_type": "follows",
    "description_zh_cn": "后金既立，萨尔浒为明清易代关键一役"},
   {"target_event_id": "event-liaoshen-shixian", "relation_type": "precedes",
    "description_zh_cn": "萨尔浒后明军转守，辽沈遂相继陷落"},
  ],
 },
}


def main() -> int:
    for rel, patch in PATCH.items():
        print(apply(rel, patch))
    return 0


if __name__ == "__main__":
    sys.exit(main())
