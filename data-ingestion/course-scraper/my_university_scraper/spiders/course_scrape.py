"""Spider for scraping CSUCI Schedule of Classes by term."""

import scrapy


class CourseScrape(scrapy.Spider):
    """Scrape course listings for a given term."""

    name = "CourseScrape"
    allowed_domains = ["ciapps.csuci.edu"]
    default_term = "fall-2023"

    def __init__(self, term=None, **kwargs):
        super().__init__(**kwargs)
        self.term = term or self.default_term

    def start_requests(self):
        """Kick off the crawl at the term-specific index page."""
        start_url = f"https://ciapps.csuci.edu/ScheduleOfClasses/SOC/index/{self.term}"
        self.logger.info("Scraping term %s", self.term)
        yield scrapy.Request(url=start_url, callback=self.parse)

    def parse(self, response, **kwargs):
        """Scrape and enqueue subject pages."""
        del kwargs  # unused
        subject_urls = response.css("li a::attr(href)").getall()
        for url in subject_urls:
            yield scrapy.Request(url=response.urljoin(url), callback=self.parse_subject)

    def parse_subject(self, response):
        """Scrape and enqueue course pages for a subject."""
        course_urls = response.css("li strong a::attr(href)").getall()
        for url in course_urls:
            yield scrapy.Request(url=response.urljoin(url), callback=self.parse_course)

    def parse_course(self, response):
        """Scrape details for a single course."""
        units = response.xpath(
            '//p/strong[contains(text(), "Units:")]/following-sibling::text()'
        ).get()
        if units:
            units = units.strip().split(" ")[0]  # unit format "Units: 3.00"

        rows = response.css("table.table--data tbody tr")
        for row in rows:
            session = row.css("td:nth-child(1)::text").get()
            section = row.css("td:nth-child(2)::text").get()
            class_number = row.css("td:nth-child(3) a::text").get()
            type_ = row.css("td:nth-child(4)::text").get()
            days = row.css("td:nth-child(5)::text").get()
            time = row.css("td:nth-child(6)::text").get()
            location = row.css("td:nth-child(7)::text").get()
            instructor = row.css("td:nth-child(8) a::text").get()

            # store in course dictionary
            course_data = {
                "course_name": response.css("h2::text").get(),
                "session": session,
                "section": section,
                "class_number": class_number,
                "type": type_,
                "days": days,
                "time": time,
                "location": location,
                "instructor": instructor,
                "units": units,
            }

            yield course_data
