# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

class TikiscraperPipeline:
    def process_item(self, item, spider):
        return item
    

class SaveToMongodbPipeline:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client['tiki_crawl']
        self.collection = self.db['product_tiki']

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        self.collection.insert_one(item)
        print("*" * 150)
        adapter = ItemAdapter(item)
        adapter.pop('_id')
        return item
    def close_spider(self, spider):
        self.client.close()



