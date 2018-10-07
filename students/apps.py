from django.apps import AppConfig


class StudentsAppConfig(AppConfig):
	name = 'students'
	verbose_name = u'База Студентів'


	def ready(self):
		from . import receivers
