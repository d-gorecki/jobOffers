import scrapy


class NoFluffSpider(scrapy.Spider):
    name = "nofluff"

    start_urls = [
        'https://nofluffjobs.com/pl/Python',
    ]

    def parse(self, response):
        for a in response.css("common-main-loader a.posting-list-item"):
            yield response.follow(a, callback=self.parse_offer_details)

        next_page = response.css("li.page-item:last-of-type a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)


    def parse_offer_details(self, response):
        offer = {}
        offer["title"] = response.css("h1::text").get()
        offer["company"] = response.css("div.mobile-list p::text").get()
        offer["location"] = response.css("div.mobile-list span::text").get()
        offer["date"] = response.css("div.mobile-list div.tw-h-12::text").get()
        offer["category"] = response.css("section ul.posting-info-row aside a::text").getall()
        offer["seniority"] = response.css("section ul.posting-info-row li#posting-seniority span::text").get()
        offer["requirements"] = response.css("div#posting-requirements span::text").getall()
        offer["optional"] = response.css("div#posting-requirements section#posting-nice-to-have span::text").getall()
        offer["offer_specs"] = response.css("section#posting-specs li::text").getall()
        offer["salary_value"] = response.css("section.banner-section h4 span::text").get()
        offer["salary_type"] = response.css("section.banner-section p.intervals-salary-type::text").get()
        offer["requirements_description"] = response.xpath("//common-posting-content-wrapper/div/section[2]//text()").getall()
        offer["offer_description"] = response.xpath("//section[@id='posting-description']//text()").getall()
        offer["tasks_range"] = response.xpath("//section[@id='posting-tasks']//text()").getall()

        for key, value in offer.items():
            if value:
                if isinstance(value, list):
                    offer[key] = [item.strip() for item in value]
                else:
                    offer[key] = value.strip()

        yield offer




