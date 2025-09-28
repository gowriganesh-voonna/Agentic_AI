from functools import wraps
import logging
from fastapi import HTTPException
from app.utiles.logger import get_logger
from pymongo.errors import DuplicateKeyError
 
logger = get_logger(__name__)  # Using your custom logger
 
# def handle_exceptions(func):
#     @wraps(func)
#     async def wrapper(*args, **kwargs):
#         try:
#             logger.info(f"Calling function: {func.__name__}")
#             result = await func(*args, **kwargs)
#             logger.info(f"Function {func.__name__} completed successfully")
#             return result
#         except Exception as e:
#             logger.exception(f"Exception in function: {func.__name__} - {str(e)}")
#             raise HTTPException(status_code=500, detail="Internal Server Error")
#     return wrapper


def handle_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            logger.info(f"Calling function: {func.__name__}")
            result = await func(*args, **kwargs)
            logger.info(f"Function {func.__name__} completed successfully")
            return result

        except ValueError as e:
            # Bad request (e.g., invalid input, duplicate hub_id check in your service)
            logger.warning(f"ValueError in {func.__name__}: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))

        except LookupError as e:
            # Resource not found
            logger.warning(f"LookupError in {func.__name__}: {str(e)}")
            raise HTTPException(status_code=404, detail=str(e))

        except DuplicateKeyError as e:
            # MongoDB unique index violation
            logger.error(f"DuplicateKeyError in {func.__name__}: {str(e)}")
            raise HTTPException(status_code=409, detail="Duplicate key error: resource already exists")

        except HTTPException as e:
            # If any part of your code already raised HTTPException, just re-raise it
            raise e

        except Exception as e:
            # Unknown/unhandled errors
            logger.exception(f"Unhandled exception in {func.__name__}: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    return wrapper