import scrapy
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector  
from urlparse import urljoin
from stats.items import StatsItem
import snowflake.client

import re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class StatsSpider(scrapy.Spider):
    name="stats"
    allowed_domains = ['stats.gov.cn']
    start_urls = ['http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/index.html']
    snowflake.client.setup('127.0.0.1', 30001)
    #雪花算法  pip install pysnowflake
    #snowflake_start_server   --address=0.0.0.0   --port=30001   --dc=1   --worker=1   --log_file_prefix=/tmp/pysnowflask.log

    def parse(self, response):
        data = HtmlXPathSelector(response)
        provincetr = data.select('''//tr[@class="provincetr"]//a''')
        for item in provincetr:
            regionItem = StatsItem()
            regionItem['region_name'] = item.select('text()').extract_first()
            url = item.select('@href').extract_first()
            regionItem['region_code']= re.match(r'(\d+)',url).group(0) +'0000'
            regionItem['region_level'] = 1
            regionItem['parent_id'] = 0
            regionItem['id'] = snowflake.client.get_guid()
            province_url = urljoin(response.url,url)
            yield regionItem
            request = scrapy.Request(province_url,callback=self.parse_city)
            request.meta['parent_id'] = regionItem['id']
            yield request
            # print name,province_url
    def parse_city(self, response):
        data = Selector(response)
        citytr = data.xpath('''//tr[@class="citytr"]''')
        parent_id = response.meta['parent_id']
        for item in citytr:
            regionItem = StatsItem()
            regionItem['region_name'] = item.xpath('.//td[2]//text()').extract_first()
            regionItem['region_code'] =  item.xpath('.//td[1]//text()').extract_first()[0:6]
            regionItem['parent_id'] = parent_id
            regionItem['id'] = snowflake.client.get_guid()
            regionItem['region_level'] =2
            yield regionItem
            url = item.xpath('.//td[1]//@href').extract_first()
            if not url:
                continue
            city_url = urljoin(response.url,url)
            request = scrapy.Request(city_url,callback=self.parse_county)
            request.meta['parent_id'] = regionItem['id']
            yield request

    def parse_county(self,response):
        data = Selector(response)
        countytr = data.xpath('''//tr[@class="countytr"]''')
        parent_id = response.meta['parent_id']
        for item in countytr:
            regionItem = StatsItem()
            regionItem['region_name'] = item.xpath('.//td[2]//text()').extract_first()
            regionItem['region_code'] =  item.xpath('.//td[1]//text()').extract_first()[0:6]
            regionItem['parent_id'] = parent_id
            regionItem['id'] = snowflake.client.get_guid()
            regionItem['region_level'] = 3
            yield regionItem
            url = item.xpath('.//td[1]//@href').extract_first()
            if not url:
                continue
            city_url = urljoin(response.url,url)
            request = scrapy.Request(city_url,callback=self.parse_town)
            request.meta['parent_id'] = regionItem['id']
            yield request

    def parse_town(self,response):
        data = Selector(response)
        towntr = data.xpath('''//tr[@class="towntr"]''')
        parent_id = response.meta['parent_id']
        for item in towntr:
            regionItem = StatsItem()
            regionItem['region_name'] = item.xpath('.//td[2]//text()').extract_first()
            regionItem['region_code'] =  item.xpath('.//td[1]//text()').extract_first()[0:9]
            regionItem['parent_id'] = parent_id
            regionItem['id'] = snowflake.client.get_guid()
            regionItem['region_level'] = 4
            yield regionItem
            url = item.xpath('.//td[1]//@href').extract_first()
            if not url:
                continue
            city_url = urljoin(response.url,url)
            request = scrapy.Request(city_url,callback=self.parse_village)
            request.meta['parent_id'] = regionItem['id']
            yield request

    def parse_village(self,response):
        data = Selector(response)
        towntr = data.xpath('''//tr[@class="villagetr"]''')
        parent_id = response.meta['parent_id']
        for item in towntr:
            regionItem = StatsItem()
            regionItem['region_name'] = item.xpath('.//td[3]//text()').extract_first()
            regionItem['region_code'] =  item.xpath('.//td[1]//text()').extract_first()
            regionItem['parent_id'] = parent_id
            regionItem['id'] = snowflake.client.get_guid()
            regionItem['region_level'] = 5
            yield regionItem