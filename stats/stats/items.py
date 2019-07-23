# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class StatsItem(Item):
    # define the fields for your item here like:
    id = Field()
    #区域名称
    region_name = Field()
    #区域代码
    region_code = Field()
    #区域级别 省1 市2 县3 乡4 村5
    region_level = Field()
    #父Id
    parent_id = Field()
    
