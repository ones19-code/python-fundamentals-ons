# src/indexing/insert.py
from qdrant_client.http.models import PointStruct
from db.qdrant import qdrant
from config.settings import COLLECTION_NAME

def save_chunk(point_id, vector, payload):
    point = PointStruct(
        id=int(point_id),     # ID entier, comme Qdrant le veut
        vector=vector,
        payload=payload,
    )

    qdrant.upsert(
        collection_name=COLLECTION_NAME,
        points=[point],
    )
