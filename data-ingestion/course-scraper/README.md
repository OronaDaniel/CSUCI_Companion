# Course Catalog Scraper

Scrapy-based crawler that ingests Schedule of Classes data by term and emits one JSON record per section.

## Requirements
- Python 3.10+
- Install deps for this scraper: `pip install -r requirements.txt` (Scrapy)

## How to run
From `data-ingestion/course-scraper/`:

```bash
scrapy crawl CourseScrape -a term=spring-2024 -O output.json
```

- `term` is optional; defaults to `fall-2023` if omitted.
- `output.json` is gitignored. A small example schema is in `../../data/samples/sample_output.json`.

## What it scrapes
Traverses the schedule-of-classes site (subject → course → section) to extract course names, sections, class numbers, types, days/times, locations, instructors, and units. See `my_university_scraper/spiders/course_scrape.py`.

## Refreshing for a new term
- Pass the new term via `-a term=<term>` (e.g., `spring-2025`).
- Adjust selectors only if the site structure changes.
- Re-run to regenerate the JSON feed.

## Notes
- Respects `robots.txt` (`ROBOTSTXT_OBEY = True`).
- Rate limiting: enable AutoThrottle or set `DOWNLOAD_DELAY` in `settings.py` if needed.
- Keep the scraper isolated in a virtualenv for clean installs.
