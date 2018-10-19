from django.core.management.base import BaseCommand
from students.models.students import Student
from students.models.groups import Group
from django.contrib.auth.models import User

class Command(BaseCommand):
	args = '<model_name model_name ...>'
	help = "Prints to console number of student related objects in a database."

	models = (('student', Student), ('group', Group), ('user', User))

	def add_arguments(self, parser):
		parser.add_argument('objects_name', nargs='+', type=str)

	def handle(self, *args, **options):
		# if options['student']:
		# 	self.stdout.write('Number of students in database: %d' %
		# 			Student.students.count())
		objects_name = options['objects_name']
		for name, model in self.models:
			if name in objects_name:
				self.stdout.write('Number of %ss in database: %d' %
					(name, model.objects.count()))