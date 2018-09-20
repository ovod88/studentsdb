import logging
import json
import datetime
from ..settings import BASE_DIR
from os.path import basename, relpath, normpath
import os

class RelativePathFormatter(logging.Formatter):
	# pass
	data ={}

	# def __init__(self):
 #        super(RelativePathFormatter, self).__init__()

	def format(self, record):

		# super().format(record)
		record.message = record.getMessage()
		record.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		name_arr = record.name.split('.')

		if len(name_arr) == 1 and name_arr[0] == 'django':
			path_str = str(relpath(normpath(record.pathname), BASE_DIR)).split('.')[:-1][0]
			path_str = path_str.replace(os.sep, '.')

			record.module = path_str
			# print(str(os.path.basename(os.path.relpath(os.path.normpath(record.pathname), BASE_DIR))).replace(os.sep, '.'))

		# print(record.__dict__)
		return super().formatMessage(record)

	# # 	return super(RelativePathFormatter, self).format(record)
	# 	# print(record)
	# 	# record.message = record.getMessage()
	# 	# input_data = {}
	# 	# input_data['@timestamp'] = datetime.utcnow().isoformat()[:-3] + 'Z'
	# 	# input_data['level'] = record.levelname

	# 	# if record.message:
	# 	#     input_data['message'] = record.message

	# 	# input_data.update(self.data)
	# 	# return json.dumps(input_data)