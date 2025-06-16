# This is normal baisc code for loggers which will only stored in log file and endlessly log
# file size will be increased.
# import logging

# def get_logger(name):
#     logging.basicConfig(
#         filename="bank_api.log",
#         level= logging.INFO,
#         format= "%(asctime)s - %(levelname)s - %(threadname)s - %(message)s"
#     )

#     return logging.getLogger(name)

# Another approach for better  debuging added console log and file log with optimized way.

import logging
from logging.handlers  import RotatingFileHandler  # For controlling the log file size and reusing it.

def get_logger(name):
    # Get a logger instance with the specified name.
    # If it already exists, it will return the same logger.
    logger = logging.getLogger(name)
    
    # Set the minimum log level to INFO (ignores DEBUG, but logs INFO and above).
    logger.setLevel(logging.INFO)

    # Prevent adding handlers multiple times (common when get_logger is called repeatedly).
    if not logger.handlers:
        # Define the log message format.
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(threadName)s - %(message)s"
        )

        # Create a rotating file handler:
        # - Logs go to 'bank_api.log'
        # - Rotates the file after it reaches 100,000 bytes (about 100KB)
        # - Keeps up to 7 backup log files (bank_api.log.1, bank_api.log.2, ..., bank_api.log.7)
        file_handlers = RotatingFileHandler(
            "bank_api.log", maxBytes=100_000_00, backupCount=10 , encoding='utf-8'
        )
        file_handlers.setFormatter(formatter)  # Apply the formatter to the file handler

        # Create a console handler to also log to the terminal
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)  # Apply the same formatter to console logs

        # Attach both handlers to the logger
        logger.addHandler(file_handlers)
        logger.addHandler(console_handler)

    # Return the configured logger
    return logger

