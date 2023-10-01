# external imports
import time
from time import sleep
from random import randint
import requests
from bs4 import BeautifulSoup
import pandas as pd
from os import environ
from loguru import logger
from typing import Dict, List

# internal imports
from backend.app import create_app
from backend.extensions import db
from backend.models import Product, DailyPrice
from backend.jobs.tcg_api_util import generate_new_token

ACCESS_TOKEN = ""

MAX_REQUESTS = 1  # 3_000
SPACE_CHAR = " "


def gen_urls():
    # @TODO change view to grid instead of list. This displays 2x the number of cards. The HTML scraping logic will need to be adjusted.
    return [
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Main+Deck+Monster&Rarity=Common+%2f+Short+Print&newSearch=false&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Main+Deck+Monster&newSearch=false&Rarity=Super+Rare&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Main+Deck+Monster%20&newSearch=false&Rarity=Rare&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Main+Deck+Monster&newSearch=false&Rarity=Ultra+Rare&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Main+Deck+Monster&newSearch=false&Rarity=Secret+Rare&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Main+Deck+Monster&Rarity=Ultimate+Rare&newSearch=false&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Main+Deck+Monster&newSearch=false&Rarity=Starfoil+Rare&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Main+Deck+Monster&newSearch=false&Rarity=Gold+Rare&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Main+Deck+Monster&newSearch=false&Rarity=Mosaic+Rare&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Main+Deck+Monster&newSearch=false&Rarity=Gold+Secret+Rare&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Main+Deck+Monster&newSearch=false&Rarity=Shatterfoil+Rare&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Main+Deck+Monster&newSearch=false&Rarity=Prismatic+Secret+Rare&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Main+Deck+Monster&newSearch=false&Rarity=Ghost+Rare&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Main+Deck+Monster&newSearch=false&Rarity=Parallel+Rare&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Main+Deck+Monster&newSearch=false&Rarity=Platinum+Rare&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Main+Deck+Monster&newSearch=false&Rarity=Short+Print&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Main+Deck+Monster&newSearch=false&Rarity=Promo&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Main+Deck+Monster&newSearch=false&Rarity=Ghost%2fGold+Rare&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Spell&Rarity=Common+%2f+Short+Print&newSearch=false&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Spell&newSearch=false&Rarity=Super+Rare&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Spell%20&newSearch=false&Rarity=Rare&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Spell&newSearch=false&Rarity=Ultra+Rare&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Spell&newSearch=false&Rarity=Secret+Rare&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Spell&Rarity=Ultimate+Rare&newSearch=false&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Spell&newSearch=false&Rarity=Starfoil+Rare&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Spell&newSearch=false&Rarity=Gold+Rare&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Spell&newSearch=false&Rarity=Mosaic+Rare&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Spell&newSearch=false&Rarity=Gold+Secret+Rare&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Spell&newSearch=false&Rarity=Shatterfoil+Rare&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Spell&newSearch=false&Rarity=Prismatic+Secret+Rare&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Spell&newSearch=false&Rarity=Ghost+Rare&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Spell&newSearch=false&Rarity=Parallel+Rare&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Spell&newSearch=false&Rarity=Platinum+Rare&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Spell&newSearch=false&Rarity=Short+Print&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Spell&newSearch=false&Rarity=Promo&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Spell&newSearch=false&Rarity=Ghost%2fGold+Rare&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Trap&Rarity=Common+%2f+Short+Print&newSearch=false&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Trap&newSearch=false&Rarity=Super+Rare&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Trap%20&newSearch=false&Rarity=Rare&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Trap&newSearch=false&Rarity=Ultra+Rare&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Trap&newSearch=false&Rarity=Secret+Rare&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Trap&Rarity=Ultimate+Rare&newSearch=false&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Trap&newSearch=false&Rarity=Starfoil+Rare&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Trap&newSearch=false&Rarity=Gold+Rare&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Trap&newSearch=false&Rarity=Mosaic+Rare&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Trap&newSearch=false&Rarity=Gold+Secret+Rare&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Trap&newSearch=false&Rarity=Shatterfoil+Rare&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Trap&newSearch=false&Rarity=Prismatic+Secret+Rare&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Trap&newSearch=false&Rarity=Ghost+Rare&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Trap&newSearch=false&Rarity=Parallel+Rare&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Trap&newSearch=false&Rarity=Platinum+Rare&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Trap&newSearch=false&Rarity=Short+Print&orientation=list",
        "https://shop.tcgplayer.com/yugioh/product/show?advancedSearch=true&Price_Condition=Less+Than&Type=Cards&Card+Type=Trap&newSearch=false&Rarity=Ghost%2fGold+Rare&orientation=list",
    ]


