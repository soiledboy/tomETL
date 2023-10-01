# internal modules
from ariadne import (
    load_schema_from_path,
    make_executable_schema,
    graphql_sync,
    snake_case_fallback_resolvers,
    ObjectType,
    QueryType,
)
from loguru import logger
from typing import List, Dict, Tuple

# external modules
from backend.queries import Queries, GroupQueries
from backend.models import Group, Product, DailyPrice
from backend.fake_data import (
    gen_ts_data,
    convert_time_period_to_days,
    gen_top_gainers,
    gen_top_losers,
)


## multi card resolvers


def resolve_cards(obj, info) -> Dict:
    pagination_default_limit = 25
    try:
        cards = [x.to_dict() for x in Product.query.limit(pagination_default_limit)]
        res = dict(success=True, cards=cards)
    except Exception as e:
        res = dict(success=False, errors=[str(e)])
    return res


### single card resolvers


def resolve_card_by_id(obj, info, _id: int) -> Dict:
    try:
        card = Product.find(_id)
        res = dict(success=True, card=card.to_dict())
    except Exception as e:
        res = dict(success=False, errors=[str(e)])
    return res


def resolve_card_by_name(obj, info, name: str) -> Dict:
    try:
        card = Prodcut.get_by_name(name)
        res = dict(success=True, card=card.to_dict())
    except Exception as e:
        res = dict(success=False, errors=[str(e)])
    return res


def resolve_card_by_name_with_prices(obj, info, name: str, duration: int = 7) -> Dict:
    try:
        card = Product.get_by_name(name)
        card_dict = card.to_dict()
        card_dict["prices"] = DailyPrice.price_values_for_card(card)
        res = dict(success=True, card=card_dict)
    except Exception as e:
        res = dict(success=False, errors=[str(e)])
    return res


def __gen_series(name, tp):
    days = convert_time_period_to_days(tp)
    values = gen_ts_data(days)
    element = dict(name=name, timePeriod=tp, values=values)
    return element


def resolve_time_series(obj, info, name: str, timePeriod: str = "1m") -> Dict:
    try:
        res = __gen_series(name, timePeriod)
    except Exception as e:
        res = dict(errors=[str(e)])
    return res


def resolve_time_series_collection(
    obj, info, names: List[str], timePeriod: str = "1m"
) -> Dict:
    try:
        return dict(collection=[__gen_series(name, timePeriod) for name in names])
    except Exception as e:
        res = dict(errors=[str(e)])
    return res


def resolve_time_series_collection_by_ids(
    obj, info, ids: List[id], timePeriod: str = "1m"
) -> Dict:
    try:
        return dict(collection=[__gen_series(str(_id), timePeriod) for _id in ids])
    except Exception as e:
        res = dict(errors=[str(e)])
    return res


def resolve_top_gainers(obj, info, timePeriod: str = "1m", count: int = 10) -> Dict:
    try:
        cards = gen_top_gainers(timePeriod, count)
        return dict(name="topGainers", timePeriod=timePeriod, count=count, cards=cards)
    except Exception as e:
        res = dict(errors=[str(e)])
    return res


def resolve_top_losers(obj, info, timePeriod: str = "1m", count: int = 10) -> Dict:
    try:
        cards = gen_top_losers(timePeriod, count)
        return dict(name="topLosers", timePeriod=timePeriod, count=count, cards=cards)
    except Exception as e:
        res = dict(errors=[str(e)])
    return res


def resolve_indexes(obj, info, name: str = "") -> Dict:
    try:
        query = CardSet.query.limit(100).all()
        card_sets = [x for x in query]
        indexes = [dict(name=x.set_sku, id=x.id) for x in card_sets]
        return dict(success=True, indexes=indexes)
    except Exception as e:
        return dict(success=False, errors=str(e))


def resolve_cardSetPricesByIds(obj, info, ids, timePeriod) -> Dict:
    try:
        cardSets = []
        for id in ids:
            card_set = CardSet.query.get(id)
            card_set_dict = dict(
                id=card_set.id,
                name=card_set.set_sku,
                setSku=card_set.set_sku,
                dateValues=CardSetQueries.mid_price_by_date(card_set.id),
            )
            cardSets.append(card_set_dict)
        return dict(success=True, cardSets=cardSets)
    except Exception as e:
        return dict(success=False, errors=str(e))


query = ObjectType("Query")
mutation = ObjectType("Mutation")

query.set_field("cardsAll", resolve_cards)
query.set_field("cardById", resolve_card_by_id)
query.set_field("cardByName", resolve_card_by_name)
query.set_field("cardByNameWithPrices", resolve_card_by_name_with_prices)
query.set_field("timeSeries", resolve_time_series)
query.set_field("timeSeriesCollection", resolve_time_series_collection)
query.set_field("timeSeriesCollectionByIds", resolve_time_series_collection_by_ids)
query.set_field("topGainers", resolve_top_gainers)
query.set_field("topLosers", resolve_top_losers)
query.set_field("indexes", resolve_indexes)
query.set_field("cardSetPricesByIds", resolve_cardSetPricesByIds)

type_defs = load_schema_from_path("backend/schema.graphql")
schema = make_executable_schema(type_defs, query, mutation)
