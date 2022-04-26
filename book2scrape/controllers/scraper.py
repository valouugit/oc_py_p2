from bs4 import BeautifulSoup, ResultSet
import requests, os
from ..models.category import Category
from ..models.book import Book
from typing import List, Optional

class Scraper:
    """Class for data scraping"""
    
    def getAllCategories(self) -> List[Category]:
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
                ),
                books=[]
            ))

        return categories
    
    def getAllBooksInCategory(self, category : Category):
        """Scraping all book on category"""
        scrape = self._scrapeBooksInOnePage(caterogy_url=category.url)
        self._addingBookInCategory(category=category, books_html=scrape["books_html"])
        while scrape["next_page"]:
            scrape = self._scrapeBooksInOnePage(caterogy_url=category.url, next_page=scrape["next_page"])
            self._addingBookInCategory(category=category, books_html=scrape["books_html"])

    def _addingBookInCategory(self, category : Category, books_html : List[ResultSet]):
        for book in books_html:
            category.books.append(
                Book(
                    product_page_url=book\
                        .a["href"]\
                        .replace("../../..", "http://books.toscrape.com/catalogue")
                        .rstrip("/index.html"),
                    category=category.name
                )
            )

    def _scrapeBooksInOnePage(self, caterogy_url : str, next_page : str = "") -> dict:
        """Get html content for category page"""
        res = requests.get("%s%s" % (caterogy_url.rstrip("index.html"), next_page))
        content = BeautifulSoup(res.content, "html.parser")
        next_page = self._getNextPageUrl(content)
        books_html = content.ol.find_all("article")
        return {
            "books_html": books_html,
            "next_page": next_page
        }
    
    def _getNextPageUrl(self, html) -> Optional[str]:
        """Check if next button is present"""
        return html.find(class_="next").a["href"] if html.find(class_="next") else None
        
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
        
    def downloadBookImg(self, book : Book):
        """Download book's image"""
        dir = "library/Image/%s" % book.category
        if not os.path.exists(dir):
            os.makedirs(dir)
        filename = "%s/%s.jpg" % (dir, book.title.replace("/", ""))
        if not os.path.exists(filename):
            res = requests.get(book.image_url, stream=True)
            with open(filename, 'wb') as img:
                for buf in res.iter_content(1024):
                    img.write(buf)