from functools import wraps
from flask import jsonify

# creating an function for excpetion handling
def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        try:
            return func(*args,**kwargs)
        except Exception as e:
            return jsonify({"Error":str(e)}),500
    return wrapper