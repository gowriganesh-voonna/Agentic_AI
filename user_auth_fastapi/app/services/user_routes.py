from fastapi import APIRouter
from app.models.user_models import RegisterRequest, RegisterResponse
from app.services.user_service import register_user
 
router = APIRouter()
 
@router.post("/register", response_model=RegisterResponse)
def register_user_route(user: RegisterRequest):
    return register_user(user)