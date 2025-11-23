from pymongo import MongoClient
from typing import Dict, Any
import pandas as pd

def load_data_to_mongodb(df: pd.DataFrame, connection_uri: str, db_name: str):
    """
    Load DataFrame to MongoDB using .apply() and MariaDB IDs
    """
    def process_mongo_row(row: pd.Series) -> bool:
        """
        Process single row for MongoDB insertion using .apply()
        """
        try:
            client = MongoClient(connection_uri)
            db = client[db_name]
            
            document = {
                'mariadb_article_id': int(row.get('mariadb_article_id', 0)),
                'mariadb_author_id': int(row.get('mariadb_author_id', 0)),
                'title': str(row['title']),
                'authors': [author.strip() for author in str(row['authors']).split(';') if author.strip()],
                'year': int(row['year']),
                'abstract': str(row['abstract']),
                'arxiv_id': str(row['arxiv_id']),
                'url': str(row['url']),
                'content': str(row.get('content', '')),
                'search_text': f"{row['title']} {row['abstract']} {row.get('content', '')}"
            }
            
            result = db.articles.insert_one(document)
            client.close()
            return True
            
        except Exception as e:
            print(f" Error inserting document to MongoDB: {e}")
            return False
    
    print(" Loading data to MongoDB using .apply()...")
    
    results = df.apply(process_mongo_row, axis=1)
    successful = results.sum()
    
    print(f" Successfully loaded {successful}/{len(df)} documents to MongoDB")

    try:
        client = MongoClient(connection_uri)
        db = client[db_name]
        db.articles.create_index([("search_text", "text")])
        client.close()
        print(" Text search index created")
    except Exception as e:
        print(f" Could not create text index: {e}")

def search_in_mongodb(query: str, connection_uri: str, db_name: str, limit: int = 5):
    """
    Search articles in MongoDB
    """
    try:
        client = MongoClient(connection_uri)
        db = client[db_name]
        
        # Search using text index
        results = db.articles.find(
            {"$text": {"$search": query}},
            {"score": {"$meta": "textScore"}}
        ).sort([("score", {"$meta": "textScore"})]).limit(limit)
        
        articles = list(results)
        client.close()
        
        return articles
        
    except Exception as e:
        print(f" Error searching MongoDB: {e}")
        return []

def get_mongodb_stats(connection_uri: str, db_name: str):
    """
    Get MongoDB statistics
    """
    try:
        client = MongoClient(connection_uri)
        db = client[db_name]
        
        stats = {
            'total_documents': db.articles.count_documents({}),
            'collections': list(db.list_collection_names())
        }
        
        client.close()
        return stats
        
    except Exception as e:
        print(f"Error getting MongoDB stats: {e}")
        return {}