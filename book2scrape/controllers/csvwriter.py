import csv
from ..models.book import Book

CSV_HEADER = [
    "product_page_url", 
    "universal_product_code",
    "title",
    "price_including_tax",
    "price_excluding_tax",
    "number_available",
    "product_description",
    "category",
    "review_rating",
    "image_url"
]

class CsvWriter:
    
    def __init__(self) -> None:
        pass
    
    def writeBooks(self, books : list[Book]) -> None:
        with open('library/%s.csv' % books[0].category, 'w+', newline='') as fcsv:
            buf = csv.DictWriter(fcsv, fieldnames=CSV_HEADER)
            buf.writeheader()
            for book in books:
                buf.writerow(
                    {
                        "product_page_url": book.product_page_url, 
                        "universal_product_code": book.universal_product_code,
                        "title": book.title,
                        "price_including_tax": book.price_including_tax,
                        "price_excluding_tax": book.price_including_tax,
                        "number_available": book.number_available,
                        "product_description": book.product_description,
                        "category": book.category,
                        "review_rating": book.review_rating,
                        "image_url": book.image_url
                    }
                )