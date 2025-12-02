from embeddings.embedder import embed_texts
from models.chunk_metadata import ChunkMetadata
from processing.dataframe import explode_articles_to_chunks
from indexing.exists import chunk_exists
from indexing.insert import save_chunk

def index_new_chunks(df):

    df_chunks = explode_articles_to_chunks(df)

    # filtrer la liste
    new_rows = df_chunks[~df_chunks["point_id"].apply(chunk_exists)]

    if new_rows.empty:
        print("Aucun nouveau chunk à indexer.")
        return

    vectors = embed_texts(new_rows["text"].tolist())

    for row, vector in zip(new_rows.to_dict("records"), vectors):
        metadata = ChunkMetadata(
            article_id=row["article_id"],
            chunk_id=row["chunk_id"],
            title=row.get("title"),
            source=row.get("source"),
            url=row.get("url"),
            created_at=row.get("created_at"),
            text=row["text"]
        )

        save_chunk(row["point_id"], vector, metadata.model_dump())

    print(f"{len(new_rows)} chunks indexés dans Qdrant.")
