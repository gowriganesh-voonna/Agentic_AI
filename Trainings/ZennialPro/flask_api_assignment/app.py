import json
import logging
import os 
from flask import Flask, request, jsonify
import datetime

app = Flask (__name__)

filename = "users_data.json"
logging.basicConfig(
    filename='userlogin.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


@app.route("/register", methods = ["POST"])
def register_user():
    """ register_user : Method will Register a New User in Database """
     # Step  1 - Get the User supplied values From Body
    data = request.get_json() 
    required = ["user_id","first_name","last_name","username","password","age","dob"]

    if not all(u in data for u in required):
        app.logger.info(f"All fields are required")
        return jsonify({"Message":"All fileds are required."}),422
    
    # load existing users file and check whether it exists or not
    users =load_users()
    for user in users:
        if user["username"] == data["username"]:
            return jsonify({"Messgae":"User Name Already Exists"}),406
        
    
    #Need to check by dob correct age or not 


    # adding user data to the .json     
    users.append(data)
    save_user(users)
    app.logger.info("User saved Successfully")

    return jsonify({"Message":f"User {data['username']} added successfully"}),200




@app.route("/user/login", methods=["POST"])
def user_login():
     
     # using try to 
     try:
        #Step1 : Get the data
        data=request.get_json()
      

        # Step2 : Get user by username from load_users()
        user=get_user_by_username(data["username"])
        

        # Step 3 : checking username and password if it is true success message
        if user.get("username") == data["username"] and user.get("password") == data.get("password"):
            app.logger.info(f"User Login Successfull for thr {data["username"]}")
           
            return jsonify({"Message":"Login Successfull"}),200
        else:
            app.logger.info(f"User Login fail for thr {data["username"]}")
            return jsonify({"Message":"Login Failed"}),400

     except Exception as e:
        app.logger.info(f"Exception : {e}")
        return jsonify({"Message":f"{e}"}),408



@app.route("/users",methods=["GET"])
def list_all():
    # Loading all users
    users=load_users()
    app.logger.info("Loading all users")
    return users


def get_user_by_username(username):
    """This function returns user """
    users=load_users()
    user=next(( u for u in users if u["username"]== username ),None)
    return user





def load_users():
    if not os.path.exists(filename):
        return []
    with open(filename,"r") as f:
        return json.load(f)
    

def save_user(data):
    with open(filename,"w") as f:
        json.dump(data,f , indent=4)
        app.logger.info("Data Saved Successfully")

if __name__ == "__main__":    
    app.run("0.0.0.0", 5000)