import requests
import xml.etree.ElementTree as ET
import pandas as pd

def fetch_arxiv_data(search_query: str, max_results: int = 10) -> pd.DataFrame:
    """
    Fetch real data from ArXiv API and convert to DataFrame
    """
    base_url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": search_query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending"
    }
    
    try:
        print(f"🔍 Fetching {max_results} results from ArXiv for: '{search_query}'")
        response = requests.get(base_url, params=params, timeout=30)
        response.raise_for_status()
        
        return parse_arxiv_xml(response.text)
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching from ArXiv API: {e}")
        return create_fallback_data()
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return create_fallback_data()

def parse_arxiv_xml(xml_data: str) -> pd.DataFrame:
    """
    Parse ArXiv XML response into pandas DataFrame
    """
    try:
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        root = ET.fromstring(xml_data)
        articles_data = []
        
        for entry in root.findall('atom:entry', ns):
            # Extract title
            title_elem = entry.find('atom:title', ns)
            title = title_elem.text.strip() if title_elem is not None and title_elem.text else "No Title"
            
            # Extract authors
            authors = []
            for author in entry.findall('atom:author', ns):
                name_elem = author.find('atom:name', ns)
                if name_elem is not None and name_elem.text:
                    authors.append(name_elem.text.strip())
            
            # Extract summary (abstract)
            summary_elem = entry.find('atom:summary', ns)
            summary = summary_elem.text.strip() if summary_elem is not None and summary_elem.text else ""
            
            # Extract arXiv ID and URL
            id_elem = entry.find('atom:id', ns)
            arxiv_url = id_elem.text if id_elem is not None else ""
            arxiv_id = arxiv_url.split('/')[-1] if arxiv_url else ""
            
            # Extract published date
            published_elem = entry.find('atom:published', ns)
            published = published_elem.text if published_elem is not None else ""
            year = int(published[:4]) if published else 2024
            
            # Find PDF link
            pdf_url = ""
            for link in entry.findall('atom:link', ns):
                if link.get('title') == 'pdf' or link.get('type') == 'application/pdf':
                    pdf_url = link.get('href', '')
                    break
            
            articles_data.append({
                'title': title,
                'authors': '; '.join(authors),
                'year': year,
                'abstract': summary,
                'arxiv_id': arxiv_id,
                'url': pdf_url,
                'content': ''  # Will be filled later with HTML content
            })
        
        # Create DataFrame with consistent string dtypes
        df = pd.DataFrame(articles_data)
        if not df.empty:
            string_columns = ['title', 'authors', 'abstract', 'arxiv_id', 'url', 'content']
            df[string_columns] = df[string_columns].astype('string')
        
        print(f"✅ Successfully parsed {len(df)} articles from ArXiv API")
        return df
        
    except ET.ParseError as e:
        print(f"❌ Error parsing XML: {e}")
        return create_fallback_data()
    except Exception as e:
        print(f"❌ Error in parse_arxiv_xml: {e}")
        return create_fallback_data()

def create_fallback_data() -> pd.DataFrame:
    """
    Create fallback data if ArXiv API fails
    """
    print("⚠️ Using fallback data")
    fallback_data = {
        'title': [
            "Attention Is All You Need",
            "BERT: Pre-training of Deep Bidirectional Transformers", 
            "Language Models are Few-Shot Learners"
        ],
        'authors': [
            "Ashish Vaswani; Noam Shazeer; Niki Parmar",
            "Jacob Devlin; Ming-Wei Chang; Kenton Lee",
            "Tom B. Brown; Benjamin Mann; Nick Ryder"
        ],
        'year': [2017, 2018, 2020],
        'abstract': [
            "We propose a new simple network architecture, the Transformer, based solely on attention mechanisms.",
            "We introduce a new language representation model called BERT.",
            "We demonstrate that scaling up language models greatly improves task-agnostic performance."
        ],
        'arxiv_id': ['1706.03762', '1810.04805', '2005.14165'],
        'url': [
            'https://arxiv.org/pdf/1706.03762.pdf',
            'https://arxiv.org/pdf/1810.04805.pdf', 
            'https://arxiv.org/pdf/2005.14165.pdf'
        ],
        'content': [''] * 3
    }
    
    df = pd.DataFrame(fallback_data)
    string_columns = ['title', 'authors', 'abstract', 'arxiv_id', 'url', 'content']
    df[string_columns] = df[string_columns].astype('string')
    return df