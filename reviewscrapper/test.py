from pprint import pprint

from bs4 import BeautifulSoup
from pathlib import Path


with open(Path(__file__).parent / "parsed_files" / f"ikyu-review-p7.html", "r", encoding="UTF-8") as fp:
    soup = BeautifulSoup(fp, "lxml")


pprint(soup.find_all("li"))