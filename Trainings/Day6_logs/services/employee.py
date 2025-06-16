import  json
import os

from utils.helpers import load_from_json, save_to_json
EMPLOYEES_JSON = os.path.join(os.path.dirname(__file__), "..", "json", "employees.json")

class Employee:
    def __init__(self, emp_id, first_name, last_name, doj, salary, department, role):
        self.emp_id = emp_id
        self.first_name = first_name
        self.last_name = last_name
        self.doj = doj
        self.salary = salary
        self.department = department
        self.role = role        

    def to_dict(self):
            return vars(self)
    
    def __str__(self):
        return f"Role [{self.role_id}] - {self.role_name}"

    @classmethod
    def add_employee(cls):
        emp_id = input ("Enter the Employee ID")
        first_name = input ("Enter the First Name")
        last_name = input ("Enter the Last Name")
        doj = input ("Enter the Date of Joining")
        salary = input ("Enter the Employee Salary")
        department = input ("Enter the Employee Department")
        role = input  ("Enter the Employee Role")

        # Load the exisitng Employee List
        employees = load_from_json(EMPLOYEES_JSON)
        emp = Employee(emp_id, first_name, last_name, doj, salary, department, role).to_dict()
        employees.append(emp) # Appended the new employee into the exisitng Employee List
        save_to_json(employees, EMPLOYEES_JSON) # Recreate JSON File
        print ("Employee is added to the Collection....")

    def list_employees():
        """List all Employees """
        # emp_id, first_name, last_name, doj, salary, department, role
        employees = load_from_json(EMPLOYEES_JSON)
        print("\033[92m\nRegistered Employees:")
        for e in employees:
            print(f"{e['emp_id']} : {e['first_name']} : {e['last_name']} : {e['salary']}")
        print("\033[0m")  

    def delete_employee():
        emp_id = input ("Enter the Employee ID to delete")
        employees = load_from_json(EMPLOYEES_JSON)
        new_list = list(filter(lambda e: e['emp_id'] != emp_id, employees))
        save_to_json(new_list, EMPLOYEES_JSON) # Recreate the Employee JSON
        print("Employee Deleted...")