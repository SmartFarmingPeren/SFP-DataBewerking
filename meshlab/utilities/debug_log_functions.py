import logging

from termcolor import colored

from utilities.configuration_file import *

# Create a log file to save errors.
logging.basicConfig(filename=OUTPUT_LOG_DIR + LOG_FILE_NAME, level=logging.DEBUG, filemode='w+',
                    format='%(asctime)s - %(name)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


def debug_message(message):
    """
    This function prints a green tag with the text [Debug] in front of a message.
    This message will be logged to a log file named code_logging.log.
    :param message: a message.
    """
    print(colored('[Debug] ', 'green'), message)
    logging.debug(message)


def info_message(message):
    """
    This function prints a megenta tag with the text [Info] in front of a message.
    This message will be logged to a log file named code_logging.log.
    :param message: a message.
    """
    print(colored('[Info] ', 'magenta'), message)
    logging.info(message)


def error_message(message):
    """
    This function prints a red tag with the text [Error] in front of a message.
    This message will be logged to a log file named code_logging.log.
    :param message: a message.
    """
    print(colored('[Error] ', 'red'), message)
    logging.error(message)


def warning_message(message):
    """
    This function prints a yellow tag with the text [Warning] in front of a message.
    This message will be logged to a log file named code_logging.log.
    :param message: a message.
    """
    print(colored('[Warning] ', 'yellow'), message)
    logging.warning(message)
