# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class Zhongbiao2Pipeline(object):
    #def process_item(self, item, spider):
        #return item
    def __init__(self):
        self.f2 = open("第二部分爬取内容筛选结果2.json","w")
        #self.f1 = open("第二部分爬取内容.json","w")

    def process_item(self, item, spider):
        content = json.dumps(dict(item),ensure_ascii = False) + ",\n"
        #content1 = json.dumps(dict(information),ensure_ascii = False + ",\n")
        self.f2.write(content)
        #self.f1.write(information)
        #return information
        return item

    def close_spider(self,spider):
        self.f2.close()
        #self.f1.close()



