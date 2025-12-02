# src/db/qdrant.py
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance
from config.settings import QDRANT_HOST, QDRANT_PORT, COLLECTION_NAME, VECTOR_SIZE

qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

def create_collection_if_not_exists():
    existing = [c.name for c in qdrant.get_collections().collections]

    if COLLECTION_NAME not in existing:
        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )
        print(f"Collection '{COLLECTION_NAME}' créée.")
    else:
        print(f"Collection '{COLLECTION_NAME}' déjà existante.")

