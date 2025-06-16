from fastapi import HTTPException,status

class Account_Already_Exists_Exception(Exception):
    """It will raise an Exception if Account Already Exists"""
    pass

class Account_Not_Found_Exception(Exception):
    """It will raise an Exception if Account Does Not exists"""
    pass

class Insuficient_Fund_Exception(Exception):
    """It will raise an Exception when amount is Insufficient"""

def account_already_exists():
    return HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = " Account Already Exists"
    )

def account_does_not_exists():
    return HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = " Account Not Found"
    )

def insufficient_fund():
     return HTTPException(
        status_code = status.HTTP_400_NOT_FOUND,
        detail = " Insufficient Fund "
    )