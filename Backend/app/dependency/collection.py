import configparser
import os

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.collection import Collection

load_dotenv()
mongodb_url = os.getenv("MONGODB_URL")
client = MongoClient(mongodb_url)  # Use your actual MongoDB connection string
db = client.get_database("talktix")  # Use the 'talktix' database


def get_ticket_collection() -> Collection:
    return db.get_collection("ticket")


def get_user_collection() -> Collection:
    return db.get_collection("user")


def get_service_collection() -> Collection:
    return db.get_collection("service")


def get_department_collection() -> Collection:
    return db.get_collection("department")


def get_category_collection() -> Collection:
    return db.get_collection("category")


def get_location_collection() -> Collection:
    return db.get_collection("location")
