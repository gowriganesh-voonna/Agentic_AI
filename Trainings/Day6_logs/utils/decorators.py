import functools
import traceback
from utils.helpers import logger

def log_exception(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug (f"Entering the Function: {func.__name__}")
        try:
            result = func(*args, **kwargs) # Invole the Calling Function
            logger.debug (f"Executed and Exiting the Function: {func.__name__}")
            return result 
        except Exception  as e:
            logger.error (f"Error  while executing function: {func.__name__} : Trace {e}")
    return wrapper