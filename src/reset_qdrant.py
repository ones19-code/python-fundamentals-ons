from db.qdrant import qdrant
from config.settings import COLLECTION_NAME

print("Suppression de la collection :", COLLECTION_NAME)
qdrant.delete_collection(collection_name=COLLECTION_NAME)
print("OK. Collection supprimée.")
