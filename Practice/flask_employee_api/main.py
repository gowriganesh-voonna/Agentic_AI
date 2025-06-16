from app.service.employee_service import get_employees,get_bench_employees,get_project_status,get_by_department
from flask import Flask,json, request, jsonify
from app.utils.decoratores import handle_exceptions

app = Flask(__name__)

@handle_exceptions
@app.route("/employees", methods = ["GET"])
def all_employees():
    users=get_employees()
    
    return users

@handle_exceptions
@app.route("/employee/bench", methods =["GET"])
def bench_employee():
    employees=get_bench_employees()

    return employees

@handle_exceptions
@app.route("/employees/active_project",methods=["GET"])
def active_projects():

    employess=get_project_status("active")

    return employess


@handle_exceptions
@app.route("/employees/completed_project",methods=["GET"])
def completed_projects():

    employess=get_project_status("completed")

    return employess

@handle_exceptions
@app.route("/employees/department_name",methods =['POST'])
def get_by_dept_name():
    data=request.get_json()
    department_name=data["Department"]
    try:
        employess=get_by_department(department_name)

        return employess
    except Exception as e:

        return jsonify({"Message":f"{e}"}),500

if __name__=="__main__":
    app.run(debug=True)