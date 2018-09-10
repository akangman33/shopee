# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import ShopeeItem

class ShopeeBasicSpider(scrapy.Spider):
    name = 'shopee_basic'
    allowed_domains = ['shopee.tw']
    start_urls = ['http://shopee.tw/']

    def __init__(self):
        self.keyword = "CARHARTT短褲"
        self.newest = 0
        self.url = "https://shopee.tw/api/v2/search_items/?by=relevancy&keyword={}&limit=50&newest={}&order=desc&page_type=search"
        self.headers = {
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'if-none-match': '"fac392d3ff15c1c08235952bae8f33f0;gzip"',
            'if-none-match-': '55b03-978c0d4b5896a0232388ea6606f02581',
            'referer': 'https://shopee.tw/search?category=69&keyword=iphone&page=0&sortBy=relevancy',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'x-api-source': 'pc',
            'x-requested-with': 'XMLHttpRequest',
        }

    def start_requests(self):
        url = self.url.format(self.keyword, self.newest)
        yield scrapy.Request(url=url, headers=self.headers, callback=self.parse, dont_filter=True, meta={'key': self.keyword, 'count': self.newest})


    def parse(self, response):
        sp = ShopeeItem()
        key = response.meta.get('key')
        count = response.meta.get('count')
        data = json.loads(response.text)
        results = data['items']
        if len(results) > 0:
            for result in results:
                sp['name'] = result['name']
                sp['price_min'] = result['price_min']
                sp['price_max'] = result['price_max']
                # print(sp, '****************************************'*10)
                yield sp
            url = self.url.format(self.keyword, str(count+50))
            print(url, '****************************************'*10)
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse, dont_filter=True, meta={'key': key, 'count': count+50})

        else:
            pass


