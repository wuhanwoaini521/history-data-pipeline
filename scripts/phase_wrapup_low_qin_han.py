"""Phase Wrap-up · Depth Sprint 02 batch 1：秦 7 + 汉 3 + 战国 3 = 13 LOW 处理。

A 类（→STRONG）：qin-shihuang-beng, shaqiu-zhengbian, qin-beiji-xiongnu, qin-nanzheng-baiyue,
                 qin-xiu-changcheng, han-dingdu-changan, hanwudi-jiwei
B 类（→ADEQUATE）：qin-shutongwen, qin-tongyi-duliangheng, han-yuandi-jiwei, likui-bianfa, wuqi-bianfa
"""
from __future__ import annotations
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _depth_util import apply  # noqa: E402

P = {
 # ---------- A: 秦 ----------
 "qin_han/event-qin-shihuang-beng.yml": {
  "background_zh_cn": "始皇三十七年东巡，西还至平原津而病；帝素恶言死，群臣莫敢言死事，法令严苛而讳言凶——主上之崩实伏于巡狩道中，遗诏亦未及定。",
  "process_zh_cn": "七月丙寅，始皇崩于沙丘平台；丞相李斯「为上崩在外，恐诸公子及天下有变，乃秘之，不发丧」——置辒凉车中，百官奏事如故，中官进食如常。",
  "result_zh_cn": "丧既秘而不发，胡亥、赵高与李斯遂得从容行其谋；太子胡亥袭位为二世皇帝——始皇之死未经公议而嗣位已定，秦廷之变自此始。",
  "impact_zh_cn": "始皇之死为其身后大变的起点：秘丧、矫诏、易嗣皆自此出，秦以骤兴之势二世即亡，论者谓沙丘之事实为秦亡之枢；此后历代论秦亡者必先及此。",
 },
 "qin_han/event-shaqiu-zhengbian.yml": {
  "background_zh_cn": "七月丙寅，始皇崩于沙丘平台——主上崩于巡狩途中，遗诏未定；赵高故尝教胡亥书及狱律令法事、胡亥私幸之，故得居中用事，矫诏之谋由是而起。",
  "process_zh_cn": "赵高说胡亥，复与丞相李斯合谋：诈以始皇之命立胡亥为太子，又「更为书赐公子扶苏、蒙恬，数以罪，赐死」——外诛长子与边将，内定嗣君。",
  "result_zh_cn": "矫诏既行，扶苏赐死于上郡、蒙恬夺兵被囚，秦之良将贤嗣一时俱尽；胡亥袭位为二世皇帝，沙丘之谋遂成事实。",
  "impact_zh_cn": "沙丘之变以阴谋易嗣，秦政自此崩坏：二世继位而严刑督责、赋役益重，戍卒陈胜、吴广遂起，秦之覆亡实肇于此。",
  "relations": [
   {"target_event_id": "event-chuhan-qin-revolt", "relation_type": "leads_to", "confidence": 0.85,
    "description_zh_cn": "二世以阴谋立而政乱，次年戍卒起义，秦末大乱由此起"},
  ],
 },
 "qin_han/event-qin-beiji-xiongnu.yml": {
  "background_zh_cn": "秦已并天下，北边匈奴为患；始皇乃以蒙恬统三十万众北逐戎狄——用兵之众、专任之重，见秦以全力经营北疆之志。",
  "process_zh_cn": "蒙恬将三十万众北逐戎狄，收河南——河套之地尽入秦疆；秦以重兵长戍北边，蒙恬暴师于外十余年、居上郡，威名之盛为匈奴所惮。",
  "result_zh_cn": "是时蒙恬威振匈奴，匈奴远遁而北边暂安——河南既收，秦之北疆推至阴山一线，戍守与屯备之制随之而立。",
  "impact_zh_cn": "北击匈奴既收河南，秦遂筑长城、通直道以固边，戍边之役与长城之筑皆自此役始；然暴师十余年、民力大耗，亦为秦政苛暴之一端。",
  "relations": [
   {"target_event_id": "event-qin-xiu-changcheng", "relation_type": "precedes",
    "description_zh_cn": "北逐匈奴收河南后，乃筑长城以固新边"},
  ],
 },
 "qin_han/event-qin-nanzheng-baiyue.yml": {
  "background_zh_cn": "秦既并天下，又使尉屠睢将楼船之士南攻百越，使监禄凿渠运粮——以楼船水师与粮道工程并进，南征非徒恃兵力，而兼资水利之便。",
  "process_zh_cn": "秦军深入越地，越人遁逃；然瘴疠阻隔、戍守艰难，乃发诸尝逋亡人、赘婿、贾人略取陆梁地，为桂林、象郡、南海三郡，以适遣戍——以谪戍实岭南，军事征服与移民实边并行。",
  "result_zh_cn": "岭南置三郡、谪戍实边，中原政制自此行于岭南；其后赵佗据其地，「以兵威边，财物赂遗闽越、西瓯、骆，役属焉，东西万余里」——南越之局由此胎息。",
  "impact_zh_cn": "南征百越使岭南首次入于中国版图，桂林、象郡、南海三郡之设为后世两广政区之始；赵佗南越国立于是，秦汉之际南方政治格局由此奠定。",
  "relations": [
   {"target_event_id": "event-qin-shihuang-beng", "relation_type": "precedes",
    "description_zh_cn": "南征百越与北逐匈奴并为始皇末年之大役，四年而帝崩"},
  ],
 },
 "qin_han/event-qin-xiu-changcheng.yml": {
  "background_zh_cn": "秦已并天下，乃使蒙恬将三十万众北逐戎狄、收河南——北疆既拓而新边绵长，乃议筑长城以固之，就山川险要联络燕、赵旧城为一。",
  "process_zh_cn": "筑长城「因地形，用制险塞，起临洮，至辽东，延袤万余里」；役连万里而北边亭障相连，又通直道自九原抵云阳，堑山堙谷以利转输。",
  "result_zh_cn": "长城「起临洮属之辽东，城堑万余里」，北边亭障相连，匈奴不易南下——秦之北疆以长城为界，戍守之制亦缘之而立。",
  "impact_zh_cn": "太史公亲行其地而论曰「行观蒙恬所为秦筑长城亭障，堑山堙谷，通直道，固轻百姓力矣」——长城之役固边之功与劳民之过并见史评；后世长城遂为农耕与游牧之分界、秦汉北边秩序之象征。",
  "relations": [
   {"target_event_id": "event-qin-beiji-xiongnu", "relation_type": "follows",
    "description_zh_cn": "承北逐匈奴收河南之役而筑长城固边"},
  ],
 },
 # ---------- B: 秦制度短事件 ----------
 "qin_han/event-qin-shutongwen.yml": {
  "background_zh_cn": "秦并天下、分天下以为三十六郡，郡置守、尉、监；六国异文异制并存，文书政令难以通行，统一文字之势遂急。",
  "process_zh_cn": "书同文字——以秦文为准统一天下文字，罢其不与秦文合者；又与一法度衡石丈尺、车同轨并行，制度次第画一。",
  "result_zh_cn": "刻石纪功曰「器械一量，同书文字」——文字之统一与度量、车轨同列为秦制成就而昭示天下。",
  "impact_zh_cn": "书同文使六国文字归于一律，政令文书得以通行郡县；文字之统一与交通规制并行，为此后中华文化共同体之基。",
  "relations": [
   {"target_event_id": "event-qin-tongyi", "relation_type": "part_of",
    "description_zh_cn": "书同文为秦统一制度之一端"},
  ],
 },
 "qin_han/event-qin-tongyi-duliangheng.yml": {
  "background_zh_cn": "秦并天下、置郡县，而六国度量衡各异；赋税征收、工程营造与市易通商皆无所准，混一之制不可复缓。",
  "process_zh_cn": "一法度衡石丈尺——以秦制为准统一度、量、衡，颁之天下；又与书同文字、车同轨并行，皆所以画一制度。",
  "result_zh_cn": "刻石曰「器械一量」——器物规格随度量衡而划一，制度之统一见诸金石铭文，秦制之信验昭于后世。",
  "impact_zh_cn": "度量衡统一使全国赋税、工程与贸易有了共同尺度，秦制为汉所承，此制直行二千余年，为中国经济行政统一之基。",
  "relations": [
   {"target_event_id": "event-qin-tongyi", "relation_type": "part_of",
    "description_zh_cn": "统一度量衡为秦统一制度之一端"},
  ],
 },
 # ---------- 战国 ----------
 "chunqiu_zhanguo/event-guiling-zhizhan.yml": {
  "background_zh_cn": "魏围赵邯郸，赵请救于齐——齐使田忌、孙膑救赵；孙膑以「批亢捣虚」为策，不趋邯郸而与魏争其必救，救赵之谋实为制魏之谋。",
  "process_zh_cn": "田忌从孙膑之计，直趋大梁；魏果去邯郸而还师自救，与齐战于桂陵——齐以逸待劳，一战而大破梁军。",
  "result_zh_cn": "十月，邯郸抜而齐因起兵击魏，大败之桂陵；魏之东线受挫，齐之军威大振于诸侯。",
  "impact_zh_cn": "「围魏救赵」之策由是成为兵家范式，孙膑兵法传于后世；魏、齐之强弱易势自此始，十三年后马陵之战遂定魏之衰局。",
  "relations": [
   {"target_event_id": "event-maling-zhizhan", "relation_type": "precedes",
    "description_zh_cn": "桂陵之捷为齐魏争衡之首役，马陵之战继之而定局"},
  ],
 },
 "chunqiu_zhanguo/event-likui-bianfa.yml": {
  "background_zh_cn": "当魏文侯时，李克务尽地力，而白圭乐观时变——战国初期魏国率先以农事与治术求富强，李悝变法之机已具。",
  "process_zh_cn": "魏有李悝，「尽地力之教」：教民勤于农事、地尽其利，以农富国——教令行于田野，耕稼之利尽出。",
  "result_zh_cn": "魏用李克、尽地力，「为强君」——魏国由是富强，为战国初期之首次强国，诸侯莫敢与之争。",
  "impact_zh_cn": "尽地力之教开列国变法之先声，其后商鞅变法即承此路径；魏之富强为战国变法时代揭幕，李悝之教遂为法家农战之祖。",
  "relations": [
   {"target_event_id": "event-shangyang-bianfa", "relation_type": "related_to",
    "description_zh_cn": "李悝尽地力之教为商鞅变法之先声"},
  ],
 },
 "chunqiu_zhanguo/event-wuqi-bianfa.yml": {
  "background_zh_cn": "吴起去魏之楚，楚悼王闻其贤而相之；吴起乃以魏之治术施于楚——「明法审令，捐不急之官，废公族疏远者，以抚养战斗之士」。",
  "process_zh_cn": "变法既行：削公族疏远者之禄，罢不急之官，厚战斗之士；于是楚人争奋，兵势骤张，南平百越、北并陈蔡、却三晋、西伐秦——楚之疆域与兵威一时大振。",
  "result_zh_cn": "楚以吴起之谋扩地千里，兵威南暨百越、北抗三晋；然新法削贵戚之权，宗室大臣怨望日深，变局已伏杀机。",
  "impact_zh_cn": "及悼王死，宗室大臣作乱而攻吴起，「击起之徒因射刺吴起，并中悼王」——变法中辍、吴起殉难；然其明法审令、废公族之路径为后世楚制改革所本。",
  "relations": [
   {"target_event_id": "event-shangyang-bianfa", "relation_type": "related_to",
    "description_zh_cn": "吴起变法与商鞅变法同为战国法家改革之先例"},
  ],
 },
 # ---------- 汉 ----------
 "qin_han/event-han-dingdu-changan.yml": {
  "background_zh_cn": "高祖欲长都雒阳；齐人刘敬说以关中形胜，留侯亦劝上入都关中——「关中阻山河四塞，地肥饶，可都以霸」，东都雒阳与西都关中之议遂决。",
  "process_zh_cn": "高祖从刘敬、张良之言，是日驾而西，入都关中；其后长乐宫成，丞相已下徙治长安——宫室官署次第就绪，都邑之制以立。",
  "result_zh_cn": "高祖自布军至长安，都城秩序既定；关中遂为汉家根本之地，与雒阳隔河相望而为东西两京之始基。",
  "impact_zh_cn": "定都关中据山河四塞之形胜，长安自此为西汉二百年之国都；此后新莽、隋唐皆都关中，其基实肇于汉初之议，长安遂为中国千年古都之首。",
  "relations": [
   {"target_event_id": "event-chuhan-gaixia", "relation_type": "follows",
    "description_zh_cn": "垓下既定而天下归汉，乃有定都之议"},
  ],
 },
 "qin_han/event-hanwudi-jiwei.yml": {
  "background_zh_cn": "景帝崩，太子彻即位，年方十六而嗣大位；黄老之治行于汉家已数十年，而儒术之士渐起，政风之变已伏于即位之际。",
  "process_zh_cn": "甲子，太子即皇帝位，尊皇太后窦氏曰太皇太后、皇后曰皇太后；即位之初即诏丞相、御史、列侯等「举贤良方正直言极谏之士」，求言之路大开。",
  "result_zh_cn": "贤良之诏既下，赵绾、王臧之属以儒学进用，汉廷用人自黄老而转向儒术，一代政治之新局自此启。",
  "impact_zh_cn": "「及今上即位，赵绾、王臧之属明儒学，而上亦乡之，于是招方正贤良文学之士」——儒术之士由是入朝，汉武一朝之制度、学术与用兵皆自此发端。",
  "relations": [
   {"target_event_id": "event-mobei-zhizhan", "relation_type": "precedes",
    "description_zh_cn": "即位举贤、儒术进用，数十年后乃有汉匈决战与汉武之世"},
  ],
 },
 "qin_han/event-han-yuandi-jiwei.yml": {
  "background_zh_cn": "「孝元皇帝，宣帝太子也」；宣帝尝「有意欲用淮阳王代太子，然以少依许氏，俱从微起，故终不背焉」——储位几易而终定，元帝之立实系于许氏旧恩。",
  "process_zh_cn": "黄龙元年十二月，宣帝崩；癸巳，太子即皇帝位，谒高庙——继统之礼依制而行，昭宣之政遂告终。",
  "result_zh_cn": "元帝即位，尊皇太后、立皇后，外戚许氏之望与儒臣之进并起；汉廷自昭宣之综核名实转入元成之宽柔。",
  "impact_zh_cn": "元帝柔仁好儒之君临朝，汉政自此转向儒术与权臣交争之局；昭宣中兴之业渐替，西汉中后期之外戚与儒臣政治皆肇于此。",
 },
}
for rel, patch in P.items():
    print(apply(rel, patch) if "relations" in patch else apply(rel, patch))
