"""Search functionality for MongoDB."""
from typing import List, Dict, Any
from models.document import ScientificArticleDocument

def search_articles(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Search articles using MongoDB text index.
    
    Args:
        query: Search query string
        limit: Maximum number of results to return
        
    Returns:
        List of matching articles with score
    """
    try:
        # Utiliser la recherche de texte de MongoDB
        results = ScientificArticleDocument.objects.search_text(query).limit(limit)
        
        search_results: List[Dict[str, Any]] = []
        for article in results:
            search_results.append({
                'title': article.title,
                'arxiv_id': article.arxiv_id,
                'author': article.author.full_name,
                'summary': article.summary[:200] + '...' if len(article.summary) > 200 else article.summary,
                'score': getattr(article, 'score', 0)  # Text search score
            })
        
        return search_results
    except Exception as e:
        print(f"Search error: {e}")
        return []