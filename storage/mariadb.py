import mysql.connector
from mysql.connector import Error
from typing import Dict, Any
import pandas as pd

def create_mariadb_tables(connection_params: dict):
    """
    Create necessary tables in MariaDB
    """
    try:
        conn = mysql.connector.connect(**connection_params)
        cursor = conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title TEXT NOT NULL,
            authors TEXT,
            year INT,
            abstract TEXT,
            arxiv_id VARCHAR(50),
            url TEXT,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        print(" MariaDB tables created successfully")
        
    except Error as e:
        print(f"Error creating MariaDB tables: {e}")

def load_data_to_mariadb(df: pd.DataFrame, connection_params: dict) -> pd.DataFrame:
    """
    Load DataFrame to MariaDB using .apply() and return DataFrame with IDs
    """
    def process_article_row(row: pd.Series) -> Dict[str, Any]:
        """
        Process single article row and return IDs using .apply()
        """
        try:
            conn = mysql.connector.connect(**connection_params)
            cursor = conn.cursor()
            
            # Insert article
            article_query = """
            INSERT INTO articles (title, authors, year, abstract, arxiv_id, url, content)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(article_query, (
                str(row['title']),
                str(row['authors']),
                int(row['year']),
                str(row['abstract']),
                str(row['arxiv_id']),
                str(row['url']),
                str(row.get('content', ''))
            ))
            article_id = cursor.lastrowid
            
            # For simplicity, using article_id as author_id
            author_id = article_id
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return {
                'mariadb_article_id': article_id,
                'mariadb_author_id': author_id
            }
            
        except Error as e:
            print(f"Error processing article '{row['title'][:50]}...': {e}")
            return {'mariadb_article_id': None, 'mariadb_author_id': None}
    
    print(" Loading data to MariaDB using .apply()...")
    
    # Use .apply() to process each row
    id_data = df.apply(process_article_row, axis=1)
    
    # Convert the result to DataFrame and concatenate
    id_df = pd.DataFrame(id_data.tolist(), index=df.index)
    result_df = pd.concat([df, id_df], axis=1)
    
    successful = result_df['mariadb_article_id'].notna().sum()
    print(f" Successfully loaded {successful} articles to MariaDB")
    
    return result_df