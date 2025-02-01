from logger.loggers import get_logger
logger = get_logger("API_NO")

def log_messages():
    """Logs messages at different levels."""

    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")

if __name__ == "__main__":
    log_messages()
