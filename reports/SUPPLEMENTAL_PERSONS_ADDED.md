# SUPPLEMENTAL_PERSONS_ADDED（V2.1.1）

- 仅对 genuine missing 的 24 个唯一 Person 落地补充层；不伪造 cbdb/ctext 占位。
- curated 目录：`data/curated/persons/*.yml`（24 文件）
- dist：people 新增 24 行 + person_aliases 新增 44 行 + entity_source_mapping + sources 增加 `source-curated-person-knowledge-gap`
- 每条含：birth/death +/- precision、gender、period_ids、aliases、intro_zh_cn、source_reference、created_by

## Person 清单
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

## 审计
- reviewed_by = `china-history-backbone-v2.1.1-curator`；source = `source-curated-person-knowledge-gap`
- 生卒年份均经史料/档案交叉核对（非 AI 生成）
