#Problem statement
# 1. if username and password is correct ->login sucess.
#2. Password reattempt upto 3 times.
#3  Maximum attempt=3.
#4 password ="Voonna123"

def user_login():
    password="Voonna123"
    max_attempts=3
    attempts=0

    while attempts<=max_attempts:
        user_password=input("Enter the password please:")
        if user_password == password :
            print("Login Successfull 200.")
            return True
        else:
            attempts+=1
            print(f"Please Re-Enter the password you have {max_attempts-attempts}")

    print("You have Exceed the maximum limits your access has been denied.")
    return False

#login function()
user_login()
