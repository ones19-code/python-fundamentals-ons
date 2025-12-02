# src/indexing/exists.py
from db.qdrant import qdrant
from config.settings import COLLECTION_NAME

def chunk_exists(point_id: int) -> bool:
    result = qdrant.retrieve(
        collection_name=COLLECTION_NAME,
        ids=[int(point_id)],
    )
    return len(result) > 0


