import os

from flask import Flask, Response
from flask_cors import CORS
from pymongo.database import Database
from pymongo.mongo_client import MongoClient

import sub

app = Flask(__name__)

client: MongoClient = MongoClient(host="localhost", port=27017)
db: Database = client["sse-pubsub-test"]
CORS(app)

@app.route("/pubsub/connect/<username>", methods=["GET"])
def connect(username: str) -> Response:
    return sub.connect(db.messagesystem, username)

@app.route("/pubsub/subscribe/<username>", methods=["GET"])
def subscribe(username: str) -> Response:
    return Response(
        sub.subscribe(db.messagesystem, username), 
        content_type="text/event-stream"
    )

@app.route("/pubsub/disconnect/<username>", methods=["GET"])
def disconnect(username: str) -> Response:
    return sub.disconnect(db.messagesystem, username)

if __name__ == "__main__":
    if db.get_collection("messagesystem") is None:
        db.create_collection("messagesystem")
        
    app.run(port=8000, debug=True)
