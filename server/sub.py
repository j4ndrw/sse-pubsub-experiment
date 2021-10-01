import time
from typing import *

from flask import Response
from pymongo.collection import Collection

def subscribe(message_system: Collection, username: str) -> Optional[Generator[str, None, None]]:
    if message_system.find_one({"username": username}) is None:
        message_system.insert_one({ 
            "username": username,
            "connected": True,
            "messages": [],
            "sent_messages": [],
        })

    user = message_system.find_one({"username": username})
    if len(messages := user["sent_messages"]) > 0:
        for message in messages:
            yield f"data: {message}\n\n"

    while True:
        user = message_system.find_one({"username": username})
        if not user["connected"]:
            return

        if user and len(messages := user["messages"]) > 0:
            print(f"Sending messages!: {messages}")
            for message in messages:
                yield f"data: {message}\n\n"           
            
            message_system.update_one(user, {
                "$set": {
                    "sent_messages": [*user["sent_messages"], *messages],
                    "messages": []
                }
            })

def connect(message_system: Collection, username: str) -> Response:
    if (user := message_system.find_one({"username": username})) is not None:
        if not user["connected"]:
            print(f"{username} connected!")
            message_system.update_one(user, {
                "$set": {
                    "connected": True 
                }
            })
    return Response("OK", 200)

def disconnect(message_system: Collection, username: str) -> Response:
    if (user := message_system.find_one({"username": username})) is not None:
        if user["connected"]:
            print(f"{username} disconnected...")
            message_system.update_one(user, {
                "$set": {
                    "connected": False 
                }
            })
    return Response("OK", 200)
