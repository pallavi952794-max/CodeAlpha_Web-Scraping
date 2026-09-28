# Task 1: Web Scraping

## Project Overview
This project extracts structured book catalog information from the public e-commerce testing website **[Books to Scrape](http://books.toscrape.com/)** using Python's `BeautifulSoup` and `requests` libraries.

## Features
- **Pagination Traversal:** Automates HTTP GET requests across multiple pages.
- **HTML Parsing:** Navigates DOM structure to isolate product cards (`article.product_pod`).
- **Data Cleaning:** Cleans currency symbols (£), standardizes whitespace, and converts string star ratings (`One` to `Five`) to numeric integers (1 to 5).
- **Data Export:** Saves structured data into `scraped_books_dataset.csv`.

## Dataset Schema
| Column | Data Type | Description |
|---|---|---|
| `Title` | String | Full title of the book |
| `Price_GBP` | Float | Price in British Pounds (£) |
| `Star_Rating` | Integer | Rating out of 5 (1 to 5) |
| `Availability` | String | Stock availability status |
| `Product_URL` | String | Direct link to product detail page |

## Execution
```bash
pip install requests beautifulsoup4 pandas
python CodeAlpha_Task1_Web_Scraping.py
```
