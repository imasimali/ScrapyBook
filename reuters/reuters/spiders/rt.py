# -*- coding: utf-8 -*-
import scrapy
import time
import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from reuters.items import ReutersItem


class RtSpider(scrapy.Spider):
    name = 'rt'
    allowed_domains = ['reuters.com']
    # start_urls = ['https://www.reuters.com/companies/AAPL.O/news']

    def __init__(self, code='', **kwargs):
        self.start_urls = [f'https://www.reuters.com/companies/{code}.O/news']
        super().__init__(**kwargs)

    def parse(self, response):
        options = Options()
        options.headless = True
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference('permissions.default.image', 2)
        firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
        browser = webdriver.Firefox(options=options,firefox_profile=firefox_profile)
    
        urls_list = set()
        l = 10000
        js = 'var q=document.documentElement.scrollTop=%d' %l

        browser.get(response.request.url)
        browser.execute_script(js)
        time.sleep(2)
        items_list = browser.find_elements_by_xpath('//*[@id="__next"]/div/div[4]/div[1]/div/div/div/div[2]/div/div/a')
        
        num_of_items = 0
        while num_of_items <= 125:
            num_of_items = len(items_list)
            l += 5000
            js = 'var q=document.documentElement.scrollTop=%d' %l
            browser.execute_script(js)
            time.sleep(2)
            items_list = browser.find_elements_by_xpath('//*[@id="__next"]/div/div[4]/div[1]/div/div/div/div[2]/div/div/a')

        for item in items_list:
            urls_list.add(item.get_attribute('href'))

        browser.quit()

        for url in urls_list:
            if re.match(r'https?://www.reuters.com/article/.*', url) != None: 
                request = scrapy.Request(url, callback=self.parse_reuters_news_contents)
                yield request
            else:
                continue

    # parse the news content from finance.yahoo.com/news/
    def parse_reuters_news_contents(self, response):
        item = ReutersItem()
        item['title'] = response.xpath('//*[@id="fusion-app"]/div/div[2]/div/div[1]/article/div/header/div/div[1]/h1/text()').extract_first()
        # item['dates'] = response.xpath('//*[@id="fusion-app"]/div/div[2]/div/div[1]/article/div/header/div/time/span[1]/text()').extract_first()
        item['dates'] = response.xpath('//meta[@name="article:published_time"]/@content').extract_first()
        yield item