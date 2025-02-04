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
