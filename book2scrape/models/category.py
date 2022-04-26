from dataclasses import dataclass
from typing import List
from .book import Book

@dataclass
class Category:
    """Class for category data storage"""
    name: str
    url: str
    books: List[Book]