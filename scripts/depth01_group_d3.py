"""Depth Sprint 01 · D3（南北朝隋 4 事件）——北魏分裂/北周灭北齐/侯景之乱/隋灭陈。"""
from __future__ import annotations
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _depth_util import apply, ev  # noqa: E402

TAG = "depth01-D3"

PATCH = {
 "jin_southern_northern/event-beiwei-fenlie.yml": {
  "background_zh_cn": "魏末君臣相疑：斛斯椿等与南阳王宝炬、武卫将军元毗、王思政「构神武于魏帝」，魏帝由是心贰于贺拔岳；高乾密启神武言魏帝之贰而神武封呈于帝，魏帝遂杀乾，"
                      "又遣使密敕长乐太守庞苍鹰令杀其弟昂——「于是魏帝与神武隙矣」。永熙三年，魏帝还邺，神武饯于乾脯山，执手而别，实已决裂。",
  "process_zh_cn": "永熙三年七月丁未，魏孝武帝「遂从洛阳率轻骑入关」，宇文泰（太祖）备仪卫奉迎，谒见东阳驿——帝西迁长安、依关陇以自固；"
                   "初，魏帝在洛阳许以冯翊长公主配太祖，未及结纳而帝西迁。高氏则以婚姻缔结魏室：孝静皇后高氏为齐献武王第二女，孝静帝妹又适高氏——东魏之政实出高欢。",
  "result_zh_cn": "是岁闰十二月，魏孝武帝崩于长安；魏室于是西东并立，宇文泰、高欢各挟一帝，北魏之名虽存而实亡。"
                  "此后西魏文帝、东魏孝静帝并立于长安、邺城，东西相攻无岁不有，至周、齐受禅而终成两国。",
  "impact_zh_cn": "北魏分裂为北齐、北周之所自出：宇文泰所统之关陇集团与高欢所统之山东豪族自此分途，"
                  "府兵制、六官制皆立于西魏北周，隋唐皇室与制度皆出关陇一系——北魏分裂实为北朝后期政治之枢纽，亦隋唐统一之远源。",
  "evidence": [
   ev("北齐书", "神武纪", "本纪/卷一#p227", "text-niutrans-0ba046206ba530369bf3", "background", "primary",
      "斛斯椿由是内不自安，乃与南阳王宝炬及武卫将军元毗、魏光、王思政构神武于魏帝。", TAG),
   ev("北齐书", "神武纪", "本纪/卷一#p242", "text-niutrans-c2cd883649588a39fc27", "background", "primary",
      "于是魏帝与神武隙矣。", TAG),
   ev("北齐书", "神武纪", "本纪/卷一#p212", "text-niutrans-3f8a7a62d914f2bd8ded", "background", "supporting",
      "壬辰，还邺，魏帝饯于乾脯山，执手而别。", TAG),
   ev("周书", "文帝纪", "本纪/卷一#p259", "text-niutrans-8eacfbd5a431229f733e", "process", "primary",
      "七月丁未，帝遂从洛阳率轻骑入关，太祖备仪卫奉迎，谒见东阳驿。", TAG),
   ev("周书", "文帝纪", "本纪/卷一#p269", "text-niutrans-4316466e7ce203a4219f", "process", "supporting",
      "初，魏帝在洛阳，许以冯翊长公主配太祖，未及结纳，而帝西迁。", TAG),
   ev("周书", "文帝纪", "本纪/卷一#p278", "text-niutrans-3d668c0dd86d8239bb59", "result", "primary",
      "闰十二月，魏孝武帝崩。", TAG),
   ev("魏书", "列传", "列传/卷一#p432", "text-niutrans-6c5a398f9d6c7b62f55d", "result", "supporting",
      "孝静皇后高氏，齐献武王之第二女也。", TAG, "东魏之政出高氏之证"),
   ev("周书", "列传", "列传/卷三十#p27", "text-niutrans-6bfd3ab32d41467cc3ed", "impact", "supporting",
      "时帝与齐神武构隙，以炽有威重，堪处爪牙之任……遂从帝西迁。", TAG),
  ],
 },
 "jin_southern_northern/event-beizhou-mie-beiqi.yml": {
  "background_zh_cn": "周武帝以晋州为平齐之基：既拔晋州，执守臣之手曰「朕有晋州，为平齐之基，宜善守之」——伐齐之策已定于晋州一城。"
                      "时北齐政乱，周军逼并州，又遣大将军达奚武帅众数万至东雍及晋州，与突厥相应，南北夹击之势既成。",
  "process_zh_cn": "建德六年（577年），周武帝亲总大军东讨：先拔晋州、再克并州，长驱而东，直指邺城；北齐之众望风而溃，"
                   "诸将从军攻晋州者以功授使持节、车骑将军，更论晋州及平齐之勋加骠骑大将军、开府仪同三司——战功之赏皆以平齐为最。",
  "result_zh_cn": "丁未，齐主至，周武帝「降自阼阶，以宾主之礼相见」——北齐后主为周所获，齐亡；周尽有齐地，北方复归一统，"
                  "自东西魏分裂以来四十余年之局至此终结。",
  "impact_zh_cn": "北周灭北齐使北方重归统一，为隋代周后平陈混一奠定基础；关陇之政既兼山东，府兵、均田诸制遂行于河北，"
                  "而周宣帝之后杨坚受禅建隋，齐之亡实启隋之兴，北方统一乃南方统一之先声。",
  "evidence": [
   ev("周书", "列传", "列传/卷三十一#p76", "text-niutrans-25188e1dfab3ce31b7fd", "background", "primary",
      "执其手曰：朕有晋州，为平齐之基，宜善守之。及齐平，封郕国公，位上柱国、雍州总管。", TAG),
   ev("北齐书", "后主纪", "本纪/卷七#p59", "text-niutrans-22539a7916da605e7e93", "background", "supporting",
      "己未，周军逼并州，又遣大将军达奚武帅众数万至东雍及晋州，与突厥相应。", TAG),
   ev("周书", "武帝纪", "本纪/卷六#p241", "text-niutrans-c392fc17051abd38b103", "result", "primary",
      "丁未，齐主至，帝降自阼阶，以宾主之礼相见。", TAG),
   ev("周书", "列传", "列传/卷三十一#p70", "text-niutrans-d5b21b4677cee2415fb2", "process", "supporting",
      "后以熊州刺史从武帝拔晋州，进位大将军，除晋州刺史。", TAG),
   ev("周书", "列传", "列传/卷三十#p95", "text-niutrans-a9a484ff0fc2a61b8b5c", "result", "supporting",
      "从高祖平齐，封赞国公，除西兖州总管。", TAG),
   ev("周书", "列传", "列传/卷三十六#p356", "text-niutrans-68229e1036e0e1a43a78", "process", "supporting",
      "后更论晋州及平齐勋，加骠骑大将军、开府仪同三司。迁兖州刺史。", TAG),
  ],
 },
 "jin_southern_northern/event-houjing-zhi-luan.yml": {
  "background_zh_cn": "侯景本东魏将，大同二年「魏遣将侯景率众七万寇楚州」，既败而降梁，梁武帝纳之，景遂据寿阳。"
                      "太清二年，侯景围历阳，梁将启云「采石急须重镇，王质水军轻弱，恐虑不济」——江防之疏、藩镇之骄，祸机已伏。",
  "process_zh_cn": "太清二年（548年）八月戊戌，侯景举兵反，擅攻马头、木栅、荆山等戍；是岁侯景寇京师，梁将率所部入援，有卒于围内者。"
                   "太清三年，侯景攻陷台城：「时太宗居永福省，贼众奔入，举兵上殿，侍卫奔散，莫有存者」——台城既陷，梁武帝、简文帝相继受制于景。",
  "result_zh_cn": "台城陷后，侯景纵兵大掠，建康残破、士民死亡相继；梁室诸王拥兵相攻而不赴国难，"
                  "其后景篡立为汉帝，为王僧辩、陈霸先所讨平，而梁祚亦尽——江陵再陷于西魏，陈霸先遂代梁而立。",
  "impact_zh_cn": "侯景之乱为南朝由盛转衰之枢：建康宫阙焚毁，门阀士族凋零殆尽，江南文物之盛一落千丈；"
                  "梁亡而陈立，南朝仅余一国之力，终不能敌北；隋之平陈实肇于此役之耗，论者谓南朝之亡自侯景始。",
  "evidence": [
   ev("梁书", "列传", "列传/卷三十二#p102", "text-niutrans-62481e4456c5818b100c", "background", "primary",
      "大同二年，魏遣将侯景率众七万寇楚州，刺史桓和陷没，景仍进军淮上。", TAG),
   ev("梁书", "列传", "列传/卷三十二#p125", "text-niutrans-c903107ae4fec26de4b1", "background", "supporting",
      "太清二年，侯景围历阳，敕召昕还，昕启云：采石急须重镇，王质水军轻弱，恐虑不济。", TAG),
   ev("梁书", "武帝纪", "本纪/卷三#p594", "text-niutrans-fecbb1e5fdd39f4912e2", "process", "primary",
      "戊戌，侯景举兵反，擅攻马头、木栅、荆山等戍。", TAG),
   ev("梁书", "列传", "列传/卷三十#p155", "text-niutrans-b7bc5468cde6d94afa75", "result", "primary",
      "太清三年，侯景攻陷台城，时太宗居永福省，贼众奔入，举兵上殿，侍卫奔散，莫有存者。", TAG),
   ev("梁书", "列传", "列传/卷三十九#p128", "text-niutrans-c70ee64c159e17611567", "process", "supporting",
      "侯景反，攻陷历阳，高祖问侃讨景之策。", TAG),
   ev("梁书", "列传", "列传/卷三十七#p43", "text-niutrans-cfe75a4050821d380a43", "result", "supporting",
      "是岁，侯景寇京师，举卒于围内。", TAG),
  ],
  "relations": [
   {"target_event_id": "event-sui-mie-chen", "relation_type": "precedes",
    "description_zh_cn": "侯景之乱耗竭南朝国力，为隋灭陈之远因"},
  ],
 },
 "jin_southern_northern/event-sui-mie-chen.yml": {
  "background_zh_cn": "陈后主之世，「新失淮南之地，隋师临江，又国遭大丧，后主病疮，不能听政」，诛叔陵、供丧事、边境防守及百司众务皆决于皇太后——"
                      "主幼国疑，江防日弛；隋将贺若弼先献取陈十策，文帝纳之，伐陈之谋遂决。",
  "process_zh_cn": "开皇九年（589年）正月辛未，贺若弼拔陈京口，韩擒虎拔陈南豫州；丙子，贺若弼败陈师于蒋山，获其将萧摩诃；"
                   "韩擒虎进师入建邺，获其将任蛮奴，获陈主叔宝——从韩擒虎、贺若弼两路并进，陈之江防一战而溃。",
  "result_zh_cn": "陈亡：「及隋军陷台城，妃与后主俱入于井，隋军出之，晋王广命斩贵妃，榜于青溪中桥」；"
                  "隋尽有陈地，自永嘉之乱以来近三百年之南北分裂至此终结，天下复归一统。",
  "impact_zh_cn": "隋灭陈为魏晋南北朝之终、隋唐统一之始：南北制度、学术、文学由是合流，南朝文物入于关中，"
                  "此后唐宋之盛皆以大一统为前提——三百年分裂之局既合，中国历史遂入新期。",
  "evidence": [
   ev("陈书", "列传", "列传/卷一#p87", "text-niutrans-aa55f042d79e9866de71", "background", "primary",
      "当是之时，新失淮南之地，隋师临江，又国遭大丧，后主病疮，不能听政……实皆决之于后。", TAG),
   ev("隋书", "列传", "列传/卷六#p72", "text-niutrans-86a34844970926297497", "background", "supporting",
      "上尝从容命颎与贺若弼言及平陈事，颎曰：贺若弼先献十策，后于蒋山苦战破贼。", TAG),
   ev("隋书", "帝纪", "帝纪/卷二#p24", "text-niutrans-220819073266317017e3", "process", "primary",
      "辛未，贺若弼拔陈京口，韩擒虎拔陈南豫州。", TAG),
   ev("隋书", "帝纪", "帝纪/卷二#p26", "text-niutrans-0b5cdcf5aa0de806ff40", "process", "primary",
      "丙子，贺若弼败陈师于蒋山，获其将萧摩诃。", TAG),
   ev("隋书", "帝纪", "帝纪/卷二#p27", "text-niutrans-b183fb733c790940ed64", "result", "primary",
      "韩擒虎进师入建鄴，获其将任蛮奴，获陈主叔宝。", TAG),
   ev("陈书", "列传", "列传/卷一#p130", "text-niutrans-9ad3da5d99101be4a29f", "result", "supporting",
      "及隋军陷台城，妃与后主俱入于井，隋军出之，晋王广命斩贵妃，榜于青溪中桥。", TAG),
  ],
 },
}


def main() -> int:
    for rel, patch in PATCH.items():
        print(apply(rel, patch))
    return 0


if __name__ == "__main__":
    sys.exit(main())
