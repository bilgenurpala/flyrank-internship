import json

import pytest
from urllib.error import HTTPError

from scraper import Book, CatalogueParser, PoliteClient, USER_AGENT, save


HTML = """
<article class="product_pod">
  <p class="star-rating Three"></p>
  <h3><a href="catalogue/example_1/index.html" title="  Example Book  ">Example</a></h3>
  <p class="price_color">£12.34</p>
  <p class="instock availability"> In stock </p>
</article>
<li class="next"><a href="page-2.html">next</a></li>
"""


class Response:
    def __init__(self, content):
        self.content = content.encode()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return None

    def read(self):
        return self.content


def test_parser_extracts_clean_structured_record():
    parser = CatalogueParser("https://books.toscrape.com/")
    parser.feed(HTML)
    assert parser.books == [Book("Example Book", 12.34, "In stock", 3, "https://books.toscrape.com/catalogue/example_1/index.html")]
    assert parser.next_url == "https://books.toscrape.com/page-2.html"


def test_client_checks_robots_and_identifies_itself():
    requests = []

    def opener(request, timeout):
        requests.append((request.full_url, request.headers, timeout))
        content = "User-agent: *\nAllow: /" if request.full_url.endswith("robots.txt") else HTML
        return Response(content)

    client = PoliteClient("https://books.toscrape.com/", delay=0, opener=opener, sleeper=lambda _: None)
    client.load_robots()
    assert "Example Book" in client.fetch("https://books.toscrape.com/")
    assert requests[1][1]["User-agent"] == USER_AGENT


def test_client_refuses_disallowed_path():
    client = PoliteClient("https://example.com/", delay=0, opener=lambda request, timeout: Response("User-agent: *\nDisallow: /private"))
    client.load_robots()
    with pytest.raises(PermissionError):
        client.fetch("https://example.com/private/page")


def test_missing_robots_file_allows_crawl():
    def opener(request, timeout):
        if request.full_url.endswith("robots.txt"):
            raise HTTPError(request.full_url, 404, "Not Found", {}, None)
        return Response(HTML)

    client = PoliteClient("https://example.com/", delay=0, opener=opener)
    client.load_robots()
    assert "Example Book" in client.fetch("https://example.com/")


def test_save_writes_verifiable_json(tmp_path):
    output = tmp_path / "books.json"
    save([Book("Example", 8.5, "In stock", 4, "https://example.com/book")], output)
    assert json.loads(output.read_text(encoding="utf-8"))[0]["price_gbp"] == 8.5
