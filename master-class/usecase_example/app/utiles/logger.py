import logging
from logging.handlers import RotatingFileHandler  # For controlling the log file size and reusing it.

def get_logger(name):
    # Get a logger instance with the specified name.
    # if it already exists, it will return the same logger.
    logger = logging.getLogger(name)

    # set the minimum log level to INFO (ignores DEBUG,but logs INFO and above).
    logger.setLevel(logging.INFO)

    #Prevent adding handlers multiple times (common when get_logger is called repeatedly).

    if not logger.handlers:
        #define the log message format.
        formatter = logging.Formatter(
             "%(asctime)s - %(name)s - %(levelname)s - %(threadName)s - %(message)s"
        )

        file_handlers = RotatingFileHandler(
            "usecase.log",maxBytes=100_000_00,backupCount=10,encoding="utf-8"
        )

        file_handlers.setFormatter(formatter) # Apply the formatter to the file handler

        # stream handler (console output)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        # Attach both handlers to the logger
        logger.addHandler(file_handlers)
        logger.addHandler(stream_handler)

    #Return the configured to the logger
    return logger