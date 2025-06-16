from flask import Flask , request , jsonify

import os,json, jwt, datetime 

app= Flask(__name__)


SECRET_KEY = "voonna123"
TOKEN_EXPIRY_MINUTES = 30

def generate_token(user_name,password):
    users=load_users()
    for user in users:
        if user["user_name"] == user_name and user["password"] == password :
            payload ={
                "user_name":user_name,
                "exp": datetime.datetime.utcnow()+datetime.timedelta(minutes=TOKEN_EXPIRY_MINUTES)
            }
            token=jwt.encode(payload,SECRET_KEY, algorithm= "HS256")
            return token
    return None
    

def decode_token(token):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=["HS256"])    # we need to pass list of algoirthms
        return payload
    except jwt.ExpiredSignatureError:
        return "Token Expired"
    except jwt.InvalidKeyError:
        return "Invalid Error"



@app.route("/register",methods=["POST"])
def register():
    data=request.get_json()
    email=data.get("email").strip().lower()
    
    required = ["user_name","password","email","dob"]
    if not all(r in data for r in required):
        return jsonify({"Message":"Required fields are Missing"}),404
    
    users=load_users()
    for u in users:
        print(u)
        if u["email"]==email:
            return jsonify({"Message":"User Already Exist"}),405
    users.append(data)
    
    save_user(users)
   
    return jsonify({"Message":f"User {data["user_name"]} added successfully"}),200


@app.route("/user/<email>")
def get_user_by_email(email):
    users=load_users()
    user=next(( u for u in users if u["email"]== email ),None)
    return user
        
            
    
@app.route("/login",methods=["POST"])
def user_login():
    try:
        data=request.get_json()
        user=get_user_by_email(data["email"])
        if user.get("email") == data["email"] and user.get("password") == data.get("password"):
            return jsonify({"Message":"Login Successfull"}),200
        else:return jsonify({"Message":"Login Failed"}),400

    except Exception as e:
        return jsonify({"Message":f"{e}"}),408
    


@app.route("/change_password",methods=["POST"])
def change_password():
    data=request.get_json()
    try:
        users=load_users()
        for user in users:
            print(user)
            if user.get("email") == data["email"] and user.get("password") == data.get("old_password"):
                
                user["password"]=data["new_password"]
                save_user(users)
                return jsonify({"Message":"Password changed"}),200
        return jsonify({"Message":"Something wrong"}),400  

    except Exception as e:
        return jsonify({"Message":f"{e}"}),407
            






@app.route("/users")
def fetch_users():
    users=load_users()
    return users
   
def get_user_path():
    #d:\self_practice\app.py
    current_dir= os.path.dirname(__file__)
    default_path = os.path.join(current_dir,"data","users_data.json")
    return os.path.abspath(default_path)


def load_users():
    user_file_path=get_user_path()

    if not  os.path.exists(user_file_path):
        return []
    with open(user_file_path,"r") as f:
        return json.load(f)
        
def save_user(user):
    user_file_path=get_user_path()
    os.makedirs(os.path.dirname(user_file_path),exist_ok=True)

    with open(user_file_path,"w") as f:
        json.dump(user,f ,indent=4)



@app.route("/generate_token", methods=["POST"])
def token_generate():
    data = request.get_json()
    if not data.get("user_name") or not data.get("password"):
        return jsonify({"Message": "user_name and password are required"}), 400
    
    token = generate_token(data["user_name"], data["password"])
    if token:
        return jsonify({"token": token}), 200
    else:
        return jsonify({"Message": "Invalid credentials"}), 401

    

@app.route("/decode_token", methods=["POST"])
def token_decode():
    data=request.get_json()
    if not (data["token"]):
        return jsonify({"Message":"token required"}),400
    return decode_token(data["token"])
    

if __name__=="__main__":
    app.run(debug=True,port=5001)
    




