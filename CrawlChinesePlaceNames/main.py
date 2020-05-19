# Author    : 不凡不弃
# Datetime  : 2020/5/19 0019 20:53
# description   : 主函数，指定并执行爬虫任务
from scrapy.cmdline import execute
import os
import sys

if __name__ == '__main__':
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    execute(['scrapy', 'crawl', 'CrawlPlaceSpiders'])
