import os, time, pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
PROMO_KEYWORDS = ["off", "discount", "%", "sale", "up to", "flat", "offer"]

def is_promo(text):
    return any(kw in text.lower() for kw in PROMO_KEYWORDS)

def scrape_ajio():
    HEADLESS = os.getenv("HEADLESS") == "True"
    DELAY = int(os.getenv("SCRAPE_DELAY", 5))
    DATA_DIR = os.getenv("DATA_DIR", "./data")
    options = Options()
    if HEADLESS:
        options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    urls = [
        "https://www.ajio.com/sale",
        "https://www.ajio.com/men-sale",
        "https://www.ajio.com/women-sale"
    ]

    data = []
    for url in urls:
        for page in range(1, 4):
            paged = url + f"?page={page}"
            driver.get(paged)
            time.sleep(DELAY)
            soup = BeautifulSoup(driver.page_source, 'lxml')

            for tag in soup.find_all(['h1','h2','h3','span','a','div']):
                text = tag.get_text(strip=True)
                if text and len(text.split()) > 1:
                    data.append({"source":"ajio","type":tag.name,"text":text,"image_url":"","is_promo":is_promo(text)})

            for img in soup.find_all('img'):
                src = img.get('src')
                alt = img.get('alt','')
                if src:
                    data.append({"source":"ajio","type":"image","text":alt,"image_url":src,"is_promo":is_promo(alt)})

    driver.quit()
    df = pd.DataFrame(data)
    os.makedirs(DATA_DIR, exist_ok=True)
    df.to_csv(os.path.join(DATA_DIR,"ajio_raw_data.csv"), index=False)
    print(f"Ajio done: {len(df)} rows")
