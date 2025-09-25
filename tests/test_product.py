from pathlib import Path

from product import parse_product, Product


def test_parse_product():
    page_content = (Path(__file__).parent / "product_page.html").read_text()
    assert parse_product(page_content) == Product(article_number='39309',
        description='&lt;p&gt;Bburago gyártmányú 1/50 méretarányú magyar '
                    'mentőautó modell, amely az Országos Mentőszolgálat '
                    'engedélyével készült. A modell a 2013-ban forgalomban '
                    'lévő VW cratfer esetkocsik eredeti licence alapján '
                    'készült. Az autó mellé elsősegély-könyvjelzőt is '
                    'csomagoltunk a jövő életmentőinek.&lt;/p&gt;\n'
                    'Méretek: 12 x 5 x 5 cm.',
        images=['https://www.regiojatek.hu/data/regio_images/normal2/39309_0.jpg',
                'https://www.regiojatek.hu/data/regio_images/normal2/39309_1.jpg',
                'https://www.regiojatek.hu/data/regio_images/normal2/39309_2.jpg',
                'https://www.regiojatek.hu/data/regio_images/normal2/39309_3.jpg',
                'https://www.youtube.com/watch?v=gm0URNlR4yM',
                'https://www.youtube.com/watch?v=7WSLvJ5Yd7Q'],
        age_min=3,
        age_max=6,
        gender='fiú')