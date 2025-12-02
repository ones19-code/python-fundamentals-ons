import numpy as np
from embeddings.embedder import embed_text
from db.qdrant import qdrant
from config.settings import COLLECTION_NAME

def cosine_similarity(a, b):
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)

    if a is None or b is None:
        return 0.0

    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.0

    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def search_chunks(query: str, limit=5):
    # 1) Embed la requête
    query_vec = embed_text(query)

    # 2) Récuperation des points Qdrant
    points = []
    next_page = None

    while True:
        scrolled, next_page = qdrant.scroll(
            collection_name=COLLECTION_NAME,
            limit=100,
            offset=next_page,
            with_vectors=True
        )

        points.extend(scrolled)

        if next_page is None:
            break

    if len(points) == 0:
        print("⚠ Aucun chunk trouvé dans Qdrant.")
        return []

    # 3) Calculer la similarité cosinus
    scored = []
    for p in points:
        sim = cosine_similarity(query_vec, p.vector)
        scored.append((sim, p))

    # 4) Trier du plus similaire au moins similaire
    scored.sort(key=lambda x: x[0], reverse=True)

    # 5) AFFICHER les scores pour debug
    print("\n===== Scores de similarité =====")
    for sim, p in scored[:limit]:
        print(f"Score: {sim:.4f} → ID: {p.id}")

    print("================================\n")

    return scored[:limit]





