from bs4 import BeautifulSoup
import requests
from ..models.category import Category
from ..models.book import Book

class Scraper:
    """Class for data scraping"""
    
    def __init__(self) -> None:
        pass
    
    def getAllCategories(self) -> list[Category]:
        """Scraping all categories from homepage"""
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
        """Scraping all book on category"""
        res = requests.get("%s%s" % (category.url.rstrip("index.html"), next))
        html = BeautifulSoup(res.content, "html.parser")
        next = self._checkNextPage(html)
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
    
    def _checkNextPage(self, html) -> str or None:
        """Check if next button is present"""
        if html.find(class_="next") != None:
            return html.find(class_="next").a["href"]
        
    def getBook(self, book : Book) -> None:
        """Scraping book data"""
        res = requests.get(book.product_page_url)
        html = BeautifulSoup(res.content, "html.parser")
        
        table = html.table.find_all("td")
        book.universal_product_code = table[0].string
        book.price_excluding_tax = table[2].string
        book.price_including_tax = table[3].string
        book.number_available = int(table[5]\
                                    .string\
                                    .split("(")[1]\
                                    .split(" ")[0])
        
        book.title = html.h1.string
        book.product_description = html.article.find_all("p")[3].string
        book.review_rating = html.article.find_all("p")[2]["class"][1]
        book.image_url = html.img["src"].replace(
            "../..", 
            "http://books.toscrape.com"
        )