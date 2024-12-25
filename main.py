from pymongo import MongoClient
from config import MONGO_URI, DATABASE_NAME

class MongoDBHandler:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[DATABASE_NAME]

    def create(self, collection_name, data):
        collection = self.db[collection_name]
        result = collection.insert_one(data)
        return str(result.inserted_id)

    def read(self, collection_name, query):
        collection = self.db[collection_name]
        documents = collection.find(query)
        return list(documents)

    def update(self, collection_name, query, update_data):
        collection = self.db[collection_name]
        result = collection.update_one(query, {"$set": update_data})
        return result.modified_count   

    def delete(self, collection_name, query):
        collection = self.db[collection_name]
        result = collection.delete_one(query)
        return result.deleted_count
