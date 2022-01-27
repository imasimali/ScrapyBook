# -*- coding: utf-8 -*-
import scrapy
import time
import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from yahoo.items import YahooItem

class YhSpider(scrapy.Spider):
    name = 'yh'
    allowed_domains = ['finance.yahoo.com']
    # start_urls = ['https://finance.yahoo.com/quote/'+company+'/news']

    def __init__(self, code='', **kwargs):
        self.start_urls = [f'https://finance.yahoo.com/quote/{code}/news']
        super().__init__(**kwargs)

    def parse(self, response):
        options = Options()
        options.headless= True
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
        items_list = browser.find_elements_by_xpath('//*[@id="latestQuoteNewsStream-0-Stream"]/ul/li/div/div/div[2]/h3/a')
        
        num_of_items = 0
        while num_of_items != len(items_list):
            num_of_items = len(items_list)
            if num_of_items > 200:
              break
            l += 5000
            js = 'var q=document.documentElement.scrollTop=%d' %l
            browser.execute_script(js)
            time.sleep(2)
            items_list = browser.find_elements_by_xpath('//*[@id="latestQuoteNewsStream-0-Stream"]/ul/li/div/div/div[2]/h3/a')

        for item in items_list:
            urls_list.add(item.get_attribute('href'))

        browser.quit()

        for url in urls_list:
            if re.match(r'https?://finance.yahoo.com/news/.*', url) != None: 
                request = scrapy.Request(url, callback=self.parse_yahoo_news_contents)
                yield request
            else:
                continue

    # parse the news content from finance.yahoo.com/news/
    def parse_yahoo_news_contents(self, response):
        item = YahooItem()
        item['title'] = response.xpath('//header/h1/text()').extract_first()
        item['dates'] = response.xpath('/html/body/div/div/main/div/div/div/div/div/article/div/div/div/div/div/div/div/div/div/div/time/@datetime').extract_first()
        yield item