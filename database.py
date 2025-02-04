from pymongo import MongoClient

# Initialize MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["customer_support"]

# Define collections
network_status_collection = db["network_status"]
tickets_collection = db["tickets"]