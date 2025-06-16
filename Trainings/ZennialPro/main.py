
from services.departments import Department
from services.employee import Employee
from services.roles import Role
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