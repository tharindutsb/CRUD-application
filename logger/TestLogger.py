# import logging
# from loguru import logger

# logger.add("application.log", rotation="500 MB", compression="zip", level="INFO")

# # Optionally, you can add custom handlers here, for instance, to send logs to a file, database, or monitoring system.


# import logging

# # Define log file location
# LOG_FILE = "application.log"
# # Configure logging
# logging.basicConfig(
#     level=logging.INFO,  # Change to INFO to reduce unnecessary debug logs
#     format="%(asctime)s - %(name)s - %(levelname)s - %(filename)s - line %(lineno)d - %(message)s",
    
    
#     # format="%(asctime)s - %(levelname)s - %(message)s",
#     handlers=[
#         logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8"),  # Log to file
#         logging.StreamHandler()  # Log to console
#     ]
# )

# logger = logging.getLogger("intern_app")  # Use a consistent logger name

# logger.info("Logging system initialized successfully!")


import logging
from logging import config
import os
# logging.config.fileConfig('logging.ini')

# Get the absolute path of the logging.ini file
log_config_path = os.path.join(os.path.dirname(__file__), 'logging.ini')

# Load logging configuration
logging.config.fileConfig(log_config_path)

logger1 = logging.getLogger('name1')
logger2 = logging.getLogger('name2')

logger1.debug('This is logger1')
logger2.info('This is logger2')
logger1.warning('This is logger1')
logger1.error('This is logger1')
logger2.warning('This is logger2')
logger2.error('This is logger2')