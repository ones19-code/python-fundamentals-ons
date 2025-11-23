from mongoengine import connect

def init_db():
    connect(
        db="appdb",
        username="appuser",
        password="apppass123",
        host="localhost",
        port=27017,
        authentication_source="admin"
    )
