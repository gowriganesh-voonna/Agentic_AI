#Decorater :  A decorater is a function that wraps another function to extend or modify its behaviour without changing its code.


# decorater log function.
def log_function(func):
    def wrapper(*agrs,**kwargs):
        print(f"log_function Execution {func.__name__} with args {agrs} ,keywords {kwargs}")
        result=func(*agrs,**kwargs)
        print(f"Completed {func.__name__}")
        return result
    return wrapper

# Sample data
employee = [

    {"name":"Voonna","Department":"IT"},
    {"name":"Gowri","Department":"IT"},
    {"name":"Ganesh","Department":"HR"},
    {"name":"ammu","Department":"Admin" }
  ]


#Get employee Department.
@log_function 
def get_employee_dept(dept):
    return  list(filter(lambda e:e["Department"]==dept , employee))   # function to filter employees based on dept name by using filter and lambda.


#calling decorated function 
employee1=get_employee_dept("IT")
print("Tech Department of the EMployee is :",employee1)