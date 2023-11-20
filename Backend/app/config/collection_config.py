import configparser
from typing import Any

from pymongo import MongoClient
from pymongo.collection import Collection


def get_ticket_collection() -> Collection:
    config = configparser.ConfigParser()
    config.read("config.ini")
    mongodb_url = config["DEFAULT"]["MONGODB_URL"]
    client = MongoClient(mongodb_url)  # Use your actual MongoDB connection string
    db = client.get_database("talktix")  # Use the 'talktix' database
    return db.get_collection("ticket")
