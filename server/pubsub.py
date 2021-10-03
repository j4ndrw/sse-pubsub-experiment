from typing import *

from flask import Response
from pymongo.collection import Collection

from utils import MessageSystem

def subscribe(
    collection: Collection, 
    username: str
) -> Optional[Generator[str, None, None]]:
    message_system = MessageSystem(collection)

    # Check if user is in DB
    # If they're not, create that user
    user_criterion = {"username": username}
    user = message_system.find_user(user_criterion)
    if user is None:
        user = message_system.create_user({ 
            "username": username,
            "connected": True,
            "messages": [],
            "sent_messages": [],
        })

    sent_messages = user["sent_messages"]
    if len(sent_messages) > 0:
        for message in sent_messages:
            yield f"data: {message} \n\n"

    # Event loop
    while True:
        # If the user is not connected, exit out of the loop
        user = message_system.find_user(user_criterion)
        if not user["connected"]:
            return

        # Publish any messages in the user entity
        messages = user["messages"]
        if user and len(messages) > 0:        
            for message in messages:
                yield f"data: {message} \n\n"

        message_system.update_messages(user)

def connect(collection: Collection, username: str) -> Response:
    message_system = MessageSystem(collection)
    user_criterion = {"username": username}
    user = message_system.find_user(user_criterion)
    if user is not None:
        # If the user isn't connected, connect them
        if not user["connected"]:
            message_system.update_connection_status(user, True)
    return Response("OK", 200)

def disconnect(collection: Collection, username: str) -> Response:
    message_system = MessageSystem(collection)
    user_criterion = {"username": username}
    user = message_system.find_user(user_criterion)
    if user is not None:
        # If the user is connected, disconnect them
        if user["connected"]:
            message_system.update_connection_status(user, False)
    return Response("OK", 200)
