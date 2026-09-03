"""Reference Resolution：Backbone 引用 → Knowledge Store 实体解析。

规则（第十八、二十节）：
- Event 只允许引用 knowledge.person.id / knowledge.place.id /
  knowledge.historical_text.id；
- 无法确认时保留 name_raw + id=null + link_status=needs_linking；
- 错误链接比 NULL 更严重：link_status=linked 但实体不存在 → broken，
  必须阻断 build。

curated seeds：迁移自 legacy Semantic Layer QA 的 canonical identity 作为
知识库最小种子（例如 cbdb-person-30257=曹操）。正式 Knowledge Store 由
Layer 1/2 构建时以同样 ID 重建并取代种子。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .loader import Backbone

# legacy QA 确认的 canonical 简体名（迁移依据，来自 semantic_layer.CURATED_PERSON_NAMES）
CANONICAL_PERSON_NAMES: dict[str, str] = {
    "cbdb-person-16622": "刘邦",
    "cbdb-person-22437": "韩信",
    "ctext-person-664414": "彭越",
    "ctext-person-933340": "英布",
    "cbdb-person-30257": "曹操",
    "cbdb-person-135353": "刘备",
    "cbdb-person-20609": "孙权",
    "cbdb-person-135152": "袁绍",
    "cbdb-person-25403": "诸葛亮",
    "ctext-person-817615": "周瑜",
    "cbdb-person-19244": "李隆基（唐玄宗）",
    "cbdb-person-379873": "安禄山",
    "cbdb-person-32814": "史思明",
    "cbdb-person-31221": "杨国忠",
    "cbdb-person-94373": "郭子仪",
    "cbdb-person-146097": "李光弼",
    "ctext-person-62031": "唐肃宗",
    "curated-person-fan-zeng": "范增",
}


@dataclass
class ResolutionResult:
    knowledge_available: bool
    knowledge_db: Path | None = None
    persons: dict[str, int] = field(default_factory=dict)
    places: dict[str, int] = field(default_factory=dict)
    evidences: dict[str, int] = field(default_factory=dict)
    broken: list[str] = field(default_factory=list)
    pending: list[str] = field(default_factory=list)
    seed_persons: dict[str, str] = field(default_factory=dict)
    seed_places: dict[str, str] = field(default_factory=dict)


class KnowledgeResolver:
    def __init__(self, knowledge_db: Path | None = None):
        self.knowledge_db = knowledge_db
        self.person_ids: set[str] = set()
        self.place_ids: set[str] = set()
        self.text_ids: set[str] = set()

    def _load_from_db(self) -> None:
        if not self.knowledge_db or not self.knowledge_db.exists():
            return
        try:
            import duckdb
        except ImportError:  # pragma: no cover
            return
        with duckdb.connect(str(self.knowledge_db), read_only=True) as connection:
            for table, target in (("people", "person_ids"), ("places", "place_ids"), ("historical_texts", "text_ids")):
                try:
                    rows = connection.execute(f"SELECT id FROM {table}").fetchall()
                    getattr(self, target).update(str(row[0]) for row in rows)
                except Exception:
                    pass

    @property
    def available(self) -> bool:
        return bool(self.person_ids or self.place_ids or self.text_ids)


def _seed_place_ids(backbone: Backbone) -> dict[str, str]:
    seeds: dict[str, str] = {}
    for event in backbone.events:
        for place in event.get("places", []):
            identifier = place.get("place_id")
            if identifier and not place.get("link_status") == "needs_linking":
                seeds.setdefault(identifier, place.get("place_name_raw") or identifier)
    return seeds


def resolve_references(backbone: Backbone, knowledge_db: Path | None = None) -> ResolutionResult:
    """解析全部事件引用；broken（linked 但实体缺失）必须阻断 build。"""
    resolver = KnowledgeResolver(knowledge_db)
    resolver._load_from_db()

    result = ResolutionResult(
        knowledge_available=resolver.available,
        knowledge_db=knowledge_db,
        seed_persons=dict(CANONICAL_PERSON_NAMES),
        seed_places=_seed_place_ids(backbone),
    )

    persons = {"linked": 0, "needs_linking": 0, "pending_knowledge": 0, "rejected": 0}
    places = {"linked": 0, "needs_linking": 0, "pending_knowledge": 0, "rejected": 0}
    evidences = {"linked": 0, "needs_linking": 0, "pending_knowledge": 0, "rejected": 0}

    for event in backbone.events:
        for person in event.get("people", []):
            status = person.get("link_status", "needs_linking")
            identifier = person.get("person_id")
            if status == "linked":
                exist = identifier in resolver.person_ids or identifier in result.seed_persons
                if identifier and exist:
                    persons["linked"] += 1
                else:
                    result.broken.append(f"events/{event['id']}: linked person 引用缺失 {identifier}（knowledge 不可用且非 curated seed）")
            elif status in persons:
                persons[status] += 1
            elif status is None:
                persons["needs_linking"] += 1
                result.pending.append(f"events/{event['id']}: person 未设置 link_status")
            else:
                result.pending.append(f"events/{event['id']}: person link_status={status!r}")
        for place in event.get("places", []):
            status = place.get("link_status", "needs_linking")
            identifier = place.get("place_id")
            if status == "linked":
                exist = identifier in resolver.place_ids or identifier in result.seed_places
                if identifier and exist:
                    places["linked"] += 1
                else:
                    result.broken.append(f"events/{event['id']}: linked place 引用缺失 {identifier}")
            elif status in places:
                places[status] += 1
            elif status is None:
                places["needs_linking"] += 1
                result.pending.append(f"events/{event['id']}: place 未设置 link_status")
            else:
                result.pending.append(f"events/{event['id']}: place link_status={status!r}")
        for evidence in event.get("evidence", []):
            status = evidence.get("link_status", "pending_knowledge")
            identifier = evidence.get("historical_text_id")
            if status == "linked":
                if identifier and identifier in resolver.text_ids:
                    evidences["linked"] += 1
                else:
                    result.broken.append(f"events/{event['id']}: linked evidence 文本缺失 {identifier}")
            elif status in evidences:
                evidences[status] += 1
            elif status is None:
                evidences["pending_knowledge"] += 1
                result.pending.append(f"events/{event['id']}: evidence 未设置 link_status")
            else:
                result.pending.append(f"events/{event['id']}: evidence link_status={status!r}")

    result.persons = persons
    result.places = places
    result.evidences = evidences
    return result


def knowledge_seed_rows(result: ResolutionResult) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    """从解析结果生成知识库种子行（people / places / works）。"""
    people: list[dict[str, Any]] = []
    for person_id, name in sorted(result.seed_persons.items()):
        people.append({
            "id": person_id, "canonical_name_zh_cn": name, "name_raw": name,
            "quality_status": "reviewed", "created_from_source": "source-curated-backbone-v1",
            "search_name": name, "search_aliases": "", "search_text": name,
        })
    places: list[dict[str, Any]] = []
    for place_id, name in sorted(result.seed_places.items()):
        places.append({
            "id": place_id, "canonical_name_zh_cn": name, "historical_name": name,
            "place_type": "historical_place", "source_id": "source-curated-backbone-v1",
            "external_id": place_id, "quality_status": "reviewed",
        })
    works: list[dict[str, Any]] = [
        {"id": "work-curated-shiji", "title": "史记", "title_raw": "史记", "title_zh_cn": "史记", "source_id": "source-curated-backbone-v1", "quality_status": "reviewed"},
        {"id": "work-curated-hanshu", "title": "汉书", "title_raw": "汉书", "title_zh_cn": "汉书", "source_id": "source-curated-backbone-v1", "quality_status": "reviewed"},
        {"id": "work-curated-houhanshu", "title": "后汉书", "title_raw": "后汉书", "title_zh_cn": "后汉书", "source_id": "source-curated-backbone-v1", "quality_status": "reviewed"},
        {"id": "work-curated-sanguozhi", "title": "三国志", "title_raw": "三国志", "title_zh_cn": "三国志", "source_id": "source-curated-backbone-v1", "quality_status": "reviewed"},
        {"id": "work-curated-zizhitongjian", "title": "资治通鉴", "title_raw": "资治通鉴", "title_zh_cn": "资治通鉴", "source_id": "source-curated-backbone-v1", "quality_status": "reviewed"},
        {"id": "work-curated-jiutangshu", "title": "旧唐书", "title_raw": "旧唐书", "title_zh_cn": "旧唐书", "source_id": "source-curated-backbone-v1", "quality_status": "reviewed"},
        {"id": "work-curated-xintangshu", "title": "新唐书", "title_raw": "新唐书", "title_zh_cn": "新唐书", "source_id": "source-curated-backbone-v1", "quality_status": "reviewed"},
        # ---- China History Backbone V1 · Batch 1：先秦 works seeds ----
        {"id": "work-curated-chunqiu", "title": "春秋", "title_raw": "春秋", "title_zh_cn": "春秋", "source_id": "source-curated-backbone-v1", "quality_status": "reviewed"},
        {"id": "work-curated-zuozhuan", "title": "左传", "title_raw": "左传", "title_zh_cn": "左传", "source_id": "source-curated-backbone-v1", "quality_status": "reviewed"},
        {"id": "work-curated-guoyu", "title": "国语", "title_raw": "国语", "title_zh_cn": "国语", "source_id": "source-curated-backbone-v1", "quality_status": "reviewed"},
        {"id": "work-curated-shangshu", "title": "尚书", "title_raw": "尚书", "title_zh_cn": "尚书", "source_id": "source-curated-backbone-v1", "quality_status": "reviewed"},
        {"id": "work-curated-zhushu-jinian", "title": "竹书纪年", "title_raw": "竹书纪年", "title_zh_cn": "竹书纪年", "source_id": "source-curated-backbone-v1", "quality_status": "reviewed"},
        {"id": "work-curated-zhanguoce", "title": "战国策", "title_raw": "战国策", "title_zh_cn": "战国策", "source_id": "source-curated-backbone-v1", "quality_status": "reviewed"},
        # ---- China History Backbone V1 · Batch 3：魏晋南北朝 works seeds ----
        {"id": "work-curated-jinshu", "title": "晋书", "title_raw": "晋书", "title_zh_cn": "晋书", "source_id": "source-curated-backbone-v1", "quality_status": "reviewed"},
        {"id": "work-curated-songshu", "title": "宋书", "title_raw": "宋书", "title_zh_cn": "宋书", "source_id": "source-curated-backbone-v1", "quality_status": "reviewed"},
        {"id": "work-curated-liangshu", "title": "梁书", "title_raw": "梁书", "title_zh_cn": "梁书", "source_id": "source-curated-backbone-v1", "quality_status": "reviewed"},
        {"id": "work-curated-chenshu", "title": "陈书", "title_raw": "陈书", "title_zh_cn": "陈书", "source_id": "source-curated-backbone-v1", "quality_status": "reviewed"},
        {"id": "work-curated-weishu", "title": "魏书", "title_raw": "魏书", "title_zh_cn": "魏书", "source_id": "source-curated-backbone-v1", "quality_status": "reviewed"},
        {"id": "work-curated-beiqishu", "title": "北齐书", "title_raw": "北齐书", "title_zh_cn": "北齐书", "source_id": "source-curated-backbone-v1", "quality_status": "reviewed"},
        {"id": "work-curated-zhoushu", "title": "周书", "title_raw": "周书", "title_zh_cn": "周书", "source_id": "source-curated-backbone-v1", "quality_status": "reviewed"},
        {"id": "work-curated-nanshi", "title": "南史", "title_raw": "南史", "title_zh_cn": "南史", "source_id": "source-curated-backbone-v1", "quality_status": "reviewed"},
        {"id": "work-curated-beishi", "title": "北史", "title_raw": "北史", "title_zh_cn": "北史", "source_id": "source-curated-backbone-v1", "quality_status": "reviewed"},
        {"id": "work-curated-suishu", "title": "隋书", "title_raw": "隋书", "title_zh_cn": "隋书", "source_id": "source-curated-backbone-v1", "quality_status": "reviewed"},
        # ---- China History Backbone V1 · Batch 4：五代/辽 works seeds ----
        {"id": "work-curated-jiuwudaishi", "title": "旧五代史", "title_raw": "旧五代史", "title_zh_cn": "旧五代史", "source_id": "source-curated-backbone-v1", "quality_status": "reviewed"},
        {"id": "work-curated-xinwudaishi", "title": "新五代史", "title_raw": "新五代史", "title_zh_cn": "新五代史", "source_id": "source-curated-backbone-v1", "quality_status": "reviewed"},
        {"id": "work-curated-liaoshi", "title": "辽史", "title_raw": "辽史", "title_zh_cn": "辽史", "source_id": "source-curated-backbone-v1", "quality_status": "reviewed"},
        # ---- China History Backbone V1 · Batch 5：宋辽夏金/元 works seeds ----
        {"id": "work-curated-songshi", "title": "宋史", "title_raw": "宋史", "title_zh_cn": "宋史", "source_id": "source-curated-backbone-v1", "quality_status": "reviewed"},
        {"id": "work-curated-jinshi", "title": "金史", "title_raw": "金史", "title_zh_cn": "金史", "source_id": "source-curated-backbone-v1", "quality_status": "reviewed"},
        {"id": "work-curated-xuzizhitongjianchangbian", "title": "续资治通鉴长编", "title_raw": "续资治通鉴长编", "title_zh_cn": "续资治通鉴长编", "source_id": "source-curated-backbone-v1", "quality_status": "reviewed"},
        {"id": "work-curated-yuanshi", "title": "元史", "title_raw": "元史", "title_zh_cn": "元史", "source_id": "source-curated-backbone-v1", "quality_status": "reviewed"},
        # ---- China History Backbone V1 · Batch 6：明 works seeds ----
        {"id": "work-curated-mingshi", "title": "明史", "title_raw": "明史", "title_zh_cn": "明史", "source_id": "source-curated-backbone-v1", "quality_status": "reviewed"},
        {"id": "work-curated-mingshilu", "title": "明实录", "title_raw": "明实录", "title_zh_cn": "明实录（校勘本）", "source_id": "source-curated-backbone-v1", "quality_status": "reviewed"},
    ]
    return people, places, works