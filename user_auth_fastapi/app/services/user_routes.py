from fastapi import APIRouter, Header
from app.models.user_models import (
    RegisterRequest, RegisterResponse,
    LoginRequest, LoginResponse,
    UpdateDetailsRequest, UpdateDetailsResponse,
    ChangePassword, VerifyOtpRequest ,ForgotPasswordRequest ,VerifyOtpChangePassword

)
from app.services.user_service import (
    register_user, login_user,
    update_user_details, change_password,verify_otp_and_reset_password ,forgot_password,
    verify_otp_password
)
from app.utiles.decoratores import handle_exceptions
from app.utiles.logger import get_logger
 
router = APIRouter()

logger = get_logger(__name__)
 
@handle_exceptions
@router.post("/register", response_model=RegisterResponse)
async def register_user_route(user: RegisterRequest):
    """
    Endpoint to handle user registration.
    """
    logger.info("Received registration request.")
    return await register_user(user)
 
@handle_exceptions
@router.post("/login", response_model=LoginResponse)
async def login_route(data: LoginRequest):
    """
    Endpoint for user login.
    """
    logger.info("Login attempt for user: %s", data.username_or_email)
    return await login_user(data)
 
@handle_exceptions
@router.put("/update-details", response_model=UpdateDetailsResponse)
async def update_user_route(
    update_data: UpdateDetailsRequest,
    authorization: str = Header(...)
):
    """
    Endpoint to update user details.
    Requires Bearer Token authentication.
    """
    logger.info("Updating user details.")
    token = authorization.replace("Bearer ", "")
    return await update_user_details(token, update_data)
 
@handle_exceptions
@router.put("/change-password")
async def change_password_route(change_request: ChangePassword):
    """
    Endpoint to change user password.
    """
    logger.info("Password change request received.")
    return await change_password(change_request)

@handle_exceptions
@router.post("/change-password/verify-otp")
async def Verfiy_otp_change_password(data : VerifyOtpChangePassword):
    return await verify_otp_password(data)
 
@handle_exceptions
@router.post("/Forgot_Password")
async def Forgot_password(data:ForgotPasswordRequest):
    """
    Step 1: Endpoint to initiate forgot password process.
    Sends OTP to the registered email.
    """
    logger.info("Forgot password request for email/username: %s", data.username_or_email)
    return await forgot_password(data)


@handle_exceptions
@router.post("/verfiy-otp-reset-password")
async def otp_verification_reset_password(data:VerifyOtpRequest):
    """
    Step 2: Endpoint to verify OTP and reset password.
    Accepts new password and OTP.
    """
    logger.info("OTP verification and password reset request.")
    return await verify_otp_and_reset_password(data)