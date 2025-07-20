from scraper.amazon import scrape_amazon
from scraper.flipkart import scrape_flipkart
from scraper.walmart import scrape_walmart
from scraper.ajio import scrape_ajio

if __name__ == "__main__":
    scrape_amazon()
    scrape_flipkart()
    scrape_walmart()
    scrape_ajio()
    print("All platforms scraped.")
