"""MongoEngine models for MongoDB."""
from mongoengine import Document, EmbeddedDocument, fields

class AuthorEmbedded(EmbeddedDocument):
    """Embedded Author document for MongoDB."""
    full_name = fields.StringField(required=True, max_length=255)
    title = fields.StringField(required=True, max_length=255)

class ScientificArticleDocument(Document):
    """Scientific Article document for MongoDB."""
    title = fields.StringField(required=True, max_length=500)
    summary = fields.StringField(required=True)
    file_path = fields.StringField(required=True, max_length=500)
    arxiv_id = fields.StringField(required=True, unique=True, max_length=100)
    author = fields.EmbeddedDocumentField(AuthorEmbedded, required=True)
    text = fields.StringField(required=True)  # Markdown content from PDF
    mariadb_article_id = fields.IntField()  # New field for MariaDB article ID
    mariadb_author_id = fields.IntField()   # New field for MariaDB author ID
    
    meta = {
        'collection': 'scientific_articles',
        'indexes': [
            {
                'fields': ['$title', '$summary', '$text'],
                'default_language': 'english',
                'weights': {'title': 10, 'summary': 5, 'text': 1}
            }
        ]
    }