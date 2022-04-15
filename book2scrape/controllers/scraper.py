from bs4 import BeautifulSoup
import requests
from ..models.category import Category

class Scraper:
    
    def __init__(self) -> None:
        pass
    
    def getAllCategories(self) -> list[Category]:
        res = requests.get("http://books.toscrape.com")
        html = BeautifulSoup(res.content, "html.parser")
        html = html.find_all("ul")[1].find("ul")
        categories = []
        for li in html.find_all("li"):
            categories.append(Category(
                name=li.a.string.replace(" ", "").replace("\n", ""),
                url="%s%s" % (
                    "http://books.toscrape.com/",
                    li.a["href"]
                )
            ))

        return categories