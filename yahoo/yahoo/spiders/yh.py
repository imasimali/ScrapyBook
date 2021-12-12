# -*- coding: utf-8 -*-
import scrapy
import sys
import datetime
import csv
import time
import dateparser
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
#from scrapy.selector import HtmlXPathSelector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from scrapy.selector import Selector


from yahoo.items import YahooItem

#reload(sys)
#sys.setdefaultencoding('utf-8')
# print("Examples of Stocks Symbols are : AAPL, TSLA, NFLX, CAT")
# symbol=input("Enter Symbol of Stock : ")

# Load command line parameters
# init_url = f"https://finance.yahoo.com/quote/{symbol}/news?p={symbol}"
nextpage_pattern = '//*[@id="render-target-default"]/div/div[3]'
block_pattern = '//*[@id="latestQuoteNewsStream-0-Stream"]/ul/li/div/div'
title_pattern = '//*[@id="quoteNewsStream-0-Stream"]/ul/li/div/div/div[2]/h3/a/text()'
date_pattern = '//*[@id="quoteNewsStream-0-Stream"]/ul/li/div/div/div[2]/div/span[2]/text()'
FILE_NAME = 'AAPL'

class YhSpider(scrapy.Spider):
    name = 'yh'
    allowed_domains = ['finance.yahoo.com']
    start_urls = ['https://finance.yahoo.com/quote/BTC?p=BTC']

    # def start_requests(self):
    #     url = "http://quotes.toscrape.com"
    #     yield scrapy.Request(url=url, callback=self.parse_url)
  
    def parse(self, response):
        options = Options()
        options.headless = True
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference('permissions.default.image', 2)
        firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
        driver = webdriver.Firefox(options=options,firefox_profile=firefox_profile)

        driver.get(response.url)


        sel = Selector(text=driver.page_source)

        title = sel.xpath(title_pattern).get()
        dates = sel.xpath(date_pattern).get()




        item = YahooItem()
        item["title"] = title
        item["dates"] = dates
        yield item