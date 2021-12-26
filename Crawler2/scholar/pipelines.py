# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
from scholar.items import AminerItem


class AminerPipeline:
    def __init__(self):
        # self.client = pymongo.MongoClient('localhost')
        self.client = pymongo.MongoClient(
            'mongodb://scholar:r4u30dYkgeqVdlaR@121.5.169.182:28887/admin')
        self.db = self.client['scholar']
        self.table1 = self.db['aminer_researcher']
        self.table2 = self.db['aminer_paper']
        self.table1.drop()
        self.table2.drop()
        # self.crawled1 = set()
        # for item in self.table1.find({}, {"_id":0, "id":1}):
        # self.crawled1.add(item['id'])
        # self.crawled2 = set()
        # for item in self.table2.find({}, {"_id":0, "id":1}):
        # self.crawled2.add(item['id'])

    def process_item(self, item, spider):
        if isinstance(item, AminerItem):
            # if item['id'] not in self.crawled1:
            self.table1.insert_one(dict(item))
        else:
            # if item['id'] not in self.crawled2:
            self.table2.insert_one(dict(item))
        return item


class SemanticPipeline:
    def __init__(self):
        # self.client = pymongo.MongoClient('localhost')
        self.client = pymongo.MongoClient(
            'mongodb://scholar:r4u30dYkgeqVdlaR@121.5.169.182:28887/admin')
        self.db = self.client['scholar']
        self.table1 = self.db['aminer_researcher']
        self.table2 = self.db['aminer_paper']
        # self.table1.drop()
        # self.table2.drop()
        self.crawled1 = set()
        for item in self.table1.find():
            self.crawled1.add(item['id'])
        self.crawled2 = set()
        for item in self.table2.find():
            self.crawled2.add(item['id'])

    def process_item(self, item, spider):
        if isinstance(item, AminerItem):
            if item['id'] not in self.crawled1:
                self.table1.insert(dict(item))
        else:
            if item['id'] not in self.crawled2:
                self.table2.insert(dict(item))
        return item
