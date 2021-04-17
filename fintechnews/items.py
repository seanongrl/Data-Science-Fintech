# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class FintechnewsItem(Item):
    title = Field()
    category = Field()
    desc = Field()
    source = Field()
    datetime = Field()
    image = Field()
    article_link = Field()


