from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import gridfs

MONGO_URI = "cluster0-shard-00-00.y2d81.mongodb.net:27017"

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.server_info()
    print("Connected to MongoDB successfully!")
except ServerSelectionTimeoutError as err:
    print(f"Failed to connect to MongoDB: {err}")
    client = None

if client:
    db = client['messaging_app']
    users_collection = db['users']
    messages_collection = db['messages']
    fs = gridfs.GridFS(db)
else:
    users_collection = None
    messages_collection = None
    fs = None
