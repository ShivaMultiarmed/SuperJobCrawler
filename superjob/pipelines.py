# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class SuperjobPipeline:

    def open_spider(self, spider):
        self.mongo_client = MongoClient('mongodb://127.0.0.1:27017')
        self.db = self.mongo_client.get_database('superjob_db')
        self.collection = self.db.get_collection('superjob_collection')

    def close_spider(self, spider):
        self.mongo_client.close()

    def __add_to_collection(self, item):
        self.collection.insert_one(dict(item))
    def process_item(self, item, spider):
        self.__add_to_collection(item)
        return item
