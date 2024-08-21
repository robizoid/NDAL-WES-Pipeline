import logging

def setup_logging(log_file):
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(message)s')

def log_message(message):
    logging.info(message)

