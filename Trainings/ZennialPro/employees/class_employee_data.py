from functools import wraps
import json
import logging

DATA_JSON = "employees.json"

logging.basicConfig(
    filename = 'class_employees_data.log',
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



class Employee:
    def __init__(self, emp_id, name, department, projects):
        self.emp_id = emp_id 
        self.name = name
        self.department = department 
        self.projects = projects


    @staticmethod
    def from_dict(emp_dict):
        return Employee(emp_dict["emp_id"],
        emp_dict["name"],
        emp_dict["department"],
        emp_dict["projects"]
        )
    

    def to_dict (self):
        return {
        "emp_id": self.emp_id,
        "name": self.name,
        "department": self.department,
        "projects":self.projects
    }

def has_active_project(emp):
    for project in emp.get("projects",[]):
            if project['status'] == 'Active':
                return True
    return False


# for emp in employee_data:
#         for project in emp.get("projects",[]):
#             if project['status']=="Active":
#                 result.append(project)
#                 break



# Helper Methods *************************************

@handle_exceptions
def load_data(filename):
    with open(filename, 'r') as f:
        return json.load(f)
    
@handle_exceptions
def save_data (filename, data):
    with open (filename, 'w') as f:
        json.dump(data, f, indent=4)
        logging.info ("Saved the JSON File Successfully")

def main():
    employees = load_data(DATA_JSON)
    # it will save list of objects address
    emp=[Employee.from_dict(emp) for emp in employees]

    for e in emp:
        # by using to_dict() converting that value to its original value
        employee= e.to_dict()
        if has_active_project(employee):
            print (f"{employee['name']} has active Project ")
        else:
            print (f"{employee['name']} does not have active Project ")
       

    # for emp in employees:
    #     if emp.has_active_project():
    #         print (f"{emp.name} has active Project ")
    #     else:
    #         print (f"{emp.name} does not have active Project ")
    
    
    # emp = Employee (1,"Ameet", "IT", projects= "Projects")
    # emp.has_active_project

if __name__ == "__main__":
    main()