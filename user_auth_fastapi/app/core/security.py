from passlib.context import CryptContext
import jwt
from datetime import datetime,timedelta, timezone
from app.core.config import SECRET_KEY

pwd_context = CryptContext(schemes=["bcrypt"] , deprecated = "auto")

def hash_password(password:str)->str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain,hashed)

def generate_jwt(username: str,email:str):

    payload = {
        'user':username,
        'email':email,
        'exp': datetime.now(timezone.utc) + timedelta(hours=1)
    }

    token = jwt.encode(payload,SECRET_KEY,algorithm = 'HS256')

    return token