import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import load_users
import jwt, datetime 


SECRET_KEY = "voonna123"
TOKEN_EXPIRY_MINUTES = 30

def generate_token(user_name,password):
    users=load_users()
    for user in users:
        if user["user_name"] == user_name and user["password"] == password :
            payload ={
                "user_name":user_name,
                "exp": datetime.datetime.utcnow()+datetime.timedelta(minutes=TOKEN_EXPIRY_MINUTES)
            }
            token=jwt.encode(payload,SECRET_KEY, algorithm= "HS256")
            return token
    return None
    

def decode_token(token):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=["HS256"])    # we need to pass list of algoirthms
        return payload
    except jwt.ExpiredSignatureError:
        return "Token Expired"
    except jwt.InvalidKeyError:
        return "Invalid Error"


