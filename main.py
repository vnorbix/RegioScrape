import logging
from pathlib import Path
from regio_scrape import scrape_products
import argparse

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(message)s")
parser = argparse.ArgumentParser()
parser.add_argument("xlsx_file", help="regioscrape file to process", type=Path)
args = parser.parse_args()
scrape_products(args.xlsx_file)
