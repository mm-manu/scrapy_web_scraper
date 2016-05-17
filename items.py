# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BrandURL(scrapy.Item):
    url = scrapy.Field()
    category = scrapy.Field()
    
class Product(scrapy.Item):
    name = scrapy.Field()
    category = scrapy.Field()
    
