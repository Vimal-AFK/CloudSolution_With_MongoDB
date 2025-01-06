from pymongo import MongoClient
from .database_interface import DatabaseInterface

class CloudDatabase(DatabaseInterface):
    def __init__(self, mongo_uri, db_name, collection_name):
        self.client = MongoClient(mongo_uri)
        self.collection = self.client[db_name][collection_name]

    def enqueue_data(self, data: dict):
        self.collection.insert_one(data)

    def dequeue_data(self) -> dict:
        raise NotImplementedError("Dequeue not supported for Cloud Database.")

    def get_all_data(self) -> list:
        return list(self.collection.find().sort("_id", -1))
