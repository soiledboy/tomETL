from datetime import date, timedelta, datetime
from faker import Faker
import random
from typing import List, Dict


fake = Faker()


def convert_time_period_to_days(tp: str) -> int:
    if tp == "1m":
        return 30
    if tp == "3m":
        return 120
    if tp == "12m":
        return 365
    return 30


def gen_ts_data(max_days):
    result = []
    now = datetime.now().replace(microsecond=0)
    for i in range(max_days, 0, -1):
        x = (now - timedelta(days=i)).isoformat()
        result.append({"date": x, "value": random.random()})
    return result


def gen_gls(t: str, count: int) -> List[Dict]:
    array = []
    for i in range(0, count):
        name = f"Product #{i}"
        value = ((random.random() * random.random()) * 10.0) - 2
        array.append(dict(name=name, value=value))
    return array


def gen_top_gainers(tp: str, count: int) -> List[Dict]:
    return gen_gls("gainers", count)


def gen_top_losers(tp: str, count: int) -> List[Dict]:
    return gen_gls("losers", count)
