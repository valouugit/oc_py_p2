from book2scrape import Scraper, CsvWriter

if __name__ == "__main__":
    scraper = Scraper()
    csv = CsvWriter()
    
    book = []
    for cat in scraper.getAllCategories():
        print("[Book in category] %s" % cat.name)
        books = scraper.getAllBookInCategory(category=cat, books=[])
        for book in books:
            scraper.getBook(book)
            print("[Book] Scraping %s" % book.title)
            scraper.downloadBookImg(book=book)
        print("[Save CSV] %s" % cat.name)
        csv.writeBooks(books)