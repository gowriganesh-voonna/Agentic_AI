
# from db import accounts
from app.data.storage import load_accounts, save_accounts
from app.errors.exceptions import (
    Account_Already_Exists_Exception,
    Account_Not_Found_Exception,
    Insuficient_Fund_Exception
)

from app.utils.loggers import get_logger

logger= get_logger(__name__)

accounts = load_accounts() or {}
async def create_customer_account(customer_id : str):
    if customer_id   in accounts:
        logger.warning(f"Account Already Exists Exception  with {customer_id}")
        raise Account_Already_Exists_Exception()
    accounts[customer_id]=0.0
    save_accounts(accounts)
    return True

async def fund_customer_account(customer_id : str, amount : float):
    if customer_id not in accounts:
        logger.warning(f"Account Not Found with  {customer_id}")

        raise Account_Not_Found_Exception()
    accounts[customer_id]+= amount
    save_accounts(accounts)

    return accounts[customer_id]

async def with_customer_fund(customer_id : str, amount : float):
    if customer_id not  in accounts:
        logger.warning(f"Account Not Found with  {customer_id}")
        raise Account_Not_Found_Exception()
    if accounts[customer_id] < amount :
        logger.warning(f"account does not balance for customer id {customer_id}, current balance {accounts[customer_id]}")
        raise Insuficient_Fund_Exception()
    accounts[customer_id] -= amount
    save_accounts(accounts)

    return accounts[customer_id]



