"""Transfer data from DataFrame to MongoDB."""
import pandas as pd
from typing import List
import re

from models.document import ScientificArticleDocument, AuthorEmbedded

def extract_text_from_html(html_content: str) -> str:
    """
    Extract clean text from HTML content.
    
    Args:
        html_content: HTML content as string
        
    Returns:
        Clean text content
    """
    # Remove HTML tags
    text = re.sub('<[^<]+?>', ' ', html_content)
    # Remove extra whitespace
    text = re.sub('\s+', ' ', text)
    # Remove specific ArXiv elements
    text = re.sub(r'arXiv:\d+\.\d+v\d+\[\w+\.\w+\]', '', text)
    return text.strip()

def save_article_to_mongodb(row: pd.Series) -> None:
    """
    Save a single article to MongoDB.
    
    Args:
        row: DataFrame row with article data
    """
    # Check if document already exists
    existing_doc = ScientificArticleDocument.objects(arxiv_id=row['arxiv_id']).first()
    
    if not existing_doc:
        # Extract text from HTML content
        html_text = extract_text_from_html(row.get('html_content', ''))
        
        # Create embedded author document
        author_embedded = AuthorEmbedded(
            full_name=row['author_full_name'],
            title=row['author_title']
        )
        
        # Create MongoDB document with optional MariaDB IDs
        mongo_doc = ScientificArticleDocument(
            title=row['title'],
            summary=row['summary'],
            file_path=row['file_path'],
            arxiv_id=row['arxiv_id'],
            author=author_embedded,
            text=html_text
        )
        
        # Add MariaDB IDs if they exist in the DataFrame
        if 'mariadb_article_id' in row and pd.notna(row['mariadb_article_id']):
            mongo_doc.mariadb_article_id = int(row['mariadb_article_id'])
        if 'mariadb_author_id' in row and pd.notna(row['mariadb_author_id']):
            mongo_doc.mariadb_author_id = int(row['mariadb_author_id'])
        
        mongo_doc.save()

def load_dataframe_to_mongodb(df: pd.DataFrame) -> None:
    """
    Load DataFrame data to MongoDB.
    
    Args:
        df: DataFrame with article data
    """
    # Use apply to save each row to MongoDB
    df.apply(save_article_to_mongodb, axis=1)
    print(f"Successfully transferred {len(df)} articles to MongoDB")