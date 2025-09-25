from pathlib import Path

from category import parse_categories, Category, parse_products, ProductListItem


def test_parse_categories():
    page_content = (Path(__file__).parent / "categories_page.html").read_text()

    categories = parse_categories(page_content)

    assert len(categories) == 27
    assert categories[0] == Category(name='Ajándék', url='/kat-59-ajandek.html', id='59', name_hash="ajandek")



def test_parse_products():
    page_content = (Path(__file__).parent / "product_list_page.html").read_text()
    products_page = parse_products(page_content)
    assert len(products_page.products) == 30
    assert products_page.products[0] == ProductListItem(
        url='https://www.regiojatek.hu/termek-08784-csillogo-unikornis-vegyes-penztarca.html',
        name='Csillogó unikornis +vegyes pénztárca',
        article_number='08784'
    )

