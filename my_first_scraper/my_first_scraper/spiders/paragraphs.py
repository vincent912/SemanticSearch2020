## -*- coding: utf-8 -*-
#import scrapy
#
#
#class ParagraphsSpider(scrapy.Spider):
#    name = 'paragraphs'
#    allowed_domains = ['https://www.mist.com/documentation/category/getting-started/']
#    start_urls = ['http://https://www.mist.com/documentation/category/getting-started//']
#
#    def parse(self, response):
#        pass




import scrapy

class LinkCheckerSpider(scrapy.Spider):
    name = 'paragraph_cralwer'
    allowed_domains = ['www.mist.com']
    # start_urls = ['https://www.mist.com/documentation']
    start_urls = ["https://www.mist.com/documentation/category/getting-started/"]

    def parse(self, response):
    # Get all the divisions with class entry-content
        all_content = response.xpath('//div[@class="entry-content"]/text()').getall()
        # Loop on each tag
        for content in all_content:
            content = content.strip()
            if content != "":
                yield {'text': content}



