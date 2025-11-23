"""Load data from DataFrame to MariaDB using pandas."""
import pandas as pd
from typing import Tuple
from sqlalchemy.orm import Session

from models.relational import ScientificArticle, Author
from storage.mariadb import mariadb_connection

def save_article_to_mariadb(row: pd.Series) -> Tuple[int, int]:
    """
    Save a single article to MariaDB and return IDs.
    
    Args:
        row: DataFrame row with article data
        
    Returns:
        Tuple of (article_id, author_id)
    """
    session_gen = mariadb_connection.get_session()
    session: Session = next(session_gen)
    
    try:
        # Check if author exists
        author = session.query(Author).filter_by(
            full_name=row['author_full_name']
        ).first()
        
        if not author:
            author = Author(
                full_name=row['author_full_name'],
                title=row['author_title']
            )
            session.add(author)
            session.flush()
        
        # Check if article exists
        existing_article = session.query(ScientificArticle).filter_by(
            arxiv_id=row['arxiv_id']
        ).first()
        
        if not existing_article:
            article = ScientificArticle(
                title=row['title'],
                summary=row['summary'],
                file_path=row['file_path'],
                arxiv_id=row['arxiv_id'],
                author_id=author.id
            )
            session.add(article)
            session.flush()
            article_id = article.id
        else:
            article_id = existing_article.id
        
        session.commit()
        return (article_id, author.id)
        
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def load_dataframe_to_mariadb(df: pd.DataFrame) -> pd.DataFrame:
    """
    Load DataFrame data to MariaDB and add IDs back to DataFrame.
    
    Args:
        df: DataFrame with article data
        
    Returns:
        DataFrame with added MariaDB IDs
    """
    # Use apply to save each row and get IDs
    id_results = df.apply(save_article_to_mariadb, axis=1)
    
    # Extract IDs and add to DataFrame
    df['mariadb_article_id'] = [result[0] for result in id_results]
    df['mariadb_author_id'] = [result[1] for result in id_results]
    
    return df