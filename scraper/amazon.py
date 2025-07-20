import os, time, pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

PROMO_KEYWORDS = ["off", "discount", "%", "deal", "limited time", "save", "exclusive", "offer", "clearance", "big sale", "up to", "flat"]

def is_promo(text):
    return any(kw in text.lower() for kw in PROMO_KEYWORDS)

def scrape_amazon():
    HEADLESS = os.getenv("HEADLESS") == "True"
    DELAY = int(os.getenv("SCRAPE_DELAY", 5))
    DATA_DIR = os.getenv("DATA_DIR", "./data")
    options = Options()
    if HEADLESS:
        options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    urls = [
        "https://www.amazon.com/gp/goldbox?bubble-id=trending-bubble",
        "https://www.amazon.com/s?k=electronics+deals",
        "https://www.amazon.com/s?k=mens+clothing+sale",
        "https://www.amazon.com/s?k=home+discounts",
        "https://www.amazon.com/s?k=books+offer"
    ]
    data = []
    for url in urls:
        for page in range(1, 10): 
            paged = url + (f"&page={page}" if "s?k=" in url else "")
            driver.get(paged)
            time.sleep(DELAY + 2)
            soup = BeautifulSoup(driver.page_source, 'lxml')

            for tag in soup.find_all(['h1','h2','h3','span','a','button','div']):
                text = tag.get_text(strip=True)
                if text and len(text.split()) > 1:
                    promo = is_promo(text)
                    data.append({"source":"amazon","type":tag.name,"text":text,"image_url":"","is_promo":promo})
            for img in soup.find_all('img'):
                src = img.get('src')
                alt = img.get('alt','')
                if src:
                    promo = is_promo(alt)
                    data.append({"source":"amazon","type":"image","text":alt,"image_url":src,"is_promo":promo})

    driver.quit()
    df = pd.DataFrame(data)
    os.makedirs(DATA_DIR, exist_ok=True)
    df.to_csv(os.path.join(DATA_DIR,"amazon_raw_data.csv"), index=False)
    print(f"Amazon done: {len(df)} rows")

if __name__ == "__main__":
    scrape_amazon()
