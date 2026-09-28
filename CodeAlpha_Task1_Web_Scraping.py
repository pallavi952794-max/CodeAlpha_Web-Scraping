"""
CodeAlpha Data Analytics Internship
Task 1: Web Scraping
Project: CodeAlpha_WebScraping
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

BASE_URL = "http://books.toscrape.com/catalogue/page-{}.html"

RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

def scrape_books(num_pages=5):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    books_data = []
    print(f"[*] Initiating web scraping for {num_pages} catalogue pages...")

    for page in range(1, num_pages + 1):
        url = BASE_URL.format(page)
        print(f"--> Scraping Page {page}: {url}")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                print(f"[!] Warning: HTTP {response.status_code} received on page {page}.")
                continue
            soup = BeautifulSoup(response.text, "html.parser")
            book_containers = soup.find_all("article", class_="product_pod")

            for book in book_containers:
                title_tag = book.find("h3").find("a")
                title = title_tag.get("title", "").strip() if title_tag else "Unknown"
                rel_link = title_tag.get("href", "") if title_tag else ""
                full_link = f"http://books.toscrape.com/catalogue/{rel_link}"
                price_text = book.find("p", class_="price_color")
                clean_price = float(price_text.text.replace("£", "").replace("Â", "").strip()) if price_text else 0.0
                rating_tag = book.find("p", class_="star-rating")
                rating_str = rating_tag.get("class", ["", ""])[1] if rating_tag else "Zero"
                rating = RATING_MAP.get(rating_str, 0)
                avail_tag = book.find("p", class_="instock availability")
                availability = avail_tag.text.strip() if avail_tag else "Unknown"

                books_data.append({
                    "Title": title,
                    "Price_GBP": clean_price,
                    "Star_Rating": rating,
                    "Availability": availability,
                    "Product_URL": full_link
                })
            time.sleep(0.3)
        except Exception as e:
            print(f"[!] Network issue on page {page}: {e}")
            break

    df = pd.DataFrame(books_data)
    return df

def save_and_summarize(df, filename="scraped_books_dataset.csv"):
    if df.empty:
        print("[!] No data scraped. Exiting.")
        return
    df.to_csv(filename, index=False, encoding="utf-8")
    print(f"\n[+] Saved {len(df)} records to '{filename}' successfully!")
    print("="*50)
    print("DATASET OVERVIEW & SUMMARY STATISTICS")
    print("="*50)
    print(f"Total Books Scraped : {len(df)}")
    print(f"Average Price (£)   : {df['Price_GBP'].mean():.2f}")
    print(f"Min Price (£)       : {df['Price_GBP'].min():.2f}")
    print(f"Max Price (£)       : {df['Price_GBP'].max():.2f}")
    print(f"Average Star Rating : {df['Star_Rating'].mean():.2f} / 5.0")
    print("="*50)

if __name__ == "__main__":
    df_books = scrape_books(num_pages=5)
    save_and_summarize(df_books)
