import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    """ Configures the logging system for the application.
     Sets up the root logger to log messages to both a rotating file and the console with a specific format.
     """

    # Get the root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Log message format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # File handler with log rotation
    file_handler = RotatingFileHandler('app.log', maxBytes=10_000_000, backupCount=5)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
