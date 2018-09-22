import logging
import datetime
from ..utils import getMobuleProjectPath
import traceback
import sys

class RelativePathFormatter(logging.Formatter):
	# pass
	# data ={}

	# def __init__(self):
 #        super(RelativePathFormatter, self).__init__()

	def format(self, record):

		# super().format(record)
		record.message = record.getMessage()
		record.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		name_arr = record.name.split('.')

		if len(name_arr) == 1 and (name_arr[0] == 'django' or name_arr[0] == 'database'):
			record.module = getMobuleProjectPath(record.pathname)
			# print(str(os.path.basename(os.path.relpath(os.path.normpath(record.pathname), BASE_DIR))).replace(os.sep, '.'))

		if record.exc_info is not None:
			record.exc_data = '\n'.join(traceback.format_tb(record.exc_info[2])) + str(record.exc_info[1])
		else:
			record.exc_data = ''

		return super().formatMessage(record)
