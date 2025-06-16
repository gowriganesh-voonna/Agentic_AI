from functools import wraps
import json
import logging

DATA_JSON = "user_login.json"

logging.basicConfig(
    filename = 'user_login.log',
    level= logging.INFO,
    format= '%(asctime)s - %(levelname)s - %(message)s'
)

def handle_exceptions(func):
    @wraps (func)
    def wrapper (*args, **kwargs):
        try:
            logging.info(f"Loading the data for file {func.__name__}")
            return func (*args, **kwargs)
        except Exception as e:
            logging.exception(f"Exception in {func.__name__} :{e}")
            print (f"Exception in {func.__name__} :{e}")
    return wrapper