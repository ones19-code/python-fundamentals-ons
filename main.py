from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, func
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# ------------------------
# 1. SQLAlchemy Configuration
# ------------------------
DATABASE_URL = "mysql+pymysql://testuser:testpass@localhost:3306/testdb"

engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    echo=False  # Set True to see SQL queries
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ------------------------
# 2. ORM Base
# ------------------------
Base = declarative_base()

# ------------------------
# 3. ORM Model
# ------------------------
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

# ------------------------
# 4. CRUD Functions
# ------------------------
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

# ------------------------
# 5. Example Usage
# ------------------------
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
