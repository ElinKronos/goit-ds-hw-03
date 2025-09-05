# Here begins a new World...

import requests, json, time
from bs4 import BeautifulSoup
from urllib.parse import urljoin

URL = 'https://quotes.toscrape.com/'
session = requests.Session()

def get_soup(url: str) -> BeautifulSoup:
    r = session.get(url, timeout=15)
    r.raise_for_status()
    return BeautifulSoup(r.text, "html.parser")

def scrape():
    authors_by_name = {}
    qoutes = []

    url = URL
    while True:
        soup = get_soup(url)

        # кожна цитата на сторінці
        for q in soup.select(".quote"):
            text = q.select_one(".text").get_text(strip=True)
            author_name = q.select_one(".author").get_text(strip=True)
            tags = [t.get_text(strip=True) for t in q.select(".tags a.tag")]

            # посилання на автора
            author_a = q.select_one("span a[href*='/author/']")
            author_href = author_a["href"]
            author_url = urljoin(URL, author_href)

            # підтягнути автора, якщо ще не тягнули
            if author_name not in authors_by_name:
                a_soup = get_soup(author_url)
                fullname = a_soup.select_one(".author-title").get_text(strip=True)
                born_date = a_soup.select_one(".author-born-date").get_text(strip=True)
                born_location = a_soup.select_one(".author-born-location").get_text(strip=True)
                description = a_soup.select_one(".author-description").get_text(strip=True)

                authors_by_name[author_name] = {
                    "fullname": fullname,
                    "born_date": born_date,
                    "born_location": born_location,
                    "description": description,
                }
                time.sleep(0.15)  # чемний скрапінг

            # структура записи для qoutes.json
            qoutes.append({
                "tags": tags,
                "author": author_name,
                "quote": text
            })

        # пагінація
        next_a = soup.select_one(".pager .next a")
        if not next_a:
            break
        url = urljoin(url, next_a["href"])
        time.sleep(0.15)

    # зберегти у файли
    with open("qoutes.json", "w", encoding="utf-8") as f:
        json.dump(qoutes, f, ensure_ascii=False, indent=2)

    with open("authors.json", "w", encoding="utf-8") as f:
        json.dump(list(authors_by_name.values()), f, ensure_ascii=False, indent=2)

    print(f"Saved {len(qoutes)} quotes -> qoutes.json")
    print(f"Saved {len(authors_by_name)} authors -> authors.json")

if __name__ == "__main__":
    scrape()
