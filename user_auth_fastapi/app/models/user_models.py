from pydantic import BaseModel, EmailStr, Field, validator
from fastapi import HTTPException
from typing import Optional
import re

class RegisterRequest(BaseModel):
    first_name : str
    last_name : str
    username : str
    email : EmailStr
    phone_number : int
    password : str
    dob : str
    doj : str
    address : str

    @validator('email')
    def validate_gmail(cls, v):
        if not v.endswith("@gmail.com"):
            raise HTTPException(status_code = 400,
                                detail = "Invalid Email")
        return v
    
    @validator('password')
    def validate_password(cls,v):
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!#%*?&]{8,20}$', v):
            raise HTTPException(status_code =400,
                                detail = "Password must be 8-20 chars, include uppercase, lowercase, number, special char")
        return v
    
class RegisterResponse(BaseModel):
    message : str
    username : str
    email : str
