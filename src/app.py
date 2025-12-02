# src/app.py
import pandas as pd
from db.qdrant import create_collection_if_not_exists
from indexing.pipeline import index_new_chunks
from search.search_engine import search_chunks

if __name__ == "__main__":
    print("=== Initialisation Qdrant ===")
    create_collection_if_not_exists()

    print("=== Chargement des articles ===")
    df = pd.read_json("data/articles.json")

    print("=== Indexation des nouveaux chunks ===")
    index_new_chunks(df)

    print("=== Test recherche ===")
    results = search_chunks("Pourquoi la base de données plante ?", limit=3)

    if not results:
        print("Aucun résultat trouvé.")
    else:
        for score, point in results:
            print("\nScore:", score)
            print("Chunk:", point.payload.get("text", "(pas de texte)"))
            print("ID:", point.id)
            print("------")

