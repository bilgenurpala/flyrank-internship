import argparse
import json
import random
import time
from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen
from urllib.robotparser import RobotFileParser


DEFAULT_URL = "https://books.toscrape.com/"
USER_AGENT = "BilgenurPalaPortfolioBot/1.0 (+https://bilgenurpala.netlify.app/)"


@dataclass(frozen=True)
class Book:
    title: str
    price_gbp: float
    availability: str
    rating: int
    url: str


class CatalogueParser(HTMLParser):
    def __init__(self, page_url):
        super().__init__()
        self.page_url = page_url
        self.books = []
        self.next_url = None
        self.current = None
        self.capture_price = False
        self.capture_availability = False

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        classes = values.get("class", "").split()
        if tag == "article" and "product_pod" in classes:
            self.current = {"rating": 0}
        elif self.current is not None and tag == "p" and "star-rating" in classes:
            names = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
            self.current["rating"] = next((names[name] for name in classes if name in names), 0)
        elif self.current is not None and tag == "a" and values.get("title"):
            self.current["title"] = values["title"].strip()
            self.current["url"] = urljoin(self.page_url, values.get("href", ""))
        elif self.current is not None and tag == "p" and "price_color" in classes:
            self.capture_price = True
        elif self.current is not None and tag == "p" and "availability" in classes:
            self.capture_availability = True
        elif tag == "li" and "next" in classes:
            self.current_next = True
        elif tag == "a" and getattr(self, "current_next", False):
            self.next_url = urljoin(self.page_url, values.get("href", ""))
            self.current_next = False

    def handle_data(self, data):
        if self.current is not None and self.capture_price:
            value = data.strip().replace("£", "").replace("Â", "")
            if value:
                self.current["price_gbp"] = float(value)
                self.capture_price = False
        if self.current is not None and self.capture_availability:
            value = " ".join(data.split())
            if value:
                self.current["availability"] = value

    def handle_endtag(self, tag):
        if tag == "p":
            self.capture_availability = False
        if tag == "article" and self.current is not None:
            required = {"title", "price_gbp", "availability", "rating", "url"}
            if required.issubset(self.current):
                self.books.append(Book(**self.current))
            self.current = None


class PoliteClient:
    def __init__(self, start_url, delay=1.0, retries=3, timeout=10.0, opener=urlopen, sleeper=time.sleep):
        self.start_url = start_url
        self.delay = delay
        self.retries = retries
        self.timeout = timeout
        self.opener = opener
        self.sleeper = sleeper
        parsed = urlparse(start_url)
        self.robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        self.robots = RobotFileParser(self.robots_url)
        self.last_request = None

    def load_robots(self):
        request = Request(self.robots_url, headers={"User-Agent": USER_AGENT})
        try:
            with self.opener(request, timeout=self.timeout) as response:
                content = response.read().decode("utf-8", errors="replace")
        except HTTPError as error:
            if 400 <= error.code < 500:
                content = "User-agent: *\nAllow: /"
            else:
                raise RuntimeError(f"Could not verify robots.txt: {error}") from error
        except (URLError, TimeoutError) as error:
            raise RuntimeError(f"Could not verify robots.txt: {error}") from error
        self.robots.parse(content.splitlines())

    def fetch(self, url):
        if not self.robots.can_fetch(USER_AGENT, url):
            raise PermissionError(f"robots.txt does not allow {url}")
        if self.last_request is not None:
            remaining = self.delay - (time.monotonic() - self.last_request)
            if remaining > 0:
                self.sleeper(remaining)
        request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html"})
        for attempt in range(self.retries):
            try:
                self.last_request = time.monotonic()
                with self.opener(request, timeout=self.timeout) as response:
                    return response.read().decode("utf-8", errors="replace")
            except HTTPError as error:
                if error.code != 429 and error.code < 500:
                    raise
                wait = float(error.headers.get("Retry-After", 2 ** attempt))
            except (URLError, TimeoutError):
                wait = 2 ** attempt + random.uniform(0, 0.25)
            if attempt + 1 < self.retries:
                self.sleeper(wait)
        raise RuntimeError(f"Request failed after {self.retries} attempts: {url}")


def scrape(start_url=DEFAULT_URL, pages=1, delay=1.0, client=None):
    polite_client = client or PoliteClient(start_url, delay=delay)
    polite_client.load_robots()
    records = []
    url = start_url
    for _ in range(pages):
        if url is None:
            break
        parser = CatalogueParser(url)
        parser.feed(polite_client.fetch(url))
        records.extend(parser.books)
        url = parser.next_url
    return records


def save(records, output_path):
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps([asdict(record) for record in records], indent=2), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--pages", type=int, default=1)
    parser.add_argument("--delay", type=float, default=1.0)
    parser.add_argument("--output", default="output/books.json")
    args = parser.parse_args()
    records = scrape(args.url, max(1, args.pages), max(0.5, args.delay))
    save(records, args.output)
    print(f"Saved {len(records)} records to {args.output}")


if __name__ == "__main__":
    main()
