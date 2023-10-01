from bs4 import BeautifulSoup
import csv
import json
from loguru import logger
import requests
from tqdm import tqdm
import traceback

from backend.app import create_app
from backend.extensions import db
from backend.models import Product, DailyPrice
from backend.settings import TCG_API_BEARER_KEY
from backend.jobs.tcg_api_util import generate_new_token

TCG_API_VERSION = "v1.39.0"

configs = {"access_token": ""}

def fetch_data_by_product_id(product_id):
    url = f"http://api.tcgplayer.com/{TCG_API_VERSION}/pricing/product/{product_id}"
    headers = {"Authorization": f"bearer {configs['access_token']}"}
    response = requests.get(url, headers=headers)
    json_data = response.json()
    return json_data["results"]


def select_non_empty_rows(rows):
    return list(filter(lambda x: x["lowPrice"] != None and x["midPrice"] != None, rows))


def daily_price_factory(row, product_id) -> DailyPrice:
    return DailyPrice(
        product_id=product_id,
        sub_type=row["subTypeName"],
        low=row["lowPrice"],
        mid=row["midPrice"],
        high=row["highPrice"],
        market=row["marketPrice"],
    )


def fetch_and_persist_by_product(product_id: int) -> None:
    product = Product.query.get(product_id)

    data = fetch_data_by_product_id(product.product_id)

    # if len(select_non_empty_rows(data)) > 1:
    # import pdb
    # pdb.set_trace()
    # logger.info(f"Number of rows = {len(select_non_empty_rows(data))}")

    for row in select_non_empty_rows(data):
        dp = daily_price_factory(row, product.id)
        db.session.add(dp)
    db.session.commit()


def run():
    app = create_app()

    configs["access_token"] = generate_new_token()

    with app.app_context():
        product_ids = [x.id for x in Product.query.all()]
        for product_id in tqdm(product_ids):
            fetch_and_persist_by_product(product_id)
