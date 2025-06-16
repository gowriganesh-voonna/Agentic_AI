from fastapi import FastAPI,HTTPException,APIRouter
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

account_router=APIRouter()

logger = get_logger(__name__)

@account_router.post("/create-account")
async def create_account(data : CreateAccountRequest):
    try:
        await create_customer_account(data.customer_id)
        logger.info(f"Account created for the {data.customer_id} Successfully")
        return {"message": f"Customer {data.customer_id} created with 0.0 Balance"}
    except Account_Already_Exists_Exception:
        
        raise account_already_exists()
    except Exception as e:
        logger.error(f"Something went wrong and details are {str(e)} - data -  {data.customer_id}")
        raise HTTPException(
            status_code = 500,
            detail = str(e)
        )

@account_router.post("/fund")
async def fund_account(data : FundAccountRequest):
    try:
        result = await fund_customer_account(data.customer_id,data.amount)
        logger.info(f"Fund added to the customer {data.customer_id} with amount : {data.amount}")
        return {"message" : f"Customer {data.customer_id}  added to the account balance : {result}"}
    except Account_Not_Found_Exception:
        logger.info (f"Account_Not_Found Exception for the customer : {data.customer_id}")
        raise account_does_not_exists()
    except Exception as e:
        logger.error(f"Something went wrong and details are {str(e)} - data -  {data.customer_id}")
        raise HTTPException(status_code = 400,detail= str(e))


@account_router.post ("/withdraw")
async def withdraw_from_account(data: WithdrawRequest):
    try:
        result = await with_customer_fund(data.customer_id,data.amount)
        logger.info(f"Amount with drawed Successfully from the customer : {data.customer_id} with amount {data.amount}")
        return {"message" : f"Customer {data.customer_id}, Fund withdrawed : {data.amount}, account balance : {result}"}
    except Account_Not_Found_Exception:
        logger.info(f"Account_Not_Found for the customer : {data.customer_id}")
        raise account_does_not_exists()
    except Insuficient_Fund_Exception():
        logger.info(f"Insuficient_Fund_Exception for the {data.customer_id}")
        raise insufficient_fund()
    except Exception as e:
        logger.error(f"Something went wrong and details are {str(e)} - data -  {data.customer_id}")
        raise HTTPException(status_code = 400,detail= str(e))
    

@account_router.get("/fetch_customers")
async def fetch_all_customers():
    try:
        customers=load_accounts()
        logger.info(f"All Customer Id has been fetced succesfully")
        return [customer for customer in customers.keys()]
    except Exception as e:
        logger.error(f"Something went wrong and details are {str(e)} ")

    