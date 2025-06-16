import json
import logging
from flask import Flask, request, jsonify

app = Flask (__name__)

VALID_USERNAME = "voonna@gmail.com"
VALID_PASSWORD = "password123"

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
    required = ["user_id","first_name","last_name","username","password",]

@app.route('/user/login', methods=['POST'])
def login():

    login_data = request.get_json()
    username = login_data.get("username")
    password = login_data.get("password")

    if username == VALID_USERNAME and password == VALID_PASSWORD:
        logging.info(f"{username} logged in")
        
        return jsonify({
            "status" : "success", 
            "message" : f"{username} logged in"
        }), 200
    else:
        logging.warning(f"Login failed for {username}")        
        return jsonify({
            "status" : "failed", 
            "message" : f"Login failed for {username}"
        }), 401       

@app.route('/users/', methods=['GET'])
def list_users():
    users = ["Voonna", "Gowri", "Ganesh", "Suresh"]
    # return users, 200
    return jsonify({"users": users}), 200


    # if Username and Password are Correct 
    #   Return Success Response (HTTP Codes, Messages)
    # Else
    #   Return Failed Response (HTTP Codes, Messages)
    return True


if __name__ == "__main__":    
    app.run("0.0.0.0", 5000)