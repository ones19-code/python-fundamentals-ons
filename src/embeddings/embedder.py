# src/embeddings/embedder.py
import json
import numpy as np
import hashlib

W2V_PATH = "models/mini_w2v.json"

with open(W2V_PATH, "r", encoding="utf-8") as f:
    W2V = json.load(f)

EMBED_DIM = len(next(iter(W2V.values())))

def hash_vector(word: str):
    """Fallback : génère un vecteur déterministe via un hash."""
    h = hashlib.sha256(word.encode()).digest()
    rng = np.random.default_rng(int.from_bytes(h[:8], "big"))
    vec = rng.normal(0, 1, EMBED_DIM)
    return vec / np.linalg.norm(vec)

def embed_text(text: str):
    words = text.lower().split()
    vectors = []

    for w in words:
        if w in W2V:
            vectors.append(np.array(W2V[w]))
        else:
            vectors.append(hash_vector(w))

    if not vectors:
        return [0.0] * EMBED_DIM

    avg = np.mean(vectors, axis=0)
    avg = avg / np.linalg.norm(avg)
    return avg.tolist()

def embed_texts(texts):
    return [embed_text(t) for t in texts]



