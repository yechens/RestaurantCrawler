# -*- coding: utf-8 -*-
import pymongo
from MeiTuanRestaurant.items import Comment
from MeiTuanRestaurant.settings import LOCAL_MONGO_PORT, LOCAL_MONGO_HOST, DB_NAME
from pymongo.errors import DuplicateKeyError


class MongoDBPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient(LOCAL_MONGO_HOST, LOCAL_MONGO_PORT)
        db = self.client[DB_NAME]
        # 对应mongodb数据库中的三张表
        self.Comment = db['Comment']

    def process_item(self, item, spider):
        """ 判断item的类型，并作相应的处理，再入数据库 """
        if isinstance(item, Comment):
            self.insert_item(self.Comment, item)
        return item

    @staticmethod
    def insert_item(collection, item):
        try:
            collection.insert_one(dict(item))
        except DuplicateKeyError:
            pass

    def close_spider(self, spider):
        self.client.close()
