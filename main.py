import pandas as pd
import time
from usecases.arxiv_api import fetch_arxiv_data
from usecases.content_fetcher import add_content_to_dataframe
from storage.mariadb import load_data_to_mariadb, create_mariadb_tables
from storage.mongodb import load_data_to_mongodb, search_in_mongodb

def main():
    print(" Starting Scientific Articles Pipeline with Real ArXiv API...")
    
    # Database configuration
    mariadb_config = {
        'host': 'mariadb',
        'user': 'app_user',
        'password': 'app_password',
        'database': 'scientific_articles'
    }
    
    
    mongodb_config = {
        'uri': 'mongodb://app_user:app_password@mongodb:27017/scientific_articles?authSource=scientific_articles',
        'db_name': 'scientific_articles'
    }

    print("Waiting for databases to start...")
    time.sleep(15)  # Increased wait time for MongoDB auth setup
    
    try:
  
        print("1. Creating MariaDB tables...")
        create_mariadb_tables(mariadb_config)
        
       
        print("2. Fetching data from ArXiv API...")
        df = fetch_arxiv_data("transformer neural network", max_results=5)
        
        if df.empty:
            print(" No data retrieved. Exiting pipeline.")
            return
    
        string_columns = ['title', 'authors', 'abstract', 'arxiv_id', 'url', 'content']
        for col in string_columns:
            if col in df.columns:
                df[col] = df[col].astype('string')
        
        print(f" Fetched {len(df)} real articles from ArXiv API")
        
 
        print(" Sample articles:")
        for i, title in enumerate(df['title'].head(3)):
            print(f"   {i+1}. {title[:80]}...")
        
        print("3. Downloading HTML content...")
        df = add_content_to_dataframe(df)
        
    
        print("4. Loading data to MariaDB...")
        df_with_ids = load_data_to_mariadb(df, mariadb_config)
        
       
        print("5. Transferring data to MongoDB...")
        load_data_to_mongodb(df_with_ids, mongodb_config['uri'], mongodb_config['db_name'])

        print("6. Performing search in MongoDB...")
        search_results = search_in_mongodb("transformer", mongodb_config['uri'], mongodb_config['db_name'])
        
        print(f"\n Search results for 'transformer':")
        print("=" * 50)
        
        if search_results:
            for i, article in enumerate(search_results, 1):
                print(f"{i}. {article['title']}")
                authors = article.get('authors', [])
                authors_display = ', '.join(authors[:2]) + ('...' if len(authors) > 2 else '')
                print(f"   Authors: {authors_display}")
                print(f"   arXiv: {article.get('arxiv_id', 'N/A')}")
                print()
        else:
            print("No results found")
        
        # Display DataFrame info
        print(" DataFrame information:")
        print(f"Shape: {df_with_ids.shape}")
        print(f"Columns: {list(df_with_ids.columns)}")
        print(f"Articles with MariaDB IDs: {df_with_ids['mariadb_article_id'].notna().sum()}")
        
        print("\n Pipeline completed successfully!")
        
    except Exception as e:
        print(f" Pipeline failed: {e}")

if __name__ == "__main__":
    main()