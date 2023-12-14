import configparser

from pymongo import MongoClient
from pymongo.collection import Collection

config = configparser.ConfigParser()
config.read("config.ini")
mongodb_url = config["DEFAULT"]["MONGODB_URL"]
client = MongoClient(mongodb_url)  # Use your actual MongoDB connection string
db = client.get_database("talktix")  # Use the 'talktix' database


def get_ticket_collection() -> Collection:
    return db.get_collection("ticket")


def get_user_collection() -> Collection:
    return db.get_collection("user")
