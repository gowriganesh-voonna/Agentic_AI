import json
import os
from app.utiles.loggers import get_logger
from fastapi import HTTPException
from app.utiles.decoratores import handle_exceptions

logger = get_logger(__name__)



@handle_exceptions
def load_json(File_path):

    if not os.path.exists(File_path):
        return []
    
    with open(File_path,"r") as f:
        try:

            content = f.read().strip()

            if not content:
                return []
            return json.loads(content)
        
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error : {str(e)}")
            return []
        

def save_json(File_path,data):
    try:
        with open(File_path,"w") as f:
            json.dump(data,f,indent=4)
    except Exception as e:
        logger.error(f"Error saving books: {str(e)}")
        raise HTTPException(status_code=500,detail ="Failed to save data")
    
