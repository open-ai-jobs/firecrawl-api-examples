#!/usr/bin/env python3
"""Start a Firecrawl crawl and poll its status until it finishes.

Usage: python3 crawl_and_poll.py SITE_URL

Env:
  FIRECRAWL_API_KEY  your key
  FIRECRAWL_API_URL  base URL from the API reference introduction
"""
import os
import sys
import time

import requests

API_KEY = os.environ['FIRECRAWL_API_KEY']
BASE_URL = os.environ['FIRECRAWL_API_URL'].rstrip('/')
HEADERS = {'Authorization': f'Bearer {API_KEY}'}
POLL_SECONDS = 5
MAX_POLLS = 120  # give up after ten minutes


def start_crawl(url: str) -> str:
    # Endpoint name per the API reference: Start Crawl.
    resp = requests.post(f'{BASE_URL}/crawl', headers=HEADERS, json={'url': url}, timeout=60)
    resp.raise_for_status()
    return str(resp.json().get('id'))  # job id field: confirm on the crawl page


def crawl_status(job_id: str) -> dict:
    # Endpoint name per the API reference: Get Crawl Status.
    resp = requests.get(f'{BASE_URL}/crawl/{job_id}', headers=HEADERS, timeout=60)
    resp.raise_for_status()
    return resp.json()


def main() -> None:
    if len(sys.argv) != 2:
        print('usage: crawl_and_poll.py SITE_URL')
        sys.exit(2)
    job_id = start_crawl(sys.argv[1])
    print(f'crawl started: {job_id}')
    for _ in range(MAX_POLLS):
        status = crawl_status(job_id)
        state = status.get('status')  # status value names: confirm on the status page
        docs = status.get('data', [])
        print(f'  status={state} documents={len(docs)}')
        if state in ('completed', 'failed', 'cancelled'):
            break
        time.sleep(POLL_SECONDS)
    else:
        print('gave up waiting; check the crawl status and crawl errors endpoints')


if __name__ == '__main__':
    main()
