# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LifeserviceItem(scrapy.Item):
    # define the fields for your item here like:
    IndexID = scrapy.Field()
    ItemName = scrapy.Field()
    Classify_First_Level = scrapy.Field()
    Classify_Second_Level = scrapy.Field()
    Item_Link = scrapy.Field()
