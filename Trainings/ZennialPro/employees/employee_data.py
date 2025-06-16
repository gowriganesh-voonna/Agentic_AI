# {
#         "emp_id": "E003",
#         "name": "Rohit Desai",
#         "department": "Finance",
#         "projects": [
#             {
#                 "project_name": "Audit",
#                 "status": "Completed"
#             }
#         ]
#     }

#Problem Statement
# Building a Python program that manages employee records stored in
# a JSON file. Each employee belongs to a department and may work on multiple projects. 
# Your program should allow loading, saving, and querying data using both standard Python 
# techniques (loops, conditionals) and optimized methods (lambda, comprehension, generator, etc.). 
# Demonstrate the difference clearly in your code with comments.


from functools import wraps
import json
import logging

DATA_JSON ="employees.json"

logging.basicConfig(
    filename = 'employee_app_poc.log',
    level = logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(message)s'
)

def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        try:
            logging.info(f"Loading the data for file {func.__name__}")
            return func(*args,**kwargs)
        except Exception as e:
            logging.exception(f"Exception  in {func.__name__} : {e}")
            print(f"Exception in {func.__name__} : {e}")
    return wrapper
    
@handle_exceptions
def load_data(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except Exception as e:
        logging.exception(f"Exception in Function :load_data :{e}")
    
@handle_exceptions
def save_data(file_name,data):
    with open(file_name,"w") as f:
        json.dump(data,f ,indent=4)
        logging.info("Data Saved Sucessfully in json")


@handle_exceptions
def find_by_department(employee_data,department_name):

    #Standard approach
    result=[]
    for emp in employee_data:

        if emp["department"] == department_name:
            result.append(emp)
    print(f"Stanard Approach result is {result}")


    # optimized approach through lambda

    result = list(filter(lambda e:e["department"]==department_name,employee_data))

    print(f"Optimized Approach result - lambda {result}")

    #optimized approach - list
    result = [emp for emp in employee_data if emp["department"] == department_name ]
    print(f"Optimized Approach result - lambda {result}")


@handle_exceptions
def find_by_active_department(employee_data):
    result=[]

    for emp in employee_data:
        for project in emp.get("projects",[]):
            if project['status']=="Active":
                result.append(project)
                break
    #Standard - Approach
    print(f"Standard Approach - Nested for loops {result} ")

    # Optimized Approach
    result=list(emp for emp in employee_data if any(p["status"]=="Active" for p in emp.get("projects",[])))
    print(f"Optimized  Approach - Nested for loops {result} ")

@handle_exceptions
def summary_stats(employee_data):
    #displaying dept count with emp count by standard approach
    dept_count = {}
    for emp in employee_data:
        dept_name = emp["department"]
        dept_count[dept_name] = dept_count.get(dept_name,0)+1
    #Displaying all departments with total emploees
    print(f"Total Count: {dept_count}")

    # Now displaying max employees (highest) department in standard 
    result= max(dept_count, key=dept_count.get)
    print(f"Deaprtment with Maxmimum or Most number of employees is '{result}'")

    #now by single statement it is an key-value pair so list is not possible we will use tuple
    result=max([(k,v) for k,v in dept_count.items()],key= lambda x:x[1])
    print(f"Deaprtment with Maxmimum or Most number of employees is '{result}'")

    # Unique Department - optimized
    unique_dept = set(emp["department"] for emp in employee_data)
    print(f"Optimized : unique dept { unique_dept}")
    pairs=[(emp['emp_id'],emp['name'],emp['department']) for emp in employee_data]
    print(f"ID-Name Pairs - Tuples :{pairs}")


@handle_exceptions
def iterator(employee_data):
    emp_iter = iter(employee_data)  # it will travserse all the list
    print(next(emp_iter))  # first employee
    print(next(emp_iter))  # second employee
    print(next(emp_iter))




if __name__ == "__main__":
    employee_data=load_data(DATA_JSON)
    # find_by_department(employee_data,"Tech")
    # find_by_active_department(employee_data)
    # summary_stats(employee_data)
    