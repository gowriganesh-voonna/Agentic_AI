from fastapi import FastAPI,HTTPException
from app.services.account_service import create_customer_account,fund_customer_account,with_customer_fund
from app.models.schema import (
    CreateAccountRequest,
    FundAccountRequest,
    WithdrawRequest
)

from app.errors.exceptions import (
    Account_Already_Exists_Exception,
    Account_Not_Found_Exception,
    Insuficient_Fund_Exception,
    account_already_exists,
    account_does_not_exists,
    insufficient_fund
)

from app.data.storage import load_accounts
from app.utils.loggers import get_logger
from app.api.accounts_route import account_router

app = FastAPI()

logger = get_logger(__name__)

app.include_router(account_router,prefix="/api/v1")

@app.get("/")
async def root():
    """Root Entry point -- point to navigation"""
    return {"Message":"Bank API is Running see/Documention"}



