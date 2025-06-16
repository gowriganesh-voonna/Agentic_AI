# Bild employee and Department
# Employee
# Add employee
# Delete Emp
#list emp (all)
# list emp (By condition)
#find emp with highest salary'
# find emp with min salary
# Department
# Add Department

# list department
#delete department
# Roles
# Roles -> Software Developer
#Roles-> IT - Manger

import json
import os 


#File paths
EMPLOYEES_JSON="employees.json"
DEPARTMENTS_JSON="departments.json"
ROLES_JSON="roles.json"
# --------------- Helper methods------------------
def save_to_file(data,file):
    """It will save list of dictionaries"""
    with open(file,"w") as f:
        json.dump(data,f,indent=4)

def load_from_json(file):
    """load and return list of dictionaries from a json file"""
    if not os.path.exists(file):
        return []
    with open(file,"r") as f:
        return json.load(f)

# --------------- Implementation methods ------------------------
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



    def list_departments():
        """Displaying the list of saved departments."""

        departments=load_from_json(DEPARTMENTS_JSON)
        print("\n Available Departmets:")

        for d in departments:
            print(f"{d['dept_id']} : {d['dept_name']}")
        print(" ")

    def __str__(self):
        return f"Department [{self.dept_id}] - {self.dept_name}"

class Role:
    def __init__(self,role_id,role_name):
        self.role_id= role_id
        self.role_name= role_name
    def to_dict(self):
        return vars(self)
    

    @classmethod
    def add_role(cls):
        """Add a role to the list of roles."""
        # Ask for role id and name
        # Load the roles
        # Create a new role
        # Append it to the list of roles
        # Save the roles back to the file
        role_id=input("Enter the role_id :")
        role_name=input("Enter the role_name:")
        roles=load_from_json(ROLES_JSON)
        role=Role(role_id,role_name).to_dict()
        roles.append(role)
        save_to_file(roles,ROLES_JSON)

    def list_roles():
        """Displaying the list of saved roles."""

        roles=load_from_json(ROLES_JSON)
        print("\n Available Roles:")

        for r in roles:
            print(f"{r['role_id']} : {r['role_name']}")
        print(" ")

        

    def __str__(self):
        return f"Role [{self.role_id}] - {self.role_name}"

def menu():
    print("========================structure of the Employee in company==========================")
    while True:
        print("1.Add_Employee_Department")
        print("2.List All Departments")
        print(" 3.Add Roles")
        print("4. List all Roles ")
        print("5. Add Employee")
        print("6.List all Employees")
        print("7. Delete Employee")
        print("0. For Exit")
        choice = int(input("Enter your choice:"))
        if choice == 1:
            Department.add_department()
        elif choice == 2:
            Department.list_departments()
        elif choice == 3:
            Role.add_role()
        elif choice ==4:
            Role.list_roles()
        elif choice == 5:
            Employee.add_employee()
        elif choice == 6:
            Employee.list_employees()
        elif choice == 7:
            Employee.delete_employee()
        elif choice == 0:
            print("Exiting the program")
            break
        else :
            print("\n Invalid choice")

if __name__=="__main__":
    menu()