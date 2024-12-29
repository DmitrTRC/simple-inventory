import logging
from logging.handlers import RotatingFileHandler


class LogColors:
    """ANSI escape sequences for colors"""
    BLUE = '\033[0;34m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD_RED = '\033[1;91m'
    RESET = '\033[0m'


class ColorFormatter(logging.Formatter):
    """Custom formatter to add colors based on log level."""
    LEVEL_COLORS = {
        logging.DEBUG: LogColors.BLUE,
        logging.INFO: LogColors.BLUE,
        logging.WARNING: LogColors.YELLOW,
        logging.ERROR: LogColors.RED,
        logging.CRITICAL: LogColors.BOLD_RED
    }

    def format(self, record):
        color = self.LEVEL_COLORS.get(record.levelno, LogColors.RESET)
        record.msg = f'{color}{record.msg}{LogColors.RESET}'
        return super().format(record)


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
    console_handler.setFormatter(ColorFormatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    ))
    logger.addHandler(console_handler)
