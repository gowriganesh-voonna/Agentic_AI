from pydantic import BaseModel

class CreateAccountRequest(BaseModel):
    customer_id : str

class FundAccountRequest(BaseModel):
    customer_id : str
    amount : float

class WithdrawRequest(BaseModel):
    customer_id : str
    amount : float