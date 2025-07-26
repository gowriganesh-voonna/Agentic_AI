from app.db.mongo import user_collection
from app.core.security import hash_password,verify_password,generate_jwt,verify_jwt
from app.models.user_models import RegisterRequest,LoginRequest,UpdateDetailsRequest
from app.utiles.logger import get_logger
from datetime import datetime ,timedelta
from fastapi import HTTPException


logger = get_logger(__name__)
 
def register_user(user_data: RegisterRequest):
    # Check if user already exists
    existing_user = user_collection.find_one({
        "$or": [
            {"email": user_data.email},
            {"phone_number": user_data.phone_number},
            {"username": user_data.username}
        ]
    })
    if existing_user:
        raise HTTPException(status_code=400, detail="User with given email, phone number, or username already exists")
 
    # Prepare data
    full_username = f"{user_data.first_name}{user_data.last_name}"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_doc = {
        "username": user_data.username,
        "first_name": user_data.first_name,
        "last_name": user_data.last_name,
        "full_name": full_username,
        "email": user_data.email,
        "phone_number": user_data.phone_number,
        "password": hash_password(user_data.password),
        "dob": user_data.dob,
        "doj": user_data.doj,
        "address": user_data.address,
        "status": "Active",
        "password_created_at": timestamp,
        "failed_attempts": 0
    }
 
    user_collection.insert_one(user_doc)
 
    logger.info(f"User {full_username} registered with email: {user_data.email}")
 
    return {
        "message": "User registered successfully",
        "username": full_username,
        "email": user_data.email
    }


def login_user(data : LoginRequest):
    user = user_collection.find_one({
        "$or" : [{"email":data.username_or_email} , {"username": data.username_or_email}]
    })

    if not user:
        raise HTTPException(status_code = 404, detail = "User Not found")
    
    if user["status"] != "Active":
        raise HTTPException(status_code = 403,
                            detail = "User is inactive due to failed attempts or admin block")
    
    # Check Password expiration
    pwd_created = datetime.strptime(user["password_created_at"] , "%Y-%m-%d %H:%M:%S")
    if (datetime.now()-pwd_created).days >30 :
        raise HTTPException(status_code = 403,
                            detail="Password expired.Please change your password and try again.")
    
    #check password
    if not verify_password(data.password,user["password"]):
        user_collection.update_one({"_id":user["_id"]}, {"$inc":{"failed_attempts":1}})

        if user["failed_attempts"] + 1 >=3:
            user_collection.update_one({"_id":user["_id"]}, {
                "$set":{"status":"Inactive", "inactive_until": datetime.now()+timedelta(hours=24)}
            
            })
            logger.warning(f"User {user['username']} blocked due to multiple failed login attempts")
        raise HTTPException(status_code = 401,
                            detail = "Invalid_Password")
    # Reset failed_attempts
    user_collection.update_one({"_id":user["_id"]},{"$set":{"failed_attempts":0}})

    token = generate_jwt(user["username"],user["email"])

    logger.info(f"{user['username']} logged successfully")

    return {
        "message":"Login Successful",
        "username" : user["username"],
        "token":token
    }

def update_user_details(token: str, data: UpdateDetailsRequest):
    payload = verify_jwt(token)
   
    logged_in_username = payload.get("email")
 
    if not logged_in_username:
        raise HTTPException(status_code=401, detail="Invalid token: no username found")
 
    # Fetch user
    user = user_collection.find_one({"email": logged_in_username})
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
 
    # Verify password
    if not verify_password(data.password, user["password"]):
        raise HTTPException(status_code=403, detail="Incorrect password")
 
    # Check if user is trying to update someone else (security check)
    if data.username and data.username != logged_in_username:
        raise HTTPException(status_code=403, detail="You can only update your own account")
 
    # Prepare updates
    updates = {}
    for field in ["username", "first_name", "last_name", "email", "phone_number", "dob", "address"]:
        new_val = getattr(data, field)
        if new_val is not None and new_val != user.get(field):
            updates[field] = new_val
 
    if not updates:
        raise HTTPException(status_code=400, detail="No new details provided or same as existing.")
 
    user_collection.update_one({"_id": user["_id"]}, {"$set": updates})
 
    logger.info(f"User {logged_in_username} updated details: {list(updates.keys())}")
 
    return {
        "message": "Details updated successfully",
        "username": updates.get("username", logged_in_username)
    }