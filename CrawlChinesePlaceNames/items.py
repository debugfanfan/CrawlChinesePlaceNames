# -*- coding: utf-8 -*-
# Author    : 不凡不弃
# Datetime  : 2020/5/19 0019 20:53
# description   : 爬取的字段

import scrapy


class ChineseItem(scrapy.Item):
    province_num = scrapy.Field()  # 省代号
    province_name = scrapy.Field()  # 省名
    province_url = scrapy.Field()  # 省url
    city_num = scrapy.Field()  # 市代号
    city_name = scrapy.Field()  # 市名
    city_url = scrapy.Field()  # 市url
    county_num = scrapy.Field()  # 县代号
    county_name = scrapy.Field()  # 县名
    county_url = scrapy.Field()  # 县url
    town_num = scrapy.Field()  # 镇代号
    town_name = scrapy.Field()  # 镇名
    town_url = scrapy.Field()  # 镇url
    village_num = scrapy.Field()  # 村代号
    village_class = scrapy.Field()  # 村分类
    village_name = scrapy.Field()  # 村名
