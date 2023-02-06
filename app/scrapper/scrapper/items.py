import scrapy


class ScrapperItem(scrapy.Item):
    """Define the Item fields that will be scraped."""

    title = scrapy.Field()
    company = scrapy.Field()
    location = scrapy.Field()
    date = scrapy.Field()
    category = scrapy.Field()
    seniority = scrapy.Field()
    requirements = scrapy.Field()
    optional = scrapy.Field()
    offer_specs = scrapy.Field()
    salary_value = scrapy.Field()
    salary_type = scrapy.Field()
    requirements_description = scrapy.Field()
    offer_description = scrapy.Field()
    tasks_range = scrapy.Field()
