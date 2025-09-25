import json
from dataclasses import dataclass

from bs4 import BeautifulSoup


@dataclass
class Product:
    article_number: str
    description: str
    images: list[str]
    age_min: int
    age_max: int
    gender: str

def parse_product(page_content: str) -> Product:
    soup = BeautifulSoup(page_content, "html.parser")
    product_data = next(filter(
        lambda data: data["@type"] == "Product",
        (
            json.loads(tag.text, strict=False) for tag in soup.find_all("script", type="application/ld+json")
        )
    ))

    product = Product(
        article_number=product_data["sku"],
        description=product_data["description"],
        images=[tag.get("href") for tag in soup.find(id="gallery-links").find_all("a")],
        age_min=int(soup.find("input", attrs={"name": "product_age_min"}).get("value")),
        age_max=int(soup.find("input", attrs={"name": "product_age_max"}).get("value")),
        gender=soup.find("input", attrs={"name":"product_gender"}).get("value"),
    )
    return product
