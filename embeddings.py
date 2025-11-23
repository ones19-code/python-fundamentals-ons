import os
import json
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer



 




 # chnstaamel hugging face moush l atah prof khtr mush gratuit 


print("Loading embedding model...")

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

print("Model loaded successfully.\n")




phrases = [
    "anous mzyeeen.",
    "anous enssen behy .",
    "i love germany but my tunisia is my heart "
]

print("Generating embeddings for simple phrases...")

phrase_embeddings = model.encode(phrases)

print("Phrase embeddings generated.\n")



#  similarity

print("Computing cosine similarity matrix...")

similarity_matrix = cosine_similarity(phrase_embeddings)

print("Cosine similarity matrix:")
print(similarity_matrix)
print("\n")



# bch naamlee chargement 

print("Loading articles...")

article_files = [f for f in os.listdir("articles") if f.endswith(".txt")]

if not article_files:
    raise FileNotFoundError("No .txt files were found in the 'articles/' folder.")

titles = []
texts = []

for file in article_files:
    with open(os.path.join("articles", file), "r", encoding="latin-1", errors="ignore") as f:

        titles.append(file)
        texts.append(f.read())

df = pd.DataFrame({"title": titles, "text": texts})

print("Articles loaded:", df["title"].tolist(), "\n")



def chunk_text(text, chunk_size=300, overlap=50):
    words = text.split()
    chunks = []

    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks


print("Chunking texts...")

df["chunks"] = df["text"].apply(chunk_text)

total_chunks = sum(len(x) for x in df["chunks"])

print(f"Total chunks created: {total_chunks}\n")



print("Generating embeddings for all chunks...")

all_chunks_embeddings = []

for _, row in df.iterrows():
    title = row["title"]
    for chunk in row["chunks"]:
        emb = model.encode([chunk])[0]

        all_chunks_embeddings.append({
            "title": title,
            "text": chunk,
            "embedding": emb.tolist()
        })

print(f"Embeddings generated for {len(all_chunks_embeddings)} chunks.\n")




os.makedirs("data", exist_ok=True)

output_file = "data/article_embeddings.json"

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(all_chunks_embeddings, f, indent=2)

print(f"Embeddings saved to: {output_file}")
print("Assignment completed successfully.")
