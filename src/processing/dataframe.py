# src/processing/dataframe.py
import pandas as pd
from processing.chunker import split_text_into_chunks

def explode_articles_to_chunks(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["chunks"] = df["content"].apply(split_text_into_chunks)

    df_chunks = df.explode("chunks").reset_index(drop=True)
    df_chunks = df_chunks.rename(columns={"chunks": "text"})

    df_chunks["chunk_id"] = df_chunks.groupby("article_id").cumcount()

    # point_id entier (ex: article 1 → 1000 + chunk_id)
    df_chunks["point_id"] = df_chunks["article_id"] * 1000 + df_chunks["chunk_id"]

    return df_chunks

