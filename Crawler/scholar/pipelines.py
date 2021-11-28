# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface

from itemadapter import ItemAdapter
from scholar.items import ScholarAuthorItem, ScholarPaperItem
from pymongo import MongoClient


class ScholarPipeline:
    def __init__(self):
        self.client = MongoClient(host='121.5.169.182', port=28887, username='scholar', password='r4u30dYkgeqVdlaR')
        self.database = self.client.scholar
        self.collection_author = self.database.scholarAuthor
        self.collection_paper = self.database.scholarPaper

    def process_item(self, item, spider):
        if isinstance(item, ScholarAuthorItem):
            self.collection_author.update({'id': item['id']}, {'$set': item.__dict__}, True)
        else:
            self.collection_paper.update({'id': item['id']}, {'$set': item.__dict__}, True)
        return item
