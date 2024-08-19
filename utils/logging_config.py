import logging
import os

def setup_logging(log_directory):
    """Set up logging to file located in log_directory."""
    os.makedirs(log_directory, exist_ok=True)  # Ensure log directory exists

    # Create logger
    logger = logging.getLogger('GenomicPipeline')
    logger.setLevel(logging.DEBUG)
    logger.handlers = []  # Clear existing handlers

    # Create file handler and set level to debug
    log_file = os.path.join(log_directory, 'pipeline.log')
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)

    # Add file handler to logger
    logger.addHandler(file_handler)

    return logger
