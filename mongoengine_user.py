from mongoengine import Document, EmbeddedDocument, fields
from mongoengine_utils import init_db

init_db()  # initialise la connexion

class Profile(EmbeddedDocument):
    full_name = fields.StringField(required=True)
    age = fields.IntField(required=True)
    location = fields.StringField(required=True)

class User(Document):
    username = fields.StringField(required=True, unique=True)
    email = fields.StringField(required=True, unique=True)
    profile = fields.EmbeddedDocumentField(Profile)
    roles = fields.ListField(fields.StringField())

def create_user(user_data):
    profile = Profile(**user_data["profile"])
    user = User(
        username=user_data["username"],
        email=user_data["email"],
        profile=profile,
        roles=user_data["roles"]
    )
    user.save()
    return str(user.id)

def get_user_by_id(uid):
    user = User.objects(id=uid).first()
    if user:
        return {
            "username": user.username,
            "email": user.email,
            "profile": {
                "full_name": user.profile.full_name,
                "age": user.profile.age,
                "location": user.profile.location
            },
            "roles": user.roles,
            "id": str(user.id)
        }
    return None

def update_user(uid, updates):
    user = User.objects(id=uid).first()
    if not user:
        return 0
    for k, v in updates.items():
        keys = k.split(".")
        if keys[0] == "profile":
            setattr(user.profile, keys[1], v)
        else:
            setattr(user, keys[0], v)
    user.save()
    return 1





