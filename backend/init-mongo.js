// MongoDB initialization script
db = db.getSiblingDB('camel_rating');

// Create collections
db.createCollection('users');
db.createCollection('images');
db.createCollection('feedback');

// Create indexes
db.users.createIndex({ "email": 1 }, { unique: true });
db.users.createIndex({ "username": 1 }, { unique: true });
db.images.createIndex({ "user_id": 1 });
db.images.createIndex({ "created_at": 1 });
db.feedback.createIndex({ "image_id": 1 });
db.feedback.createIndex({ "user_id": 1 });

// Create a demo user
db.users.insertOne({
  email: "demo@camelrating.com",
  username: "demo",
  full_name: "Demo User",
  hashed_password: "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8Kz8KzK", // demo123
  is_active: true,
  created_at: new Date(),
  updated_at: new Date()
});

print("Database initialized successfully!");
