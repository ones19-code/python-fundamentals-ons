from pymongo_utils import get_client, to_object_id

def users_collection():
    client = get_client()
    return client['appdb']['users']

def create_user(doc):
    col = users_collection()
    res = col.insert_one(doc)
    return str(res.inserted_id)

def get_user_by_id(user_id):
    col = users_collection()
    _id = to_object_id(user_id)
    doc = col.find_one({"_id": _id})
    if doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
    return doc

def update_user(user_id, update_dict):
    col = users_collection()
    _id = to_object_id(user_id)
    result = col.update_one({"_id": _id}, {"$set": update_dict})
    return result.modified_count
