
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

    message_system: Collection = db.messagesystem

    while True:
        message = input("Enter a message to broadcast: ")

        users: Cursor = message_system.find({})
        for user in users:
            new_messages = [*user["messages"], message]
            message_system.update_one({"_id": user["_id"]}, {
                "$set": { 
                    "messages": new_messages 
                }
            })

        