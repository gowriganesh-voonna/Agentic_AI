
class Employee:
    company="ZennialPro"
    all_employees=[]

    def __init__(self,name:str,hourly_rate:int):
        self.name=name
        self.hourly_rate=hourly_rate   
        self._hours_worked=0  # using underscore to indicate that this is a private variable
        Employee.all_employees.append(self)

    def __str__(self):   #string method is used to return a string representation of the object
        return f"Employee {self.name} works at {self.company} and earns {self.hourly_rate} per hour"
    
    def __repr__(self): #repr method is used to return a string representation of the object that can be used to recreate the object
        return f"Employee(Name = {self.name}, Hourly_rate={self.hourly_rate})"
    
    def total_salary(self):
        return self.hourly_rate * self._hours_worked
    
    def __getitem__(self,key): # getitem method is used to get the value of the key from the object.
        return getattr(self,key,None) #getattr is used to get the value of the key from the object.
    
    def __setitem__(self,key,value): # setitem method is used to set the value of the key in the object.
        setattr(self,key,value)

    def __eq__(self,other):
        return isinstance(other,Employee) and self.name==other.name 
    
    def __call__(self): #Make instance varible
        print(f"Name of the employee {self.name} works {self.company}")
    
    # def __del__(self):
    #     print(f"Deleted emplyee and his name is {self.name}")

    def __len__(self): # len method is used to return the length of the object
        return len(self.name)

    get_uppercase=lambda self:self.name.upper() # lambda function is used to return the uppercase of the name

    def log_hours(self,hours:int):
        if hours>0:
            self._hours_worked+=hours
        else:
            raise ValueError("Hours worked must be positive")

    @property
    def salary(self):
        return self.hourly_rate * self._hours_worked
    
    @salary.setter
    def salary(self,new_rate:int):
        if new_rate>0:
            self.hourly_rate=new_rate
    
emp1=Employee("Voonna",50000)

print(emp1.total_salary())

#displaying the getitem method
print(emp1["name"])

#setting the setitem method
emp1["name"]="Gowri"

print(emp1.company)

# # displating the string method
# print(f"Displaying the string method:{emp1}")

# displaying the repr method
print(f"Displaying the repr method:rep({emp1})")

#Displaying the call method
emp1()
print(emp1.get_uppercase())

#displaying the getter and setter methode
b=Employee("Ganesh",10000)
c=Employee("Gannu",20000)

d=Employee("Bhavya",34000)

emp1.log_hours(10)
b.log_hours(20)
c.log_hours(9)

#Highest employee salary
highest_salary=max(Employee.all_employees,key = lambda x:x.salary)
print(f"Highest employee salary is {highest_salary.salary}")

