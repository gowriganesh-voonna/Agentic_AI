import secrets

# Generate a secure random secret key (once, then use it)
SECRET_KEY = secrets.token_hex(32) # You can hardcode this securely for production

MONGO_URI = "mongodb+srv://gowriganeshvoonna:3EhpwdUK0FnSh3YP@resume-data.wz0y1el.mongodb.net/"