# BE-05: The Polite Scraper

This command-line scraper collects book catalogue records from [Books to Scrape](https://books.toscrape.com/), a public practice site built for scraping exercises. It follows `robots.txt`, identifies itself, waits at least 500 ms between page requests, uses timeouts, and retries only temporary network, `429`, and `5xx` failures.

## Output

Each JSON record contains a cleaned title, GBP price, availability, one-to-five rating, and absolute product URL. The default run writes `output/books.json`.

## Run

```bash
cd backend-engineering/be-05
python3.14 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scraper.py --pages 2 --delay 1.0 --output output/books.json
python -m pytest -q
```

The scraper refuses a page when `robots.txt` disallows it. Following RFC 9309, a `4xx` response means the robots file is unavailable and crawling may continue; a network or `5xx` failure stops the run because permission cannot be checked reliably. Retry backoff cannot make an unavailable site available, and HTML changes can require parser updates. The project does not bypass authentication, CAPTCHAs, paywalls, or access controls. It does not establish that scraping an arbitrary site is legally permitted; operators must review the target's terms, jurisdiction, and data sensitivity.
