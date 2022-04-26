from book2scrape import Scraper, CsvWriter
from rich.progress import Progress

def main():
    scraper = Scraper()
    csv = CsvWriter()
    
    with Progress() as progress:
        books_progress = progress.add_task("[yellow]Scraping books...", total=1000)
        for cat in scraper.getAllCategories():
            print("[Book in category] %s" % cat.name)
            scraper.getAllBooksInCategory(category=cat)
            for book in cat.books:
                scraper.getBook(book)
                progress.update(books_progress, advance=1)
                print("[Book] Scraping %s" % book.title)
                scraper.downloadBookImg(book=book)
            print("[Save CSV] %s" % cat.name)
            csv.writeBooks(cat)


if __name__ == "__main__":
    main()