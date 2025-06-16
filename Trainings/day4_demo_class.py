
# define class

class Employee:
    company_name="Zennial_Pro"
    def __init__(self,name,hourly_rate : int):
        self.name=name
        self.hourly_rate=hourly_rate
        self._hours_worked=0

    def log_hours(self,hours:int):
        self._hours_worked+=hours
        return f"Hours Worked : {self._hours_worked}"

    @property
    def total_salary(self):
        return f"Total Salary:{self._hours_worked*self.hourly_rate}"

    @classmethod      # class reference : IT will return class value
    def company_name(cls):
        return f"The name of the company is {cls.Employee}"

    @staticmethod
    def is_valid(value):
        return value>0

emp1=Employee("Voonna",50000)
emp2=Employee("Gowri",70809)


print(emp1.company_name)
print(emp2.company_name)

user1 = emp1.log_hours(4)
print(user1)

print(emp1.total_salary)
print(emp1.company_name)

#Now we are using static method
print(emp1.is_valid(8))