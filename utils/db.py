from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["subscription_db"]

users_collection = db["users"]
plans_collection = db["plans"]
subscriptions_collection = db["subscriptions"]
transactions_collection = db["transactions"]
