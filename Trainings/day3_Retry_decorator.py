
# retry decorator to retry a function call if it raises an exception

import random

def retry_decorater(max_attempts):
    def decorater(func):
        def wrapper(*args,**kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args,**kwargs)
                except Exception as e:
                    print(f"Attempt failed Function recalling {attempt+1}.Error {e}")
            print("All retries are failed.")
        return wrapper
    return decorater


@retry_decorater(3)
def risky_function():
    if random.random() <0.7:
        raise ValueErro("Error Occurred")
    return "Success"


print(risky_function())