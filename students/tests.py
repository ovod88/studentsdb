from django.test import TestCase

# Create your tests here.

import logging


# logger = logging.getLogger(__name__)

# logger.setLevel(logging.DEBUG)

# ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)

# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# ch.setFormatter(formatter)

# logger.addHandler(ch)

# logger.debug('debug повідомлення')
# logger.info('info повідомлення')
# logger.warn('warn повідомлення')
# logger.error('error повідомлення')
# logger.critical('critical повідомлення')

try:
	open('/path/to/file/does/not/exist', 'rb')
except Exception as e:
	logging.error('Failed to open file', exc_info=True)