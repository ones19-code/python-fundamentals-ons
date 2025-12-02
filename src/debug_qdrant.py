from db.qdrant import qdrant
from config.settings import COLLECTION_NAME

def debug_qdrant():
    points, next_page = qdrant.scroll(collection_name=COLLECTION_NAME, limit=500)

    print("============================================")
    print("Nombre de chunks en base :", len(points))
    print("============================================")

    for p in points:
        print("\n----------------------------------------")
        print("ID :", p.id)
        print("Texte :", p.payload.get("text"))
        print("----------------------------------------")

if __name__ == "__main__":
    debug_qdrant()
