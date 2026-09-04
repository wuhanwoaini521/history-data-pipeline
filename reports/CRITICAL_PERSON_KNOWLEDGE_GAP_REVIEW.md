# CRITICAL_PERSON_KNOWLEDGE_GAP_REVIEW（V2.1.1）

- **Gate: `CRITICAL_PERSON_KNOWLEDGE_GAP_RECOVERY_READY=true`**
- events = **618**（V1 frozen，未增未删）
- V2.1 accepted **110** links 全部保留（append-only，零重写）
- 本阶段新增链接：**32**（4 resolved_existing + 28 supplemental）
- event_person 总行数（dist）= **200** = 58 legacy + 110 V2.1 + 32 V2.1.1
- store 文件：**61**（54 + 7 新建）；store person 总数：**142**
- **KNOWN_WRONG_IDENTITY = 0**；broken = 0（resolve_references 通过，build gate 通过）

## 判定明细
| event-bawang-zhi-luan | 贾南风 | supplemental（新增 curated Person） | curated-person-jia-nanfeng |
| event-beiwei-tongyi-beifang | 沮渠牧犍 | supplemental（新增 curated Person） | curated-person-juqu-mujian |
| event-changping-zhizhan | 赵括 | supplemental（新增 curated Person） | curated-person-zhao-kuo |
| event-houliang-dai-tang | 朱温 | resolved_existing（既有 KB 命中） | cbdb-person-377600 |
| event-huangchao-qiyi | 朱温 | resolved_existing（既有 KB 命中） | cbdb-person-377600 |
| event-jiawu-zhanzheng | 慈禧太后 | supplemental（新增 curated Person） | curated-person-cixi-taihou |
| event-jingkang-zhi-bian | 宋徽宗 | supplemental（新增 curated Person） | curated-person-songhuizong |
| event-jiuyiba-shibian | 石原莞尔 | supplemental（新增 curated Person） | curated-person-ishihara-kanji |
| event-jiuyiba-shibian | 板垣征四郎 | supplemental（新增 curated Person） | curated-person-itagaki-seishiro |
| event-jiuyiba-shibian | 张学良 | supplemental（新增 curated Person） | curated-person-zhang-xueliang |
| event-jiuyiba-shibian | 蒋介石 | supplemental（新增 curated Person） | curated-person-chiang-kai-shek |
| event-nanjing-datusha | 松井石根 | supplemental（新增 curated Person） | curated-person-matsui-iwane |
| event-nanjing-datusha | 谷寿夫 | supplemental（新增 curated Person） | curated-person-tani-hisao |
| event-nanjing-datusha | 唐生智 | supplemental（新增 curated Person） | curated-person-tang-shengzhi |
| event-qiguo-zhi-luan | 吴王刘濞 | supplemental（新增 curated Person） | curated-person-liu-bi |
| event-qin-tongyi | 李斯 | resolved_existing（既有 KB 命中） | ctext-person-751995 |
| event-qingdi-tuiwei | 隆裕太后 | supplemental（新增 curated Person） | curated-person-longyu |
| event-qingdi-tuiwei | 孙中山 | supplemental（新增 curated Person） | curated-person-sun-yat-sen |
| event-qiqishi-bian | 宋哲元 | supplemental（新增 curated Person） | curated-person-song-zheyuan |
| event-qiqishi-bian | 秦德纯 | supplemental（新增 curated Person） | curated-person-qin-dechun |
| event-qiqishi-bian | 牟田口廉也 | supplemental（新增 curated Person） | curated-person-mutaguchi-renya |
| event-riben-touxiang | 裕仁 | supplemental（新增 curated Person） | curated-person-hirohito |
| event-riben-touxiang | 蒋介石 | supplemental（新增 curated Person） | curated-person-chiang-kai-shek |
| event-shangtang-miexia | 商汤 | supplemental（新增 curated Person） | curated-person-shang-tang |
| event-wusi-yundong | 陈独秀 | supplemental（新增 curated Person） | curated-person-chen-duxiu |
| event-xian-shibian | 张学良 | supplemental（新增 curated Person） | curated-person-zhang-xueliang |
| event-xian-shibian | 杨虎城 | supplemental（新增 curated Person） | curated-person-yang-hucheng |
| event-xian-shibian | 蒋介石 | supplemental（新增 curated Person） | curated-person-chiang-kai-shek |
| event-xian-shibian | 周恩来 | supplemental（新增 curated Person） | curated-person-zhou-enlai |
| event-xin-mie | 刘玄 | ambiguous（不建 Person） | — |
| event-xinzhongguo-chengli | 毛泽东 | supplemental（新增 curated Person） | curated-person-mao-zedong |
| event-xinzhongguo-chengli | 周恩来 | supplemental（新增 curated Person） | curated-person-zhou-enlai |
| event-xinzhongguo-chengli | 朱德 | ambiguous（不建 Person） | — |
| event-yangjian-dai-beizhou | 周静帝 | resolved_existing（既有 KB 命中） | ctext-person-293600 |

## 质量约束执行
- 未为 `ambiguous` 创建 Person（刘玄、朱德 仅记 null ambiguous review）
- 24 条补充 Person 全部位于 `data/curated/persons/*.yml`，各有 `source_reference` 与 `source-curated-person-knowledge-gap`
- 新链接 identity_evidence / event_evidence / resolution 完整性 100%
- 补充 Person aliases 进入 `person_aliases`（source 溯源），无占位/伪造 ID

## 阻断
- 无（validate=OK，pytest 150/150 通过）
