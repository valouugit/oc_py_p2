from dataclasses import dataclass
from typing import Optional

@dataclass
class Book:
    """Class for book data storage"""
    product_page_url: str
    category: str
    universal_product_code: Optional[str] = None
    title: Optional[str] = None
    price_including_tax: Optional[float] = None
    price_excluding_tax: Optional[float] = None
    number_available: Optional[int] = None
    product_description: Optional[str] = None
    review_rating: Optional[float] = None
    image_url: Optional[str] = None