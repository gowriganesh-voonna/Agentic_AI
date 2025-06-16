from functools import wraps
import json
import logging

DATA_JSON = "employees.json"

logging.basicConfig(
    filename = 'employee_app_poc.log',
    level= logging.INFO,
    format= '%(asctime)s - %(levelname)s - %(message)s'
)

def handle_exceptions(func):
    @wraps (func)
    def wrapper (*args, **kwargs):
        try:
            logging.info(f"Loading the data for file {func.__name__}")
            return func (*args, **kwargs)
        except Exception as e:
            logging.exception(f"Exception in {func.__name__} :{e}")
            print (f"Exception in {func.__name__} :{e}")
    return wrapper

@handle_exceptions
def load_data(filename):
    with open(filename, 'r') as f:
        return json.load(f)
    
@handle_exceptions
def save_data (filename, data):
    with open (filename, 'w') as f:
        json.dump(data, f, indent=4)
        logging.info ("Saved the JSON File Successfully")

@handle_exceptions
def find_by_department(employee_data, department_name):
    # standard approach 
    result = []
    for emp in employee_data:
        if emp["department"] == department_name:
          result.append(emp)
    print (f"Standard Approach result is {result}")  

    # Optimized Approach - Lambda
    result  = list(filter(lambda e: e['department']== department_name,employee_data ))
    print (f"Lambda Optimized Approach result is {result}")  

    # Optimized Approach using list comprehension
    result  = [emp for emp in employee_data if emp['department'] == department_name ]    
    print (f"List  Comprehension - Optimized Approach result is {result}")  

@handle_exceptions
def find_by_active_project (employee_data):

    # Standard Approach 
    result = []
    for emp in employee_data:
        for project in emp.get('projects', []):
            if project['status'] == 'Active':
                result.append (emp)
                break    
    print ("Standard Approach - Nested for Loops", result )

    # Optimized using generators, All 
    result =  [emp for emp in employee_data  if any(p['status'] == 'Active' for p in emp.get('projects',[]))]

def load_data_standard(filename):   
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except Exception as e:
        logging.exception(f"Exception in Function : load_data ")

if __name__ == "__main__":

    employee_data = load_data(DATA_JSON)
    find_by_department (employee_data, 'Tech')
    find_by_active_project(employee_data)
