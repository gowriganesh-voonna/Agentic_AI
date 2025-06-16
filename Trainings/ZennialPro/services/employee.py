from utils.helper import load_from_json,save_to_file
import json
import os





EMPLOYEES_JSON=os.path.join(os.path.dirname(__file__), "..","json" ,"employee.json")


class Employee:
    def __init__(self,emp_id,first_name,last_name,doj,salary,department, role):
        self.emp_id=emp_id
        self.first_name= first_name
        self.last_name= last_name
        self.doj=doj
        self.salary=salary
        self.department=department
        self.role=role

    def to_dict(self):
        return vars(self)

    @classmethod
    def add_employee(cls):
        """Add an employee to the list of employees."""
        # Ask for employee details
        # Load the employees
        # Create a new employee
        # Append it to the list of employees
        # Save the employees back to the file
        emp_id=input("Enter the emp_id :")
        first_name=input("Enter the first_name :")
        last_name=input("Enter the last_name :")
        doj=input("Enter the date of joining :")
        salary=input("Enter the salary :")
        department=input("Enter the department :")
        role=input("Enter the role :")

        employees=load_from_json(EMPLOYEES_JSON)
        employee= Employee(emp_id,first_name,last_name,doj,salary,department,role).to_dict()
        employees.append(employee)

        save_to_file(employees,EMPLOYEES_JSON)

    def list_employees():
        """Displaying the list of saved employees."""
        employees=load_from_json(EMPLOYEES_JSON)
        print("\n Available Employees:")

        for e in employees:
            print(f"{e['emp_id']} : {e['first_name']} {e['last_name']} - {e['department']} - {e['role']}")
        print(" ")


    def delete_employee():
        emp_id=input("Enter the emp_id to delete:")
        employees=load_from_json(EMPLOYEES_JSON)
        new_list=list(filter(lambda x:x['emp_id']!=emp_id,employees))
        save_to_file(new_list,EMPLOYEES_JSON)
        print(f"Employee with emp_id {emp_id} deleted successfully")
    def __str__(self):
        return f"Employee_ID [{self.emp_id}] - {self.role}"
        
