# -*- coding: utf-8 -*-
import scrapy


class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['https://www.collegedata.com/en/prepare-and-apply/common-application-guide/']
    start_urls = ['http://https://www.collegedata.com/en/prepare-and-apply/common-application-guide//']

    def parse(self, response):
        pass
