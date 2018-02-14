# -*- coding: utf-8 -*-
import scrapy
import logging
from scrapy.spiders import CrawlSpider
from NameSpiderProject.items import NamespiderprojectItem

base_url = 'https://www.yw11.com/'

class NamespiderSpider(scrapy.Spider):
    name = "nameSpider"
    allowed_domains = ["http://www.yw11.com"]
    start_urls = ['https://http://www.yw11.com/namelist.php']

    def parse(self, response):
        '''
        解析初始页面
        :param response:
        :return:
        '''
        item = NamespiderprojectItem()
        # 获取所有姓氏的url
        logging.info('起名网初始页（姓氏大全）请求成功 : -----url--->' + response.url)
        surname_a_all =response.xpath('//div[@class="listbox"]//ul//a')
        for surname_a in surname_a_all:
            # 取出姓氏
            item['surname'] = surname_a.xpath('text()').extract()
            logging.info('当前正在爬取的姓氏是：-----surname--->' + item['surname'])
            surname_url = surname_a.xpath('@href').extract()
            surname_url = base_url+surname_url
            # 解析每个姓氏的名字数据
            request = scrapy.Request(surname_url, callback=self.parse_peer_surname, meta={'item': item})
            yield request

    def parse_peer_surname(self, response):
        '''
        解析每个姓氏下面的名字,分别产生男生和女生的url
        :param response:
        :return:
        '''
        # 获取所有的性别
        logging.info('起名网二级页面（某姓氏）请求成功 : -----url--->' + response.url)
        sex_list_a_all = response.xpath('//div[@class="listbox1_title"]//a')
        item = response.meta['item']
        for sex_url_a in sex_list_a_all:
            # 遍历性别a标签
            sex_url = sex_url_a.xpath('@href').extract()
            #从url中解析出用户的性别，0：男孩， 1：女孩
            item['sex'] = sex_url[-7]
            logging.info('当前正在爬取的性别是：-----sex--->【' + item['sex'] + '】【0：男孩；1：女孩】')
            item['category'] = sex_url_a.xpath('text()').extract()
            sex_url = base_url + sex_url
            request = scrapy.Request(sex_url,callback=self.parse_name,meta={'item':item})
            yield request

    def parse_name(self,response):
        '''
        解析 姓氏/性别/名字
        :param response:
        :return:
        '''
        logging.info('起名网三级页面（某姓氏下的某性别）请求成功 : -----url--->' + response.url)
        name_li_all = response.xpath('//div[@class="listbox1_text"]//li')
        item = response.meta['item']
        for name in name_li_all:
            item['name'] = name.xpath('text()').extract()
            yield item






