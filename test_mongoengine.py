from mongoengine_user import create_user, get_user_by_id, update_user

users = [
    {
        "username": "eva",
        "email": "eva@example.com",
        "profile": {"full_name": "Eva Al-Hassan", "age": 30, "location": "Cairo"},
        "roles": ["user"]
    },
    {
        "username": "adam",
        "email": "adam@example.com",
        "profile": {"full_name": "Adam Al-Farouq", "age": 35, "location": "Riyadh"},
        "roles": ["user", "admin"]
    },
    {
        "username": "leila",
        "email": "leila@example.com",
        "profile": {"full_name": "Leila Al-Mansour", "age": 28, "location": "Beirut"},
        "roles": ["user"]
    }
]

user_ids = []
for user in users:
    uid = create_user(user)
    print(f"User created: {user['username']} with id {uid}")
    user_ids.append(uid)

for uid in user_ids:
    u = get_user_by_id(uid)
    print("Retrieved:", u)

update_count = update_user(user_ids[2], {"profile.age": 29})
print(f"Updated {update_count} document(s)")

u = get_user_by_id(user_ids[2])
print("Updated:", u)
