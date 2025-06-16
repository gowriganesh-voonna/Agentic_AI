from flask import request, json , jsonify
from app.models.employee import Employee

DATA = "app/data/employees_details.json"
def load_users():
    try:
        with open(DATA,'r') as f:
            employee_data = json.load(f)

            # if employee_data:
            #     sample=employee_data[0].copy()

            #     if 'salary' in sample:
            #         sample['salary']="*********"
               

            employess = [Employee(**e)for e in employee_data]

            return employess
    except Exception as  e:
        return e
    

employees = load_users()

def get_employees():
    result = [e.to_dict() for e in employees]
    return result

def get_bench_employees():
    bench=list(filter(lambda e:e.is_on_bench() , employees))
    result =[b.to_dict() for b in bench]

    return result

def get_project_status(status):
    project_status =list(filter(lambda e:e.has_active_projects(status),employees))
    result =[p.to_dict() for p in project_status]

    return result

def get_by_department(dept_name):

    by_department_name=get_employees()

    result= [emp for emp in by_department_name if emp['department']==dept_name]
    
    
   
    # result = [emp.to_dict() for emp in employee]

    return result