#dynamic typing in action

x=42
print(type(x))    #<class 'int'>


# varible naming
user_name = "Gowri"  # snake case
MAX_ATTEMPTS =3      #upper case in constants
totalStudets =100  #pascal case 

print("\n -----Varibles Naming COnventions-----")

#Memory management

a=[1,2,3]
b=a
b.append(4)  # it modifies the shared list
print("--------Memory management-------------")
print(a)
print(b)


#creating copy
c=a.copy()
c.append(4)
print("-------Copy of the list-----------")
print(f"A:{a}")
print(f"C: {c}")

# Varibles 
# Basic varible Assignment
name = "Voonna"
age= 22
height = 5.4
is_student = True

print(name,age,height,is_student)

# updating varibles
score =90
score = 100
print(score)

# Dynamic typing exa
# mple
x = 5       # int
y = "five"  # now a string
print(type(x), type(y))

#E- commerence example
product_name ="laptop"
product_price = 5000.00
no_of_items =8
is_Availble = True

Inventory_Value = no_of_items * product_price

print(f"Value of the Inventory_Value {Inventory_Value}")



#Integer operations
age = 25
count = 1_000_000
hex_value = 0xFF #Hexa Decimal
bin_value = 0b1010  # binary_value

price=23.56
pi=3.14
scientific=23.e-6

print(f"Scientifc with power {scientific}")

# Avoiding floating-point precision issues
from decimal import Decimal

total = Decimal('19.9') *Decimal('0.15')

print(f"Displaying total value of decimal { total}")


# String creation and formatting

name ="Voonna"
print(f"Name of the person is {name} !")  #By using format specifier displaying name
message = "Hello Mr {}! Welcome to Zennial Pro".format(name)  #Format method

#String method
course_name ="   Python Full Stack   "
print(course_name.lower())
print(course_name.upper())
print(course_name.strip())
course_name = course_name.strip()
print(course_name.split(" "))


def doc():
    """ Dell is the no 2 laptop brand in india"""
    pass

print(doc.__doc__)