# src/processing/chunker.py

def split_text_into_chunks(text: str, size: int = 200, overlap: int = 20):
    """
    Découpe un texte en plusieurs chunks (morceaux) de taille fixe.
    
    - size     : taille maximale d’un chunk (en mots)
    - overlap  : nombre de mots qui se répètent entre chunks (pour le contexte)
    """

    words = text.split()
    chunks = []
    step = size - overlap  # avancer sans perdre le contexte

    for i in range(0, len(words), step):
        chunk_words = words[i:i + size]

        if not chunk_words:
            continue

        chunks.append(" ".join(chunk_words))

        # si on arrive à la fin du texte, on stoppe
        if i + size >= len(words):
            break

    return chunks
