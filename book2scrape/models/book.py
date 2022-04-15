from dataclasses import dataclass

@dataclass
class Book:
    """Class for book data storage"""
    product_page_url: str
    category: str
    universal_product_code: str = None
    title: str = None
    price_including_tax: float = None
    price_excluding_tax: float = None
    number_available: int = None
    product_description: str = None
    review_rating: float = None
    image_url: str = None