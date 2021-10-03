from functools import partial
from typing import *

from pymongo.collection import Collection

class MessageSystem:
    def __init__(self, collection: Collection):
        self.collection = collection

    def find_user(
        self, 
        criterion: Dict[str, str]
    ) -> Optional[Dict[str, Any]]:
        return self.collection.find_one(criterion)

    def create_user(
        self,
        user: Dict[str, Any]
    ) -> Dict[str, Any]:
        self.collection.insert_one(user)
        return user

    def update_user(
        self,
        user: Dict[str, Any],
        payload: Dict[str, Any]
    ) -> None:
        self.collection.update_one(user, payload)

    def update_messages(self, user: Dict[str, Any]):
        messages = user["messages"]
        if user and len(messages) > 0:
            self.update_user(user, {
                "$set": {
                    "sent_messages": [
                        *user["sent_messages"], 
                        *messages
                    ],
                    "messages": []
                }
            })

    def update_connection_status(self, user: Any, status: bool):
        print(
            f"{user['username']} \
            {'connected!' if status == True else 'disconnected...'}"
        )
        self.update_user(user, {
            "$set": {
                "connected": status
            }
        })