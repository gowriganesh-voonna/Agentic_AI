import json
import logging
from datetime  import datetime
from functools import wraps

logging.basicConfig (
    filename = 'employee_app.log',
    level = logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(message)s'
)

logging = logging.getLogger(__name__)

def handle_exceptions(func):
    @wraps(func)
    def wrapper (*args, **kwargs):
        try:
            logging.info(f"Executing: {func.__name__}")
            return func(*args, **kwargs)
        except Exception as e:
            logging.exception(f"Error while Executing: {func.__name__} : {e}")
    return wrapper

class Project:
    def __init__(self, project_id, name,status):
        self.project_id = project_id 
        self.name = name
        self.status = status

class Employee:
    def __init__(self, emp_id, name, department,salary,designation, location,dob, projects):
        self.emp_id =  emp_id
        self.name = name 
        self.department = department
        self.salary = salary
        self.designation =  designation
        self.location = location
        self.dob = dob
        self.projects = [ Project(**p) for p in projects]

    def is_on_bench(self):
        return len(self.projects) == 0 

    def has_project_with_status(self, status):
            return any (p.status == status for p in self.projects)
    
    def get_age (self):
        birth_date = datetime.strptime(self.dob, "%Y-%m-%d")
        return (datetime.now() - birth_date).days // 365
 




# ***** Helper Methods
@handle_exceptions
def load_employees(filepath):
    with open (filepath, 'r') as f:
        employees  = json.load(f)
        return [Employee(**emp) for emp in  employees]

def showcli():
    while True:
        print ("\n ===== Employee Search Menu =====")       
        print ("1. List All Employees")
        print ("2. Find All Employees On Bench")
        print ("3. Find All Employees With Active Projects")
        print ("4. Find All Employees With Completed Projects")
        print ("5. Search Employees By Department")
        print ("6. Search Employees By Designation")
        print ("7. Search Employees By Location")
        print ("8. Search Employees By Salary Range")
        print ("9. Find All Employees Aged Above 'X'")
        print ("10.Find All Employees Aged Between X and Y")
        print ("11.Find All Employees In Specific Project")
        print ("12.Count Employees per Department")
        print ("13.Exit")

        choice = input("Please Select an Option : ")

        if choice == "1": # List All Employees
            for emp in employees:
                print(f"{emp.emp_id} - {emp.name} - {emp.department} - {emp.salary} - {emp.designation} -  {emp.location} - {emp.dob}")
        
        elif choice == "2": # Find All Employees On Bench
            for emp in employees:
                logging.info(f"{emp.name}")
                if emp.is_on_bench():
                    print(f"{emp.emp_id} - {emp.name} - {emp.department} - {emp.salary} - {emp.designation} -  {emp.location} - {emp.dob}")
        
        elif choice == "3": # Find All Employees With Active Projects
            for emp in employees:
                if emp.has_project_with_status('active'):
                    print(f"{emp.emp_id} - {emp.name} - {emp.department} - {emp.salary} - {emp.designation} -  {emp.location} - {emp.dob}")
        
        elif choice == "4": # Find All Employees With Completed Projects
            for emp in employees:
                if emp.has_project_with_status('completed'):
                    print(f"{emp.emp_id} - {emp.name} - {emp.department} - {emp.salary} - {emp.designation} -  {emp.location} - {emp.dob}")
        
        elif choice == "5": # Search Employees By Department
            department = input ("Please enter Department Name :")
            for emp in employees:
                if emp.department.lower() == department.lower():
                    print(f"{emp.emp_id} - {emp.name} - {emp.department} - {emp.salary} - {emp.designation} -  {emp.location} - {emp.dob}")

        elif choice == "6": # Search Employees By Designation
            designation = input ("Enter the Employee Designation : ")
            for emp in employees:
                if emp.designation.lower() == designation.lower() :
                    print(f"{emp.emp_id} - {emp.name} - {emp.department} - {emp.salary} - {emp.designation} -  {emp.location} - {emp.dob}")

        elif choice == "7": # Search Employees By Location
            location = input ("Enter the Location : ")
            for emp in employees:
                if emp.location.lower() == location.lower() :
                    print(f"{emp.emp_id} - {emp.name} - {emp.department} - {emp.salary} - {emp.designation} -  {emp.location} - {emp.dob}")
        
        elif choice == "8": # Search Employees By Salary Range
            min_sal = int(input ("Enter Minimum salary for the Employee : "))  # 75K
            max_sal = int(input ("Enter Maximum for the Employee : ")) # 100K
            for emp in employees:
                if min_sal <= emp.salary <= max_sal:
                    print(f"{emp.emp_id} - {emp.name} - {emp.department} - {emp.salary} - {emp.designation} -  {emp.location} - {emp.dob}")

        elif choice == "9": # Find All Employees Aged Above 'X'
            age_limit = int (input ("Enter the age threshold : "))
            for emp in employees:
                if emp.get_age() > age_limit:
                    print(f"{emp.emp_id} - {emp.name} - {emp.department} - {emp.salary} - {emp.designation} -  {emp.location} - {emp.dob}")
        
        elif choice == "10": # Find All Employees Aged Between X and Y
            min_age = int(input("Enter Minimum Age : "))
            max_age = int(input("Enter Max Age : "))
            for emp in employees:
                age = emp.get_age()
                if min_age <= age <= max_age:
                    print(f"{emp.emp_id} - {emp.name} - {emp.department} - {emp.salary} - {emp.designation} -  {emp.location} - {emp.dob}")

        elif choice == "11": # Find All Employees In Specific Project
            project_name = input ("Enter the name of Project : ").lower()
            for emp in employees:
                if any (project.name.lower() == project_name for project in emp.projects):
                    print(f"{emp.emp_id} - {emp.name} - {emp.department} - {emp.salary} - {emp.designation} -  {emp.location} - {emp.dob}")

        elif choice == "12": # Count Employees per Department
            dept_count = {}
            for emp in employees:
                dept_count[emp.department] = dept_count.get(emp.department, 0) + 1
            for dept, count in dept_count.items():
                print (f"{dept} : {count} employees")

        elif choice == "13": # Exit
            print ("Exititng Application. See you later.....")
            break
        else:
            print ("Invalid Choice, please ennter number between 1 to 13")

if __name__ == "__main__":
    filepath = "employee_details.json"
    employees = load_employees(filepath=filepath)

    if employees:
        showcli()
    else:
        print ("No Employees found or file is missing")