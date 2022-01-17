# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from itemadapter import ItemAdapter
import logging
import pymongo
from datetime import datetime

class Covid19Pipeline(object):
    collection_name = "Nepal"

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        ## pull in information from settings.py
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGODB_DB')
        )
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        
        item = ItemAdapter(item)        
        temp_ts = item.get('day_timestamp')
        dt = [datetime.fromtimestamp(int(t)) for t in temp_ts]
        
        for row in range(10):
            data = {"day_timestamp":dt[row],"daily_change_percent":item.get("daily_change_percent")[row],"daily_increase":item.get("daily_increase")[row],"daily_confirmed_cases":item.get("daily_confirmed_cases")[row]}
            self.db[self.collection_name].insert_one(dict(data))

        logging.debug("Timeseires data added to MongoDb")
        return item
