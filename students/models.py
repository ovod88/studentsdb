from django.db import models

# Create your models here.

class TicketIntManager(models.Manager):
	def all_with_ticket_sorted(self, reverse):
		students = self.get_queryset()

		def ticket_sorting(student):
			return int(student.ticket)

		return sorted(students, key=ticket_sorting, reverse=reverse)
		
class Student(models.Model):

	class Meta(object):
		verbose_name=u"Студент"
		verbose_name_plural = u"Студенти"

	first_name = models.CharField(
		max_length=256,
		blank=False,
		verbose_name=u"Ім'я")

	last_name = models.CharField(
		max_length=256,
		blank=False,
		verbose_name=u"Прізвище")

	middle_name = models.CharField(
 		max_length=256,
 		blank=True,
		verbose_name=u"По-батькові",
		default='')

	birthday = models.DateField(
		blank=False,
		verbose_name=u"Дата народження",
		null=True)

	photo = models.ImageField(
 		blank=True,
		verbose_name=u"Фото",
 		null=True)

	ticket = models.CharField(
		max_length=256,
		blank=False,
		verbose_name=u"Білет")

	notes = models.TextField(
		blank=True,
		verbose_name=u"Додаткові нотатки")

	def __str__(self):
		return "{},{},{}".format(self.first_name, self.last_name, self.ticket)

	#JUST TO TEST TICKET SORTING BY CLASSMETHOD
	@classmethod
	def ticket_int(cls):
		return [int(s.ticket) for s in cls.students.all()]

	def get_ticket_int(self):
		return int(self.ticket)

	#JUST TO TEST CUSTOM DEFAULT MANAGER NAME
	# students=models.Manager()

	#JUST TASTE CUSTOM MANAGER WITH TICKET INT CONVERSION
	students = TicketIntManager()