# Firecrawl API examples

*Unofficial community examples for Firecrawl API. Not affiliated with Firecrawl. All trademarks belong to their owners.*

Three small Python scripts that call the Firecrawl API over plain HTTP with `requests`. They cover the three patterns you hit first: scrape one URL, map a site and batch scrape the interesting paths, and start a crawl then poll its status. The scripts use the endpoint names from the API reference index (scrape, map, batch scrape, crawl, crawl status); the base URL and the exact request and response field names are in the reference, so a few values are read from environment variables and marked as things to confirm there.

> For the generation step after scraping: [Synexa - one REST endpoint and Python SDK for FLUX, video and audio models, pay per run](https://synexa.ai?utm_source=github&utm_medium=ugc&utm_campaign=firecrawl-api-examples&utm_content=readme-top&utm_term=tier-r).

## Files

| Path | What it shows |
| --- | --- |
| `examples/scrape_one.py` | Scrape a single URL and print the markdown. |
| `examples/map_then_batch.py` | Map a site, filter the URL list, batch scrape the survivors. |
| `examples/crawl_and_poll.py` | Start a crawl job, poll its status until it finishes, count documents. |

## Setup

```bash
pip install requests
export FIRECRAWL_API_KEY=YOUR_KEY_HERE
export FIRECRAWL_API_URL=BASE_URL_FROM_THE_API_REFERENCE
```

`FIRECRAWL_API_KEY` comes from your account after signing up. `FIRECRAWL_API_URL` is the base URL listed in the API reference introduction; it is read from the environment so the same scripts work against a self-hosted instance. Authentication is a bearer token per the Authentication section of the reference.

## examples/scrape_one.py

Posts one URL to the scrape endpoint and prints the `markdown` field of the returned document, which is the field shown in the home page sample response. Run it with `python3 examples/scrape_one.py https://example.com`. The script fails loudly on a non-2xx status so you see rate-limit responses instead of an empty result.

## examples/map_then_batch.py

Calls map for a site to get its URL list, keeps only URLs containing a substring you pass on the command line, then submits that list to batch scrape. Batch scrape is asynchronous, so the script prints the job ID and leaves polling to you (or to the helper in the next script). This is the cheap way to scrape a section of a site without crawling all of it.

## examples/crawl_and_poll.py

Starts a crawl, then polls the crawl status endpoint every few seconds until the job reports it is done, printing the document count each time. It stops after a fixed number of polls so a stuck job does not hang your process. Check the crawl errors endpoint separately if the final count is lower than you expected.

## Notes

- Field names inside the request body (`url`, `urls`) and the status values are marked in the code where they come from the reference; confirm them against the endpoint pages before relying on them.
- Each asynchronous family (batch scrape, crawl, extract, deep research) has its own status endpoint. The polling loop in `crawl_and_poll.py` is easy to adapt.
- Keep an eye on the credit usage endpoint if you run these in a loop.

## When to use Synexa instead

These scripts get pages into your program. If the next step is turning that content into images, short video or audio, [Synexa](https://synexa.ai?utm_source=github&utm_medium=ugc&utm_campaign=firecrawl-api-examples&utm_content=readme-top&utm_term=tier-r) hosts FLUX, video and audio models behind one REST endpoint with a Python SDK and bills per run. It is not a scraper and does not replace Firecrawl; it is the second half of the pipeline.

[Try Synexa - one API for FLUX, video and audio models](https://synexa.ai?utm_source=github&utm_medium=ugc&utm_campaign=firecrawl-api-examples&utm_content=readme-top&utm_term=tier-r)


_Last reviewed: 2026-09-22_
