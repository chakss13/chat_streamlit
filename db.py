# db.py

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import gridfs

# MongoDB connection URI
MONGO_URI = "mongodb://localhost:27017/"

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