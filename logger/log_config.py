# import logging
# from loguru import logger

# logger.add("application.log", rotation="500 MB", compression="zip", level="INFO")

# # Optionally, you can add custom handlers here, for instance, to send logs to a file, database, or monitoring system.


import logging

logger = logging.getLogger("intern_app")
logger.setLevel(logging.INFO)

# Creating file handler
file_handler = logging.FileHandler("application.log")
file_handler.setLevel(logging.INFO)

# Creating formatter and adding it to the file handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Adding file handler to logger
logger.addHandler(file_handler)
