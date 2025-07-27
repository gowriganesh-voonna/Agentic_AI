from functools import wraps
import logging
from fastapi import HTTPException
from app.utiles.logger import get_logger
 
logger = get_logger(__name__)  # Using your custom logger
 
def handle_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            logger.info(f"Calling function: {func.__name__}")
            result = await func(*args, **kwargs)
            logger.info(f"Function {func.__name__} completed successfully")
            return result
        except Exception as e:
            logger.exception(f"Exception in function: {func.__name__} - {str(e)}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
    return wrapper