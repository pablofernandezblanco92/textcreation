import pymongo


class DatabaseAccessor:

    def __init__(self, host_name, database_name, collection_name):
        self.__host_name = host_name
        self.__database_name = database_name
        self.__collection_name = collection_name
        self.__client = None
        self.__database = None
        self.__collection = None

    def connect(self):
        self.__client = pymongo.MongoClient(self.__host_name)
        self.__database = self.__client[self.__database_name]
        self.__collection = self.__database[self.__collection_name]

    def close(self):
        self.__client.close()

    def insert(self, object_item):
        self.__collection.insert_one(object_item)
