from utilities.configuration_file import *
import logging
from termcolor import colored

# Create a log file to save errors.
logging.basicConfig(filename=OUTPUT_LOG_DIR + 'code_logging.log', level=logging.DEBUG, filemode='w+',
                    format='%(asctime)s - %(name)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


def debug_message(message):
    print(colored('[Debug] ', 'green'), message)
    logging.debug(message)


def info_message(message):
    print(colored('[Info] ', 'magenta'), message)
    logging.info(message)


def error_message(message):
    print(colored('[Error] ', 'red'), message)
    logging.error(message)


def warning_message(message):
    print(colored('[Warning] ', 'yellow'), message)
    logging.warning(message)
