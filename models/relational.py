"""SQLAlchemy models for MariaDB."""
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from typing import List, Optional

Base = declarative_base()

class Author(Base):
    """Author model for MariaDB."""
    __tablename__ = 'authors'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    
    # Correction: utiliser relationship sans annotation de type problématique
    articles = relationship("ScientificArticle", back_populates="author")

class ScientificArticle(Base):
    """Scientific Article model for MariaDB."""
    __tablename__ = 'scientific_articles'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(500), nullable=False)
    summary = Column(Text, nullable=False)
    file_path = Column(String(500), nullable=False)
    arxiv_id = Column(String(100), nullable=False, unique=True)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
    
    # Correction: utiliser relationship sans annotation de type problématique
    author = relationship("Author", back_populates="articles")