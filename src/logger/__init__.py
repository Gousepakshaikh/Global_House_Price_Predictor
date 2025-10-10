import logging
import os 
from logging.handlers import RotatingFileHandler
from from_root import from_root
from datetime import datetime

log_dir="logs"
log_file=f"{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.log"
max_log_size=5*1024*1024 
backup_count=3

log_dir_path=os.path.join(from_root(),log_dir)
os.makedirs(log_dir_path,exist_ok=True)
log_file_path=os.path.join(log_dir_path,log_file)

def configure_logger():
    '''
    configures logging with rotating file handler and a console handler
    '''

    logger=logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter=logging.Formatter("[%(asctime)s] - %(name)s - %(levelname)s - %(message)s",datefmt='%d_%m_%Y_%H_%M_%S')


    file_handler=RotatingFileHandler(log_file_path,maxBytes=max_log_size,backupCount=backup_count)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler=logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

configure_logger()



