# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import json


from scrapy.exceptions import DropItem
from scrapy.conf import settings


class TransparencyPipeline(object):
    def process_item(self, item, spider):
        return item

class StateFilterPipeline(object):
    def process_item(self, item, spider):
        if item['state'] in settings['STATE_TO_FILTER']:
            return item
        else:
            raise DropItem('Not in PARAIBA motherfucker')

class JsonWriterPipeline(object):

    def __init__(self):
        self.faults = {}

    def process_item(self, item, spider):
        # Here be dragons 
        if item['deputy'] not in self.faults:
            self.faults[item['deputy']] = []
        item_dic = dict(item)
        del item_dic['deputy']
        self.faults[item['deputy']].append(item_dic)
        line = json.dumps(self.faults)
        self.file = open('items.json', 'wb')
        self.file.write(line)
        return item
