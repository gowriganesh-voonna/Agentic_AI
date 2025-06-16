
import traceback 
#log function 
def log_function(func):
    def wrapper(*args,**kwargs):
        try:
            return func(*args,**kwargs)    #func= divide_salary_by_employee(salary,count)
        except Exception as e:
            with open("log_file.txt","a") as file:
                file.write(f"\n function {func.__name__}  with args {args} ")
                file.write(f"\n Execution in {func.__name__} \n")
                file.write(traceback.format_exc())
            print(f"Error Logged in {func.__name__}")
            raise # re - raising the exception 
    return wrapper



#sample division function.
@log_function
def divide_salary_by_employee(salary,count):
    return salary/ count

try:
    divide_salary_by_employee(400000,0)
except Exception as e:
    print(e)
    pass 