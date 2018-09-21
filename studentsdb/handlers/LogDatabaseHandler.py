import logging
import datetime
import pytz
from ..settings import TIME_ZONE
from ..utils import getMobuleProjectPath

class LogDatabaseHandler(logging.Handler):

	def __init__(self, model_name=''):
		super().__init__()
		self.model_name = model_name

	def emit(self, record):
		
		data = {}
		logger = logging.getLogger('django')


		try:
			model = self.get_model(self.model_name)
		except Exception as e:
			from students.models.logentry import LogEntry as model

			data['message'] = record.getMessage()
			data['date'] = datetime.datetime.now(pytz.timezone(TIME_ZONE))
			data['module'] = getMobuleProjectPath(record.pathname)
			data['log_level'] = record.levelname
		# print(data['date'])



		try:
			log = model(**data)
			log.save()
		except Exception as e:
			logger.exception(e, exc_info=True)

	def get_model(self, name):
		names = name.split('.')
		mod = __import__('.'.join(names[:-1]), fromlist=names[-1:])

		return getattr(mod, names[-1])