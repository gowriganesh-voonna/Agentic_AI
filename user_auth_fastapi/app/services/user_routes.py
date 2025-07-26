from fastapi import APIRouter
from app.models.user_models import RegisterRequest, RegisterResponse,LoginRequest,LoginResponse
from app.services.user_service import register_user,login_user
 
router = APIRouter()
 
@router.post("/register", response_model=RegisterResponse)
def register_user_route(user: RegisterRequest):
    return register_user(user)

@router.post("/login",response_model = LoginResponse)
def login_route(data : LoginRequest):
    return login_user(data)