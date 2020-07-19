import os
import json
import inspect
import logging
from logging.handlers import RotatingFileHandler

def logger():
    '''
    Creates a logger instance with the propper format, terminal and file handlers.
    When the main log file reaches its file byte size, it will dump its contents
    onto the next backup log file (if backupFileCount > 0)

    OS environment parameters:
        LOG_FILE_PATHNAME     (str): The pathname of the log file where the logs will be written
        BACKUP_LOG_FILE_COUNT (str): The number of backup log files that will be created (cached log files)
        LOG_FILE_BYTE_SIZE    (str): The total number of bytes that the log files can reach before being purged

    Returns:
        logging (object): A logger object with a custom formatter and log handlers
    '''
    
    # create logger
    logger = logging.getLogger('')
    logger.setLevel(logging.INFO)

    # create formatter - this formats the log messages accordingly
    formatter = logging.Formatter(json.dumps({
        'time': '%(asctime)s',
        'pathname': '%(pathname)s',
        'line': '%(lineno)d',
        'logLevel': '%(levelname)s',
        'message': '%(message)s'
    }))

    # create rotating file handler and set level to info
    fhandler = RotatingFileHandler(
        os.environ['LOG_FILE_PATHNAME'], 
        maxBytes=int(os.environ['LOG_FILE_BYTE_SIZE']), 
        backupCount=int(os.environ['BACKUP_LOG_FILE_COUNT'])
    )
    
    fhandler.setLevel(logging.INFO)
    # add formatter to file handler
    fhandler.setFormatter(formatter)

    # create console handler and set level to debug
    chandler = logging.StreamHandler()
    chandler.setLevel(logging.INFO)
    # add formatter to console handler
    chandler.setFormatter(formatter)

    # add handlers to logger
    logger.addHandler(fhandler)
    logger.addHandler(chandler)

    return logger

# singleton logger instance
log = logger()