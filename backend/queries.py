# external modules
from loguru import logger
from sqlalchemy import sql
from typing import List, Dict

# internal modules
from backend.extensions import db


def execute_get_all_results(query, params) -> List[Dict]:
    with db.engine.connect() as con:
        res = con.execute(query, **params).fetchall()
        results = [dict(row) for row in res]
        return results


class Queries:
    @staticmethod
    def market_value(db, params: Dict) -> List[Dict]:
        """
        params:
            - duration
        """
        query = sql.text(
            """
            SELECT
                date(date) AS date
                , sum(market) AS sum_market
            FROM daily_prices
            GROUP BY date(date)
            """
        )
        _params = dict(duration=params["duration"])
        return execute_get_all_results(query, _params)


class GroupQueries:
    @staticmethod
    def mid_price_by_date(group_id: int) -> List[Dict]:
        query = sql.text(
            """
            WITH cards_within_set_date_and_mid AS (
                select 
                    date_format(dp.date, "%Y-%m-%d") as date
                    , dp.mid
                from products as p
                join product_groups as pg on pgs.product_id = p.id
                join groups as g on g.id = pg.group_id
                join prices on prices.product_id = p.id
                where
                    g.id = :group_id
            )

            SELECT 
                x.date AS date
                , sum(x.mid) AS value
            FROM cards_within_set_date_and_mid AS x
            GROUP BY x.date
            ORDER BY x.date
            """
        )
        params = dict(group_id=group_id)
        return execute_get_all_results(query, params)
