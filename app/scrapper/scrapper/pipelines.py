from dataclasses import asdict

import pymongo
from itemadapter import ItemAdapter
from scrapper.items import ScrapperItem
from scrapy.utils.project import get_project_settings

"""settings = get_project_settings()
class MongoDBPipeline:
    def __init__(self):
        connection = pymongo.MongoClient(
            settings.get("MONGO_HOST"),
            settings.get("MONGO_PORT")
        )
        db = connection[settings.get("MONGO_DB_NAME")]
        self.collection = db[settings["MONGO_COLLECTION_NAME"]]

    def process_item(self, item, spider):
        data = dict(ScrapperItem(item))
        self.collection.insert_one(data)
        return data

"""


class MongoDBPipeline:
    """Item pipeline to write data to MongoDB"""

    def __init__(self, mongo_uri, mongo_db, mongo_coll):
        """Init Item pipeline with settings for MongoDB"""
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_collection = mongo_coll

    @classmethod
    def from_crawler(cls, crawler):
        """Create a pipeline instance from Crawler"""
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE", "offers"),
            mongo_coll=crawler.settings.get("MONGO_COLLECTION", "nofluff"),
        )

    def open_spider(self, spider):
        """Connect to MongoDB when the spider is opened"""
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.mongo_collection]

    def close_spider(self, spider):
        """Close the connection to MongoDB when the spider is closed"""
        self.client.close()

    def process_item(self, item, spider):
        item_dict = ItemAdapter(item).asdict()
        self.collection.insert_one(item_dict)
        return item
