# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Covid19Item(scrapy.Item):
    confirmed_cases = scrapy.Field()
    confirmed_deaths = scrapy.Field()
    countries_cumulative_cases = scrapy.Field()

class DecemberCases(scrapy.Item): 
    day_timestamp = scrapy.Field()
    daily_confirmed_cases = scrapy.Field()
    daily_increase = scrapy.Field()
    daily_change_percent = scrapy.Field()