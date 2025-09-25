import logging
import re
from dataclasses import dataclass

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


@dataclass
class Category:
    name: str
    url: str
    id: str
    name_hash: str


@dataclass
class ProductListItem:
    url: str
    name: str
    article_number: str

@dataclass
class ProductsPage:
    products: list[ProductListItem]


def parse_categories(page_content: str) -> list[Category]:
    soup = BeautifulSoup(page_content, "html.parser")
    return [
        Category(
            name=tag.text, url=tag.get('href'), id=re.match(r"/kat-(\d+)-", tag.get('href')).group(1),
            name_hash=re.match(r"/kat-\d+-(.*)\.html", tag.get('href')).group(1).replace("_", "-")
        )
        for tag in soup.find("div", class_="teaser-categories").find_all("a")
        if tag.get('href') is not None and tag.get('href').startswith("/kat")
    ]

def filter_category(categories: list[Category], filter_categories: set[str]) -> list[Category]:
    logger.info(f"Szűrés '%s' kategóriákra", filter_categories)
    return list(filter(lambda category: category.name in filter_categories, categories))


def filter_product_list_items(products: list[ProductListItem], filtered_article_numbers: set[str]) -> list[ProductListItem]:
    return list(filter(lambda product: product.article_number in filtered_article_numbers, products))

def parse_products(page_content: str) -> ProductsPage:
    soup = BeautifulSoup(page_content, "html.parser")
    return ProductsPage(
        products=[
            ProductListItem(
                url=product_tag.a.get("href"),
                name=product_tag.a.get("title"),
                article_number=product_tag.find(class_="d-block").get("data-cart-product-no")
            )
            for product_tag in soup.find_all(class_="product-item")
        ],
    )
