# -*- coding: utf-8 -*-
import scrapy


class GleSpider(scrapy.Spider):
    name = 'gle'
    allowed_domains = ['google.com']
    start_urls = ['https://www.google.com/finance/quote/AAPL:NASDAQ']

    def parse(self, response):
        pass
