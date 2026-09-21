#!/usr/bin/env python3
"""Map a site, keep URLs matching a substring, then batch scrape them.

Usage: python3 map_then_batch.py SITE_URL SUBSTRING

Env:
  FIRECRAWL_API_KEY  your key
  FIRECRAWL_API_URL  base URL from the API reference introduction
"""
import os
import sys

import requests

API_KEY = os.environ['FIRECRAWL_API_KEY']
BASE_URL = os.environ['FIRECRAWL_API_URL'].rstrip('/')
HEADERS = {'Authorization': f'Bearer {API_KEY}'}


def map_site(url: str) -> list[str]:
    # Endpoint name per the API reference: Map URLs.
    resp = requests.post(f'{BASE_URL}/map', headers=HEADERS, json={'url': url}, timeout=60)
    resp.raise_for_status()
    body = resp.json()
    # Confirm the response field on the map page; 'links' is illustrative.
    return body.get('links', body.get('data', []))


def batch_scrape(urls: list[str]) -> str:
    # Endpoint name per the API reference: Batch scrape multiple URLs.
    resp = requests.post(f'{BASE_URL}/batch/scrape', headers=HEADERS, json={'urls': urls}, timeout=60)
    resp.raise_for_status()
    body = resp.json()
    return str(body.get('id', body))  # job id field: confirm on the batch scrape page


def main() -> None:
    if len(sys.argv) != 3:
        print('usage: map_then_batch.py SITE_URL SUBSTRING')
        sys.exit(2)
    site, needle = sys.argv[1], sys.argv[2]
    links = map_site(site)
    keep = [u for u in links if needle in u]
    print(f'mapped {len(links)} urls, keeping {len(keep)} containing {needle!r}')
    if not keep:
        return
    job_id = batch_scrape(keep)
    print(f'batch scrape job started: {job_id}')
    print('poll the batch status endpoint with this id')


if __name__ == '__main__':
    main()
