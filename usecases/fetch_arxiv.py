"""Fetch data from ArXiv API and process with pandas."""
import requests
import pandas as pd
from typing import List, Dict, Any
import time
import random

def fetch_arxiv_data(query: str = "transformer", max_results: int = 5) -> pd.DataFrame:
    """
    Mock ArXiv data for testing (avoid rate limiting).
    """
    print("Using mock ArXiv data to avoid rate limiting...")
    
    articles_data = [
        {
            'title': 'Attention Is All You Need',
            'summary': 'The dominant sequence transduction models are based on complex recurrent or convolutional neural networks. We propose a novel network architecture, the Transformer, based solely on attention mechanisms.',
            'file_path': 'papers/1706.03762.pdf',
            'arxiv_id': '1706.03762',
            'author_full_name': 'Yasmin Al-Qasimi',
            'author_title': 'Research Professor'
        },
        {
            'title': 'BERT: Pre-training of Deep Bidirectional Transformers',
            'summary': 'We introduce BERT, a new language representation model that stands for Bidirectional Encoder Representations from Transformers.',
            'file_path': 'papers/1810.04805.pdf',
            'arxiv_id': '1810.04805',
            'author_full_name': 'Khalid Al-Shammari',
            'author_title': 'Lead Researcher'
        },
        {
            'title': 'Language Models are Few-Shot Learners',
            'summary': 'We demonstrate that scaling up language models greatly improves task-agnostic, few-shot performance.',
            'file_path': 'papers/2005.14165.pdf',
            'arxiv_id': '2005.14165',
            'author_full_name': 'Noura Al-Harbi',
            'author_title': 'Software Engineer'
        }
    ]
    
    # Create DataFrame with string dtype for consistency
    df = pd.DataFrame(articles_data[:max_results])
    df = df.astype('string')
    
    print(f"Created mock DataFrame with {len(df)} articles")
    return df

def download_article_html(row: pd.Series) -> str:
    """
    Mock HTML content download to avoid rate limiting.
    """
    arxiv_id = row['arxiv_id']
    title = row['title']
    
    # Return mock HTML content
    mock_html = f"""
    <html>
    <head><title>{title}</title></head>
    <body>
        <h1>{title}</h1>
        <div class="abstract">
            <h2>Abstract</h2>
            <p>{row['summary']}</p>
        </div>
        <div class="authors">
            <h2>Authors</h2>
            <p>{row['author_full_name']} - {row['author_title']}</p>
        </div>
        <div class="arxiv">
            <p>arXiv:{arxiv_id}</p>
        </div>
    </body>
    </html>
    """
    
    return mock_html