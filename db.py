from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import gridfs

MONGO_URI = "mongodb+srv://<admin>:<admin>@cluster0.y2d81.mongodb.net/messaging_app?retryWrites=true&w=majority"

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.server_info()  # Force connection on a request as a test
    print("Connected to MongoDB successfully!")
except ServerSelectionTimeoutError as err:
    print(f"Failed to connect to MongoDB: {err}")
    client = None

db = client['messaging_app'] if client else None
users_collection = db['users'] if db else None
messages_collection = db['messages'] if db else None
fs = gridfs.GridFS(db) if db else None
