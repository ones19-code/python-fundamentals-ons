import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def download_html_content(url: str) -> str:
    """
    Download and extract text content from URL using .apply()
    """
    if not url or pd.isna(url) or url == "":
        return ""
    
    try:
        print(f"Downloading content from: {url[:80]}...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        # For PDF URLs, return a placeholder message
        if url.endswith('.pdf') or 'application/pdf' in response.headers.get('content-type', ''):
            return f"PDF content available at: {url}"
        
        # For HTML content, extract text
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get clean text
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        clean_text = ' '.join(chunk for chunk in chunks if chunk)
        
        return clean_text[:5000]  # Limit content length
        
    except requests.exceptions.RequestException as e:
        print(f"Could not download {url}: {e}")
        return ""
    except Exception as e:
        print(f" Error processing {url}: {e}")
        return ""

def add_content_to_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add HTML content as new column using .apply()
    """
    if df.empty:
        return df
    
    print(" Downloading content for all articles...")
    
    # Use .apply() to download content for each row
    df = df.copy()
    df['content'] = df['url'].apply(download_html_content)
    
    # If content is empty, use abstract as fallback
    empty_content = df['content'].isna() | (df['content'] == "")
    df.loc[empty_content, 'content'] = df.loc[empty_content, 'abstract']
    
    print(" Content download completed")
    return df