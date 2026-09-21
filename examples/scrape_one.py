#!/usr/bin/env python3
"""Scrape one URL with the Firecrawl API and print its markdown.

Env:
  FIRECRAWL_API_KEY  your key
  FIRECRAWL_API_URL  base URL from the API reference introduction
"""
import os
import sys

import requests

API_KEY = os.environ['FIRECRAWL_API_KEY']
BASE_URL = os.environ['FIRECRAWL_API_URL'].rstrip('/')


def scrape(url: str) -> dict:
    # Endpoint name per the API reference: Scrape a single URL.
    resp = requests.post(
        f'{BASE_URL}/scrape',
        headers={'Authorization': f'Bearer {API_KEY}'},
        json={'url': url},  # body field name: confirm on the scrape page
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()


def main() -> None:
    if len(sys.argv) != 2:
        print('usage: scrape_one.py URL')
        sys.exit(2)
    result = scrape(sys.argv[1])
    # The home page sample shows documents with url/markdown/json/screenshot.
    doc = result.get('data', result)
    print(doc.get('markdown', '')[:2000])


if __name__ == '__main__':
    main()
