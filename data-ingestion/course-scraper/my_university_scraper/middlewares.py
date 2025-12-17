"""Scrapy spider and downloader middleware stubs for my_university_scraper"""

from scrapy import signals


class MyUniversityScraperSpiderMiddleware:
    """Spider middleware stub that leaves requests/responses untouched."""

    @classmethod
    def from_crawler(cls, crawler):
        """Create middleware instance and wire signals."""
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        """Called for each response before the spider processes it; return None to continue."""
        return None

    def process_spider_output(self, response, result, spider):
        """Iterate over spider results; must yield Request or item objects."""
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        """Handle exceptions from the spider or previous middleware; return None or new results."""
        pass

    def process_start_requests(self, start_requests, spider):
        """Handle initial start_requests iterable; must yield only Request objects."""
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        """Log spider start."""
        spider.logger.info("Spider opened: %s", spider.name)


class MyUniversityScraperDownloaderMiddleware:
    """Downloader middleware stub that forwards requests/responses without changes."""

    @classmethod
    def from_crawler(cls, crawler):
        """Create middleware instance and wire signals."""
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        """Inspect/modify outgoing requests; return None to continue processing."""
        return None

    def process_response(self, request, response, spider):
        """Inspect/modify responses; return a Response or Request to continue."""
        return response

    def process_exception(self, request, exception, spider):
        """Handle exceptions from download handlers or process_request; return None/Response/Request."""
        pass

    def spider_opened(self, spider):
        """Log spider start."""
        spider.logger.info("Spider opened: %s", spider.name)
