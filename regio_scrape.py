from __future__ import annotations

import logging
import random
import time
from pathlib import Path
from typing import Generator

import requests

from filter import load_filter_data, ArticleFilter
from output import save_products
from category import parse_categories, parse_products, filter_category, filter_product_list_items
from product import Product, parse_product
from utils.http import COMMON_HTTP_HEADERS

logger = logging.getLogger(__name__)

BASE_URL = "https://www.regiojatek.hu"
CATEGORIES_URL = "/kategoriak.html"
MAX_PRODUCTS_PER_PAGE = 30



def _fetch_page(url: str) -> str:
    response = requests.get(url, headers=COMMON_HTTP_HEADERS)
    response.raise_for_status()
    time.sleep(random.uniform(1, 2))
    return response.text


def download_products(article_filter: ArticleFilter) -> Generator[Product, None, None]:
    logger.info("Kategóriák letöltése")
    categories = parse_categories(_fetch_page(f"{BASE_URL}{CATEGORIES_URL}"))
    logger.info("%d kategória linket találtam", len(categories))
    is_last_page = False
    for category in filter_category(categories, article_filter.categories):
        next_category_page_url = f"{BASE_URL}{category.url}"
        page_count = 1
        while True:
            logger.info("'%s' kategória %d. oldal letöltése", category.name, page_count)
            product_list = parse_products(_fetch_page(next_category_page_url))
            if len(product_list.products) == 0 or is_last_page:
                logger.info("Elértem az utolsó oldalt a '%s' kategóriában", category.name)
                break
            if len(product_list.products) != MAX_PRODUCTS_PER_PAGE:
                # Last page has probably less elements than max, so it's a safe mechanism to stop the loop
                # when the same number of elements returned every time
                is_last_page = True
            logger.info("%d terméket találtam a kategória oldalon", len(product_list.products))
            for product_count, product in enumerate(
                    filter_product_list_items(product_list.products, article_filter.article_numbers), start=1):
                logger.info("'%s' termék letöltése, %d. az oldalon", product.name, product_count)
                yield parse_product(_fetch_page(product.url))
            page_count += 1
            next_category_page_url = f"{BASE_URL}/index.php?action=webstore&ws_action=view_cat&category_id={category.id}&name_hash={category.name_hash}&pg={page_count}&fragment="
    logger.info("Az összes kategória oldalról letöltöttem a termékekeket")


def scrape_products(product_file: Path):
    article_filter = load_filter_data(product_file)
    logger.info(f"Szűrés %d db termékre cikkszám alapján", len(article_filter.article_numbers))
    products = list(download_products(article_filter))
    save_products(product_file, products)





