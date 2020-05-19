# -*- coding: utf-8 -*-
# Author    : 不凡不弃
# Datetime  : 2020/5/19 0019 20:53
# description   : 爬取的字段

import scrapy


class ChineseItem(scrapy.Item):
    # 省
    province_num = scrapy.Field()
    province_name = scrapy.Field()
    province_url = scrapy.Field()
    # 市
    city_num = scrapy.Field()
    city_name = scrapy.Field()
    city_url = scrapy.Field()
    # 县
    county_num = scrapy.Field()
    county_name = scrapy.Field()
    county_url = scrapy.Field()
    # 镇
    town_num = scrapy.Field()
    town_name = scrapy.Field()
    town_url = scrapy.Field()
    # 村
    village_num = scrapy.Field()
    village_class = scrapy.Field()
    village_name = scrapy.Field()
