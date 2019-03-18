# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CaipiaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 双色球期数
    qishu = scrapy.Field()

    # 开奖日期
    open_data = scrapy.Field()

    # 双色球号码
    nub = scrapy.Field()