# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class OlxItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    user_name = scrapy.Field()
    user_url = scrapy.Field()
    phone_number = scrapy.Field()

    title = scrapy.Field()
    description = scrapy.Field()
    photo_urls = scrapy.Field()
    price = scrapy.Field()
    address = scrapy.Field()
    date_time = scrapy.Field()
    ad_number = scrapy.Field()

