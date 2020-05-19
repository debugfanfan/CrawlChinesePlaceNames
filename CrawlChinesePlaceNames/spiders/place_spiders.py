# Author    : 不凡不弃
# Datetime  : 2020/5/19 0019 20:53
# description   : 爬虫任务模块
import scrapy
from CrawlChinesePlaceNames.items import ChineseItem

# 根网址
base_url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/'


# 抽取链接的公用方法
def common(response):
    common_list = response.xpath("//a")[:-1]
    number_list = [number for n, number in enumerate(common_list) if n % 2 == 0]
    name_list = [name for n, name in enumerate(common_list) if n % 2 == 1]
    return zip(number_list, name_list)


class CrawlPlaceSpiders(scrapy.Spider):
    # 爬虫名称
    name = "CrawlPlaceSpiders"
    # 允许的域名
    allowed_domains = ["'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/index.html'"]

    # 首页
    start_urls = [
        'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/index.html'
    ]
    # 客户端信息设置
    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36'
        }
    }

    # 爬虫任务的第一层任务
    def parse(self, response):
        """
            省
        :param response:
        :return:
        """
        # 匹配省份链接
        province_list = response.xpath("//a[@href]")
        province_list = province_list[0:1]
        # 对每一个省份进行处理
        for province in province_list:
            # 省份名
            province_name = province.xpath("text()").extract()[0]
            # 省份url
            province_url = base_url + province.xpath("@href").extract()[0]
            # 省份代号
            province_num = province.xpath("@href").extract()[0].split('.', 1)[0]

            print("省名：", province_name, " 链接：", province_url)
            # 保存三个字段的值
            item = ChineseItem(province_num=province_num, province_name=province_name, province_url=province_url)
            # province_url：接下来要爬取的网址
            # callback：接下来爬取网址的回调函数
            # dont_filter：True  不过滤不在允许域名里的网址
            request = scrapy.Request(url=province_url, callback=self.parse_city, dont_filter=True)
            # 暂时保存item数据
            request.meta['item'] = item
            yield request

    # 爬虫任务的第二层任务
    def parse_city(self, response):
        """
            市
        :param response:
        :return:
        """
        # 对每一个市进行处理
        for number, name_tem in common(response):
            # 市代号
            num = number.xpath("text()").extract()[0]
            # 市名
            name = name_tem.xpath("text()").extract()[0]
            # 市url
            url = base_url + number.xpath("@href").extract()[0]

            print("number：", num, " 名称：", name, " 链接：", url)

            # 获取上一步暂存的item数据，重新构造item
            item = response.meta['item']

            item = ChineseItem(province_num=item["province_num"], province_name=item["province_name"],
                               province_url=item["province_url"],
                               city_num=num, city_name=name, city_url=url)
            request = scrapy.Request(url=url, callback=self.parse_county, dont_filter=True)
            request.meta['item'] = item
            yield request

    # 爬虫任务的第三层任务
    def parse_county(self, response):
        """
            县
        :param response:
        :return:
        """
        # 对每一个县进行处理
        for number, name_tem in common(response):
            # 县代号
            num = number.xpath("text()").extract()[0]
            # 县名
            name = name_tem.xpath("text()").extract()[0]
            # 县url
            url = base_url + num[:2] + "/" + number.xpath("@href").extract()[0]

            print("number：", num, " 名称：", name, " 链接：", url)

            # 获取上一步暂存的item数据，重新构造item
            item = response.meta['item']

            item = ChineseItem(province_num=item["province_num"], province_name=item["province_name"],
                               province_url=item["province_url"],
                               city_num=item["city_num"], city_name=item["city_name"], city_url=item["city_url"],
                               county_num=num, county_name=name, county_url=url)

            request = scrapy.Request(url=url, callback=self.parse_town, dont_filter=True)
            request.meta['item'] = item
            yield request

    # 爬虫任务的第四层任务
    def parse_town(self, response):
        """
            镇
        :param response:
        :return:
        """
        # 对每一个镇进行处理
        for number, name_tem in common(response):
            # 镇代号
            num = number.xpath("text()").extract()[0]
            # 镇名
            name = name_tem.xpath("text()").extract()[0]
            # 镇url
            url = base_url + num[0:2] + "/" + num[2:4] + "/" + number.xpath("@href").extract()[0]

            print("number：", num, " 名称：", name, " 链接：", url)

            # 获取上一步暂存的item数据，重新构造item
            item = response.meta['item']

            item = ChineseItem(province_num=item["province_num"], province_name=item["province_name"],
                               province_url=item["province_url"],
                               city_num=item["city_num"], city_name=item["city_name"], city_url=item["city_url"],
                               county_num=item["county_num"], county_name=item["county_name"],
                               county_url=item["county_url"],
                               town_num=num, town_name=name, town_url=url)

            request = scrapy.Request(url=url, callback=self.parse_village, dont_filter=True)
            request.meta['item'] = item
            yield request

    # 爬虫任务的第五层任务
    def parse_village(self, response):
        """
            村
        :param response:
        :return:
        """
        # 匹配村信息
        village_list = response.xpath("//tr[@class='villagetr']")
        # 对每一个村进行处理
        for village in village_list:
            # 村代号
            village_num = village.xpath("td[1]/text()").extract()[0]
            # 村分类
            village_class = village.xpath("td[2]/text()").extract()[0]
            # 村名
            village_name = village.xpath("td[3]/text()").extract()[0]

            print("number：", village_num, " 村名：", village_name, " 分类代码：", village_class)

            # 获取上一步暂存的item数据，重新构造item
            item = response.meta['item']

            item = ChineseItem(province_num=item["province_num"], province_name=item["province_name"],
                               province_url=item["province_url"],
                               city_num=item["city_num"], city_name=item["city_name"], city_url=item["city_url"],
                               county_num=item["county_num"], county_name=item["county_name"],
                               county_url=item["county_url"],
                               town_num=item["town_num"], town_name=item["town_name"], town_url=item["town_url"],
                               village_num=village_num, village_name=village_name, village_class=village_class)

            # 这是最后一层直接返回item，不再需要scrapy.Request()函数
            yield item
