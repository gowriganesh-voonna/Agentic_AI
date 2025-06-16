#Problem statement : Function
# feature : login=> username, password as parameters
#login ==> Your Request --- Your response
# login => voonna123 , welcome123 --- if success : Response will be login successful :: Message "Login_sucessfull" ,code =200.
# login => voonna123 , welcome123 --- if Fail : Response will be login Fail :: Message "Login_fail" ,code =404.

#login_function
def user_login(username:str,password:str)->bool:
   try:
     if username == "Voonna" and password == "Gowri123" :
        print("Login Sucessfull")
        return True
     else:
        print("Login Fail")
        return False
   except Exception as e:
        print(f"Status code : 404. Response {e}")
user_credentials=user_login("Voonna",2)
print(user_credentials)