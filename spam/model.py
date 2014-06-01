# -*- coding: utf-8 -*-

from pymongo import MongoClient
from bson import ObjectId


class Model(dict):
    __database__ = None
    __collection__ = None
    __dburi__ = None

    @classmethod
    def getClient(cls):
        if hasattr(cls, "_client"):
            client = cls._client
        else:
            client = MongoClient(cls.__dburi__)
            cls._client = client
        return client

    @classmethod
    def getCollection(cls):
        return cls.getClient()[cls.__database__][cls.__collection__]

    @classmethod
    def findOne(cls, *args, **kw):
        kw["as_class"] = cls
        return cls.getCollection().find_one(*args, **kw)

    @classmethod
    def findDocs(cls, *args, **kw):
        kw["as_class"] = cls
        return cls.getCollection().find(*args, **kw)

    @classmethod
    def updateDocs(cls, *args, **kw):
        return cls.getCollection().update(*args, **kw)

    @classmethod
    def removeDocs(cls, *args, **kw):
        return cls.getCollection().remove(*args, **kw)

    @classmethod
    def group(cls, key, condition, initial, reduce, finalize=None):
        return cls.getCollection().group(key, condition, initial, reduce, finalize)

    def save(self, *args, **kw):
        return self.getCollection().save(self, *args, **kw)

    @classmethod
    def aggregate(cls, pipeline):
        return cls.getCollection().aggregate(pipeline)

    @classmethod
    def dropCollection(cls):
        return cls.getCollection().drop()


class Record(Model):
    __database__ = 'spam'
    __collection__ = 'log'
    __dburi__ = 'mongodb://db.taiben.com:27017/'

    @classmethod
    def create(cls):
        return cls({
            "_id"       : ObjectId(), 
            "ip"        : "",           # 访问ip
            "name"      : "",           # 用户名称
            "url"       : "",           # 访问页面
            "time"      : None,           # 访问时间
        })

