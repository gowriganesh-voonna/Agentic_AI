from app.db.mongo import user_collection
from app.core.security import hash_password, verify_password, generate_jwt, verify_jwt
from app.models.user_models import RegisterRequest, LoginRequest, UpdateDetailsRequest, ChangePassword ,ForgotPasswordRequest,VerifyOtpRequest,ChangePasswordotp
from app.utiles.logger import get_logger
from datetime import datetime, timedelta
from fastapi import HTTPException
from app.utiles.email import send_otp_email,send_token
import bcrypt
import os
from app.core.session import create_session

 
logger = get_logger(__name__)

app_password = os.getenv("App_password")
 
otp_store = {}

# Register User 
async def register_user(user_data: RegisterRequest):
     # Check if user already exists based on email, phone, or username
    existing_user = await user_collection.find_one({
        "$or": [
            {"email": user_data.email},
            {"phone_number": user_data.phone_number},
            {"username": user_data.username}
        ]
    })
 
    if existing_user:
        logger.warning("Attempted registration with existing user details.")
        raise HTTPException(status_code=400, detail="User with given email, phone number, or username already exists")
    
     #  Prepare user document for insertion
    full_username = f"{user_data.first_name}{user_data.last_name}"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
 
    hashed_pwd = hash_password(user_data.password)
    user_doc = {
        "username": user_data.username,
        "first_name": user_data.first_name,
        "last_name": user_data.last_name,
        "full_name": full_username,
        "email": user_data.email,
        "phone_number": user_data.phone_number,
        "password": hashed_pwd,
        "dob": user_data.dob,
        "doj": user_data.doj,
        "address": user_data.address,
        "status": "Active",
        "password_history": [hashed_pwd],
        "password_created_at": timestamp,
        "failed_attempts": 0
    }
 
    await user_collection.insert_one(user_doc)
    logger.info(f"User {full_username} registered with email: {user_data.email}")
    return {
        "message": "User registered successfully",
        "username": user_data.username,
        "email": user_data.email
    }
 

#  Login User 
async def login_user(data: LoginRequest):
    #  Find user by email or username
    user = await user_collection.find_one({
        "$or": [
            {"email": data.username_or_email},
            {"username": data.username_or_email}
        ]
    })
 
    if not user:
        logger.warning(f"Login attempt failed: User not found for {data.username_or_email}")
        raise HTTPException(status_code=404, detail="User Not found")
    
     #  Check if user is inactive
    if user["status"] != "Active":
        logger.warning(f"User '{user['username']}' is inactive.")
        raise HTTPException(status_code=403, detail="User is inactive due to failed attempts or admin block")
 
    pwd_created = datetime.strptime(user["password_created_at"], "%Y-%m-%d %H:%M:%S")
    #  Check if password has expired (valid for 30 days)
    if (datetime.now() - pwd_created).days > 30:
        logger.warning(f"User '{user['username']}' password expired.")
        raise HTTPException(status_code=403, detail="Password expired. Please change your password and try again.")
    
    #  Verify Password
    if not verify_password(data.password, user["password"]):
        await user_collection.update_one({"_id": user["_id"]}, {"$inc": {"failed_attempts": 1}})
         # Block user after 3 failed attempts
        if user["failed_attempts"] + 1 >= 3:
            await user_collection.update_one({"_id": user["_id"]}, {
                "$set": {
                    "status": "Inactive",
                    "inactive_until": datetime.now() + timedelta(hours=24)
                }
            })
            logger.warning(f"User {user['username']} blocked due to multiple failed login attempts")
        raise HTTPException(status_code=401, detail="Invalid Password")
    #  Successful login → Reset failed attempts
    await user_collection.update_one({"_id": user["_id"]}, {"$set": {"failed_attempts": 0}})
 
    token = generate_jwt(user["username"], user["email"])
    create_session(user["email"],token)
    send_token(
        receiver_email=user["email"],
        sender_email="voonnagowriganesh@gmail.com",
        app_password=app_password,
        token=token,
        username=user["username"]
    )

    logger.info(f"{user['username']} logged in successfully")
    return {
        "message": "Login Successful",
        "username": user["username"],
        "token": "Sent to your Registered Mail ID.Please Check your Inbox"
    }
 

# Function to update user details after verifying JWT and password
async def update_user_details(token: str, data: UpdateDetailsRequest):
    payload = verify_jwt(token)
    logged_in_email = payload.get("email")
    if not logged_in_email:
        logger.warning("Invalid token: No email found in JWT")
        raise HTTPException(status_code=401, detail="Invalid token: no email found")
 
    user = await user_collection.find_one({"email": logged_in_email})
    if not user:
        logger.warning(f"User not found with email: {logged_in_email}")
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if provided password matches the existing one
    if not verify_password(data.password, user["password"]):
        logger.warning(f"Incorrect password for user: {logged_in_email}")
        raise HTTPException(status_code=403, detail="Incorrect password")
    
    # Prevent changing another user's details
    if data.username and data.username != user["username"]:
        logger.warning(f"Attempt to update different username by user: {logged_in_email}")
        raise HTTPException(status_code=403, detail="You can only update your own account")
 
    updates = {}
    for field in ["username", "first_name", "last_name", "email", "phone_number", "dob", "address"]:
        new_val = getattr(data, field)
        if new_val is not None and new_val != user.get(field):
            updates[field] = new_val
 
    if not updates:
        logger.info(f"No new details provided by user: {logged_in_email}")
        raise HTTPException(status_code=400, detail="No new details provided or same as existing.")
 
    await user_collection.update_one({"_id": user["_id"]}, {"$set": updates})
    logger.info(f"User {logged_in_email} updated details: {list(updates.keys())}")
    return {
        "message": "Details updated successfully",
        "username": updates.get("username", user["username"])
    }
 

