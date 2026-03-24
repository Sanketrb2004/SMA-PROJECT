"""
scraping_demo.py

This script shows a simple and beginner-friendly web scraping example.
It does NOT scrape Facebook.

Instead, it uses a public practice website made for learning scraping:
https://quotes.toscrape.com/

Why?
- Real Facebook scraping is restricted by platform rules, login requirements,
  privacy concerns, and anti-bot protections.
- For classroom or beginner projects, a public demo site is safer and easier.
"""

import csv

import requests
from bs4 import BeautifulSoup


URL = "https://quotes.toscrape.com/"
OUTPUT_FILE = "scraped_posts_demo.csv"


def scrape_demo_posts():
    """
    Download a public webpage and extract a few text items.

    We treat quotes like simple "posts" for demonstration purposes.
    """
    response = requests.get(URL, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    quote_blocks = soup.find_all("div", class_="quote")

    scraped_rows = []

    for index, block in enumerate(quote_blocks[:5], start=1):
        text = block.find("span", class_="text").get_text(strip=True)
        author = block.find("small", class_="author").get_text(strip=True)

        scraped_rows.append(
            {
                "post_id": index,
                "text": text,
                "author": author,
            }
        )

    return scraped_rows


def save_to_csv(rows, filename):
    """Save scraped rows into a small CSV file."""
    with open(filename, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["post_id", "text", "author"])
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    print("Starting scraping demo...")
    posts = scrape_demo_posts()
    save_to_csv(posts, OUTPUT_FILE)
    print(f"Saved {len(posts)} demo rows to {OUTPUT_FILE}")
    print("This is a learning example using a public website, not Facebook.")
