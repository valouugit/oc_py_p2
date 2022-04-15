from bs4 import BeautifulSoup
import requests
from ..models.category import Category
from ..models.book import Book

class Scraper:
    
    def __init__(self) -> None:
        pass
    
    def getAllCategories(self) -> list[Category]:
        res = requests.get("http://books.toscrape.com")
        html = BeautifulSoup(res.content, "html.parser")
        html = html.find_all("ul")[1].find("ul")
        categories = []
        for cat in html.find_all("li"):
            categories.append(Category(
                name=cat.a.string.replace(" ", "").replace("\n", ""),
                url="%s%s" % (
                    "http://books.toscrape.com/",
                    cat.a["href"]
                )
            ))

        return categories
    
    def getAllBookInCategory(self,
                             category : Category,
                             next : str = "",
                             books : list = []) -> list[Book]:
        res = requests.get("%s%s" % (category.url.rstrip("index.html"), next))
        html = BeautifulSoup(res.content, "html.parser")
        next = self.checkNextPage(html)
        html = html.ol.find_all("article")
        for book in html:
            books.append(
                Book(
                    product_page_url=book\
                        .a["href"]\
                        .replace("../../..", "http://books.toscrape.com/catalogue")
                        .rstrip("/index.html"),
                    category=category.name
                )
            )
        
        if next != None:
            self.getAllBookInCategory(category=category, next=next, books=books)
        
        return books
    
    def checkNextPage(self, html) -> str or None:
        if html.find(class_="next") != None:
            return html.find(class_="next").a["href"]