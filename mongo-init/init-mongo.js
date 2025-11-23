const dbName = process.env.MONGO_INITDB_DATABASE || 'appdb';
const appUser = 'appuser';
const appPass = 'apppass123';

db = db.getSiblingDB(dbName);

db.createUser({
  user: appUser,
  pwd: appPass,
  roles: [{ role: 'readWrite', db: dbName }]
});

db.users.insertMany([
  {
    username: 'alice',
    email: 'alice@example.com',
    profile: { full_name: 'Alice Liddell', age: 28, location: 'Wonderland' },
    roles: ['user']
  },
  {
    username: 'bob',
    email: 'bob@example.com',
    profile: { full_name: 'Bob Builder', age: 35, location: 'Builderland' },
    roles: ['user', 'admin']
  }
]);

print('✅ MongoDB initialized with sample data');
