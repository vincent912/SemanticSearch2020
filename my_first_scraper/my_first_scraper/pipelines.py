## -*- coding: utf-8 -*-
#
## Define your item pipelines here
##
## Don't forget to add your pipeline to the ITEM_PIPELINES setting
## See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#
#
#class MyFirstScraperPipeline:
#    def process_item(self, item, spider):
#        return item




import json

class JsonWriterPipeline:
    
    def open_spider(self, spider):
        self.file = open('items.jl', 'w')
    
    def close_spider(self, spider):
        self.file.close()
    
    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
