# -*- coding: utf-8 -*-
import scrapy


class RtSpider(scrapy.Spider):
    name = 'rt'
    allowed_domains = ['reuters.com']
    start_urls = ['https://www.reuters.com/companies/AAPL.O/news']

    def parse(self, response):
        pass
