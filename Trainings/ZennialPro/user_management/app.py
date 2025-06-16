from flask import Flask,request, jsonify

import json
import os
import logging

app= Flask(__name__) # Create an flask Application


logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

DATA_FILE="users.json"
@app.route("/welcome")
def hello():
    return "Hello Gowri Ganesh"

@app.route("/register",methods=["POST"])
def register_user():
    data = request.get_json()   # get the users supplied data
    #Mandatory fields 
    #Take each item from required and compare with each item of body values
    required =["first_name","last_name","email","dob","password"]
    users=load_user()
    if not all(r in data for r in required):
        return jsonify({"Message":"All fields required",
                        "Code":"501"}),400
    # Add new users details for the user collection
    users.append(data)
    # save users details back to the json
    save_user(users)

    return jsonify({"Message":"User Registered successfully",
                    "Code":"200"})

@app.route("/users")
def list_users():
    users=load_user()
    return users




@app.route("/change_password", methods=["POST"])
def change_password():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "No JSON data provided"}), 400
            
        email = data.get("email")
        if not email:
            return jsonify({"message": "Email is required"}), 400
            
        email = email.strip().lower()
        old_password = data.get("old_password")
        new_password = data.get("new_password")
        
        if not old_password or not new_password:
            return jsonify({"message": "Both old_password and new_password are required"}), 400

        users = load_user()
        for u in users:
            stored_email = u["email"].strip().lower()
            app.logger.info(f"Comparing emails: input='{email}' stored='{stored_email}'")
            
            if stored_email == email:
                app.logger.info("Email match found")
                if u["password"] == old_password:
                    u["password"] = new_password
                    save_user(users)
                    return jsonify({"message": "Password changed successfully."}), 200
                else:
                    return jsonify({"message": "Old password is incorrect."}), 400

        app.logger.info(f"No user found with email: {email}")
        return jsonify({"message": "User does not exist."}), 404
    except Exception as e:
        app.logger.error(f"Error in change_password: {str(e)}")
        return jsonify({"message": f"Something went wrong... {str(e)}"}), 500
        
        
        
@app.route("/user/login", methods=["POST"] )
def user_login():
    try:
        data=request.get_json()
        email=data.get("email")
        password=data.get("password")
        user_data=find_user_by_email(email)
         
        app.logger.info(f"User found is {user_data}")
        app.logger.info(f"User found is {data.get("email")}")

        if not email or not password :
            return jsonify({"Message": "Mail or password are required"}),400
        
        if user_data and user_data["password"]==data.get("password"):
            return jsonify({"message":f"user {email} logged in successfully"}),200
        else:
            return jsonify({"message":f"user {email} login fail "}),404
    except Exception as e:

        return jsonify({"Message":f"Internal Server error"})





#Helper method
#Genrator - next () - it will return first match found if not returns None
@app.route("/find_user/<email>")
def fetch_user(email):
    user=find_user_by_email(email)
    if user:
        return user
    return jsonify({"Message":" User not Found"}),404

def find_user_by_email(email):
    users=load_user()
    return next((u  for u  in users if u["email"]==email),None)


def load_user():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE , "r") as f:
        return json.load(f)







def save_user(users):
    with open(DATA_FILE,"w") as f:
        json.dump(users,f)
        
        
        
if __name__=="__main__":
    app.run(debug=True)

