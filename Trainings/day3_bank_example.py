#Problem statement
# two classes Bank and customer
#Customer - Gowri , Account -> Balance ->499000
#Customer - Pavani, Account -> Balance -> 40000
# from balance he should withdraw amount 2000 -> Success.
# you need to log all customers.

from datetime import datetime

def log_transcation(func):
    def wrapper(*args,**kwargs):
        result= func(*args,**kwargs)
        print(f"[{datetime.now()}] {func.__name__} is executed ")
    return wrapper

class Bank:
    def __init__(self,name):
        self.name=name
        self.customers=[]
    
    def add_customers(self,customer):
        self.customers.append(customer)
class Customer:
    def __init__(self,name,balance):
        self.name= name
        self.balance=balance
    @log_transcation
    def deposite(self,amount):
        self.balance+=amount
        message=f"Dear {self.name} Amount has been credited successfully.Total balance is {amount}"
        print(message)
    
    def withdraw(self,amount):
        if amount>self.balance:
            print( f"Dear {self.name} Insufficient Balance")
        else:
            self.balance-=amount
            message=f"Dear {self.name} Amount has been desposited successfully.Total balance is {amount}"
            print(message)



my_bank=Bank("SBI")

#create customer
cust1=Customer("Gowri",50009)
cust2=Customer("Surendhra",89900)


#Adding New customer
my_bank.add_customers(cust1)
my_bank.add_customers(cust2)


cust1.deposite(150000)
cust2.deposite(500)
cust1.withdraw(1000)
cust2.withdraw(234)