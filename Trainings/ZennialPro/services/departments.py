from utils.helper import load_from_json,save_to_file , logger
import os
import json
from utils.decorators import log_exception

DEPARTMENTS_JSON = os.path.join(os.path.dirname(__file__), "..","json", "departments.json")


class Department:
    def __init__(self,dept_id,dept_name):
        self.dept_id = dept_id
        self.dept_name=dept_name 
        

    def to_dict(self):
        return vars(self)       # It will 
    
    @classmethod
    def add_department(cls):
        """Add a department to the list of departments."""
        # Ask for department id and name
        # Load the departments
        # Create a new department
        # Append it to the list of departments
        # Save the departments back to the file
        dept_id=input("Enter the dept_id :")
        dept_name=input("Enter the dept_name :")

        departments=load_from_json(DEPARTMENTS_JSON)
        department= Department(dept_id,dept_name).to_dict()
        departments.append(department)

        save_to_file(departments,DEPARTMENTS_JSON)


    @log_exception
    def list_departments():
        """Displaying the list of saved departments."""

        departments=load_from_json(DEPARTMENTS_JSON)
        logger.info("All Departments Loaded....")
        print("\n Available Departmets: ")

        for d in departments:
            print(f"{d['dept_id']} : {d['dept_name']}")
        print(" ")

    def __str__(self):
        return f"Department [{self.dept_id}] - {self.dept_name}"
