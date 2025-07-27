from fastapi import APIRouter, Header
from app.models.user_models import (
    RegisterRequest, RegisterResponse,
    LoginRequest, LoginResponse,
    UpdateDetailsRequest, UpdateDetailsResponse,
    ChangePassword, VerifyOtpRequest ,ForgotPasswordRequest

)
from app.services.user_service import (
    register_user, login_user,
    update_user_details, change_password,verify_otp_and_reset_password ,forgot_password
)
from app.utiles.decoratores import handle_exceptions
 
router = APIRouter()
 
@handle_exceptions
@router.post("/register", response_model=RegisterResponse)
async def register_user_route(user: RegisterRequest):
    return await register_user(user)
 
@handle_exceptions
@router.post("/login", response_model=LoginResponse)
async def login_route(data: LoginRequest):
    return await login_user(data)
 
@handle_exceptions
@router.put("/update-details", response_model=UpdateDetailsResponse)
async def update_user_route(
    update_data: UpdateDetailsRequest,
    authorization: str = Header(...)
):
    token = authorization.replace("Bearer ", "")
    return await update_user_details(token, update_data)
 
@handle_exceptions
@router.put("/change-password")
async def change_password_route(change_request: ChangePassword):
    return await change_password(change_request)
 
@handle_exceptions
@router.post("/Forgot_Password")
async def Forgot_password(data:ForgotPasswordRequest):
    return await forgot_password(data)


@handle_exceptions
@router.post("/verfiy-otp-reset-password")
async def otp_verification_reset_password(data:VerifyOtpRequest):
    return await verify_otp_and_reset_password(data)