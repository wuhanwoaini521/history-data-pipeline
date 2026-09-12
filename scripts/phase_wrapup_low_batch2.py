"""Phase Wrap-up · Depth Sprint 02 batch 2：三国 2 + 唐 2 + 明 2 LOW + batch1 弱项补足。"""
from __future__ import annotations
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _depth_util import apply  # noqa: E402

P = {
 # ---------- batch1 弱项补足（≥40 且 ≥2 阶段） ----------
 "qin_han/event-qin-tongyi-duliangheng.yml": {
  "impact_zh_cn": "度量衡统一使全国赋税征收、工程营造与市易通商有了共同尺度，秦制为汉所承，此制直行二千余年，为中国经济与行政统一之基；秦虽二世而亡，其度量之制则历代相沿。",
 },
 "chunqiu_zhanguo/event-guiling-zhizhan.yml": {
  "result_zh_cn": "十月，邯郸拔而齐因起兵击魏，大败之桂陵——魏军弃邯郸而还自救，终为齐所破，魏之东线由是受挫，齐之军威大振于诸侯。",
 },
 "qin_han/event-hanwudi-jiwei.yml": {
  "result_zh_cn": "贤良之诏既下，赵绾、王臧之属以儒学进用，汉廷用人自黄老而转向儒术，一代政治与学术之新局自此启于即位之初。",
 },
 # ---------- 三国 ----------
 "three_kingdoms/event-three-guandu.yml": {
  "background_zh_cn": "曹操还军官渡，袁绍乃议攻许，田丰谏之以持久而不从——袁绍倾河北之众南下，两雄决战之势已成；曹军兵少粮绌而据守要津，胜负之数系于粮道与人心。",
  "process_zh_cn": "袁氏辎重万余乘在故市、乌巢，屯军无严备；曹操纳降将之计，以轻兵袭之，「不意而至，燔其积聚，不过三日，袁氏自败也」——乌巢火起，绍军粮谷尽焚。",
  "result_zh_cn": "士卒皆殊死战，遂大破之，斩淳于琼等、尽燔其粮谷；于是绍军惊扰大溃，绍及谭等幅巾乘马、与八百骑渡河——河北之众一夜而溃。",
  "impact_zh_cn": "官渡之败使袁绍元气大伤，河北由盛转衰；曹操由此奠定统一北方之势，此后攻邺、平河北皆循此局，三国鼎立之北方一极实肇于此役。",
  "relations": [
   {"target_event_id": "event-three-north-consolidation", "relation_type": "precedes",
    "description_zh_cn": "官渡既胜，曹操乘势进军河北、平袁氏"},
  ],
 },
 "three_kingdoms/event-three-north-consolidation.yml": {
  "background_zh_cn": "官渡战后，曹操进军邺——袁氏根本之地；袁绍既死，谭、尚争冀州，河北之势自内而裂，曹操乘其兄弟阋墙而次第收之。",
  "process_zh_cn": "公之去邺而南也，谭、尚争冀州，谭为尚所败、走保平原；曹操因其内溃而北伐乌桓，九月引兵自柳城还，康即斩尚、熙及速仆丸等，传其首——袁氏余烬尽灭。",
  "result_zh_cn": "袁氏覆灭而河北悉平，幽、冀、并、青四州尽入于曹操；北方群雄略定，许都之政令得行于大河以北。",
  "impact_zh_cn": "河北既平，汉罢三公官、置丞相、御史大夫——曹操中枢集权，为南征荆州与魏室肇基铺路，北方一统遂成三国之局的基础。",
  "relations": [
   {"target_event_id": "event-three-guandu", "relation_type": "follows",
    "description_zh_cn": "官渡之胜为其后平定河北、巩固北方之本"},
  ],
 },
 # ---------- 唐 ----------
 "sui_tang/event-anlu-shi-siming.yml": {
  "background_zh_cn": "安庆绪既败，史思明一度降唐而旋复自立：承恩说思明降唐，然唐廷处置失当，思明遂拥众自固于范阳——安史之乱由安禄山集团转入史思明主导之阶段。",
  "process_zh_cn": "乾元二年春正月己巳朔，史思明筑坛于魏州城北，自称大圣燕王，以周挚为行军司马——僭号建制，与安庆绪分道；安庆绪收子仪等营中粮得六七万石，闭门拒思明。",
  "result_zh_cn": "思明与庆绪决裂而并其众：乃手疏唁庆绪而不称臣，且曰「愿为兄弟之国，更作藩篱之援」——使者往复之间，思明已成河北最强之势力，唐军所面对着由安庆绪易为史思明。",
  "impact_zh_cn": "史思明之再叛使安史之乱延长数年：唐军洛阳之捷得而复失，河北藩镇之降将皆观思明之向背；乱平之后河朔三镇之割据，实由此阶段之势力格局所奠定。",
  "relations": [
   {"target_event_id": "event-anlu-uprising", "relation_type": "part_of", "confidence": 0.9,
    "description_zh_cn": "史思明再叛为安史之乱之后期阶段"},
  ],
 },
 "sui_tang/event-anlu-xuanzong-shu.yml": {
  "background_zh_cn": "杨国忠自以身领剑南，闻安禄山反，即令副使崔圆阴具储偫，以备有急投之，至是首唱幸蜀之策——入蜀之议实先有所备，非仓卒之谋。",
  "process_zh_cn": "丙申，玄宗一行至马嵬驿，将士饥疲、皆愤怒——马嵬之变既起，杨国忠、杨贵妃相继而殒；玄宗乃命将士陈之庭前，亲谕曰「朕比来衰耄，托任失人，致逆胡乱常，须远避其锋」，遂继续西行入蜀。",
  "result_zh_cn": "庚辰，上皇至成都，从官及六军至者千三百人而已——玄宗随行力量大为缩减，唐廷中枢实际转入肃宗灵武集团，皇帝与上皇分处两地。",
  "impact_zh_cn": "玄宗入蜀使唐廷政治中心暂时转移，肃宗灵武即位而组织反攻；此后上皇还京而不复预政，唐代皇权更迭与宦官、藩镇之局自安史之乱起皆由此转折。",
  "relations": [
   {"target_event_id": "event-anlu-uprising", "relation_type": "part_of", "confidence": 0.9,
    "description_zh_cn": "玄宗幸蜀为安史之乱中唐廷播迁之阶段"},
  ],
 },
 # ---------- 明 ----------
 "ming/event-lizicheng-gong-beijing.yml": {
  "background_zh_cn": "崇祯十七年，流贼自秦入豫、渐逼畿甸：辛丑，京师戒严；辛卯，李自成陷陕州——明廷外有清兵之压、内有流寇之逼，辽饷加派而民困，畿辅之防已不能支。",
  "process_zh_cn": "三月丁未，昧爽，内城陷——李自成军自居庸关、昌平而下，太监开门内应，京师外城、内城次第不守；帝登万岁山自缢，王承恩从死，明之京畿中枢一夜崩解。",
  "result_zh_cn": "帝崩于万岁山，王承恩从死——崇祯殉国，明朝作为全国政权的统治终结；李自成入居大内，大顺政权代明而有京师。",
  "impact_zh_cn": "是年夏四月，大清兵破贼于山海关，五月入京师，以帝体改葬、令臣民为服丧三日，谥曰庄烈愍皇帝，陵曰思陵——李自成败亡而清朝入主，易代之局完成，明祚乃移于南明。",
  "relations": [
   {"target_event_id": "event-nanming-hongguang", "relation_type": "leads_to",
    "description_zh_cn": "北京既陷，明臣拥立福王于南京，南明之局始"},
  ],
 },
 "ming/event-zhuyuanzhang-chendi.yml": {
  "background_zh_cn": "陈友谅既亡，太祖曰「友谅亡，天下不难定也」——南方群雄次第削平，张士诚、方国珍相继而灭，帝业之势已成；徐达、常遇春北伐中原，元室北遁。",
  "process_zh_cn": "洪武元年春正月乙亥，祀天地于南郊，即皇帝位，定国号曰明，建元洪武——郊祀告天，正位号以承天命，明之开国大典具焉。",
  "result_zh_cn": "追尊四代考妣为帝后、立妃马氏为皇后、世子标为皇太子——宗庙与国本一时并定，开国之后继有人焉。",
  "impact_zh_cn": "以李善长、徐达为左、右丞相，诸功臣进爵有差——明初之中枢架构与功臣体制自此建立，洪武之政由是推行三十余年。",
  "relations": [
   {"target_event_id": "event-chenyouliang-dai-han", "relation_type": "follows",
    "description_zh_cn": "陈友谅败亡为明室削平群雄、建立帝业之先"},
  ],
 },
}
for rel, patch in P.items():
    print(apply(rel, patch))
