# # Arithmetic operators
# # Assignment operators
# # Comparison operators
# # Logical operators
# # Identity operators
# # Membership operators
# # Bitwise operators 


# # Arithmetic operators
# x,y = 23,8

# print(x + y)  # Output: 13
# print(x - y)  # Output: 7
# print(x * y)  # Output: 30
# print(x / y)  # Output: 3.333...
# print(x % y)  # Output: 1   Modules 
# print(x ** y) # Output: 1000   #Power or exponent
# print(x // y) # Output: 3 Floor divison 


# # Assignment Operators

# # Initial value
# x = 10
# print("Initial x =", x)

# # Addition assignment
# x += 5
# print("After x += 5:", x)

# # Subtraction assignment
# x -= 3
# print("After x -= 3:", x)

# # Multiplication assignment
# x *= 2
# print("After x *= 2:", x)

# # Division assignment
# x /= 4
# print("After x /= 4:", x)

# # Modulus assignment
# x %= 3
# print("After x %= 3:", x)

# # Floor division assignment
# x = 10
# x //= 3
# print("After x //= 3:", x)

# # Exponent assignment
# x **= 2
# print("After x **= 2:", x)

# # Bitwise AND assignment
# x &= 1
# print("After x &= 1:", x)

# # Bitwise OR assignment
# x |= 2
# print("After x |= 2:", x)

# # Bitwise XOR assignment
# x ^= 3
# print("After x ^= 3:", x)

# # Bitwise right shift assignment
# x >>= 1
# print("After x >>= 1:", x)

# # Bitwise left shift assignment
# x <<= 2
# print("After x <<= 2:", x)



# # Basic comparisons
# x, y = 5, 7
# print("\n ------ Comparison operators-------------------")
# print(f"\n \n X:{x} and Y:  {y}")
# print("equal = ",x == y)           # Equal to: False
# print("not_equal = ",x != y)       # Not equal to: True
# print("greater = ",x > y  )        # Greater than: False
# print("less =", x < y)             # Less than: True
# print("greater_equal = ",x >= y )  # Greater than or equal: False
# print("less_equal =", x <= y)      # Less than or equal: True

# # String comparisons
# name1 = "Alice"
# name2 = "Bob"
# print(name1 < name2)      # True (alphabetical comparison)

# # Real-world example: Age verification
# age = 18
# is_adult = age >= 18     # True
# can_vote = age >= 18     # True


# # logical operators
# user_name ="Voonna"
# password = "Gowri123"

# input_username = input("Please Enter username :")
# input_password = input("Please enter the password :")

# if user_name == input_username and password == input_password :
#     print("Login Successfull")
# else:
#     print(" Login fail")
# guest_name ="Guest1"
# input_guest = input("ENter the guest name")

# if user_name == input_username or input_guest == guest_name :
#     print("OR operator success")

# else:
#     print("login for the guest")


print("-----------Bitwise Operator ----------------------")

a=12
b=13
print("Bitse operation will be performed on binary values only")
print(f"Binary Value of a : {bin(a)}")
print(f"Binary value of b : {bin(b)}")
print(f"Bitwise AND : {(a & b)} in binary value {bin(a&b)}")
print(f"Bitwise OR : {(a | b)} in binary value {bin(a|b)}")
print(f"Bitwise XOR : {(a ^ b)} in binary value {bin(a^b)}")
print(f"Bitwise Left Shift : {(a << b)} in binary value {bin(a<<b)}")
print(f"Bitwise Right Shift : {(a >> b)} in binary value {bin(a>>b)}")
print(f"Bitwise not a: {~a} , b: {~b}")

print("----------------Identity and Membership Operators----------------------------")
list1 = [1,2,3,4]
list2 =[1,2,3,4]
list3 = list1

print(f"List1 : {list1}, list2 : {list2}")
print(list1 is list3)
print(list1 is list2)
print(list1 is not list2)

print("Member ship operator")
students_name =["Voonna","Gowri" ,"Ganesh" ,"Gannu"]
print("Gowri" in students_name)
print("Rahul" not in students_name )
print("Rahul" in  students_name )

# Real-world example: Menu options
MENU_OPTIONS = {'view', 'edit', 'delete'}
user_action = 'edit'

if user_action in MENU_OPTIONS :
    print(f"Processing user Operation {user_action}")

else:
    print("Invalid Operation")