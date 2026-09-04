# CRITICAL_PERSON_KNOWLEDGE_GAP_SCOPE（V2.1.1 冻结范围）

- 来源：`reports/PERSON_KNOWLEDGE_GAPS.md`（V2.1 记录的 34 条 not_found 全部纳入，不扩展）
- 范围总数：**34**；未知 event_id = ∅（全部命中 618 events backbone）
- 判定分布：
  - `resolved_existing`：**4** → 既有 KB 命中，新增链接，不新增 Person
  - `ambiguous`：**2** → 同名多项/类别冲突，保留 gap，不建第二条 canonical
  - `supplemental`：**28** → **24 unique Persons**（genuinely missing 才补）

## 逐条判定

| Event | Raw Person | 判定 | 目标 Person ID |
|---|---|---|---|
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

## 补充 Person（unique 24）

  - `curated-person-chen-duxiu` — 陈独秀（1879–1942）
  - `curated-person-chiang-kai-shek` — 蒋介石（1887–1975）
  - `curated-person-cixi-taihou` — 慈禧太后（1835–1908）
  - `curated-person-hirohito` — 裕仁（1901–1989）
  - `curated-person-ishihara-kanji` — 石原莞尔（1889–1949）
  - `curated-person-itagaki-seishiro` — 板垣征四郎（1885–1948）
  - `curated-person-jia-nanfeng` — 贾南风（?–300）
  - `curated-person-juqu-mujian` — 沮渠牧犍（?–447）
  - `curated-person-liu-bi` — 刘濞（?–-154）
  - `curated-person-longyu` — 隆裕太后（1868–1913）
  - `curated-person-mao-zedong` — 毛泽东（1893–1976）
  - `curated-person-matsui-iwane` — 松井石根（1878–1948）
  - `curated-person-mutaguchi-renya` — 牟田口廉也（1888–1966）
  - `curated-person-qin-dechun` — 秦德纯（1893–1963）
  - `curated-person-shang-tang` — 商汤（?–?）
  - `curated-person-song-zheyuan` — 宋哲元（1885–1940）
  - `curated-person-songhuizong` — 赵佶(宋徽宗)（1082–1135）
  - `curated-person-sun-yat-sen` — 孙中山（1866–1925）
  - `curated-person-tang-shengzhi` — 唐生智（1889–1970）
  - `curated-person-tani-hisao` — 谷寿夫（1882–1947）
  - `curated-person-yang-hucheng` — 杨虎城（1893–1949）
  - `curated-person-zhang-xueliang` — 张学良（1901–2001）
  - `curated-person-zhao-kuo` — 赵括（?–-260）
  - `curated-person-zhou-enlai` — 周恩来（1898–1976）

## 来源与审计
- reviewed_by = `china-history-backbone-v2.1.1-curator`；补充 Person source_id = `source-curated-person-knowledge-gap`
- 规则：AI 不作为数据源；每条补充 Person 均含真实 `source_reference` 与 `source_id` 溯源。
