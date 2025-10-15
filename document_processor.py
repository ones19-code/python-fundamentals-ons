from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional
import json


@dataclass
class Document:
    id: int
    title: str
    tags: List[str] = field(default_factory=list)
    published: bool = False
    metadata: Optional[Dict[str, object]] = None

def load_documents(file_path: str) -> List[Document]:
  
    base_path = Path(__file__).parent.parent 
    full_path = base_path / file_path

    if not full_path.exists():
        raise FileNotFoundError(f"{full_path} not found")

    with full_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    documents: List[Document] = []
    for doc_data in data:
        try:
            documents.append(Document(**doc_data))
        except TypeError as e:
            print(f"Type error for document {doc_data.get('id', 'Unknown')}: {e}")
    return documents

def display_documents(documents: List[Document]) -> None:
    for doc in documents:
        print(f"ID: {doc.id}")
        print(f"Title: {doc.title}")
        print(f"Tags: {', '.join(doc.tags) if doc.tags else 'No tags'}")
        print(f"Published: {doc.published}")
        if doc.metadata:
            for key, value in doc.metadata.items():
                print(f"{key.capitalize()}: {value}")
        print("-" * 30)

if __name__ == "__main__":

    docs = load_documents("data/documents.json")
    display_documents(docs)