# Function to change password after validating current password and ensuring it's not reused
async def change_password(change_request: ChangePassword):
    user = await user_collection.find_one({"email": change_request.email})
    logger.info(f"Password change requested for email: {change_request.email}")
 
    if not user:
        logger.warning(f"User not found for email: {change_request.email}")
        raise HTTPException(status_code=404, detail=f"{change_request.email} Not Found")
 
    if not verify_password(change_request.old_password, user["password"]):
        logger.warning(f"Incorrect old password for user: {change_request.email}")
        raise HTTPException(status_code=401, detail="Current password is incorrect")
 
    
    for old_hased in user['password_history']:
        if verify_password(change_request.new_password,old_hased):
            logger.warning(f"New password matches one of the old passwords for user: {change_request.email}")
            raise HTTPException(
                status_code = 400,
                detail = "New Password must not match any of the previous passwords."
            )
        
    # Generate and Send OTP
    otp = send_otp_email(
        receiver_email=user["email"],
        sender_email="voonnagowriganesh@gmail.com",
        app_password=app_password
    )

    # store OTP +new_password temporarily
    otp_store[user["username"]] = {
        "otp":otp,
        "new_password" : change_request.new_password,
        "expires" : datetime.utcnow()+timedelta(minutes=5)
    }
    
 
    return {"message": "OTP Sent to your registered email"}


async def verify_otp_password(data : ChangePasswordotp):
    record = otp_store.get(data.username)

    if not record:
        logger.warning(f"User not found for username: {data.username}")
        raise HTTPException(status_code=404, detail=f"{data.username} Not Found")
    
    if datetime.utcnow()> record["expires"] :
        logger.info("OTP Expried for change_password")
        del otp_store[data.username]
        raise HTTPException(status_code = 410, detail = "OTP Expired")
    
    if data.otp != record["otp"] :
        logger.info("Invalid OTP ")
        raise HTTPException(status_code = 401,
                            detail = "Invalid OTP")
    
    new_hashed_password = hash_password(record["new_password"])

    result = await user_collection.update_one(
        {"username": data.username},
        {
            "$set": {
                "password": new_hashed_password,
                "password_created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            "$push": {
                "password_history": new_hashed_password
            }
        }
    )

    if result.modified_count == 1:
        logger.info(f"Password successfully updated for user: {data.username}")
    else:
        logger.error(f"Failed to update password for user: {data.username}")
        raise HTTPException(status_code=500, detail="Failed to update password")
    
    del otp_store[data.username]

    logger.info(f"Password Changed Successfully for {data.username}")

    return {"mesage":"Password Changed successfully after otp verification"}




# Function to handle forgot password - sends OTP to registered email
async def forgot_password(data:ForgotPasswordRequest):
    user = await user_collection.find_one({
        "$or": [{"username":data.username_or_email},{"email":data.username_or_email}]
    })

    if not user:
        logger.warning(f"User not found for email or username: {data.username_or_email}")
        raise HTTPException(status_code = 404,
                            detail= f"User Not Found")
    otp = send_otp_email(
        receiver_email=user["email"],
        sender_email="voonnagowriganesh@gmail.com",
        app_password=app_password
    )

    otp_store[data.username_or_email]= {"otp":otp,"expires":datetime.utcnow() + timedelta(minutes=5)}
    logger.info(f"OTP sent to registered email for user: {data.username_or_email}")

    return {"message":"OTP sent to your registred email."}

# Function to verify OTP and reset password
async def verify_otp_and_reset_password(data:VerifyOtpRequest):
    record = otp_store.get(data.username_or_email)
    user = await user_collection.find_one({
        "$or": [{"username":data.username_or_email},{"email":data.username_or_email}]
    })

    if not record:
        logger.warning(f"No OTP found for user: {data.username_or_email}")
        raise HTTPException(status_code = 404,
                            detail="No  OTP Found.")
    if datetime.utcnow()>record["expires"]:
        logger.warning(f"OTP expired for user: {data.username_or_email}")
        raise HTTPException(status_code =410,
                            detail = "OTP Expired.")
    
    if data.otp!= record["otp"]:
        logger.warning(f"Invalid OTP entered for user: {data.username_or_email}")
        raise HTTPException(status_code = 404,
                            detail ="Invalid OTP")
    
    hased_password = hash_password(data.new_password)

    for old_hased in user['password_history']:
        if verify_password(data.new_password,old_hased):
            logger.warning(f"New password matches one of the old passwords for user: {change_request.email}")
            raise HTTPException(
                status_code = 400,
                detail = "New Password must not match any of the previous passwords."
            )

    await user_collection.update_one(
        {"$or" : [{"username":data.username_or_email},{"email":data.username_or_email}]},
        {
            "$set":{"password":hased_password},
            "$push":{"password_history":hased_password}
        }
    )

    del otp_store[data.username_or_email]
    logger.info(f"OTP verified and password reset for user: {data.username_or_email}")
    return {"message" :" OTP Verified Successfully and password reset successful"}

