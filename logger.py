import logging
from logging.handlers import RotatingFileHandler
import os
import shutil
import sys
import constants
shutil.rmtree('logs', ignore_errors=True)
os.makedirs(constants.LOG_DIR, exist_ok=True)

def init_logger(debug=False):
    log = logging.getLogger('main')
    if debug:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)
    rotate = logging.handlers.RotatingFileHandler(os.path.join(constants.LOG_DIR, 'log.log'), maxBytes=10000000,
                                                          encoding='utf-8', backupCount=2)
    consoleHandler = logging.StreamHandler(sys.stdout)
    _form = "[%(asctime)s] [%(levelname)8s] (%(filename)s:%(lineno)s)--- %(message)s"
    _form_console = "[%(asctime)s] [%(levelname)8s] :  %(message)s"
    rotate.setFormatter(logging.Formatter(_form))
    consoleHandler.setFormatter(logging.Formatter(_form_console))
    log.addHandler(rotate)
    log.addHandler(consoleHandler)
    log.info(f"Start bot. Version {constants.VERSION}")
