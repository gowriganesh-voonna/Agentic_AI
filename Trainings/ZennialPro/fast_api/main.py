
from fastapi import FastAPI,HTTPException, Request
from pydantic import BaseModel

import logging
import time
import json

logger = logging.getLogger(__name__)

logging.basicConfig(
    filename= "employee_app.log",
    level= logging.INFO,
    format= '%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

app=FastAPI(
    title = "Employee API",
    description = "Employee API tool will return crud operations",
    version = "1.0.0", docs_url ="/documents"
)

#----------------------Models -------------------------------
class Project(BaseModel):
    project_id : str
    name       : str
    status     : str

class Employee (BaseModel):
    emp_id : str
    name   : str
    department : str
    salary  : int
    designation : str
    location  : str
    dob  : str
    projects : list[Project]

class Login_User(BaseModel):
    username : str
    password : str

#----------------- load Employee -----------------------

with open("employees_details.json",'r') as f:
    raw_employees = json.load(f)
Employees =[Employee(**r) for r in raw_employees]

@app.post("/employees/login")
async def login_user(data :Login_User ):
    if data.username == "Gowri"  and data.password =="12345@":
        return{"Message":"Login Successfull"}
    raise HTTPException(status_code =401 , detail = "Login_Failed")

@app.get("/employees" , response_model = list[Employee])
async def get_all_employees():
    return Employees

@app.get("/employees/bench",response_model = list[Employee])
async def get_bench_employees():
    return [emp for emp in Employees if not emp.projects]

@app.get("/employees/project-status/{status}",response_model = list[Employee])
async def get_by_status(status: str):
    return [emp for emp in Employees if any(e.status == status for e in emp.projects)]

