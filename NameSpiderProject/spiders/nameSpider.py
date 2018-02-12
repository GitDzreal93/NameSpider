# -*- coding: utf-8 -*-
import scrapy


class NamespiderSpider(scrapy.Spider):
    name = "nameSpider"
    allowed_domains = ["www.yw11.com/namelist.php"]
    start_urls = ['http://www.yw11.com/namelist.php/']

    def parse(self, response):
        pass
