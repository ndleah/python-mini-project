import os
import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_url(url: str):
    """Fetch content from URL and return parsed BeautifulSoup object."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except Exception as e:
        print(f"Error fetching '{url}': {e}")
        return None

def scrape_books(max_pages: int = 5, output_csv: str = "books.csv"):
    """Scrape book titles, prices, and star ratings across pages."""
    data = []
    print(f"Starting book scraping (up to {max_pages} pages)...")

    for page in range(1, max_pages + 1):
        url = f'https://books.toscrape.com/catalogue/page-{page}.html'
        soup = scrape_url(url)
        if not soup:
            break

        ol = soup.find('ol', class_='row')
        if not ol:
            break

        articles = ol.find_all('article', class_='product_pod')
        print(f"Scraping page {page}: found {len(articles)} books.")

        for article in articles:
            title_element = article.find('h3')
            title = title_element.find('a')['title'] if title_element and title_element.find('a') else (title_element.get_text(strip=True) if title_element else "N/A")

            # Fix: Search within article scope instead of global page soup
            price_element = article.find('p', class_='price_color')
            price = price_element.get_text(strip=True) if price_element else "N/A"

            star_element = article.find('p', class_='star-rating')
            star = star_element['class'][1] if (star_element and len(star_element.get('class', [])) > 1) else "N/A"

            data.append({"title": title, "price": price, "star": star})

    df = pd.DataFrame(data)
    df.to_csv(output_csv, index=False)
    print(f"Scraping complete! Saved {len(df)} books to '{output_csv}'.")
    return df

def main():
    scrape_books(max_pages=5)

if __name__ == '__main__':
    main()