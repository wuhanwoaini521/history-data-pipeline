# CRITICAL_EVENT_PERSON_LINKING_REVIEW

- Scope = **62** Critical Events（V1 frozen）
- Candidate（含 unlinked 决策回顾）: **150**
- Unique Raw Person Names: **134**
- Resolved exact: **89**
- Resolved high_confidence: **21**
- Ambiguous: **6**（未进入 EventPerson）
- Not Found: **34**（未伪造 Person）
- Rejected: **0**
- Accepted EventPerson Count: **110**
- Events With Accepted Person: **54**
- Events Without Person: **8**（event-jiuyiba-shibian、event-nanjing-datusha、event-qiqishi-bian、event-riben-touxiang、event-shangtang-miexia、event-xian-shibian、event-xijin-mie-wang、event-xinzhongguo-chengli）
- Existing Links Audited: 58（legacy；不在 critical 上，身份核对通过，无需 recheck）
- Existing Links Correct: 58
- Existing Links Needs Recheck: 0 / Rejected: 0
- Top Duplicate Names（跨事件同人）: 朱元璋(3)；刘秀(2)；嬴政(2)；吴三桂(2)；武则天(2)；杨坚(2)；唐高祖(2)；李世民(2)
- Ambiguous Names: 6 → 梁武帝@event-houjing-zhi-luan；王濬@event-jin-mie-wu；孙武@event-wuchang-qiyi；晋愍帝@event-xijin-mie-wang；刘曜@event-xijin-mie-wang；晋愍帝@event-yongjia-zhi-luan
- Knowledge Store Gaps（not_found）: 34

## 质量指标（§62）
- wrong_accepted_links = **0**
- accepted_links_with_provenance = **100%**（identity/event evidence 在 store 与 accepted review）
- accepted_person_ids_resolve = **100%**（110/110）
- accepted_event_ids_resolve = **100%**（54/54）

## 人员粒度（§44）
- per-event accepted: min=1, max=4, avg=2.04, median=2
（全部 ≤4，远低于 15 上限，无需 Granularity Review）