from pymongo import MongoClient
from bson import ObjectId
MONGO_URI = "mongodb://appuser:apppass123@localhost:27017/appdb?authSource=admin"


def get_client(uri=MONGO_URI):
    return MongoClient(uri)

def to_object_id(id_like):
    try:
        return ObjectId(id_like)
    except:
        raise ValueError("Invalid ObjectId")