def process_url(url):
    start_time = time.time()
    requests_count = 0

    headers = {"Accept-Language": "en-US, en;q=0.5"}

    # Declare the lists to store data in
    nameL = []
    setNumberL = []
    productIdL = []
    low1 = []
    mid1 = []
    high1 = []
    market1 = []
    lowU = []
    midU = []
    highU = []
    marketU = []
    quantity = []
    listingL = []

    # Select all page link data
    response = requests.get(url)
    html_soup = BeautifulSoup(response.text, "html.parser")
    pageNum = html_soup.find_all("a", class_="page-link")

    # Transform data type to str
    pageNum_str = str(pageNum)

    # Splice str to grab section with page number
    pageStr = pageNum_str[-20:-5]

    # Remove all non-numeric characters from splice
    pageStr = "".join(c for c in pageStr if c.isnumeric())

    # Check if int is '', if not set to number parsed
    if pageStr == "":
        pageStr = "1"
        pageint = int(pageStr)
    else:
        pageint = int(pageStr)

    # Create range for scraper to parse for each url
    pages = [str(i) for i in range(1, pageint + 1)]

    # For every page in the interval 1-10
    for page in pages:
        # Make a get request
        # set stream to true to  so that Requests cannot release the connection back to the pool unless you consume all the data or call Response.close

        response = requests.get(
            url + "&PageNumber=" + page, headers=headers, stream=True
        )

        # Pause the Loop
        sleep(randint(1, 5))

        # Monitor the requests
        requests_count += 1
        elapsed_time = time.time() - start_time
        logger.info(
            f"Request: {requests_count}; Frequency: {requests_count / elapsed_time} requests/s"
        )

        # Throw a warning for non-200 status codes
        if response.status_code != 200:
            logger.warning(
                f"Request: {requests_count}; Status code: {response.status_code}"
            )

        # Break the loop if the number of requests is greater than expected
        if requests_count > MAX_REQUESTS:
            logger.warning(f"Number of requests was greater than expected.")
            break

        # Parse the content of the request with BeautifulSoup
        page_html = BeautifulSoup(response.text, "html.parser")

        # Select all 10 of the card containers from a single page
        pd_containers = page_html.find_all("div", class_="product")

        # For every card of these 10
        for container in pd_containers:

            # If the card has no setNumber, then:
            if container.find("span", class_="product__extended-field") is not None:

                # Scrape the name
                name = container.find("a", class_="product__name").text
                nameL.append(name)

                # Scrape the setNumber
                setNumber = container.find(
                    "span", class_="product__extended-field"
                ).text
                setNumberL.append(setNumber)

                # Scrape the productId
                href = container.find("a", {"class": "product__price-guide btn"})
                hrefLink = href["href"]
                productIdChar = hrefLink[-6:]
                productId = productIdChar.replace("a", "")
                productIdL.append(productId)

                # Scrape the listing quantity
                if container.find("a", class_="product__offers-more-count") is not None:
                    listing = container.find(
                        "a", class_="product__offers-more-count"
                    ).text
                    listingNew = "".join(c for c in listing if c.isnumeric())
                    listingL.append(listingNew)

    df = pd.DataFrame(
        {
            "name": pd.Series(nameL),
            "set_number": pd.Series(setNumberL),
            "product_id": pd.Series(productIdL),
            "listings": pd.Series(listingL),
        }
    )

    return df


def daily_price_factory(row, product_id) -> DailyPrice:
    return DailyPrice(product_id=product_id, listings=int(row["listings"]))


def format_raw_set_number(set_number: str) -> str:
    return set_number.split(SPACE_CHAR)[1]


def format_raw_product_id(product_id: str) -> int:
    return int(product_id)


def get_product_id_by_product_id(row: Dict) -> int:
    product = Product.query.filter(Product.product_id == row["product_id"]).first()
    if product is None:
        product = Product(
            name=row["name"],
            number=format_raw_set_number(row["set_number"]),
            product_id=format_raw_product_id(row["product_id"]),
        )
        db.session.add(product)
        db.session.commit()

        # TODO(weston) associate with set (create set if it doesn't exist)

        logger.info(f"created new Product={product}")
    return product.id


def run():
    app = create_app()

    ACCESS_TOKEN = generate_new_token()

    with app.app_context():
        for url in gen_urls():
            df = process_url(url)
            for index, row in df.iterrows():
                product_id = get_product_id_by_product_id(row)
                dp = daily_price_factory(row, product_id)
                db.session.add(dp)
                db.session.commit()

            logger.debug(f"Finished url = {url}")
