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
# def modifiy_list(my_list):
#     my_list.append(23)
#     return my_list
# my_list=[1,2,3,4]
# print(modifiy_list(my_list))
# print(my_list)



#Intger operations 
# age=26
# count=1_000_000   #using underscores for readbility (python provides that beauty )
# print(age)
# print(count)

hex_value= 0xFF   #Hexavalue

# converting an decimal number into hex value
# decimal_num = 255
# hex_num = hex(decimal_num)
# print(hex_num)  # Output: 0xff
# print(int("0xff",16))    # converting again back to decimal value


# converting an decimal number into bin value
# bin_value = bin(decimal_num)
# print(bin_value)
# print(int("0b11111111",2))   # converting again back to decimal value


#float operations

# a=23.13  #postive float value
# b=-1.0  # negative float vale
# c= 1.23e4 # Scientific notation (1.23 × 10⁴ = 12300.0)
# d= 3e-5
# print(a,b,c,d)


#Aviding floating point precision issues.
# from decimal import Decimal
# total = Decimal('23.1') * Decimal('32.1')  #precise decimal calculations
# print(total)



# name= "Voonna"
# age =23
# message= f"His name is {name} and his age is {age}"
# print(message)

# #Their is another for using format specifier.
# message= "His name is {} and his age is {}".format(name,age)   #second way of using format specifier.
# print(message)

# #use of the strip method
# message="     Voonna is the founder and CEO of G_Creations      "   #  Strip method will remove unwanted space at the starting and ending only it will remove in the middle .
# print(message.strip())


# by following the naming convention now are using collections
# fruitslist - here we already using an list that does nt make any sense by mentions fruits.
# fruitList=["apple","banna","grap"]
# print(fruitList)
# fruitList.append("mango")
# print(fruitList)
# fruitList.insert(1,"Sapota")
# print(fruitList)
# print(fruitList[-1])
# print(fruitList.sort())
# print(fruitList.remove("banna"))


# Tuples - collections of different items , ordered and immutble data type.
# fruitlist= ("apple","banna")
# city =("Vijayawada","Hyderabad")
# print(f"{fruitlist} and type is {type(fruitlist)}")


# location1,loaction2 = city
# print(location1,loaction2)

# user=("Voonna",22)
# name,age = user
# print(f"Dear {name } your age is {age}")


# user1 =("Voonna","Gowri" , 22)
# name1, _ , age = user1   # you can underscore when 3 parameters their when you want 2 parameters .
# print(f"Dear {name} your age is {age}")



# def get_user_information():
#     name= "Voonna"
#     age = 22
#     return name , age

# name,age=get_user_information()
# print(f"Dear {name } your age is {age}")


def division(a,b):
    quotient = a//b 
    remainder = a%b 
    return quotient, remainder 

q,r = division(5,6)
print(f"the  quotient {q} and the remainder is {r}")