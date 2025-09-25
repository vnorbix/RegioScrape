from pathlib import Path

from filter import load_filter_data


def test_load_filter_data():
    article_filter = load_filter_data(Path(__file__).parent / "Bburago_termekek.xlsx")

    assert article_filter.categories == {"Autó, jármű"}
    assert len(article_filter.article_numbers) == 130
    assert "12171" in article_filter.article_numbers
    assert "01677" in article_filter.article_numbers
