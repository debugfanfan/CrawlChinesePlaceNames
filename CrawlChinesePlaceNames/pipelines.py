# -*- coding: utf-8 -*-
# Author    : 不凡不弃
# Datetime  : 2020/5/19 0019 20:53
# description   : 保存爬取到的数据


import json
import codecs


class CrawlchineseplacenamesPipeline:

    def __init__(self):
        # 创建要保存到的文件
        self.file = codecs.open('data.json', 'w', 'utf-8')

    def process_item(self, item, spider):
        # 将item转为字典格式，一行一行写入
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item

    def close_spider(self, spider):
        # 关闭资源
        self.file.close()
