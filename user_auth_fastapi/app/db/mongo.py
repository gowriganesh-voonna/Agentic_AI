from pymongo import MongoClient

MONGO_URI = "mongodb+srv://gowriganeshvoonna:3EhpwdUK0FnSh3YP@resume-data.wz0y1el.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client["user_auth_db"]
user_collection = db["users"]