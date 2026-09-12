"""Cluster H 收尾：把 result/impact 补足到 STRONG 档（>=90 字、阶段化），内容仍只见于已锚定段落。"""
from __future__ import annotations
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
EVENTS = ROOT / "data" / "curated" / "history_backbone" / "events" / "ming"

PATCH = {
 "event-chongzhen-jiwei.yml": {
  "result_zh_cn": "魏忠贤既诛，其党崔呈秀戮尸，冯铨、魏广微削籍；崇祯二年定逆案，自崔呈秀以下凡六等，阉党之局遂倾；汪文言狱所陷诸臣得赠恤，东林善类稍得伸眉。然门户之见已深，定逆案之后朝论益分，攻东林者转以「逆案」为口实相攻。",
  "impact_zh_cn": "崇祯初政以诛阉、定案为始，一时号清明；然党争并未止息，十七年间阁臣屡易、边事日坏，终至李自成入京师、帝崩于万岁山，王承恩从死——明代之亡虽非阉祸直接所致，而朝局内耗与门户之祸实为长因之一。",
 },
 "event-jianwen-xuefan.yml": {
  "background_zh_cn": "洪武三十一年太祖崩，皇太孙即位，命齐泰与黄子澄同参国政，寻进尚书；太祖旧尝重泰，皇太孙素重之，二人遂为腹心。时诸王以叔父之尊拥兵边塞，周、齐、湘、代、岷诸王多不法，朝廷议削藩以固皇权，遂有次第废徙之举。",
  "result_zh_cn": "朝廷初贬齐泰、黄子澄于外以缓燕师，旋复召二人；南北转战四年，建文四年六月乙丑燕兵犯金川门，左都督徐增寿谋内应伏诛，宫中火起，帝不知所终——削藩之政以藩王入继告终，齐、黄皆死难。",
  "impact_zh_cn": "建文削藩失败，燕王以「靖难」入承大统，是为成祖；事定之后，削藩之议转为厉禁宗室之制——有明一代藩王不典兵、不预政，而永乐以后内阁与宦官之制亦由此开其端，明初政治格局为之一变。",
 },
 "event-donglin-dangzheng.yml": {
  "result_zh_cn": "崇祯初定逆案，阉党既黜，杨涟、左光斗等死难诸臣得赠恤；然门户之见已深，继任阁臣张至发、薛国观皆不喜东林，所司不敢复奏；南明诸朝犹以门户相攻，党争与国祚相终始。",
  "impact_zh_cn": "东林由书院讲学而成政治标目，党争自万历延至南明，凡京察、三案、逆案皆以门户为断，人才进退系于党派；明代士大夫政治之激化与内阁票拟、言路风宪之败坏于此可见，识者以为明亡之由之一，而东林诸君子以气节相高，其风节亦自有不可废者。",
 },
 "event-duomen-zhibian.yml": {
  "result_zh_cn": "夺门诸臣以功邀宠，曹吉祥有宠颛政，石亨益横；天顺三年后石亨以罪罢，未几有罪下狱死，曹吉祥复以谋反败诛；英宗晚年从李贤之言，始悟「夺门」非是，诏诸夺门冒功者许自首改正，于谦、王文之冤至是渐白。",
  "impact_zh_cn": "夺门之变以「迎复」之名矫杀社稷之臣，于谦、王文之死为明代第一大冤狱，萧维桢附会徐有贞而成之；此后天顺一朝宦官曹吉祥、武将石亨相继用事，英宗复辟之局反成内耗之源，「夺门」二字终为士论所非，明代君臣互信再受重创。",
 },
 "event-houjin-jianguo.yml": {
  "result_zh_cn": "抚顺既克，明廷以杨镐经略辽东，四路出师而萨尔浒大败，杜松战死；六月大清兵克开原，马林败没，乃以大理寺丞熊廷弼为兵部右侍郎兼右佥都御史经略辽东——辽东战守自此为明代第一重务，明军由攻转守。",
  "impact_zh_cn": "后金既立，辽东攻守之势逆转：萨尔浒一战明军主力尽丧，开原继陷，明由进攻转为守御；此后二十余年间清兵数入塞，终有明清易代之事，而明廷竭天下之力以事辽东，民穷财尽，流寇乘之，内外交病。",
 },
 "event-dongnan-wokou.yml": {
  "result_zh_cn": "东南倭寇次第荡平：胡宗宪破倭于刘家庄，复征俞大猷、戚继光、刘显诸将合击破之于福建；戚继光、俞大猷复兴化城，共破海倭，福建巡抚游震得以浙江温、处与福宁接壤、倭所出没，请进戚继光为副总兵守之，海防之制由此重整。",
  "impact_zh_cn": "倭患既平，戚继光等列海防善后事、修城练兵，募兵之制渐代卫所，明代东南海防为一变；而倭乱之起由海禁与互市之失，官军围南沙五阅月不克，尤见卫所积弛之弊，驭海之策遂为有识者所深论。",
 },
 "event-daliyi.yml": {
  "result_zh_cn": "大礼议以帝意得伸告终：十月追尊父兴献王为兴献帝，既而命称孝宗皇考、兴献帝后为本生父母，杨廷和等持礼之臣或罢或贬；张璁、桂萼、方献夫等以议礼骤贵，夏言继之，成为嘉靖前期内阁之新局。",
  "impact_zh_cn": "大礼议表面争「继统」「继嗣」之礼，实为嘉靖帝确立皇权自主、重组外廷之契机：持礼旧臣去而议礼新贵进，内阁与言路之势为之一变；此后世宗以制礼作乐自任，明代礼制与政治之关系愈密，而议礼一事遂为嘉靖一朝人事更迭之枢机。",
 },
}


def main() -> int:
    n = 0
    for name, patch in PATCH.items():
        path = EVENTS / name
        if not path.exists():
            print(f"MISSING {name}")
            continue
        d = yaml.safe_load(path.read_text(encoding="utf-8"))
        changed = False
        for k, v in patch.items():
            if d.get(k) != v:
                d[k] = v
                changed = True
        if not changed:
            print(f"SKIP {name}")
            continue
        # preserve header comments by rewriting body only
        text = path.read_text(encoding="utf-8")
        header = []
        for line in text.splitlines():
            if line.startswith("#") or line.strip() == "":
                header.append(line)
            else:
                break
        body = yaml.safe_dump(d, allow_unicode=True, sort_keys=False,
                              default_flow_style=False, width=10**6)
        path.write_text("\n".join(header).rstrip("\n") + "\n" + body, encoding="utf-8")
        n += 1
        print(f"patched {name}")
    print(f"total: {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
