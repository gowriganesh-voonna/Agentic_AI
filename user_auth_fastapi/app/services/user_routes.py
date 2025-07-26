from fastapi import APIRouter,Header,Depends
from app.models.user_models import (RegisterRequest,
                                     RegisterResponse,
                                     LoginRequest,
                                     LoginResponse,
                                     UpdateDetailsRequest,
                                     UpdateDetailsResponse)
from app.services.user_service import register_user,login_user,update_user_details
 
router = APIRouter()


@router.post("/register", response_model=RegisterResponse)
def register_user_route(user: RegisterRequest):
    return register_user(user)

@router.post("/login",response_model = LoginResponse)
def login_route(data : LoginRequest):
    return login_user(data)

@router.put("/update-details", response_model=UpdateDetailsResponse)
def update_user_route(
    update_data: UpdateDetailsRequest,
    authorization: str = Header(...)
):
    token = authorization.replace("Bearer ", "")
    return update_user_details(token, update_data)