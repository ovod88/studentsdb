import logging
import datetime
import pytz
from ..settings import TIME_ZONE

class LogDatabaseHandler(logging.Handler):

	def emit(self, record):
		
		data = {}
		logger = logging.getLogger('django')

		try:
			from students.models.logentry import LogEntry
			from ..utils import getMobuleProjectPath

			data['message'] = record.getMessage()
			data['date'] = datetime.datetime.now(pytz.timezone(TIME_ZONE))
			data['module'] = getMobuleProjectPath(record.pathname)
			data['log_level'] = record.levelname
			print(data['date'])
		except Exception as e:
			logger.exception('Error occured', exc_info=True)

		try:
			log = LogEntry(**data)
			log.save()
		except Exception as e:
			logger.exception(e, exc_info=True)

