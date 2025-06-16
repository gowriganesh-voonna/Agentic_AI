import json
import os
import logging

#Logger configuration
logger=logging.getLogger("emp_logger")
logger.setLevel(logging.DEBUG)
logger.propagate = True
log_dir=os.path.join(os.path.dirname(__file__),"..","logs")

os.makedirs(log_dir,exist_ok=True)   # Creates logs if it doesnt exists

log_file=os.path.join(log_dir,"action.log")
file_handler=logging.FileHandler(log_file)    #This line creates a file handler that will write log messages to a file specified by log_file.
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s | %(levelname)s | %(module)s | %(funcName)s | line:%(lineno)d | %(message)s'
))


if not logger.handlers:
    logger.addHandler(file_handler)    #May be addHandler
def save_to_file(data,file):
    """It will save list of dictionaries"""
    try:
        with open(file,"w") as f:
            print("saved ")
            json.dump(data,f,indent=4)
        logger.info(f"saved the data into the {file}")
    except Exception as e:
        logger.exception(f"Failed to save {file} due to {e}")



def load_from_json(file):
    """load and return list of dictionaries from a json file"""
    try:
        if not os.path.exists(file):
            print("Not their")
            logger.warning(f"File not found {file} returning an empty list")
            return []
        with open(file,"r") as f:
            print("With open")
            logger.info(f"Loaded data from the Json file { file}")
            print("Load_from_json")
            return json.load(f)
    except Exception as e:
        logger.exception(f"unable to load the file {file}")
        print("Exception")
        return []
