<<<<<<< HEAD
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
=======
from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, func
from sqlalchemy.orm import declarative_base, sessionmaker, Session


DATABASE_URL = "mysql+pymysql://testuser:testpass@localhost:3306/testdb"

engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    echo=False  # Set True to see SQL queries
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#rom
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    created_at = Column(TIMESTAMP, server_default=func.now())


def get_all_users(db: Session):
    return db.query(User).all()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, username: str, email: str):
    new_user = User(username=username, email=email)
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        db.rollback()
        print(f"Error creating user: {e}")
        return None

def update_user_email(db: Session, username: str, new_email: str):
    user = db.query(User).filter(User.username == username).first()
    if user:
        user.email = new_email
        db.commit()
        db.refresh(user)
        return user
    return None


if __name__ == "__main__":
    db = SessionLocal()

    print("All existing users:")
    for u in get_all_users(db):
        print(u.username, u.email)

    # Add some users if they do not exist
    users_list = [
        ("eva", "eva@example.com"),
        ("adam", "adam@example.com"),
        ("ons", "ons@example.com"),
        ("jamel", "jamel@example.com")
    ]

    for username, email in users_list:
        if not get_user_by_username(db, username):
            create_user(db, username, email)

    print("\nSearching for user 'ons':")
    user = get_user_by_username(db, "ons")
    if user:
        print(user.username, user.email)
    else:
        print("User 'ons' not found")

    print("\nCreating new user 'areej':")
    new_user = create_user(db, "areej", "areej@example.com")
    if new_user:
        print(new_user.username, new_user.email)

    print("\nUpdating email of 'areej':")
    updated_user = update_user_email(db, "areej", "newareej@example.com")
    if updated_user:
        print(updated_user.username, updated_user.email)
    else:
        print("User 'areej' not found")

    db.close()
>>>>>>> 831940ce815bed44f390c5aae8a6d62fe00914e7
