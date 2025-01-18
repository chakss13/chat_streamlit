from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import gridfs
import os

# MongoDB connection URI from environment variable
MONGO_URI = os.getenv(" cluster0-shard-00-00.y2d81.mongodb.net:27017", "mongodb://localhost:27017/")


# Initialize MongoDB client with a timeout to catch connection issues
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.server_info()  # This will raise an exception if the connection fails
    print("Connected to MongoDB successfully!")
except ServerSelectionTimeoutError as err:
    print(f"Failed to connect to MongoDB: {err}")
    client = None

# Define the database and collections if the connection is successful
if client:
    db = client['messaging_app']
    users_collection = db['users']
    messages_collection = db['messages']
    fs = gridfs.GridFS(db)  # Initialize GridFS
