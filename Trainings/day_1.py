#Data Types.

a=1 #integer
b=1.5 # float
c= 4j

# print(a)
# print(b)
# print(c)

# print(f"data type of a {type(a)}")
# print(type(b))
# print(type(c))

# now re defining varible 
a=2
b=3.3
c=3j
# print(a)  # immutable we are re-definig the varibles.
# print(b)
# print(c)

# my_list=[1,2,3]  # list is an mutable data type
# my_list.append(4)
# print(my_list)

#now defining an list by using def method
def modifiy_list(my_list):
    my_list.append(23)
    return my_list
my_list=[1,2,3,4]
print(modifiy_list(my_list))
print(my_list)



#Intger operations 
age=26
count=1_000_000   #using underscores for readbility (python provides that beauty )
print(age)
print(count)

hex_value= 0xFF   #Hexavalue

# converting an decimal number into hex value
decimal_num = 255
hex_num = hex(decimal_num)
print(hex_num)  # Output: 0xff
print(int("0xff",16))    # converting again back to decimal value


# converting an decimal number into bin value
bin_value = bin(decimal_num)
print(bin_value)
print(int("0b11111111",2))   # converting again back to decimal value


#float operations

a=23.13  #postive float value
b=-1.0  # negative float vale
c= 1.23e4 # Scientific notation (1.23 × 10⁴ = 12300.0)
d= 3e-5
print(a,b,c,d)


#Aviding floating point precision issues.
from decimal import Decimal
total = Decimal('23.1') * Decimal('32.1')  #precise decimal calculations
print(total)



