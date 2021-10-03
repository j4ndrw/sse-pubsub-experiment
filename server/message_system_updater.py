
import os
from typing import *

from pymongo.collection import Collection
from pymongo.cursor import Cursor
from pymongo.database import Database
from pymongo.mongo_client import MongoClient

if __name__ == '__main__':

    client: MongoClient = MongoClient(host="localhost", port=27017)
    db: Database = client["sse-pubsub-test"]
    if db is None:
        raise Exception("No database found")

    collection: Collection = db.messagesystem

    while True:
        message = input("Enter a message to broadcast: ")

        users: Cursor = collection.find({})
        for user in users:
            new_messages = [*user["messages"], message]
            collection.update_one({"_id": user["_id"]}, {
                "$set": { 
                    "messages": new_messages 
                }
            })

        